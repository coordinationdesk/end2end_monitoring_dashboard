"""Tests for MP consolidation into datatake"""
import datetime

import pytest

from unittest.mock import patch

from opensearchpy import Search

from maas_model import datestr_to_utc_datetime

import maas_cds.model as model

from maas_cds.model.datatake import CdsDatatake

from maas_cds.model.enumeration import CompletenessScope

from maas_cds.engines.reports.consolidate_mp_file import ConsolidateMpFileEngine

MP_DICT_S1A_1 = {
    "satellite_id": "S1A",
    "datatake_id": "318318",
    "observation_time_start": "2021-12-07T13:49:09.983Z",
    "observation_duration": 20000,
    "l0_sensing_time_start": "2021-12-07T13:49:08.682Z",
    "l0_sensing_duration": 21595,
    "absolute_orbit": "40903",
    "relative_orbit": "56",
    "polarization": "DV",
    "instrument_mode": "RFC",
    "instrument_swath": "0",
    "timeliness": "NTC",
    "interface_name": "MissionPlanning",
    "production_service_type": "EDS",
    "production_service_name": "CGS",
    "reportName": "S1A_MP_ACQ__L0__20211203T160000_20211215T180000.csv",
    "ingestionTime": "2022-01-28T07:59:30.277Z",
}


MP_DICT_S1A_2 = {
    "satellite_id": "S1A",
    "datatake_id": "318318",
    "observation_time_start": "2021-12-07T13:49:09.983Z",
    "observation_duration": 20000,
    "l0_sensing_time_start": "2021-12-07T13:49:08.682Z",
    "l0_sensing_duration": 21595,
    "absolute_orbit": "40903",
    "relative_orbit": "56",
    "polarization": "DV",
    "instrument_mode": "RFC",
    "instrument_swath": "0",
    "timeliness": "NTC",
    "interface_name": "MissionPlanning",
    "production_service_type": "EDS",
    "production_service_name": "CGS",
    "reportName": "S1A_MP_ACQ__L0__20211101T160000_20211215T180000.csv",
    "ingestionTime": "2022-01-28T07:59:30.277Z",
}

MP_DICT_S1A_3 = {
    "satellite_id": "S1A",
    "datatake_id": "318318",
    "observation_time_start": "2021-12-07T13:49:09.983Z",
    "observation_duration": 20000,
    "l0_sensing_time_start": "2021-12-07T13:49:08.682Z",
    "l0_sensing_duration": 21595,
    "absolute_orbit": "40903",
    "relative_orbit": "56",
    "polarization": "DV",
    "instrument_mode": "IW",
    "instrument_swath": "0",
    "timeliness": "NTC",
    "interface_name": "MissionPlanning",
    "production_service_type": "EDS",
    "production_service_name": "CGS",
    "reportName": "S1A_MP_ACQ__L0__20211101T160000_20211215T180000.csv",
    "ingestionTime": "2022-01-28T07:59:30.277Z",
}

MP_DICT_S1A_3_bis = {
    "satellite_id": "S1A",
    "datatake_id": "318318",
    "observation_time_start": "2021-12-07T13:49:09.983Z",
    "observation_duration": 20000,
    "l0_sensing_time_start": "2021-12-07T13:49:08.682Z",
    "l0_sensing_duration": 21595,
    "absolute_orbit": "40903",
    "relative_orbit": "56",
    "polarization": "DV",
    "instrument_mode": "EW",
    "instrument_swath": "0",
    "timeliness": "NTC",
    "interface_name": "MissionPlanning",
    "production_service_type": "EDS",
    "production_service_name": "CGS",
    "reportName": "S1A_MP_ACQ__L0__20211101T160000_20211215T180000.csv",
    "ingestionTime": "2022-01-28T07:59:30.277Z",
}


MP_DICT_S2A = {
    "satellite_id": "S2A",
    "datatake_id": "318319",
    "observation_time_start": "2021-12-07T13:49:09.983Z",
    "observation_time_stop": "2021-12-07T13:59:09.983Z",
    "observation_duration": 68552,
    "number_of_scenes": 20,
    "absolute_orbit": "40903",
    "relative_orbit": "56",
    "polarization": "DV",
    "instrument_mode": "NOBS",
    "timeliness": "NTC",
    "interface_name": "MissionPlanning",
    "production_service_type": "EDS",
    "production_service_name": "CGS",
    "reportName": "S2A_MP_ACQ__MTL_20211203T160000_20211215T180000.csv",
    "ingestionTime": "2022-01-28T07:59:30.277Z",
}

