from unittest.mock import patch
from pytest import fixture

from maas_cds.engines.reports.interface_status import InterfaceStatusConsolidatorEngine
from maas_cds.model.generated import InterfaceProbe
from maas_cds.model import CdsInterfaceStatus


@fixture
def source_probe():
    return {
        "reportName": "MAAS-Monitoring-20220901_072649795946.json",
        "probe_time_start": "2022-09-01T07:26:43.892Z",
        "probe_time_stop": "2022-09-01T07:26:44.882Z",
        "probe_duration": 0.989614,
        "interface_name": "Jira_CAMS",
        "status": "OK",
        "status_code": 0,
        "most_recent_modification_date": "2022-08-31T11:51:00.000Z",
        "ingestionTime": "2022-09-01T07:26:49.823Z",
    }


@fixture
def previous_probe():
    return {
        "interface_name": "Jira_CAMS",
        "status": "OK",
        "status_time_start": "2022-07-29T13:52:36.098Z",
        "status_time_stop": "2022-08-01T16:49:24.075Z",
        "status_duration": 269807,
        "updateTime": "2022-08-01T16:49:47.504Z",
    }


@fixture
def next_probe():
    return {
        "interface_name": "Jira_CAMS",
        "status": "OK",
        "status_time_start": "2022-09-01T07:27:44.882Z",
        "status_time_stop": "2022-09-01T07:28:44.882Z",
        "status_duration": 60,
        "updateTime": "2022-09-01T07:29:44.882Z",
    }


def test_evaluate_interface_status_with_previous_status(source_probe, previous_probe):
    input_doc = InterfaceProbe(**source_probe)
    input_doc.meta.id = "d38a3bd9b68d85e6d978ea01d815c010"
    input_doc.clean_fields()

    previous_doc = CdsInterfaceStatus(**previous_probe)
    previous_doc.meta.id = "0fe6d6d302963c99851be322540ee6cc"
    previous_doc.clean_fields()

    interface_status_engine = InterfaceStatusConsolidatorEngine()

    result = interface_status_engine.consolidate_from_InterfaceProbe(
        input_doc, [previous_doc, None]
    )

    assert result.to_dict() == {
        "interface_name": "Jira_CAMS",
        "status": "OK",
        "status_duration": 2914448.784,
        "status_time_start": "2022-07-29T13:52:36.098Z",
        "status_time_stop": "2022-09-01T07:26:44.882Z",
        "updateTime": "2022-08-01T16:49:47.504Z",
    }


@patch("opensearchpy.Document.save", return_value=[])
@patch("opensearchpy.Document.delete", return_value=[])
def test_evaluate_interface_status_with_previous_and_next_status(
    mock_save, mock_delete, source_probe, previous_probe, next_probe
):
    input_doc = InterfaceProbe(**source_probe)
    input_doc.meta.id = "d38a3bd9b68d85e6d978ea01d815c010"
    input_doc.clean_fields()

    previous_doc = CdsInterfaceStatus(**previous_probe)
    previous_doc.meta.id = "0fe6d6d302963c99851be322540ee6cc"
    previous_doc.clean_fields()

    next_doc = CdsInterfaceStatus(**next_probe)
    next_doc.meta.id = "0fe6d6d302963c99851be322540ee6cd"
    next_doc.clean_fields()

    interface_status_engine = InterfaceStatusConsolidatorEngine()

    result = interface_status_engine.consolidate_from_InterfaceProbe(
        input_doc, [previous_doc, next_doc]
    )

    assert result.to_dict() == {
        "interface_name": "Jira_CAMS",
        "status": "OK",
        "status_duration": 2914568.784,
        "status_time_start": "2022-07-29T13:52:36.098Z",
        "status_time_stop": "2022-09-01T07:28:44.882Z",
        "updateTime": "2022-08-01T16:49:47.504Z",
    }
