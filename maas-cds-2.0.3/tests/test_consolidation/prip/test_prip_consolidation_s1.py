from unittest.mock import patch

import pytest

import maas_cds.model as model

from maas_cds.engines.reports import (
    ProductConsolidatorEngine,
    PublicationConsolidatorEngine,
)


@pytest.fixture
def prip_product_s1_eta():
    data_dict = {
        "reportName": "https://s1a.prip.copernicus.eu",
        "product_id": "0d97b026-119a-48f1-b654-9f932ba9fcf1",
        "product_name": "S1A_IW_ETA__AXDV_20230831T201111_20230831T201141_050124_06083C_81A7.SAFE.zip",
        "content_length": 89365277,
        "publication_date": "2023-09-21T15:16:38.245Z",
        "start_date": "2023-08-31T20:11:11.583Z",
        "end_date": "2023-08-31T20:11:41.495Z",
        "origin_date": "2023-09-01T02:46:13.852Z",
        "eviction_date": "2023-10-05T03:16:37.966Z",
        "interface_name": "PRIP_S1A_Serco",
        "production_service_type": "PRIP",
        "production_service_name": "S1A-Serco",
        "ingestionTime": "2023-09-21T15:39:06.238Z",
    }
    raw_document = model.PripProduct(**data_dict)
    raw_document.meta.id = "aecc9319b103df919c7fe929b6f28910"
    raw_document.full_clean()
    return raw_document


@patch("maas_cds.model.CdsDatatake.mget_by_ids")
def test_prip_publication_consolidation_s1_eta(mock_mget_by_ids, prip_product_s1_eta):
    datatake_doc = model.CdsDatatake()

    datatake_doc.datatake_id = "395324"
    datatake_doc.absolute_orbit = "50124"
    datatake_doc.instrument_mode = "IW"
    datatake_doc.timeliness = "NTC"

    mock_mget_by_ids.return_value = [datatake_doc]

    engine = PublicationConsolidatorEngine()

    publication = engine.consolidate_from_PripProduct(
        prip_product_s1_eta, model.CdsPublication()
    )

    engine.consolidated_documents = [publication]

    engine.on_post_consolidate()

    publication = engine.consolidated_documents[0]

    publication.full_clean()

    assert publication.to_dict() == {
        "absolute_orbit": "50124",
        "content_length": 89365277,
        "datatake_id": "395324",
        "eviction_date": "2023-10-05T03:16:37.966Z",
        "from_sensing_timeliness": 1796696750000.0,
        "instrument_mode": "IW",
        "key": "aecc9319b103df919c7fe929b6f28910",
        "mission": "S1",
        "name": "S1A_IW_ETA__AXDV_20230831T201111_20230831T201141_050124_06083C_81A7.SAFE.zip",
        "origin_date": "2023-09-01T02:46:13.852Z",
        "polarization": "DV",
        "product_level": "A",
        "product_class": "X",
        "product_type": "IW_ETA__AX",
        "product_uuid": "0d97b026-119a-48f1-b654-9f932ba9fcf1",
        "publication_date": "2023-09-21T15:16:38.245Z",
        "satellite_unit": "S1A",
        "sensing_start_date": "2023-08-31T20:11:11.583Z",
        "sensing_end_date": "2023-08-31T20:11:41.495Z",
        "sensing_duration": 29912000,
        "service_id": "S1A-Serco",
        "service_type": "PRIP",
        "transfer_timeliness": 1773024393000,
        "timeliness": "NTC",
    }


@pytest.fixture
def prip_product_s1_sm_footprint_bug():
    data_dict = {
        "reportName": "https://s1a.prip.copernicus.eu",
        "product_id": "2617797b-06c8-416c-84f1-38c78b7103cf",
        "product_name": "S1A_S6_RAW__0SDV_20231004T082929_20231004T083002_050613_0618E5_2CB0.SAFE.zip",
        "content_length": 1497084027,
        "publication_date": "2023-10-04T09:17:26.647Z",
        "start_date": "2023-10-04T08:29:29.717Z",
        "end_date": "2023-10-04T08:30:02.417Z",
        "origin_date": "2023-10-04T08:57:21.450Z",
        "eviction_date": "2023-10-17T21:17:25.819Z",
        "footprint": "geography'SRID=4326;Polygon((145.5501 17.3358,146.2801 17.4215,145.8977 19.3978,145.159 19.3133,145.5501 17.3358))'",
        "interface_name": "PRIP_S1A_Serco",
        "production_service_type": "PRIP",
        "production_service_name": "S1A-Serco",
        "ingestionTime": "2023-10-04T09:41:22.535Z",
    }
    raw_document = model.PripProduct(**data_dict)
    raw_document.meta.id = "b134306f56054f80a1801bc983fbc238"
    raw_document.full_clean()
    return raw_document


@patch("maas_cds.model.CdsDatatake.mget_by_ids")
def test_prip_publication_consolidation_s1_sm_footprint_bug(
    mock_mget_by_ids, prip_product_s1_sm_footprint_bug
):
    datatake_doc = model.CdsDatatake()

    datatake_doc.datatake_id = "399589"
    datatake_doc.absolute_orbit = "50613"
    datatake_doc.instrument_mode = "SM"
    datatake_doc.timeliness = "NTC"

    mock_mget_by_ids.return_value = [datatake_doc]

    engine = ProductConsolidatorEngine()

    product = engine.consolidate_from_PripProduct(
        prip_product_s1_sm_footprint_bug, model.CdsProduct()
    )

    engine.consolidated_documents = [product]

    engine.on_post_consolidate()

    product = engine.consolidated_documents[0]

    product.full_clean()

    assert product.to_dict() == {
        "absolute_orbit": "50613",
        "datatake_id": "399589",
        "key": "4a19a9cc4b96420de2c15df1d90704a2",
        "instrument_mode": "SM",
        "mission": "S1",
        "name": "S1A_S6_RAW__0SDV_20231004T082929_20231004T083002_050613_0618E5_2CB0.SAFE.zip",
        "polarization": "DV",
        "product_class": "S",
        "product_type": "S6_RAW__0S",
        "product_level": "L0_",
        "satellite_unit": "S1A",
        "sensing_start_date": "2023-10-04T08:29:29.717Z",
        "sensing_end_date": "2023-10-04T08:30:02.417Z",
        "sensing_duration": 32700000,
        "timeliness": "NTC",
        "content_length": 1497084027,
        "prip_id": "2617797b-06c8-416c-84f1-38c78b7103cf",
        "prip_publication_date": "2023-10-04T09:17:26.647Z",
        "prip_service": "PRIP_S1A_Serco",
        "OCN_coverage_percentage": 100.0,
    }
