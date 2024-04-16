"""

acquisition sass status engines for consolidation
"""
from maas_engine.engine.replicate import ReplicatorEngine
from maas_cds.engines.reports.anomaly_impact import (
    AnomalyImpactMixinEngine,
)
from datetime import datetime, timezone

from opensearchpy import Q

from typing import Any, Dict, Iterator


from maas_cds.model import (
    MpHktmAcquisitionProduct,
    CdsHktmAcquisitionCompleteness,
)

from maas_cds.model import (
    CdsCadipAcquisitionPassStatus,
    CdsEdrsAcquisitionPassStatus,
)


class HktmConsolidatorEngine(AnomalyImpactMixinEngine, ReplicatorEngine):
    """

    Base to consolidate acquisition pass status
    """

    ENGINE_ID = ""

    def __init__(
        self,
        args,
        target_model: str = None,
        exclude_fields=None,
        raw_data_type=None,
        send_reports=False,
        min_doi=None,
    ):
        if exclude_fields is None:
            exclude_fields = [
                "ingestionTime",
                "interface_name",
                "reportName",
                "production_service_name",
                "production_service_type",
            ]
        super().__init__(
            args,
            target_model=target_model,
            exclude_fields=exclude_fields,
            send_reports=send_reports,
            min_doi=min_doi,
        )

        self.raw_data_type = raw_data_type
        self.raw_data = self.get_model(self.raw_data_type)

    def action_iterator(self) -> Iterator[Dict[str, Any]]:
        """elastic search bulk actions generator"""
        consolidated_documents = self.get_consolidated_documents()
        self.populate_initial_state(consolidated_documents)

        for raw_document, document in zip(
            self.input_documents,
            consolidated_documents,
        ):
            self._consolidate(self.consolidate, raw_document, document)

        self.populate_output_cache()
        # flush the cache at the end because of possible conflicts when several input
        # documents consolidate the same output document (large payload case)
        for document in self._output_cache.values():
            # go feed parallel_bulk
            yield document.to_bulk_action()

    def get_input_documents(self, message) -> list[str]:
        """Get the input documents. Can be overriden for custom behaviour

        Args:
            message (maas_model.MAASMessage): input message

        Returns:
            list[str]: list of documents id (path of mp file in this particular case)
        """
        input_documents = []
        for report_name in message.document_ids:
            search = self.raw_data.search().filter("term", reportName=report_name)
            self.logger.debug("[%s] to consolidate query : %s", report_name, search)
            search = search.params(ignore=404)
            raw_input_documents = list(search.scan())
            self.logger.debug(
                "[%s] to consolidate query result list: %s",
                report_name,
                raw_input_documents,
            )
            input_documents.extend(raw_input_documents)
        return input_documents

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


