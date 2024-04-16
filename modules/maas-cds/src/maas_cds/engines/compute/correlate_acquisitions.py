"""Product consolidation"""

from datetime import timedelta
from typing import Any, Dict, Iterator, List
from maas_engine.engine.rawdata import DataEngine
from maas_cds.model import (
    CdsDownlinkDatatake,
    CdsEdrsAcquisitionPassStatus,
    CdsCadipAcquisitionPassStatus,
    CdsDatatake,
)
from maas_cds.lib.dateutils import get_microseconds_delta
from opensearchpy import MultiSearch, Q, Search


class CorrelateAcquisitionsEngine(DataEngine):
    """Add fields delivery_stop and observation_time_start in CdsDownlinkDatatake
    using infos from edrs,cadip acqusitions and cds_datatake"""

    ENGINE_ID = "CORRELATE_ACQUISITIONS"

    def __init__(
        self,
        args=None,
        source_type=None,
        chunk_size=1,
        send_reports=False,
    ):
        super().__init__(args, chunk_size=chunk_size, send_reports=send_reports)
        self.source_type = self.get_model(source_type)
        self.update_search = None
        self.delivery_stop_field = None
        self.needed_fields = []

        if self.source_type == CdsEdrsAcquisitionPassStatus:
            self.generate_search = self.generate_edrs_search
            self.delivery_stop_field = "dissemination_stop"
            self.needed_fields = [
                self.delivery_stop_field,
                "satellite_id",
                "geo_satellite_id",
                "dissemination_start",
            ]
        elif self.source_type == CdsCadipAcquisitionPassStatus:
            self.generate_search = self.generate_cadip_search
            self.delivery_stop_field = "delivery_stop"
            self.needed_fields = [
                "ground_station",
                "downlink_orbit",
                "satellite_id",
                self.delivery_stop_field,
            ]
        elif self.source_type == CdsDatatake:
            self.needed_fields = ["datatake_id", "satellite_unit"]

    def generate_edrs_search(self, doc: CdsEdrsAcquisitionPassStatus) -> Search:
        """This function is used to generate a downlink search
        using fields of the input document

        Args:
            doc (CdsEdrsAcquisitionPassStatus): EDRS Acquisition input document

        Returns:
            Search: Search object using doc fields as filter
        """
        return (
            CdsDownlinkDatatake.search()
            .filter("term", satellite_unit=doc.satellite_id)
            .filter("term", station=doc.geo_satellite_id)
            .filter(
                "range",
                effective_downlink_start={
                    "gte": doc.dissemination_start - timedelta(minutes=30)
                },
            )
            .filter(
                "range",
                effective_downlink_stop={
                    "lte": doc.dissemination_stop + timedelta(minutes=30)
                },
            )
        )

    def generate_cadip_search(self, doc: CdsCadipAcquisitionPassStatus) -> Search:
        """This function is used to generate a downlink search
         using fields of the input document

        Args:
            doc (CdsCadipAcquisitionPassStatus): Cadip Acquisition Input Document

        Returns:
            Search: Search object using doc fields as filter
        """
        return (
            CdsDownlinkDatatake.search()
            .filter("term", satellite_unit=doc.satellite_id)
            .filter("term", downlink_absolute_orbit=doc.downlink_orbit)
            .filter(
                "bool", must=[Q("regexp", station=".*" + doc.ground_station + ".*")]
            )
        )

    def action_iterator(self) -> Iterator[Dict[str, Any]]:
        """elastic search bulk actions generator"""

        if self.source_type in (
            CdsEdrsAcquisitionPassStatus,
            CdsCadipAcquisitionPassStatus,
        ):
            updated_docs = self.update_downlink_from_acq(self.input_documents)
        elif self.source_type == CdsDatatake:
            updated_docs = self.update_downlink_from_datatake(self.input_documents)

        for document in updated_docs:
            yield document.to_bulk_action()

    def update_downlink_from_acq(
        self,
        input_documents: List[
            CdsEdrsAcquisitionPassStatus | CdsCadipAcquisitionPassStatus
        ],
    ) -> List[CdsDownlinkDatatake]:
        """This function is used to add the delivery_stop field to the downlike datatakes elements
          associated to the acquisitions in input
          If observation start is also available then
          the observation-deliverystop timeliness is also calculated

        Args:
            input_documents (List[ CdsEdrsAcquisitionPassStatus
              |  CdsCadipAcquisitionPassStatus ]): List of input acquisitions documents

        Returns:
            List[CdsDownlinkDatatake]: List of CdsDownlinkDatatake to update in DB
        """
        # Ignore acq which does not have all the required field for the msearch
        input_docs = []
        for doc in input_documents:
            if not all(key in doc for key in self.needed_fields):
                self.logger.debug(
                    "No downlink datatake correlation will "
                    "be done for Acquisition %s because all the"
                    " needed fields %s were not found in it",
                    doc.meta.id,
                    self.needed_fields,
                )
            else:
                input_docs.append(doc)

        if not input_docs:
            return []

        msearch_downlink = MultiSearch()
        for doc in input_docs:
            msearch_downlink = msearch_downlink.add(self.generate_search(doc))

        cached_downlink: Dict[str, CdsDownlinkDatatake] = {}

        for doc, responses in zip(input_docs, msearch_downlink.execute()):
            if responses:
                for downlink in responses:
                    if downlink.meta.id in cached_downlink:
                        downlink = cached_downlink[downlink.meta.id]
                    else:
                        cached_downlink[downlink.meta.id] = downlink

                    if (
                        not "delivery_stop" in cached_downlink[downlink.meta.id]
                        or cached_downlink[downlink.meta.id].delivery_stop
                        < doc[self.delivery_stop_field]
                    ):
                        cached_downlink[downlink.meta.id].delivery_stop = doc[
                            self.delivery_stop_field
                        ]

        versionned_downlinks = list(
            CdsDownlinkDatatake.mget_by_ids(list(cached_downlink.keys()))
        )
        for downlink in versionned_downlinks:
            downlink.delivery_stop = cached_downlink[downlink.meta.id].delivery_stop
            if downlink.observation_time_start:
                downlink.from_sensing_to_delivery_stop_timeliness = (
                    get_microseconds_delta(
                        downlink.delivery_stop,
                        downlink.observation_time_start,
                    )
                )
        return list(versionned_downlinks)

    def update_downlink_from_datatake(
        self, input_documents: List[CdsDatatake]
    ) -> List[CdsDownlinkDatatake]:
        """This function is used to add the observation start date
          field to the downlike datatakes elements
          associated to the datatakes in input
          If delivery stop field is also available then
          the observation-deliverystop timeliness is also calculated

        Args:
            input_documents (List[CdsDatatake]): List of input CdsDatatakes documents

        Returns:
            List[CdsDownlinkDatatake]: List of CdsDownlink to update in DB
        """
        msearch_downlink = MultiSearch()
        cached_downlink: Dict[str, CdsDownlinkDatatake] = {}

        input_docs = []
        for doc in input_documents:
            if not all(key in doc for key in self.needed_fields):
                self.logger.debug(
                    "No downlink datatake correlation will "
                    "be done for datatake %s because all the"
                    " needed fields %s were not found in it",
                    doc.meta.id,
                    self.needed_fields,
                )
            else:
                input_docs.append(doc)

        if not input_docs:
            return []

        for doc in input_docs:
            msearch_downlink = msearch_downlink.add(
                CdsDownlinkDatatake.search()
                .filter("term", datatake_id=doc.datatake_id)
                .filter("term", satellite_unit=doc.satellite_unit)
            )

        for doc, responses in zip(input_docs, msearch_downlink.execute()):
            for downlink in responses:
                if downlink.meta.id in cached_downlink:
                    downlink = cached_downlink[downlink.meta.id]
                else:
                    cached_downlink[downlink.meta.id] = downlink

                cached_downlink[
                    downlink.meta.id
                ].observation_time_start = doc.observation_time_start

        versionned_downlinks = list(
            CdsDownlinkDatatake.mget_by_ids(list(cached_downlink.keys()))
        )

        for downlink in versionned_downlinks:
            downlink.observation_time_start = cached_downlink[
                downlink.meta.id
            ].observation_time_start
            if "delivery_stop" in downlink:
                downlink.from_sensing_to_delivery_stop_timeliness = (
                    get_microseconds_delta(
                        downlink.delivery_stop,
                        downlink.observation_time_start,
                    )
                )
        return versionned_downlinks
