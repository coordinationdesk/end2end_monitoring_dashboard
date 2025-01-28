"""Tests for MP consolidation into datatake"""

import copy
from dataclasses import dataclass
import datetime
import logging
from unittest.mock import patch
from maas_model import MAASMessage, datestr_to_utc_datetime

import pytest

from opensearchpy import Search

import maas_cds.model as model

from maas_cds.model.enumeration import CompletenessScope

from maas_cds.engines.reports.consolidate_hktm import HktmAcquisitionConsolidatorEngine
from maas_cds.engines.reports.consolidate_mp_file import ConsolidateMpFileEngine
from maas_engine.engine.base import EngineReport


class CustomSearch:
    """Small dataclaas used to mock opensearch functions"""

    @dataclass
    class CustomSearchAggs:
        # pylint: disable=W0613
        def metric(self, *args, **kwargs) -> Search:
            "Mock search query function"
            return self

    class Aggregations:
        def __init__(self):
            self.data_produced = {"value": 6666}

    class Container:
        def __init__(self):
            self.reportName = "ABCD"

    def __init__(
        self, count_value: int, get_next_report_shall_return_non_null: bool = False
    ):
        self.count_value = count_value
        self.aggs = self.CustomSearchAggs()
        self.aggregations = self.Aggregations()
        self.execute_call_nb = 0
        self.scan_call_nb = 0

        self.scan_return_list_delete = []
        self.scan_return_list_mp_consolidate_list = []
        self.get_next_report_shall_return_non_null = (
            get_next_report_shall_return_non_null
        )

    def __iter__(self):
        for x in ["66666666", "9999999"]:
            ticket = model.CdsCamsTickets()
            ticket.datatake_ids = x
            ticket.acquisition_pass = "VDGDGF"
            yield ticket

    def count(self):
        "Mock search count function"
        return self.count_value

    # pylint: disable=W0613
    def filter(self, *args, **kwargs) -> Search:
        "Mock search filter function"
        return self

    # pylint: disable=W0613
    def query(self, *args, **kwargs) -> Search:
        "Mock search query function"
        return self

    # pylint: disable=W0613
    def scan(self, *args, **kwargs) -> Search:
        "Mock search scan function"

        self.scan_call_nb += 1

        # To test action iterator process, we shall return a different value depending
        # on the search scan call, when search.scan() is called from get_to_delete_consolidated_data(),
        #  the counter is expected to be 1
        if self.scan_call_nb == 1:
            return self.scan_return_list_delete

        # on the search scan call, when search.scan() is called from get_to_be_consolidated_raw_data(),
        #  the counter is expected to be 2
        if self.scan_call_nb == 2:
            return self.scan_return_list_mp_consolidate_list

        return []

    # pylint: disable=W0613
    def execute(self, *args, **kwargs) -> Search:
        "Mock search execute function"
        self.execute_call_nb += 1

        # To test action iterator process, we shall return a different value depending
        # on the search execute call, when search.execute() is called from get_next_report(),
        #  the counter is expected to be 2
        if self.execute_call_nb == 2:
            if self.get_next_report_shall_return_non_null:
                return [self.Container()]
            else:
                return []

        return self

    # pylint: disable=W0613
    def sort(self, *args, **kwargs) -> Search:
        "Mock search sort function"
        return self

    # pylint: disable=W0613
    def params(self, *args, **kwargs) -> Search:
        "Mock search params function"
        return self

    def __getitem__(self, item):
        return self


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
    "absolute_orbit": "40904",
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
    "satellite_id": "S1A",
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
    "satellite_id": "S1A",
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

