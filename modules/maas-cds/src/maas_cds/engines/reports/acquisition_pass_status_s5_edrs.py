"""
acquisition pass status engines for consolidation
"""

import copy
import hashlib

from datetime import datetime, timezone
from maas_engine.engine.base import EngineReport

from typing import List, Dict, Any, Generator

from opensearchpy import Q
from maas_engine.engine.rawdata import DataEngine
from maas_cds.engines.reports.anomaly_impact import (
    AnomalyImpactMixinEngine,
)

from maas_cds.model import (
    CdsAcquisitionPassStatus,
    CdsEdrsAcquisitionPassStatus,
    ApsEdrs,
    ApsProduct,
)


def get_hash(fields: List[str], input_document: Any):
    """Calculate an hash using the value of different field in an input document

    Args:
        fields (List[str]): field name to use for hash calculation
        input_document (Any): input document containing the fields
    Raises:
        ValueError: triggered when field used to calculate
        hash are missing from document

    Returns:
        str: calculated hash
    """
    md5 = hashlib.md5()
    for name in fields:
        try:
            md5.update(str(input_document[name]).encode())
        except KeyError as error:
            raise ValueError(
                f"Field {name} is missing from {input_document}"
            ) from error
    return md5.hexdigest()


class AcquisitionPassStatusConsolidatorS5AndEDRS(AnomalyImpactMixinEngine, DataEngine):
    """
    Consolidate X-Band acquisition pass status from S5 and EDRS raw data
    """

    ENGINE_ID = ""
    RAW_DATA_TYPE: Any = None
    CONSOLIDATED_DATA_TYPE: Any = None

    def __init__(
        self,
        args=None,
        send_reports=False,
        chunk_size=128,
        hktm_chunk_size=128,
    ):
        super().__init__(args, send_reports=send_reports, chunk_size=chunk_size)
        self.periodicity_dict = {"daily": 1, "weekly": 2, "monthly": 3}
        self.extra_document_to_consolidate: Dict[Dict[List]] = {}
        self.hktm_related_products = []
        self.hktm_chunk_size = hktm_chunk_size

    def get_consolidated_aps_documents(
        self, consolidated_id_list: List[str]
    ) -> List[Any]:
        """Retrieve from DB, the document associated to the ids given in parameter.
           If model does not already exist, it is created
        Args:
            consolidated_id_list (List[str]): list of consolidated id string

        Returns:
            List[Any]:
            return a list of consolidated documents
        """
        consolidated_documents_list = []
        document_list = self.CONSOLIDATED_DATA_TYPE.mget_by_ids(
            consolidated_id_list, ignore_missing_index=True
        )
        for i, document in enumerate(document_list):
            if document is None:
                # CONSOLIDATED_DATA_TYPE is callable in inherited class
                # pylint: disable=E1102
                document = self.CONSOLIDATED_DATA_TYPE()
                document.meta.id = consolidated_id_list[i]
            consolidated_documents_list.append(document)
        return consolidated_documents_list

    def preprocess_input_documents(self, input_documents: List[Any]) -> List[ApsEdrs]:
        """Allow sub-class to perform some operation on input documents before consolidation"""
        return input_documents

    def postprocess_consolidated_documents(self, consolidated_document_list: List[Any]):
        """Allow sub-class to perform some actions on consolidated documents before yielding them"""
        return consolidated_document_list

    def consolidate_from_raw_data(self, input_documents: List[Any]) -> List[Any]:
        """Main function of the engine responsible to populate a list
        with consolidated APS data DAO using the input documents

        Args:
            input_document (List[ANY]): raw data to ingest

        Returns:
            List[Any]:
            list of filled consolidated documents DAO
        """
        input_documents = self.preprocess_input_documents(input_documents)

        consolidated_id_list = []

        # Retrieve list of consolidated ID
        for input_document in input_documents:
            consolidated_id_list.append(self.get_consolidated_id(input_document))

        # Retrieve the consolidated documents using the retrieved ids
        consolidated_document_list = self.get_consolidated_aps_documents(
            consolidated_id_list
        )

        # Store the consolidated documents in a dict ( key is the raw id)
        consolidated_documents_dict = {}
        for i, input_doc in enumerate(input_documents):
            consolidated_documents_dict[
                self.get_consolidated_id(input_doc)
            ] = consolidated_document_list[i]

        # populate ticket cache for attachement
        self._populate_ticket_cache(consolidated_document_list)

        consolidated_documents_list = self.fill_and_filter_consolidated_document(
            input_documents, consolidated_documents_dict
        )

        return self.postprocess_consolidated_documents(consolidated_documents_list)

    def get_consolidated_id(self, input_document: Any) -> str:
        """Field from raw data input document are used to create a consolidated data identifier.

        Args:
            input_document (Any): Raw Data document

        Returns:
            str: consolidated data identifier
        """
        # Abstract Class
        raise NotImplementedError()

    def action_iterator(self) -> Generator:
        """override

        Iter throught input documents and find products who are inside
        Then add informations on these products

        Yields:
            Iterator[Generator]: bulk actions
        """
        consolidated_document_list = self.consolidate_from_raw_data(
            self.input_documents
        )

        # if self.payload.document_class == "ApsEdrs":
        #     yield from self.update_hktm(
        #         self.payload.document_class, consolidated_document_list
        #     )

        for document in consolidated_document_list:
            self.hktm_related_products.append(document)
            self.report(document)
            yield document.to_bulk_action()

    def fill_report_name(
        self, report_type: str, report_name: str, consolidated_document: Any
    ):
        """This function fill the proper report_name field of the consolidated document
        depending on the report type

        Args:
            report_type (str): report type ( daily,monthly,weekly)
            report_name (str): name of the raw data file ingested
            consolidated_document (Any): consolidated document about to be filled

        Returns:
            Any: consolidated document with its report name filled
        """
        if report_type == "daily":
            consolidated_document.report_name_daily = report_name
        elif report_type == "weekly":
            consolidated_document.report_name_weekly = report_name
        elif report_type == "monthly":
            consolidated_document.report_name_monthly = report_name
        return consolidated_document

    def fill_and_filter_consolidated_document(
        self,
        raw_data_list: List[Any],
        consolidated_documents_dict: Dict[Any, Any],
    ) -> List[Any]:
        """Fill a dict of consolidated data using a list of raw data.
           also discard creation of some consolidated data in DB if there is already better
           data ( eg: do not ingest daily data for a APS where there is already a monthly one)

        Args:
            raw_data_list (Any): list of raw data to ingest
            consolidated_documents_dict
                    (Dict[Any, Any]):
                    dict of consolidated documents DAO

        Returns:
            List[Any]:
              list of filled consolidated documents DAO
        """
        modified_consolidated_document_set = set()
        for raw in raw_data_list:
            # Not a copy, only use a smaller variable name
            consolid = consolidated_documents_dict[self.get_consolidated_id(raw)]

            # Create or update a consolidated data only if there is ..
            # ..no better consolidated data already in DB
            if (
                not consolid.report_type
                or self.periodicity_dict[consolid.report_type]
                <= self.periodicity_dict[raw.report_type]
            ):
                # Fill the consolidated data using raw data as source
                filled = self.fill_data(raw, consolid)
                if filled:
                    consolid = filled
                    modified_consolidated_document_set.add(
                        self.get_consolidated_id(raw)
                    )
            else:
                self.logger.debug(
                    "data in raw data with report name %s "
                    "has already been consolidated through a document with same data "
                    "but fresher source (eg:monthly vs daily ) in DB with id %s"
                    "only its report_name_%s field will be updated",
                    raw.reportName,
                    consolid.meta.id,
                    raw.report_type,
                )

                consolid = self.fill_report_name(
                    raw.report_type, raw.reportName, consolid
                )
                modified_consolidated_document_set.add(self.get_consolidated_id(raw))

        return [
            consolidated_documents_dict[x] for x in modified_consolidated_document_set
        ]

    def fill_data(
        self,
        raw_data: Any,
        consolidated_document: Any,
    ) -> Any:
        """Fill a consolidated data using a raw data document.

        Args:
            raw_data (Any): raw data to ingest
            consolidated_document
                    (Any): consolidated documents DAO

        Returns:
            Any:  filled consolidated documents DAO
        """
        # Identify the type of consolidate data ( weekly, daily or monthly
        #   and also keep track of the report name)
        consolidated_document.report_type = raw_data.report_type

        consolidated_document = self.fill_report_name(
            raw_data.report_type, raw_data.reportName, consolidated_document
        )

        consolidated_document.updateTime = datetime.now(tz=timezone.utc)

        consolidated_document.fill_common_fields(raw_data)

        return consolidated_document

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
                "CdsEdrsAcquisitionPassStatus",
            )

            yield EngineReport(
                "update.hktm-acquisition",
                [document.meta.id for document in self.hktm_related_products],
                "CdsEdrsAcquisitionPassStatus",
                document_indices=self.get_index_names(self.hktm_related_products),
                chunk_size=self.hktm_chunk_size,
            )


