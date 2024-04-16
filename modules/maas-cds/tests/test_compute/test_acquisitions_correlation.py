from copy import deepcopy
from unittest.mock import patch
import maas_cds.model
from opensearchpy import MultiSearch
import pytest
from maas_cds.model import (
    CdsCadipAcquisitionPassStatus,
    CdsEdrsAcquisitionPassStatus,
    CdsDatatake,
    CdsDownlinkDatatake,
)

from maas_cds.engines.compute.correlate_acquisitions import CorrelateAcquisitionsEngine


@pytest.fixture
def downlink_datatake_1():
    data_dict = {
        "observation_time_start": "2010-01-01T00:00:00.000Z",
        "acquisition_absolute_orbit": "456",
        "delivery_stop": "2023-01-01T00:00:00.000Z",
        "effective_downlink_start": "2022-01-01T00:00:00.000Z",
        "effective_downlink_stop": "2022-02-01T00:00:00.000Z",
        "satellite_unit": "S1A",
        "station": "MTI",
        "datatake_id": "1234",
    }
    document = CdsDownlinkDatatake(**data_dict)
    document.meta.id = "qwerty1"
    document.full_clean()
    return document


@pytest.fixture
def downlink_datatake_2():
    data_dict = {
        "observation_time_start": "2011-01-01T00:00:00.000Z",
        "acquisition_absolute_orbit": "789",
        "delivery_stop": "2025-01-01T00:00:00.000Z",
        "effective_downlink_start": "2024-01-01T00:00:00.000Z",
        "effective_downlink_stop": "2024-02-01T00:00:00.000Z",
        "satellite_unit": "S1A",
        "station": "SGS",
        "datatake_id": "5678",
    }
    document = CdsDownlinkDatatake(**data_dict)
    document.meta.id = "qwerty2"
    document.full_clean()
    return document


@pytest.fixture
def cadip1():
    data_dict = {
        "delivery_stop": "2018-01-01T00:00:00.000Z",
        "satellite_id": "S1A",
        "downlink_orbit": "456",
        "ground_station": "MTI",
    }
    document = CdsCadipAcquisitionPassStatus(**data_dict)
    document.meta.id = "qwertz1"
    document.full_clean()
    return document


@pytest.fixture
def cadip2():
    data_dict = {
        "delivery_stop": "2019-01-01T00:00:00.000Z",
        "satellite_id": "S1A",
        "downlink_orbit": "789",
        "ground_station": "MTI",
    }
    document = CdsCadipAcquisitionPassStatus(**data_dict)
    document.meta.id = "qwertz2"
    document.full_clean()
    return document


@pytest.fixture
def cds_datatake_1():
    data_dict = {
        "datatake_id": "1234",
        "satellite_unit": "S1A",
        "observation_time_start": "2021-01-01T00:00:00.000Z",
    }

    document = CdsDatatake(**data_dict)
    document.meta.id = "azerty1"
    document.full_clean()
    return document


@pytest.fixture
def cds_datatake_2():
    data_dict = {
        "datatake_id": "5678",
        "satellite_unit": "S1A",
        "observation_time_start": "2022-01-01T00:00:00.000Z",
    }

    document = CdsDatatake(**data_dict)
    document.meta.id = "azerty2"
    document.full_clean()
    return document


@pytest.fixture
def edrs1():
    data_dict = {
        "dissemination_stop": "2022-02-01T00:05:00.000Z",
        "dissemination_start": "2022-01-01T00:00:00.001Z",
        "geo_satellite_id": "MTI",
        "satellite_id": "S1A",
    }
    document = CdsEdrsAcquisitionPassStatus(**data_dict)
    document.meta.id = "bepo1"
    document.full_clean()
    return document


@pytest.fixture
def edrs2():
    data_dict = {
        "dissemination_stop": "2024-02-01T00:05:00.000Z",
        "dissemination_start": "2024-01-01T00:00:00.001Z",
        "geo_satellite_id": "MTI",
        "satellite_id": "S1A",
    }
    document = CdsEdrsAcquisitionPassStatus(**data_dict)
    document.meta.id = "bepo2"
    document.full_clean()
    return document


@patch("opensearchpy.MultiSearch.add")
@patch("opensearchpy.MultiSearch.execute")
@patch("maas_cds.model.CdsDownlinkDatatake.mget_by_ids")
def test_downlink_observation_start_update(
    mock_getids,
    mock_msearch_execute,
    mock_msearch_add,
    downlink_datatake_1,
    downlink_datatake_2,
    cds_datatake_1,
    cds_datatake_2,
):
    """Verify that the Downlink Datatake observation_time_start field by a related datatake"""

    del downlink_datatake_1["observation_time_start"]
    del downlink_datatake_2["observation_time_start"]

    mock_msearch_execute.return_value = [
        [downlink_datatake_1],
        [downlink_datatake_2],
    ]
    mock_getids.return_value = [downlink_datatake_1, downlink_datatake_2]
    mock_msearch_add.return_value = MultiSearch()

    CorrelateAcquisitionsEngine.MODEL_MODULE = maas_cds.model
    engine = CorrelateAcquisitionsEngine(source_type="CdsDatatake")
    update_downlinks = engine.update_downlink_from_datatake(
        [cds_datatake_1, cds_datatake_2]
    )

    assert len(update_downlinks) == 2

    assert (
        update_downlinks[0].observation_time_start
        == cds_datatake_1.observation_time_start
    )

    assert (
        update_downlinks[1].observation_time_start
        == cds_datatake_2.observation_time_start
    )

    timeliness_1 = (
        downlink_datatake_1.delivery_stop - cds_datatake_1.observation_time_start
    )

    assert (
        update_downlinks[0].from_sensing_to_delivery_stop_timeliness
        == timeliness_1.total_seconds() * 1000000
    )

    timeliness_2 = (
        downlink_datatake_2.delivery_stop - cds_datatake_2.observation_time_start
    )

    assert (
        update_downlinks[1].from_sensing_to_delivery_stop_timeliness
        == timeliness_2.total_seconds() * 1000000
    )