MP_ALL_DICT = {
    "absolute_orbit": "41000",
    "acquisition_duration": 12345,
    "acquisition_start": datetime.datetime(
        2000, 1, 1, 1, 1, 1, 1000, tzinfo=datetime.timezone.utc
    ),
    "acquisition_stop": datetime.datetime(
        2000, 2, 2, 2, 2, 2, 2000, tzinfo=datetime.timezone.utc
    ),
    "channel": "TestChannel",
    "datatake_id": "318318",
    "downlink_absolute_orbit": "45645",
    "downlink_duration": 999,
    "downlink_execution_time": datetime.datetime(
        2000, 3, 3, 3, 3, 3, 3000, tzinfo=datetime.timezone.utc
    ),
    "downlink_polarization": "TestPolarizationDownlink",
    "effective_downlink_start": datetime.datetime(
        2000, 4, 4, 4, 4, 4, 4000, tzinfo=datetime.timezone.utc
    ),
    "effective_downlink_stop": datetime.datetime(
        2000, 5, 5, 5, 5, 5, 5000, tzinfo=datetime.timezone.utc
    ),
    "instrument_mode": "InstrumentTestMode",
    "interface_name": "InterfaceTestName",
    "latency": 98765,
    "mission": "S1",
    "number_of_scenes": 600,
    "partial": "PartialTest",
    "polarization": "TestPolarization",
    "relative_orbit": "TestRelativeOrbit",
    "reportFolder": "TestReportFolder",
    "satellite_id": "S1A",
    "station": "INS",
    "status": "TestStatus",
    "timeliness": "TimelinessTest",
    "reportName": "S1A_MP_ALL__MTL_20220808T160000_20220820T180000",
    "session_id": [
        "DCS_0X_S1A_20240112161124052076",
    ],
}

MP_ALL_S2_DICT = {
    "satellite_id": "S2B",
    "effective_downlink_start": "2024-05-13T09:41:32.655Z",
    "effective_downlink_stop": "2024-05-13T09:43:57.716Z",
    "downlink_duration": 145061,
    "acquisition_start": "2024-05-13T09:35:40.960Z",
    "acquisition_stop": "2024-05-13T09:38:19.712Z",
    "acquisition_duration": 158752,
    "latency": 5,
    "station": "SGS_",
    "partial": "P",
    "number_of_scenes": 44,
    "timeliness": "NOMINAL",
    "mission": "S2",
    "datatake_id": "37528-1",
    "absolute_orbit": "37528",
    "relative_orbit": "36",
    "downlink_absolute_orbit": "37528",
    "interface_name": "S2MissionPlanningALL",
    "reportName": "S2B_MP_ALL__MTL_20240425T120000_20240513T150000.csv",
    "ingestionTime": "2024-04-23T09:19:49.062Z",
}

DOUBLE_MP_ALL_DICT = copy.deepcopy(MP_ALL_DICT)
DOUBLE_MP_ALL_DICT["session_id"] = [
    "DCS_0X_S1A_20240112161124052076",
    "DCS_0X_S1A_20240112162229052076",
]

DOUBLE_MP_ALL_DICT["station"] = "SGS_MTI_"

MpHktmDownlink = {
    "absolute_orbit": "1234",
    "acquisition_duration": 456789,
    "acquisition_start": datetime.datetime(
        2000, 6, 7, 8, 9, 10, 6000, tzinfo=datetime.timezone.utc
    ),
    "acquisition_stop": datetime.datetime(
        2000, 7, 8, 9, 10, 11, 7000, tzinfo=datetime.timezone.utc
    ),
    "datatake_id": "ABCD",
    "downlink_absolute_orbit_": "EFGH",
    "downlink_duration": 98765,
    "downlink_execution_time": datetime.datetime(
        2000, 8, 9, 10, 11, 12, 8000, tzinfo=datetime.timezone.utc
    ),
    "downlink_mode": "DOWNLINK_HKTM_SAD",
    "downlink_start": datetime.datetime(
        2000, 9, 10, 11, 12, 13, 9000, tzinfo=datetime.timezone.utc
    ),
    "downlink_stop": datetime.datetime(
        2000, 10, 11, 12, 13, 14, 1000, tzinfo=datetime.timezone.utc
    ),
    "effective_downlink_start": datetime.datetime(
        2000, 11, 12, 13, 14, 15, 2000, tzinfo=datetime.timezone.utc
    ),
    "effective_downlink_stop": datetime.datetime(
        2000, 12, 13, 14, 15, 16, 3000, tzinfo=datetime.timezone.utc
    ),
    "interface_name": "S2MissionPlanning",
    "latency": 5657,
    "mission": "S2",
    "number_of_scenes": "845",
    "partial": "TestPartial",
    "relative_orbit": "TestRelativeOrbit",
    "reportFolder": "/files/CDS/STAGE/INBOX/AUXIP",
    "satellite_id": "S2A",
    "station": "SVL",
    "x_off": datetime.datetime(
        2000, 1, 14, 15, 16, 17, 4000, tzinfo=datetime.timezone.utc
    ),
    "x_on": datetime.datetime(
        2000, 2, 15, 16, 17, 18, 5000, tzinfo=datetime.timezone.utc
    ),
    "reportName": "S2A_MP_DWL__MTL_20231130T120000_20231218T150000.csv",
}

