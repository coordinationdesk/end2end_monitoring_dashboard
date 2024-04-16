""" Custom CDS model definition for s2 product"""

import logging

from maas_cds.lib.queryutils.find_datatake_from_sensing import (
    find_datatake_from_sensing,
)
from maas_cds.lib.queryutils.find_datatake_from_product_group_id import (
    find_datatake_from_product_group_id,
)
from maas_cds.model.product import CdsProduct
import maas_cds.lib.parsing_name.utils as utils


__all__ = ["CdsProductS2"]


LOGGER = logging.getLogger("CdsModelProductS2")


class CdsProductS2(CdsProduct):
    """CdsProduct specific for sentinel 2"""

    NO_DATATAKE_PRODUCT_TYPES = ("AUX_SADATA", "OLQC_REPORT", "PRD_HKTM__")

    PRODUCT_TYPES_WITH_TILES = ("MSI_L1C_DS", "MSI_L2A_DS")

    def get_datatake_id(self):
        """Return the associate datatake id of the product

        Returns:
            str: associate datatake id
        """

        if not self.datatake_id or self.datatake_id == utils.DATATAKE_ID_MISSING_VALUE:
            self.find_datatake_id()

        return (
            f"{self.satellite_unit}-{self.datatake_id}"
            if not self.datatake_id_is_missing()
            else None
        )

    def find_datatake_id(self):
        """Find datatake id associate to the product

        For sentinel 2 we need to look in datatake if a mission planning cover the product range
        This method allow product to search in datatake
        and retrieve all matching datatake who cover the product

        """
        # prevent search for products that are not attached to any datastrip
        if self.product_type in CdsProductS2.NO_DATATAKE_PRODUCT_TYPES:
            return

        datatake_document_that_match = find_datatake_from_product_group_id(
            mission=self.mission,
            satellite=self.satellite_unit,
            product_group_id=self.product_group_id,
        )

        if len(datatake_document_that_match) == 0:
            datatake_document_that_match = find_datatake_from_sensing(
                start_date=self.sensing_start_date,
                end_date=self.sensing_end_date,
                mission=self.mission,
                satellite=self.satellite_unit,
            )

        nb_datatake_document_that_match = len(datatake_document_that_match)

        if nb_datatake_document_that_match > 1:
            LOGGER.warning(
                "[%s] - Product match with %s datatake document",
                self.key,
                nb_datatake_document_that_match,
            )

        if nb_datatake_document_that_match == 0:
            LOGGER.warning(
                "[%s] - Product can't match with datatake document", self.key
            )
            product_datatake_id = None
        else:
            product_datatake_id = datatake_document_that_match[0].datatake_id

        setattr(
            self, "nb_datatake_document_that_match", nb_datatake_document_that_match
        )
        setattr(self, "datatake_id", product_datatake_id)

    def get_compute_key(self):
        if self.product_type[-2:] not in ["GR", "TL", "TC", "DS"]:
            LOGGER.debug("ComputeKey -> wrong product_type : %s", self.product_type)
            return None

        if self.get_datatake_id() is None:
            LOGGER.debug("ComputeKey -> no datatake_id : %s", self.datatake_id)
            return None

        return (self.get_datatake_id(), self.product_type)
