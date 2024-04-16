import pytest

from maas_cds.engines.compute.compute_hktm_related import ComputeHktmRelatedEngine

from maas_cds import model


@pytest.fixture
def hktm_dwl():
    data_dict = {
        "ingestionTime": "2023-11-07T10:17:22.465820+00:00",
        "reportName": "S2B_MP_DWL__MTL_20230928T120000_20231016T150000.csv",
        "satellite_unit": "S2B",
        "mission": "S2",
        "effective_downlink_start": "2023-09-29T03:05:07.980Z",
        "effective_downlink_stop": "2023-09-29T03:05:18.980Z",
        "downlink_duration": 11000,
        "station": "SGS_",
        "downlink_absolute_orbit": "34278",
        "updateTime": "2023-11-07T10:17:22.469524+00:00",
        "application_date": "2023-09-28T12:00:00+00:00",
        "completeness": 0,
    }

    document = model.CdsHktmProductionCompleteness(**data_dict)
    document.full_clean()
    return document


@pytest.fixture
def hktm_acq_edrs():
    data_dict = {
        "ingestionTime": "2023-11-06T15:21:08.517039+00:00",
        "reportName": "S1A_MP_HKTM_MTL_20230905T174207_20230917T010101.csv",
        "interface_name": "S1MissionPlanning",
        "channel": 1,
        "session_id": "L20220629103733153001045",
        "absolute_orbit": "2",
        "satellite_unit": "S1A",
        "mission": "S1",
        "ground_station": "EDRS-A",
        "execution_time": "2023-09-10T18:11:54.831Z",
        "production_service_name": "CGS",
        "production_service_type": "AUXIP",
        "edrs_completeness": 1,
    }
    document = model.CdsHktmAcquisitionCompleteness(**data_dict)
    document.full_clean()
    return document


@pytest.fixture
def hktm_acq_cadip():
    data_dict = {
        "ingestionTime": "2023-11-06T15:21:08.534237+00:00",
        "reportName": "S1A_MP_HKTM_MTL_20230905T174207_20230917T010101.csv",
        "interface_name": "S1MissionPlanning",
        "channel": 1,
        "session_id": "DCS_0X_S1A_20230917181149050371",
        "absolute_orbit": "5",
        "satellite_unit": "S1A",
        "mission": "S1",
        "ground_station": "EDRS",
        "execution_time": "2023-09-16T18:11:54.831Z",
        "production_service_name": "CGS",
        "production_service_type": "AUXIP",
        "cadip_completeness": 0,
    }
    document = model.CdsHktmAcquisitionCompleteness(**data_dict)
    document.full_clean()
    return document


@pytest.mark.parametrize(
    "document, input_model, update_method_str, completeness_attr",
    [
        (
            "hktm_acq_cadip",
            "CdsCadipAcquisitionPassStatus",
            "update_hktm_acquisition",
            "cadip_completeness",
        ),
        (
            "hktm_acq_edrs",
            "CdsEdrsAcquisitionPassStatus",
            "update_hktm_acquisition",
            "edrs_completeness",
        ),
        (
            "hktm_dwl",
            "CdsProduct",
            "update_hktm_production",
            "completeness",
        ),
    ],
)
def test_update_hktm_production(
    document, input_model, update_method_str, completeness_attr, request, monkeypatch
):
    engine = ComputeHktmRelatedEngine()
    engine.input_model = getattr(model, input_model)

    update_method = getattr(engine, update_method_str)

    doc = update_method(request.getfixturevalue(document))
    doc = doc.to_dict()
    assert doc[completeness_attr] == 1


@pytest.mark.parametrize(
    "target_model, update_method_str",
    [
        (
            "CdsHktmAcquisitionCompleteness",
            "update_hktm_acquisition",
        ),
        (
            "CdsHktmAcquisitionCompleteness",
            "update_hktm_acquisition",
        ),
        (
            "CdsHktmProductionCompleteness",
            "update_hktm_production",
        ),
    ],
)
def test_update_hktm_factory(target_model, update_method_str):
    engine = ComputeHktmRelatedEngine()
    engine.target_model = target_model
    update_method = engine.update_hktm_factory()

    assert update_method.__name__ == update_method_str


@pytest.mark.parametrize(
    "target_model, search_method_str",
    [
        (
            "CdsHktmAcquisitionCompleteness",
            "search_hktm_acquisition",
        ),
        (
            "CdsHktmAcquisitionCompleteness",
            "search_hktm_acquisition",
        ),
        (
            "CdsHktmProductionCompleteness",
            "search_hktm_production",
        ),
    ],
)
def test_search_hktm_factory(target_model, search_method_str):
    engine = ComputeHktmRelatedEngine()
    engine.target_model = target_model
    search_method = engine.search_hktm_factory()

    assert search_method.__name__ == search_method_str
