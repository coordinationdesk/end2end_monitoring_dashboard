"""Sat unavailability Product consolidation"""

import hashlib

from maas_engine.engine.rawdata import RawDataEngine

from maas_model import datestr_to_utc_datetime, MAASMessage
from maas_cds.lib.dateutils import get_microseconds_delta

from maas_cds import model


class SatUnavailabilityConsolidatorEngine(RawDataEngine):
    """Consolidate sat unavailability from raw products"""

    ENGINE_ID = "CONSOLIDATE_SATUNAVAILABILITY"

    CONSOLIDATED_MODEL = model.CdsSatUnavailability

    _existing = {}

    def get_consolidated_id(self, raw_document) -> str:
        """Get the document id for CdsSatUnavailability

        Args:
            raw_document: raw document

        Returns:
            str: he document id
        """
        md5 = hashlib.md5()
        for field in "mission", "subsystem", "start_time":
            md5.update(getattr(raw_document, field).encode())
        return md5.hexdigest()

    def _load_input_documents(self, payload: MAASMessage, routing_key: str = ""):
        """Batch populate existing consolidated documents"""

        super()._load_input_documents(payload, routing_key)

        # Fetch and store existing consolidated objects
        existing_consolidated_documents = model.CdsSatUnavailability.mget_by_ids(
            list(
                set(
                    self.get_consolidated_id(raw_document)
                    for raw_document in self.input_documents
                )
            ),
            ignore_missing_index=True,
            log_missing=False,
        )

        self._existing = {
            consolidated_document.meta.id: consolidated_document
            for consolidated_document in existing_consolidated_documents
            if consolidated_document
        }

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    def consolidate_from_SatUnavailabilityProduct(
        self,
        raw_document: model.SatUnavailabilityProduct,
        document: model.CdsSatUnavailability,
    ) -> model.CdsSatUnavailability:
        """
        "consolidated products from sat Unavailability ingestion"

        Args:
            raw_document (model.SatUnavailabilityProduct): raw document
            document (model.CdsSatUnavailability): CdsSatUnavailability document

        Returns:
            model.CdsSatUnavailability: CdsSatUnavailability document
        """

        document.key = self.get_consolidated_id(raw_document)

        if existing := self._existing.get(document.key):
            more_complete = not existing.end_time and raw_document.end_time
            less_complete = existing.end_time and not raw_document.end_time
            ingestion_time = (
                datestr_to_utc_datetime(raw_document.ingestionTime)
                if isinstance(raw_document.ingestionTime, str)
                else raw_document.ingestionTime
            )
            is_update = ingestion_time > existing.raw_data_ingestion_time
            if less_complete or (not more_complete and not is_update):
                return None

        document.satellite_unit = "S" + raw_document.mission[-2:]
        document.mission = document.satellite_unit[:2]
        document.comment = raw_document.comment
        document.end_anx_offset = raw_document.end_anx_offset
        document.end_orbit = (
            str(raw_document.end_orbit).lstrip("0")
            if raw_document.end_orbit is not None
            else None
        )
        document.file_name = raw_document.file_name
        document.start_anx_offset = raw_document.start_anx_offset
        document.start_time = datestr_to_utc_datetime(raw_document.start_time[4:])
        document.start_orbit = (
            str(raw_document.start_orbit).lstrip("0")
            if raw_document.start_orbit is not None
            else None
        )
        document.subsystem = raw_document.subsystem
        document.type = raw_document.type

        if len(raw_document.end_time) != 0:
            document.end_time = datestr_to_utc_datetime(raw_document.end_time[4:])

            document.unavailability_duration = get_microseconds_delta(
                document.start_time.replace(tzinfo=None),
                document.end_time.replace(tzinfo=None),
            )
        else:
            document.end_time = None

        document.unavailability_type = raw_document.unavailability_type
        document.unavailability_reference = raw_document.unavailability_reference
        document.raw_data_ingestion_time = raw_document.ingestionTime

        return document
