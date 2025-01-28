""" Custom CDS model definition for publication"""

import logging

from maas_cds.lib.parsing_name import utils
from maas_cds.model.datatake_s1 import CdsDatatakeS1
from opensearchpy import Keyword
from maas_cds.model.anomaly_mixin import AnomalyMixin
from maas_cds.model.dynamic_partition_mixin import DynamicPartitionMixin
from maas_cds.model.product_datatake_mixin import ProductDatatakeMixin

from maas_cds.model import generated

__all__ = ["CdsPublication"]


LOGGER = logging.getLogger("CdsPublication")


class CdsPublication(
    DynamicPartitionMixin, AnomalyMixin, ProductDatatakeMixin, generated.CdsPublication
):
    """CdsPublication custom"""

    cams_tickets = Keyword(multi=True)

    _PARTITION_FIELDS = [
        "publication_date",
    ]

    def mark_as_deleted(self, issue: "DeletionIssue", service_ids: dict = None):
        """Populate attributes to reflect deletion from the interface.

        Args:
            issue (DeletionIssue): issue
            service_ids (dict): Unused. Defaults to None
        """
        self.deletion_issue = issue.key
        self.deletion_date = issue.deletion_date
        self.deletion_cause = issue.deletion_cause

    def get_compute_key(self):

        if (
            self.service_type != "PRIP"
            and not self.get_datatake_id()
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

        return (self.get_datatake_id(), self.product_type, self.service_id)

    def get_datatake_id(self) -> str | None:
        """Return the associate datatake id of the product

        Returns:
            str: associate cds-datatake id
        """

        return (
            f"{self.satellite_unit}-{self.datatake_id}"
            if not self.datatake_id_is_missing()
            else None
        )

    def datatake_id_is_missing(self) -> bool:
        """Returns true if datatake id is missing or None

        Returns:
            boolean: datatake is missing
        """
        return (
            self.datatake_id is None
            or self.datatake_id == utils.DATATAKE_ID_MISSING_VALUE
        )