MP_DICT_HktmAcquisitionProduct = {
    "absolute_orbit": "1234",
    "channel": 1,
    "execution_time": datetime.datetime(
        2000, 2, 15, 16, 17, 18, 5000, tzinfo=datetime.timezone.utc
    ),
    "ground_station": "INS",
    "interface_name": "AZERTY",
    "production_service_name": "QWERTY",
    "production_service_type": "QWERTZ",
    "reportFolder": "/files/CDS/STAGE/INBOX/AUXIP",
    "satellite_id": "S1A",
    "session_id": "DCS_0X_",
}


@patch("maas_cds.model.datatake_s1.CdsDatatakeS1.compute_local_value", return_value=0)
@patch("opensearchpy.Search.scan")
@patch("maas_model.document.Document.search")
# pylint: disable=W0613
# false unused argument warning because mock_datatake_compute_local_value is indeed used
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

    datatake = engine.consolidate_data_from_raw_data(raw)

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
# pylint: disable=W0613
# false unused argument warning because mock_compute_local_value is indeed used
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
# pylint: disable=W0613
# false unused argument warning because mock_datatake_compute_local_value is indeed used
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

    # Check it is possible to consolidate even if polarization and timeliness are missing from raw
    raw_bis = copy.deepcopy(raw)
    delattr(raw_bis, "polarization")
    delattr(raw_bis, "timeliness")
    datatake = engine.consolidtate_cdsdatatake_from_mpproduct(raw_bis)
    assert "polarization" not in datatake
    assert "timeliness" not in datatake


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

    assert datatake.absolute_orbit == "40904"

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
# pylint: disable=W0613
# false unused argument warning because mock_datatake_compute_local_value is indeed used
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

    ConsolidateMpFileEngine.MODEL_MODULE = model
    engine = ConsolidateMpFileEngine(
        raw_data_type="MpProduct", consolidated_data_type="CdsDatatake"
    )
    datatake = engine.consolidtate_cdsdatatake_from_mpproduct(raw)

    assert datatake is None


def test_consolidate_cdsdownlinkdatatake_from_mpallproduct():
    """Test CDS Downlink Datatake consolidation from a MP All Product"""
    ConsolidateMpFileEngine.MODEL_MODULE = model
    engine = ConsolidateMpFileEngine(
        raw_data_type="MpAllProduct",
        consolidated_data_type="CdsDownlinkDatatake",
    )
    raw = model.MpAllProduct(**MP_ALL_DICT)
    raw.meta.id = "rawID"

    consolidated = engine.consolidate_data_from_raw_data(raw)
    consolidated.full_clean()
    for key, value in MP_ALL_DICT.items():
        if key in (
            "absolute_orbit",
            "acquisition_duration",
            "downlink_execution_time",
            "instrument_mode",
            "interface_name",
            "number_of_scenes",
            "polarization",
            "relative_orbit",
            "reportFolder",
            "status",
            "timeliness",
        ):
            assert key not in consolidated
        elif key == "satellite_id":
            assert consolidated["satellite_unit"] == raw.satellite_id
        elif key == "session_id":
            assert consolidated["session_id"] == "S1A_20240112161124052076"
        else:
            assert consolidated[key] == value

        assert consolidated["application_date"] == datestr_to_utc_datetime(
            raw.reportName[16:31]
        )


