from unittest.mock import patch

import pytest

import maas_cds.model as model


from maas_cds.engines.reports.dd_product import DDProductConsolidatorEngine
from maas_cds.engines.reports import PublicationConsolidatorEngine


def test_dd_archive_product_consolidation_publication(
    s5_dd_archive_product,
):
    engine = PublicationConsolidatorEngine()

    publication = engine.consolidate_from_DdArchive(
        s5_dd_archive_product, model.CdsPublication()
    )

    assert publication.partition_index_name == "cds-publication-2021-12"


def test_dd_archive_product_consolidation_product(s5_dd_archive_product, dd_attrs):
    engine = DDProductConsolidatorEngine(dd_attrs=dd_attrs)

    product = engine.consolidate_from_DdArchive(
        s5_dd_archive_product, model.CdsProduct()
    )

    assert product.partition_index_name == "cds-product-2021-12"
