"""Update entities after some products from containers are seen"""
import typing

from opensearchpy import MultiSearch

from maas_engine.engine.rawdata import DataEngine

import maas_cds.model as model


class ComputeContainerProductsEngine(DataEngine):
    """Update documents related to datatake creation or update"""

    ENGINE_ID = "COMPUTE_CONTAINER_PRODUCTS"

    def __init__(self, args=None, send_reports=False, chunk_size=0, dd_attrs=None):
        """constructor

        Args:
            args (namespace, optional): cli options. Defaults to None.
            send_reports (bool, optional): flag. Defaults to False.
        """

        super().__init__(args, send_reports=send_reports, chunk_size=chunk_size)

        self.dd_attrs = dd_attrs or {}

    def action_iterator(self) -> typing.Generator:
        """override

        Iter throught input documents and find products who are inside
        Then add informations on these products

        Yields:
            Iterator[typing.Generator]: bulk actions
        """
        msearch = MultiSearch()

        # Documents are CdsProductS2 from PRIP consolidation
        for document in self.input_documents:
            # use creation_date as product_discriminator_date, used by related container
            # to make the link with product_discriminator_date

            # try to find a container at DDHUS
            msearch = msearch.add(
                model.CdsPublication.search()
                .filter("term", satellite_unit=document.satellite_unit)
                # creation date make the link with container
                .filter(
                    "term",
                    product_discriminator_date=document.product_discriminator_date,
                )
                .filter("term", product_level=document.product_level)
                .filter("terms", product_type=model.DdProduct.S2_CONTAINER_TYPES)
                .filter("term", tile_number=document.tile_number)
                .filter("term", service_type="DD")
            )

        # process results
        for document, response in zip(self.input_documents, msearch.execute()):
            matched_dd_publication = list(response)

            if len(matched_dd_publication) == 0:
                self.logger.debug(
                    "%s document: no container found yet for %s",
                    document,
                    document.name,
                )
                continue

            initial_dict = document.to_dict()

            for container in matched_dd_publication:
                dd_attr_config = self.dd_attrs.get(container.service_id)

                if dd_attr_config is None:
                    self.logger.error(
                        "Unknown dd service_id name : %s. "
                        "Cannot associate with container for product : %s.",
                        container.service_id,
                        document.name,
                    )
                    continue

                setattr(
                    document,
                    dd_attr_config["container_id"],
                    container.meta.id,
                )
                setattr(
                    document,
                    dd_attr_config["container_name"],
                    container.name,
                )
                setattr(
                    document,
                    dd_attr_config["publication_date"],
                    container.publication_date,
                )

            if initial_dict != document.to_dict():
                yield document.to_bulk_action()
            else:
                self.logger.debug("%s has no modification", document)
