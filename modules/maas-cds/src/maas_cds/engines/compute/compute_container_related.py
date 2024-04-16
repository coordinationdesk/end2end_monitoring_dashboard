"""Update entities after some container products are see"""
import typing

from opensearchpy import MultiSearch

from maas_engine.engine.rawdata import DataEngine

from maas_cds.lib.parsing_name.parsing_name_s2 import (
    extract_data_from_product_name_s2_compact_naming,
)
from maas_cds.model import CdsProductS2, DisseminationMixin


class ComputeContainerRelatedEngine(DataEngine):
    """Update documents related to datatake creation or update"""

    ENGINE_ID = "COMPUTE_CONTAINER_RELATED"

    def __init__(
        self,
        args=None,
        target_model: str = None,
        send_reports=False,
        chunk_size=0,
        dd_attrs=None,
    ):
        """constructor

        Args:
            args (namespace, optional): cli options. Defaults to None.
            target_model (str, optional): Model class name. Defaults to None.
            send_reports (bool, optional): flag. Defaults to False.
        """

        super().__init__(args, send_reports=send_reports, chunk_size=chunk_size)

        self.target_model = target_model

        self.dd_attrs = dd_attrs or {}

    def action_iterator(self) -> typing.Generator:
        """override

        Iter throught input documents and find products who are inside
        Then add informations on these products

        Yields:
            Iterator[typing.Generator]: bulk actions
        """

        msearch = MultiSearch()

        valid_input_documents = []

        for raw_document in self.input_documents:
            try:
                data_dict = extract_data_from_product_name_s2_compact_naming(
                    raw_document.product_name
                )
            except (ValueError, IndexError) as error:
                self.logger.error(
                    "Cannot parse product name: %s", raw_document.product_name
                )
                continue

            product_level = data_dict["product_level"]

            # find product types to find depending the product level
            contained_types = [
                content_type
                for content_type in DisseminationMixin.S2_CONTAINED_TYPES
                if product_level in content_type
            ]

            if not contained_types:
                self.logger.error(
                    "Product level %s is not handled by S2_CONTAINED_TYPES: %s",
                    product_level,
                    DisseminationMixin.S2_CONTAINED_TYPES,
                )
                continue

            valid_input_documents.append(raw_document)

            msearch = msearch.add(
                CdsProductS2.search()
                .filter("term", satellite_unit=data_dict["satellite_unit"])
                .filter("terms", product_type=contained_types)
                .filter("term", tile_number=data_dict["tile_number"])
                .filter(
                    "term",
                    product_discriminator_date=data_dict["product_discriminator_date"],
                )
            )

        if not valid_input_documents:
            self.logger.warning("No valid input documents")
            return

        # contained identifier to container instance as MultiSearch does not support
        # metadata like params(version=True, seq_no_primary_term=True)
        result_map = {}

        for raw_document, response in zip(valid_input_documents, msearch.execute()):
            if not response:
                self.logger.warning(
                    "No S2 product found container %s", raw_document.product_name
                )
                continue

            for document in response:
                # store link between content and container
                result_map[document.meta.id] = raw_document

        # retrieve again targeted documents as msearch does not support versionning :'(
        for document in CdsProductS2.mget_by_ids(list(result_map.keys())):
            raw_document = result_map[document.meta.id]

            initial_dict = document.to_dict()

            dd_attr_config = self.dd_attrs.get(raw_document.production_service_name)

            if dd_attr_config is None:
                self.logger.warning(
                    "Unhandle dd config for service %s",
                    raw_document.production_service_name,
                )
                continue

            setattr(
                document,
                dd_attr_config["container_id"],
                raw_document.product_id,
            )
            setattr(
                document,
                dd_attr_config["container_name"],
                raw_document.product_name,
            )
            setattr(
                document,
                dd_attr_config["publication_date"],
                raw_document.publication_date,
            )

            document.calculate_dd_timeliness(
                raw_document.production_service_name, self.dd_attrs
            )

            if initial_dict | document.to_dict() != initial_dict:
                self.logger.debug(
                    "[%s] - Update : %s",
                    document.meta.id,
                    document.name,
                )
                yield document.to_bulk_action()

            else:
                self.logger.debug(
                    "[%s] - Nothing to do : %s",
                    document.meta.id,
                    document.name,
                )
