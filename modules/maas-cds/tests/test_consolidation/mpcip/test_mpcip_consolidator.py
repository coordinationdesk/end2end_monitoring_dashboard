import pytest

import maas_cds.model as model

from maas_cds.engines.reports import (
    ProductConsolidatorEngine,
    PublicationConsolidatorEngine,
)

import datetime


@pytest.fixture
def mpcip_product():
    data_dict = {
        "reportName": "MPCIP_Acri_gip.json",
        "product_id": "ec4789a8-5ff8-47da-9cab-11c2194d3fcf",
        "product_name": "S2B_OPER_GIP_R2EQOG_MPC__20221114T162000_V20221116T010000_21000101T000000_B12.TGZ",
        "content_length": 345439,
        "publication_date": "2022-12-07T15:02:29.138Z",
        "start_date": "2022-11-16T01:00:00.000Z",
        "end_date": "2100-01-01T00:00:00.000Z",
        "origin_date": "2022-12-07T14:34:31.000Z",
        "eviction_date": "2023-01-07T15:02:29.138Z",
        "interface_name": "MPCIP_Acri",
        "production_service_type": "MPCIP",
        "production_service_name": "Acri",
        "reportFolder": "C:\\Users\\guest2063\\maas\\tmp\\mpcip",
        "ingestionTime": "2023-10-05T08:51:44.969Z",
    }

    raw_document = model.MpcipProduct(**data_dict)
    raw_document.meta.id = "63acb4648cd5d627a45f8593b9e95c4d"
    raw_document.full_clean()
    return raw_document


def test_mpcip_product_consolidation(mpcip_product):
    engine = ProductConsolidatorEngine()
    engine.input_documents = [mpcip_product]
    engine.on_pre_consolidate()

    product = engine.consolidate_from_MpcipProduct(mpcip_product, model.CdsProduct())

    engine.consolidated_documents = [product]

    assert product.to_dict() == {
        "MPCIP_Acri_id": "ec4789a8-5ff8-47da-9cab-11c2194d3fcf",
        "nb_mpcip_served": 1,
        "mission": "S2",
        "MPCIP_Acri_is_published": True,
        "MPCIP_Acri_publication_date": datetime.datetime(
            2022, 12, 7, 15, 2, 29, 138000, tzinfo=datetime.timezone.utc
        ),
        "key": "6347db6fa0d7bc655dfcdb058db13883",
        "product_level": "AUX",
        "site_center": "MPC_",
        "datatake_id": "______",
        "name": "S2B_OPER_GIP_R2EQOG_MPC__20221114T162000_V20221116T010000_21000101T000000_B12.TGZ",
        "product_type": "GIP_R2EQOG",
        "satellite_unit": "S2B",
        "sensing_start_date": "2022-11-16T01:00:00.000Z",
        "sensing_end_date": "2100-01-01T00:00:00.000Z",
        "sensing_duration": 2433884400000000.0,
        "timeliness": "_",
        "content_length": 345439,
    }


def test_mpcip_publication_consolidation(mpcip_product):
    engine = PublicationConsolidatorEngine()
    engine.input_documents = [mpcip_product]
    engine.on_pre_consolidate()

    publication = engine.consolidate_from_MpcipProduct(
        mpcip_product, model.CdsPublication()
    )

    assert publication.to_dict() == {
        "key": "63acb4648cd5d627a45f8593b9e95c4d",
        "mission": "S2",
        "name": "S2B_OPER_GIP_R2EQOG_MPC__20221114T162000_V20221116T010000_21000101T000000_B12.TGZ",
        "product_type": "GIP_R2EQOG",
        "product_level": "AUX",
        "satellite_unit": "S2B",
        "site_center": "MPC_",
        "sensing_start_date": "2022-11-16T01:00:00.000Z",
        "sensing_end_date": "2100-01-01T00:00:00.000Z",
        "sensing_duration": 2433884400000000.0,
        "timeliness": "_",
        "content_length": 345439,
        "service_id": "Acri",
        "datatake_id": "______",
        "service_type": "MPCIP",
        "product_uuid": "ec4789a8-5ff8-47da-9cab-11c2194d3fcf",
        "eviction_date": "2023-01-07T15:02:29.138Z",
        "origin_date": "2022-12-07T14:34:31.000Z",
        "publication_date": "2022-12-07T15:02:29.138Z",
        "transfer_timeliness": 1678138000.0,
        "from_sensing_timeliness": 2432019450862000.0,
    }
