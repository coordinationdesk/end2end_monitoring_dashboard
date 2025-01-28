import pytest
from unittest.mock import patch

import datetime
from maas_cds.model import (
    CdsCadipAcquisitionPassStatus,
    ApsSession,
    ApsQualityInfo,
)
from maas_engine.engine import Engine

from opensearchpy import Search

from maas_cds.engines.reports.acquisition_pass_status import (
    XBandV2AcquisitionPassStatusConsolidatorEngine,
)


@pytest.fixture
def init_engine(monkeypatch):
    def get_model_mock(*args, **kwargs):
        return CdsCadipAcquisitionPassStatus

    monkeypatch.setattr(Engine, "get_model", get_model_mock)
    engine = XBandV2AcquisitionPassStatusConsolidatorEngine(args=None)
    return engine


@pytest.fixture
def raw_session():
    data_dict = {
        "session_id": "S1A_pytest",
        "num_channels": 4,
        "publication_date": "2019-02-16T12:00:00.000Z",
        "satellite_id": "S2A",
        "station_unit_id": "SGS",
        "downlink_orbit": "62343",
        "acquisition_id": "415_01",
        "antenna_id": "INU",
        "front_end_id": "aaa",
        "ground_station": "pytest",
        "retransfer": False,
        "antenna_status": True,
        "front_end_status": False,
        "planned_data_start": "2019-02-16T02:00:00.000Z",
        "planned_data_stop": "2019-02-16T02:10:00.000Z",
        "downlink_start": "2022-01-03T02:11:00.000Z",
        "downlink_stop": "2019-02-16T02:15:00.000Z",
        "downlink_status": True,
        "delivery_push_status": True,
        "quality_infos": [
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 2,
                "CorrectedTFs": 8,
                "UncorrectableTFs": 5,
                "DataTFs": 100,
                "ErrorDataTFs": 5,
                "CorrectedDataTFs": 95,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 500,
                "TotalVolume": 1024,
                "DeliveryStart": "2022-01-01T00:00:00.000Z",
                "DeliveryStop": "2022-01-02T00:00:00.000Z",
            },
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 1,
                "CorrectedTFs": 4,
                "UncorrectableTFs": 5,
                "DataTFs": 50,
                "ErrorDataTFs": 2,
                "CorrectedDataTFs": 48,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 250,
                "TotalVolume": 512,
                "DeliveryStart": "2022-01-02T00:00:00.000Z",
                "DeliveryStop": "2022-01-03T00:00:00.000Z",
            },
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 1,
                "CorrectedTFs": 6,
                "UncorrectableTFs": 5,
                "DataTFs": 70,
                "ErrorDataTFs": 3,
                "CorrectedDataTFs": 67,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 350,
                "TotalVolume": 716,
                "DeliveryStart": "2022-01-03T00:00:00.000Z",
                "DeliveryStop": "2022-01-04T00:00:00.000Z",
            },
        ],
    }
    raw_document = ApsSession(**data_dict)
    raw_document.meta.id = "5b65d059c9dac47b8bdbb6f6fdddecbe"
    raw_document.full_clean()
    return raw_document


