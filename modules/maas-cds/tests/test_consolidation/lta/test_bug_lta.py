from unittest.mock import patch

import pytest
import datetime
import maas_cds.model as model

from maas_cds.engines.reports import (
    PublicationConsolidatorEngine,
    LTAProductConsolidatorEngine,
)


@pytest.fixture
def prip_product_wont_consolidate():
    data_dict = {
        "reportName": "https://lta.cloudferro.copernicus.eu",
        "product_id": "2c08a752-c1b3-4a58-80e0-afb5c9f1ff7c",
        "product_name": "S1A_OPER_AMV_ERRMAT_MPC__20201222T040009_V20000101T000000_20201221T232325.EOF.zip",
        "content_length": 11487,
        "publication_date": "2020-12-22T06:12:39.839Z",
        "origin_date": "2020-12-22T04:24:23.058Z",
        "modification_date": "2020-12-22T06:12:39.839Z",
        "eviction_date": "9999-12-31T23:59:59.999Z",
        "interface_name": "LTA_CloudFerro",
        "production_service_type": "LTA",
        "production_service_name": "CloudFerro",
        "ingestionTime": "2024-01-18T22:53:35.784Z",
    }
    raw_document = model.PripProduct(**data_dict)
    raw_document.meta.id = "7108d1c9f43d35118a5e0db6861bd73b"
    raw_document.full_clean()
    return raw_document


@patch("maas_cds.model.CdsDatatake.mget_by_ids")
def test_prip_publication_consolidation_s1_bug_wont_consolidate(
    mock_mget_by_ids, prip_product_wont_consolidate
):
    engine = PublicationConsolidatorEngine()

    publication = engine.consolidate_from_PripProduct(
        prip_product_wont_consolidate, model.CdsPublication()
    )

    assert publication is not None

    assert publication._PARTITION_FIELD is not None

    assert publication.has_partition_field_value is True

    assert publication.partition_index_name == "cds-publication-2020-12"

    assert publication.to_dict() == {
        "key": "7108d1c9f43d35118a5e0db6861bd73b",
        "mission": "S1",
        "name": "S1A_OPER_AMV_ERRMAT_MPC__20201222T040009_V20000101T000000_20201221T232325.EOF.zip",
        "product_type": "AMV_ERRMAT",
        "product_level": "AUX",
        "satellite_unit": "S1A",
        "timeliness": "_",
        "datatake_id": "______",
        "content_length": 11487,
        "service_id": "CloudFerro",
        "service_type": "LTA",
        "product_uuid": "2c08a752-c1b3-4a58-80e0-afb5c9f1ff7c",
        "publication_date": "2020-12-22T06:12:39.839Z",
        "eviction_date": "9999-12-31T23:59:59.999Z",
        "origin_date": "2020-12-22T04:24:23.058Z",
        "transfer_timeliness": 6496781000.0,
    }


@patch("maas_cds.model.CdsDatatake.mget_by_ids")
def test_prip_product_consolidation_s1_bug_wont_consolidate(
    mock_mget_by_ids, prip_product_wont_consolidate
):
    engine = LTAProductConsolidatorEngine()

    product = engine.consolidate_from_LtaProduct(
        prip_product_wont_consolidate, model.CdsProduct()
    )

    assert product is not None

    assert product._PARTITION_FIELD is not None

    assert product.has_partition_field_value is True

    assert product.partition_index_name == "cds-product-2020-12"

    assert product.to_dict() == {
        "datatake_id": "______",
        "key": "0f7e9022f4447a5c2fff8c9a037d16d9",
        "mission": "S1",
        "name": "S1A_OPER_AMV_ERRMAT_MPC__20201222T040009_V20000101T000000_20201221T232325.EOF.zip",
        "product_type": "AMV_ERRMAT",
        "product_level": "AUX",
        "satellite_unit": "S1A",
        "timeliness": "_",
        "content_length": 11487,
        "LTA_CloudFerro_is_published": True,
        "LTA_CloudFerro_publication_date": datetime.datetime(
            2020, 12, 22, 6, 12, 39, 839000, tzinfo=datetime.timezone.utc
        ),
        "LTA_CloudFerro_id": "2c08a752-c1b3-4a58-80e0-afb5c9f1ff7c",
        "nb_lta_served": 1,
        "expected_lta_number": 4,
    }
