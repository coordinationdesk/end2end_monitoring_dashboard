from unittest.mock import patch
from pytest import fixture

from maas_cds.engines.reports.interface_status import InterfaceStatusConsolidatorEngine
from maas_cds.model.generated import InterfaceProbe
from maas_cds.model import CdsInterfaceStatus
from opensearchpy import Search
import datetime
import hashlib


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


class CustomSearch:
    """Small dataclaas used to mock opensearch functions"""

    def __init__(self, execute_return_values=[]):
        self.execute_return_values = execute_return_values
        self.executer_counter = 0

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
        return self

    # pylint: disable=W0613
    def execute(self, *args, **kwargs) -> Search:
        "Mock search execute function"

        retval = self.execute_return_values[self.executer_counter]
        self.executer_counter += 1
        return retval

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


@patch("maas_model.document.Document.search")
def test_get_consolidated_documents(
    mock_search, source_probe, previous_probe, next_probe
):
    input_doc = InterfaceProbe(**source_probe)
    input_doc.meta.id = "d38a3bd9b68d85e6d978ea01d815c010"
    input_doc.clean_fields()

    cs = CustomSearch([previous_probe, next_probe])
    mock_search.return_value = cs

    refresh = 300

    interface_status_engine = InterfaceStatusConsolidatorEngine(
        refresh_interval_seconds=refresh
    )
    interface_status_engine.input_documents = [input_doc]

    # Case no previous, no next
    cs.execute_return_values = [None, None]
    assert interface_status_engine.get_consolidated_documents() == [(None, None)]

    # Case previous and next exist but out of refresh_delta
    input_doc.probe_time_start = "2022-02-01T00:00:00.000Z"
    input_doc.clean_fields()

    prev_probe_out_of_bound = CdsInterfaceStatus(**previous_probe)
    prev_probe_out_of_bound.status_time_stop = (
        input_doc.probe_time_start - datetime.timedelta(seconds=301)
    )

    next_probe_out_of_bound = CdsInterfaceStatus(**next_probe)
    next_probe_out_of_bound.status_time_start = (
        input_doc.probe_time_stop + datetime.timedelta(seconds=301)
    )

    cs.executer_counter = 0
    cs.execute_return_values = [[prev_probe_out_of_bound], [next_probe_out_of_bound]]

    assert interface_status_engine.get_consolidated_documents() == [(None, None)]

    # Case previous and next exist in refresh_delta range
    input_doc.probe_time_start = "2022-02-01T00:00:00.000Z"
    input_doc.clean_fields()

    prev_probe_out_of_bound = CdsInterfaceStatus(**previous_probe)
    prev_probe_out_of_bound.status_time_stop = (
        input_doc.probe_time_start - datetime.timedelta(seconds=300)
    )

    next_probe_out_of_bound = CdsInterfaceStatus(**next_probe)
    next_probe_out_of_bound.status_time_start = (
        input_doc.probe_time_stop + datetime.timedelta(seconds=300)
    )

    cs.executer_counter = 0
    cs.execute_return_values = [[prev_probe_out_of_bound], [next_probe_out_of_bound]]

    assert interface_status_engine.get_consolidated_documents() == [
        (prev_probe_out_of_bound, next_probe_out_of_bound)
    ]


def test_probe_status_creation(source_probe):
    input_doc = InterfaceProbe(**source_probe)
    input_doc.meta.id = "d38a3bd9b68d85e6d978ea01d815c010"
    input_doc.clean_fields()

    interface_status_engine = InterfaceStatusConsolidatorEngine()
    res = interface_status_engine.create_status_from_probe(input_doc)

    assert isinstance(res, CdsInterfaceStatus)
    assert res.interface_name == input_doc.interface_name
    assert res.status == input_doc.status

    duration = (input_doc.probe_time_stop - input_doc.probe_time_start).total_seconds()
    assert res.status_duration == duration

    assert res.status_time_start == input_doc.probe_time_start
    assert res.status_time_stop == input_doc.probe_time_stop

    resdict = res.to_dict()
    expected_id = hashlib.md5()
    expected_id.update(resdict["interface_name"].encode())
    expected_id.update(resdict["status_time_start"].encode())
    expected_id.update(resdict["status_time_stop"].encode())

    assert res.meta.id == expected_id.hexdigest()


class MockSave:
    # pylint: disable=W0613
    def saved(self, *args, **kwargs):
        "Mock search query function"
        # yield self