@pytest.fixture
def raw_session_s2c_station_id():
    data_dict = {
        "session_id": "S2C_20241214165751001440",
        "station_unit_id": "21",
        "front_end_status": True,
        "num_channels": 2,
        "downlink_orbit": 1440,
        "planned_data_start": "2024-12-14T16:57:51.000Z",
        # "Id": "28db0efa-e300-3bbd-b852-60d742d73a13",
        "ground_station": "INS",
        "acquisition_id": "01",
        "planned_data_stop": "2024-12-14T16:58:58.000Z",
        "station_id": "PAR_",
        "downlink_start": "2024-12-14T16:57:51.000Z",
        "antenna_id": "CLPA01",
        "downlink_stop": "2024-12-14T16:58:57.000Z",
        "publication_date": "2024-12-14T16:58:25.000Z",
        "front_end_id": "CLPA00HDR01,CLPA00HDR01-SEND,CLPA00HDR02",
        "downlink_status": True,
        "satellite_id": "S2C",
        "retransfer": False,
        "delivery_push_status": True,
        "antenna_status": True,
        "quality_infos": [
            {
                "AcquiredTFs": 1518859,
                "CorrectedTFs": 0,
                "DataTFs": 1144000,
                "ErrorDataTFs": 0,
                "UncorrectableDataTFs": 0,
                "DeliveryStop": "2024-12-14T16:59:45.000Z",
                "TotalVolume": 2338336000,
                "Channel": 1,
                "SessionId": "S2C_20241214165751001440",
                "ErrorTFs": 3,
                "UncorrectableTFs": 0,
                "CorrectedDataTFs": 0,
                "DeliveryStart": "2024-12-14T16:58:04.000Z",
                "TotalChunks": 8,
            },
            {
                "AcquiredTFs": 1509506,
                "CorrectedTFs": 0,
                "DataTFs": 1145500,
                "ErrorDataTFs": 0,
                "UncorrectableDataTFs": 0,
                "DeliveryStop": "2024-12-14T16:59:45.000Z",
                "TotalVolume": 2341402000,
                "Channel": 2,
                "SessionId": "S2C_20241214165751001440",
                "ErrorTFs": 3,
                "UncorrectableTFs": 0,
                "CorrectedDataTFs": 0,
                "DeliveryStart": "2024-12-14T16:58:05.000Z",
                "TotalChunks": 8,
            },
        ],
    }
    raw_document = ApsSession(**data_dict)
    raw_document.meta.id = "fake_id"
    raw_document.full_clean()
    return raw_document


@pytest.fixture
def cds_session_1():
    data_dict = {
        "session_id": "S1A_pytest",
        "num_channels": 4,
        "publication_date": "2019-02-16T12:00:00.000Z",
        "satellite_id": "S2A",
        "station_unit_id": "SGS",
        "downlink_orbit": "62343",
        "acquisition_id": "415_01",
        "ground_station": "pytest",
        "antenna_id": "INU",
        "front_end_id": "aaa",
        "retransfer": False,
        "antenna_status": True,
        "front_end_status": False,
        "planned_data_start": "2019-02-16T02:00:00.000Z",
        "planned_data_stop": "2019-02-16T02:10:00.000Z",
        "downlink_start": "2022-01-03T02:11:00.000Z",
        "downlink_stop": "2019-02-16T02:15:00.000Z",
        "downlink_status": True,
        "delivery_push_status": True,
        "global_status": "NOK",
        "quality_infos": [
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 2,
                "CorrectedTFs": 8,
                "UncorrectableTFs": 0,
                "DataTFs": 100,
                "ErrorDataTFs": 5,
                "CorrectedDataTFs": 95,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 500,
                "TotalVolume": 1024,
                "DeliveryStart": "2022-01-01T00:00:00.000Z",
                "DeliveryStop": "2022-01-02T00:00:00.000Z",
            },
            {
                "AcquiredTFs": 5,
                "ErrorTFs": 1,
                "CorrectedTFs": 4,
                "UncorrectableTFs": 0,
                "DataTFs": 50,
                "ErrorDataTFs": 2,
                "CorrectedDataTFs": 48,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 250,
                "TotalVolume": 512,
                "DeliveryStart": "2022-01-02T00:00:00.000Z",
                "DeliveryStop": "2022-01-03T00:00:00.000Z",
            },
            {
                "AcquiredTFs": 7,
                "ErrorTFs": 1,
                "CorrectedTFs": 6,
                "UncorrectableTFs": 0,
                "DataTFs": 70,
                "ErrorDataTFs": 3,
                "CorrectedDataTFs": 67,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 350,
                "TotalVolume": 716,
                "DeliveryStart": "2022-01-03T00:00:00.000Z",
                "DeliveryStop": "2022-01-04T00:00:00.000Z",
            },
        ],
    }
    document = CdsCadipAcquisitionPassStatus(**data_dict)
    document.meta.id = "5b65d059c9dac47b8bdbb6f6fdddecbe"
    document.full_clean()
    return document


