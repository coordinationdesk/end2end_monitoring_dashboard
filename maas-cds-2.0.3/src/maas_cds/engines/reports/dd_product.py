"""DD Product consolidation"""
import typing

from maas_engine.engine.base import EngineReport

from maas_cds.engines.reports.anomaly_impact import anomaly_link
from maas_cds.engines.reports.product import ProductConsolidatorEngine

from maas_cds import model
from maas_cds.lib.parsing_name.parsing_name_s2 import (
    is_compact,
    extract_data_from_product_name_s2_compact_naming,
)


class DDProductConsolidatorEngine(ProductConsolidatorEngine):
    """Consolidate raw products to CdsProduct"""

    ENGINE_ID = "CONSOLIDATE_DD_PRODUCT"

    CONSOLIDATED_MODEL = model.CdsProduct

    def __init__(
        self,
        args=None,
        send_reports=True,
        min_doi=None,
        output_rk=None,
        chunk_size=0,
        container_chunk_size=0,
        dd_attrs=None,
    ):
        super().__init__(
            args,
            send_reports=send_reports,
            min_doi=min_doi,
            chunk_size=chunk_size,
            container_chunk_size=container_chunk_size,
        )

        self.output_rk = output_rk

        self.dd_attrs = dd_attrs or {}

        self.containers = []

    def is_valid_container(
        self,
        raw_document: typing.Union[
            model.DdProduct, model.DasProduct, model.CreodiasProduct
        ],
    ) -> bool:
        """
        Test if a container product if valid for attachement

        Args:
            raw_document (typing.Union[model.DdProduct, model.DasProduct]): container

        Returns:
            bool: True if the container shall be attached to products
        """
        # extract dict for sensing time
        data_dict = extract_data_from_product_name_s2_compact_naming(
            raw_document.product_name
        )
        # test if container shall be actually linked
        return (
            self.min_doi is None
            or data_dict["datatake_id_sensing_time"] >= self.min_doi
        )

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    @anomaly_link
    def consolidate_from_DdProduct(
        self, raw_document: model.DdProduct, document: model.CdsProduct
    ) -> model.CdsProduct:
        """Consolidate a DdProduct into CdsProduct

        Args:
            raw_document (model.DdProduct): raw DD DHUS document
            document (model.CdsProduct): target document

        Returns:
            model.CdsProduct: consolidated document
        """

        # Container products
        if is_compact(raw_document.product_name):
            if self.is_valid_container(raw_document):
                # Will forward message to another engine
                self.containers.append(raw_document)

            # Nothing to do with container products
            return None

        self.fill_common_attributes(raw_document, document, fill_name=False)

        document.ddip_name = raw_document.product_name

        document.ddip_publication_date = raw_document.publication_date

        document.calculate_dd_timeliness(
            raw_document.production_service_name, self.dd_attrs
        )

        return document

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    @anomaly_link
    def consolidate_from_DasProduct(
        self, raw_document: model.DasProduct, document: model.CdsProduct
    ) -> model.CdsProduct:
        """Consolidate a DasProduct into CdsProduct

        Args:
            raw_document (model.DdProduct): raw DD DHUS document
            document (model.CdsProduct): target document

        Returns:
            model.CdsProduct: consolidated document
        """

        # Container products
        if is_compact(raw_document.product_name):
            if self.is_valid_container(raw_document):
                # Will forward message to another engine
                self.containers.append(raw_document)

            # Nothing to do with container products
            return None

        self.fill_common_attributes(raw_document, document, fill_name=False)

        document.dddas_name = raw_document.product_name

        document.dddas_publication_date = raw_document.publication_date

        document.calculate_dd_timeliness(
            raw_document.production_service_name, self.dd_attrs
        )

        return document

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    @anomaly_link
    def consolidate_from_CreodiasProduct(
        self, raw_document: model.CreodiasProduct, document: model.CdsProduct
    ) -> model.CdsProduct:
        """Consolidate a CreodiasProduct into CdsProduct

        Args:
            raw_document (model.DdProduct): raw DD DHUS document
            document (model.CdsProduct): target document

        Returns:
            model.CdsProduct: consolidated document
        """

        # Container products
        if is_compact(raw_document.product_name):
            if self.is_valid_container(raw_document):
                # Will forward message to another engine
                self.containers.append(raw_document)

            # Nothing to do with container products
            return None

        self.fill_common_attributes(raw_document, document, fill_name=False)

        document.ddcreodias_name = raw_document.product_name

        document.ddcreodias_publication_date = raw_document.publication_date

        document.calculate_dd_timeliness(
            raw_document.production_service_name, self.dd_attrs
        )

        return document

    def _generate_reports(self):
        """Override to report only containers


        Yields:
            EngineReport: report
        """
        # deliberately don't call super()._generate_reports() as no completeness
        # is calculated for dd product.

        # only containers are reported to be consolidated by another engine
        if self.containers:
            self.logger.debug(
                "Sending custom reports to %s of %s %s",
                self.output_rk,
                self.payload.document_class,
                self.containers,
            )

            yield EngineReport(
                self.output_rk,
                [document.meta.id for document in self.containers],
                self.payload.document_class,
                chunk_size=self.container_chunk_size,
            )
