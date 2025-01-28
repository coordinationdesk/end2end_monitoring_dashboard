from unittest.mock import patch

import pytest

import datetime
import maas_cds.model as model

from maas_cds.engines.reports import (
    ProductConsolidatorEngine,
    PublicationConsolidatorEngine,
    SatUnavailabilityConsolidatorEngine,
)


@pytest.fixture
def datatake_s1():
    datatake_dict = {
        "name": "S1A_MP_ACQ__L0__20231212T172509_20231224T194320.csv",
        "key": "S1A-408706",
        "datatake_id": "408706",
        "hex_datatake_id": "63C82",
        "satellite_unit": "S1A",
        "mission": "S1",
        "observation_time_start": "2023-12-14T06:36:29.627Z",
        "observation_duration": 650952000,
        "observation_time_stop": "2023-12-14T06:47:20.579Z",
        "l0_sensing_duration": 652529000,
        "l0_sensing_time_start": "2023-12-14T06:36:28.836Z",
        "l0_sensing_time_stop": "2023-12-14T06:47:21.365Z",
        "absolute_orbit": "51647",
        "relative_orbit": "125",
        "polarization": "DV",
        "timeliness": "NRT-PT",
        "instrument_mode": "IW",
        "instrument_swath": "0",
        "application_date": "2023-12-12T17:25:09.000Z",
        "updateTime": "2023-12-14T08:25:06.681Z",
    }
    datatake_s1 = model.CdsDatatake(**datatake_dict)
    datatake_s1.full_clean()
    datatake_s1.meta.id = "S1A-408706-1"
    datatake_s1.meta.index = "cds-datatake-s1-s2"

    return datatake_s1


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


@patch(
    "maas_cds.engines.reports.base.BaseProductConsolidatorEngine.get_datatake_dict_S1"
)
def test_auxip_product_consolidation(mock_find_datatake, auxip_product_1, datatake_s1):
    engine = ProductConsolidatorEngine()
    engine.input_documents = [auxip_product_1]
    engine.on_pre_consolidate()

    mock_find_datatake.return_value = {
        "S1A_IW_GRDH_1SDV_20231214T064159_20231214T064224_051647_063C82_63C0_COG": datatake_s1
    }
    product = engine.consolidate_from_AuxipProduct(auxip_product_1, model.CdsProduct())

    engine.consolidated_documents = [product]
    engine.on_post_consolidate()

    assert product.to_dict() == {
        "AUXIP_Exprivia_id": "dc03b87e-9461-11ec-9d4b-fa163e7968e5",
        "AUXIP_Exprivia_is_published": True,
        "AUXIP_Exprivia_publication_date": datetime.datetime(
            2022, 2, 23, 4, 34, 16, 559000, tzinfo=datetime.timezone.utc
        ),
        "nb_auxip_served": 1,
        "key": "3f465f68e5d494b50cefc1171aed06ca",
        "mission": "S1",
        "auxip_id": "dc03b87e-9461-11ec-9d4b-fa163e7968e5",
        "auxip_publication_date": "2022-02-23T04:34:16.559Z",
        "product_level": "AUX",
        "name": "S1__AUX_WAV_V20220223T090000_G20220223T043356.SAFE.zip",
        "product_type": "AUX_WAV",
        "satellite_unit": "S1_",
        "datatake_id": "______",
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
        "datatake_id": "______",
    }