MP_DICT_S1A_DOC = {
    "key": "c43d34bf843b455cdb83505fb49714f3",
    "satellite_id": "S1A",
    "mission": "S1",
    "datatake_id": "318318",
    # "observation_time_start": "2021-12-07T13:49:09.983Z",
    "observation_time_start": datetime.datetime(
        2021, 12, 7, 13, 49, 9, 983000, tzinfo=datetime.timezone.utc
    ),
    "observation_time_stop": datetime.datetime(
        2021, 12, 8, 13, 49, 9, 983000, tzinfo=datetime.timezone.utc
    ),
    "observation_duration": 20000,
    "l0_sensing_time_start": datetime.datetime(
        2021, 12, 7, 13, 49, 9, 682000, tzinfo=datetime.timezone.utc
    ),
    "l0_sensing_time_stop": datetime.datetime(
        2021, 12, 9, 13, 49, 9, 682000, tzinfo=datetime.timezone.utc
    ),
    "l0_sensing_duration": 21595,
    "absolute_orbit": "41000",
    "relative_orbit": "50",
    "polarization": "DV",
    "instrument_mode": "RFC",
    "instrument_swath": "0",
    "timeliness": "NTC",
    "interface_name": "MissionPlanning",
    "production_service_type": "EDS",
    "production_service_name": "CGS",
    "reportName": "S1A_MP_ACQ__L0__20211103T160000_20211215T180000.csv",
    "ingestionTime": "2022-01-28T07:59:30.277Z",
}

MP_HKTM_CADIP_DICT = {
    "satellite_unit": "S1A",
    "session_id": "DCS_0X_S1A_20230928063754050524",
    "ground_station": "MPS_",
    "channel": 1,
    "execution_time": "2023-09-05T17:50:48.000Z",
    "absolute_orbit": "1",
    "interface_name": "S1MissionPlanning",
    "production_service_type": "AUXIP",
    "production_service_name": "CGS",
    "reportName": "S1A_MP_HKTM_MTL_20230905T174207_20230917T010101.csv",
}

MP_HKTM_EDRS_DICT = {
    "satellite_unit": "S1A",
    "session_id": "L20230812092833855000202",
    "ground_station": "EDRS",
    "channel": 1,
    "execution_time": "2023-09-05T17:50:48.000Z",
    "absolute_orbit": "1",
    "interface_name": "S1MissionPlanning",
    "production_service_type": "AUXIP",
    "production_service_name": "CGS",
    "reportName": "S1A_MP_HKTM_MTL_20230905T174207_20230917T010101.csv",
}

MP_DICT_S1A_NOT_RECORDING_DOC = {
    "key": "c43d34bf843b455cdb83505fb49714f3",
    "satellite_unit": "S1A",
    "mission": "S1",
    "datatake_id": "318318",
    # "observation_time_start": "2021-12-07T13:49:09.983Z",
    "observation_time_start": datetime.datetime(
        2021, 12, 7, 13, 49, 9, 983000, tzinfo=datetime.timezone.utc
    ),
    "observation_time_stop": datetime.datetime(
        2021, 12, 8, 13, 49, 9, 983000, tzinfo=datetime.timezone.utc
    ),
    "observation_duration": 20000,
    "l0_sensing_time_start": datetime.datetime(
        2021, 12, 7, 13, 49, 9, 682000, tzinfo=datetime.timezone.utc
    ),
    "l0_sensing_time_stop": datetime.datetime(
        2021, 12, 9, 13, 49, 9, 682000, tzinfo=datetime.timezone.utc
    ),
    "l0_sensing_duration": 21595,
    "absolute_orbit": "41000",
    "relative_orbit": "50",
    "polarization": "DV",
    "instrument_mode": "RFC",
    "instrument_swath": "0",
    "timeliness": "NOT_RECORDING",
    "interface_name": "MissionPlanning",
    "production_service_type": "EDS",
    "production_service_name": "CGS",
    "reportName": "S1A_MP_ACQ__L0__20211103T160000_20211215T180000.csv",
    "ingestionTime": "2022-01-28T07:59:30.277Z",
}


