"""Basic raw data engine for one-to-one consolidation"""
from typing import Any, Callable, Dict, Iterator, List, Type

from opensearchpy.exceptions import OpenSearchException

from maas_model import MAASRawDocument, MAASDocument, datestr_to_utc_datetime

from maas_engine.engine.data import DataEngine


class RawDataEngine(DataEngine):
    """

    A consolidation engine for basic consolidation needs: one input document is
    consolidated in one output document.

    Target document class is configured by the CONSOLIDATED_MODEL class attribute that
    is expected to hold a MAASDocument
    """

    # target model class for consolidation
    CONSOLIDATED_MODEL: Type[MAASDocument] = MAASDocument

    def __init__(self, args=None, send_reports=True, min_doi=None, chunk_size=0):
        """constructor

        Args:
            args (namespace, optional): command line arguments. Defaults to None.
            send_reports (bool, optional): publish messages. Defaults to True.
            min_doi (str, optional): minimum value for the date of interest of a
                consolidated document. This allow to exclude too old document to
                consolidate. Defaults to None.
        """
        super().__init__(args, send_reports=send_reports, chunk_size=chunk_size)

        # minimum date of interest. Note datestr_to_zulu returns None if min_doi is None
        self.min_doi = datestr_to_utc_datetime(min_doi)

        self.initial_state_dict = {}

        self.consolidated_documents = []

        # store output entities to avoid conflict when a message contains several inputs
        # that consolidate the same document
        self._output_cache = {}

    def get_consolidated_id(self, raw_document: MAASRawDocument) -> str:
        """return the id of the consolidated document from a raw document

        Args:
            raw_document (MAASRawDocument): a raw document

        Raises:
            NotImplementedError: because this is an abstract method

        Returns:
            str: consolidted document identifier
        """
        raise NotImplementedError()

    def consolidate(
        self,
        raw_document: MAASRawDocument,
        document: MAASDocument,
    ) -> MAASDocument:
        """
        Template method for default consolidation. It is not decorated as an abstract
        method because of the duck typing approach of get_consolidation_method()


        Args:
            raw_document (MAASRawDocument): raw document
            document (MAASDocument): consolidated document instance of
                CONSOLIDATED_MODEL

        Raises:
            NotImplementedError: if not implemented

        Returns:
            MAASDocument: consolidated document
        """
        raise NotImplementedError()

    def _find_method_by_document_class(
        self, prefix, document_class, default_method
    ) -> Callable:
        """Get the adequate function depending a document class used for consolidated
        identifier generation and consolidate method, providing optionnal routing by
        document class.

        Default is self.consolidate() but routing depending the input data type is
        possible by implementing method with a naming consolidate_from_ suffixed by
        the document class name like:

            self.consolidate_from_SomeDocument()

        This can be useful to limitate the number of Engine classes that has little
        changes between consolidation method / identifier generation.

        Note that is an example of Duck Typing ;)

        Returns:
            typing.Callable: adequate method or default
        """

        # default consolidation method
        method = default_method

        # model-specific consolidation method
        spec_func_name = f"{prefix}{document_class}"

        if hasattr(self, spec_func_name):
            spec_func = getattr(self, spec_func_name)

            # usability check
            if callable(spec_func):
                self.logger.debug("Found specific function %s", spec_func_name)
                method = spec_func

            elif spec_func:
                # may be raise an exception
                self.logger.warning("%s is not callable")

        return method

    def get_consolidation_method(self) -> Callable:
        """
        get the consolidation method depending the document class in the payload
        """
        return self._find_method_by_document_class(
            "consolidate_from_", self.payload.document_class, self.consolidate
        )

    def get_consolidated_id_method(self) -> Callable:
        """get the consolidation identifier generation depending the document class
        in the payload

        Returns:
            typing.Callable: consolidated identifier method
        """
        return self._find_method_by_document_class(
            "get_consolidated_id_from_",
            self.payload.document_class,
            self.get_consolidated_id,
        )

    def get_consolidated_documents(self) -> list[MAASDocument]:
        """Get or create the target documents for a one-to-one consolidation."""

        # get the specific method to compute consolidated document identifiers
        get_consolidated_id_method = self.get_consolidated_id_method()

        # associate raw document identifiers with consolidated document identifiers
        input_output_dict = {
            raw_document.meta.id: get_consolidated_id_method(raw_document)
            for raw_document in self.input_documents
        }

        # create a list of document consolidated identifiers without duplicates
        unique_consolidated_ids = list(dict.fromkeys(input_output_dict.values()))

        extra_args = {}

        # disable assignment-from-no-return as it's a template method
        # pylint: disable=assignment-from-no-return
        consolidated_indices = self.get_consolidated_indices()
        # pylint: enable=assignment-from-no-return

        if consolidated_indices:
            extra_args["document_indices"] = consolidated_indices

        output_dict = {}

        for document_id, document in zip(
            unique_consolidated_ids,
            self.CONSOLIDATED_MODEL.mget_by_ids(
                unique_consolidated_ids,
                ignore_missing_index=True,
                log_missing=False,
                **extra_args,
            ),
        ):
            if document is None:
                document = self.CONSOLIDATED_MODEL()
                document.meta.id = document_id

            output_dict[document_id] = document

        # return the list of document instances that matches the raw document
        # identifiers. In a way that raw data matching the consolidated documents
        # will get the same consolitdated instance
        return [output_dict[document_id] for document_id in input_output_dict.values()]

    def get_consolidated_indices(self) -> List[str]:
        """
        Template method to specify the indices where consolidated documents are stored

        Returns:
            list[str]: A list of index names
        """
        return []

    def action_iterator(self) -> Iterator[Dict[str, Any]]:
        """elastic search bulk actions generator"""

        self.on_pre_consolidate()

        methodobj = self.get_consolidation_method()

        consolidated_documents = self.get_consolidated_documents()

        self.populate_initial_state(consolidated_documents)

        for raw_document, document in zip(
            self.input_documents,
            consolidated_documents,
        ):
            self._consolidate(methodobj, raw_document, document)

        # call template method
        self.on_post_consolidate()

        # fill the self._output_cache dict
        self.populate_output_cache()

        # flush the cache at the end because of possible conflicts when several input
        # documents consolidate the same output document (large payload case)
        for document in self._output_cache.values():
            # tell to generate a report about this document
            self.report(document)

            # go feed parallel_bulk
            yield document.to_bulk_action()

    def populate_initial_state(self, consolidated_documents: List[MAASDocument]):
        """
        Save the state of documents in initial_state_dict attribute for later comparison

        Args:
            consolidated_documents (List[MAASDocument]): documents
        """
        if self.args and self.args.force:
            # no need to populate initial_state_dict
            return

        self.initial_state_dict = {
            document.meta.id: document.to_dict()
            for document in consolidated_documents
            if isinstance(document, (MAASDocument))
        }

    def populate_output_cache(self):
        """

        Fill the _output_cache dictionnary with writen documents
        """
        # now fill the self._output_cache dict
        for document in self.consolidated_documents:
            if self.args.force:
                self._output_cache[document.meta.id] = document
                continue

            if document.meta.id in self.initial_state_dict:
                initial_dict = self.initial_state_dict[document.meta.id]
                document_has_changed = initial_dict | document.to_dict() != initial_dict

            else:
                # Some engine don't store consistent initial state for special purpose
                document_has_changed = True

            if document_has_changed:
                self._output_cache[document.meta.id] = document

    def on_pre_consolidate(self):
        """

        Template method executed before consolidating any raw data

        A place to fill some data cache if raw data attributes can be query criterias

        Note that consolidated documents are not populated when called to allow
        explicit consolidated indices to be deduced from raw data.

        """

    def on_post_consolidate(self):
        """
        template method executed after consolidating all raw data.

        A nice place to make queries with criterias from the currently process data set.
        """

    def _consolidate(
        self,
        methodobj: Callable,
        raw_document: MAASDocument,
        document: MAASDocument,
    ) -> None:
        """Consolidate a document from raw data using a callable

        Args:
            methodobj (Callable): a callable that behave like a consolidation method
            raw_document (MAASDocument): raw document
            document (MAASDocument): consolidated document
        """
        self.logger.debug("Consolidating raw document %s to %s", raw_document, document)

        try:
            document = methodobj(raw_document, document)

            if document:
                # FIXME PERFO may be not necessary because later serialization will
                # break but nice for concistency
                document.full_clean()

        except OpenSearchException as error:
            raise error

        # catch broad exception to not break
        # pylint: disable=W0703
        except Exception as error:
            self.logger.error("Error consolidating %s to %s", raw_document, document)
            self.logger.exception(error)
            return

        if not document:
            # if can be legit to not return a document to signify nothing has to
            # be consolidated, or consolidation method has done its own document
            # updates
            self.logger.info("Not consolidating %s", raw_document)
            return

        # check mandatory field for serialization
        if not document.has_partition_field_value:
            self.logger.warning(
                (
                    "Won't consolidate: partition field has not value in %s."
                    "Raw document: %s %s"
                ),
                document,
                raw_document,
                raw_document,
            )
            return

        if self.min_doi and document.partition_field_value < self.min_doi:
            self.logger.info(
                "Document %s is to old for consolidation (doi=%s < min_doi=%s)",
                document,
                document.partition_field_value,
                self.min_doi,
            )
            return

        self.consolidated_documents.append(document)
