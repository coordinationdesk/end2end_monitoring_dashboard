"""
This file contain all mixin to be used for dissemination products
"""
import logging

__all__ = ["DisseminationMixin"]

LOGGER = logging.getLogger("DisseminationMixin")


class DisseminationMixin:
    """class mixin for dissemination products"""

    # Possible container types
    S2_CONTAINER_TYPES = ("MSI_L1C___", "MSI_L2A___")

    # Possible product types contained in a DD container
    S2_CONTAINED_TYPES = (
        "MSI_L1C_TC",
        "MSI_L1C_TL",
        "MSI_L2A_TC",
        "MSI_L2A_TL",
    )