# @patch("maas_model.document.Document.search")
# @pytest.mark.parametrize(
#     "mp_hktm_dict, doc_execution_time",
#     [
#         (MP_HKTM_CADIP_DICT, -1),
#         (MP_HKTM_CADIP_DICT, +1),
#         (MP_HKTM_EDRS_DICT, -1),
#         (MP_HKTM_EDRS_DICT, +1),
#     ],
#     ids=[
#         "Case CADIP, Older execution time in base",
#         "Case CADIP, Newer execution time in base",
#         "Case EDRS, Older execution time in base",
#         "Case EDRS, Newer execution time in base",
#     ],
# )
# def test_mp_hktm_consolidation(mock_completeness, mp_hktm_dict, doc_execution_time):
#     "hktm cadip consolidation test"

#     mock_completeness.return_value = CustomSearch(count_value=1)

#     raw = model.MpHktmAcquisitionProduct(**mp_hktm_dict)
#     raw.meta.id = "93ba2dfa0d4120a7ef7969979a83c87d"
#     raw.full_clean()

#     HktmAcquisitionConsolidatorEngine.MODEL_MODULE = model
#     engine = HktmAcquisitionConsolidatorEngine(
#         args=None,
#         raw_data_type="MpHktmAcquisitionProduct",
#     )
#     execution_time = raw.execution_time + datetime.timedelta(days=doc_execution_time)
#     document = model.CdsHktmAcquisitionCompleteness(execution_time=execution_time)

#     hktm = engine.consolidate(raw_document=raw, document=document)

#     if execution_time > raw.execution_time:
#         # case where the input document is older than the one in base
#         # so we don't consolidate it
#         assert hktm is None
#     else:
#         if mp_hktm_dict["session_id"][0] == "L":
#             # EDRS Case

#             assert hktm.cadip_completeness is None
#             assert hktm.edrs_completeness == 1
#         else:
#             # CADIP case
#             assert hktm.cadip_completeness == 1
#             assert hktm.edrs_completeness is None


@patch("maas_model.document.Document.search")
def test_consolidate_cds_hktm_production_completeness_from_mphktmdownlink(
    mock_search,
):
    """Test CdsHktmProductionCompleteness consolidation from a MpHktmDownlink"""

    mock_search.return_value = CustomSearch(count_value=1)

    ConsolidateMpFileEngine.MODEL_MODULE = model
    engine = ConsolidateMpFileEngine(
        raw_data_type="MpHktmDownlink",
        consolidated_data_type="CdsHktmProductionCompleteness",
    )
    raw = model.MpHktmDownlink(**MpHktmDownlink)
    raw.meta.id = "rawID"

    # Check if downlink_mode is not DOWNLINK_HKTM_SAD then nothing is done
    raw_wrong_downlink_mode = copy.deepcopy(raw)
    raw_wrong_downlink_mode["downlink_mode"] = "WRONGMODE"
    assert engine.consolidate_data_from_raw_data(raw_wrong_downlink_mode) is None

    mock_search.return_value = CustomSearch(count_value=1)
    consolidated = engine.consolidate_data_from_raw_data(raw)
    consolidated.full_clean()

    assert consolidated.application_date == datestr_to_utc_datetime(
        raw.reportName[16:31]
    )
    assert consolidated.reportName == raw.reportName
    assert consolidated.satellite_unit == raw.satellite_id
    assert consolidated.mission == raw.mission
    assert consolidated.datatake_id == raw.datatake_id
    assert consolidated.effective_downlink_start == (raw.effective_downlink_start)
    assert consolidated.effective_downlink_stop == (raw.effective_downlink_stop)
    assert consolidated.acquisition_start == (raw.acquisition_start)
    assert consolidated.acquisition_stop == (raw.acquisition_stop)
    assert consolidated.downlink_duration == (raw.downlink_duration)
    assert consolidated.latency == raw.latency
    assert consolidated.station == raw.station
    assert consolidated.downlink_absolute_orbit == (raw.absolute_orbit)
    assert consolidated.partial == raw.partial
    assert consolidated.meta.id == raw.meta.id
    assert consolidated.completeness == 1

    mock_search.return_value = CustomSearch(count_value=0)
    consolidated = engine.consolidate_data_from_raw_data(raw)
    assert consolidated.completeness == 0


