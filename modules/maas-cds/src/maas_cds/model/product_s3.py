""" Custom CDS model definition for s3 product"""

import logging

from maas_cds.model.product import CdsProduct
from maas_cds import model
import maas_cds.lib.parsing_name.utils as utils

__all__ = ["CdsProductS3"]


LOGGER = logging.getLogger("CdsModelProductS3")


class CdsProductS3(CdsProduct):
    """CdsProduct specific for sentinel 3"""

    def get_datatake_id(self):
        """Return the associate datatake id of the product

        Returns:
            str: associate cds-datatake id
        """

        return f"{self.datatake_id}" if not self.datatake_id_is_missing() else None

    def get_compute_key(self):
        """Compose compute key from product (used to match completeness)

        Returns:
            str: a combinaison as key allowing us to group product computation
                format is <datatake_id>#<product_type>#<timeliness>
        """

        # on S3 completeness is excluded for sseveral products types
        if model.cds_s3_completeness.CdsS3Completeness.is_exclude_for_completeness(
            self.product_type
        ):
            return None

        return self.calculate_compute_key(
            self.get_datatake_id(), self.product_type, self.timeliness
        )

    @staticmethod
    def calculate_compute_key(datatake_id: str, product_type: str, timeliness: str):
        if None in [datatake_id, product_type, timeliness]:

            LOGGER.warning(
                "Can't create a compute_key : %s %s %s",
                datatake_id,
                product_type,
                timeliness,
            )

            return None

        return datatake_id + "#" + product_type + "#" + timeliness

    def data_for_completeness(self):
        """compose defaults completeness values from product

        Returns minimal completenes values
        """
        return {
            "key": self.get_compute_key(),
            "datatake_id": self.datatake_id,
            "mission": self.mission,
            "satellite_unit": self.satellite_unit,
            "timeliness": self.timeliness,
            "product_type": self.product_type,
            "product_level": self.product_level,
            "observation_time_start": self.sensing_start_date,
            "observation_time_stop": self.sensing_end_date,
        }
