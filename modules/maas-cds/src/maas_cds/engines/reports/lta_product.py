"""LTA Product consolidation"""

from maas_cds.engines.reports.product import ProductConsolidatorEngine
from maas_cds.engines.reports.anomaly_impact import anomaly_link

from maas_cds import model


class LTAProductConsolidatorEngine(ProductConsolidatorEngine):
    """Consolidate raw products to CdsProduct"""

    ENGINE_ID = "CONSOLIDATE_LTA_PRODUCT"

    CONSOLIDATED_MODEL = model.CdsProduct

    def __init__(
        self,
        args=None,
        send_reports=True,
        min_doi=None,
        expected_lta_number=4,
    ):
        super().__init__(
            args,
            send_reports=send_reports,
            min_doi=min_doi,
        )

        # TODO this must be based on mission
        self.expected_lta_number = expected_lta_number

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    @anomaly_link
    def consolidate_from_LtaProduct(
        self, raw_document: model.LtaProduct, document: model.CdsProduct
    ) -> model.CdsProduct:
        """Consolidated a LtaProduct from a raw lta product

        Args:
            raw_document (model.LtaProduct): raw-document product from the lta
            document (model.CdsProduct): cds product document enriched by the raw document

        Returns:
            model.CdsProduct: cds-product document consolidated
        """

        self.fill_common_attributes(
            raw_document, document, start_key="sensing_start_date"
        )

        document.expected_lta_number = self.expected_lta_number

        return document

    def shall_report(self, document: model.CdsProduct) -> bool:
        """override to allow reporting on S5 mission

        Args:
            document (document:model.CdsProduct): consolidated product

        Returns:
            bool: True if product satisfies S5 condition
        """
        # TODO add product type clause !
        return document.product_level == "L0_" and document.mission == "S5"