class S5AcquisitionPassStatusConsolidatorEngine(
    AcquisitionPassStatusConsolidatorS5AndEDRS
):
    """
    Consolidate S5 acquisition pass status
    """

    ENGINE_ID = "CONSOLIDATE_S5APS"
    RAW_DATA_TYPE = ApsProduct
    CONSOLIDATED_DATA_TYPE = CdsAcquisitionPassStatus
    ANOMALY_KEY = lambda _, aps: "_".join(
        [aps.satellite_id, "X-Band", aps.downlink_orbit, aps.ground_station]
    )

    def fill_data(
        self,
        raw_data: ApsProduct,
        consolidated_document: CdsAcquisitionPassStatus,
    ) -> CdsAcquisitionPassStatus:
        """Fill a consolidated data using a raw data document.

        Args:
            raw_data (ApsProduct): raw data to ingest
            consolidated_document
                    (CdsAcquisitionPassStatus): consolidated documents DAO

        Returns:
            CdsAcquisitionPassStatus:  filled consolidated documents DAO
        """

        consolidated_document = super().fill_data(raw_data, consolidated_document)

        consolidated_document.ground_station = raw_data.reportName.split("_")[0]

        consolidated_document.from_acq_delivery_timeliness = (
            consolidated_document.calculate_timeliness()
        )

        consolidated_document.delivery_bitrate = (
            consolidated_document.calculate_bitrate(consolidated_document.meta.id)
        )

        self._apply_anomalies(consolidated_document, key=self.ANOMALY_KEY)

        return consolidated_document

    def get_consolidated_id(self, input_document: ApsProduct) -> str:
        """Field from raw data input document are used to create a consolidated data identifier.

        Args:
            input_document (Union[ApsProduct, ApsEdrs]): Raw Data document

        Returns:
            str: consolidated data identifier
        """
        return get_hash(
            [
                "satellite_id",
                "downlink_orbit",
                "planned_data_start",
                "antenna_id",
            ],
            input_document,
        )