@pytest.fixture
def raw_session_invalid_1():
    data_dict = {
        "session_id": "S1A_pytest",
        "num_channels": 4,
        "publication_date": "2019-02-16T12:00:00.000Z",
        "satellite_id": "S2A",
        "station_unit_id": "SGS",
        "downlink_orbit": "62343",
        "acquisition_id": "415_01",
        "antenna_id": "INU",
        "front_end_id": "aaa",
        "ground_station": "pytest",
        "retransfer": False,
        "antenna_status": True,
        "front_end_status": False,
        "planned_data_start": "2019-02-16T02:00:00.000Z",
        "planned_data_stop": "2019-02-16T02:10:00.000Z",
        "downlink_start": "2022-01-03T02:11:00.000Z",
        "downlink_stop": "2019-02-16T02:15:00.000Z",
        "delivery_push_status": True,
        "quality_infos": [],
    }
    raw_document = ApsSession(**data_dict)
    raw_document.meta.id = "5b65d059c9dac47b8bdbb6f6fdddecbe"
    raw_document.full_clean()
    return raw_document


@pytest.fixture
def raw_session_invalid_2():
    data_dict = {
        "session_id": "S1A_pytest",
        "num_channels": 4,
        "publication_date": "2019-02-16T12:00:00.000Z",
        "satellite_id": "S2A",
        "station_unit_id": "SGS",
        "downlink_orbit": "62343",
        "acquisition_id": "415_01",
        "antenna_id": "INU",
        "front_end_id": "aaa",
        "ground_station": "pytest",
        "retransfer": False,
        "antenna_status": True,
        "front_end_status": False,
        "downlink_start": "2022-01-03T02:11:00.000Z",
        "downlink_stop": "2019-02-16T02:15:00.000Z",
        "downlink_status": True,
        "delivery_push_status": True,
        "quality_infos": [
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 2,
                "CorrectedTFs": 8,
                "UncorrectableTFs": 5,
                "DataTFs": 100,
                "ErrorDataTFs": 5,
                "CorrectedDataTFs": 95,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 500,
                "TotalVolume": 1024,
                "DeliveryStart": "2022-01-01T00:00:00.000Z",
                "DeliveryStop": "2022-01-02T00:00:00.000Z",
            },
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 1,
                "CorrectedTFs": 4,
                "UncorrectableTFs": 5,
                "DataTFs": 50,
                "ErrorDataTFs": 2,
                "CorrectedDataTFs": 48,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 250,
                "TotalVolume": 512,
                "DeliveryStart": "2022-01-02T00:00:00.000Z",
                "DeliveryStop": "2022-01-03T00:00:00.000Z",
            },
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 1,
                "CorrectedTFs": 6,
                "UncorrectableTFs": 5,
                "DataTFs": 70,
                "ErrorDataTFs": 3,
                "CorrectedDataTFs": 67,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 350,
                "TotalVolume": 716,
                "DeliveryStart": "2022-01-03T00:00:00.000Z",
                "DeliveryStop": "2022-01-04T00:00:00.000Z",
            },
        ],
    }
    raw_document = ApsSession(**data_dict)
    raw_document.meta.id = "5b65d059c9dac47b8bdbb6f6fdddecbe"
    raw_document.full_clean()
    return raw_document


@pytest.fixture
def raw_session_invalid_3():
    data_dict = {
        "session_id": "S1A_pytest",
        "num_channels": 4,
        "publication_date": "2019-02-16T12:00:00.000Z",
        "satellite_id": "S2A",
        "station_unit_id": "SGS",
        "downlink_orbit": "62343",
        "acquisition_id": "415_01",
        "antenna_id": "INU",
        "front_end_id": "aaa",
        "ground_station": "pytest",
        "retransfer": False,
        "antenna_status": True,
        "front_end_status": False,
        "downlink_start": "2022-01-03T02:11:00.000Z",
        "downlink_stop": "2019-02-16T02:15:00.000Z",
        "quality_infos": [
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 2,
                "CorrectedTFs": 8,
                "UncorrectableTFs": 5,
                "DataTFs": 100,
                "ErrorDataTFs": 5,
                "CorrectedDataTFs": 95,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 500,
                "TotalVolume": 1024,
                "DeliveryStart": "2022-01-01T00:00:00.000Z",
                "DeliveryStop": "2022-01-02T00:00:00.000Z",
            },
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 1,
                "CorrectedTFs": 4,
                "UncorrectableTFs": 5,
                "DataTFs": 50,
                "ErrorDataTFs": 2,
                "CorrectedDataTFs": 48,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 250,
                "TotalVolume": 512,
                "DeliveryStart": "2022-01-02T00:00:00.000Z",
                "DeliveryStop": "2022-01-03T00:00:00.000Z",
            },
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 1,
                "CorrectedTFs": 6,
                "UncorrectableTFs": 5,
                "DataTFs": 70,
                "ErrorDataTFs": 3,
                "CorrectedDataTFs": 67,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 350,
                "TotalVolume": 716,
                "DeliveryStart": "2022-01-03T00:00:00.000Z",
                "DeliveryStop": "2022-01-04T00:00:00.000Z",
            },
        ],
    }
    raw_document = ApsSession(**data_dict)
    raw_document.meta.id = "5b65d059c9dac47b8bdbb6f6fdddecbe"
    raw_document.full_clean()
    return raw_document


