""" Custom CDS model definition for product"""

import logging

from opensearchpy import Keyword
from maas_cds.model import generated
from maas_cds.model.product_s3 import CdsProductS3
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

__all__ = ["CdsS3Completeness"]


LOGGER = logging.getLogger("CdsModelS3Completeness")


class CdsS3Completeness(AnomalyMixin, generated.CdsS3Completeness):
    """Document handeling cds S3 completeness"""

    S3_PRODUCTS_TYPES = {
        "DO_0_DOP___": {
            "active": True,
            "sensing": 101,
            "level": 0,
            "timeliness": ["NR"],
        },
        "DO_0_NAV___": {
            "active": True,
            "sensing": 101,
            "level": 0,
            "timeliness": ["AL"],
        },
        "GN_0_GNS___": {
            "active": True,
            "sensing": 101,
            "level": 0,
            "timeliness": ["NR"],
        },
        "MW_0_MWR___": {
            "active": True,
            "sensing": 101,
            "level": 0,
            "timeliness": ["NR"],
        },
        "MW_1_CAL___": {
            "active": True,
            "sensing": 101,
            "level": 1,
            "timeliness": ["NR"],
        },
        "MW_1_MWR___": {
            "active": True,
            "sensing": 101,
            "level": 1,
            "timeliness": ["NR", "NT", "ST"],
        },
        "OL_0_EFR___": {
            "active": True,
            "sensing": 44,
            "level": 0,
            "timeliness": ["NR"],
        },
        "OL_1_EFR___": {
            "active": True,
            "sensing": 44,
            "level": 1,
            "timeliness": ["NR", "NT"],
        },
        "OL_1_ERR___": {
            "active": True,
            "sensing": 44,
            "level": 1,
            "timeliness": ["NR", "NT"],
        },
        "OL_2_LFR___": {
            "active": True,
            "sensing": 44,
            "level": 2,
            "timeliness": ["NR", "NT"],
        },
        "OL_2_LRR___": {
            "active": True,
            "sensing": 44,
            "level": 2,
            "timeliness": ["NR", "NT"],
        },
        "SL_0_SLT___": {
            "active": True,
            "sensing": 101,
            "level": 0,
            "timeliness": ["NR"],
        },
        "SL_1_RBT___": {
            "active": True,
            "sensing": 101,
            "level": 1,
            "timeliness": ["NR", "NT"],
        },
        "SL_2_FRP___": {
            "active": True,
            "sensing": 101,
            "level": 2,
            "timeliness": ["NT"],
        },
        "SL_2_LST___": {
            "active": True,
            "sensing": 101,
            "level": 2,
            "timeliness": ["NR", "NT"],
        },
        "SR_0_SRA___": {
            "active": True,
            "sensing": 101,
            "level": 0,
            "timeliness": ["NR", "ST"],
        },
        "SR_1_SRA_A_": {
            "active": True,
            "sensing": 101,
            "level": 1,
            "timeliness": ["NR", "NT", "ST"],
        },
        "SY_1_MISR__": {
            "active": True,
            "sensing": 44,
            "level": 1,
            "timeliness": ["NT", "ST"],
        },
        "SY_2_AOD___": {
            "active": True,
            "sensing": 44,
            "level": 2,
            "timeliness": ["NT"],
        },
        "SY_2_SYN___": {
            "active": True,
            "sensing": 44,
            "level": 2,
            "timeliness": ["NT", "ST"],
        },
        "SY_2_VGK___": {
            "active": True,
            "sensing": 44,
            "level": 2,
            "timeliness": ["NT", "ST"],
        },
        "SY_2_VGP___": {
            "active": True,
            "sensing": 44,
            "level": 2,
            "timeliness": ["NT", "ST"],
        },
        "SR_1_LAN_RD": {
            "active": True,
            "sensing": 101,
            "level": 1,
            "timeliness": ["NT", "ST", "NR"],
        },
        "TM_0_HKM2__": {
            "active": True,
            "sensing": 101,
            "level": 0,
            "timeliness": ["NR"],
        },
        "TM_0_HKM___": {
            "active": True,
            "sensing": 101,
            "level": 0,
            "timeliness": ["NR"],
        },
        "TM_0_NAT___": {
            "active": True,
            "sensing": 101,
            "level": 0,
            "timeliness": ["AL"],
        },
    }

    EXCLUDED_TYPES_FOR_COMPLETENESS = [
        key for key, item in S3_PRODUCTS_TYPES.items() if not item["active"]
    ]

    SENSING_44 = [
        key for key, item in S3_PRODUCTS_TYPES.items() if item["sensing"] == 44
    ]

    PER_ORBIT_EXPECTED_44 = 44 * 60 * 1000000

    SENSING_101 = [
        key for key, item in S3_PRODUCTS_TYPES.items() if item["sensing"] == 101
    ]

    PER_ORBIT_EXPECTED_101 = 101 * 60 * 1000000

    COMPLETENESS_TOLERANCE = {}

    cams_tickets = Keyword(multi=True)

    def compute_values(self):
        """Retrieve implied products to compute completeness"""
        # get implied products matching completenes properties
        implied_product = self.get_implied_products()
        # extract completeness_value from set of products(duration in microseconds)
        completeness_value = compute_total_sensing_product(implied_product)
        return completeness_value

    def compute_observation_period(self):
        """Retrieve implied products to compute completeness"""
        # get implied products matching completenes properties
        implied_product = self.get_implied_products()
        # extract observation period from set of products(tuple start stop)
        observation_period = compute_total_sensing_period(implied_product)
        if observation_period is None:
            observation_period = Period(
                self.observation_time_start, self.observation_time_stop
            )
        return observation_period

    def get_implied_products(self):
        """Get CdsProduct implied for this completeness

        Returns:
            [CdsProduct] : Array of Product matching this completeness and having a prip_id
        """

        # get document with a prip_id
        query_scan = self.find_products_scan()

        # for debug purpose
        # if not hasattr(self,"products_list"):
        #     setattr(self, "products_list", [])

        # implied_documents = []
        # for product in query_scan:
        #     implied_documents.append(Period(product.sensing_start_date, product.sensing_end_date))
        #     getattr(self, "products_list").append(product.name)

        implied_documents = [
            Period(product.sensing_start_date, product.sensing_end_date)
            for product in query_scan
        ]

        # Sort document by sensing date
        implied_documents.sort(key=lambda product: product.start)

        return implied_documents

    def find_products_scan(self):
        """Build and execute the opensearchpy query to retrieve products matching
        completeness properties
        """
        search_request = (
            CdsProductS3.search()
            .filter("term", datatake_id=self.datatake_id)
            .filter("term", mission=self.mission)
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("term", product_type=self.product_type)
            .filter("term", timeliness=self.timeliness)
            .filter("exists", field="prip_id")
        )

        query_scan = search_request.scan()
        return query_scan

    def set_completeness(
        self,
        completeness_value,
        observation_period,
    ):
        """completeness
        Args:
            product the product to add
        """

        LOGGER.debug(
            "[%s] - set completeness for %s %s",
            self.datatake_id,
            self.product_type,
            self.timeliness,
        )

        # get expected for current completeness document
        expected_value = self.get_expected_value()

        if not expected_value:
            LOGGER.warning(
                "[%s] - Trying to evaluate completeness but expected_value = 0 | %s %s",
                self.datatake_id,
                self.product_type,
                self.timeliness,
            )
            return

        # compute other value
        adjusted_value = min(completeness_value, expected_value)
        percentage_value = adjusted_value / expected_value * 100
        completeness_status_value = evaluate_completeness_status(percentage_value)

        self.set_completeness_attribute(
            completeness_value,
            observation_period,
            expected_value,
            adjusted_value,
            percentage_value,
            completeness_status_value,
        )

    # pylint: disable=R0913
    # Parameters must be mandatory
    def set_completeness_attribute(
        self,
        completeness_value: int,
        observation_period,
        expected_value: int,
        adjusted_value: int,
        percentage_value: float,
        completeness_status_value: CompletenessStatus,
    ):
        """Store completeness in doc

        Args:
            completeness_value (int): completeness value
            observation_period named tuple start, end
            expected_value (int): expected value
            adjusted_value (int): adjusyed value
            percentage_value (float): percentage value
            completeness_status_value (CompletenessStatus): completeness value
        """
        # value
        setattr(self, "value", completeness_value)

        # observation start
        setattr(self, "observation_time_start", observation_period.start)

        # observation end
        setattr(self, "observation_time_stop", observation_period.end)

        # expected
        setattr(self, "expected", expected_value)

        # adjusted
        setattr(self, "value_adjusted", adjusted_value)

        # percentage
        setattr(self, "percentage", percentage_value)

        # status
        setattr(self, "status", completeness_status_value)

    def get_expected_value(
        self,
    ):
        """Evaluate expected for a specific product_type

        Args:
            completeness_tolerance (list): tolerance list

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

        if self.product_type in self.SENSING_44:
            expected_value = self.PER_ORBIT_EXPECTED_44

            # add tolerance concerted in microseconde
            expected_value += tolerance_value

        elif self.product_type in self.SENSING_101:
            expected_value = self.PER_ORBIT_EXPECTED_101

            # add tolerance concerted in microseconde
            expected_value += tolerance_value

        return expected_value

    def init_completenesses(self):
        """compose defaults completeness values from datattake_id

        Returns minimal completenes values array
        """
        datas_for_completenesses = {}
        satellite_unit = self.datatake_id.split("-")[0]
        mission = satellite_unit[0:2]

        for name, s3_product_type in self.S3_PRODUCTS_TYPES.items():
            if s3_product_type["active"]:
                for timeliness in s3_product_type["timeliness"]:
                    key = f"{self.datatake_id}#{name}#{timeliness}"
                    data_for_completeness = {
                        "key": key,
                        "datatake_id": self.datatake_id,
                        "mission": mission,
                        "satellite_unit": satellite_unit,
                        "timeliness": timeliness,
                        "product_type": name,
                        "product_level": f"L{s3_product_type['level']}_",
                        "observation_time_start": self.observation_time_start,
                        "observation_time_stop": self.observation_time_stop,
                    }
                    datas_for_completenesses[key] = data_for_completeness

        return datas_for_completenesses

    @staticmethod
    def is_exclude_for_completeness(product_type):
        """Get the information is the product type is exclude for completeness

        Returns:
            bool: True if he need to be excluted
        """
        # return false if one of the excluded product_types is contained in product_type

        return product_type in CdsS3Completeness.EXCLUDED_TYPES_FOR_COMPLETENESS