@patch("maas_cds.model.datatake_s1.CdsDatatakeS1.compute_local_value", return_value=0)
@patch("opensearchpy.Search.scan")
@patch("maas_model.document.Document.search")
def test_mp_datatake_s1_consolidation(
    mock_search, mock_execute, mock_datatake_compute_local_value
):
    "datatake consolidation test"

    mock_search.return_value = Search()
    mock_execute.return_value = []

    raw = model.MpProduct(**MP_DICT_S1A_1)
    raw.meta.id = "S1A-318318"
    raw.full_clean()  # deserialize dates

    ConsolidateMpFileEngine.MODEL_MODULE = model
    engine = ConsolidateMpFileEngine(
        raw_data_type="MpProduct", consolidated_data_type="CdsDatatake"
    )

    datatake = engine.consolidtate_cdsdatatake_from_mpproduct(raw)

    datatake.full_clean()

    assert datatake.satellite_unit == "S1A"

    assert datatake.mission == "S1"

    assert datatake.datatake_id == "318318"
    assert datatake.hex_datatake_id == "4DB6E"

    assert datatake.observation_time_start == datetime.datetime(
        2021, 12, 7, 13, 49, 9, 983000, tzinfo=datetime.timezone.utc
    )

    assert datatake.observation_duration == 20000 * 1000

    assert datatake.observation_time_stop == datetime.datetime(
        2021, 12, 7, 13, 49, 29, 983000, tzinfo=datetime.timezone.utc
    )

    assert datatake.l0_sensing_time_start == datetime.datetime(
        2021, 12, 7, 13, 49, 8, 682000, tzinfo=datetime.timezone.utc
    )

    assert datatake.l0_sensing_duration == 21595 * 1000

    assert datatake.l0_sensing_time_stop == datetime.datetime(
        2021, 12, 7, 13, 49, 30, 277000, tzinfo=datetime.timezone.utc
    )

    assert datatake.absolute_orbit == "40903"

    assert datatake.relative_orbit == "56"

    assert datatake.polarization == "DV"

    assert datatake.instrument_mode == "RFC"

    assert datatake.instrument_swath == "0"

    assert datatake.timeliness == "NTC"

    assert datatake.key == "S1A-318318"

    assert datatake.application_date == datestr_to_utc_datetime("20211203T160000")


@patch("maas_cds.model.datatake_s2.CdsDatatakeS2.compute_local_value", return_value=0)
@patch("opensearchpy.Search.scan")
@patch("maas_model.document.Document.search")
def test_mp_datatake_s2_consolidation(
    mock_search, mock_execute, mock_compute_local_value
):
    "datatake consolidation test"

    mock_search.return_value = Search()
    mock_execute.return_value = []

    raw = model.MpProduct(**MP_DICT_S2A)
    raw.meta.id = "S2A-318319"
    raw.full_clean()  # deserialize dates

    ConsolidateMpFileEngine.MODEL_MODULE = model
    engine = ConsolidateMpFileEngine(
        raw_data_type="MpProduct", consolidated_data_type="CdsDatatake"
    )
    datatake = engine.consolidtate_cdsdatatake_from_mpproduct(raw)
    datatake.full_clean()

    assert datatake.satellite_unit == "S2A"

    assert datatake.mission == "S2"

    assert datatake.datatake_id == "318319"

    # hex_datatake_id calculation is only for S1
    assert datatake.hex_datatake_id is None

    assert datatake.observation_time_start == datetime.datetime(
        2021, 12, 7, 13, 49, 9, 983000, tzinfo=datetime.timezone.utc
    )

    assert datatake.observation_duration == 68552000

    assert datatake.observation_time_stop == datetime.datetime(
        2021, 12, 7, 13, 59, 9, 983000, tzinfo=datetime.timezone.utc
    )

    assert datatake.number_of_scenes == 20

    assert datatake.absolute_orbit == "40903"

    assert datatake.relative_orbit == "56"

    assert datatake.polarization == "DV"

    assert datatake.instrument_mode == "NOBS"

    assert datatake.timeliness == "NTC"

    assert datatake.key == "S2A-318319"

    assert datatake.application_date == datestr_to_utc_datetime("20211203T160000")

    # assert datatake.MSI_L0__GR_local_expected == 240


