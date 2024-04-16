"""Publication consolidation"""

import dateutil

from maas_cds.engines.reports.base import BaseProductConsolidatorEngine
from maas_cds.engines.reports.anomaly_impact import (
    AnomalyImpactMixinEngine,
    anomaly_link,
)

from maas_cds import model

from maas_cds.lib.dateutils import get_microseconds_delta


class PublicationConsolidatorEngine(
    AnomalyImpactMixinEngine, BaseProductConsolidatorEngine
):
    """Consolidate publications from raw products"""

    ENGINE_ID = "CONSOLIDATE_PUBLICATION"

    CONSOLIDATED_MODEL = model.CdsPublication

    MAX_SEARCH_INDICES = 10

    def get_consolidated_id(self, raw_document) -> str:
        """Get publication identifier that is the same as the raw document which
        is the md5 sum of interface name and product name

        Args:
            raw_document: raw document

        Returns:
            str: publication identifier
        """
        return raw_document.meta.id

    def get_consolidated_indices(self) -> list[str]:
        """
        Find the publication indices based on raw document start date if sensing makes
        sens or publication_date by default.

        It reverse the logic from the dynamic partitionning for publication only

        Returns:
             list[str]: list of indices
        """
        # build the set of partition signatures
        partitions = {
            f"{partition_date.year:04d}-{partition_date.month:02d}"
            for partition_date in [
                (
                    raw_document.start_date
                    if "product_level" in data_dict
                    and self.CONSOLIDATED_MODEL.product_level_use_sensing_partitionned(
                        data_dict["product_level"]
                    )
                    else raw_document.publication_date
                )
                for raw_document, data_dict in zip(
                    self.input_documents,
                    [
                        self.session.get("all_data_dict").get(doc.product_name)
                        for doc in self.input_documents
                    ],
                )
            ]
            if ((partition_date >= self.min_doi) if self.min_doi else True)
        }

        if len(partitions) > self.MAX_SEARCH_INDICES:
            self.logger.debug(
                "Too many partition to search (%d): fallback to alias", len(partitions)
            )
            return

        indices = [
            f"{model.CdsPublication.Index.name}-{partition}" for partition in partitions
        ]

        # just for the style
        indices.sort()

        self.logger.debug(
            "Partitions to search for consolidated publications: %s", indices
        )

        return indices

    def fill_common_attributes(self, raw_document, document, **kwargs) -> dict:
        """set all common attributes"""
        data_dict = super().fill_common_attributes(raw_document, document, **kwargs)
        document.service_id = raw_document.production_service_name
        document.service_type = raw_document.production_service_type
        document.product_uuid = raw_document.product_id
        document.tile_number = data_dict.get("tile_number", document.tile_number)
        return data_dict

    def calculate_sensing_timeliness(self, document: model.CdsPublication) -> int:
        """Calculate from sensing timeliness

        Args:
            document (model.CdsPublication): publication

        Returns:
            int: timeliness in microseconds
        """

        if not (document.publication_date and document.sensing_end_date):
            self.logger.warning(
                "publication_date or sensing_end_date is None:"
                "cannot calculate from_sensing_timeliness for publication key= %s",
                document.key,
            )
            return None

        return get_microseconds_delta(
            document.sensing_end_date, document.publication_date
        )

    def calculate_transfer_timeliness(self, document: model.CdsPublication) -> int:
        """Calculate transfer timeliness

        Args:
            document (model.CdsPublication): publication

        Returns:
            int: timeliness in microseconds
        """

        if not (document.origin_date and document.publication_date):
            self.logger.warning(
                "origin_date or publication_date is None:"
                "cannot calculate transfer_timeliness for publication key= %s",
                document.key,
            )
            return None

        return get_microseconds_delta(document.origin_date, document.publication_date)

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    @anomaly_link
    def consolidate_from_LtaProduct(
        self, raw_document: model.LtaProduct, document: model.CdsPublication
    ) -> model.CdsPublication:
        "consolidated products from lta ingestion"
        self.fill_common_attributes(
            raw_document, document, start_key="sensing_start_date"
        )

        document.eviction_date = raw_document.eviction_date

        document.modification_date = raw_document.modification_date

        document.origin_date = raw_document.origin_date

        document.publication_date = raw_document.publication_date

        document.transfer_timeliness = self.calculate_transfer_timeliness(document)

        document.from_sensing_timeliness = self.calculate_sensing_timeliness(document)

        return document

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    @anomaly_link
    def consolidate_from_PripProduct(
        self, raw_document: model.PripProduct, document: model.CdsProduct
    ) -> model.CdsProduct:
        "consolidated products from prip ingestion"
        self.fill_common_attributes(raw_document, document)

        document.publication_date = raw_document.publication_date

        document.eviction_date = raw_document.eviction_date

        document.origin_date = raw_document.origin_date

        document.from_sensing_timeliness = self.calculate_sensing_timeliness(document)

        document.transfer_timeliness = self.calculate_transfer_timeliness(document)

        return document

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    @anomaly_link
    def consolidate_from_DdProduct(
        self, raw_document: model.DdProduct, document: model.CdsPublication
    ) -> model.CdsPublication:
        "consolidated products from dd ingestion for cds-publication"

        data_dict = self.fill_common_attributes(raw_document, document)

        document.modification_date = raw_document.modification_date

        document.publication_date = raw_document.publication_date

        document.from_sensing_timeliness = self.calculate_sensing_timeliness(document)

        # FIXME  publication_date and origin_date are not consolidated for DD !!!
        document.transfer_timeliness = self.calculate_transfer_timeliness(document)

        # container case: consolidate product_discriminator_date to ease content
        # attachement
        document.product_discriminator_date = data_dict.get(
            "product_discriminator_date", document.product_discriminator_date
        )

        return document

        # consolidate_from_ModelClass

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    @anomaly_link
    def consolidate_from_DasProduct(
        self, raw_document: model.DasProduct, document: model.CdsPublication
    ) -> model.CdsPublication:
        "consolidated products from das ingestion for cds-publication"

        data_dict = self.fill_common_attributes(raw_document, document)

        document.modification_date = raw_document.modification_date

        document.publication_date = raw_document.publication_date

        # for das dd_product there is no "creation_date" publication is used
        document.publication_date = raw_document.publication_date

        document.from_sensing_timeliness = self.calculate_sensing_timeliness(document)

        # FIXME  publication_date and origin_date are not consolidated for DD !!!
        document.transfer_timeliness = self.calculate_transfer_timeliness(document)

        # container case: consolidate product_discriminator_date to ease content
        # attachement
        document.product_discriminator_date = data_dict.get(
            "product_discriminator_date", document.product_discriminator_date
        )

        return document

    # pylint: disable=C0103
    def consolidate_from_CreodiasProduct(
        self, raw_document: model.CreodiasProduct, document: model.CdsPublication
    ) -> model.CdsPublication:
        "consolidated products from Creodias ingestion for cds-publication"

        document = self.consolidate_from_DasProduct(raw_document, document)

        return document

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    @anomaly_link
    def consolidate_from_DdArchive(
        self, raw_document: model.DdArchive, document: model.CdsPublication
    ) -> model.CdsPublication:
        "consolidated products from dd archive for cds-publication"
        super().fill_common_attributes(raw_document, document)

        document.content_length = raw_document.content_length

        document.service_id = "DHUS"

        document.service_type = "DD-ARCHIVE"

        document.product_uuid = raw_document.product_id

        document.publication_date = raw_document.ingestion_date

        return document

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    @anomaly_link
    def consolidate_from_AuxipProduct(
        self, raw_document: model.AuxipProduct, document: model.CdsPublication
    ) -> model.CdsPublication:
        "consolidated products from auxip ingestion"
        self.fill_common_attributes(raw_document, document)

        document.eviction_date = raw_document.eviction_date

        document.origin_date = raw_document.origin_date

        document.product_uuid = raw_document.product_id

        document.publication_date = raw_document.publication_date

        document.transfer_timeliness = self.calculate_transfer_timeliness(document)

        document.from_sensing_timeliness = self.calculate_sensing_timeliness(document)

        return document

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    @anomaly_link
    def consolidate_from_MpcipProduct(
        self, raw_document: model.MpcipProduct, document: model.CdsPublication
    ) -> model.CdsPublication:
        "consolidated products from Mpcip ingestion"
        self.fill_common_attributes(raw_document, document)

        document.eviction_date = raw_document.eviction_date

        document.origin_date = raw_document.origin_date

        document.product_uuid = raw_document.product_id

        document.publication_date = raw_document.publication_date

        document.transfer_timeliness = self.calculate_transfer_timeliness(document)

        document.from_sensing_timeliness = self.calculate_sensing_timeliness(document)

        return document