@pytest.fixture
def raw_session_missing_deliverydate():
    data_dict = {
        "session_id": "S1A_pytest",
        "num_channels": 4,
        "publication_date": "2019-02-16T12:00:00.000Z",
        "satellite_id": "S2A",
        "station_unit_id": "SGS",
        "downlink_orbit": "62343",
        "acquisition_id": "415_01",
        "antenna_id": "INU",
        "front_end_id": "aaa",
        "ground_station": "pytest",
        "retransfer": False,
        "antenna_status": True,
        "front_end_status": False,
        "planned_data_start": "2019-02-16T02:00:00.000Z",
        "planned_data_stop": "2019-02-16T02:10:00.000Z",
        "downlink_start": "2022-01-03T02:11:00.000Z",
        "downlink_stop": "2019-02-16T02:15:00.000Z",
        "downlink_status": True,
        "delivery_push_status": True,
        "quality_infos": [
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 2,
                "CorrectedTFs": 8,
                "UncorrectableTFs": 5,
                "DataTFs": 100,
                "ErrorDataTFs": 5,
                "CorrectedDataTFs": 95,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 500,
                "TotalVolume": 1024,
                "DeliveryStart": "2022-01-01T00:00:00.000Z",
                "DeliveryStop": "2022-01-02T00:00:00.000Z",
            },
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 1,
                "CorrectedTFs": 4,
                "UncorrectableTFs": 5,
                "DataTFs": 50,
                "ErrorDataTFs": 2,
                "CorrectedDataTFs": 48,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 250,
                "TotalVolume": 512,
                # "DeliveryStart": "2022-01-02T00:00:00.000Z",
                # "DeliveryStop": "2022-01-03T00:00:00.000Z",
            },
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 1,
                "CorrectedTFs": 6,
                "UncorrectableTFs": 5,
                "DataTFs": 70,
                "ErrorDataTFs": 3,
                "CorrectedDataTFs": 67,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 350,
                "TotalVolume": 716,
                "DeliveryStart": "2022-01-03T00:00:00.000Z",
                "DeliveryStop": "2022-01-04T00:00:00.000Z",
            },
        ],
    }
    raw_document = ApsSession(**data_dict)
    raw_document.meta.id = "5b65d059c9dac47b8bdbb6f6fdddecbe"
    raw_document.full_clean()
    return raw_document


## Unitary tests


def test_global_status(init_engine, raw_session):
    """
    Test the global status calculation for different session statuses.

    Args:
        init_engine: Fixture to initialize the engine object.
        raw_session: Fixture providing a raw session object.

    Returns:
        None
    """
    engine = init_engine

    global_status_NOK = engine.get_global_status(raw_session)

    raw_session.antenna_status = True
    raw_session.front_end_status = True
    raw_session.delivery_push_status = True

    global_status_OK = engine.get_global_status(raw_session)

    assert global_status_NOK == "NOK"
    assert global_status_OK == "OK"


