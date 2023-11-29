from unittest.mock import patch

import pytest


import maas_cds.model as model

from maas_cds.engines.reports import (
    ProductConsolidatorEngine,
    PublicationConsolidatorEngine,
    SatUnavailabilityConsolidatorEngine,
)


@pytest.fixture
def auxip_product_1():
    data_dict = {
        "reportName": " https://adgs.copernicus.eu",
        "product_id": "dc03b87e-9461-11ec-9d4b-fa163e7968e5",
        "product_name": "S1__AUX_WAV_V20220223T090000_G20220223T043356.SAFE.zip",
        "content_length": 466397,
        "publication_date": "2022-02-23T04:34:16.559Z",
        "start_date": "2022-02-23T09:00:00.000Z",
        "end_date": "2022-02-23T09:00:00.000Z",
        "origin_date": "2022-02-23T05:31:00.000Z",
        "eviction_date": "2022-03-30T04:34:16.559Z",
        "interface_name": "AUXIP_Exprivia",
        "production_service_type": "AUXIP",
        "production_service_name": "Exprivia",
        "ingestionTime": "2022-02-23T08:28:49.536Z",
    }

    raw_document = model.AuxipProduct(**data_dict)
    raw_document.meta.id = "63acb4648cd5d627a45f8593b9e95c4c"
    raw_document.full_clean()
    return raw_document


@pytest.fixture
def sat_unavailability_product_1():
    data_dict = {
        "product_id": "dc03b87e-9461-11ec-9d4b-fa163e7968e5",
        "reportName": "S1A_OPER_REP__SUP___20211116T122315_20211116T163855_0001.EOF",
        "file_name": "S1A_OPER_REP__SUP___20211116T122315_20211116T163855_0001",
        "mission": "Sentinel-1A",
        "unavailability_reference": "S1A-UNA-2021/0033",
        "unavailability_type": "Return to Operations",
        "subsystem": "PDHT",
        "start_time": "UTC=2021-11-16T12:23:15",
        "start_orbit": "40596",
        "start_anx_offset": 5458,
        "end_time": "UTC=2021-11-16T16:38:55",
        "end_orbit": "40599",
        "end_anx_offset": 3025,
        "type": "UNPLANNED",
        "comment": "The PDHT blockage recocurred (with a Downlink this time) after the previous recovery attempt was unsucessful.\nThe anomoly is tracked in AR GS1_SC-283.\nA manual Power Cycle of the PDHT has been performed.",
        "interface_name": "Satellite-Unavailability",
        "production_service_type": "EDS",
        "production_service_name": "CDS",
        "ingestionTime": "2022-05-16T12:00:14.985Z",
    }

    raw_document = model.SatUnavailabilityProduct(**data_dict)
    raw_document.meta.id = "63acb4648cd5d627a45f8593b9e95c4c"
    raw_document.full_clean()
    return raw_document


def test_auxip_product_consolidation(auxip_product_1):
    engine = ProductConsolidatorEngine()
    engine.input_documents = [auxip_product_1]
    engine.on_pre_consolidate()

    product = engine.consolidate_from_AuxipProduct(auxip_product_1, model.CdsProduct())

    engine.consolidated_documents = [product]
    engine.on_post_consolidate()

    assert product.to_dict() == {
        "key": "3f465f68e5d494b50cefc1171aed06ca",
        "mission": "S1",
        "auxip_id": "dc03b87e-9461-11ec-9d4b-fa163e7968e5",
        "auxip_publication_date": "2022-02-23T04:34:16.559Z",
        "product_level": "AUX",
        "name": "S1__AUX_WAV_V20220223T090000_G20220223T043356.SAFE.zip",
        "product_type": "AUX_WAV",
        "satellite_unit": "S1_",
        "sensing_start_date": "2022-02-23T09:00:00.000Z",
        "sensing_end_date": "2022-02-23T09:00:00.000Z",
        "sensing_duration": 0.0,
        "timeliness": "_",
        "content_length": 466397,
    }


