""" Tests for ddp_consolidation engine"""
from unittest.mock import patch
import pytest
import maas_cds.model as model

from maas_cds.engines.reports.acquisition_pass_status import (
    XBandAcquisitionPassStatusConsolidatorEngine,
)
from maas_cds.model import CdsAcquisitionPassStatus


@pytest.fixture
def raw_data_aps_product():
    """APSProduct raw data fixture ( report type daily)

    Returns:
        (APSProduct): raw data APS product
    """
    data_dict = {
        "reportName": "firstpart_secondpart",
        "antenna_id": "ABCD",
        "antenna_status": "EFGH",
        "delivery_push_status": "IJKL",
        "downlink_orbit": "MNOPQZ",
        "doy": 1234,
        "fer_data": 5678.9,
        "fer_downlink": 1234.5,
        "first_frame_start": "2021-06-07T02:21:15.100Z",
        "front_end_id": "QRST",
        "front_end_status": "UVWX",
        "ground_station": "YZAB",
        "interface_name": "CDEF",
        "last_frame_stop": "2001-06-08T13:42:42.100Z",
        "mission": "GHIJ",
        "notes": "KLMN",
        "number_of_chunks": 9876,
        "overall_data_volume": 456456,
        "overall_number_of_bad_data_acquired_frames": 123123,
        "overall_number_of_bad_downlinked_frames": 789789,
        "overall_number_of_data_acquired_frames": 13311331,
        "overall_number_of_downlinked_frames": 45454545,
        "planned_data_start": "2001-02-02T10:42:42.100Z",
        "planned_data_stop": "2011-11-09T05:10:10.110Z",
        "production_service_name": "PQRS",
        "production_service_type": "TUVW",
        "reportFolder": "XYXY",
        "satellite_id": "AZOPQZ",
        "start_delivery": "2020-05-06T08:12:32.100Z",
        "stop_delivery": "2021-06-07T03:23:45.100Z",
        "report_type": "daily",
    }
    raw_document = model.ApsProduct(**data_dict)
    raw_document.meta.id = "ABCDEFGH12312312312"
    raw_document.full_clean()
    return raw_document


@patch("maas_cds.model.CdsAcquisitionPassStatus.mget_by_ids")
def test_cds_acquisition_pass_status_timeliness_calculation(
    mock_mget_by_ids, raw_data_aps_product
):
    """Check consolidation of weekly aps product raw data"""

    mock_mget_by_ids.return_value = [None]

    XBandAcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = XBandAcquisitionPassStatusConsolidatorEngine(args=None)

    consolidated_document = engine.consolidate(
        raw_data_aps_product, CdsAcquisitionPassStatus()
    )

    consolidated_document.full_clean()
    result = consolidated_document.to_dict()

    assert result["antenna_id"] == "ABCD"
    assert result["antenna_status"] == "EFGH"
    assert result["delivery_push_status"] == "IJKL"
    assert result["downlink_orbit"] == "MNOPQZ"
    assert result["doy"] == 1234
    assert result["fer_data"] == 5678.9
    assert result["fer_downlink"] == 1234.5
    assert result["front_end_id"] == "QRST"
    assert result["front_end_status"] == "UVWX"
    assert result["ground_station"] == "YZAB"
    assert result["last_frame_stop"] == "2001-06-08T13:42:42.100Z"
    assert result["mission"] == "GHIJ"
    assert result["notes"] == "KLMN"
    assert result["number_of_chunks"] == 9876
    assert result["overall_data_volume"] == 456456
    assert result["overall_number_of_bad_data_acquired_frames"] == 123123
    assert result["overall_number_of_bad_downlinked_frames"] == 789789
    assert result["overall_number_of_data_acquired_frames"] == 13311331
    assert result["overall_number_of_downlinked_frames"] == 45454545
    assert result["planned_data_start"] == "2001-02-02T10:42:42.100Z"
    assert result["planned_data_stop"] == "2011-11-09T05:10:10.110Z"
    assert result["satellite_id"] == "AZOPQZ"
    assert result["start_delivery"] == "2020-05-06T08:12:32.100Z"
    assert result["report_type"] == "daily"
    assert result["report_name_daily"] == "firstpart_secondpart"
    assert result["first_frame_start"] == "2021-06-07T02:21:15.100Z"
    assert result["stop_delivery"] == "2021-06-07T03:23:45.100Z"
    assert (
        result["from_acq_delivery_timeliness"] == (1 * 60 * 60 + 2 * 60 + 30) * 1000000
    )
    assert (
        result["delivery_bitrate"] == 456456 / (1 * 60 * 60 + 2 * 60 + 30)
    )
    assert "report_name_weekly" not in result
    assert "report_name_monthly" not in result
