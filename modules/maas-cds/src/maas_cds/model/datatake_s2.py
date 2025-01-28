""" Datatake S2 model definition """

import logging

from datetime import timedelta
import typing
from maas_cds.lib.parsing_name import utils
from maas_cds.model.product import CdsProduct

from opensearchpy import Q

from maas_cds.model.datatake import CdsDatatake, evaluate_completeness_status

from maas_cds.lib.periodutils import compute_total_sensing_product, Period


from maas_cds.model.enumeration import CompletenessScope

from maas_cds.lib import tolerance

__all__ = ["CdsDatatakeS2"]


LOGGER = logging.getLogger("CdsModelDatatakeS2")


class CdsDatatakeS2(CdsDatatake):
    """CdsDatatake custom class for Sentinel 2"""

    RATIO_GRANULE_TILE = 10
    TOLERENCE_SENSING_START_GRANULE = 0.002

    MATCHING_DELTA_PRODUCTS = 15

    REFERENCE_PRODUCT_TYPE_SENSING = "MSI_L1C_DS"

    S2_EXPECTED_TYPE_FROM_PRODUCT_LEVEL_DICT = {
        "L0_": [
            "DS",
            "GR",
        ],
        "L1A": [
            "DS",
            "GR",
        ],
        "L1B": [
            "DS",
            "GR",
        ],
        "L1C": [
            "DS",
            "TL",
            "TC",
        ],
        "L2A": [
            "DS",
            "TL",
            "TC",
        ],
    }

    S2_NUMBER_OF_GR_PER_SCENE_PER_INSTRUMENT_DICT = {
        "NOBS": 12,
        "VIC": 12,
        "RAW": 4,
        "DASC": 12,
        "ABSR": 12,
        "EOBS": 12,
        "DARK-O": 12,
        "DARK-C": 12,
        "SUN": 12,
        "HKTM": 12,
        "MSMOON": 12,
    }

    S2_PRODUCT_LEVEL_FROM_INSTRUMENT_DICT = {
        "NOBS": ["L0_", "L1B", "L1C", "L2A"],
        "VIC": ["L0_", "L1B", "L1C"],
        "RAW": ["L0_", "L1A", "L1B", "L1C", "L2A"],
        "DASC": ["L0_", "L1A"],
        "ABSR": ["L0_", "L1A"],
        "EOBS": ["L0_", "L1A"],
        "DARK-O": ["L0_", "L1A"],
        "DARK-C": ["L0_", "L1A"],
        "SUN": ["L0_", "L1A"],
        "HKTM": ["L0_"],
        "MSMOON": ["L0_"],
    }

    STATIC_COMPLETENESS_VALUE = {"MSI_L.*_DS": 3608000 + 1000000}

    def __init__(self, meta=None, **kwargs):
        super().__init__(meta, **kwargs)
        self.number_of_expected_tiles = 0

    def product_type_with_missing_periods(self, product_type: str) -> bool:
        """Do we want missing periods for this product type ?"""
        return product_type == "MSI_L0__DS"

    def product_type_with_duplicated(self, product_type: str) -> bool:
        """Do we want check duplicated for this product type ?"""
        return product_type.endswith("DS")

    def get_expected_from_product_level(self, product_level):
        """Get expected from the product level

        Args:
            product_level (str): product level thaht we want expected

        Returns:
            dict: expect dict for the given product level
        """

        if (
            self.instrument_mode
            not in self.S2_NUMBER_OF_GR_PER_SCENE_PER_INSTRUMENT_DICT
        ):
            LOGGER.critical(
                "Unhandled instrument mode '%s' in %s. Unable to calculate expected products.",
                self.instrument_mode,
                self,
            )
            return {}

        # find a better name and set top level conf

        # - 3608000 -> remove one scene (cause first and last gr are at the half)
        # - 1000000 -> remove one sec (cause millisec are truncate)

        s2_number_of_gr_per_scene = self.S2_NUMBER_OF_GR_PER_SCENE_PER_INSTRUMENT_DICT[
            self.instrument_mode
        ]

        s2_expected_from_product_level_dict = {
            "L0_": {
                "DS": self.observation_duration,
                "GR": self.number_of_scenes * s2_number_of_gr_per_scene,
            },
            "L1A": {
                "DS": self.observation_duration - (2 * 3608000),
                "GR": (self.number_of_scenes - 2) * s2_number_of_gr_per_scene,
            },
            "L1B": {
                "DS": self.observation_duration - (2 * 3608000),
                "GR": (self.number_of_scenes - 2) * s2_number_of_gr_per_scene,
            },
            "L1C": {
                "DS": self.observation_duration - (2 * 3608000),
                "TL": self.number_of_expected_tiles,
                "TC": self.number_of_expected_tiles,
            },
            "L2A": {
                "DS": self.observation_duration - (2 * 3608000),
                "TL": self.number_of_expected_tiles,
                "TC": self.number_of_expected_tiles,
            },
        }

        # apply tolerance for product_level only
        product_level_with_tolerance = s2_expected_from_product_level_dict.get(
            product_level, {}
        )
        for key in product_level_with_tolerance:
            tolerance_value = tolerance.get_completeness_tolerance(
                self.COMPLETENESS_TOLERANCE,
                self.mission,
                CompletenessScope.LOCAL,
                f"MSI_{product_level}_{key}",
            )
            sensing_value_with_tolerance = (
                product_level_with_tolerance[key] + tolerance_value
            )

            # avoid negative sensing
            product_level_with_tolerance[key] = max(0, sensing_value_with_tolerance)

        return product_level_with_tolerance

    @classmethod
    def expected_type_per_level(cls, product_level):
        """Return the expected type for the given product_level

        Args:
            product_level (str): The product level to get expecte type

        Returns:
            list(str): the list of the type of product expected for this level
        """
        return cls.S2_EXPECTED_TYPE_FROM_PRODUCT_LEVEL_DICT.get(product_level, [])

    def get_expected_product_level(self):
        """Get expected product_level for the datatake

        Returns:
            list: a list of the expected product level
        """

        product_level_to_get = self.S2_PRODUCT_LEVEL_FROM_INSTRUMENT_DICT.get(
            self.instrument_mode, ["L0_"]
        )

        # We need to get at least 3 scenes to compute level L1 and L2
        if self.number_of_scenes < 3:
            product_level_to_get = ["L0_"]

        return product_level_to_get

    def impact_other_calculation(self, compute_key):
        """MSI_L1C_DS provide footprint to evaluated expected tiles

        Args:
            compute_key (tuple): the key of the compute that will be execute

        Returns:
            list(tuple): compute keys default: []
        """
        compute_product_type = compute_key[1]

        if self.REFERENCE_PRODUCT_TYPE_SENSING in compute_product_type:
            # build compute key to process

            self.number_of_expected_tiles = len(self.search_expected_tiles())

            product_types_to_compute = [
                product_type
                for product_type in self.get_all_product_types()
                if "TL" in product_type or "TC" in product_type
            ]

            return [
                (compute_key[0], product_type)
                for product_type in product_types_to_compute
            ]
        return []

    def load_data_before_compute(self):
        """Some step need to be done before starting compute all completeness"""

        # Evaluate expected tiles before compute completeness
        self.number_of_expected_tiles = len(self.search_expected_tiles())

        # Try to rattach products which have no datatake id to this datatake using sensing date
        # Also update the datastrip_ds and product_group_ids list of the datatake
        search_request = (
            CdsProduct.search()
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("term", mission=self.mission)
            .filter("exists", field="prip_id")
            .filter("range", sensing_start_date={"gte": self.observation_time_start})
            .filter("range", sensing_end_date={"lte": self.observation_time_stop})
            .filter("terms", product_type=self.get_all_product_types())
            .params(ignore=404)
        )
        res = search_request.execute()
        if res:
            for product in res:
                self.retrieve_additional_fields_from_product(product)

                if product.datatake_id in ("", utils.DATATAKE_ID_MISSING_VALUE):
                    product.datatake_id = self.datatake_id
                    LOGGER.info(
                        "Load_data_before_compute - CdsProduct with key:%s had"
                        " no datake_id, using sensing date it has been rattached"
                        " to datatake_id: %s",
                        product.key,
                        self.datatake_id,
                    )
                    yield product

    def search_expected_tiles(self) -> set[str]:
        """Look for expected tiles for this datatake

        Returns:
            int: the number of expected tiles for the whole datatake
        """
        products_scan = self.find_brother_products_scan(
            self.REFERENCE_PRODUCT_TYPE_SENSING,
        )
        expected_tiles = set()
        for product in products_scan:
            if product.expected_tiles:
                expected_tiles.update(product.expected_tiles)

        LOGGER.info(
            "Getting expected tiles %s",
            sorted(expected_tiles),
        )
        return expected_tiles

    def evaluate_all_global_expected(self):
        """Return global expected

        Returns:
            dict: The global expected of this datatake
        """

        global_expected = {}

        product_level_to_get = self.get_expected_product_level()

        for product_level in product_level_to_get:
            expected_for_product_level = self.get_expected_from_product_level(
                product_level
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

    def get_all_product_types(self):
        """Return all product type expected for this datatake

        Returns:
            list: List of all product type expected for this datatake
        """
        product_types = []

        product_level_to_get = self.get_expected_product_level()
        for product_level in product_level_to_get:
            expected_types_for_product_level = self.expected_type_per_level(
                product_level
            )

            for key in expected_types_for_product_level:
                # rebuild the product_type
                product_type = f"MSI_{product_level}_{key}"
                product_types.append(product_type)

        return product_types

    def compute_local_value(self, product_type, related_documents=None):
        """Compute local value for a specific product_type

        Args:
            product_type (str): Product type that we want to compute the value
        """

        LOGGER.debug(
            "[%s] - Compute local value for %s",
            self.datatake_id,
            product_type,
        )

        brother_of_datatake_documents = self.get_product_compute_brother(product_type)

        compute_method = self.get_compute_method(product_type)

        value = compute_method(brother_of_datatake_documents)

        if value > 0:
            value += tolerance.get_tolerance_from_scope(
                self.STATIC_COMPLETENESS_VALUE, product_type
            )

        if related_documents is not None:
            related_documents.extend(brother_of_datatake_documents)

        return value

    def get_compute_method(self, product_type):
        """Return the aggragation method for a product type

        Args:
            product_type (str): the product type where we want the compute method

        Returns:
            callable: the method to compute the completeness value
        """
        key_field = self.get_global_key_field(product_type)

        compute_method = None

        if key_field in ["TL", "TC", "GR"]:
            compute_method = len

        elif key_field in ["DS"]:
            compute_method = compute_total_sensing_product

        else:
            LOGGER.warning(
                "[%s] - Unhandle product_type for S2 on get_compute_method : %s",
                self.datatake_id,
                product_type,
            )

        return compute_method

    def get_product_compute_brother(self, key_field):
        """The method who returns all product with the same compute key

        Args:
            key_field (str): the product type who is also a part of a compute key

        Returns:
            list: products with the same key_field
        """
        # for s2 key_field is the product_type
        product_type = key_field

        LOGGER.debug(
            "[%s] - get_product_compute_brother for %s",
            self.datatake_id,
            product_type,
        )

        products_scan = self.find_brother_products_scan(
            product_type,
        )
        brother_of_datatake_documents = None

        key_field = self.get_global_key_field(product_type)

        if key_field in ["GR"]:
            brother_of_datatake_documents = set()

            for product in products_scan:
                if product.sensing_start_date and product.detector_id:
                    # Group by detector id and ± tolerance on sensing_start_date
                    for (
                        sensing_start_date,
                        detector_id,
                    ) in brother_of_datatake_documents:
                        if (
                            detector_id == product.detector_id
                            and abs(
                                sensing_start_date.timestamp()
                                - product.sensing_start_date.timestamp()
                            )
                            <= self.TOLERENCE_SENSING_START_GRANULE
                        ):
                            break
                    else:
                        brother_of_datatake_documents.add(
                            (
                                product.sensing_start_date,
                                product.detector_id,
                            )
                        )

                else:
                    LOGGER.warning(
                        "[%s][%s] - Failed to add it in document brothers [ %s, %s]",
                        self.datatake_id,
                        product.key,
                        product.sensing_start_date,
                        product.detector_id,
                    )

        elif key_field in ["TL", "TC"]:
            # get unique TL/TC number
            brother_of_datatake_documents = set()

            for product in products_scan:
                if product.tile_number:
                    brother_of_datatake_documents.add(product.tile_number)
                else:
                    LOGGER.warning(
                        "[%s][%s] - Failed to add it in document brothers [ %s, %s]",
                        self.datatake_id,
                        product.key,
                        product.sensing_start_date,
                        product.tile_number,
                    )

        elif key_field in ["DS"]:
            brother_of_datatake_documents = []

            for product in products_scan:
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

        else:
            LOGGER.warning(
                "[%s] - Unhandle product_type for S2 on get_product_compute_brother : %s",
                self.datatake_id,
                product_type,
            )

        return brother_of_datatake_documents

    def evaluate_local_expected(self, product_type):
        """Evaluate expected for a specific product_type

        Args:
            product_type (str): product_type that we want to get the local expected

        Returns:
            int: The local expected value of this datatake and the given product_type
        """
        product_level = product_type[4:7]
        local_expected_product_type = self.get_expected_from_product_level(
            product_level
        )

        key_field_value = self.get_global_key_field(product_type)
        expected_value = local_expected_product_type.get(key_field_value, None)

        return expected_value

    def get_global_key_field(self, product_type):
        """Global key is the aggregation of local value.
        Because we can't mix carrots and potatoes we have this method to extract a aggregation key

        Args:
            product_type (_type_): _description_

        Returns:
            _type_: _description_
        """
        return product_type[-2:]

    def compute_extra_completeness(self):
        """Need to compute product level completeness and final for snetinel 2"""

        LOGGER.info(
            "[%s] - Compute extra completeness",
            self.datatake_id,
        )

        final_expected = final_value = 0
        product_level_to_get = self.get_expected_product_level()

        for product_level in product_level_to_get:
            LOGGER.debug(
                "[%s] - Extra completeness : %s", self.datatake_id, product_level
            )

            product_level_expected = product_level_value = 0

            expected_for_product_level = self.get_expected_from_product_level(
                product_level
            )

            for key in expected_for_product_level:
                # rebuild the product_type
                product_type = f"MSI_{product_level}_{key}"

                attr_product_type_value = f"{product_type}_local_value_adjusted"
                product_type_value = getattr(self, attr_product_type_value, 0)

                attr_expected_ds_value = f"MSI_{product_level}_DS_local_expected"
                expected_ds_value = getattr(self, attr_expected_ds_value, 0)

                attr_product_type_expected = f"{product_type}_local_expected"
                expected_value = getattr(self, attr_product_type_expected, 0)

                if 0 in (expected_ds_value, expected_value):
                    # Sometime geometry arrive later
                    LOGGER.warning(
                        "[%s] - Missing expected : %s -> %s | DS : %s -> %s",
                        self.datatake_id,
                        attr_product_type_expected,
                        expected_value,
                        attr_expected_ds_value,
                        expected_ds_value,
                    )
                    value = 0
                    expected = 0

                else:
                    value = expected_ds_value / expected_value * product_type_value
                    expected = expected_ds_value

                product_level_value += value
                product_level_expected += expected

                final_value += value
                final_expected += expected

            # product level completeness
            if product_level_expected == 0:
                LOGGER.warning(
                    "[%s] - No product level expected for : %s",
                    self.datatake_id,
                    product_level,
                )

                product_level_percentage = 0

            else:
                product_level_percentage = (
                    product_level_value / product_level_expected * 100
                )

            setattr(self, f"{product_level}_local_value", product_level_value)
            setattr(self, f"{product_level}_local_expected", product_level_expected)

            setattr(self, f"{product_level}_local_percentage", product_level_percentage)
            setattr(
                self,
                f"{product_level}_local_status",
                evaluate_completeness_status(product_level_percentage),
            )

        # final completeness
        if final_expected == 0:
            LOGGER.warning(
                "[%s] - No final expected",
                self.datatake_id,
            )
            percentage = 0
        else:
            percentage = final_value / final_expected * 100

        setattr(self, "final_completeness_value", final_value)
        setattr(self, "final_completeness_expected", final_expected)

        setattr(self, "final_completeness_percentage", percentage)
        setattr(
            self, "final_completeness_status", evaluate_completeness_status(percentage)
        )

    def get_related_documents_query(self) -> Q:
        """override"""

        # We match all product between observation ± delta in seconds

        start_date = self.observation_time_start - timedelta(
            seconds=self.MATCHING_DELTA_PRODUCTS
        )
        end_date = self.observation_time_stop + timedelta(
            seconds=self.MATCHING_DELTA_PRODUCTS
        )
        return Q(
            "bool",
            filter=[
                Q("term", satellite_unit=self.satellite_unit),
                Q(
                    "range",
                    sensing_start_date={"gte": start_date},
                ),
                Q(
                    "range",
                    sensing_end_date={"lte": end_date},
                ),
            ],
        )

    def retrieve_additional_fields_from_product(self, product: CdsProduct):
        """Fill the datastrip_ids and product_group_ids field of the datatake using the value
        from the product
        Args:
            products (CdsProduct): Product which belongs to this datatake
        """

        if (
            "datastrip_id" in product
            and product.datastrip_id
            and product.datastrip_id not in self.datastrip_ids
        ):
            LOGGER.debug(
                "datastrip_id %s has been added to the list of datastrip_id of datatake:%s because of CdsProduct:%s",
                product.datastrip_id,
                self.datatake_id,
                product.key,
            )
            self.datastrip_ids.append(product.datastrip_id)

        if (
            "product_group_id" in product
            and product.product_group_id
            and product.product_group_id not in self.product_group_ids
        ):
            LOGGER.debug(
                "product_group_id %s has been added to the list of product_group_ids of datatake:%s because of CdsProduct:%s",
                product.product_group_id,
                self.datatake_id,
                product.key,
            )
            self.product_group_ids.append(product.product_group_id)
