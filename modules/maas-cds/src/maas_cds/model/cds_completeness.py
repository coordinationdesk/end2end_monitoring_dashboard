""" Custom CDS model definition """

import logging

from maas_cds.model.datatake import CdsDatatake
from maas_cds.model.publication import CdsPublication

from maas_cds.model import generated

__all__ = ["CdsCompleteness"]


LOGGER = logging.getLogger("CdsModelCompleteness")


class CdsCompleteness(generated.CdsCompleteness, CdsDatatake):

    def find_brother_products_scan(self, product_type):
        """Find products with the same datatake and the same product_type

        Note: Seek only product with a prip_id

        Args:
            product_type (str): product_type searched

        Returns:
            list(CdsPublication): list of products matching datatake_id and product_type
        """
        # TODO MAAS_CDS-1236: make a single query to find all the whole brotherhood
        # with list of datatake / product types later post-processed to be grouped by
        # tuple (datatake_id, product_type) in a dict

        search_request = (
            CdsPublication.search()
            .filter("term", datatake_id=self.datatake_id)
            .filter("term", satellite_unit=self.satellite_unit)
            .filter("term", product_type=product_type)
            .filter("term", service_id=self.prip_name)
            .filter("term", service_type="PRIP")
            .params(ignore=404)
        )

        query_scan = search_request.scan()

        return query_scan

    def retrieve_additional_fields_from_publication(self, product: CdsPublication):
        """Abstract function which allow to fill additional
        datatake fields during completeness calculation"""
