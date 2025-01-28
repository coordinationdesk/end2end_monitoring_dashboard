"""Product consolidation"""

from itertools import chain
import re
from opensearchpy import Q

from maas_engine.engine.rawdata import DataEngine


from maas_cds import model


class ComputeCamsReferencesEngine(DataEngine):
    """Consolidate cams references"""

    ENGINE_ID = "COMPUTE_CAMS_REFERENCES"

    MAX_IMPACTED_DATATAKE_COUNT = 256

    REFERENCE_PATTERNS = {
        "S1": re.compile("S1(A|B|C|D)-[0-9]{6}"),
        "S2": re.compile("S2(A|B|C|D)-[0-9]{5}(-[0-9]([0-9])?)?"),
        "S3": re.compile("S3(A|B)-[0-9]{3}-[0-9]{3}"),
        "S5": re.compile("S5P-[0-9]{5}"),
    }

    def __init__(
        self, args=None, send_reports=False, base_url="https://cams.esa.int/browse/"
    ):
        super().__init__(args, send_reports=send_reports)
        self._consolidated_ticket_dict = {}
        self.base_url = base_url

    def action_iterator(self):
        # retrieve consolidated tickets for correlation file check
        if self.payload.document_class in ("CamsTickets", "CamsCloudTickets"):
            self._consolidated_ticket_dict = {
                ticket.meta.id: ticket
                for ticket in self.get_consolidated_tickets()
                if ticket
            }

        for document in self.input_documents:
            if isinstance(document, (model.CamsTickets, model.CamsCloudTickets)):
                self.logger.debug("Cams reference update trigged by cams ingestion")
                environment = document.environment
                cams_id = document.key

                consolidated_ticket = self._consolidated_ticket_dict.get(cams_id)

                if not consolidated_ticket:
                    self.logger.error(
                        "Raw ticket %s has not been consolidated", cams_id
                    )
                    continue
                elif consolidated_ticket.correlation_file_id:
                    self.logger.info(
                        "%s has a correlation file %s: skipping environment",
                        cams_id,
                        consolidated_ticket.correlation_file_id,
                    )
                    continue

                # remove all references of the given cams
                yield from self.update_action_that_remove_out_of_date_reference(
                    cams_id, environment
                )

                if environment:
                    # add all references of the cams
                    impacted_entities = {
                        entity.strip() for entity in environment.split(";")
                    }
                    for impacted_entity in impacted_entities:
                        yield from self.update_impacted_entity(cams_id, impacted_entity)

            elif isinstance(document, (model.CdsDatatakeS1, model.CdsDatatakeS2)):
                self.logger.debug("Cams reference update trigged by datatake ingestion")
                yield from self.update_cams_references_for_datatake()

            elif isinstance(
                document, (model.CdsS3Completeness, model.CdsS5Completeness)
            ):
                self.logger.debug(
                    "Cams reference update trigged by s3 or s5 completeness ingestion"
                )
                yield from self.update_cams_references_for_s3_s5_completeness()

            else:
                self.logger.warning(
                    "The compute_cams_reference engine does not support the document type : %s",
                    str(type(document)),
                )

    def get_consolidated_tickets(self) -> list[model.CdsCamsTickets]:
        """
        Search consolidated tickets from the payload

        Returns:
            list[model.CdsCamsTickets]: consolidated tickets
        """

        results = list(model.CdsCamsTickets.mget_by_ids(self.payload.document_ids))

        if not all(results):
            self.logger.error(
                "CdsCamsTickets: missing consolidated tickets from %s",
                self.payload.document_ids,
            )

        return results

    def update_cams_references_for_datatake(self):
        """update cams reference for datatakes

        Yields:
            _type_: _description_
        """
        for datatake in self.input_documents:
            datatake.cams_tickets = []
            self.logger.info("Clear references of cams for datatake %s", datatake.key)
            for cams in self.search_all_cams_with_environment_not_empty():
                if datatake.key in cams.environment:
                    self.logger.info(
                        "Create new reference of cams %s on datatake %s referenced on cams environment : %s",
                        cams.key,
                        datatake.key,
                        cams.environment,
                    )
                    if cams.key not in datatake.cams_tickets:
                        datatake.cams_tickets.append(cams.key)
                    datatake.last_attached_ticket = cams.key
                    datatake.last_attached_ticket_url = self.base_url + cams.key
            yield datatake.to_bulk_action()

    def update_cams_references_for_s3_s5_completeness(self):
        """update cams references for s3 and s5 completeness

        Yields:
            _type_: _description_
        """
        for completeness in self.input_documents:
            completeness.cams_tickets = []
            self.logger.info(
                "Clear references of cams for completeness %s",
                completeness.datatake_id,
            )
            for cams in self.search_all_cams_with_environment_not_empty():
                if completeness.datatake_id in cams.environment:
                    self.logger.info(
                        "Create new reference of cams %s on s3 completeness %s referenced on cams environment : %s",
                        cams.key,
                        completeness.datatake_id,
                        cams.environment,
                    )
                    if cams.key not in completeness.cams_tickets:
                        completeness.cams_tickets.append(cams.key)
                    completeness.last_attached_ticket = cams.key
                    completeness.last_attached_ticket_url = self.base_url + cams.key
            yield completeness.to_bulk_action()

    def update_impacted_entity(self, cams_id: str, impacted_entity: str):
        """update impacted entity

        Args:
            cams_id (str): current cams
            impacted_entity (str): impacted entity to update

        Yields:
            dict: bulk action to update the entity
        """

        if self.REFERENCE_PATTERNS["S1"].match(
            impacted_entity
        ) or self.REFERENCE_PATTERNS["S2"].match(impacted_entity):
            for datatake in self.search_datatakes_not_linked_to_cams_by_id(
                impacted_entity, cams_id
            ):
                if not datatake.cams_tickets:
                    datatake.cams_tickets = []
                self.logger.info(
                    "Create new reference of cams %s on datatake %s ",
                    cams_id,
                    datatake.key,
                )
                if cams_id not in datatake.cams_tickets:
                    datatake.cams_tickets.append(cams_id)
                datatake.last_attached_ticket = cams_id
                datatake.last_attached_ticket_url = self.base_url + cams_id
                yield datatake.to_bulk_action()

        elif self.REFERENCE_PATTERNS["S3"].match(
            impacted_entity
        ) or self.REFERENCE_PATTERNS["S5"].match(impacted_entity):
            model_completeness = model.CdsS5Completeness
            if self.REFERENCE_PATTERNS["S3"].match(impacted_entity):
                model_completeness = model.CdsS3Completeness

            for completeness in self.search_s3_s5_completeness_not_linked_to_cams_by_id(
                model_completeness, impacted_entity, cams_id
            ):
                if not completeness.cams_tickets:
                    completeness.cams_tickets = []
                self.logger.info(
                    "Create new reference of cams %s on completeness %s ",
                    cams_id,
                    completeness.datatake_id,
                )
                if cams_id not in completeness.cams_tickets:
                    completeness.cams_tickets.append(cams_id)
                completeness.last_attached_ticket = cams_id
                completeness.last_attached_ticket_url = self.base_url + cams_id
                yield completeness.to_bulk_action()

    def update_action_that_remove_out_of_date_reference(
        self, cams_id: str, environment: str
    ):
        """generate update action that remove references on datatakes that is not longer in cams

        Args:
            cams_id (str): cam_id to remove
            environment (str): new environment of the cam

        Yields:
            dict: bulk action of update
        """
        for datatake in self.search_datatakes_by_linked_cams(cams_id):
            if not environment or not datatake.key in environment:
                if cams_id in datatake.cams_tickets:
                    self.logger.info(
                        "Remove reference of cams %s on datatake %s because is no longer referenced in cams environment",
                        cams_id,
                        datatake.key,
                    )
                    datatake.cams_tickets.remove(cams_id)

                    if datatake.cams_tickets:
                        datatake.last_attached_ticket = datatake.cams_tickets[-1]
                        datatake.last_attached_ticket_url = (
                            self.base_url + datatake.last_attached_ticket
                        )
                    else:
                        datatake.last_attached_ticket = None
                        datatake.last_attached_ticket_url = None
                    yield datatake.to_bulk_action()

        for completeness in chain(
            self.search_s3_s5_completeness_by_linked_cams(
                model.CdsS3Completeness, cams_id
            ),
            self.search_s3_s5_completeness_by_linked_cams(
                model.CdsS5Completeness, cams_id
            ),
        ):
            if not environment or not completeness.datatake_id in environment:
                if cams_id in completeness.cams_tickets:
                    self.logger.info(
                        "Remove reference of cams %s on completeness %s because is no longer referenced in cams environment",
                        cams_id,
                        completeness.datatake_id,
                    )
                    completeness.cams_tickets.remove(cams_id)

                    if completeness.cams_tickets:
                        completeness.last_attached_ticket = completeness.cams_tickets[
                            -1
                        ]
                        completeness.last_attached_ticket_url = (
                            self.base_url + completeness.last_attached_ticket
                        )
                    else:
                        completeness.last_attached_ticket = None
                        completeness.last_attached_ticket_url = None

                    yield completeness.to_bulk_action()

    def search_datatakes_not_linked_to_cams_by_id(self, datatake_id: str, cams_id: str):
        """search a datatake that is referenced by cams but the reference is not mentionned in datatake
        Args:
            datatake_id (str): searched datatake id
            cams_id (str): cams_id not referenced by the datatake searched

        Returns:
            itt: query
        """
        return (
            model.CdsDatatake.search()
            .filter("term", key=datatake_id)
            .filter("bool", must_not=Q("term", cams_tickets=cams_id))
            .params(
                version=True,
                seq_no_primary_term=True,
                size=self.MAX_IMPACTED_DATATAKE_COUNT,
            )
            .execute()
        )

    def search_datatakes_by_linked_cams(self, cams_id: str):
        """search datatakes that reference cams

        Args:
            cams_id (str): cams

        Returns:
            itt: query
        """
        return (
            model.CdsDatatake.search()
            .query("term", cams_tickets=cams_id)
            .params(
                version=True,
                seq_no_primary_term=True,
                size=self.MAX_IMPACTED_DATATAKE_COUNT,
            )
            .execute()
        )

    def search_s3_s5_completeness_not_linked_to_cams_by_id(
        self, model_completeness, completeness_id: str, cams_id: str
    ):
        """search a s3 or s5 completeness that is referenced by cams but the reference is not mentionned in datatake

        Args:
            completeness_id (str): searched completeness id
            cams_id (str): cams_id not referenced by the datatake searched

        Returns:
            itt: query
        """
        return (
            model_completeness.search()
            .filter("term", datatake_id=completeness_id)
            .filter("bool", must_not=Q("term", cams_tickets=cams_id))
            .params(
                version=True,
                seq_no_primary_term=True,
                size=self.MAX_IMPACTED_DATATAKE_COUNT,
            )
            .execute()
        )

    def search_s3_s5_completeness_by_linked_cams(
        self, model_completeness, cams_id: str
    ):
        """search s3 or s5 completeness that reference cams

        Args:
            cams_id (str): cams

        Returns:
        itt: query
        """
        return (
            model_completeness.search()
            .query("term", cams_tickets=cams_id)
            .params(
                version=True,
                seq_no_primary_term=True,
                size=self.MAX_IMPACTED_DATATAKE_COUNT,
            )
            .execute()
        )

    def search_all_cams_with_environment_not_empty(self):
        """return all cams with environment field set

        Returns:
            itt: query
        """
        return (
            model.CamsTickets.search()
            .filter("exists", field="environment")
            .params(
                version=True,
                seq_no_primary_term=True,
                size=self.MAX_IMPACTED_DATATAKE_COUNT,
            )
            .execute()
        )