@pytest.fixture
def quality_infos():
    """
    Fixture providing a list of mock quality info objects.
    """
    quality_infos = [
        {
            "AcquiredTFs": 10,
            "ErrorTFs": 2,
            "CorrectedTFs": 8,
            "UncorrectableTFs": 0,
            "DataTFs": 100,
            "ErrorDataTFs": 5,
            "CorrectedDataTFs": 95,
            "UncorrectableDataTFs": 0,
            "TotalChunks": 500,
            "TotalVolume": 1024,
            "DeliveryStart": "2022-01-01T00:00:00.000Z",
            "DeliveryStop": "2022-01-02T00:00:00.000Z",
        },
        {
            "AcquiredTFs": 5,
            "ErrorTFs": 1,
            "CorrectedTFs": 4,
            "UncorrectableTFs": 0,
            "DataTFs": 50,
            "ErrorDataTFs": 2,
            "CorrectedDataTFs": 48,
            "UncorrectableDataTFs": 0,
            "TotalChunks": 250,
            "TotalVolume": 512,
            "DeliveryStart": "2022-01-02T00:00:00.000Z",
            "DeliveryStop": "2022-01-03T00:00:00.000Z",
        },
        {
            "AcquiredTFs": 7,
            "ErrorTFs": 1,
            "CorrectedTFs": 6,
            "UncorrectableTFs": 0,
            "DataTFs": 70,
            "ErrorDataTFs": 3,
            "CorrectedDataTFs": 67,
            "UncorrectableDataTFs": 0,
            "TotalChunks": 350,
            "TotalVolume": 716,
            "DeliveryStart": "2022-01-03T00:00:00.000Z",
            "DeliveryStop": "2022-01-04T00:00:00.000Z",
        },
    ]

    return quality_infos


def test_aggregate_quality_infos_metrics(raw_session, init_engine):
    """
    Test aggregating quality information metrics into the document object.

    Args:
        mock_quality_infos: Fixture providing a list of mock quality info objects.

    Returns:
        None
    """
    document = CdsCadipAcquisitionPassStatus()

    engine = init_engine

    document = engine.aggregate_quality_infos_metrics(
        document, raw_session.quality_infos
    )

    assert document.AcquiredTFs == 30
    assert document.ErrorTFs == 4
    assert document.CorrectedTFs == 18
    assert document.UncorrectableTFs == 15
    assert document.DataTFs == 220
    assert document.ErrorDataTFs == 10
    assert document.CorrectedDataTFs == 210
    assert document.UncorrectableDataTFs == 0
    assert document.TotalChunks == 1100
    assert document.TotalVolume == 2252
    assert document.delivery_start == datetime.datetime.strptime(
        "2022-01-01T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%f%z"
    )
    assert document.delivery_stop == datetime.datetime.strptime(
        "2022-01-04T00:00:00.000Z", "%Y-%m-%dT%H:%M:%S.%f%z"
    )


## Integration tests