def test_auxip_publication_consolidation(auxip_product_1):
    engine = PublicationConsolidatorEngine()
    engine.input_documents = [auxip_product_1]
    engine.on_pre_consolidate()

    publication = engine.consolidate_from_AuxipProduct(
        auxip_product_1, model.CdsPublication()
    )

    assert publication.to_dict() == {
        "content_length": 466397,
        "eviction_date": "2022-03-30T04:34:16.559Z",
        "from_sensing_timeliness": 15943441000.0,
        "key": "63acb4648cd5d627a45f8593b9e95c4c",
        "mission": "S1",
        "name": "S1__AUX_WAV_V20220223T090000_G20220223T043356.SAFE.zip",
        "origin_date": "2022-02-23T05:31:00.000Z",
        "product_level": "AUX",
        "product_type": "AUX_WAV",
        "product_uuid": "dc03b87e-9461-11ec-9d4b-fa163e7968e5",
        "publication_date": "2022-02-23T04:34:16.559Z",
        "satellite_unit": "S1_",
        "sensing_start_date": "2022-02-23T09:00:00.000Z",
        "sensing_end_date": "2022-02-23T09:00:00.000Z",
        "sensing_duration": 0.0,
        "service_id": "Exprivia",
        "service_type": "AUXIP",
        "transfer_timeliness": 3403441000.0,
        "timeliness": "_",
    }


def test_sat_unavailabilty_product_consolidation(sat_unavailability_product_1):
    engine = SatUnavailabilityConsolidatorEngine()

    engine.input_documents = [sat_unavailability_product_1]
    engine.on_pre_consolidate()

    product = engine.consolidate_from_SatUnavailabilityProduct(
        sat_unavailability_product_1, model.CdsSatUnavailability()
    )

    assert product.to_dict() == {
        "key": "63acb4648cd5d627a45f8593b9e95c4c",
        "satellite_unit": "S1A",
        "mission": "S1",
        "comment": "The PDHT blockage recocurred (with a Downlink this time) after the previous recovery attempt was unsucessful.\nThe anomoly is tracked in AR GS1_SC-283.\nA manual Power Cycle of the PDHT has been performed.",
        "end_anx_offset": 3025,
        "end_orbit": "40599",
        "end_time": "2021-11-16T16:38:55.000Z",
        "file_name": "S1A_OPER_REP__SUP___20211116T122315_20211116T163855_0001",
        "start_anx_offset": 5458,
        "start_orbit": "40596",
        "start_time": "2021-11-16T12:23:15.000Z",
        "subsystem": "PDHT",
        "type": "UNPLANNED",
        "unavailability_type": "Return to Operations",
        "unavailability_reference": "S1A-UNA-2021/0033",
        "unavailability_duration": 15340000000,
    }


@patch("maas_cds.model.CdsDatatake.get_by_id", return_value=None)
def test_action(mock_get_by_id, auxip_product_1):
    engine = ProductConsolidatorEngine()

    engine.input_documents = [auxip_product_1]
    engine.on_pre_consolidate()

    product = engine.consolidate_from_AuxipProduct(auxip_product_1, model.CdsProduct())

    assert engine.get_report_action("created", product) == "new.cds-product-s1"

    assert engine.get_report_document_classname(product) == "CdsProductS1"


def test_auxip_product_consolidation_1(dd_attrs):
    product = {
        "reportName": " https://adgs.copernicus.eu",
        "product_id": "17a1f3d6-e238-11ec-8988-fa163e7968e5",
        "product_name": "S1__AUX_WND_V20220602T140000_G20220602T055103.SAFE.zip",
        "content_length": 25279336,
        "publication_date": "2022-06-02T05:51:48.415Z",
        "start_date": "2022-06-02T14:00:00.000Z",
        "end_date": "2022-06-02T14:00:00.000Z",
        "origin_date": "2022-06-02T05:49:00.000Z",
        "eviction_date": "2022-07-07T05:51:48.415Z",
        "interface_name": "AUXIP_Exprivia",
        "production_service_type": "AUXIP",
        "production_service_name": "Exprivia",
        "ingestionTime": "2022-06-20T15:26:44.618Z",
    }

    auxip_product = model.AuxipProduct(**product)
    auxip_product.full_clean()

    engine = ProductConsolidatorEngine(dd_attrs=dd_attrs)

    engine.input_documents = [auxip_product]
    engine.on_pre_consolidate()

    output = engine.consolidate_from_AuxipProduct(auxip_product, model.CdsProduct())

    assert output.to_dict() == {
        "auxip_id": "17a1f3d6-e238-11ec-8988-fa163e7968e5",
        "auxip_publication_date": "2022-06-02T05:51:48.415Z",
        "key": "d374307f62caeb94e36b0f74e98e17c3",
        "mission": "S1",
        "name": "S1__AUX_WND_V20220602T140000_G20220602T055103.SAFE.zip",
        "product_level": "AUX",
        "product_type": "AUX_WND",
        "satellite_unit": "S1_",
        "sensing_duration": 0.0,
        "sensing_end_date": "2022-06-02T14:00:00.000Z",
        "sensing_start_date": "2022-06-02T14:00:00.000Z",
        "timeliness": "_",
        "content_length": 25279336,
    }

