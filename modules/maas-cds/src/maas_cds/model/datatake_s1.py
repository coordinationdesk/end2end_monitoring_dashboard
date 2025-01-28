""" Datatake S1 model definition """

import logging
from typing import Callable
from opensearchpy import Q

from maas_cds.model.datatake import CdsDatatake
from maas_cds.model import CdsProduct
from maas_cds.lib.config import get_good_threshold_config_from_value
from maas_cds.lib.periodutils import compute_total_sensing_product, Period

from maas_cds.model.enumeration import CompletenessScope

from maas_cds.lib import tolerance


__all__ = ["CdsDatatakeS1"]


LOGGER = logging.getLogger("CdsModelDatatakeS1")


class CdsDatatakeS1(CdsDatatake):
    """CdsDatatake custom class for Sentinel 1"""

    EXCLUDES_PRODUCTED_TYPES = ["AMALFI_REPORT"]

    MINIMUM_PERCENTAGE_OVERLAPPING_AREA = {
        "OCN": {"0": 20, "2024-06-06T13:20:00.000Z": 17},
        "SLC": {"0": 0},
    }

    REFERENCE_PRODUCT_TYPE_SENSING = "RAW__0S"

    DEFAULT_MASKS_APPLIED = "EU"

    PRODUCT_TYPES_OVER_SPECIFIC_AREA = {
        "IW": ["OCN"],
        "EW": ["OCN", "SLC"],
        "SM": ["OCN"],
    }

    L0_RAW__PRODUCT_TYPE = ["RAW__0A", "RAW__0C", "RAW__0N", "RAW__0S"]
    L1_SLC__PRODUCT_TYPE = ["SLC__1A", "SLC__1S"]
    L1_GRDH_PRODUCT_TYPE = ["GRDH_1A", "GRDH_1S"]
    L1_GRDM_PRODUCT_TYPE = ["GRDM_1A", "GRDM_1S"]
    L2_OCN__PRODUCT_TYPE = ["OCN__2A", "OCN__2S"]
    LA__PRODUCT_TYPE = ["ETA__AX"]

    REFERENCE_PRODUCT_TIME_FIELD = "prip_publication_date"

    def product_type_with_missing_periods(self, product_type: str) -> bool:
        """Do we want missing periods for this product type ?"""
        return not product_type.startswith("RF") and product_type.endswith("RAW__0S")

    def product_type_with_duplicated(self, product_type: str) -> bool:
        """Do we want check duplicated for this product type ?"""
        return True

    def impact_other_calculation(self, compute_key):
        """Reference product sensing provide expected for OCN or SLC

        Args:
            compute_key (tuple): the key of the compute that will be execute

        Returns:
            list(tuple): compute keys default: []
        """

        compute_product_type = compute_key[1]

        extra_compute_key = []

        if "SLC" in compute_key[1]:
            return [(compute_key[0], f"{compute_key[1][:2]}_ETA__AX")]

        if self.REFERENCE_PRODUCT_TYPE_SENSING in compute_product_type:
            # build compute key to process
            product_types_to_compute = [
                product_type
                for product_type in self.get_all_product_types()
                if self.product_type_over_specific_area(product_type)
            ]

            extra_compute_key = [
                (compute_key[0], product_type)
                for product_type in product_types_to_compute
            ]

        return extra_compute_key

    def get_compute_method(self, product_type: str) -> Callable:
        """Factory that returns the aggregation method for a product type

        Args:
            product_type (str): the product type where we want the compute method

        Returns:
            callable: the method to compute the completeness value
        """

        if "ETA" in product_type:
            # number of brother files
            compute_method = len

        else:
            # compute total sensing product
            compute_method = compute_total_sensing_product

        return compute_method

    def compute_local_value(self, product_type, related_documents=None):
        """Compute local value for a specific product_type"""

        LOGGER.debug(
            "[%s] - Compute local value for %s",
            self.datatake_id,
            product_type,
        )

        # Find related products for the datatake (brothers)
        brother_of_datatake_documents = self.get_datatake_product_type_brother(
            product_type
        )

        # Compute the local completeness value
        compute_method = self.get_compute_method(product_type)
        value = compute_method(brother_of_datatake_documents)

        if related_documents is not None:
            related_documents.extend(brother_of_datatake_documents)

        return value

    def add_prefix_instrument(self, product_type):
        """Add instrument mode at the given product_type

        Note:
            for the SM instrument mode it is S{instrument_swath}_product_type

        Args:
            product_type (str): type of product

        Returns:
            str: product_type prefixed by the instrument mode
        """

        if self.instrument_mode == "SM":
            product_type_with_instrument = f"S{self.instrument_swath}_{product_type}"
        else:
            product_type_with_instrument = f"{self.instrument_mode[:2]}_{product_type}"

        return product_type_with_instrument

    def product_type_over_specific_area(self, product_type):
        """Get the information if the product type is concerned by specific area completeness

        Args:
            product_type (str): type of the product

        Returns:
            bool: True if the product type is over specific area
        """

        # return false if one of the product type over specific area is in the product type
        datatake_product_type_over_specific_area = (
            self.PRODUCT_TYPES_OVER_SPECIFIC_AREA.get(self.instrument_mode)
        )

        is_product_type_over_specific_area = False

        if datatake_product_type_over_specific_area:
            is_product_type_over_specific_area = not all(
                excluded_product not in product_type
                for excluded_product in datatake_product_type_over_specific_area
            )

        return is_product_type_over_specific_area

    def evaluate_global_expected(self, key_field):
        global_expected = {}

        products_types_expected_list = self.get_all_product_types()

        for product_type in products_types_expected_list:
            expected_for_product_type = self.get_expected_from_product_type(
                product_type
            )

            for key, value in expected_for_product_type.items():
                if key not in global_expected:
                    global_expected[key] = 0

                global_expected[key] += value

        if not global_expected:
            LOGGER.warning(
                "[%s] - Unhandle instrument mode : %s",
                self.datatake_id,
                self.instrument_mode,
            )

        return global_expected.get(key_field, 0)

    def get_expected_value_over_speficic_area(self, product_type):
        """Evaluate expected value for a product type over specific area

        Args:
            product_type (str): the product type

        Returns:
            int: The sensing value of L0 product that intersect the specific area mask
        """

        reference_product_type = self.add_prefix_instrument(
            CdsDatatakeS1.REFERENCE_PRODUCT_TYPE_SENSING
        )

        LOGGER.debug(
            "[%s] - Over specific area expected using product_type : %s",
            self.datatake_id,
            reference_product_type,
        )

        query_scan = self.find_brother_products_scan(reference_product_type)

        raw_l0_sensing_period = []
        type_of_area = product_type[3:6]

        for product in query_scan:
            target_attr_coverage = f"{type_of_area}{self.COVERING_AREA_FIELD}"

            config = self.MINIMUM_PERCENTAGE_OVERLAPPING_AREA.get(type_of_area)
            (_, target_threshold) = get_good_threshold_config_from_value(
                config, str(getattr(product, self.REFERENCE_PRODUCT_TIME_FIELD))
            )
            if getattr(product, target_attr_coverage, 0) > target_threshold:
                raw_l0_sensing_period.append(
                    Period(product.sensing_start_date, product.sensing_end_date)
                )
        l0_sensing_over_specific_area = 0
        for l0_sensing in raw_l0_sensing_period:
            l0_sensing_over_specific_area += (
                l0_sensing.end - l0_sensing.start
            ).total_seconds() * 1000000

        slices_tolerance = len(
            raw_l0_sensing_period
        ) * tolerance.get_completeness_tolerance(
            self.COMPLETENESS_TOLERANCE,
            self.mission,
            CompletenessScope.SLICE,
            product_type,
        )
        return int(l0_sensing_over_specific_area + slices_tolerance)

    def get_slc_1s_count(self):
        """Count all SLC__1S products that are linked to the datatake

        Returns:
            int: count of products
        """
        search = (
            CdsProduct.search()
            .filter("term", datatake_id=self.datatake_id)
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("term", product_type=f"{self.instrument_mode}_SLC__1S")
        )

        count = search.count()

        return count

    def get_expected_from_product_type(self, product_type):
        """Evaluate expected for a specific product_type

        Args:
            product_type (str): product_type that we want to get the local expected

        Returns:
            dict: The expected value of this datatake for the given product_type
        """

        if "ETA" in product_type:
            etad = self.get_slc_1s_count()
            return {"etad": etad}

        sensing_value = 0

        # nominal
        if self.l0_sensing_duration:
            sensing_value = self.l0_sensing_duration

        if self.product_type_over_specific_area(product_type):
            sensing_value = self.get_expected_value_over_speficic_area(product_type)

        # specific
        if product_type == "RF_RAW__0S":
            sensing_value = 2800000

        # apply tolerance if we have sensing value
        if sensing_value:
            tolerance_value = tolerance.get_completeness_tolerance(
                self.COMPLETENESS_TOLERANCE,
                self.mission,
                CompletenessScope.LOCAL,
                product_type,
            )
            sensing_value += tolerance_value

            # avoid negative sensing
            sensing_value = max(0, sensing_value)

        return {"sensing": sensing_value}

    def get_all_product_types(
        self,
    ):
        """Return all product type expected for this datatake

        Returns:
            list: List of all product type expected for this datatake
        """

        s1_expected_from_instrument_mode = {
            "IW": self.L0_RAW__PRODUCT_TYPE
            + self.L1_SLC__PRODUCT_TYPE
            + self.L1_GRDH_PRODUCT_TYPE
            + self.L2_OCN__PRODUCT_TYPE
            + self.LA__PRODUCT_TYPE,
            "EW": self.L0_RAW__PRODUCT_TYPE
            + self.L1_SLC__PRODUCT_TYPE
            + self.L1_GRDM_PRODUCT_TYPE
            + self.L2_OCN__PRODUCT_TYPE
            + self.LA__PRODUCT_TYPE,
            "SM": self.L0_RAW__PRODUCT_TYPE
            + self.L1_SLC__PRODUCT_TYPE
            + self.L1_GRDH_PRODUCT_TYPE
            + self.L2_OCN__PRODUCT_TYPE
            + self.LA__PRODUCT_TYPE,
            "WV": self.L0_RAW__PRODUCT_TYPE
            + self.L1_SLC__PRODUCT_TYPE
            + self.L2_OCN__PRODUCT_TYPE,
            "RFC": ["RAW__0S"],
            "Z1": ["RAW__0S"],
            "Z2": ["RAW__0S"],
            "Z3": ["RAW__0S"],
            "Z4": ["RAW__0S"],
            "Z5": ["RAW__0S"],
            "Z6": ["RAW__0S"],
            "ZI": ["RAW__0S"],
            "ZE": ["RAW__0S"],
            "ZW": ["RAW__0S"],
            "AIS": ["RAW__0S"],
        }

        if self.instrument_mode[:2] not in [
            key[:2] for key in s1_expected_from_instrument_mode
        ]:
            LOGGER.warning(
                "[%s] - No instrument mode expected : %s",
                self.datatake_id,
                self.instrument_mode,
            )

            return []

        expected_product_type = [
            self.add_prefix_instrument(product_type)
            for product_type in s1_expected_from_instrument_mode.get(
                self.instrument_mode, []
            )
        ]

        if not expected_product_type:
            LOGGER.warning(
                "[%s] - No product type expected : %s",
                self.datatake_id,
                self.instrument_mode,
            )

        return expected_product_type

    def evaluate_local_expected(self, key_field):
        """Get local expected for a key who is the product_type

        Args:
            key_field (str): key of the expected (in this case the product type)

        Returns:
            dict: expected value for this kind of product
        """
        local_expected_for_product_type = self.get_expected_from_product_type(key_field)

        key_field_value = self.get_global_key_field(key_field)

        expected_value = local_expected_for_product_type.get(key_field_value, None)

        return expected_value

    def get_datatake_product_type_brother(self, product_type):
        """Get CdsProduct whith the same product type and the same datatake_id

        Args:
            product_type (str): the product type we want to have on the products

        Returns:
            [CdsProduct] : Array of Product that have the product_type
        """
        # TODO MAAS_CDS-1236: make a single query to find all the whole brotherhood

        # get document with same datatake_id and product_type and with a prip_id
        query_scan = self.find_brother_products_scan(product_type)

        brother_of_datatake_documents = []

        for product in query_scan:
            if (
                product.sensing_duration
                and product.sensing_start_date
                and product.sensing_end_date
            ):
                brother_of_datatake_documents.append(
                    Period(product.sensing_start_date, product.sensing_end_date)
                )

            else:
                LOGGER.warning(
                    "[%s][%s] - Failed to add it in document brothers [ %s, %s]",
                    self.datatake_id,
                    product.key,
                    product.sensing_start_date,
                    product.sensing_end_date,
                )

        # Sort document by sensing date
        brother_of_datatake_documents.sort(
            key=lambda product: (product.start, product.end)
        )

        return brother_of_datatake_documents

    def get_global_key_field(self, product_type):
        """Override

        Note:
            For sentinel they are only one type of data called sensing

        Args:
            product_type (str): the product_type to get the global key

        Returns:
            str: the global key
        """
        # Product Level A case :
        if "ETA" in product_type:
            return "etad"

        # Unique aggregation in s1
        return "sensing"

    def evaluate_all_global_expected(self):
        """Return global expected

        Returns:
            dict: The global expected of this datatake
        """
        global_expected = {}

        product_types_expected = self.get_all_product_types()

        for product_type in product_types_expected:
            expected_for_product_level = self.get_expected_from_product_type(
                product_type
            )

            for key, value in expected_for_product_level.items():
                if key not in global_expected:
                    global_expected[key] = 0

                global_expected[key] += value

        if not global_expected:
            LOGGER.warning(
                "[%s] - Unhandle instrument mode : %s",
                self.datatake_id,
                self.instrument_mode,
            )

        return global_expected

    def get_related_documents_query(self) -> Q:
        """override"""
        return Q("term", datatake_id=self.datatake_id)