def test_evaluate_interface_status_without_prev_and_next(source_probe):
    input_doc = InterfaceProbe(**source_probe)
    input_doc.meta.id = "d38a3bd9b68d85e6d978ea01d815c010"
    input_doc.clean_fields()

    interface_status_engine = InterfaceStatusConsolidatorEngine()

    result = interface_status_engine.consolidate_from_InterfaceProbe(
        input_doc, [None, None]
    )

    duration = (result.status_time_stop - result.status_time_start).total_seconds()

    assert result.to_dict() == {
        "interface_name": "Jira_CAMS",
        "status": "OK",
        "status_duration": duration,
        "status_time_start": "2022-09-01T07:26:43.892Z",
        "status_time_stop": "2022-09-01T07:26:44.882Z",
    }


@patch("opensearchpy.Document.delete", return_value=[])
def test_evaluate_interface_status_merge_previous_and_next_status(
    mock_delete, source_probe, previous_probe, next_probe
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

    duration = (
        next_doc.status_time_stop - previous_doc.status_time_start
    ).total_seconds()
    assert result.status_duration == duration


@patch("opensearchpy.Document.save", return_value=[])
def test_evaluate_interface_status_merge_previous_and_probe_same_status(
    mock_save, source_probe, previous_probe
):
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

    duration = (
        input_doc.probe_time_stop - previous_doc.status_time_start
    ).total_seconds()

    assert previous_doc.status_time_stop == result.status_time_stop

    assert result.status_duration == duration


@patch("opensearchpy.Document.save", return_value=[], autospec=True)
def test_evaluate_interface_status_no_merge_previous_and_probe_different_status(
    mock_save, source_probe, previous_probe
):
    input_doc = InterfaceProbe(**source_probe)
    input_doc.meta.id = "d38a3bd9b68d85e6d978ea01d815c010"
    input_doc.clean_fields()

    previous_doc = CdsInterfaceStatus(**previous_probe)
    previous_doc.meta.id = "0fe6d6d302963c99851be322540ee6cc"
    previous_doc.status = "KO"
    previous_doc.clean_fields()

    interface_status_engine = InterfaceStatusConsolidatorEngine()

    result = interface_status_engine.consolidate_from_InterfaceProbe(
        input_doc, [previous_doc, None]
    )

    # Check stop time of previous is increased till the start of the probe start
    prev_status = mock_save.call_args_list[0].args[0]
    duration = (
        input_doc.probe_time_start - previous_doc.status_time_start
    ).total_seconds()
    assert prev_status.status_duration == duration

    # Check new status is generated
    assert result.status_time_start == input_doc.probe_time_start
    assert result.status_time_stop == input_doc.probe_time_stop
    duration = (result.status_time_stop - result.status_time_start).total_seconds()
    assert result.status_duration == duration


@patch("opensearchpy.Document.save", return_value=[])
def test_evaluate_interface_status_merge_next_and_probe_same_status(
    mock_save, source_probe, next_probe
):
    input_doc = InterfaceProbe(**source_probe)
    input_doc.meta.id = "d38a3bd9b68d85e6d978ea01d815c010"
    input_doc.clean_fields()

    next_doc = CdsInterfaceStatus(**next_probe)
    next_doc.meta.id = "0fe6d6d302963c99851be322540ee6cc"
    next_doc.clean_fields()

    interface_status_engine = InterfaceStatusConsolidatorEngine()

    result = interface_status_engine.consolidate_from_InterfaceProbe(
        input_doc, [None, next_doc]
    )

    duration = (next_doc.status_time_stop - input_doc.probe_time_start).total_seconds()

    assert result.status_time_stop == next_doc.status_time_stop
    assert result.status_time_start == input_doc.probe_time_start
    assert result.status_duration == duration


@patch("opensearchpy.Document.save", return_value=[], autospec=True)
def test_evaluate_interface_status_no_merge_next_and_probe_different_status(
    mock_save, source_probe, next_probe
):
    input_doc = InterfaceProbe(**source_probe)
    input_doc.meta.id = "d38a3bd9b68d85e6d978ea01d815c010"
    input_doc.clean_fields()

    next_doc = CdsInterfaceStatus(**next_probe)
    next_doc.meta.id = "0fe6d6d302963c99851be322540ee6cc"
    next_doc.status = "KO"
    next_doc.clean_fields()

    interface_status_engine = InterfaceStatusConsolidatorEngine()

    result = interface_status_engine.consolidate_from_InterfaceProbe(
        input_doc, [None, next_doc]
    )

    # Check a new status is generated using parameter of the current probe
    duration = (input_doc.probe_time_stop - input_doc.probe_time_start).total_seconds()
    assert result.status_time_stop == input_doc.probe_time_stop
    assert result.status_time_start == input_doc.probe_time_start
    assert result.status_duration == duration
    assert result.status == "OK"

    # Check start time of next doc is set to start date of probe
    next_status = mock_save.call_args_list[0].args[0]
    duration = (
        next_status.status_time_stop - input_doc.probe_time_stop
    ).total_seconds()

    assert next_status.status_duration == duration
    assert next_status.status_time_start == input_doc.probe_time_stop
    assert next_status.status == "KO"


@patch("maas_model.document.Document.save", autospec=True)
def test_status_split_case_previous(mock_save, source_probe):
    # Create a status between 2022-01-01H00:00:00 and 2022-12-31H23:59:59
    previous = CdsInterfaceStatus()
    previous.interface_name = "test"
    previous.status_time_start = "2022-01-01T00:00:00.000Z"
    previous.status_time_stop = "2022-12-31T23:11:59.000Z"
    previous.clean_fields()

    # Create a probe during 1 month in the middle of the previous status period
    input_doc = InterfaceProbe(**source_probe)
    input_doc.meta.id = "d38a3bd9b68d85e6d978ea01d815c010"
    input_doc.probe_time_start = "2022-02-01T00:00:00.000Z"
    input_doc.probe_time_stop = "2022-03-01T00:00:00.000Z"
    input_doc.clean_fields()

    interface_status_engine = InterfaceStatusConsolidatorEngine()

    retval = interface_status_engine.consolidate_from_InterfaceProbe(
        input_doc, [previous, None]
    )

    # Check split part before probe
    status = mock_save.call_args_list[0].args[0]
    status = status.to_dict()
    assert status["status_time_start"] == "2022-01-01T00:00:00.000Z"
    assert status["status_time_stop"] == "2022-02-01T00:00:00.000Z"

    # Check split part after probe
    status = mock_save.call_args_list[1].args[0]
    status = status.to_dict()
    assert status["status_time_start"] == "2022-02-01T00:05:00.000Z"
    assert status["status_time_stop"] == "2022-12-31T23:11:59.000Z"

    # Check split part matching probe
    status = retval
    status = status.to_dict()
    assert status["status_time_start"] == "2022-02-01T00:00:00.000Z"
    assert status["status_time_stop"] == "2022-02-01T00:05:00.000Z"


@patch("maas_model.document.Document.save", autospec=True)
def test_status_split_case_after(mock_save, source_probe):
    # Create a status between 2022-01-01H00:00:00 and 2022-12-31H23:59:59
    prev = CdsInterfaceStatus()
    prev.interface_name = "test"
    prev.status_time_start = "2022-01-01T00:00:00.000Z"
    prev.status_time_stop = "2022-12-31T23:11:59.000Z"
    prev.clean_fields()

    # Create a probe during 1 month in the middle of the prev status period
    input_doc = InterfaceProbe(**source_probe)
    input_doc.meta.id = "d38a3bd9b68d85e6d978ea01d815c010"
    input_doc.probe_time_start = "2022-02-01T00:00:00.000Z"
    input_doc.probe_time_stop = "2022-03-01T00:00:00.000Z"
    input_doc.clean_fields()

    interface_status_engine = InterfaceStatusConsolidatorEngine()

    retval = interface_status_engine.consolidate_from_InterfaceProbe(
        input_doc, [prev, None]
    )

    # Check split part before probe
    status = mock_save.call_args_list[0].args[0]
    status = status.to_dict()
    assert status["status_time_start"] == "2022-01-01T00:00:00.000Z"
    assert status["status_time_stop"] == "2022-02-01T00:00:00.000Z"

    # Check split part after probe
    status = mock_save.call_args_list[1].args[0]
    status = status.to_dict()
    assert status["status_time_start"] == "2022-02-01T00:05:00.000Z"
    assert status["status_time_stop"] == "2022-12-31T23:11:59.000Z"

    # Check split part matching probe
    status = retval
    status = status.to_dict()
    assert status["status_time_start"] == "2022-02-01T00:00:00.000Z"
    assert status["status_time_stop"] == "2022-02-01T00:05:00.000Z"
