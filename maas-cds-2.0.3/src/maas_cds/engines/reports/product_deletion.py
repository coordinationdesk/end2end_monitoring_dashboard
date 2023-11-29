"""Deletion consolidation"""
import itertools
from typing import List, Generator

from opensearchpy.exceptions import NotFoundError

from maas_engine.engine.rawdata import DataEngine

from maas_cds.model import (
    DeletionIssue,
    ProductDeletion,
    CdsInterfaceProductDeletion,
    CdsProduct,
    CdsPublication,
)

from maas_cds.lib.parsing_name.utils import remove_extension_from_product_name

from maas_cds.lib.parsing_name.utils import (
    normalize_product_name_list,
    normalize_product_name,
)


class DeletionConsolidatorEngine(DataEngine):
    """Consolidate CdsInterfaceProductDeletion / DeletionIssue"""

    ENGINE_ID = "CONSOLIDATE_DELETION"

    def __init__(self, args=None, send_reports=True, interface_dict=None):
        super().__init__(args, send_reports=send_reports)
        if not interface_dict:
            self.logger.error("You must supply an interface dict")
            interface_dict = {}

        self.interface_dict = interface_dict

    def translate_service_ids(self, names: List[str]) -> List[str]:
        """
        Translate user input to real service name using the engine parameter map

        Args:
            names (List[str]): service names from jira ticket

        Returns:
            List[str]: translated names
        """
        return [self.interface_dict.get(name.lower(), name) for name in names]

    def action_iterator(self):
        """route the action iterator depending of the payload document class"""
        document_class = self.payload.document_class

        if document_class == "CdsInterfaceProductDeletion":
            yield from self.action_iterator_from_deletions(self.input_documents)

        elif document_class == "DeletionIssue":
            for issue in self.input_documents:
                yield from self.action_iterator_from_issue(issue)

        else:
            raise TypeError(
                f"Unexpected input document class for deletion: {document_class}"
            )

    def action_iterator_from_issue(self, issue: DeletionIssue):
        """
        Generate bulk action of products and publication based on a deletion issue

        Args:
            issue (DeletionIssue): issue containing deletion info

        Yields:
            dict: bulk actions
        """

        try:
            deletion_result = (
                CdsInterfaceProductDeletion.search()
                .filter("term", jira_issue=issue.key)
                .params(size=10000)
                .execute()
            )
        except NotFoundError as error:
            self.logger.info(
                "CdsInterfaceProductDeletion is not populated yet: skipping"
            )
            return

        # get the deletion related to the issue
        product_names = normalize_product_name_list(
            [deletion.product_name for deletion in deletion_result]
        )

        service_ids = self.translate_service_ids(issue.interfaces_to_remove_list)

        yield from self.action_iterator_from_deletable(
            issue,
            service_ids,
            self.deletable_iterator(
                product_names,
                issue.interface_type,
                service_ids,
            ),
        )

    def action_iterator_from_deletions(
        self, deletion_list: List[CdsInterfaceProductDeletion]
    ):
        """
        Generate bulk action of products and publication based on a list of product
        deletion

        Args:
            deletion_list (List[CdsInterfaceProductDeletion]): product deletions

        Yields:
            dict: bulk actions
        """

        # map issue identifiers with product. nominal case has only one issue
        issue_product_dict = {}

        # get the deletion related to the issue
        for deletion in deletion_list:
            if deletion.jira_issue not in issue_product_dict:
                issue_product_dict[deletion.jira_issue] = []

            issue_product_dict[deletion.jira_issue].append(
                normalize_product_name(deletion.product_name)
            )

        # map the issues into a dict
        issue_dict = {
            issue.key: issue
            for issue in DeletionIssue.search()
            .filter("terms", key=list(issue_product_dict.keys()))
            .params(ignore=404, size=len(deletion_list))
            .execute()
        }

        for issue_id, product_names in issue_product_dict.items():
            if not issue_id in issue_dict:
                self.logger.warning(
                    "Issue %s does not exist (yet): skipping deletion", issue_id
                )
                continue

            issue = issue_dict[issue_id]

            service_ids = self.translate_service_ids(issue.interfaces_to_remove_list)

            yield from self.action_iterator_from_deletable(
                issue,
                service_ids,
                self.deletable_iterator(
                    product_names,
                    issue.interface_type,
                    service_ids,
                ),
            )

    def action_iterator_from_deletable(
        self,
        issue: DeletionIssue,
        service_ids: List[str],
        deletable_iterator: Generator,
    ):
        """
        Generate bulk action of document marked deleted

        Args:
            issue (DeletionIssue): origin issue
            service_ids (List[str]): list of services to mark as deleted
            deletable_iterator (Generator): a generator of document to mark as deleted

        Yields:
            _type_: _description_
        """
        for deletable in deletable_iterator:
            original_deletable_dict = deletable.to_dict()

            deletable.mark_as_deleted(issue, service_ids)

            if original_deletable_dict | deletable.to_dict() != original_deletable_dict:
                yield deletable.to_bulk_action()

    def deletable_iterator(
        self, products_names: List[str], service_type: str, service_ids: List[str]
    ):
        """Get a generator deletable documents (products and publications) based on
        criteria arguments

        Args:
            products_names (List[str]): product to mark deleted
            service_type (str): service type (currently DD or LTA)
            service_ids (List[str]): service identifiers

        Returns:
            Generator:
        """
        self.logger.debug(
            "Get %d deletables for %s / %s",
            len(products_names),
            service_type,
            service_ids,
        )

        products = (
            CdsProduct.search()
            .filter("terms", name=products_names)
            .params(version=True, seq_no_primary_term=True, ignore=404, size=10000)
            .execute()
        )

        if service_type == "DD":
            # strip extensions
            products_names = [
                remove_extension_from_product_name(name) for name in products_names
            ]

        publications = (
            CdsPublication.search()
            .filter(
                "term",
                service_type=service_type,
            )
            .filter(
                "terms",
                service_id=service_ids,
            )
            .filter(
                "terms",
                name=products_names,
            )
            .params(version=True, seq_no_primary_term=True, ignore=404, size=10000)
            .execute()
        )

        return itertools.chain(
            products,
            publications,
        )