def test_unsupported_consolidated_type(caplog):
    """Test that the engine does not crash and print a warning when
    an unsupported consolidated type is used"""
    ConsolidateMpFileEngine.MODEL_MODULE = model
    engine = ConsolidateMpFileEngine(
        raw_data_type="MpAllProduct",
        consolidated_data_type="CdsDownlinkDatatake",
    )
    engine.consolidated_data_type = "WRONG"
    raw = model.MpAllProduct(**MP_ALL_DICT)
    raw.meta.id = "rawID"
    with caplog.at_level(logging.WARNING):
        engine.consolidate_data_from_raw_data(raw)
    assert ["Unknow type for consolidation : WRONG"] == [
        rec.message for rec in caplog.records
    ]


@patch("maas_model.document.Document.search")
@pytest.mark.parametrize(
    "test_input_raw,test_input_consolidated",
    [
        ("MpProduct", "CdsDatatake"),
        ("MpAllProduct", "CdsDownlinkDatatake"),
    ],
)
def test_whole_action_iterator(
    mock_search, caplog, test_input_raw, test_input_consolidated
):
    """Test Whole action iterator function processing"""
    ConsolidateMpFileEngine.MODEL_MODULE = model
    engine = ConsolidateMpFileEngine(
        raw_data_type=test_input_raw,
        consolidated_data_type=test_input_consolidated,
    )
    rep_name = "S1A_MP_ALL__MTL_20220808T160000_20220820T180000"
    engine.input_documents = [rep_name]

    # Check log is printed when empty report is received
    mock_search.return_value = CustomSearch(count_value=0)

    with caplog.at_level(logging.INFO):
        list(engine.action_iterator())
    assert [f"[{rep_name}] report empty no completeness computed for empty report"] == [
        rec.message for rec in caplog.records
    ]

    # Check nominal processing
    cs = CustomSearch(count_value=1)

    if test_input_raw == "MpAllProduct":
        raw1 = model.MpAllProduct(**MP_ALL_DICT)
        raw1.meta.index = "raw-data-mp-all-product"
        raw1.meta.id = "rawID"
        raw1.full_clean()
        cs.scan_return_list_mp_consolidate_list = [raw1]
    else:
        raw1 = model.MpProduct(**MP_DICT_S1A_1)
        raw1.meta.index = "raw-data-mp-product"
        raw1.meta.id = "rawID3"
        raw1.full_clean()
        raw2 = model.MpProduct(**MP_DICT_S1A_2)
        raw2.meta.index = "raw-data-mp-product"
        raw2.datatake_id = "66666666"
        raw2.meta.id = "rawID4"
        raw2.full_clean()
        cs.scan_return_list_mp_consolidate_list = [raw1, raw2]

    del_doc = copy.deepcopy(raw1)
    del_doc.meta.id = "rawdel"
    cs.scan_return_list_delete = [del_doc]

    mock_search.return_value = cs
    engine.data_time_start_field_name = "acquisition_start"

    retval = list(engine.action_iterator())

    assert retval[0]["_id"] == "rawdel"
    assert retval[0]["_op_type"] == "delete"
    assert retval[1]["_op_type"] == "create"

    if test_input_raw == "MpAllProduct":
        assert retval[0]["_index"] == "raw-data-mp-all-product"
        assert retval[1]["_index"] == "cds-downlink-datatake-static"
        assert retval[1]["_source"]["downlink_absolute_orbit"] == "45645"

    else:
        assert retval[0]["_index"] == "raw-data-mp-product"
        assert retval[1]["_index"] == "cds-datatake-s1-s2"
        assert retval[1]["_source"]["absolute_orbit"] == "40903"

        assert retval[2]["_op_type"] == "create"
        assert retval[2]["_index"] == "cds-datatake-s1-s2"
        assert retval[2]["_source"]["absolute_orbit"] == "40904"


