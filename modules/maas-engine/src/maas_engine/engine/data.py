"""base class for engine"""

import abc
import dataclasses
import logging
import time
import typing

from typing import ClassVar, Dict, Iterator, List, Type

from opensearchpy.connection.connections import connections as db_connections
from opensearchpy.helpers import parallel_bulk

import maas_model
from maas_engine.engine.base import Engine, EngineReport
from maas_engine.exceptions import CannotProcessMessageException, HandleMessageException


@dataclasses.dataclass
class DataEngineStatistics:
    """Store statistics about an data engine run"""

    logger: logging.Logger

    created: int = 0

    updated: int = 0

    deleted: int = 0

    errors: int = 0

    conflicts: int = 0

    start_timestamp: float = dataclasses.field(default_factory=time.time, init=True)

    end_timestamp: float = dataclasses.field(default_factory=time.time, init=True)

    @property
    def duration(self) -> float:
        """get the run duration

        Returns:
            float: time in seconds
        """
        return self.end_timestamp - self.start_timestamp

    def update(self, details):
        """populate stats from responses to bulk actions"""
        result = details["result"]

        document_id = details["_id"]

        if result == "created":
            self.created += 1
            self.logger.debug("Created %s id: %s ", details, document_id)

        elif result == "updated":
            self.updated += 1
            self.logger.debug("Updated %s id: %s", details, document_id)

        elif result == "deleted":
            self.deleted += 1
            self.logger.debug("Deleted %s id: %s", details, document_id)

        else:
            self.errors += 1
            self.logger.error("Unexpected result: %s", result)

    def finish(self):
        """set end_timestamp to now and log overall stats"""
        self.end_timestamp = time.time()

        self.logger.info(
            "%d created, %d updated, %d deleted, %d errors, %d conflicts in %.3fs",
            self.created,
            self.updated,
            self.deleted,
            self.errors - self.conflicts,
            self.conflicts,
            self.duration,
        )

    @staticmethod
    def get_details(info) -> dict:
        """extract details dict from opensearch response info"""

        # find the right key in info dict
        for op_type in ("create", "update", "delete", "index"):
            if op_type in info:
                return info[op_type]
        # unhandled operation type
        return None


