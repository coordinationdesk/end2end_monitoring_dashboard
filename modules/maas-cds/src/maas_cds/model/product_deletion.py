""" Custom CDS model definition for product deletion"""
from typing import List

from maas_model import ZuluDate

from maas_cds.model import generated


__all__ = ["DeletionIssue", "ProductDeletion", "CdsInterfaceProductDeletion"]


class CdsInterfaceProductDeletion(generated.CdsInterfaceProductDeletion):
    """
    CdsInterfaceProductDeletion override because ingestionTime is excluded from
    generation
    """

    ingestionTime = ZuluDate()


class ProductDeletion(generated.ProductDeletion):
    """ProductDeletion custom"""

    @property
    def jira_issue(self) -> str:
        """Get the issue name contained in the report name

        Returns:
            str: The issue name
        """
        return self.reportName.split("_")[0]


class DeletionIssue(generated.DeletionIssue):
    """DeletionIssue custom"""

    @property
    def interfaces_to_remove_list(self) -> set[str]:
        """Get the set of service to remove"""
        if not self.deletion_interfaces:
            return set()
        return set(name.strip() for name in self.deletion_interfaces)