@patch("maas_cds.model.CdsSatUnavailability.get_by_id", return_value=None)
def test_sat_unavailabilty_product_consolidation(
    get_by_id, sat_unavailability_product_1
):
    engine = SatUnavailabilityConsolidatorEngine()

    engine.input_documents = [sat_unavailability_product_1]
    engine.on_pre_consolidate()

    product = engine.consolidate_from_SatUnavailabilityProduct(
        sat_unavailability_product_1, model.CdsSatUnavailability()
    )

    assert product.to_dict() == {
        "key": "ea887b25bb5b1dd8484479f1cf6e78b7",
        "satellite_unit": "S1A",
        "mission": "S1",
        "raw_data_ingestion_time": "2022-05-16T12:00:14.985Z",
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
        "AUXIP_Exprivia_id": "17a1f3d6-e238-11ec-8988-fa163e7968e5",
        "AUXIP_Exprivia_is_published": True,
        "AUXIP_Exprivia_publication_date": datetime.datetime(
            2022, 6, 2, 5, 51, 48, 415000, tzinfo=datetime.timezone.utc
        ),
        "nb_auxip_served": 1,
        "auxip_id": "17a1f3d6-e238-11ec-8988-fa163e7968e5",
        "auxip_publication_date": "2022-06-02T05:51:48.415Z",
        "key": "d374307f62caeb94e36b0f74e98e17c3",
        "mission": "S1",
        "name": "S1__AUX_WND_V20220602T140000_G20220602T055103.SAFE.zip",
        "product_level": "AUX",
        "product_type": "AUX_WND",
        "satellite_unit": "S1_",
        "sensing_duration": 0.0,
        "datatake_id": "______",
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
        "ingestionTime": "2023-07-26T12:03:29.168Z",
    }

    auxip_product = model.AuxipProduct(**raw_product)
    auxip_product.meta.id = "random_id"
    auxip_product.full_clean()

    engine = ProductConsolidatorEngine()

    engine.input_documents = [auxip_product]
    engine.on_pre_consolidate()

    output = engine.consolidate_from_AuxipProduct(auxip_product, model.CdsProduct())

    assert output.to_dict() == {
        "AUXIP_Exprivia_id": "b1301c7e-2ba9-11ee-8b4d-fa163e7968e5",
        "AUXIP_Exprivia_is_published": True,
        "AUXIP_Exprivia_publication_date": datetime.datetime(
            2023, 7, 26, 11, 43, 51, 723000, tzinfo=datetime.timezone.utc
        ),
        "nb_auxip_served": 1,
        "key": "775c1ac4e6b2c7df8545b3b006d4f4e8",
        "mission": "S1",
        "name": "S1A_MP_FULL_20230726T174000_20230815T194000.kml.zip",
        "product_type": "MP_FULL",
        "product_level": "___",
        "satellite_unit": "S1A",
        "sensing_start_date": "2023-07-26T17:40:00.000Z",
        "sensing_end_date": "2023-08-15T19:40:00.000Z",
        "sensing_duration": 1735200000000.0,
        "timeliness": "_",
        "datatake_id": "______",
        "content_length": 331841,
        "auxip_id": "b1301c7e-2ba9-11ee-8b4d-fa163e7968e5",
        "auxip_publication_date": "2023-07-26T11:43:51.723Z",
    }

    engine = PublicationConsolidatorEngine()

    engine.input_documents = [auxip_product]
    engine.on_pre_consolidate()

    output = engine.consolidate_from_AuxipProduct(auxip_product, model.CdsPublication())
    print(output.to_dict())

    assert output.to_dict() == {
        "key": "random_id",
        "mission": "S1",
        "name": "S1A_MP_FULL_20230726T174000_20230815T194000.kml.zip",
        "product_type": "MP_FULL",
        "product_level": "___",
        "satellite_unit": "S1A",
        "sensing_start_date": "2023-07-26T17:40:00.000Z",
        "sensing_end_date": "2023-08-15T19:40:00.000Z",
        "sensing_duration": 1735200000000.0,
        "timeliness": "_",
        "content_length": 331841,
        "service_id": "Exprivia",
        "service_type": "AUXIP",
        "datatake_id": "______",
        "product_uuid": "b1301c7e-2ba9-11ee-8b4d-fa163e7968e5",
        "eviction_date": "2023-08-30T11:43:51.723Z",
        "origin_date": "2023-07-26T11:42:07.000Z",
        "publication_date": "2023-07-26T11:43:51.723Z",
        "transfer_timeliness": 104723000.0,
        "from_sensing_timeliness": 1756568277000.0,
    }