@patch("maas_cds.model.datatake_s1.CdsDatatakeS1.compute_local_value", return_value=0)
@patch("opensearchpy.Search.scan")
@patch("maas_model.document.Document.search")
def test_mp_datatake_application_date_consolidation_1(
    mock_search, mock_scan, mock_datatake_compute_local_value
):
    "datatake consolidation test"

    mock_search.return_value = Search()
    mock_scan.return_value = []

    raw = model.MpProduct(**MP_DICT_S1A_1)
    raw.meta.id = "S1A-318318"

    raw.full_clean()  # deserialize dates

    ConsolidateMpFileEngine.MODEL_MODULE = model
    engine = ConsolidateMpFileEngine(
        raw_data_type="MpProduct", consolidated_data_type="CdsDatatake"
    )
    datatake = engine.consolidtate_cdsdatatake_from_mpproduct(raw)

    assert datatake.satellite_unit == "S1A"

    assert datatake.mission == "S1"

    assert datatake.datatake_id == "318318"
    assert datatake.hex_datatake_id == "4DB6E"

    assert datatake.observation_time_start == datetime.datetime(
        2021, 12, 7, 13, 49, 9, 983000, tzinfo=datetime.timezone.utc
    )

    assert datatake.observation_duration == 20000 * 1000

    assert datatake.observation_time_stop == datetime.datetime(
        2021, 12, 7, 13, 49, 29, 983000, tzinfo=datetime.timezone.utc
    )

    assert datatake.l0_sensing_time_start == datetime.datetime(
        2021, 12, 7, 13, 49, 8, 682000, tzinfo=datetime.timezone.utc
    )

    assert datatake.l0_sensing_duration == 21595 * 1000

    assert datatake.l0_sensing_time_stop == datetime.datetime(
        2021, 12, 7, 13, 49, 30, 277000, tzinfo=datetime.timezone.utc
    )

    assert datatake.absolute_orbit == "40903"

    assert datatake.relative_orbit == "56"

    assert datatake.polarization == "DV"

    assert datatake.instrument_mode == "RFC"

    assert datatake.instrument_swath == "0"

    assert datatake.timeliness == "NTC"

    assert datatake.key == "S1A-318318"

    assert datatake.application_date == datestr_to_utc_datetime("20211203T160000")


@patch("opensearchpy.Search.scan")
@patch("maas_model.document.Document.search")
def test_mp_datatake_application_date_consolidation_2(mock_search, mock_execute):
    "datatake consolidation test"

    mock_search.return_value = Search()
    mock_execute.return_value = []

    raw = model.MpProduct(**MP_DICT_S1A_2)
    raw.meta.id = "649c7e1fe7835fa60d623233936c3349"
    raw.full_clean()  # deserialize dates

    ConsolidateMpFileEngine.MODEL_MODULE = model
    engine = ConsolidateMpFileEngine(
        raw_data_type="MpProduct", consolidated_data_type="CdsDatatake"
    )
    datatake = engine.consolidtate_cdsdatatake_from_mpproduct(raw)

    assert datatake.satellite_unit == "S1A"

    assert datatake.mission == "S1"

    assert datatake.datatake_id == "318318"
    assert datatake.hex_datatake_id == "4DB6E"

    assert datatake.observation_time_start == datetime.datetime(
        2021, 12, 7, 13, 49, 9, 983000, tzinfo=datetime.timezone.utc
    )

    assert datatake.observation_duration == 20000 * 1000

    assert (
        datatake.observation_time_stop
        == datatake.observation_time_start
        + datetime.timedelta(milliseconds=datatake.observation_duration / 1000)
    )

    assert datatake.l0_sensing_time_start == datetime.datetime(
        2021, 12, 7, 13, 49, 8, 682000, tzinfo=datetime.timezone.utc
    )

    assert datatake.l0_sensing_duration == 21595 * 1000

    assert (
        datatake.l0_sensing_time_stop
        == datatake.l0_sensing_time_start
        + datetime.timedelta(milliseconds=datatake.l0_sensing_duration / 1000.0)
    )

    assert datatake.absolute_orbit == "40903"

    assert datatake.relative_orbit == "56"

    assert datatake.polarization == "DV"

    assert datatake.instrument_mode == "RFC"

    assert datatake.instrument_swath == "0"

    assert datatake.timeliness == "NTC"

    assert datatake.key == "S1A-318318"

    assert datatake.application_date == datestr_to_utc_datetime("20211101T160000")


