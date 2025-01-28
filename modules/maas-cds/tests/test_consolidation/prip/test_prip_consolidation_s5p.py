from unittest.mock import patch

import pytest
import datetime
import maas_cds.model as model


from maas_cds.engines.reports import (
    ProductConsolidatorEngine,
    PublicationConsolidatorEngine,
)


@pytest.fixture
def prip_product_1():
    data_dict = {
        "reportName": "PRIP_S5P",
        "product_id": "d30d0187-5de5-4031-a160-1bac13e19689",
        "product_name": "S5P_OFFL_L1B_IR_SIR_20171115T103323_20171115T121452_00469_01_001200_20171115T143947.nc",
        "content_length": 6486596,
        "publication_date": "2021-07-07T12:50:45.77Z",
        "start_date": "2017-11-15T10:32:23Z",
        "end_date": "2017-11-15T12:15:52Z",
        "eviction_date": "2022-03-31T09:36:06.71Z",
        "interface_name": "PRIP_S5P_DLR",
        "production_service_type": "PRIP",
        "production_service_name": "S5P_DLR",
        "ingestionTime": "2022-02-11T14:45:45.713Z",
    }
    raw_document = model.PripProduct(**data_dict)
    raw_document.meta.id = "5b65d059c9dac47b8bdbb6f6fdddecbe"
    raw_document.full_clean()
    return raw_document


@pytest.fixture
def prip_product_2():
    data_dict = {
        "reportName": "https://s5p-oda-prip.eoc.dlr.de/proseo/prip",
        "product_id": "8d69ee20-90df-4827-8a15-3269ddd495c1",
        "product_name": "NISE_SSMISF18_20230130.HDFEOS",
        "content_length": 2189155,
        "publication_date": "2023-01-31T05:20:52.307Z",
        "start_date": "2023-01-30T00:00:00.000Z",
        "end_date": "2023-01-31T00:00:00.000Z",
        "origin_date": "1970-01-01T00:00:00.000Z",
        "eviction_date": "9999-12-31T23:59:59.999Z",
        "interface_name": "PRIP_S5P_DLR",
        "production_service_type": "PRIP",
        "production_service_name": "S5P_DLR",
        "ingestionTime": "2023-01-31T05:47:25.396Z",
    }
    raw_document = model.PripProduct(**data_dict)
    raw_document.meta.id = "bac271391449a1a6e76534e73f481eb7"
    raw_document.full_clean()
    return raw_document


def test_s5p_extracting_consolidation_publication(prip_product_1):
    engine = PublicationConsolidatorEngine()

    engine.input_documents = [prip_product_1]

    engine.on_pre_consolidate()

    publication = engine.consolidate_from_PripProduct(
        prip_product_1, model.CdsPublication()
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
        "service_type": "PRIP",
        "datatake_id": "S5P-00469",
    }


def test_prip_product_consolidation(prip_product_1, dd_attrs):
    engine = ProductConsolidatorEngine(dd_attrs=dd_attrs)

    engine.input_documents = [prip_product_1]

    engine.on_pre_consolidate()

    product = engine.consolidate_from_PripProduct(prip_product_1, model.CdsProduct())

    product.full_clean()

    assert product.to_dict() == {
        "PRIP_S5P_DLR_id": "d30d0187-5de5-4031-a160-1bac13e19689",
        "PRIP_S5P_DLR_is_published": True,
        "PRIP_S5P_DLR_publication_date": datetime.datetime(
            2021, 7, 7, 12, 50, 45, 770000, tzinfo=datetime.timezone.utc
        ),
        "nb_prip_served": 1,
        "absolute_orbit": "469",
        "key": "59f5375b291bda5643dbe95f1f1b8890",
        "mission": "S5",
        "content_length": 6486596,
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
        "prip_id": "d30d0187-5de5-4031-a160-1bac13e19689",
        "prip_publication_date": "2021-07-07T12:50:45.770Z",
        "prip_service": "PRIP_S5P_DLR",
        "datatake_id": "S5P-00469",
    }


def test_prip_consolidation_bis(prip_product_2):
    engine = PublicationConsolidatorEngine()

    engine.input_documents = [prip_product_2]

    engine.on_pre_consolidate()

    publication = engine.consolidate_from_PripProduct(
        prip_product_2, model.CdsPublication()
    )

    publication.full_clean()

    assert publication.to_dict() == {
        "key": "bac271391449a1a6e76534e73f481eb7",
        "name": "NISE_SSMISF18_20230130.HDFEOS",
        "product_level": "AUX",
        "sensing_start_date": "2023-01-30T00:00:00.000Z",
        "sensing_end_date": "2023-01-31T00:00:00.000Z",
        "sensing_duration": 86400000000,
        "timeliness": "_",
        "content_length": 2189155,
        "service_id": "S5P_DLR",
        "service_type": "PRIP",
        "product_uuid": "8d69ee20-90df-4827-8a15-3269ddd495c1",
        "publication_date": "2023-01-31T05:20:52.307Z",
        "eviction_date": "9999-12-31T23:59:59.999Z",
        "origin_date": "1970-01-01T00:00:00.000Z",
        "from_sensing_timeliness": 19252307000,
        "transfer_timeliness": 1675142452307000,
        "mission": "S5",
        "satellite_unit": "S5P",
        "datatake_id": "______",
        "product_type": "AUX_NISE",
    }