@patch("opensearchpy.Search.execute")
@patch("maas_model.document.Document.search")
def test_session_consolidation(
    mock_search,
    mock_execute,
    init_engine,
    raw_session,
):
    """Test for consolidation method"""

    mock_search.return_value = Search()
    mock_execute.return_value = []

    engine = init_engine

    publication = engine.consolidate(raw_session, CdsCadipAcquisitionPassStatus())
    publication.full_clean()

    assert publication.to_dict() == {
        "session_id": "S1A_pytest",
        "num_channels": 4,
        "publication_date": "2019-02-16T12:00:00.000Z",
        "satellite_id": "S2A",
        "mission": "S2",
        "station_unit_id": "SGS",
        "downlink_orbit": "62343",
        "acquisition_id": "415_01",
        "ground_station": "pytest",
        "antenna_id": "INU",
        "front_end_id": "aaa",
        "retransfer": False,
        "antenna_status": True,
        "front_end_status": False,
        "planned_data_start": "2019-02-16T02:00:00.000Z",
        "planned_data_stop": "2019-02-16T02:10:00.000Z",
        "downlink_start": "2022-01-03T02:11:00.000Z",
        "downlink_stop": "2019-02-16T02:15:00.000Z",
        "from_acq_delivery_timeliness": (21 * 60 * 60 + 49 * 60)
        * 1000000,  # downlink_stop - delivery_start
        "delivery_bitrate": 2252
        / (
            21 * 60 * 60 + 49 * 60
        ),  # total volume / from_acq_delivery_timeliness * 1000000
        "downlink_status": True,
        "delivery_push_status": True,
        "global_status": "NOK",
        "delivery_start": "2022-01-01T00:00:00.000Z",
        "delivery_stop": "2022-01-04T00:00:00.000Z",
        "AcquiredTFs": 30,
        "ErrorTFs": 4,
        "CorrectedTFs": 18,
        "UncorrectableTFs": 15,
        "fer_data": 0.5,
        "DataTFs": 220,
        "ErrorDataTFs": 10,
        "CorrectedDataTFs": 210,
        "UncorrectableDataTFs": 0,
        "TotalChunks": 1100,
        "TotalVolume": 2252,
        "quality_infos": [
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 2,
                "CorrectedTFs": 8,
                "UncorrectableTFs": 5,
                "DataTFs": 100,
                "ErrorDataTFs": 5,
                "CorrectedDataTFs": 95,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 500,
                "TotalVolume": 1024,
                "DeliveryStart": "2022-01-01T00:00:00.000Z",
                "DeliveryStop": "2022-01-02T00:00:00.000Z",
            },
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 1,
                "CorrectedTFs": 4,
                "UncorrectableTFs": 5,
                "DataTFs": 50,
                "ErrorDataTFs": 2,
                "CorrectedDataTFs": 48,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 250,
                "TotalVolume": 512,
                "DeliveryStart": "2022-01-02T00:00:00.000Z",
                "DeliveryStop": "2022-01-03T00:00:00.000Z",
            },
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 1,
                "CorrectedTFs": 6,
                "UncorrectableTFs": 5,
                "DataTFs": 70,
                "ErrorDataTFs": 3,
                "CorrectedDataTFs": 67,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 350,
                "TotalVolume": 716,
                "DeliveryStart": "2022-01-03T00:00:00.000Z",
                "DeliveryStop": "2022-01-04T00:00:00.000Z",
            },
        ],
    }


def test_session_consolidation_retransfer_logic(
    init_engine, raw_session, cds_session_1
):
    """Test that we do not consolidate a raw data without retransfer flag if the
    same session id exist in DB with retransfer flag"""

    # raw: NOT RETRANSFER consolidated: RETRANSFER
    # Case Document already exist with retransfer flag active, we check raw
    # document without retransfer flag is ignored
    retransfer_session = cds_session_1
    retransfer_session.retransfer = True
    raw_session.retransfer = False

    retransfer_session.satellite_id = "RETRANSFER"
    retransfer_session.meta.id = "metaID"

    engine = init_engine
    publication = engine.consolidate(raw_session, retransfer_session)
    assert publication is None

    # raw: NOT RETRANSFER consolidated: NOT RETRANSFER
    # Case Document already exist with retransfer flag inactive, we check raw
    # document without retransfer flag is not ignored
    retransfer_session.retransfer = False
    raw_session.retransfer = False

    publication = engine.consolidate(raw_session, retransfer_session)
    publication.full_clean()

    assert publication.to_dict()["session_id"] == "S1A_pytest"
    assert publication.to_dict()["satellite_id"] == "S2A"
    assert not publication.to_dict()["retransfer"]

    # raw: RETRANSFER consolidated: NOT RETRANSFER
    # Case Document already exist with retransfer flag inactive, we check raw
    # document with retransfer flag is not ignored
    retransfer_session.retransfer = False
    raw_session.retransfer = True
    publication = engine.consolidate(raw_session, retransfer_session)
    publication.full_clean()

    assert publication.to_dict()["session_id"] == "S1A_pytest"
    assert publication.to_dict()["satellite_id"] == "S2A"
    assert publication.to_dict()["retransfer"]

    # raw: RETRANSFER consolidated: RETRANSFER
    # Case Document already exist with retransfer flag active, we check raw
    # document with retransfer flag is not ignored
    retransfer_session.retransfer = True
    raw_session.retransfer = True
    publication = engine.consolidate(raw_session, retransfer_session)
    publication.full_clean()

    assert publication.to_dict()["session_id"] == "S1A_pytest"
    assert publication.to_dict()["satellite_id"] == "S2A"
    assert publication.to_dict()["retransfer"]