@patch("maas_cds.model.datatake_s1.CdsDatatakeS1.compute_local_value", return_value=0)
@patch("opensearchpy.Search.scan")
@patch("maas_model.document.Document.search")
def test_mp_datatake_s1_consolidation_change_instrument(
    mock_search, mock_scan, mock_datatake_compute_local_value
):
    "datatake consolidation test when we change instrument mode on s1"

    mock_search.return_value = Search()
    mock_scan.return_value = []

    raw = model.MpProduct(**MP_DICT_S1A_3)
    raw.meta.id = "649c7e1fe7835fa60d623233936c3349"
    raw.full_clean()  # deserialize dates

    raw_bis = model.MpProduct(**MP_DICT_S1A_3_bis)
    raw_bis.meta.id = "649c7e1fe7835fa60d623233936c3349"
    raw_bis.full_clean()  # deserialize dates

    instrument_mode = MP_DICT_S1A_3["instrument_mode"]
    instrument_mode_bis = MP_DICT_S1A_3_bis["instrument_mode"]

    ConsolidateMpFileEngine.MODEL_MODULE = model
    engine = ConsolidateMpFileEngine(
        raw_data_type="MpProduct", consolidated_data_type="CdsDatatake"
    )
    datatake = engine.consolidtate_cdsdatatake_from_mpproduct(raw)

    for attr in dir(datatake):
        if CompletenessScope.LOCAL.value in attr:
            assert instrument_mode in attr and instrument_mode_bis not in attr

    datatake.full_clean()

    for attr in dir(datatake):
        if CompletenessScope.LOCAL.value in attr:
            assert instrument_mode not in attr and instrument_mode_bis in attr


@patch("opensearchpy.Search.scan")
@patch("maas_model.document.Document.search")
def test_mp_datatake_not_recording_consolidation(mock_search, mock_execute):
    "datatake consolidation test"

    mock_search.return_value = Search()
    mock_execute.return_value = []

    raw = model.MpProduct(**MP_DICT_S1A_NOT_RECORDING_DOC)
    raw.meta.id = "649c7e1fe7835fa60d623233936c3349"
    raw.full_clean()  # deserialize dates

    document = model.CdsDatatake(**MP_DICT_S1A_DOC)

    ConsolidateMpFileEngine.MODEL_MODULE = model
    engine = ConsolidateMpFileEngine(
        raw_data_type="MpProduct", consolidated_data_type="CdsDatatake"
    )
    datatake = engine.consolidtate_cdsdatatake_from_mpproduct(raw)

    assert datatake is None


@patch(
    "maas_cds.engines.reports.consolidate_mp_file.ConsolidateMpFileEngine.count_hktm_acquisition_completeness"
)
@pytest.mark.parametrize(
    "mp_hktm_dict",
    [
        pytest.param(MP_HKTM_CADIP_DICT, id="Case CADIP"),
        pytest.param(MP_HKTM_EDRS_DICT, id="Case EDRS"),
    ],
)
def test_mp_hktm_consolidation(mock_completeness, mp_hktm_dict):
    "hktm cadip consolidation test"

    mock_completeness.return_value = 1

    raw = model.MpProduct(**mp_hktm_dict)
    raw.meta.id = "93ba2dfa0d4120a7ef7969979a83c87d"
    raw.full_clean()

    ConsolidateMpFileEngine.MODEL_MODULE = model
    engine = ConsolidateMpFileEngine(
        raw_data_type="MpHktmAcquisitionProduct",
        consolidated_data_type="CdsHktmAcquisitionCompleteness",
    )
    hktm = (
        engine.consolidate_cdshktmacquisitioncompleteness_from_mphktmacquisitionproduct(
            raw
        )
    )
    hktm.full_clean()

    if mp_hktm_dict["session_id"][0] == "L":
        # EDRS Case

        assert hktm.cadip_completeness is None
        assert hktm.edrs_completeness == 1
    else:
        # CADIP case
        assert hktm.cadip_completeness == 1
        assert hktm.edrs_completeness is None