class EDRSAcquisitionPassStatusConsolidatorEngine(
    AcquisitionPassStatusConsolidatorS5AndEDRS
):
    """
    Consolidate EDRS acquisition pass status
    """

    ENGINE_ID = "CONSOLIDATE_APS_EDRS"
    RAW_DATA_TYPE = ApsEdrs
    CONSOLIDATED_DATA_TYPE = CdsEdrsAcquisitionPassStatus
    ANOMALY_KEY = lambda _, aps: "_".join(
        [aps.satellite_id, "EDRS", aps.link_session_id, aps.ground_station]
    )

    GROUND_STATION_DICT = {
        "BFLGS": "FLGS",
        "FLGS": "BFLGS",
        "RDGS": "HDGS",
        "HDGS": "RDGS",
    }
    SAT_GROUND_STATION_DICT = {
        "S1A": ("RDGS", "HDGS"),
        "S1B": ("RDGS", "HDGS"),
        "S2A": ("FLGS", "BFLGS"),
        "S2B": ("FLGS", "BFLGS"),
    }

    def __init__(
        self, args=None, send_reports=False, chunk_size=128, hktm_chunk_size=None
    ):
        super().__init__(
            args,
            send_reports=send_reports,
            chunk_size=chunk_size,
            hktm_chunk_size=hktm_chunk_size,
        )
        self.deduced_ground_station = {}

    def fill_data(
        self,
        raw_data: ApsEdrs,
        consolidated_document: CdsEdrsAcquisitionPassStatus,
    ) -> CdsEdrsAcquisitionPassStatus | None:
        """Fill a consolidated data using a raw data document.

        Args:
            raw_data (ApsProduct): list of raw data to ingest
            consolidated_document
                    (CdsAcquisitionPassStatus): list of consolidated documents DAO

        Returns:
            CdsAcquisitionPassStatus: filled consolidated documents DAO
        """
        # Case where ground_station was not present in the raw data about to be consolidated
        # The ground station to use for consolidation was deduced from other raw data
        ground_station_to_use = self.get_ground_station(raw_data)

        # filter out pass without enough attribute to search for anomaly correlation
        if not all(
            [
                raw_data.satellite_id,
                raw_data.link_session_id,
                ground_station_to_use,
            ]
        ):
            self.logger.warning(
                "Won't consolidate incomplete ApsEdrs entry: %s ", raw_data
            )
            return None

        consolidated_document = super().fill_data(raw_data, consolidated_document)

        consolidated_document.ground_station = ground_station_to_use

        self._apply_anomalies(consolidated_document, key=self.ANOMALY_KEY)

        return consolidated_document

    def deduce_ground_station_from_other_documents(
        self, link_session_id: str, report_type: str
    ) -> str | None:
        """Look for other ApsEdrs document either in the chunk or in the DB which have the
        same link_session_id and a defined ground_station to deduce the ground_station to use
        for the document which has its field ground_station not defined

        Args:
            link_session_id (str): link_session_id to use when looking for other
                                   document ground_stations
            report_type (str): report type ( daily,weekly or monthly) of the docuemnt
        Returns:
            str|None: deduced ground station to use or None if it could not deduce it
        """

        # Sometimes ground station is not written in the raw data
        # We use the link_session_id of the raw data without ground station
        # to find another raw data with the same link_session_id and the same report type
        # to get its ground_station. If one has ground station A
        #  then the other will necessarly have ground station B
        # ( refer to the dict ground_station_dict )

        # Step 1 : Look for other raw document with same link_session_id and ...
        # ...report_type in the chunk
        for document in self.input_documents:
            if (
                document["link_session_id"] == link_session_id
                and document["report_type"] == report_type
                and "ground_station" in document
                and document["ground_station"] != ""
            ):
                self.logger.debug(
                    "Found a document with same link_session_id and report type"
                    " in the chunk and it has ground_station %s."
                    "  %s will be used for our document",
                    document["ground_station"],
                    self.GROUND_STATION_DICT[document["ground_station"]],
                )

                return self.GROUND_STATION_DICT[document["ground_station"]]

        # Step 2 : Look for other raw document with same link_session_id in the DB
        response = (
            ApsEdrs.search()
            .filter("term", link_session_id=link_session_id)
            .filter("term", report_type=report_type)
            .filter("bool", must=[Q("exists", field="ground_station")])
            .execute()
        )

        if len(list(response)) == 1:
            other_ground_station = list(response)[0]["ground_station"]

            self.logger.debug(
                "Another ApsEdrs document with link_session_id : "
                "%s and report_type: %s has been found in DB with ground station %s. %s"
                " will be used for the new ApsEdrs document",
                link_session_id,
                report_type,
                other_ground_station,
                self.GROUND_STATION_DICT[other_ground_station],
            )

            return self.GROUND_STATION_DICT[other_ground_station]

        return None

    def get_consolidated_id(self, input_document: ApsEdrs) -> str:
        """Field from raw data input document are used to create a consolidated data identifier.

        Args:
            input_document (ApsEdrs): Raw Data document

        Returns:
            str: consolidated data identifier
        """
        return get_hash(["link_session_id", "ground_station"], input_document)

    def get_ground_station(
        self,
        raw_data: ApsEdrs,
    ) -> str:
        """During process to get the consolidated id, the ground station field may
        have been deduced from other documents if it was missing.
        Instead of reading the ground_station field of the raw_data, we check if it was not deduced

        Args:
            raw_data (ApsEdrs): raw_data_document about to be ingested

        Returns:
            str: ground station string to use
        """
        if raw_data.meta.id in self.deduced_ground_station:
            return self.deduced_ground_station[raw_data.meta.id]
        else:
            return raw_data.ground_station

    def preprocess_input_documents(
        self, input_documents: List[ApsEdrs]
    ) -> List[ApsEdrs]:
        """This function is used to pre-process the input documents and
        fix any issues concerning the missing ground_station field by either deducing it or
        creating 2 consolidated documents with both ground stations

        Args:
            input_documents (List[ApsEdrs]): list of input documents received by the engine

        Returns:
            List[ApsEdrs]: Input ApsEdrs documents with the
            ground_station field fixed on each element
        """
        for input_document in input_documents:
            if "ground_station" not in input_document:
                self.logger.debug(
                    "APSEdrs document %s has no ground_station, it is"
                    " checked if another APSEdrs document with the same link_session_id"
                    " : %s exists and has a ground_station",
                    input_document.meta.id,
                    input_document["link_session_id"],
                )

                res = self.deduce_ground_station_from_other_documents(
                    input_document["link_session_id"], input_document["report_type"]
                )

                if res:
                    self.logger.debug(
                        "%s will be used for the new APSEdrs document %s",
                        res,
                        input_document.meta.id,
                    )
                    input_document.ground_station = res
                    self.deduced_ground_station[input_document.meta.id] = res
                else:
                    # Neither nominal nor backup ground station is
                    #  written in the raw data file for a given link_session_id
                    sat_id = input_document["satellite_id"]
                    ground_stations_guessed = (
                        self.SAT_GROUND_STATION_DICT[sat_id][0],
                        self.SAT_GROUND_STATION_DICT[sat_id][1],
                    )

                    self.logger.warning(
                        "We have no info to deduce the ground_station for document "
                        "with id:%s with link_session_id:%s"
                        ". 2 Consolidated documents will be created for link_session_id "
                        "with the following ground stations %s - %s",
                        input_document.meta.id,
                        input_document["link_session_id"],
                        ground_stations_guessed[0],
                        ground_stations_guessed[1],
                    )
                    input_document["ground_station"] = ground_stations_guessed[0]
                    self.deduced_ground_station[
                        input_document.meta.id
                    ] = ground_stations_guessed[0]

                    # Create a fictive input document which is a copy of the input document but
                    # with the opposite ground_station and store it for later usage
                    fictive_input_doc = copy.deepcopy(input_document)
                    fictive_input_doc["ground_station"] = ground_stations_guessed[1]
                    self.extra_document_to_consolidate.setdefault(
                        input_document["link_session_id"], {}
                    ).setdefault(fictive_input_doc["ground_station"], []).append(
                        fictive_input_doc
                    )

        return input_documents

    def postprocess_consolidated_documents(
        self,
        consolidated_document_list: List[CdsEdrsAcquisitionPassStatus],
    ) -> List[CdsEdrsAcquisitionPassStatus]:
        """Perform actions on consolidated documents just before yielding them

        Args:
            consolidated_document_list (List[CdsEdrsAcquisitionPassStatus]): ^
            list of consolidated documents

        Returns:
            List[CdsEdrsAcquisitionPassStatus]: list of consolidated documents
            where additional actions may have been performed
        """

        # This code is used when a raw_data has been received without any ground_station for
        #  a specific link_session_id / report type, we have to generate 2 consolidated elements for
        # both ground_stations even if a single raw_data exists for this link_session_id

        # iterate on link_session_id
        for doc_link_session_id_dict in self.extra_document_to_consolidate.values():
            # iterate on ground station
            for fictive_input_doct_list in doc_link_session_id_dict.values():
                # In case there are multiple fictive document about to be created for
                # the same link_session_id / ground_station, we shall only consolidate
                #  the better one( monthly better than weekly etc..) It can happen if
                #  in the same chunk we parse a daily report and a monthly report (or daily/monthly,
                #  weekly/daily,etc..) and all these document have the same defect where
                #  both nominal and redudant ground station field are empty

                # We sort by report type, to consolidate the better one
                fictive_input_doct_list.sort(key=lambda x: x.report_type)

                fictive_best_input_doc = fictive_input_doct_list[-1]

                consolid_id = self.get_consolidated_id(fictive_best_input_doc)

                # check if document with same id already exist in the list of consolidated data about to be yield
                consolid_doc = next(
                    (
                        item
                        for item in consolidated_document_list
                        if item.meta.id == consolid_id
                    ),
                    None,
                )

                # If not then check if it already exist in db
                if consolid_doc is None:
                    consolid_doc = self.CONSOLIDATED_DATA_TYPE.get_by_id(
                        consolid_id, ignore_missing_index=True
                    )

                # If not then we have to create it
                if consolid_doc is None:
                    consolid_doc = self.CONSOLIDATED_DATA_TYPE()
                    consolid_doc.meta.id = consolid_id

                # Overwrite data only if this one fresher than the one in db
                if (
                    "report_type" not in consolid_doc.to_dict()
                    or self.periodicity_dict[consolid_doc.report_type]
                    <= self.periodicity_dict[fictive_best_input_doc.report_type]
                ):
                    # Fill it with the same data as the one which has an associated raw_data
                    consolid_doc.fill_common_fields(fictive_best_input_doc)
                    consolid_doc.updateTime = datetime.now(tz=timezone.utc)

                # Fill the report_name_X (daily,weekly)
                for x in fictive_input_doct_list:
                    consolid_doc["report_name_" + x["report_type"]] = x["reportName"]

                self.logger.info(
                    "A consolidated document id:%s for link_session_id:%s "
                    "report_type:%s with ground_station:%s"
                    " is created using same data as the raw document with id:%s",
                    consolid_id,
                    consolid_doc["link_session_id"],
                    consolid_doc["report_type"],
                    consolid_doc["ground_station"],
                    fictive_best_input_doc.meta.id,
                )

                if consolid_doc not in consolidated_document_list:
                    consolidated_document_list.append(consolid_doc)
        return consolidated_document_list
