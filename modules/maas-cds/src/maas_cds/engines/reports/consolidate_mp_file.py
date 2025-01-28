"""Update entities after some container products are see"""

import typing
import hashlib
import copy
from datetime import datetime, timedelta, timezone
from maas_cds.model.datatake import CdsDatatake
from opensearchpy import Q
from itertools import groupby

from maas_engine.engine.rawdata import DataEngine
from maas_engine.engine.base import EngineReport
from maas_model import (
    MAASMessage,
    MAASDocument,
    MAASRawDocument,
    datestr_to_utc_datetime,
    datetime_to_zulu,
)
from maas_cds.engines.reports.mission_mixin import MissionMixinEngine
from maas_cds.engines.reports.anomaly_impact import (
    AnomalyImpactMixinEngine,
    anomaly_link,
)

from maas_cds.model.generated import (
    MaasConfigCompleteness,
    MpProduct,
    MpAllProduct,
    MpHktmDownlink,
    MpHktmAcquisitionProduct,
)
from maas_cds.model import (
    CdsCamsTickets,
    CdsCompleteness,
    CdsProduct,
    CdsCadipAcquisitionPassStatus,
    CdsEdrsAcquisitionPassStatus,
    CdsHktmAcquisitionCompleteness,
    CdsHktmProductionCompleteness,
)


