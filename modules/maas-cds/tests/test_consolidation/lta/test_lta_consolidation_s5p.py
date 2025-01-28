import logging
from maas_model import datestr_to_utc_datetime

import pytest


import maas_cds.model as model

from maas_cds.engines.reports import (
    PublicationConsolidatorEngine,
)

from maas_cds.engines.reports.lta_product import LTAProductConsolidatorEngine


@pytest.fixture
def lta_product_1():
    data_dict = {
        "reportName": "LTA_S5P",
        "product_id": "d30d0187-5de5-4031-a160-1bac13e19689",
        "product_name": "S5P_OFFL_L1B_IR_SIR_20171115T103323_20171115T121452_00469_01_001200_20171115T143947.nc",
        "content_length": 6486596,
        "publication_date": "2021-07-07T12:50:45.77Z",
        "start_date": "2017-11-15T10:32:23Z",
        "end_date": "2017-11-15T12:15:52Z",
        "eviction_date": "2022-03-31T09:36:06.71Z",
        "interface_name": "LTA_S5P_DLR",
        "production_service_type": "LTA",
        "production_service_name": "S5P_DLR",
        "ingestionTime": "2022-02-11T14:45:45.713Z",
    }
    raw_document = model.LtaProduct(**data_dict)
    raw_document.meta.id = "5b65d059c9dac47b8bdbb6f6fdddecbe"
    raw_document.full_clean()
    return raw_document


def test_s5p_extracting_consolidation_publication(lta_product_1):
    engine = PublicationConsolidatorEngine()

    publication = engine.consolidate_from_LtaProduct(
        lta_product_1, model.CdsPublication()
    )

    publication.full_clean()

    assert publication.to_dict() == {
        "absolute_orbit": "469",
        "key": "5b65d059c9dac47b8bdbb6f6fdddecbe",
        "mission": "S5",
        "name": "S5P_OFFL_L1B_IR_SIR_20171115T103323_20171115T121452_00469_01_001200_20171115T143947.nc",
        "product_level": "L1_",
        "product_type": "OFFL_L1B_IR_SIR",
        "satellite_unit": "S5P",
        "sensing_start_date": "2017-11-15T10:32:23.000Z",
        "sensing_end_date": "2017-11-15T12:15:52.000Z",
        "sensing_duration": 6209000000,
        "timeliness": "OFFL",
        "processor_version": "001200",
        "collection_number": "01",
        "content_length": 6486596,
        "eviction_date": "2022-03-31T09:36:06.710Z",
        "from_sensing_timeliness": 114914093770000,
        "product_uuid": "d30d0187-5de5-4031-a160-1bac13e19689",
        "publication_date": "2021-07-07T12:50:45.770Z",
        "service_id": "S5P_DLR",
        "service_type": "LTA",
        "datatake_id": "S5P-00469",
    }


def test_lta_product_consolidation(lta_product_1):
    engine = LTAProductConsolidatorEngine()

    product = engine.consolidate_from_LtaProduct(lta_product_1, model.CdsProduct())

    product.full_clean()

    assert product.to_dict() == {
        "absolute_orbit": "469",
        "key": "59f5375b291bda5643dbe95f1f1b8890",
        "mission": "S5",
        "name": "S5P_OFFL_L1B_IR_SIR_20171115T103323_20171115T121452_00469_01_001200_20171115T143947.nc",
        "product_level": "L1_",
        "product_type": "OFFL_L1B_IR_SIR",
        "satellite_unit": "S5P",
        "sensing_start_date": "2017-11-15T10:32:23.000Z",
        "sensing_end_date": "2017-11-15T12:15:52.000Z",
        "content_length": 6486596,
        "sensing_duration": 6209000000,
        "timeliness": "OFFL",
        "processor_version": "001200",
        "collection_number": "01",
        "LTA_S5P_DLR_id": "d30d0187-5de5-4031-a160-1bac13e19689",
        "LTA_S5P_DLR_is_published": True,
        "LTA_S5P_DLR_publication_date": datestr_to_utc_datetime(
            "2021-07-07T12:50:45.770Z"
        ),
        "expected_lta_number": 4,
        "nb_lta_served": 1,
        "datatake_id": "S5P-00469",
    }


def test_lta_l5p_product_consolidation(s5_lta_product_l0):
    engine = LTAProductConsolidatorEngine()
    consolidated = model.CdsProduct()

    # Check that the output of the consolidation will have this value incremented by 1
    consolidated.nb_lta_served = 4

    product = engine.consolidate_from_LtaProduct(s5_lta_product_l0, consolidated)

    product.full_clean()

    assert product.to_dict() == {
        "absolute_orbit": "24429",
        "key": "1d0138fbb1de98d3462fc344904b26a5",
        "mission": "S5",
        "LTA_S5P_DLR_id": "501e0178-5a04-4ada-8beb-d04094bebb24",
        "name": "S5P_OPER_L0__SAT_A__20220701T051131_20220701T053148_24429_05.RAW",
        "product_type": "OPER_L0__SAT_A_",
        "product_level": "L0_",
        "satellite_unit": "S5P",
        "collection_number": "05",
        "sensing_start_date": "2022-07-01T05:11:31.000Z",
        "sensing_end_date": "2022-07-01T05:31:48.000Z",
        "sensing_duration": 1217000000,
        "content_length": 384888,
        "timeliness": "OPER",
        "expected_lta_number": 4,
        "LTA_S5P_DLR_is_published": True,
        "LTA_S5P_DLR_publication_date": datestr_to_utc_datetime(
            "2022-07-01T13:41:03.872Z"
        ),
        "nb_lta_served": 5,
        "datatake_id": "S5P-24429",
    }


def test_lta_shall_report_function(s5_lta_product_l0):
    engine = LTAProductConsolidatorEngine()
    "Verify shall_report return True only if product_level = L0_ and mission = S5"
    prod = s5_lta_product_l0
    prod.product_level = "L0_"
    prod.mission = "S5"
    assert engine.shall_report(prod)
    prod.product_level = "_L0_"
    assert not engine.shall_report(prod)
    prod.product_level = "L0_"
    for x in ("S1", "S2", "S3", "S10"):
        prod.mission = x
        assert not engine.shall_report(prod)


def test_lta_already_registered_check(s5_lta_product_l0, caplog):
    "Make sure the engine is able to distinguish already registered documents"
    engine = LTAProductConsolidatorEngine()
    prod = s5_lta_product_l0
    consolidated = model.CdsProduct()
    consolidated[f"{prod.interface_name}_is_published"] = True

    with caplog.at_level(logging.WARNING):
        out_consolidated = engine.consolidate_from_LtaProduct(prod, consolidated)
        assert out_consolidated.to_dict() == consolidated.to_dict()
    assert "product is already register in cds-product" in caplog.records[0].message
