"""

acquisition sass status engines for consolidation
"""

from maas_engine.engine.replicate import ReplicatorEngine
from maas_cds.engines.reports.anomaly_impact import (
    AnomalyImpactMixinEngine,
)
from maas_engine.engine.base import EngineReport
from maas_model import datestr_to_utc_datetime

import hashlib
from typing import Any, Dict, Iterator


from maas_cds.model import (
    CdsAcquisitionPassStatus,
    CdsCadipAcquisitionPassStatus,
    ApsProduct,
    ApsSession,
)


class AcquisitionPassStatusConsolidatorEngine(
    AnomalyImpactMixinEngine, ReplicatorEngine
):
    """

    Base to consolidate acquisition pass status
    """

    ANOMALY_KEY = ""

    ENGINE_ID = ""

    def __init__(
        self,
        args,
        target_model: str = None,
        exclude_fields=None,
        send_reports=False,
        min_doi=None,
        hktm_chunk_size: int = None,
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

        self.hktm_related_products = []

        self.hktm_chunk_size = hktm_chunk_size

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

    def consolidate(
        self, raw_document: ApsSession, document: CdsAcquisitionPassStatus
    ) -> CdsAcquisitionPassStatus:
        document = super().consolidate(raw_document, document)

        self._apply_anomalies(document, key=self.ANOMALY_KEY)

        return document

    def _generate_reports(self):
        """Override to additionnaly report product attachement to container


        Yields:
            EngineReport: report
        """

        yield from super()._generate_reports()

        # yield product reports to calculate completeness
        if self.hktm_related_products:
            self.logger.debug(
                "Sending custom reports to %s of %s %s instances",
                "update.hktm-acquisition",
                len(
                    self.hktm_related_products,
                ),
                "CdsCadipAcquisitionPassStatus",
            )

            yield EngineReport(
                "update.hktm-acquisition",
                [document.meta.id for document in self.hktm_related_products],
                "CdsCadipAcquisitionPassStatus",
                document_indices=self.get_index_names(self.hktm_related_products),
                chunk_size=self.hktm_chunk_size,
            )


class XBandAcquisitionPassStatusConsolidatorEngine(
    AcquisitionPassStatusConsolidatorEngine
):
    """

    Consolidate X-Band acquisition pass status
    """

    ENGINE_ID = "CONSOLIDATE_APS"

    ANOMALY_KEY = lambda _, aps: "_".join(
        [aps.satellite_id, "X-Band", aps.downlink_orbit, aps.ground_station]
    )

    def __init__(
        self,
        args,
        exclude_fields=None,
        send_reports=False,
        min_doi=None,
        hktm_chunk_size=None,
    ):
        super().__init__(
            args,
            target_model="CdsAcquisitionPassStatus",
            exclude_fields=exclude_fields,
            send_reports=send_reports,
            min_doi=min_doi,
            hktm_chunk_size=hktm_chunk_size,
        )

    def consolidate(
        self, raw_document: ApsProduct, document: CdsAcquisitionPassStatus
    ) -> CdsAcquisitionPassStatus:
        document = super().consolidate(raw_document, document)
        # S1,S2,S3 only daily report are collected, so report_name_daily = reportName
        document.report_name_daily = raw_document.reportName

        document.from_acq_delivery_timeliness = document.calculate_timeliness()

        document.delivery_bitrate = document.calculate_bitrate(
            raw_document.meta.id,
        )

        return document


class XBandV2AcquisitionPassStatusConsolidatorEngine(
    AcquisitionPassStatusConsolidatorEngine
):
    """

    Consolidate X-Band (v2) acquisition pass status
    """

    ENGINE_ID = "CONSOLIDATE_APS_SESSION"

    # For reviewer : X-Band-V2 est un placeholder, je ne sais pas ce qu'il faut mettre
    ANOMALY_KEY = lambda _, aps: "_".join(
        [aps.satellite_id, "X-Band", str(aps.downlink_orbit), aps.ground_station]
    )

    def __init__(
        self,
        args,
        exclude_fields=None,
        send_reports=False,
        min_doi=None,
        hktm_chunk_size=None,
    ):
        super().__init__(
            args,
            target_model="CdsCadipAcquisitionPassStatus",
            exclude_fields=exclude_fields,
            send_reports=send_reports,
            min_doi=min_doi,
            hktm_chunk_size=hktm_chunk_size,
        )

    @staticmethod
    def generate_session_id(session_id, retransfer) -> str:
        """Generate a session identifier

        Args:
            status (CdsInterfaceStatus): consolidated session

        Returns:
            str: unique identifier
        """

        md5 = hashlib.md5()
        md5.update(session_id.encode())
        md5.update(str(retransfer).encode())
        return md5.hexdigest()

    @staticmethod
    def get_global_status(raw_document: ApsSession) -> str:
        return (
            "OK"
            if (
                raw_document.antenna_status
                and raw_document.front_end_status
                and raw_document.delivery_push_status
            )
            else "NOK"
        )

    @staticmethod
    def aggregate_quality_infos_metrics(
        document: CdsCadipAcquisitionPassStatus, quality_infos: list
    ) -> CdsCadipAcquisitionPassStatus:
        """
        Aggregate quality information metrics from a list of quality_infos and update the provided document.

        Args:
            document (CdsCadipAcquisitionPassStatus): The document to update with aggregated metrics.
            quality_infos (list): A list of quality_info objects.

        Returns:
            CdsCadipAcquisitionPassStatus: The updated document with aggregated metrics.
        """

        metrics = [
            "ErrorTFs",
            "CorrectedTFs",
            "DataTFs",
            "CorrectedDataTFs",
            "TotalChunks",
            "AcquiredTFs",
            "UncorrectableTFs",
            "ErrorDataTFs",
            "UncorrectableDataTFs",
            "TotalVolume",
        ]

        # sum all metrics across all chanels
        for metric in metrics:
            reduced_metric = sum(
                getattr(quality_info, metric, 0) for quality_info in quality_infos
            )
            setattr(document, metric, reduced_metric)

        # Oldest delivery start -> global session delivery start
        min_delivery_start = min(
            getattr(quality_info, "DeliveryStart")
            or datestr_to_utc_datetime("2999-01-01T01:01:01.000Z")
            for quality_info in quality_infos
        )

        document.delivery_start = min_delivery_start

        # Most recent delivery stop -> global session delivery stop
        max_delivery_stop = max(
            getattr(quality_info, "DeliveryStop")
            or datestr_to_utc_datetime("1970-01-01T01:01:01.000Z")
            for quality_info in quality_infos
        )

        document.delivery_stop = max_delivery_stop

        if document.AcquiredTFs > 0:
            document.fer_data = document.UncorrectableTFs / document.AcquiredTFs

        return document

    def session_is_valid(self, raw_document):
        """Verify if session contains all mandatory attributes

        Args:
            raw_document : ApsSession raw document

        Returns:
            boolean: session is valid to be consolidated
        """
        mandatory_attr = [
            "planned_data_start",
            "planned_data_stop",
            "antenna_status",
            "front_end_status",
            "delivery_push_status",
            "downlink_status",
            "downlink_start",
            "downlink_stop",
        ]

        missing_attributes = [
            attr for attr in mandatory_attr if getattr(raw_document, attr) is None
        ]

        if len(missing_attributes) != 0:
            self.logger.warning(
                "Missing mandatory attributes for consolidation : %s for entity %s",
                missing_attributes,
                raw_document.to_dict(),
            )
            return False

        return True

    def get_consolidated_id(self, raw_document: ApsSession) -> str:
        """
        Consolidated id is the session id

        Args:
            raw_document (ApsSession): raw document

        Returns:
            str: consolidated identifier
        """
        return raw_document.session_id

    def consolidate(
        self,
        raw_document: ApsSession,
        document: CdsCadipAcquisitionPassStatus,
    ) -> CdsCadipAcquisitionPassStatus:
        """
        Consolidate cadip acquisition pass status.

        Args:
            raw_document (ApsSession): The raw session to consolidate.
            document (CdsCadipAcquisitionPassStatus): The session to update with consolidated data.

        Returns:
            CdsCadipAcquisitionPassStatus: The updated session with consolidated data.
        """
        if document.retransfer and not raw_document.retransfer:
            self.logger.warning(
                "A Consolidated document already exist for this ID: %s and it has retransfer flag, this raw_document does not have retransfer flag so it is ignored : %s ",
                document.meta.id,
                raw_document,
            )
            return None

        document = super().consolidate(raw_document, document)

        if raw_document.publication_date < document.publication_date:
            self.logger.warning("Raw document is too old : %s ", raw_document)
            return None

        self.hktm_related_products.append(document)

        # List of metrics from quality to aggregate (sum) across all channels
        quality_infos = raw_document.quality_infos

        if quality_infos:
            document = self.aggregate_quality_infos_metrics(document, quality_infos)

        document.mission = raw_document.satellite_id[:-1]

        document.from_acq_delivery_timeliness = document.calculate_timeliness()

        document.delivery_bitrate = document.calculate_bitrate(raw_document.meta.id)
        if not self.session_is_valid(raw_document):
            self.logger.info("Incomplete session: %s ", raw_document)

            document.global_status = "INCOMPLETE"

        else:
            document.global_status = self.get_global_status(raw_document)

        return document