class DataEngine(Engine):
    """

    Base class for data engine that deserializes documents contained in payload and
    writes back data by exposing the action_iterator() abstract method.
    """

    # a map storing association between elastic search bulk result and maas data action
    ES_MAAS_ACTION_MAP: ClassVar[Dict[str, maas_model.DataAction]] = {
        "created": maas_model.DataAction.NEW,
        "updated": maas_model.DataAction.UPDATE,
        "deleted": maas_model.DataAction.DELETE,
    }

    def __init__(self, args=None, send_reports=True, chunk_size=0):
        super().__init__(args, send_reports=send_reports, chunk_size=chunk_size)

        # store raw dsl class, updated by payload
        self.input_model = None

        # as bulk action is fed with action dictionnaries, link to DAO is lost.
        # this dict (index_name, id) => DAO store this link for report generation
        self._index_id_document_map = {}

        # a dict storing report data like { "ClassName": {"Action": [id1, id2]} }
        # to generate final reports
        self._report_data = {}

        # store data statistics
        self._stats = None

    @property
    def input_documents(self) -> typing.List[maas_model.MAASDocument]:
        """
        Property that alias input document contained in the session

        Returns:
            typing.List[maas_model.MAASDocument]: deserialize input documents
        """
        return self.session.get("input_documents")

    @input_documents.setter
    def input_documents(self, value: typing.List[maas_model.MAASDocument]):
        """
        property setter of the input documents

        Args:
            value (typing.List[maas_model.MAASDocument]): input documents
        """
        self.session.put("input_documents", value)

    def run(
        self, routing_key: str, payload: maas_model.MAASMessage
    ) -> Iterator[EngineReport]:
        """overide"""
        # initialize input lazily
        if not self.input_documents:
            self._load_input_documents(payload, routing_key)
        else:
            self.logger.debug("Won't load input documents: reuse from session")

        # store time info for performance logging
        self._stats = DataEngineStatistics(logger=self.logger)

        error_msg = ""

        for success, info in parallel_bulk(
            db_connections.get_connection(),
            self.action_iterator(),
            refresh=True,  # TODO set refresh as engine option
            raise_on_error=False,
            raise_on_exception=False,
            request_timeout=self.args.es_timeout if self.args else 120,
        ):
            # store the action specific dict feedback
            details = self._stats.get_details(info)

            if not details:
                self.logger.warning("Unhandled bulk info: %s", info)
                continue

            if not success:
                self._stats.errors += 1

                status = details.get("status", 500)

                if status == 409:
                    self._stats.conflicts += 1
                    self.logger.info("Conflict detected: %s", info)
                else:
                    self.logger.error("Error pushing to database: %s", info)
                    error_msg += f"{info} "
                continue

            self._stats.update(details)

            if self.send_reports:
                self._handle_es_result_for_report(details)

        self._stats.finish()

        if self._stats.errors and self._stats.conflicts != self._stats.errors:
            # in some cases, database can encounter errors that can be solved
            # by requeuing the message. Rejecting the message is not supposed to happen
            # if validation process covers the data related issues, like wrong types
            # however, the es_reject_errors cli argument allows rejection so engine
            # can restart and drop faulty message loop

            error_class: Type[Exception]

            if self.args and self.args.es_reject_errors:
                # reject message if all errors are not conflicts
                error_class = CannotProcessMessageException
            else:
                error_class = HandleMessageException

            raise error_class(f"{self.__class__.__name__}: {error_msg}")

        if self._stats.conflicts:
            # only conflicts happened, will requeue
            raise HandleMessageException(
                f"{self.__class__.__name__}: "
                + f"{self._stats.conflicts} conflicts occured"
            )

        # generate all the reports for bus messenging
        for report in self._generate_reports():
            self.reports.append(report)
            yield report

    def _load_input_documents(
        self, payload: maas_model.MAASMessage, routing_key: str = ""
    ):
        """Populate input_model and input_documents attributes

        Args:
            payload (maas_model.MAASMessage): message payload
        """
        self.logger.debug("Loading input documents")
        # get source model from payload
        self.input_model = self.get_input_model(payload)

        # load all documents, as a list to check all are present and log a meaningful
        # message if some are missing.
        # as all documents are already retrieved by the underlying execute() and not
        # scan(), there is no real memory impact.
        #
        # put the list in a class cache so a sequence of engine won't reload
        # at each run() call. Note that this cache shall be cleared at the end of the
        # execution sequence
        # child classes will have to use report() method to explicitly tell a document
        # modification is notified on the amqp bus
        self.input_documents = self.get_input_documents(payload)

        if not all(self.input_documents):
            # this is really bad: raw documents have been deleted since the payload
            # have been sent, or the document class or identifiers are wrong !
            missing = set(payload.document_ids) - {
                document.meta.id for document in self.input_documents if document
            }

            self.logger.critical(
                "Some input documents %s on queue %s are missing: %s",
                self.input_model,
                routing_key,
                missing,
            )

            if self.args.es_requeue_missing_input:
                raise HandleMessageException(
                    f"{self.__class__.__name__}:Missing {self.input_model.__name__} "
                    f"on {routing_key}:{missing}"
                )

            # purify the input
            self.input_documents = [
                document for document in self.input_documents if document
            ]

    def _push_report_data(self, document, es_result):
        """store the db result for a document for later report generation"""
        document_classname = self.get_report_document_classname(document)

        if document_classname not in self._report_data:
            self._report_data[document_classname] = {}

        if es_result not in self._report_data[document_classname]:
            self._report_data[document_classname][es_result] = []

        self._report_data[document_classname][es_result].append(document)

    def _generate_reports(self) -> Iterator[EngineReport]:
        """Generate reports from the stored database search result


        Yields:
            Iterator[EngineReport]: EngineReport
        """

        for classname, es_result_dict in self._report_data.items():
            for es_result, all_documents in es_result_dict.items():
                # group documents
                action_documents = {}

                for document in all_documents:
                    action = self.get_report_action(es_result, document)

                    if not action:
                        # won't send report
                        continue

                    if action not in action_documents:
                        action_documents[action] = [document]
                    else:
                        action_documents[action].append(document)

                for action, documents in action_documents.items():
                    yield from self.report_strategy(classname, action, documents)
                   

    def report_strategy(self, classname, action, documents):
        """Default strategy to make report """
        yield EngineReport(
            action,
            [document.meta.id for document in documents],
            document_class=classname,
            chunk_size=self.chunk_size,
            document_indices=self.get_index_names(documents),
        )

    @staticmethod
    def get_index_names(documents: list[maas_model.MAASDocument]) -> list[str]:
        """Return the names of indices, without duplicates, from a list of documents

        Args:
            documents (list[maas_model.MAASDocument]): documents

        Returns:
            list[str]: list of index names
        """
        return list(set(document.partition_index_name for document in documents))

    def report(self, document: maas_model.MAASDocument):
        """Tell the engine to report the action on this document for later use in bulk.

        This is mandatory to maintain the link between object and dictionnaries
        generated by action iterator.

        Args:
            document (MAASDocument): document to report
        """
        self._index_id_document_map[
            (document.partition_index_name, document.meta.id)
        ] = document

    def get_report_document_classname(self, document: maas_model.MAASDocument) -> str:
        """Allow customization of document class in reports for subclasses.

        Args:
            document (maas_model.MAASDocument): document

        Returns:
            str: the document class name for message
        """
        return document.__class__.__name__

    def get_report_action(
        self, es_result: str, document: maas_model.MAASDocument
    ) -> str:
        """
        Get the report action (i.e. routing key for message). Override this in
        subclasses so routing key can be choosen not only from the index but with
        additional business logic, like mission, satellite, etc.

        Returning None will omit the document from reporting.

        Args:
            es_result (str): database status string (created, updated, deleted)
            document (maas_model.MAASDocument): document to report

        Returns:
            str: action string, typically new.index-name
        """
        return f"{self.ES_MAAS_ACTION_MAP[es_result].value}.{document.Index.name}"

    def get_input_model(self, message: maas_model.MAASMessage):
        """Get the model class from the message. Can be overriden for custom behaviour

        Args:
            message (maas_model.MAASMessage): input message

        Returns:
            class: Model DAO class
        """
        return self.get_model(message.document_class)

    def get_input_documents(
        self, message: maas_model.MAASMessage
    ) -> List[maas_model.MAASDocument]:
        """Get the input documents. Can be overriden for custom behaviour

        Args:
            message (maas_model.MAASMessage): input message

        Returns:
            list[maas_model.MAASDocument]: input documents
        """
        if self.input_model:
            if result := self.input_model.mget_by_ids(
                message.document_ids, message.document_indices
            ):
                return list(iter(result))
            return []

        raise ValueError("No Input Model Class")

    def shall_report(self, _: maas_model.MAASDocument) -> bool:
        """
        Method to include or exclude some documents from reporting on the bus.

        Defaults to True

        Args:
            document (maas_model.MAASDocument): document to inspect

        Returns:
            bool: True if document is to report on the bus.
        """
        return True

    # pylint: enable=unused-argument,no-self-use

    def _handle_es_result_for_report(self, details: dict):
        """Decide to report or not document on the bus.

        Children classes shall override shall_report() for business logic implementation
        (mission, product type, etc)

        Args:
            details (dict): Elastic search result details dict
        """

        # retrieve the document object based on status information
        document = self._index_id_document_map.get((details["_index"], details["_id"]))

        if not document:
            self.logger.debug(
                "Document not found in local map: won't send report for %s",
                details,
            )
            return

        if self.shall_report(document):
            self._push_report_data(document, details["result"])

        else:
            self.logger.debug(
                "shall_report() returned False: no report sent on the bus for %s",
                details,
            )

    @abc.abstractmethod
    def action_iterator(self) -> typing.Iterator[dict]:
        """
        Iterator to feed the bulk by yielding action dictionnaries
        """
        raise NotImplementedError()