class HktmAcquisitionConsolidatorEngine(HktmConsolidatorEngine):
    """

    Consolidate HKTM Acquisition mission plannings
    """

    ENGINE_ID = "CONSOLIDATE_HKTM_ACQ"

    def __init__(
        self,
        args,
        exclude_fields=None,
        raw_data_type=None,
        send_reports=False,
        min_doi=None,
    ):
        super().__init__(
            args,
            target_model="CdsHktmAcquisitionCompleteness",
            exclude_fields=exclude_fields,
            send_reports=send_reports,
            min_doi=min_doi,
            raw_data_type=raw_data_type,
        )

    def get_consolidated_id(self, raw_document) -> str:
        """
        Consolidated id is the session id

        Args:
            raw_document (ApsSession): raw document

        Returns:
            str: consolidated identifier
        """
        return raw_document.session_id

    def count_hktm_acquisition_completeness(
        self, acquisition_class, session_criteria, status_criteria
    ):
        """
        Compute the completeness of acquisitions based on session and status criteria.

        Args:
            acquisition_class (Type): The Opensearch DSL class representing the
                type of acquisitions to search.
            session_criteria (dict): session specific criteria
            status_criteria (dict): status specific criteria

        Returns:
            int: The count of document that met the criteria

        """
        class_name = acquisition_class.__name__

        if class_name == "CdsCadipAcquisitionPassStatus":
            status_filter = Q("term", **status_criteria)

        elif class_name == "CdsEdrsAcquisitionPassStatus":
            # every row that is not NOK is considered OK for EDRS
            status_filter = Q("bool", must_not=[Q("term", **status_criteria)])

        session_filter = Q("term", **session_criteria)
        combined_query = Q("bool", filter=[status_filter, session_filter])

        count = acquisition_class.search().query(combined_query).count()

        self.logger.info(
            "Number of acquisition associated to this HKTM: %s",
            count,
        )
        return count

    def consolidate(
        self,
        raw_document: MpHktmAcquisitionProduct,
        document: CdsHktmAcquisitionCompleteness,
    ) -> CdsHktmAcquisitionCompleteness:
        """
        Consolidate cadip acquisition pass status.

        Args:
            raw_document (ApsSession): The raw session to consolidate.
            document (CdsHktmAcquisitionCompleteness): The session to update with consolidated data.

        Returns:
            CdsHktmAcquisitionCompleteness: The updated session with consolidated data.
        """
        if (
            document.execution_time
            and raw_document.execution_time < document.execution_time
        ):
            self.logger.warning("Raw document is too old : %s ", raw_document)
            return None

        document = super().consolidate(raw_document, document)

        document.ingestionTime = datetime.now(tz=timezone.utc)
        document.reportName = raw_document.reportName
        document.interface_name = raw_document.interface_name
        document.channel = raw_document.channel
        document.session_id = raw_document.session_id
        document.absolute_orbit = raw_document.absolute_orbit
        document.satellite_unit = raw_document.satellite_id
        document.mission = raw_document.satellite_id[:2]
        document.ground_station = raw_document.ground_station
        document.execution_time = raw_document.execution_time
        document.production_service_name = raw_document.production_service_name
        document.production_service_type = raw_document.production_service_type
        document.meta.id = raw_document.session_id

        cadip_completeness = None
        edrs_completeness = None

        if "DCS_0X_" in raw_document.session_id:  # cadip session
            session_id = raw_document.session_id.split("DCS_0X_")[-1]
            self.logger.debug("HKTM associated to a CADIP acquisition")

            session_criteria = {"session_id": session_id}
            status_criteria = {"global_status": "OK"}

            count = self.count_hktm_acquisition_completeness(
                CdsCadipAcquisitionPassStatus, session_criteria, status_criteria
            )

            cadip_completeness = 1 if count == 1 else 0

            anomaly_key = lambda hktm: "_".join(
                [
                    hktm.satellite_unit,
                    "X-Band",
                    str(hktm.absolute_orbit),
                    hktm.ground_station,
                ]
            )

        elif (
            "EDRS" in raw_document.ground_station and raw_document.session_id[0] == "L"
        ):
            self.logger.debug("HKTM associated to a EDRS acquisition")

            session_id = raw_document.session_id

            session_criteria = {"link_session_id": session_id}
            status_criteria = {"total_status": "NOK"}  # will be negated

            count = self.count_hktm_acquisition_completeness(
                CdsEdrsAcquisitionPassStatus, session_criteria, status_criteria
            )

            edrs_completeness = 1 if count >= 1 else 0

            anomaly_key = lambda hktm: "_".join(
                [
                    hktm.satellite_unit,
                    "EDRS",
                    session_id,
                    hktm.ground_station,
                ]
            )

        document.cadip_completeness = cadip_completeness
        document.edrs_completeness = edrs_completeness

        self.logger.debug("CADIP Completeness : %s | EDRS Completeness : %s")
        self.logger.debug("Applying anomalies ...")
        self._apply_anomalies(document, key=anomaly_key)

        return document