@patch("maas_model.document.Document.search")
def test_whole_action_iterator_max_date_defined(
    mock_search,
):
    """Test Whole action iterator function processing (Test case where max date is defined)"""
    ConsolidateMpFileEngine.MODEL_MODULE = model
    engine = ConsolidateMpFileEngine(
        raw_data_type="MpAllProduct",
        consolidated_data_type="CdsDownlinkDatatake",
    )
    rep_name = "S1A_MP_ALL__MTL_20220808T160000_20220820T180000"
    engine.input_documents = [rep_name]

    # Check nominal processing
    cs = CustomSearch(count_value=1, get_next_report_shall_return_non_null=True)

    raw1 = model.MpAllProduct(**MP_ALL_DICT)
    raw1.meta.index = "raw-data-mp-all-product"
    raw1.meta.id = "rawID"
    raw1.full_clean()
    cs.scan_return_list_mp_consolidate_list = [raw1]

    rawdel = copy.deepcopy(raw1)
    rawdel.meta.id = "deleteid"
    cs.scan_return_list_delete = [rawdel]

    mock_search.return_value = cs
    engine.data_time_start_field_name = "acquisition_start"

    retval = list(engine.action_iterator())

    assert retval[0]["_id"] == "deleteid"
    assert retval[0]["_op_type"] == "delete"
    assert retval[1]["_op_type"] == "create"
    assert retval[1]["_source"]["downlink_absolute_orbit"] == "45645"


@patch("maas_engine.engine.data.DataEngine._generate_reports")
def test_whole_action_iterator_related_function(
    mock_generate_report,
):
    """Test Whole action iterator function processing (Test case where max date is defined)"""
    ConsolidateMpFileEngine.MODEL_MODULE = model
    engine = ConsolidateMpFileEngine(
        raw_data_type="MpAllProduct",
        consolidated_data_type="CdsDownlinkDatatake",
    )

    # Test get_input_documents function
    mess = MAASMessage()
    mess.document_ids = ["TEST", "TEST2"]
    assert engine.get_input_documents(mess) == ["TEST", "TEST2"]

    # Test shall_report function + generate reports (without futur id)
    now = datetime.datetime.now(datetime.timezone.utc)
    past = now.replace(year=2000)
    futur = now.replace(year=3000)
    engine.data_time_start_field_name = "acquisition_start"

    raw1 = model.MpAllProduct(**MP_ALL_DICT)
    raw1.meta.id = "rawID"
    raw1[engine.data_time_start_field_name] = past

    engine.shall_report(raw1)
    assert not engine.future_ids

    report = EngineReport("other.AZERTY", [], "DocumentClass")

    mock_generate_report.return_value = [report]
    res = list(engine._generate_reports())

    assert len(res) == 1
    assert res[0].action == "other.AZERTY"

    # Test shall_report function + generate reports (with futur id)
    # We also test 'delete' report does not generate additional reports
    raw2 = model.MpAllProduct(**MP_ALL_DICT)
    raw2.meta.id = "rawID2"
    raw2[engine.data_time_start_field_name] = futur
    engine.shall_report(raw2)
    res = set()
    res.add(raw2.meta.id)
    assert engine.future_ids == res

    report = EngineReport(
        "delete.QWERTY", ["rawID2", "DELETETESTVAL4", "DELETETESTVAL6"], "DocumentClass"
    )
    report2 = EngineReport(
        "other.QWERTY", ["rawID2", "OTHERTESTVAL7", "OTHERTESTVAL8"], "DocumentClass"
    )

    mock_generate_report.return_value = [report, report2]
    res = list(engine._generate_reports())

    assert len(res) == 3

    assert res[0].action == "other.QWERTY-product"
    assert res[1].action == "other.QWERTY-publication"
    assert res[2].action == "other.QWERTY"


