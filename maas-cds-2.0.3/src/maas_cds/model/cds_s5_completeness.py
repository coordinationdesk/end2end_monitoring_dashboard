""" Custom CDS model definition for product"""

import logging


from opensearchpy import Keyword
from maas_cds.model import generated
from maas_cds.model.product_s5 import CdsProductS5
from maas_cds.model.enumeration import CompletenessStatus
from maas_cds.model.enumeration import CompletenessScope

from maas_cds.model.datatake import (
    evaluate_completeness_status,
)

from maas_cds.lib.periodutils import (
    compute_total_sensing_product,
    compute_total_sensing_period,
    Period,
)
from maas_cds.lib import tolerance

from maas_cds.model.anomaly_mixin import AnomalyMixin

__all__ = ["CdsS5Completeness"]


LOGGER = logging.getLogger("CdsS5Completeness")


class CdsS5Completeness(AnomalyMixin, generated.CdsS5Completeness):
    """Document handeling cds S5 completeness"""

    _BASE_S5_PRODUCTS_TYPES = {
        "OPER_L0__ENG_A_": {
            "active": True,
            "slices": 6,
            "sensing": 100,
            "level": "L0_",
            "timeliness": "OPER",
        },
        "OPER_L0__ODB_1_": {
            "active": True,
            "slices": 6,
            "sensing": 100,
            "level": "L0_",
            "timeliness": "OPER",
        },
        "OPER_L0__ODB_2_": {
            "active": True,
            "slices": 6,
            "sensing": 100,
            "level": "L0_",
            "timeliness": "OPER",
        },
        "OPER_L0__ODB_3_": {
            "active": True,
            "slices": 6,
            "sensing": 100,
            "level": "L0_",
            "timeliness": "OPER",
        },
        "OPER_L0__ODB_4_": {
            "active": True,
            "slices": 6,
            "sensing": 100,
            "level": "L0_",
            "timeliness": "OPER",
        },
        "OPER_L0__ODB_5_": {
            "active": True,
            "slices": 6,
            "sensing": 100,
            "level": "L0_",
            "timeliness": "OPER",
        },
        "OPER_L0__ODB_6_": {
            "active": True,
            "slices": 6,
            "sensing": 100,
            "level": "L0_",
            "timeliness": "OPER",
        },
        "OPER_L0__ODB_7_": {
            "active": True,
            "slices": 6,
            "sensing": 100,
            "level": "L0_",
            "timeliness": "OPER",
        },
        "OPER_L0__ODB_8_": {
            "active": True,
            "slices": 6,
            "sensing": 100,
            "level": "L0_",
            "timeliness": "OPER",
        },
        "OPER_L0__SAT_A_": {
            "active": True,
            "slices": 6,
            "sensing": 100,
            "level": "L0_",
            "timeliness": "OPER",
        },
        "NRTI_L1B_ENG_DB": {
            "active": True,
            "slices": 21,
            "sensing": 100,
            "level": "L1B",
            "timeliness": "NRTI",
        },
        "NRTI_L1B_RA_BD1": {
            "active": True,
            "slices": 13,
            "sensing": 60,
            "level": "L1B",
            "timeliness": "NRTI",
        },
        "NRTI_L1B_RA_BD2": {
            "active": True,
            "slices": 13,
            "sensing": 60,
            "level": "L1B",
            "timeliness": "NRTI",
        },
        "NRTI_L1B_RA_BD3": {
            "active": True,
            "slices": 13,
            "sensing": 60,
            "level": "L1B",
            "timeliness": "NRTI",
        },
        "NRTI_L1B_RA_BD4": {
            "active": True,
            "slices": 13,
            "sensing": 60,
            "level": "L1B",
            "timeliness": "NRTI",
        },
        "NRTI_L1B_RA_BD5": {
            "active": True,
            "slices": 13,
            "sensing": 60,
            "level": "L1B",
            "timeliness": "NRTI",
        },
        "NRTI_L1B_RA_BD6": {
            "active": True,
            "slices": 13,
            "sensing": 60,
            "level": "L1B",
            "timeliness": "NRTI",
        },
        "NRTI_L1B_RA_BD7": {
            "active": True,
            "slices": 13,
            "sensing": 60,
            "level": "L1B",
            "timeliness": "NRTI",
        },
        "NRTI_L1B_RA_BD8": {
            "active": True,
            "slices": 13,
            "sensing": 60,
            "level": "L1B",
            "timeliness": "NRTI",
        },
        "NRTI_L2__AER_AI": {
            "active": True,
            "slices": 13,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "NRTI",
        },
        "NRTI_L2__AER_LH": {
            "active": True,
            "slices": 13,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "NRTI",
        },
        "NRTI_L2__CLOUD_": {
            "active": True,
            "slices": 13,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "NRTI",
        },
        "NRTI_L2__CO____": {
            "active": True,
            "slices": 13,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "NRTI",
        },
        "NRTI_L2__FRESCO": {
            "active": True,
            "slices": 13,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "NRTI",
        },
        "NRTI_L2__HCHO__": {
            "active": True,
            "slices": 13,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "NRTI",
        },
        "NRTI_L2__NO2___": {
            "active": True,
            "slices": 13,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "NRTI",
        },
        "NRTI_L2__O3__PR": {
            "active": True,
            "slices": 13,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "NRTI",
        },
        "NRTI_L2__O3____": {
            "active": True,
            "slices": 13,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "NRTI",
        },
        "NRTI_L2__SO2___": {
            "active": True,
            "slices": 13,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "NRTI",
        },
        "OFFL_L1B_ENG_DB": {
            "active": True,
            "slices": 1,
            "sensing": 100,
            "level": "L1B",
            "timeliness": "OFFL",
        },
        "OFFL_L1B_RA_BD1": {
            "active": True,
            "slices": 1,
            "sensing": 100,
            "level": "L1B",
            "timeliness": "OFFL",
        },
        "OFFL_L1B_RA_BD2": {
            "active": True,
            "slices": 1,
            "sensing": 100,
            "level": "L1B",
            "timeliness": "OFFL",
        },
        "OFFL_L1B_RA_BD3": {
            "active": True,
            "slices": 1,
            "sensing": 100,
            "level": "L1B",
            "timeliness": "OFFL",
        },
        "OFFL_L1B_RA_BD4": {
            "active": True,
            "slices": 1,
            "sensing": 100,
            "level": "L1B",
            "timeliness": "OFFL",
        },
        "OFFL_L1B_RA_BD5": {
            "active": True,
            "slices": 1,
            "sensing": 100,
            "level": "L1B",
            "timeliness": "OFFL",
        },
        "OFFL_L1B_RA_BD6": {
            "active": True,
            "slices": 1,
            "sensing": 100,
            "level": "L1B",
            "timeliness": "OFFL",
        },
        "OFFL_L1B_RA_BD7": {
            "active": True,
            "slices": 1,
            "sensing": 100,
            "level": "L1B",
            "timeliness": "OFFL",
        },
        "OFFL_L1B_RA_BD8": {
            "active": True,
            "slices": 1,
            "sensing": 100,
            "level": "L1B",
            "timeliness": "OFFL",
        },
        "OFFL_L2__AER_AI": {
            "active": True,
            "slices": 1,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "OFFL",
        },
        "OFFL_L2__AER_LH": {
            "active": True,
            "slices": 1,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "OFFL",
        },
        "OFFL_L2__CH4___": {
            "active": True,
            "slices": 1,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "OFFL",
        },
        "OFFL_L2__CLOUD_": {
            "active": True,
            "slices": 1,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "OFFL",
        },
        "OFFL_L2__CO____": {
            "active": True,
            "slices": 1,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "OFFL",
        },
        "OFFL_L2__FRESCO": {
            "active": True,
            "slices": 1,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "OFFL",
        },
        "OFFL_L2__HCHO__": {
            "active": True,
            "slices": 1,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "OFFL",
        },
        "OFFL_L2__NO2___": {
            "active": True,
            "slices": 1,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "OFFL",
        },
        "OFFL_L2__NP_BD3": {
            "active": True,
            "slices": 1,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "OFFL",
        },
        "OFFL_L2__NP_BD6": {
            "active": True,
            "slices": 1,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "OFFL",
        },
        "OFFL_L2__NP_BD7": {
            "active": True,
            "slices": 1,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "OFFL",
        },
        "OFFL_L2__O3__PR": {
            "active": True,
            "slices": 1,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "OFFL",
        },
        "OFFL_L2__O3____": {
            "active": True,
            "slices": 1,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "OFFL",
        },
        "OFFL_L2__SO2___": {
            "active": True,
            "slices": 1,
            "sensing": 55,
            "level": "L2_",
            "timeliness": "OFFL",
        },
    }

    # /!\ Take care of this because product_level is not accorded to dataflow
    INCLUDED_TYPES_FOR_COMPLETENESS = [
        key for key, item in _BASE_S5_PRODUCTS_TYPES.items() if item["active"]
    ]

    COMPLETENESS_TOLERANCE = {}

    _S5_PRODUCTS_TYPES = None

    cams_tickets = Keyword(multi=True)
    cams_origin = Keyword(multi=True)
    cams_descriptions = Keyword(multi=True)

    @classmethod
    def s5_products_types(cls):
        """property to get a cache

        Returns:
            dict: cached product_types with dataflow overload or load it for the first time
        """
        if cls._S5_PRODUCTS_TYPES is None:
            cls._S5_PRODUCTS_TYPES = cls.load_level_product_types()
        return cls._S5_PRODUCTS_TYPES

    @classmethod
    def included_types_for_completeness(cls):
        """property that filter active product_type for completeness

        Returns:
            dict: product_type with medatada that be active
        """
        return {
            key: item
            for (key, item) in cls.s5_products_types().items()
            if item["active"]
        }

    @classmethod
    def load_level_product_types(cls):
        """Overide default product_level with dataflow product_level

        Returns:
            dict: s5 product_type with metadata
        """
        search_request = generated.CdsDataflow.search().query("term", mission="S5")
        request_result = search_request.params(size=1000).execute()

        result_mapping = {conf.product_type: conf.level for conf in request_result}
        base = cls._BASE_S5_PRODUCTS_TYPES

        for product_type, metadata in base.items():
            metadata["level"] = result_mapping.get(product_type, "___")

        dataflow_product_type = set([conf.product_type for conf in request_result])
        modelclass_product_type = set(base.keys())

        LOGGER.debug(
            "Diff between dataflow and class (should be contains not computed completeness) : %s",
            dataflow_product_type - modelclass_product_type,
        )
        LOGGER.debug(
            "Diff between class and dataflow (should be empty) : %s",
            modelclass_product_type - dataflow_product_type,
        )

        return base

    def compute(self):
        """Retrieve implied products to compute sensing completeness"""
        # get implied periods from products matching completenes properties
        implied_periods = self.get_implied_periods()

        # extract completeness_value from set of periods from products(tuple start stop)
        sensing_value = compute_total_sensing_product(implied_periods)

        # extract slice_value from set of implied_periods(count of periods)
        slice_value = len(implied_periods)

        # extract observation period from set of periods from products(tuple start stop)
        observation_period = compute_total_sensing_period(implied_periods)
        if observation_period is None:
            observation_period = Period(
                self.observation_time_start, self.observation_time_stop
            )

        return sensing_value, slice_value, observation_period

    def get_implied_products(self):
        """Get CdsProduct implied for this completeness

        Returns:
            [CdsProduct] : Array of Product matching this completeness and having a prip_id
        """

        # get document with a prip_id
        query_scan = self.find_products_scan()

        # TODO Dangerous memory abuse
        implied_products = list(query_scan)

        return implied_products

    def get_implied_periods(self):
        """Get CdsProduct Periods implied for this completeness

        Returns:
            [CdsProduct] : Array of Period for the product array.
        """

        implied_products = self.get_implied_products()

        implied_documents = []
        if implied_products is not None:
            for product in implied_products:
                implied_documents.append(
                    Period(product.sensing_start_date, product.sensing_end_date)
                )

        # Sort document by sensing date
        implied_documents.sort(key=lambda product: product.start)

        return implied_documents

    def find_products_scan(self):
        """Build and execute the opensearchpy query to retrive products matching completenes properties"""

        # Products L0_ comes from LTA
        if self.product_level == "L0_":
            search_request = (
                CdsProductS5.search()
                .filter("term", datatake_id=self.datatake_id)
                .filter("term", mission=self.mission)
                .filter("term", product_type=self.product_type)
            )
        else:
            search_request = (
                CdsProductS5.search()
                .filter("term", datatake_id=self.datatake_id)
                .filter("term", mission=self.mission)
                .filter("term", product_type=self.product_type)
                .filter("exists", field="prip_id")
            )

        query_scan = search_request.scan()

        return query_scan

    def set_completeness(
        self,
        sensing_value: int,
        slice_value: int,
        observation_period: Period,
    ):
        """completeness
        Args:
            product the product to add
            completeness_tolerance (list): tolerance list
        """

        LOGGER.debug(
            "[%s] - set completeness for %s", self.datatake_id, self.product_type
        )

        # get expected for current completeness document
        sensing_expected_value = self.get_expected_value()

        if not sensing_expected_value:
            LOGGER.warning(
                "[%s] - Trying to evaluate completeness but sensing_expected_value = 0 | %s",
                self.datatake_id,
                self.product_type,
            )
            return

        # compute other value
        sensing_adjusted_value = min(sensing_value, sensing_expected_value)
        sensing_percentage_value = sensing_adjusted_value / sensing_expected_value * 100
        sensing_completeness_status_value = evaluate_completeness_status(
            sensing_percentage_value
        )
        slice_expected_value = self.get_slice_expected_value()
        self.set_completeness_attribute(
            observation_period,
            sensing_value,
            sensing_expected_value,
            sensing_adjusted_value,
            sensing_percentage_value,
            sensing_completeness_status_value,
            slice_value,
            slice_expected_value,
        )

    # pylint: disable=R0913
    # Parameters must be mandatory
    def set_completeness_attribute(
        self,
        observation_period,
        sensing_value: int,
        sensing_expected_value: int,
        sensing_adjusted_value: int,
        sensing_percentage_value: float,
        sensing_completeness_status_value: CompletenessStatus,
        slice_value: int,
        slice_expected_value: int,
    ):
        """Store completeness in doc

        Args:
            observation_period (named tuple Period(start, end)): observation period
            sensing_value (int): sensing value (used as completeness)
            sensing_expected_value (int): sensing expected value (depending on type)
            sensing_adjusted_value (int): sensing adjusted value (adjusted to avoid percentages > 100%)
            sensing_percentage_value (float): persentage of sensing vs expected
            sensing_completeness_status_value (CompletenessStatus): Status label
            slice_value (int): number of slices
            slice_expected_value (int): number of expected slices
        """

        setattr(self, "value", sensing_value)

        setattr(self, "expected", sensing_expected_value)

        setattr(self, "value_adjusted", sensing_adjusted_value)

        setattr(self, "percentage", sensing_percentage_value)

        setattr(self, "status", sensing_completeness_status_value)

        setattr(self, "slice_value", slice_value)

        setattr(self, "slice_expected", slice_expected_value)

        setattr(self, "observation_time_start", observation_period.start)

        setattr(self, "observation_time_stop", observation_period.end)

    def get_expected_value(
        self,
    ):
        """Evaluate expected for a specific product_type

        Returns:
            int: The local expected value of this datatake and the given product_type
        """

        expected_value = 0

        tolerance_value = tolerance.get_completeness_tolerance(
            self.COMPLETENESS_TOLERANCE,
            self.mission,
            CompletenessScope.LOCAL,
            self.product_type,
        )
        expected_minutes = self.included_types_for_completeness()[self.product_type][
            "sensing"
        ]

        expected_value = (expected_minutes * 60 * 1000000) + tolerance_value

        return expected_value

    def get_slice_expected_value(self):
        """Evaluate slice expected for a specific product_type

        Returns:
            int: The local slice expected value of this datatake and the given product_type
        """

        expected_slices = self.included_types_for_completeness()[self.product_type][
            "slices"
        ]

        return expected_slices

    def init_completenesses(self):
        """compose other product_type completeness values from current completeness

        Returns:
            dict: minimal completeness values dict
        """
        datas_for_completenesses = {}
        satellite_unit = self.datatake_id.split("-")[0]
        mission = satellite_unit[0:2]

        for name, s5_product_type in self.included_types_for_completeness().items():
            key = f"{self.datatake_id}-{name}"
            data_for_completeness = {
                "key": key,
                "datatake_id": self.datatake_id,
                "absolute_orbit": self.absolute_orbit,
                "mission": mission,
                "satellite_unit": satellite_unit,
                "timeliness": s5_product_type["timeliness"],
                "product_type": name,
                "product_level": s5_product_type["level"],
                "observation_time_start": self.observation_time_start,
                "observation_time_stop": self.observation_time_stop,
            }
            datas_for_completenesses[key] = data_for_completeness

        return datas_for_completenesses

    @classmethod
    def is_exclude_for_completeness(cls, product_type):
        """Get the information is the product type is exclude for completeness

        Returns:
            bool: True if he need to be excluted
        """
        # return false if the product_types is not contained in included product_type

        return product_type not in cls.included_types_for_completeness()