def test_auxip_product_consolidation_2():
    raw_product = {
        "reportName": " https://adgs.copernicus.eu",
        "product_id": "b1301c7e-2ba9-11ee-8b4d-fa163e7968e5",
        "product_name": "S1A_MP_FULL_20230726T174000_20230815T194000.kml.zip",
        "content_length": 331841,
        "publication_date": "2023-07-26T11:43:51.723Z",
        "start_date": "2023-07-26T17:40:00.000Z",
        "end_date": "2023-08-15T19:40:00.000Z",
        "origin_date": "2023-07-26T11:42:07.000Z",
        "eviction_date": "2023-08-30T11:43:51.723Z",
        "interface_name": "AUXIP_Exprivia",
        "production_service_type": "AUXIP",
        "production_service_name": "Exprivia",
        "ingestionTime": "2023-07-26T12:03:29.168Z"
    }

    auxip_product = model.AuxipProduct(**raw_product)
    auxip_product.meta.id = "random_id"
    auxip_product.full_clean()

    engine = ProductConsolidatorEngine()

    engine.input_documents = [auxip_product]
    engine.on_pre_consolidate()

    output = engine.consolidate_from_AuxipProduct(auxip_product, model.CdsProduct())
    print(output.to_dict())

    assert output.to_dict() == {
        'key': '775c1ac4e6b2c7df8545b3b006d4f4e8',
        'mission': 'S1',
        'name': 'S1A_MP_FULL_20230726T174000_20230815T194000.kml.zip',
        'product_type': 'MP_FULL',
        'product_level': '___',
        'satellite_unit': 'S1A',
        'sensing_start_date': '2023-07-26T17:40:00.000Z',
        'sensing_end_date': '2023-08-15T19:40:00.000Z',
        'sensing_duration': 1735200000000.0,
        'timeliness': '_',
        'content_length': 331841,
        'auxip_id': 'b1301c7e-2ba9-11ee-8b4d-fa163e7968e5',
        'auxip_publication_date': '2023-07-26T11:43:51.723Z'
    }


    engine = PublicationConsolidatorEngine()

    engine.input_documents = [auxip_product]
    engine.on_pre_consolidate()

    output = engine.consolidate_from_AuxipProduct(auxip_product, model.CdsPublication())
    print(output.to_dict())

    assert output.to_dict() == {
        'key': 'random_id',
        'mission': 'S1',
        'name': 'S1A_MP_FULL_20230726T174000_20230815T194000.kml.zip',
        'product_type': 'MP_FULL',
        'product_level': '___',
        'satellite_unit': 'S1A',
        'sensing_start_date': '2023-07-26T17:40:00.000Z',
        'sensing_end_date': '2023-08-15T19:40:00.000Z',
        'sensing_duration': 1735200000000.0,
        'timeliness': '_',
        'content_length': 331841,
        'service_id': 'Exprivia',
        'service_type': 'AUXIP',
        'product_uuid': 'b1301c7e-2ba9-11ee-8b4d-fa163e7968e5',
        'eviction_date': '2023-08-30T11:43:51.723Z',
        'origin_date': '2023-07-26T11:42:07.000Z',
        'publication_date': '2023-07-26T11:43:51.723Z',
        'transfer_timeliness': 104723000.0,
        'from_sensing_timeliness': 1756568277000.0
    }