@patch("maas_model.document.Document.search")
@pytest.mark.parametrize(
    "mp_hktm_dict",
    [
        pytest.param(MP_HKTM_CADIP_DICT, id="Case CADIP"),
        pytest.param(MP_HKTM_EDRS_DICT, id="Case EDRS"),
    ],
)
def test_mp_hktm_consolidation_2(mock_completeness, mp_hktm_dict):
    "hktm cadip consolidation test"

    mock_completeness.return_value = CustomSearch(count_value=1)

    raw = model.MpProduct(**mp_hktm_dict)
    raw.meta.id = "93ba2dfa0d4120a7ef7969979a83c87d"
    raw.full_clean()

    ConsolidateMpFileEngine.MODEL_MODULE = model
    engine = ConsolidateMpFileEngine(
        raw_data_type="MpHktmAcquisitionProduct",
        consolidated_data_type="CdsHktmAcquisitionCompleteness",
    )
    hktm = engine.consolidate_data_from_raw_data(raw)
    hktm.full_clean()

    if mp_hktm_dict["session_id"][0] == "L":
        # EDRS Case

        assert hktm.cadip_completeness is None
        assert hktm.edrs_completeness == 1
    else:
        # CADIP case
        assert hktm.cadip_completeness == 1
        assert hktm.edrs_completeness is None


@pytest.mark.parametrize(
    "mp_all",
    [
        pytest.param(MP_ALL_DICT, id="Nominal case"),
        pytest.param(DOUBLE_MP_ALL_DICT, id="Double Mp All case"),
    ],
)
def test_should_split(mp_all, request):
    case_id = request.node.nodeid

    ConsolidateMpFileEngine.MODEL_MODULE = model
    engine = ConsolidateMpFileEngine(
        raw_data_type="MpAllProduct",
        consolidated_data_type="CdsDownlinkDatatake",
    )
    raw = model.MpAllProduct(**mp_all)
    should_split = engine.should_split_mp(raw)
    if case_id == "Nominal case":
        assert not should_split
    elif case_id == "Double Mp All case":
        assert should_split


def test_split_mp_all():
    ConsolidateMpFileEngine.MODEL_MODULE = model
    engine = ConsolidateMpFileEngine(
        raw_data_type="MpAllProduct",
        consolidated_data_type="CdsDownlinkDatatake",
    )
    raw = model.MpAllProduct(**DOUBLE_MP_ALL_DICT)
    splitted_mps = engine.split_mp_all(raw)

    assert len(splitted_mps) >= 2

    for mp in splitted_mps:
        assert len(mp.session_id) == 1
        assert len(mp.station) == 4  # ex: "SGS_"


def test_bug_no_session_id():
    ConsolidateMpFileEngine.MODEL_MODULE = model
    engine = ConsolidateMpFileEngine(
        raw_data_type="MpAllProduct",
        consolidated_data_type="CdsDownlinkDatatake",
    )

    raw = model.MpAllProduct(**MP_ALL_S2_DICT)
    raw.meta.index = "raw-data-mp-all-product"
    raw.meta.id = "rawID3"

    consolidated_doc = engine.consolidate_cdsdownlinkdatatake_from_mpallproduct(raw)

    assert consolidated_doc.session_id is None
