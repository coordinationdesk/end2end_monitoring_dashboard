"""Tests for LTA Werum consolidation into products and publications"""

import datetime

from unittest.mock import patch

import pytest

import maas_cds.model as model

from opensearchpy import Search

from maas_cds.engines.reports import (
    PublicationConsolidatorEngine,
)

from maas_cds.engines.reports.lta_product import LTAProductConsolidatorEngine


from maas_cds.model.datatake import CdsDatatake


@pytest.fixture
def lta_product_1():
    data_dict = {
        "reportName": "LTA_Werum_20220111T150336_20220112T103044_1000_P103.json",
        "product_id": "9484cbcc-c1d0-48d8-0de6-0104621c7d82",
        "product_name": "S2B_OPER_AUX_PREORB_OPOD_20200511T204859_V20200511T222603_20200512T014727.EOF",
        "content_length": 2519,
        "publication_date": "2022-01-12T07:11:53.994Z",
        "start_date": "2020-05-11T22:26:03.000Z",
        "end_date": "2020-05-12T01:47:27.000Z",
        "origin_date": "2020-05-11T00:00:00.000Z",
        "modification_date": "2022-01-12T07:11:53.994Z",
        "interface_name": "LTA_Werum",
        "production_service_type": "LTA",
        "production_service_name": "Werum",
        "ingestionTime": "2022-02-12T14:25:46.396Z",
    }
    raw_document = model.LtaProduct(**data_dict)
    raw_document.meta.id = "ce44721a4ab1ccaff42b945850019ff7"
    raw_document.full_clean()
    return raw_document


@patch("opensearchpy.Search.execute")
@patch("maas_model.document.Document.search")
def test_lta_werum_product_consolidation(mock_search, mock_execute, lta_product_1):
    "product consolidation test"

    datatake_doc = CdsDatatake()

    datatake_doc.absolute_orbit = "10000"
    datatake_doc.instrument_mode = "IW"
    datatake_doc.timeliness = "NTC"
    datatake_doc.observation_time_start = datetime.datetime(
        2020, 5, 11, 22, 26, 3, 000000, tzinfo=datetime.timezone.utc
    )
    datatake_doc.observation_time_stop = datetime.datetime(
        2020, 5, 12, 1, 47, 27, 000000, tzinfo=datetime.timezone.utc
    )

    mock_search.return_value = Search()
    mock_execute.return_value = [datatake_doc]

    engine = LTAProductConsolidatorEngine()

    cds_product = model.CdsProduct()

    cds_product.sensing_start_date = datetime.datetime(
        2020, 5, 11, 22, 26, 3, 000000, tzinfo=datetime.timezone.utc
    )
    cds_product.sensing_end_date = datetime.datetime(
        2020, 5, 12, 1, 47, 27, 000000, tzinfo=datetime.timezone.utc
    )
    product = engine.consolidate_from_LtaProduct(lta_product_1, cds_product)

    # note that dynamic fields are not serialized by full_clean()
    assert product.to_dict() == {
        "key": "775f0604c418c9a48f229e7b07b66281",
        "mission": "S2",
        "name": "S2B_OPER_AUX_PREORB_OPOD_20200511T204859_V20200511T222603_20200512T014727.EOF",
        "product_level": "AUX",
        "product_type": "AUX_PREORB",
        "satellite_unit": "S2B",
        "site_center": "OPOD",
        "sensing_start_date": "2020-05-11T22:26:03.000Z",
        "sensing_end_date": "2020-05-12T01:47:27.000Z",
        "sensing_duration": 12084000000.0,
        "expected_lta_number": 4,
        "LTA_Werum_is_published": True,
        "LTA_Werum_id": "9484cbcc-c1d0-48d8-0de6-0104621c7d82",
        "datatake_id": "______",
        "LTA_Werum_publication_date": datetime.datetime(
            2022, 1, 12, 7, 11, 53, 994000, tzinfo=datetime.timezone.utc
        ),
        "nb_lta_served": 1,
        "timeliness": "_",
        "content_length": 2519,
    }


@patch("opensearchpy.Search.execute")
@patch("maas_model.document.Document.search")
def test_lta_werum_publication_consolidation(mock_search, mock_execute, lta_product_1):
    """publication consolidation test"""

    datatake_doc = CdsDatatake()

    datatake_doc.absolute_orbit = "10000"
    datatake_doc.instrument_mode = "IW"
    datatake_doc.timeliness = "NTC"

    datatake_doc.observation_time_start = datetime.datetime(
        2020, 5, 11, 22, 26, 3, 000000, tzinfo=datetime.timezone.utc
    )
    datatake_doc.observation_time_stop = datetime.datetime(
        2020, 5, 12, 1, 47, 27, 000000, tzinfo=datetime.timezone.utc
    )

    mock_search.return_value = Search()
    mock_execute.return_value = [datatake_doc]

    cds_publication = model.CdsPublication()

    cds_publication.sensing_start_date = datetime.datetime(
        2020, 5, 11, 22, 26, 3, 000000, tzinfo=datetime.timezone.utc
    )
    cds_publication.sensing_end_date = datetime.datetime(
        2020, 5, 12, 1, 47, 27, 000000, tzinfo=datetime.timezone.utc
    )

    engine = PublicationConsolidatorEngine()

    publication = engine.consolidate_from_LtaProduct(
        lta_product_1, model.CdsPublication()
    )

    assert publication.to_dict() == {
        "key": "ce44721a4ab1ccaff42b945850019ff7",
        "mission": "S2",
        "name": "S2B_OPER_AUX_PREORB_OPOD_20200511T204859_V20200511T222603_20200512T014727.EOF",
        "product_level": "AUX",
        "product_type": "AUX_PREORB",
        "satellite_unit": "S2B",
        "site_center": "OPOD",
        "sensing_start_date": "2020-05-11T22:26:03.000Z",
        "sensing_end_date": "2020-05-12T01:47:27.000Z",
        "sensing_duration": 12084000000.0,
        "content_length": 2519,
        "service_id": "Werum",
        "service_type": "LTA",
        "origin_date": "2020-05-11T00:00:00.000Z",
        "product_uuid": "9484cbcc-c1d0-48d8-0de6-0104621c7d82",
        "publication_date": "2022-01-12T07:11:53.994Z",
        "modification_date": "2022-01-12T07:11:53.994Z",
        "transfer_timeliness": 52816313994000.0,
        "from_sensing_timeliness": 52723466994000.0,
        "timeliness": "_",
        "datatake_id": "______",
    }


@patch("opensearchpy.Search.execute", return_value=[])
def test_action(mock_es, lta_product_1):
    """publication consolidation test"""

    engine = LTAProductConsolidatorEngine()

    product = engine.consolidate_from_LtaProduct(lta_product_1, model.CdsProduct())

    assert engine.get_report_action("created", product) == "new.cds-product-s2"
