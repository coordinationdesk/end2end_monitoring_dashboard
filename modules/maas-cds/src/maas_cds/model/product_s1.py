""" Custom CDS model definition for s1 product"""

import logging

from maas_cds.model.product import CdsProduct, DynamicPartitionMixin
from maas_cds.model.datatake_s1 import CdsDatatakeS1

__all__ = ["CdsProductS1"]


LOGGER = logging.getLogger("CdsModelProductS1")


class CdsProductS1(CdsProduct):
    """CdsProduct specific for sentinel 1"""

    def get_compute_key(self):
        """override specific method for sentinel 1

        Returns:
            tuple: a tuple as key allowing us to group product computation
        """

        # This is based on dataflow
        if (
            not self.get_datatake_id()
            and self.product_level
            not in DynamicPartitionMixin.PRODUCT_LEVEL_THAT_MAKE_SENSE
            or self.instrument_mode
            not in (
                "SM",
                "IW",
                "EW",
                "WV",
                "RFC",
                "Z1",
                "Z2",
                "Z3",
                "Z4",
                "Z5",
                "Z6",
                "ZI",
                "ZE",
                "ZW",
                "AIS",
            )
            or self.product_type in CdsDatatakeS1.EXCLUDES_PRODUCTED_TYPES
        ):
            return None

        return (self.get_datatake_id(), self.product_type)
