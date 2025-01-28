""" Datatake S1 model definition """

import logging
from typing import Callable
from opensearchpy import Q

from maas_cds.model import CdsCompleteness, CdsDatatakeS1, CdsPublication

from maas_cds.lib import tolerance


__all__ = ["CdsCompletenessS1"]


LOGGER = logging.getLogger("CdsModelCompletenessS1")


class CdsCompletenessS1(CdsCompleteness, CdsDatatakeS1):
    """CdsDatatake custom class for Sentinel 1"""

    REFERENCE_PRODUCT_TIME_FIELD = "publication_date"

    def get_slc_1s_count(self):
        """Count all SLC__1S products that are linked to the datatake

        Returns:
            int: count of products
        """
        search = (
            CdsPublication.search()
            .filter("term", datatake_id=self.datatake_id)
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("term", product_type=f"{self.instrument_mode}_SLC__1S")
            .filter("term", service_type="PRIP")
            .filter("term", service_id=self.prip_name)
        )

        count = search.count()

        return count

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
            return [(compute_key[0], f"{compute_key[1][:2]}_ETA__AX"), compute_key[2]]

        if self.REFERENCE_PRODUCT_TYPE_SENSING in compute_product_type:
            # build compute key to process
            product_types_to_compute = [
                product_type
                for product_type in self.get_all_product_types()
                if self.product_type_over_specific_area(product_type)
            ]

            extra_compute_key = [
                (compute_key[0], product_type, compute_key[2])
                for product_type in product_types_to_compute
            ]

        return extra_compute_key