# Hard to mock

# @patch("opensearchpy.Search.execute")
# @patch("maas_model.document.Document.search")
# def test_quality_info(
#     mock_search,
#     mock_execute,
#     raw_quality_info,
#     raw_session,
#     monkeypatch,
# ):
#     # Patch because no config file here
#     def get_model_mock(*args, **kwargs):
#         return CdsCadipAcquisitionPassStatus

#     mock_search.return_value = Search()
#     mock_execute.return_value = []

#     monkeypatch.setattr(Engine, "get_model", get_model_mock)

#     engine = XBandV2AcquisitionPassStatusConsolidatorEngine(args=None)

#     # cds_session = engine.consolidate(raw_session, CdsCadipAcquisitionPassStatus())
#     # cds_session.full_clean()

#     # mock_execute.return_value = [cds_session]

#     # mock payload
#     engine.payload = maas_model.MAASMessage(document_class="ApsQualityInfo")
#     # monkeypatch.setattr(engine, "find_or_init_session", lambda _, x: cds_session)
#     engine.input_documents = [raw_quality_info]

#     publication = next(engine.action_iterator())
#     publication = engine.consolidate(raw_quality_info, CdsCadipAcquisitionPassStatus())

#     publication.full_clean()

#     # merge dict puis comparaison
#     assert publication.to_dict() == {
#         "session_id": "S1A_pytest",
#         "num_channels": 4,
#         "publication_date": "2019-02-16T12:00:00.000Z",
#         "satellite_id": "S2A",
#         "station_unit_id": "SGS",
#         "downlink_orbit": "62343",
#         "acquisition_id": "415_01",
#         "ground_station": "pytest",
#         "antenna_id": "INU",
#         "front_end_id": "aaa",
#         "retransfer": False,
#         "antenna_status": True,
#         "front_end_status": False,
#         "planned_data_start": "2019-02-16T02:00:00.000Z",
#         "planned_data_stop": "2019-02-16T02:10:00.000Z",
#         "downlink_start": "2022-01-03T02:11:00.000Z",
#         "downlink_stop": "2022-02-16T02:15:00.000Z",
#         "downlink_status": True,
#         "delivery_push_status": True,
#         "global_status": "NOK",
#     }


@patch("opensearchpy.Search.execute")
@patch("maas_model.document.Document.search")
def test_session_consolidation_2(
    mock_search,
    mock_execute,
    init_engine,
    raw_session_invalid_1,
):
    """Test for consolidation method"""

    mock_search.return_value = Search()
    mock_execute.return_value = []

    engine = init_engine

    publication = engine.consolidate(
        raw_session_invalid_1, CdsCadipAcquisitionPassStatus()
    )
    publication.full_clean()

    assert (
        publication.partition_index_name == "cds-cadip-acquisition-pass-status-static"
    )


@patch("opensearchpy.Search.execute")
@patch("maas_model.document.Document.search")
def test_session_consolidation_3(
    mock_search,
    mock_execute,
    init_engine,
    raw_session_invalid_2,
):
    """Test for consolidation method"""

    mock_search.return_value = Search()
    mock_execute.return_value = []

    engine = init_engine

    publication = engine.consolidate(
        raw_session_invalid_2, CdsCadipAcquisitionPassStatus()
    )
    publication.full_clean()

    assert (
        publication.partition_index_name == "cds-cadip-acquisition-pass-status-static"
    )
    assert publication.global_status == "INCOMPLETE"


@patch("opensearchpy.Search.execute")
@patch("maas_model.document.Document.search")
def test_session_consolidation_4(
    mock_search,
    mock_execute,
    init_engine,
    raw_session_invalid_3,
):
    """Test for consolidation method"""

    mock_search.return_value = Search()
    mock_execute.return_value = []

    engine = init_engine

    publication = engine.consolidate(
        raw_session_invalid_3, CdsCadipAcquisitionPassStatus()
    )
    publication.full_clean()

    assert (
        publication.partition_index_name == "cds-cadip-acquisition-pass-status-static"
    )


