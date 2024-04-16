""" Custom CDS model definition for s5 product"""

import logging

from maas_cds.model.product import CdsProduct
from maas_cds import model
import maas_cds.lib.parsing_name.utils as utils

__all__ = ["CdsProductS5"]


LOGGER = logging.getLogger("CdsModelProductS5")


class CdsProductS5(CdsProduct):
    """CdsProduct specific for sentinel 5"""

    def get_datatake_id(self):
        """Return the associate datatake id of the product

        Returns:
            str: associate cds-datatake id
        """

        return self.datatake_id if not self.datatake_id_is_missing() else None

    def get_compute_key(self):
        """Compose compute key from product (used to match completeness)

        Returns:
            str: a combinaison as key allowing us to group product computation <datatake_id>-<product_type>
        """
        # on S5 completeness is excluded for several products types
        if model.cds_s5_completeness.CdsS5Completeness.is_exclude_for_completeness(
            self.product_type
        ):
            return None

        if None in [
            self.mission,
            self.get_datatake_id(),
            self.product_type,
            self.absolute_orbit,
        ]:
            LOGGER.warning(
                "[%s] - Can't create a compute_key : %s %s",
                self.meta.id,
                self.get_datatake_id(),
                self.product_type,
            )

            return None

        return self.get_datatake_id() + "-" + self.product_type

    def data_for_completeness(self):
        """compose defaults completeness values from product

        Returns minimal completenes values
        """
        return {
            "key": self.get_compute_key(),
            "datatake_id": self.datatake_id,
            "absolute_orbit": self.absolute_orbit,
            "mission": self.mission,
            "satellite_unit": self.satellite_unit,
            "timeliness": self.timeliness,
            "product_type": self.product_type,
            "product_level": self.product_level,
            "observation_time_start": self.sensing_start_date,
            "observation_time_stop": self.sensing_end_date,
        }
