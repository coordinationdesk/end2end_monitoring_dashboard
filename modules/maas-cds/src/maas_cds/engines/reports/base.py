"""Base classes for cds report engines"""

import datetime
from itertools import groupby
import string
from typing import Dict

from opensearchpy import MultiSearch
from collections import defaultdict

from maas_engine.engine.rawdata import RawDataEngine
from maas_cds.lib.periodutils import Period, reduce_periods

from maas_cds.model.datatake import CdsDatatake
from maas_cds.model.dataflow import CdsDataflow

from maas_cds.lib.parsing_name import extract_data_from_product_name
from maas_cds.lib.dateutils import get_microseconds_delta

import maas_cds.lib.parsing_name.utils as utils


class BaseProductConsolidatorEngine(RawDataEngine):
    """Group common behaviours about product and publication consolidation"""

    LEVEL_TYPE_MAPPING = None

    # a value in seconds to find the datatake of a product from sensing
    S2_DATATAKE_ATTACHEMENT_DELTA = 15

    def __init__(self, args=None, send_reports=True, min_doi=None, chunk_size=0):
        super().__init__(
            args=args, send_reports=send_reports, min_doi=min_doi, chunk_size=chunk_size
        )
        # a dict storing all product name -> extracted dictionnary (shared between session)
        self.all_data_dict = {}

    @staticmethod
    def load_level_type_mapping():
        """load the product_type level mapping in CdsDataflow index

        Returns:
            dict: contain level mapping for product_type
            ex: "MSI_L2A_TC": "L2_",
                "PRD_HKTM__": "L0_",
                "AUX_SADATA": "AUX",
                ...
        """
        search_request = CdsDataflow.search()
        request_result = search_request.params(size=1000).execute()

        return {
            f"{conf.mission}#{conf.product_type}": conf.level for conf in request_result
        }

    @classmethod
    def get_product_level(cls, mission, product_type) -> str:
        """
        Search the dataflow the correct product level for a mission and product type
        """
        return cls.LEVEL_TYPE_MAPPING.get(
            f"{mission}#{product_type}",
            utils.PRODUCT_LEVEL_MISSING_VALUE,
        )

    def fill_sensing(
        self,
        raw_document,
        document,
        data_dict=None,
        start_key="start_date",
        end_key="end_date",
    ) -> None:
        """
        fill sensing_start_date, sensing_end_date and sensing_duration attributes
        """
        if data_dict is None:
            data_dict = self.extract_data_from_product_name(raw_document.product_name)

        if hasattr(raw_document, "start_date") and raw_document.start_date:
            document.sensing_start_date = raw_document.start_date
        elif start_key in data_dict:
            document.sensing_start_date = data_dict[start_key]

        if hasattr(raw_document, "end_date") and raw_document.end_date:
            document.sensing_end_date = raw_document.end_date
        elif end_key in data_dict:
            document.sensing_end_date = data_dict[end_key]

        document.sensing_duration = get_microseconds_delta(
            document.sensing_start_date, document.sensing_end_date
        )

    def fill_common_attributes(
        self,
        raw_document,
        document,
        data_dict=None,
        start_key="start_date",
        end_key="end_date",
        fill_name=True,
    ) -> dict:
        """Consolidated commun document

        Consolidated commun document from the raw document using the data_dict
        or create a new one from the information in the product name

        Args:
            raw_document (MAASDocument): incoming document
            document (MAASDocument): document to consolidate
            data_dict (dict, optional): [description]. Defaults to None.
            start_key (str, optional): [description]. Defaults to "start_date".
            end_key (str, optional): [description]. Defaults to "end_date".

        Returns:
            dict: orginal data_dict enriched by the metod
        """

        if data_dict is None:
            data_dict = self.extract_data_from_product_name(raw_document.product_name)

        if data_dict:
            self.logger.debug("Extracted data from product name: %s", data_dict)
        else:
            self.logger.warning(
                "No data extracted from product name: %s", raw_document.product_name
            )

        absolute_orbit = data_dict.get("absolute_orbit_number", document.absolute_orbit)
        if absolute_orbit is not None:
            absolute_orbit = str(absolute_orbit).lstrip("0")
        document.absolute_orbit = absolute_orbit

        datatake_id = data_dict.get("datatake_id", document.datatake_id)

        if datatake_id is None:
            datatake_id = utils.DATATAKE_ID_MISSING_VALUE

        if datatake_id is not None and all(c in string.hexdigits for c in datatake_id):
            datatake_id = str(int(datatake_id, 16))

        document.datatake_id = datatake_id

        document.key = self.get_consolidated_id(raw_document)

        document.instrument_mode = data_dict.get(
            "instrument_mode", document.instrument_mode
        )

        document.mission = data_dict.get("mission", document.mission)

        if fill_name:
            document.name = raw_document.product_name

        document.polarization = data_dict.get("polarization", document.polarization)

        document.product_class = data_dict.get("product_class", document.product_class)

        document.product_type = data_dict.get("product_type", document.product_type)

        # product_level shall have been calculated from data flow before
        document.product_level = data_dict.get(
            "product_level", utils.PRODUCT_LEVEL_MISSING_VALUE
        )

        document.satellite_unit = data_dict.get(
            "satellite_unit", document.satellite_unit
        )

        document.site_center = data_dict.get("site_center", document.site_center)

        # S5 specific
        document.collection_number = data_dict.get(
            "collection_number", document.collection_number
        )
        document.processor_version = data_dict.get(
            "processor_version", document.processor_version
        )

        self.fill_sensing(raw_document, document, data_dict, start_key, end_key)

        # Timeliness for S1 & S2 is deduced from datatake later in on_post_consolidate()
        if document.mission in ("S3", "S5"):
            document.timeliness = data_dict.get("timeliness", document.timeliness)

        # MAAS_CDS-526 set a value different of None so grafana can display it
        if document.timeliness is None:
            document.timeliness = utils.TIMELINESS_NULL_VALUE

        if raw_document.content_length is not None:
            document.content_length = raw_document.content_length

        # S2 specific
        if getattr(raw_document, "cloud_cover", ""):
            document.cloud_cover = raw_document.cloud_cover

        if getattr(raw_document, "datastrip_id", ""):
            document.datastrip_id = raw_document.datastrip_id

        if getattr(raw_document, "quality_status", ""):
            document.quality_status = raw_document.quality_status

        if getattr(raw_document, "product_group_id", ""):
            document.product_group_id = raw_document.product_group_id

        return data_dict

    def extract_data_from_product_name(self, product_name: str) -> dict:
        """

        Return pre-calculated data dict

        Args:
            product_name (str): product name

        Returns:
            dict: extracted data
        """
        try:
            return self.all_data_dict[product_name]
        except KeyError:
            # fallback if cache has not been filled, typically for unit testing
            data_dict = self.all_data_dict[product_name] = (
                extract_data_from_product_name(product_name)
            )

            data_dict["product_level"] = self.get_product_level(
                data_dict["mission"], data_dict["product_type"]
            )
            return data_dict

    def on_pre_consolidate(self):
        """

        Calculate data extracted from product names once per session

        """
        super().on_pre_consolidate()

        # init mapping if needed
        if not BaseProductConsolidatorEngine.LEVEL_TYPE_MAPPING:
            BaseProductConsolidatorEngine.LEVEL_TYPE_MAPPING = (
                self.load_level_type_mapping()
            )

            self.logger.info(
                "Loaded dataflow product level-type mapping : %s",
                len(BaseProductConsolidatorEngine.LEVEL_TYPE_MAPPING),
            )
        else:
            self.logger.debug("Dataflow product level-type mapping is already loaded")

        self.all_data_dict = self.session.get("all_data_dict")

        if not self.all_data_dict:
            self.logger.debug("Pre-calculate data extracted from product names")

            self.all_data_dict = {
                product_name: extract_data_from_product_name(product_name)
                for product_name in [
                    raw_document.product_name for raw_document in self.input_documents
                ]
            }

            # update product levels from dataflow
            for product_name, data_dict in self.all_data_dict.items():
                if "mission" not in data_dict:
                    self.logger.debug("No mission extracted from %s", product_name)
                    continue

                data_dict["product_level"] = self.get_product_level(
                    data_dict["mission"], data_dict["product_type"]
                )

            self.session.put("all_data_dict", self.all_data_dict)
        else:
            self.logger.debug("Reuse calculated data from product names")

    def on_post_consolidate(self):
        """

        Group per-product single queries to diminish their count.

        Product or publication related to a datatake (S1 and S2) will perform datatake
        search in an optimized way:
         - 1 single query for all S1 products
         - 1 multi-search query for S2 products with a reduction of the period parameter
           as there is a high probability of having products of the same datatake

        Timeliness will then be calculated.
        """
        super().on_post_consolidate()

        # Python grouby only groups consecutive elements, we want unique groups
        # so we need to sort the list before

        # Products that have no satellite_unit are placed at the end so that we can skip them later
        self.consolidated_documents = sorted(
            self.consolidated_documents,
            key=lambda x: (
                x["satellite_unit"] if x["satellite_unit"] is not None else "SZZ"
            ),
        )

        datatake_dict = defaultdict(str)
        for mission, documents in groupby(
            self.consolidated_documents, lambda document: document.mission
        ):
            if mission not in ("S1", "S2"):
                # no datatake to attach for other missions
                continue

            documents = list(documents)

            datatake_dict_mission = getattr(self, f"get_datatake_dict_{mission}")(
                documents
            )
            datatake_dict.update(datatake_dict_mission)
            self.session.put("datatake_dict", datatake_dict)

            if not documents:
                # no document to process for this mission
                continue

            # filter documents
            documents = getattr(self, f"filter_documents_for_timeliness_{mission}")(
                documents
            )

            if not documents:
                # no document to process for this mission
                continue
            for document in documents:
                if not document.name_without_extension in datatake_dict:
                    self.logger.debug(
                        "No datatake found for product : %s",
                        document.name,
                    )
                    continue
                document.fill_from_datatake(
                    datatake_dict[document.name_without_extension]
                )

    def filter_documents_for_timeliness_S1(self, documents):
        """
        Filter AMALFI_REPORT from datatake link

        Args:
            documents (list): S1 documents

        Returns:
            list: filtered documents
        """

        return [
            document
            for document in documents
            if document.datatake_id not in [None, utils.DATATAKE_ID_MISSING_VALUE]
            and document.product_type != "AMALFI_REPORT"
        ]

    def filter_documents_for_timeliness_S2(self, documents):
        """
        Keep only product types starting with MSI

        Args:
            documents (list): S1 documents

        Returns:
            list: filtered documents
        """
        return [
            document
            for document in documents
            if document.product_type.startswith("MSI")
        ]

    def get_datatake_dict_S1(
        self, documents: list["ProductDatatakeMixin"]
    ) -> Dict[str, CdsDatatake]:
        """
        Get a dict name_without_extension -> datatake for S1 products

        Args:
            documents (list[ProductDatatakeMixin]): consolidated document

        Returns:
            Dict[str, CdsDatatake]: name_without_extension -> datatake
        """
        return {
            document.name_without_extension: datatake
            for document, datatake in zip(
                documents,
                CdsDatatake.mget_by_ids(
                    [
                        f"{document.satellite_unit}-{document.datatake_id}"
                        for document in documents
                    ]
                ),
            )
        }

    def _get_datatake_S2_map(
        self, searched_periods, satellite, tolerance_value, grouped_documents
    ):
        datatake_ms = MultiSearch()

        max_size = min(len(grouped_documents) * 2, 10000)
        for period in searched_periods:

            search = (
                CdsDatatake.search()
                .filter("term", mission="S2")
                .filter("term", satellite_unit=satellite)
                .filter(
                    "range",
                    observation_time_start={"lte": period.end + 2 * tolerance_value},
                )
                .filter(
                    "range",
                    observation_time_stop={"gte": period.start - 2 * tolerance_value},
                )
            )
            # Impossible in msearch to insert extra kwargs like size
            # pylint: disable=W0212
            search._extra = {"size": max_size}
            # pylint: enable=W0212

            datatake_ms = datatake_ms.add(search)

        datatake_map = {}

        raw_response = datatake_ms.execute()

        for response in raw_response:
            for datatake in response:
                datatake_map[datatake.meta.id] = datatake

        return datatake_map

    def get_datatake_dict_S2(
        self, documents: list["ProductDatatakeMixin"]
    ) -> Dict[str, CdsDatatake]:
        """
        Get a dict name_without_extension -> datatake for S2 products

        Args:
            documents (list[ProductDatatakeMixin]): consolidated document

        Returns:
            Dict[str, CdsDatatake]: name_without_extension -> datatake
        """
        datatake_dict = {}

        tolerance_value = datetime.timedelta(seconds=self.S2_DATATAKE_ATTACHEMENT_DELTA)

        for satellite, grouped_documents in groupby(
            documents, lambda document: document.satellite_unit
        ):
            # Multiple Search by satellite with reduced queries

            grouped_documents = list(grouped_documents)

            searched_periods = reduce_periods(
                [
                    Period(document.sensing_start_date, document.sensing_end_date)
                    for document in grouped_documents
                ],
                tolerance_value=tolerance_value,
            )

            datatake_map = self._get_datatake_S2_map(
                searched_periods, satellite, tolerance_value, grouped_documents
            )

            available_datatakes = list(datatake_map.values())

            self.logger.info(
                "mfill_timeliness_S2 (%s): found %s datatakes "
                "for %s candidate entities",
                satellite,
                len(available_datatakes),
                len(grouped_documents),
            )

            if not available_datatakes:
                self.logger.warning("No datatake found for %s", grouped_documents)
                continue

            for document in grouped_documents:
                nearest_datatake = document.find_nearest_datatake(
                    available_datatakes,
                    datetime.timedelta(seconds=self.S2_DATATAKE_ATTACHEMENT_DELTA),
                )
                if nearest_datatake is None:
                    self.logger.debug(
                        "[DT-ATTACHEMENT] - No datatake found for document %s", document
                    )
                    self.logger.debug(
                        "[DT-ATTACHEMENT] - available_datatakes: %s",
                        available_datatakes,
                    )
                    self.logger.debug(
                        "[DT-ATTACHEMENT] - searched_periods: %s", searched_periods
                    )
                datatake_dict[document.name_without_extension] = nearest_datatake

        return datatake_dict