@patch("opensearchpy.MultiSearch.add")
@patch("opensearchpy.MultiSearch.execute")
@patch("maas_cds.model.CdsDownlinkDatatake.mget_by_ids")
def test_downlink_delivery_stop_update_cadip(
    mock_getids,
    mock_msearch_execute,
    mock_msearch_add,
    downlink_datatake_1,
    downlink_datatake_2,
    cadip1,
    cadip2,
):
    """Verify that the Downlink Datatake delivery_stop field by a related cadip acquisition"""

    del downlink_datatake_1["delivery_stop"]
    del downlink_datatake_2["delivery_stop"]

    mock_msearch_execute.return_value = [
        [downlink_datatake_1],
        [downlink_datatake_2],
    ]
    mock_getids.return_value = [downlink_datatake_1, downlink_datatake_2]
    mock_msearch_add.return_value = MultiSearch()

    CorrelateAcquisitionsEngine.MODEL_MODULE = maas_cds.model
    engine = CorrelateAcquisitionsEngine(source_type="CdsCadipAcquisitionPassStatus")
    update_downlinks = engine.update_downlink_from_acq([cadip1, cadip2])

    assert len(update_downlinks) == 2

    assert update_downlinks[0].delivery_stop == cadip1.delivery_stop

    assert update_downlinks[1].delivery_stop == cadip2.delivery_stop

    timeliness_1 = cadip1.delivery_stop - downlink_datatake_1.observation_time_start

    assert (
        update_downlinks[0].from_sensing_to_delivery_stop_timeliness
        == timeliness_1.total_seconds() * 1000000
    )

    timeliness_2 = cadip2.delivery_stop - downlink_datatake_2.observation_time_start

    assert (
        update_downlinks[1].from_sensing_to_delivery_stop_timeliness
        == timeliness_2.total_seconds() * 1000000
    )


@patch("opensearchpy.MultiSearch.add")
@patch("opensearchpy.MultiSearch.execute")
@patch("maas_cds.model.CdsDownlinkDatatake.mget_by_ids")
def test_downlink_delivery_stop_update_edrs(
    mock_getids,
    mock_msearch_execute,
    mock_msearch_add,
    downlink_datatake_1,
    downlink_datatake_2,
    edrs1,
    edrs2,
):
    """Verify that the Downlink Datatake delivery_stop field by a related edrs acquisition"""
    del downlink_datatake_1["delivery_stop"]
    del downlink_datatake_2["delivery_stop"]

    mock_msearch_execute.return_value = [
        [downlink_datatake_1],
        [downlink_datatake_2],
    ]
    mock_getids.return_value = [downlink_datatake_1, downlink_datatake_2]
    mock_msearch_add.return_value = MultiSearch()

    CorrelateAcquisitionsEngine.MODEL_MODULE = maas_cds.model
    engine = CorrelateAcquisitionsEngine(source_type="CdsEdrsAcquisitionPassStatus")
    update_downlinks = engine.update_downlink_from_acq([edrs1, edrs2])

    assert len(update_downlinks) == 2

    assert update_downlinks[0].delivery_stop == edrs1.dissemination_stop

    assert update_downlinks[1].delivery_stop == edrs2.dissemination_stop

    timeliness_1 = edrs1.dissemination_stop - downlink_datatake_1.observation_time_start

    assert (
        update_downlinks[0].from_sensing_to_delivery_stop_timeliness
        == timeliness_1.total_seconds() * 1000000
    )

    timeliness_2 = edrs2.dissemination_stop - downlink_datatake_2.observation_time_start

    assert (
        update_downlinks[1].from_sensing_to_delivery_stop_timeliness
        == timeliness_2.total_seconds() * 1000000
    )


def test_no_correlation_on_incomplete_input_doc(edrs1, cadip1, cds_datatake_1):
    """Check that when the required field in the input documents are not
    available, no correlation is done"""
    CorrelateAcquisitionsEngine.MODEL_MODULE = maas_cds.model

    for x in (
        "dissemination_stop",
        "satellite_id",
        "geo_satellite_id",
        "dissemination_start",
    ):
        input_doc = deepcopy(edrs1)
        del input_doc[x]
        engine = CorrelateAcquisitionsEngine(source_type="CdsEdrsAcquisitionPassStatus")
        assert len(engine.update_downlink_from_acq([input_doc])) == 0

    for x in (
        "delivery_stop",
        "ground_station",
        "downlink_orbit",
        "satellite_id",
    ):
        input_doc = deepcopy(cadip1)
        del input_doc[x]
        engine = CorrelateAcquisitionsEngine(
            source_type="CdsCadipAcquisitionPassStatus"
        )
        assert len(engine.update_downlink_from_acq([input_doc])) == 0

    for x in ("datatake_id", "satellite_unit"):
        input_doc = deepcopy(cds_datatake_1)
        del input_doc[x]
        engine = CorrelateAcquisitionsEngine(source_type="CdsDatatake")
        assert len(engine.update_downlink_from_datatake([input_doc])) == 0