@patch("opensearchpy.Search.execute")
@patch("maas_model.document.Document.search")
def test_session_consolidation(
    mock_search,
    mock_execute,
    init_engine,
    raw_session_missing_deliverydate,
):
    """Test for consolidation method"""

    mock_search.return_value = Search()
    mock_execute.return_value = []

    engine = init_engine

    cds_acquisition = engine.consolidate(
        raw_session_missing_deliverydate, CdsCadipAcquisitionPassStatus()
    )
    cds_acquisition.full_clean()

    assert cds_acquisition.to_dict() == {
        "session_id": "S1A_pytest",
        "num_channels": 4,
        "publication_date": "2019-02-16T12:00:00.000Z",
        "satellite_id": "S2A",
        "mission": "S2",
        "station_unit_id": "SGS",
        "downlink_orbit": "62343",
        "acquisition_id": "415_01",
        "ground_station": "pytest",
        "antenna_id": "INU",
        "front_end_id": "aaa",
        "retransfer": False,
        "antenna_status": True,
        "front_end_status": False,
        "planned_data_start": "2019-02-16T02:00:00.000Z",
        "planned_data_stop": "2019-02-16T02:10:00.000Z",
        "downlink_start": "2022-01-03T02:11:00.000Z",
        "downlink_stop": "2019-02-16T02:15:00.000Z",
        "from_acq_delivery_timeliness": (21 * 60 * 60 + 49 * 60)
        * 1000000,  # downlink_stop - delivery_start
        "delivery_bitrate": 2252
        / (
            21 * 60 * 60 + 49 * 60
        ),  # total volume / from_acq_delivery_timeliness * 1000000
        "downlink_status": True,
        "delivery_push_status": True,
        "global_status": "NOK",
        "delivery_start": "2022-01-01T00:00:00.000Z",
        "delivery_stop": "2022-01-04T00:00:00.000Z",
        "AcquiredTFs": 30,
        "ErrorTFs": 4,
        "CorrectedTFs": 18,
        "UncorrectableTFs": 15,
        "fer_data": 0.5,
        "DataTFs": 220,
        "ErrorDataTFs": 10,
        "CorrectedDataTFs": 210,
        "UncorrectableDataTFs": 0,
        "TotalChunks": 1100,
        "TotalVolume": 2252,
        "quality_infos": [
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 2,
                "CorrectedTFs": 8,
                "UncorrectableTFs": 5,
                "DataTFs": 100,
                "ErrorDataTFs": 5,
                "CorrectedDataTFs": 95,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 500,
                "TotalVolume": 1024,
                "DeliveryStart": "2022-01-01T00:00:00.000Z",
                "DeliveryStop": "2022-01-02T00:00:00.000Z",
            },
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 1,
                "CorrectedTFs": 4,
                "UncorrectableTFs": 5,
                "DataTFs": 50,
                "ErrorDataTFs": 2,
                "CorrectedDataTFs": 48,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 250,
                "TotalVolume": 512,
                # "DeliveryStart": "2022-01-02T00:00:00.000Z",
                # "DeliveryStop": "2022-01-03T00:00:00.000Z",
            },
            {
                "AcquiredTFs": 10,
                "ErrorTFs": 1,
                "CorrectedTFs": 6,
                "UncorrectableTFs": 5,
                "DataTFs": 70,
                "ErrorDataTFs": 3,
                "CorrectedDataTFs": 67,
                "UncorrectableDataTFs": 0,
                "TotalChunks": 350,
                "TotalVolume": 716,
                "DeliveryStart": "2022-01-03T00:00:00.000Z",
                "DeliveryStop": "2022-01-04T00:00:00.000Z",
            },
        ],
    }


def test_station_id(raw_session_s2c_station_id, init_engine):
    """
    Test aggregating quality information metrics into the document object.

    Args:
        mock_quality_infos: Fixture providing a list of mock quality info objects.

    Returns:
        None
    """

    engine = init_engine

    cds_acquisition = engine.consolidate(
        raw_session_s2c_station_id, CdsCadipAcquisitionPassStatus()
    )

    cds_acquisition.full_clean()

    assert cds_acquisition.station_id == "PAR_"
