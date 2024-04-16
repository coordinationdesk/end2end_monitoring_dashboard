""" Custom CDS model definition for publication"""

import logging

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
