"""Product consolidation"""

import hashlib

import geomet.wkt
from opensearchpy.helpers.utils import AttrDict

from maas_engine.engine.base import EngineReport

from maas_cds.model.s2_tilpar_tiles import S2Tiles

from maas_cds.engines.reports.base import BaseProductConsolidatorEngine
from maas_cds.engines.reports.mission_mixin import MissionMixinEngine
from maas_cds.engines.reports.anomaly_impact import (
    AnomalyImpactMixinEngine,
    anomaly_link,
)

from maas_cds.lib.geo_mask_utils import GeoMaskUtils
from maas_cds.lib.parsing_name.utils import remove_extension_from_product_name
from maas_cds import model


class ProductConsolidatorEngine(
    MissionMixinEngine,
    AnomalyImpactMixinEngine,
    BaseProductConsolidatorEngine,
):
    """Consolidate raw products to CdsProduct"""

    ENGINE_ID = "CONSOLIDATE_PRODUCT"

    CONSOLIDATED_MODEL = model.CdsProduct

    def __init__(
        self,
        args=None,
        send_reports=True,
        min_doi=None,
        chunk_size=0,
        container_rk="new.container-products",
        container_chunk_size=0,
        dd_attrs=None,
    ):
        super().__init__(
            args, send_reports=send_reports, min_doi=min_doi, chunk_size=chunk_size
        )

        self.geo_mask_utils = GeoMaskUtils()

        self.container_rk = container_rk

        self.container_chunk_size = container_chunk_size

        self.container_related_products = []

        self.hktm_related_products = []

        self.custom_reports = {}

        self.dd_attrs = dd_attrs or {}

    def get_consolidated_id(self, raw_document) -> str:
        """Generate consolidated product identifier: md5 sum of the product name

        Args:
            raw_document: raw document

        Returns:
            str: product identifier
        """

        product_name_without_extension = remove_extension_from_product_name(
            raw_document.product_name
        )

        md5 = hashlib.md5(product_name_without_extension.encode())
        return md5.hexdigest()

    def fill_common_attributes(
        self,
        raw_document,
        document,
        data_dict=None,
        start_key="start_date",
        end_key="end_date",
        fill_name=True,
    ) -> dict:
        """[summary]

        Args:
            raw_document (MAASDocument): incoming document
            document (MAASDocument): document to consolidated
            data_dict (dict, optional): [description]. Defaults to None.
            start_key (str, optional): [description]. Defaults to "start_date".
            end_key (str, optional): [description]. Defaults to "end_date".

        Returns:
            dict: orginal data_dict enriched by the method
        """

        new_data_dict = super().fill_common_attributes(
            raw_document, document, data_dict, start_key, end_key, fill_name
        )

        self.consolidate_service_information(raw_document, document)

        # S2 Specific
        document.detector_id = new_data_dict.get("detector_id", None)
        document.tile_number = new_data_dict.get("tile_number", None)

        return new_data_dict

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    @anomaly_link
    def consolidate_from_PripProduct(
        self, raw_document: model.PripProduct, document: model.CdsProduct
    ) -> model.CdsProduct:
        """Consolidate a CdsProduct from a PripProduct

        Args:
            raw_document (model.PripProduct): raw prip document
            document (model.CdsProduct): target document

        Returns:
            model.CdsProduct: consolidated document
        """
        data_dict = self.fill_common_attributes(raw_document, document)

        # Need to check the use of this before removing
        document.prip_id = raw_document.product_id

        document.prip_publication_date = raw_document.publication_date

        document.prip_service = raw_document.interface_name
        #

        if document.mission == "S2" and document.product_type == "PRD_HKTM__":
            self.hktm_related_products.append(document)

        if (
            document.mission == "S2"
            and document.product_type in model.CdsProductS2.PRODUCT_TYPES_WITH_TILES
            and raw_document.footprint
        ):
            footprint = None
            # get footprint has geojson heithe source is wkt or geojson

            if isinstance(raw_document.footprint, AttrDict):
                # GeoShape database convertion
                footprint = raw_document.footprint.to_dict()

            elif isinstance(raw_document.footprint, dict):
                # Geojson noconvertion
                footprint = raw_document.footprint

            elif isinstance(raw_document.footprint, str):
                # Convert WKT footprint to geojson
                footprint = geomet.wkt.loads(
                    raw_document.footprint.replace("geography'", "").upper()
                )
            else:
                self.logger.warning(
                    "[FOOTPRINT] - Unhandle footprint format  : %s",
                    raw_document.footprint,
                )
            if footprint:
                # Store expected tiles
                document.expected_tiles = S2Tiles.intersection(footprint)
                self.logger.debug(
                    "Adding expected tiles to %s: %s (%s)",
                    document,
                    document.expected_tiles,
                    footprint,
                )
        if (
            document.mission == "S2"
            and document.tile_number
            and document.product_type in model.DdProduct.S2_CONTAINED_TYPES
        ):
            document.product_discriminator_date = data_dict["creation_date"]

            if (
                self.min_doi is None
                or document.product_discriminator_date >= self.min_doi
            ):
                # store S2 products that need later container attachement

                # store ref for later notification on a dedicated queue
                self.container_related_products.append(document)

        if raw_document.footprint and document.mission == "S1":
            instrument_mode = document.instrument_mode
            if instrument_mode in ["S1", "S2", "S3", "S4", "S5", "S6"]:
                # SM product type will be applied post fill_from_datatake
                instrument_mode = "SM"

            # Add intersect coverage
            result_dict = self.geo_mask_utils.coverage_over_specific_area_s1(
                instrument_mode,
                raw_document.footprint,
                raw_document.start_date,
            )

            self.logger.debug(
                "[%s] - Evaluate intersection masks ( %s ) - %s",
                raw_document.product_name,
                document.instrument_mode,
                result_dict,
            )

            for key, value in result_dict.items():
                setattr(document, key, value)

        # calculate all dd service timeliness on prip reception
        for known_dd_service in self.dd_attrs:
            document.calculate_dd_timeliness(known_dd_service, self.dd_attrs)

        return document

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    @anomaly_link
    def consolidate_from_DdArchive(
        self, raw_document: model.DdArchive, document: model.CdsProduct
    ) -> model.CdsProduct:
        """Consolidate a CdsProduct from a DdArchive

        Args:
            raw_document (model.DdArchive): raw dd-archive document
            document (model.CdsProduct): target document

        Returns:
            model.CdsProduct: consolidated document
        """

        # Hummm we forgot to setup the interface_name with a lambda during the collect
        raw_document.interface_name = "DD_DHUS-ARCHIVE"

        self.fill_common_attributes(raw_document, document)

        # Need to check the use of this before removing
        document.ddip_publication_date = raw_document.ingestion_date
        #

        return document

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    @anomaly_link
    def consolidate_from_AuxipProduct(
        self, raw_document: model.AuxipProduct, document: model.CdsProduct
    ) -> model.CdsProduct:
        """Consolidate a CdsProduct from a AuxipProduct

        Args:
            raw_document (model.AuxipProduct): raw prip document
            document (model.CdsProduct): target document

        Returns:
            model.CdsProduct: consolidated document
        """
        self.fill_common_attributes(raw_document, document)

        # Need to check the use of this before removing
        document.auxip_id = raw_document.product_id

        document.auxip_publication_date = raw_document.publication_date
        #

        return document

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    @anomaly_link
    def consolidate_from_MpcipProduct(
        self, raw_document: model.MpcipProduct, document: model.CdsProduct
    ) -> model.CdsProduct:
        """Consolidate a CdsProduct from a MpcipProduct

        Args:
            raw_document (model.MpcipProduct): raw prip document
            document (model.CdsProduct): target document

        Returns:
            model.CdsProduct: consolidated document
        """
        self.fill_common_attributes(raw_document, document)

        return document

    def consolidate_service_information(self, raw_document, document):
        attr_tuple_mapping = [
            (f"{raw_document.interface_name}_is_published", "true", True),
            (
                f"{raw_document.interface_name}_publication_date",
                "publication_date",
                None,
            ),
            (f"{raw_document.interface_name}_id", "product_id", "MISSING"),
        ]

        # set dynamic attributes
        if not hasattr(document, attr_tuple_mapping[0][0]):
            for attr_name, reference, missing_value in attr_tuple_mapping:
                setattr(
                    document,
                    attr_name,
                    getattr(raw_document, reference, missing_value),
                )

            service_name = raw_document.interface_name.split("_")[0].lower()
            current_service_field_name = f"nb_{service_name}_served"
            current_service_number = (
                getattr(document, current_service_field_name, 0) or 0
            )
            setattr(document, current_service_field_name, current_service_number + 1)

        else:
            self.logger.warning(
                "This product is already register in cds-product %s from %s (id: %s)",
                raw_document.product_name,
                raw_document.interface_name,
                raw_document.meta.id,
            )

    def _generate_reports(self):
        """Override to additionnaly report product attachement to container


        Yields:
            EngineReport: report
        """
        # yield product reports to calculate completeness
        yield from super()._generate_reports()

        if self.hktm_related_products:
            self.logger.debug(
                "Sending custom reports to %s of %s %s instances",
                "update.hktm-products",
                len(
                    self.hktm_related_products,
                ),
                "CdsProductS2",
            )

            yield EngineReport(
                "update.hktm-products",
                [document.meta.id for document in self.hktm_related_products],
                "CdsProductS2",
                document_indices=self.get_index_names(self.hktm_related_products),
                chunk_size=self.container_chunk_size,
            )

        # yield reports for later container attachement. Only apply for S2
        if self.container_related_products:
            self.logger.debug(
                "Sending custom reports to %s of %s %s instances",
                self.container_rk,
                len(
                    self.container_related_products,
                ),
                "CdsProductS2",
            )

            yield EngineReport(
                self.container_rk,
                [document.meta.id for document in self.container_related_products],
                "CdsProductS2",
                document_indices=self.get_index_names(self.container_related_products),
                chunk_size=self.container_chunk_size,
            )