class ConsolidateMpFileEngine(MissionMixinEngine, AnomalyImpactMixinEngine, DataEngine):
    """Deletetion of datatake due to rescheduled"""

    ENGINE_ID = "CONSOLIDATE_MP_FILE"

    TOLERANCE_IN_MINUTES = 30

    COMPLETENESS_CONFIG = None

    def __init__(
        self,
        args=None,
        raw_data_type=None,
        consolidated_data_type=None,
        data_time_start_field_name=None,
        chunk_size=1,
        send_reports=True,
        tolerance_value: int = 30,
        merge_reports: bool = True,
    ):
        super().__init__(args, chunk_size=chunk_size, send_reports=send_reports)
        self.raw_data_type = raw_data_type
        self.consolidated_data_type = consolidated_data_type
        self.raw_data = self.get_model(self.raw_data_type)
        self.consolidated_data = self.get_model(self.consolidated_data_type)
        self.data_time_start_field_name = data_time_start_field_name
        self.future_ids = set()
        self.tolerance_value = tolerance_value
        self.merge_reports = merge_reports

    def action_iterator(self) -> typing.Generator:
        """override

        Iter throught input documents and find products who are inside
        Then add informations on these products

        Yields:
            Iterator[typing.Generator]: bulk actions
        """

        for local_report_name in self.input_documents:
            # check if the report is empty i.e. there is no raw data depending on this report
            nbr_raw_data_for_report = self.get_nbr_raw_data_for_report(
                local_report_name
            )
            if nbr_raw_data_for_report == 0:
                self.logger.info(
                    "[%s] report empty no completeness computed for empty report",
                    local_report_name,
                )
                continue

            # retrieve satelite id from report
            sat_id = local_report_name[0:3]
            # Min date to delete
            # Get the minimum data time start_field from current report (i.e. local_report_name)
            min_date = self.get_report_min_date(local_report_name)
            # Get the next reportName
            next_repport_name = self.get_next_report(sat_id, local_report_name)
            # Get maximum date from next report (min of next report)
            if next_repport_name:
                # Get the minimum data time start_field from the next report
                max_date = self.get_report_min_date(next_repport_name)
                max_date = datetime_to_zulu(max_date)

            else:
                # no next report use * to get all data
                max_date = "*"
            # Delete all consolidated data between min and max date
            datatake_delete_list = self.get_to_delete_consolidated_data(
                sat_id, min_date, max_date
            )
            for to_delete_datatake in datatake_delete_list:
                yield to_delete_datatake.to_bulk_action("delete")
            # Insert from current report from min to max date
            mp_consolidate_list = self.get_to_be_consolidated_raw_data(
                local_report_name, max_date
            )

            self._populate_ticket_cache(mp_consolidate_list)

            for to_consolidate_mp in mp_consolidate_list:

                # There is double mp_all containing 2 session_id and 2 merged station (ex: "SGS_MTI_")
                # We need to split it into 2 consolidated documents having one of each
                if self.should_split_mp(to_consolidate_mp):

                    for to_consolidate_mp_all in self.split_mp_all(to_consolidate_mp):

                        yield from self.process_mp(to_consolidate_mp_all)

                # In nominal case, each MP produces 1 consolidateed document
                else:

                    yield from self.process_mp(to_consolidate_mp)

    def process_mp(
        self,
        to_consolidate_mp: (
            MpProduct | MpAllProduct | MpHktmDownlink | MpHktmAcquisitionProduct
        ),
    ):
        """
        Nominal processing flow for mission planning products.
        model specific consolidation -> report -> yield

        Args:
            to_consolidate_mp (MpProduct | MpAllProduct | MpHktmDownlink | MpHktmAcquisitionProduct): raw mp

        Yields:
            CdsHktmAcquisitionCompleteness | CdsHktmProductionCompleteness | CdsDownlinkDatatake | CdsDatatake : Consolidated document
        """
        consolidated_docs = self.consolidate_data_from_raw_data(to_consolidate_mp)

        for consolidated_doc in consolidated_docs:

            if consolidated_doc is not None:
                if self.consolidated_data_type != "CdsDownlinkDatatake":
                    self.report(consolidated_doc)
                yield consolidated_doc.to_bulk_action()

    def should_split_mp(self, to_consolidate_mp: MpAllProduct):
        """Condition to identify double mp all products

        Args:
            to_consolidate_mp (MpAllProduct): mp all product

        Returns:
            bool: wether the mp is double or not
        """
        session_id = getattr(to_consolidate_mp, "session_id", None)

        return (
            session_id is not None
            and isinstance(session_id, list)
            and len(to_consolidate_mp.session_id) > 1
        )

    def _generate_report_from_action_per_documents(self, classname, action, documents):
        """Override strategy to send report per indices"""

        # Group by require sorted data
        documents.sort(key=lambda doc: doc.partition_index_name)

        grouped_documents = {
            key: list(group)
            for key, group in groupby(
                documents, key=lambda doc: doc.partition_index_name
            )
        }

        for index, docs in grouped_documents.items():
            self.logger.debug("Using custom report strategy: %s - %s", index, classname)
            yield EngineReport(
                action,
                [document.meta.id for document in docs],
                document_class=classname,
                chunk_size=self.chunk_size,
                document_indices=[index],
            )

    def split_mp_all(self, mp_all: MpAllProduct):
        """Some mp_all documents are a merger of 2 stations and 2 session_id
        so, to be utilized in grafana, it first needs to be splitted into 2 distinct
        document, each having one session ID and one station.
        This method provide the splitting of a double mp_all

        Args:
            mp_all (MpAllProduct): double mp_all needing to be splitted

        Returns:
            list: list of individual mp all with one session_id and station
        """

        splitted_mp_list = []
        self.logger.debug(
            "Splitting MP ALL document having multiple session ids %s and station %s",
            mp_all.session_id,
            mp_all.station,
        )
        for i, session_id in enumerate(mp_all.session_id):

            self.logger.debug("Session ID : %s", session_id)

            # Station for double mp_all is in the form : "AAA_BBB_" with AAA and BBB being
            # the trigram for a station
            # I needs to be divided into 1: "AAA_", 2: "BBB_"
            splitted_station = mp_all.station[4 * i : 4 * (i + 1)]
            self.logger.debug("Splitted station : %s", splitted_station)

            new_mp_all = copy.deepcopy(mp_all)

            new_mp_all.session_id = [session_id]
            new_mp_all.station = splitted_station

            # Generate a new ID using splitted station, session_id, and other attributes
            new_id = self.generate_downlink_datatake_id(new_mp_all)

            new_mp_all.meta.id = new_id

            splitted_mp_list.append(new_mp_all)

        return splitted_mp_list

    def get_nbr_raw_data_for_report(self, local_report_name):
        """Get the number of value for the given report.

        Args:
            local_report_name (str): the report name to inspect in

        Returns:
            nbr_raw_data_for_report (int): the number of raw data in the report
        """
        nbr_raw_data_for_report = 0
        search = self.raw_data.search().filter("term", reportName=local_report_name)
        self.logger.debug(
            "[%s] get raw data nbr from report query : %s",
            local_report_name,
            search,
        )
        nbr_raw_data_for_report = search.count()
        self.logger.debug(
            "[%s] get raw data nbr from report query result : %s",
            local_report_name,
            nbr_raw_data_for_report,
        )
        return nbr_raw_data_for_report

    def get_report_min_date(self, local_report_name):
        """Get the min value of data time start field of the given report.

        Args:
            local_report_name (str): the report name to inspect in

        Returns:
            min_date_to_delete: str date of the min start date
        """
        min_date_to_delete = None
        data_produced_field = {"field": self.data_time_start_field_name}

        search = self.raw_data.search().filter("term", reportName=local_report_name)
        search.aggs.metric("data_produced", "min", **data_produced_field)
        search = search[0]
        self.logger.debug("[%s] min date : %s", local_report_name, search)

        res = search.execute()
        self.logger.debug("[%s] min date result: %s", local_report_name, res)

        min_date_to_delete = datetime.fromtimestamp(
            res.aggregations.data_produced["value"] / 1000
        )
        return min_date_to_delete

    def get_next_report(self, sat_id, local_report_name):
        """Get the next report name from the given report name.
        As report name fisrt date is the report availiabiliy
        the next report is the next availiabiliy.
        If there is no next report the next report name is set to wildcard "*"

        Args:
            local_report_name (str): the report name to inspect from

        Returns:
            next_repport_name: str name of the next report
        """
        next_repport_name = None
        search = (
            self.raw_data.search()
            .filter("term", satellite_id=sat_id)
            .filter("range", reportName={"gt": local_report_name})
            .sort("reportName")
            .params(size=1)
        )
        self.logger.debug("[%s] next report query : %s", local_report_name, search)
        res = search.execute()
        self.logger.debug("[%s] next report query result : %s", local_report_name, res)
        res = list(res)
        if res:
            next_repport_name = res[0].reportName
        return next_repport_name

    def get_to_be_consolidated_raw_data(self, report_name, max_date):
        """get the list of raw data to be consolidated form a report.
        All of raw data lower than max_date.

        Args:
            report_name (str): the report to find raw data
            max_date (str): the limit date to accept

        Returns:
            list: a list of raw data
        """
        data_time_start_range = {self.data_time_start_field_name: {"lt": max_date}}

        if max_date == "*":
            search = self.raw_data.search().filter("term", reportName=report_name)
        else:
            search = (
                self.raw_data.search()
                .filter("term", reportName=report_name)
                .filter(
                    "range",
                    **data_time_start_range,
                )
            )
        self.logger.debug("[%s] to consolidate query : %s", report_name, search)
        search = search.params(ignore=404)

        # Dangerous usage of scan
        mp_consolidate_list = list(search.scan())

        self.logger.debug(
            "[%s] to consolidate query result list: %s",
            report_name,
            mp_consolidate_list,
        )
        return mp_consolidate_list

    def get_to_delete_consolidated_data(self, sat_id, min_date, max_date):
        """get the list of raw data to be deleted form the database.
        All of raw data greter than or equal min_date and lower than max_date.

        Args:
            min_date (str): the lower or equal limit date to accept
            max_date (str): the uper limit date to accept

        Returns:
            list: a list of consolidated data
        """
        if max_date == "*":
            data_time_start_range = {self.data_time_start_field_name: {"gte": min_date}}
            cleaner = (
                self.consolidated_data.search()
                .filter("term", satellite_unit=sat_id)
                .filter(
                    "range",
                    **data_time_start_range,
                )
            )
        else:
            data_time_start_range = {
                self.data_time_start_field_name: {
                    "gte": min_date,
                    "lt": max_date,
                }
            }
            cleaner = (
                self.consolidated_data.search()
                .filter("term", satellite_unit=sat_id)
                .filter(
                    "range",
                    **data_time_start_range,
                )
            )
        cleaner = cleaner.params(ignore=404)
        self.logger.debug("To delete query : %s", cleaner)
        datatake_delete_list = list(cleaner.scan())
        self.logger.debug("To delete query result : %s", datatake_delete_list)
        return datatake_delete_list

    def get_input_documents(self, message: MAASMessage) -> list[str]:
        """Get the input documents. Can be overriden for custom behaviour

        Args:
            message (maas_model.MAASMessage): input message

        Returns:
            list[str]: list of documents id (path of mp file in this particular case)
        """
        return message.document_ids

    def consolidate_data_from_raw_data(self, raw_data: MAASRawDocument) -> MAASDocument:
        """consolidate the raw data

        Args:
            raw_document (raw_data): the raw data to consolidate

        Returns:
            consolidated_data: the consolidated data
        """

        # use specific consolidation method depending on type
        if self.consolidated_data_type == "CdsDatatake":
            yield self.consolidtate_cdsdatatake_from_mpproduct(raw_data)
        if self.consolidated_data_type == "CdsCompleteness":
            yield from self.consolidtate_cdscompleteness_from_mpproduct(raw_data)
        elif self.consolidated_data_type == "CdsDownlinkDatatake":
            yield self.consolidate_cdsdownlinkdatatake_from_mpallproduct(raw_data)
        elif self.consolidated_data_type == "CdsHktmAcquisitionCompleteness":
            yield self.consolidate_cdshktmacquisitioncompleteness_from_mphktmacquisitionproduct(
                raw_data
            )
        elif self.consolidated_data_type == "CdsHktmProductionCompleteness":
            yield (
                self.consolidate_cdshktmproductioncompleteness_from_mphktmdownlink(
                    raw_data
                )
            )
        else:
            self.logger.warning(
                "Unknow type for consolidation : %s", self.consolidated_data_type
            )

    @anomaly_link
    def consolidtate_cdsdatatake_from_mpproduct(
        self, mp_product: MpProduct
    ) -> MAASDocument:
        """generate a CDSDatatake from a MPProduct

        Args:
            mp_product (raw_data): the MPProduct to consolidate

        Returns:
            consolidated_data: the consolidated CDSDatatake
        """
        # NOT_RECORDING are test file
        if mp_product.timeliness == "NOT_RECORDING":
            return None

        cds_datatake = self.consolidated_data()

        # Get application date
        raw_document_application_date = datestr_to_utc_datetime(
            mp_product.reportName[16:31]
        )

        cds_datatake.name = mp_product.reportName
        cds_datatake.key = f"{mp_product.satellite_id}-{mp_product.datatake_id}"
        cds_datatake.meta.id = cds_datatake.key
        cds_datatake.datatake_id = mp_product.datatake_id
        if mp_product.satellite_id.startswith("S1"):
            cds_datatake.hex_datatake_id = (
                hex(int(mp_product.datatake_id, 10)).replace("0x", "").upper()
            )
        cds_datatake.satellite_unit = mp_product.satellite_id
        cds_datatake.mission = mp_product.satellite_id[:2]
        cds_datatake.observation_time_start = mp_product.observation_time_start
        cds_datatake.observation_duration = mp_product.observation_duration * 1000

        # Only S2 have observation_time_stop for S1 observation_time_stop must be computed
        if mp_product.observation_time_stop:
            cds_datatake.observation_time_stop = mp_product.observation_time_stop
        else:
            cds_datatake.observation_time_stop = (
                mp_product.observation_time_start
                + timedelta(milliseconds=mp_product.observation_duration)
            )

        # Only S1 have l0_sensing
        if mp_product.l0_sensing_duration:
            cds_datatake.l0_sensing_duration = mp_product.l0_sensing_duration * 1000
            cds_datatake.l0_sensing_time_start = mp_product.l0_sensing_time_start

            cds_datatake.l0_sensing_time_stop = (
                mp_product.l0_sensing_time_start
                + timedelta(milliseconds=mp_product.l0_sensing_duration)
            )

        # Only S2 have number_of_scenes
        if mp_product.number_of_scenes:
            cds_datatake.number_of_scenes = mp_product.number_of_scenes

        cds_datatake.absolute_orbit = (
            mp_product.absolute_orbit.lstrip("0")
            if mp_product.absolute_orbit is not None
            else None
        )
        cds_datatake.relative_orbit = (
            mp_product.relative_orbit.lstrip("0")
            if mp_product.relative_orbit is not None
            else None
        )

        # Only S1 have polarization
        if mp_product.polarization:
            cds_datatake.polarization = mp_product.polarization

        if mp_product.timeliness:
            cds_datatake.timeliness = mp_product.timeliness

        cds_datatake.instrument_mode = mp_product.instrument_mode

        # Only S1 have instrument_swath
        if mp_product.instrument_swath:
            cds_datatake.instrument_swath = mp_product.instrument_swath

        cds_datatake.application_date = raw_document_application_date

        return cds_datatake

    def consolidtate_cdscompleteness_from_mpproduct(
        self, mp_product: MpProduct
    ) -> MAASDocument:
        """generate a CdsCompleteness from a MPProduct

        Args:
            mp_product (raw_data): the MPProduct to consolidate

        Returns:
            consolidated_data: the consolidated CdsCompleteness
        """

        # NOT_RECORDING are test file
        if mp_product.timeliness == "NOT_RECORDING":
            return None

        for prip_name in self.prip_service_for_mp(mp_product):

            cds_completeness = self.consolidtate_cdsdatatake_from_mpproduct(mp_product)
            cds_completeness.prip_name = prip_name

            yield cds_completeness

    def consolidate_cdsdownlinkdatatake_from_mpallproduct(
        self, mp_all_product: MpAllProduct
    ) -> MAASDocument:
        """generate a CDSDownlinkDatatake from a MPALLProduct

        Args:
            mp_all_product (raw_data): the MpAllProduct to consolidate

        Returns:
            cds_downlink_datatake: the consolidated CdsDownlinkDatatake
        """
        cds_downlink_datatake = self.consolidated_data()

        # Get application date
        raw_document_application_date = datestr_to_utc_datetime(
            mp_all_product.reportName[16:31]
        )

        cds_downlink_datatake.reportName = mp_all_product.reportName
        cds_downlink_datatake.satellite_unit = mp_all_product.satellite_id
        cds_downlink_datatake.mission = mp_all_product.mission
        cds_downlink_datatake.datatake_id = mp_all_product.datatake_id
        cds_downlink_datatake.effective_downlink_start = (
            mp_all_product.effective_downlink_start
        )
        cds_downlink_datatake.effective_downlink_stop = (
            mp_all_product.effective_downlink_stop
        )
        cds_downlink_datatake.acquisition_start = mp_all_product.acquisition_start
        cds_downlink_datatake.acquisition_stop = mp_all_product.acquisition_stop
        cds_downlink_datatake.downlink_duration = mp_all_product.downlink_duration
        cds_downlink_datatake.latency = mp_all_product.latency
        cds_downlink_datatake.station = mp_all_product.station
        cds_downlink_datatake.downlink_polarization = (
            mp_all_product.downlink_polarization
        )
        cds_downlink_datatake.downlink_absolute_orbit = (
            mp_all_product.downlink_absolute_orbit
        )
        cds_downlink_datatake.acquisition_absolute_orbit = mp_all_product.absolute_orbit
        cds_downlink_datatake.acquisition_relative_orbit = mp_all_product.relative_orbit
        cds_downlink_datatake.channel = mp_all_product.channel
        cds_downlink_datatake.partial = mp_all_product.partial
        cds_downlink_datatake.updateTime = datetime.now(tz=timezone.utc)
        cds_downlink_datatake.meta.id = mp_all_product.meta.id
        cds_downlink_datatake.application_date = raw_document_application_date

        # MP all can have multiple session_id but they are splitted just before
        # cds downlink datatake consolidation, so at this point
        # the list il always of size 1
        if mp_all_product.session_id is not None:
            session_id = mp_all_product.session_id[0]

            cds_downlink_datatake.session_id = (
                session_id[7:] if session_id.startswith("DCS_0X_") else session_id
            )
        return cds_downlink_datatake

    @staticmethod
    def generate_downlink_datatake_id(mp_all) -> str:
        """(Re)generate the mp_all id, useful for splitted mp_all
        that now have each a different station and session_id than the
        original raw data

        Args:
            mp_all (MpAllProdudct): Splitted mp all product

        Returns:
            str: unique identifier
        """

        # Same id fields as raw data mp all product for consistency
        id_fields = [
            "satellite_id",
            "mission",
            "datatake_id",
            "effective_downlink_start",
            "station",
            "channel",
            "reportName",
        ]
        mp_all = mp_all.to_dict()
        md5 = hashlib.md5()
        for id_field in id_fields:
            md5.update(str(mp_all[id_field]).encode())
        return md5.hexdigest()

    def consolidate_cdshktmacquisitioncompleteness_from_mphktmacquisitionproduct(
        self, mp_hktm_acquisition_product: MpHktmAcquisitionProduct
    ) -> MAASDocument:
        """generate a CdsHktmAcquisitionCompleteness from a MpHktmAcquisitionProduct

        Args:
            mp_hktm_acquisition_product (raw_data): the MpHktmAcquisitionProduct to consolidate

        Returns:
            cds_downlink_datatake: the consolidated CdsHktmAcquisitionCompleteness
        """
        cds_hktm_acquisition_completeness = self.consolidated_data()

        cds_hktm_acquisition_completeness.ingestionTime = datetime.now(tz=timezone.utc)
        cds_hktm_acquisition_completeness.reportName = (
            mp_hktm_acquisition_product.reportName
        )
        cds_hktm_acquisition_completeness.interface_name = (
            mp_hktm_acquisition_product.interface_name
        )
        cds_hktm_acquisition_completeness.channel = mp_hktm_acquisition_product.channel
        cds_hktm_acquisition_completeness.session_id_full = (
            mp_hktm_acquisition_product.session_id
        )
        cds_hktm_acquisition_completeness.absolute_orbit = (
            mp_hktm_acquisition_product.absolute_orbit
        )
        cds_hktm_acquisition_completeness.satellite_unit = (
            mp_hktm_acquisition_product.satellite_id
        )
        cds_hktm_acquisition_completeness.mission = (
            mp_hktm_acquisition_product.satellite_id[:2]
        )
        cds_hktm_acquisition_completeness.ground_station = (
            mp_hktm_acquisition_product.ground_station
        )
        cds_hktm_acquisition_completeness.execution_time = (
            mp_hktm_acquisition_product.execution_time
        )
        cds_hktm_acquisition_completeness.production_service_name = (
            mp_hktm_acquisition_product.production_service_name
        )
        cds_hktm_acquisition_completeness.production_service_type = (
            mp_hktm_acquisition_product.production_service_type
        )
        cds_hktm_acquisition_completeness.meta.id = mp_hktm_acquisition_product.meta.id

        cadip_completeness = None
        edrs_completeness = None
        session_id_full = cds_hktm_acquisition_completeness.session_id_full

        if session_id_full is None:
            self.logger.error(
                "session id format. Default to full session id format for %s",
                cds_hktm_acquisition_completeness,
            )

            cds_hktm_acquisition_completeness.session_id = None

        # CADIP session has a session id with the format begining with the satellite
        elif session_id_full.startswith("DCS_0X_"):
            self.logger.debug("HKTM associated to a CADIP acquisition")

            # Removing the HKTM specific prefix to the session_id
            cds_hktm_acquisition_completeness.session_id = session_id_full[7:]
            session_id = cds_hktm_acquisition_completeness.session_id

            session_criteria = Q("term", session_id=session_id)
            status_criteria = {"global_status": "OK"}

            exact_count = self.count_hktm_acquisition_completeness(
                CdsCadipAcquisitionPassStatus,
                session_criteria,
                status_criteria,
            )

            self.logger.debug(
                "HKTM acqs found by session-id: %s (%s)", exact_count, session_id
            )

            cadip_completeness = 1 if exact_count == 1 else 0

            date_count = None
            if not cadip_completeness:
                # No match using sessionid, search by date instead
                session_id_date = datetime.strptime(session_id[4:18], r"%Y%m%d%H%M%S")
                tolerance_delta = timedelta(minutes=self.TOLERANCE_IN_MINUTES)
                session_criteria = Q(
                    "range",
                    delivery_start={
                        "lte": session_id_date + tolerance_delta,
                        "gte": session_id_date - tolerance_delta,
                    },
                )
                date_count = self.count_hktm_acquisition_completeness(
                    CdsCadipAcquisitionPassStatus,
                    session_criteria,
                    status_criteria,
                    orbit_filter=session_id[18:],
                )

                cadip_completeness = 1 if date_count >= 1 else 0
                self.logger.debug(
                    "HKTM acqs found by date: %s (%s)", date_count, session_id
                )

            anomaly_key = lambda hktm: "_".join(
                [
                    hktm.satellite_unit,
                    "X-Band",
                    str(hktm.absolute_orbit),
                    hktm.ground_station,
                ]
            )

        # EDRS session has a session id with the format begining with L[YEAR]
        elif session_id_full[0] == "L":
            self.logger.debug("HKTM associated to a EDRS acquisition")

            cds_hktm_acquisition_completeness.session_id = session_id_full
            session_id = cds_hktm_acquisition_completeness.session_id

            session_criteria = Q("term", link_session_id=session_id)
            status_criteria = {"total_status": "NOK"}  # will be negated

            exact_count = self.count_hktm_acquisition_completeness(
                CdsEdrsAcquisitionPassStatus,
                session_criteria,
                status_criteria,
            )

            edrs_completeness = 1 if exact_count >= 1 else 0

            anomaly_key = lambda hktm: "_".join(
                [
                    hktm.satellite_unit,
                    "EDRS",
                    session_id,
                    hktm.ground_station,
                ]
            )
        else:
            self.logger.warning(
                "[%s] Unrecognized session id format. Default to full session id format",
                session_id_full,
            )

            cds_hktm_acquisition_completeness.session_id = session_id_full

        cds_hktm_acquisition_completeness.cadip_completeness = cadip_completeness
        cds_hktm_acquisition_completeness.edrs_completeness = edrs_completeness

        self._apply_anomalies(cds_hktm_acquisition_completeness, key=anomaly_key)

        return cds_hktm_acquisition_completeness

    def consolidate_cdshktmproductioncompleteness_from_mphktmdownlink(
        self, mp_hktm_downlink: MpHktmDownlink
    ) -> MAASDocument:
        """generate a CdsHktmProductionCompleteness from a MpHktmDownlink

        Args:
            mp_hktm_downlink (raw_data): the MpHktmDownlink to consolidate

        Returns:
            cds_hktm_production_completeness: the consolidated CdsHktmProductionCompleteness
        """

        if mp_hktm_downlink.downlink_mode != "DOWNLINK_HKTM_SAD":
            return

        cds_hktm_production_completeness = self.consolidated_data()

        # Get application date
        raw_document_application_date = datestr_to_utc_datetime(
            mp_hktm_downlink.reportName[16:31]
        )
        cds_hktm_production_completeness.ingestionTime = datetime.now(tz=timezone.utc)

        cds_hktm_production_completeness.reportName = mp_hktm_downlink.reportName
        cds_hktm_production_completeness.satellite_unit = mp_hktm_downlink.satellite_id
        cds_hktm_production_completeness.mission = mp_hktm_downlink.mission
        cds_hktm_production_completeness.datatake_id = mp_hktm_downlink.datatake_id
        cds_hktm_production_completeness.effective_downlink_start = (
            mp_hktm_downlink.effective_downlink_start
        )
        cds_hktm_production_completeness.effective_downlink_stop = (
            mp_hktm_downlink.effective_downlink_stop
        )
        cds_hktm_production_completeness.acquisition_start = (
            mp_hktm_downlink.acquisition_start
        )
        cds_hktm_production_completeness.acquisition_stop = (
            mp_hktm_downlink.acquisition_stop
        )
        cds_hktm_production_completeness.downlink_duration = (
            mp_hktm_downlink.downlink_duration
        )
        cds_hktm_production_completeness.latency = mp_hktm_downlink.latency
        cds_hktm_production_completeness.station = mp_hktm_downlink.station
        cds_hktm_production_completeness.downlink_absolute_orbit = (
            mp_hktm_downlink.absolute_orbit
        )
        cds_hktm_production_completeness.partial = mp_hktm_downlink.partial
        cds_hktm_production_completeness.updateTime = datetime.now(tz=timezone.utc)
        cds_hktm_production_completeness.meta.id = mp_hktm_downlink.meta.id

        cds_hktm_production_completeness.application_date = (
            raw_document_application_date
        )

        count = self.count_produced_hktm(mp_hktm_downlink.effective_downlink_start)

        cds_hktm_production_completeness.completeness = 1 if count > 0 else 0

        return cds_hktm_production_completeness

    def count_produced_hktm(self, effective_downlink_start):
        """
        Compute the completeness of production based on products.


        Args:
            effective_downlink_start (datetime): The planned date around which a
            cds-product should have its sensing start date in the nominal case

        Returns:
            int: The count of document that met the criteria

        """
        tolerance_value = timedelta(minutes=self.tolerance_value)

        search = (
            CdsProduct.search()
            .filter("term", mission="S2")
            .filter("term", product_type="PRD_HKTM__")
            .filter(
                "range",
                sensing_start_date={"lte": effective_downlink_start + tolerance_value},
            )
            .filter(
                "range",
                sensing_start_date={"gte": effective_downlink_start - tolerance_value},
            )
        )

        count = search.count()

        return count

    def count_hktm_acquisition_completeness(
        self, acquisition_class, session_criteria, status_criteria, orbit_filter=None
    ):
        """
        Compute the completeness of acquisitions based on session and status criteria.


        Args:
            acquisition_class (Type): The Opensearch DSL class representing the
                type of acquisitions to search.
            session_criteria (Request): session specific criteria
            status_criteria (dict): status specific criteria
            orbit_filter (string): Optional filter for restrict to a single orbit

        Returns:
            int: The count of document that met the criteria

        """
        class_name = acquisition_class.__name__

        if class_name == "CdsCadipAcquisitionPassStatus":
            status_filter = Q("term", **status_criteria)

        elif class_name == "CdsEdrsAcquisitionPassStatus":
            # every row that is not NOK is considered OK for EDRS
            status_filter = Q("bool", must_not=[Q("term", **status_criteria)])

        session_filter = session_criteria
        combined_query = Q("bool", filter=[status_filter, session_filter])

        query = acquisition_class.search().query(combined_query)
        count = query.count()

        if orbit_filter:
            orbits = (acq.session_id[18:] for acq in query.execute())
            filtered_orbits = set(orbit for orbit in orbits if orbit == orbit_filter)
            count = len(filtered_orbits)

        return count

    def shall_report(self, document: MAASDocument) -> bool:
        """Overide to store future entity identifiers

        Args:
            document (MAASDocument): consolidated document

        Returns:
            bool: always True
        """
        report_status = super().shall_report(document)

        if getattr(document, self.data_time_start_field_name) > datetime.now(
            tz=timezone.utc
        ):
            # store identifier of future entities to later filter out messages
            self.future_ids.add(document.meta.id)

        return report_status

    def _generate_reports(self):
        """Override to create 2 reports: one for products and one for publications


        Yields:
            EngineReport: report
        """
        for report in super()._generate_reports():
            if report.action.startswith("delete."):
                self.logger.debug("Delete actions are not reported  : %s", report)
                continue

            # create a set of past or present identifiers
            non_future_ids = set(report.data_ids) - self.future_ids

            if non_future_ids:
                self.logger.debug(
                    "Create reports for past entities: %s", non_future_ids
                )

                # report for product updates
                yield EngineReport(
                    f"{report.action}-product",
                    list(non_future_ids),
                    report.document_class,
                    document_indices=report.document_indices,
                    chunk_size=self.chunk_size,
                )

                # report for publication updates
                yield EngineReport(
                    f"{report.action}-publication",
                    list(non_future_ids),
                    report.document_class,
                    document_indices=report.document_indices,
                    chunk_size=self.chunk_size,
                )

            else:
                self.logger.debug("All entities start in future time.")

            # report anyway so expected can be initialized for future entities
            yield report

    def _populate_ticket_cache(self, mp_products):
        """
        Fill the ticket cache

        Args:
            mp_products (list): list of raw mp products
        """

        self._cams_tickets_dict = {}

        if self.consolidated_data_type == "CdsHktmAcquisitionCompleteness":
            self._populate_by_CdsHktmAcquisitionCompleteness(mp_products)
            return

        if not self.consolidated_data_type == "CdsDatatake":
            self.logger.debug(
                "No anomaly correlation on %s", self.consolidated_data_type
            )
            return

        tickets = (
            CdsCamsTickets()
            .search()
            .filter(
                "terms",
                datatake_ids=[
                    f"{mp_product.satellite_id}-{mp_product.datatake_id}"
                    for mp_product in mp_products
                ],
            )
            .sort({"updated": {"order": "asc"}})
            .params(size=10000)
            .execute()
        )

        for ticket in tickets:
            for datatake_id in ticket.datatake_ids:
                if datatake_id in self._cams_tickets_dict:
                    self._cams_tickets_dict[datatake_id].append(ticket)
                else:
                    self._cams_tickets_dict[datatake_id] = [ticket]

    def prip_service_for_mp(self, mp_product: MpProduct):
        if self.COMPLETENESS_CONFIG is None:
            self.COMPLETENESS_CONFIG = self.load_completeness_configuration()

        if mp_product.satellite_id not in self.COMPLETENESS_CONFIG:
            self.logger.warning(
                "Missingt configuration completeness for %s", mp_product.satellite_id
            )
            return []

        else:
            return self.COMPLETENESS_CONFIG[mp_product.satellite_id]

    @staticmethod
    def load_completeness_configuration():
        """load the completeness configuration

        Returns:
            dict: contain level mapping for product_type
            ex: "MSI_L2A_TC": "L2_",
                "PRD_HKTM__": "L0_",
                "AUX_SADATA": "AUX",
                ...
        """
        # OPTI: Switch later to the date
        search_request = MaasConfigCompleteness.search().filter("term", activated=True)
        request_result: list[MaasConfigCompleteness] = search_request.params(
            size=1000
        ).execute()

        configuration = {}

        for conf in request_result:
            if conf.satellite_unit not in configuration:
                configuration[conf.satellite_unit] = []
            configuration[conf.satellite_unit].append(conf.prip_name)

        return configuration
