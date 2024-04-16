# pylint: disable=redefined-outer-name

""" Tests for ddp_consolidation engine"""
import hashlib
from unittest.mock import patch
import copy
from maas_cds.model.generated import ApsEdrs
import pytest
import maas_cds.model as model

from maas_cds.engines.reports.acquisition_pass_status_s5_edrs import (
    EDRSAcquisitionPassStatusConsolidatorEngine,
    S5AcquisitionPassStatusConsolidatorEngine,
)


@pytest.fixture
def raw_data_aps_product_daily():
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
        "first_frame_start": "1999-08-09T14:51:40.100Z",
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


@pytest.fixture
def raw_data_aps_product_weekly():
    """APSProduct raw data fixture ( report type weekly)

    Returns:
        (APSProduct): raw data APS product
    """
    data_dict = {
        "reportName": "firstpart_secondpart",
        "antenna_id": "ABCDE",
        "antenna_status": "EFGHI",
        "delivery_push_status": "IJKLM",
        "downlink_orbit": "MNOPQZ",
        "doy": 12345,
        "fer_data": 56789.9,
        "fer_downlink": 12345.5,
        "first_frame_start": "1998-08-09T14:51:40.100Z",
        "front_end_id": "QRSTU",
        "front_end_status": "UVWXY",
        "ground_station": "YZAB",
        "interface_name": "CDEFG",
        "last_frame_stop": "1901-06-08T13:42:42.100Z",
        "mission": "GHIJK",
        "notes": "KLMNO",
        "number_of_chunks": 98767,
        "overall_data_volume": 4564567,
        "overall_number_of_bad_data_acquired_frames": 1231234,
        "overall_number_of_bad_downlinked_frames": 7897891,
        "overall_number_of_data_acquired_frames": 133113312,
        "overall_number_of_downlinked_frames": 454545456,
        "planned_data_start": "2001-02-02T10:42:42.100Z",
        "planned_data_stop": "2011-12-09T04:10:10.110Z",
        "production_service_name": "PQRST",
        "production_service_type": "TUVWX",
        "reportFolder": "XYXYZ",
        "satellite_id": "AZOPQZ",
        "start_delivery": "2020-05-06T08:11:32.100Z",
        "stop_delivery": "2021-06-07T03:21:45.100Z",
        "report_type": "weekly",
    }
    raw_document = model.ApsProduct(**data_dict)
    raw_document.meta.id = "ABCDEFGH454545456"
    raw_document.full_clean()
    return raw_document


@pytest.fixture
def raw_data_aps_product_monthly():
    """APSProduct raw data fixture ( report type monthly)

    Returns:
        (APSProduct): raw data APS product
    """
    data_dict = {
        "reportName": "firstpart_secondpart",
        "antenna_id": "ABCDEZ",
        "antenna_status": "EFGHIZ",
        "delivery_push_status": "IJKLMZ",
        "downlink_orbit": "MNOPQZ",
        "doy": 123459,
        "fer_data": 56789.9,
        "fer_downlink": 12345.59,
        "first_frame_start": "1998-08-09T14:51:40.101Z",
        "front_end_id": "QRSTUZ",
        "front_end_status": "UVWXYZ",
        "ground_station": "YZAB",
        "interface_name": "CDEFGZ",
        "last_frame_stop": "1901-06-08T13:42:42.101Z",
        "mission": "GHIJKZ",
        "notes": "KLMNOZ",
        "number_of_chunks": 987679,
        "overall_data_volume": 45645679,
        "overall_number_of_bad_data_acquired_frames": 12312349,
        "overall_number_of_bad_downlinked_frames": 78978919,
        "overall_number_of_data_acquired_frames": 1331133129,
        "overall_number_of_downlinked_frames": 4545454569,
        "planned_data_start": "2001-02-02T10:42:42.100Z",
        "planned_data_stop": "2011-12-09T04:10:10.111Z",
        "production_service_name": "PQRSTZ",
        "production_service_type": "TUVWXZ",
        "reportFolder": "XYXYZZ",
        "satellite_id": "AZOPQZ",
        "start_delivery": "2020-05-06T08:11:32.101Z",
        "stop_delivery": "2021-06-07T03:21:45.101Z",
        "report_type": "monthly",
    }
    raw_document = model.ApsProduct(**data_dict)
    raw_document.meta.id = "ABCDEFGH4545454561"
    raw_document.full_clean()
    return raw_document


@pytest.fixture
def cds_acquisition_pass_status():
    """Consolidated cds_acquisition_pass_status

    Returns:
        (CdsAcquisitionPassStatus): consolidated data
    """
    data_dict = {
        "antenna_id": "PARAM1",
        "antenna_status": "PARAM2",
        "cams_description": "PARAM3",
        "cams_origin": "PARAM4",
        "cams_tickets": "PARAM5",
        "delivery_push_status": "PARAM6",
        "downlink_orbit": "PARAM7",
        "doy": 8,
        "fer_data": 9,
        "fer_downlink": 10.1,
        "first_frame_start": "2001-02-02T10:42:42.099Z",
        "front_end_id": "PARAM12",
        "front_end_status": "PARAM13",
        "ground_station": "PARAM14",
        "last_attached_ticket": "PARAM15",
        "last_attached_ticket_url": "PARAM16",
        "last_frame_stop": "2001-02-02T10:42:42.100Z",
        "mission": "PARAM18",
        "notes": "PARAM19",
        "number_of_chunks": 20,
        "overall_data_volume": 21,
        "overall_number_of_bad_data_acquired_frames": 22,
        "overall_number_of_bad_downlinked_frames": 23,
        "overall_number_of_data_acquired_frames": 24,
        "overall_number_of_downlinked_frames": 25,
        "planned_data_start": "2001-02-02T10:42:42.101Z",
        "planned_data_stop": "2001-02-02T10:42:42.102Z",
        "report_name_daily": "PARAM28",
        "report_name_monthly": "PARAM29",
        "report_name_weekly": "PARAM30",
        "report_type": "daily",
        "satellite_id": "PARAM32",
        "start_delivery": "2001-02-02T10:42:42.103Z",
        "stop_delivery": "2001-02-02T10:42:42.104Z",
    }
    raw_document = model.CdsAcquisitionPassStatus(**data_dict)
    raw_document.meta.id = "ABCDEFGH4545454561"
    raw_document.full_clean()
    return raw_document


@pytest.fixture
def cds_acquisition_pass_status_weekly(raw_data_aps_product_weekly):
    """Consolidated cds_acquisition_pass_status

    Returns:
        (CdsAcquisitionPassStatus): consolidated data
    """

    data_dict = raw_data_aps_product_weekly.to_dict()
    raw_document = model.CdsAcquisitionPassStatus(**data_dict)
    raw_document.meta.id = "ABCDEFGH4545454561"
    raw_document.full_clean()
    return raw_document


@pytest.fixture
def cds_acquisition_pass_status_daily(raw_data_aps_product_daily):
    """Consolidated cds_acquisition_pass_status

    Returns:
        (CdsAcquisitionPassStatus): consolidated data
    """
    data_dict = raw_data_aps_product_daily.to_dict()
    raw_document = model.CdsAcquisitionPassStatus(**data_dict)
    raw_document.meta.id = "ABCDEFGH4545454561"
    raw_document.full_clean()
    return raw_document


@pytest.fixture
def raw_data_aps_edrs():
    """APSEdrs raw data fixture

    Returns:
        (APSEdrs): raw data APS EDRS
    """
    data_dict = {
        "link_session_id": "ABC",
        "geo_satellite_id": "DEF",
        "satellite_id": "GHI",
        "mission": "JKL",
        "doy": 123,
        "planned_link_session_start": "1999-08-09T14:51:40.100Z",
        "planned_link_session_stop": "1999-09-09T14:51:40.100Z",
        "moc_accept_status": "MNO",
        "uplink_status": "PQR",
        "spacecraft_execution": "STU",
        "edte_acquisition_status": "VWX",
        "dcsu_archive_status": "YZA",
        "sfdap_dissem_status": "BCD",
        "ground_station": "EFG",
        "dissemination_start": "1999-10-11T14:51:40.100Z",
        "dissemination_stop": "1999-11-12T14:51:40.100Z",
        "cadus": 45670000,
        "fer": 891000000,
        "archived_data_size": 12.3,
        "disseminated_data": 45.6,
        "notes": "HIJ",
        "interface_name": "KLM",
        "production_service_type": "OPQ",
        "production_service_name": "RST",
        "report_type": "daily",
        "reportName": "reportNameEDRS",
    }
    raw_document = model.ApsEdrs(**data_dict)
    raw_document.meta.id = "ABCDEFGH4545454561"
    raw_document.full_clean()
    return raw_document


@pytest.fixture
def cds_edrs_acquisition_pass_status(raw_data_aps_edrs):
    """Consolidated cds_edrs_acquisition_pass_status_daily

    Returns:
        (CdsEdrsAcquisitionPassStatus): consolidated data
    """
    data_dict = raw_data_aps_edrs.to_dict()
    raw_document = model.CdsEdrsAcquisitionPassStatus(**data_dict)
    raw_document.meta.id = "ABCDEFGH4545454561"
    raw_document.full_clean()
    return raw_document


# Auto mock all tests with the following mock
@pytest.fixture(autouse=True)
def mock_populate_ticket_cache(monkeypatch):
    monkeypatch.setattr(
        "maas_cds.engines.reports.anomaly_impact.AnomalyImpactMixinEngine._populate_ticket_cache",
        lambda *args: None,
    )


@patch("maas_cds.model.CdsAcquisitionPassStatus.mget_by_ids")
def test_s5_aps_product_consolidation_daily(
    mock_mget_by_ids, raw_data_aps_product_daily
):
    """Check consolidation of daily aps product raw data"""

    mock_mget_by_ids.return_value = [None]

    S5AcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = S5AcquisitionPassStatusConsolidatorEngine()

    consolidated_documents = engine.consolidate_from_raw_data(
        [raw_data_aps_product_daily]
    )

    consolidated_documents[0].full_clean()
    result = consolidated_documents[0].to_dict()

    md5 = hashlib.md5()
    for name in [
        "satellite_id",
        "downlink_orbit",
        "planned_data_start",
        "antenna_id",
    ]:
        md5.update(str(raw_data_aps_product_daily[name]).encode())

    assert consolidated_documents[0].meta.id == md5.hexdigest()

    assert result["antenna_id"] == "ABCD"
    assert result["antenna_status"] == "EFGH"
    assert result["delivery_push_status"] == "IJKL"
    assert result["downlink_orbit"] == "MNOPQZ"
    assert result["doy"] == 1234
    assert result["fer_data"] == 5678.9
    assert result["fer_downlink"] == 1234.5
    assert result["first_frame_start"] == "1999-08-09T14:51:40.100Z"
    assert result["front_end_id"] == "QRST"
    assert result["front_end_status"] == "UVWX"
    assert result["ground_station"] == "firstpart"
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
    assert result["stop_delivery"] == "2021-06-07T03:23:45.100Z"
    assert result["report_type"] == "daily"
    assert result["report_name_daily"] == "firstpart_secondpart"
    assert "report_name_weekly" not in result
    assert "report_name_monthly" not in result


@patch("maas_cds.model.CdsAcquisitionPassStatus.mget_by_ids")
def test_s5_aps_product_consolidation_weekly(
    mock_mget_by_ids, raw_data_aps_product_weekly
):
    """Check consolidation of weekly aps product raw data"""

    mock_mget_by_ids.return_value = [None]

    S5AcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = S5AcquisitionPassStatusConsolidatorEngine()

    consolidated_documents = engine.consolidate_from_raw_data(
        [raw_data_aps_product_weekly]
    )

    consolidated_documents[0].full_clean()
    result = consolidated_documents[0].to_dict()

    md5 = hashlib.md5()
    for name in [
        "satellite_id",
        "downlink_orbit",
        "planned_data_start",
        "antenna_id",
    ]:
        md5.update(str(raw_data_aps_product_weekly[name]).encode())

    assert consolidated_documents[0].meta.id == md5.hexdigest()

    assert result["antenna_id"] == "ABCDE"
    assert result["antenna_status"] == "EFGHI"
    assert result["delivery_push_status"] == "IJKLM"
    assert result["downlink_orbit"] == "MNOPQZ"
    assert result["doy"] == 12345
    assert result["fer_data"] == 56789.9
    assert result["fer_downlink"] == 12345.5
    assert result["first_frame_start"] == "1998-08-09T14:51:40.100Z"
    assert result["front_end_id"] == "QRSTU"
    assert result["front_end_status"] == "UVWXY"
    assert result["ground_station"] == "firstpart"
    assert result["last_frame_stop"] == "1901-06-08T13:42:42.100Z"
    assert result["mission"] == "GHIJK"
    assert result["notes"] == "KLMNO"
    assert result["number_of_chunks"] == 98767
    assert result["overall_data_volume"] == 4564567
    assert result["overall_number_of_bad_data_acquired_frames"] == 1231234
    assert result["overall_number_of_bad_downlinked_frames"] == 7897891
    assert result["overall_number_of_data_acquired_frames"] == 133113312
    assert result["overall_number_of_downlinked_frames"] == 454545456
    assert result["planned_data_start"] == "2001-02-02T10:42:42.100Z"
    assert result["planned_data_stop"] == "2011-12-09T04:10:10.110Z"
    assert result["satellite_id"] == "AZOPQZ"
    assert result["start_delivery"] == "2020-05-06T08:11:32.100Z"
    assert result["stop_delivery"] == "2021-06-07T03:21:45.100Z"
    assert result["report_type"] == "weekly"
    assert result["report_name_weekly"] == "firstpart_secondpart"
    assert "report_name_daily" not in result
    assert "report_name_monthly" not in result


@patch("maas_cds.model.CdsAcquisitionPassStatus.mget_by_ids")
def test_s5_aps_product_consolidation_monthly(
    mock_mget_by_ids, raw_data_aps_product_monthly
):
    """Check consolidation of monthly aps product raw data"""

    mock_mget_by_ids.return_value = [None]

    S5AcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = S5AcquisitionPassStatusConsolidatorEngine()

    consolidated_documents = engine.consolidate_from_raw_data(
        [raw_data_aps_product_monthly]
    )

    consolidated_documents[0].full_clean()
    result = consolidated_documents[0].to_dict()

    md5 = hashlib.md5()
    for name in [
        "satellite_id",
        "downlink_orbit",
        "planned_data_start",
        "antenna_id",
    ]:
        md5.update(str(raw_data_aps_product_monthly[name]).encode())

    assert consolidated_documents[0].meta.id == md5.hexdigest()

    assert result["antenna_id"] == "ABCDEZ"
    assert result["antenna_status"] == "EFGHIZ"
    assert result["delivery_push_status"] == "IJKLMZ"
    assert result["downlink_orbit"] == "MNOPQZ"
    assert result["doy"] == 123459
    assert result["fer_data"] == 56789.9
    assert result["fer_downlink"] == 12345.59
    assert result["first_frame_start"] == "1998-08-09T14:51:40.101Z"
    assert result["front_end_id"] == "QRSTUZ"
    assert result["front_end_status"] == "UVWXYZ"
    assert result["ground_station"] == "firstpart"
    assert result["last_frame_stop"] == "1901-06-08T13:42:42.101Z"
    assert result["mission"] == "GHIJKZ"
    assert result["notes"] == "KLMNOZ"
    assert result["number_of_chunks"] == 987679
    assert result["overall_data_volume"] == 45645679
    assert result["overall_number_of_bad_data_acquired_frames"] == 12312349
    assert result["overall_number_of_bad_downlinked_frames"] == 78978919
    assert result["overall_number_of_data_acquired_frames"] == 1331133129
    assert result["overall_number_of_downlinked_frames"] == 4545454569
    assert result["planned_data_start"] == "2001-02-02T10:42:42.100Z"
    assert result["planned_data_stop"] == "2011-12-09T04:10:10.111Z"
    assert result["satellite_id"] == "AZOPQZ"
    assert result["start_delivery"] == "2020-05-06T08:11:32.101Z"
    assert result["stop_delivery"] == "2021-06-07T03:21:45.101Z"
    assert result["report_type"] == "monthly"
    assert result["report_name_monthly"] == "firstpart_secondpart"
    assert "report_name_weekly" not in result
    assert "report_name_daily" not in result


@patch("maas_cds.model.CdsAcquisitionPassStatus.mget_by_ids")
def test_s5_aps_product_consolidation_check_daily_override_daily(
    mock_mget_by_ids, raw_data_aps_product_daily, cds_acquisition_pass_status
):
    """Check that when a daily aps product raw data is received and there is
    already a daily with the same id , a consolidated data is generated which
    will override the existing one
    """

    mocked_data = copy.deepcopy(cds_acquisition_pass_status)
    mocked_data["report_type"] = "daily"

    mock_mget_by_ids.return_value = [mocked_data]

    S5AcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = S5AcquisitionPassStatusConsolidatorEngine()

    consolidated_documents = engine.consolidate_from_raw_data(
        [raw_data_aps_product_daily]
    )

    assert len(consolidated_documents) == 1


@patch("maas_cds.model.CdsAcquisitionPassStatus.mget_by_ids")
def test_s5_aps_product_consolidation_check_weekly_override_daily(
    mock_mget_by_ids, raw_data_aps_product_weekly, cds_acquisition_pass_status
):
    """Check that when a weekly aps product raw data is received and there is
    already a daily with the same id, a consolidated data is generated which
    will override the existing one
    """

    mocked_data = copy.deepcopy(cds_acquisition_pass_status)
    mocked_data["report_type"] = "daily"

    mock_mget_by_ids.return_value = [mocked_data]

    S5AcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = S5AcquisitionPassStatusConsolidatorEngine()

    consolidated_documents = engine.consolidate_from_raw_data(
        [raw_data_aps_product_weekly]
    )

    assert len(consolidated_documents) == 1


@patch("maas_cds.model.CdsAcquisitionPassStatus.mget_by_ids")
def test_s5_aps_product_consolidation_check_monthly_override_daily(
    mock_mget_by_ids, raw_data_aps_product_monthly, cds_acquisition_pass_status
):
    """Check that when a monthly aps product raw data is received and there is
    already a weekly with the same id, a consolidated data is generated which
    will override the existing one
    """

    mocked_data = copy.deepcopy(cds_acquisition_pass_status)
    mocked_data["report_type"] = "daily"

    mock_mget_by_ids.return_value = [mocked_data]

    S5AcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = S5AcquisitionPassStatusConsolidatorEngine()

    consolidated_documents = engine.consolidate_from_raw_data(
        [raw_data_aps_product_monthly]
    )

    assert len(consolidated_documents) == 1


@patch("maas_cds.model.CdsAcquisitionPassStatus.mget_by_ids")
def test_s5_aps_product_consolidation_check_weekly_override_weekly(
    mock_mget_by_ids, raw_data_aps_product_weekly, cds_acquisition_pass_status
):
    """Check that when a weekly aps product raw data is received and there is
    already a weekly with the same id, a consolidated data is generated which
    will override the existing one
    """

    mocked_data = copy.deepcopy(cds_acquisition_pass_status)
    mocked_data["report_type"] = "weekly"

    mock_mget_by_ids.return_value = [mocked_data]

    S5AcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = S5AcquisitionPassStatusConsolidatorEngine()

    consolidated_documents = engine.consolidate_from_raw_data(
        [raw_data_aps_product_weekly]
    )

    assert len(consolidated_documents) == 1


@patch("maas_cds.model.CdsAcquisitionPassStatus.mget_by_ids")
def test_s5_aps_product_consolidation_check_monthly_override_weekly(
    mock_mget_by_ids, raw_data_aps_product_monthly, cds_acquisition_pass_status
):
    """Check that when a monthly aps product raw data is received and there is
    already a weekly with the same id, a consolidated data is generated which
    will override the existing one
    """

    mocked_data = copy.deepcopy(cds_acquisition_pass_status)
    mocked_data["report_type"] = "weekly"

    mock_mget_by_ids.return_value = [mocked_data]

    S5AcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = S5AcquisitionPassStatusConsolidatorEngine()

    consolidated_documents = engine.consolidate_from_raw_data(
        [raw_data_aps_product_monthly]
    )

    assert len(consolidated_documents) == 1


@patch("maas_cds.model.CdsAcquisitionPassStatus.mget_by_ids")
def test_s5_aps_product_consolidation_check_daily_weekly_report_concatenation(
    mock_mget_by_ids, raw_data_aps_product_weekly, cds_acquisition_pass_status
):
    """Check that when a weekly aps product raw data is received and there is
    already a daily with the same id, the data of the daily are overwritten
    and the field report_name_weekly is filled and report_name_daily is kept"""

    mocked_data = copy.deepcopy(cds_acquisition_pass_status)
    mocked_data["report_type"] = "daily"
    mocked_data["report_name_daily"] = "UT_DAILY_REPORT_NAME_DAILY"
    mocked_data["report_name_weekly"] = ""
    mocked_data["report_name_monthly"] = ""
    mocked_data["antenna_id"] = "DAILY_ANTENNA_ID"

    mock_mget_by_ids.return_value = [mocked_data]

    S5AcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = S5AcquisitionPassStatusConsolidatorEngine()

    consolidated_documents = engine.consolidate_from_raw_data(
        [raw_data_aps_product_weekly]
    )

    assert (
        consolidated_documents[0]["report_name_daily"] == "UT_DAILY_REPORT_NAME_DAILY"
    )
    assert consolidated_documents[0]["report_name_weekly"] == "firstpart_secondpart"
    assert consolidated_documents[0]["report_name_monthly"] == ""
    assert consolidated_documents[0]["antenna_id"] == "ABCDE"


@patch("maas_cds.model.CdsAcquisitionPassStatus.mget_by_ids")
def test_s5_aps_product_consolidation_check_daily_monthly_report_concatenation(
    mock_mget_by_ids, raw_data_aps_product_monthly, cds_acquisition_pass_status
):
    """Check that when a monthly aps product raw data is received and there is
    already a daily with the same id, the data of the daily are overwritten
    and the field report_name_monthly is filled and report_name_daily is kept"""

    mocked_data = copy.deepcopy(cds_acquisition_pass_status)
    mocked_data["report_type"] = "daily"
    mocked_data["report_name_daily"] = "UT_DAILY_REPORT_NAME_DAILY"
    mocked_data["report_name_weekly"] = ""
    mocked_data["report_name_monthly"] = ""
    mocked_data["antenna_id"] = "DAILY_ANTENNA_ID"

    mock_mget_by_ids.return_value = [mocked_data]

    S5AcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = S5AcquisitionPassStatusConsolidatorEngine()

    consolidated_documents = engine.consolidate_from_raw_data(
        [raw_data_aps_product_monthly]
    )

    assert consolidated_documents[0]["antenna_id"] == "ABCDEZ"
    assert (
        consolidated_documents[0]["report_name_daily"] == "UT_DAILY_REPORT_NAME_DAILY"
    )
    assert consolidated_documents[0]["report_name_monthly"] == "firstpart_secondpart"
    assert consolidated_documents[0]["report_name_weekly"] == ""


@patch("maas_cds.model.CdsAcquisitionPassStatus.mget_by_ids")
def test_s5_aps_product_consolidation_check_weekly_monthly_report_concatenation(
    mock_mget_by_ids, raw_data_aps_product_monthly, cds_acquisition_pass_status
):
    """Check that when a monthly aps product raw data is received and there is
    already a weekly with the same id, the data of the weekly are overwritten
    and the field report_name_monthly is filled and report_name_weekly is kept"""

    mocked_data = copy.deepcopy(cds_acquisition_pass_status)
    mocked_data["report_type"] = "weekly"
    mocked_data["report_name_daily"] = ""
    mocked_data["report_name_weekly"] = "UT_WEEKLY_REPORT_NAME_WEEKLY"
    mocked_data["report_name_monthly"] = ""
    mocked_data["antenna_id"] = "WEEKLY_ANTENNA_ID"

    mock_mget_by_ids.return_value = [mocked_data]

    S5AcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = S5AcquisitionPassStatusConsolidatorEngine()

    consolidated_documents = engine.consolidate_from_raw_data(
        [raw_data_aps_product_monthly]
    )

    assert consolidated_documents[0]["antenna_id"] == "ABCDEZ"
    assert consolidated_documents[0]["report_name_daily"] == ""
    assert consolidated_documents[0]["report_name_monthly"] == "firstpart_secondpart"
    assert (
        consolidated_documents[0]["report_name_weekly"]
        == "UT_WEEKLY_REPORT_NAME_WEEKLY"
    )


@patch("maas_cds.model.CdsAcquisitionPassStatus.mget_by_ids")
def test_s5_aps_product_consolidation_check_daily_weekly_merge(
    mock_mget_by_ids, raw_data_aps_product_daily, cds_acquisition_pass_status_daily
):
    """Check that when a daily aps product raw data is received and there is
    already a weekly with the same id in db, the
    report_name_daily field of the document in db is updated but not the rest of the data
    """

    mocked_data = copy.deepcopy(cds_acquisition_pass_status_daily)
    mocked_data["ground_station"] = raw_data_aps_product_daily["reportName"].split("_")[
        0
    ]
    mocked_data["report_type"] = "weekly"
    mocked_data["report_name_monthly"] = ""
    mocked_data["report_name_daily"] = ""
    mocked_data["report_name_weekly"] = "RNWEEK"
    mocked_data["notes"] = "NOTEWEEK"

    mock_mget_by_ids.return_value = [mocked_data]

    S5AcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = S5AcquisitionPassStatusConsolidatorEngine()

    consolidated_documents = engine.consolidate_from_raw_data(
        [raw_data_aps_product_daily]
    )
    res = consolidated_documents[0].to_dict()

    for key, val in mocked_data.to_dict().items():
        assert res[key] == val

    assert res["report_name_daily"] == "firstpart_secondpart"
    assert res["report_name_weekly"] == "RNWEEK"


@patch("maas_cds.model.CdsAcquisitionPassStatus.mget_by_ids")
def test_s5_aps_product_consolidation_check_daily_monthly_merge(
    mock_mget_by_ids, raw_data_aps_product_daily, cds_acquisition_pass_status_daily
):
    """Check that when a daily aps product raw data is received and there is
    already a monthly with the same id in db, the
    report_name_daily field of the document in db is updated but not the rest of the data
    """

    mocked_data = copy.deepcopy(cds_acquisition_pass_status_daily)
    mocked_data["report_type"] = "monthly"
    mocked_data["ground_station"] = raw_data_aps_product_daily["reportName"].split("_")[
        0
    ]
    mocked_data["report_name_monthly"] = "RNMONTH"
    mocked_data["report_name_daily"] = ""
    mocked_data["report_name_weekly"] = ""
    mocked_data["notes"] = "NOTEMONTH"

    mock_mget_by_ids.return_value = [mocked_data]

    S5AcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = S5AcquisitionPassStatusConsolidatorEngine()

    consolidated_documents = engine.consolidate_from_raw_data(
        [raw_data_aps_product_daily]
    )
    res = consolidated_documents[0].to_dict()
    for key, val in mocked_data.to_dict().items():
        assert res[key] == val

    assert res["report_name_monthly"] == "RNMONTH"
    assert res["report_name_daily"] == "firstpart_secondpart"


@patch("maas_cds.model.CdsAcquisitionPassStatus.mget_by_ids")
def test_s5_aps_product_consolidation_check_weekly_monthly_merge(
    mock_mget_by_ids, raw_data_aps_product_weekly, cds_acquisition_pass_status_weekly
):
    """Check that when a weekly aps product raw data is received and there is
    already a monthly with the same id in db, the
    report_name_weekly field of the document in db is updated but not the rest of the data
    """

    mocked_data = copy.deepcopy(cds_acquisition_pass_status_weekly)
    mocked_data["ground_station"] = raw_data_aps_product_weekly["reportName"].split(
        "_"
    )[0]
    mocked_data["report_type"] = "monthly"
    mocked_data["report_name_monthly"] = "RNMONTH"
    mocked_data["report_name_weekly"] = ""
    mocked_data["report_name_daily"] = ""
    mocked_data["notes"] = "RNMONTH"

    mock_mget_by_ids.return_value = [mocked_data]

    S5AcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = S5AcquisitionPassStatusConsolidatorEngine()

    consolidated_documents = engine.consolidate_from_raw_data(
        [raw_data_aps_product_weekly]
    )
    res = consolidated_documents[0].to_dict()

    for key, val in mocked_data.to_dict().items():
        assert res[key] == val

    assert res["report_name_monthly"] == "RNMONTH"
    assert res["report_name_weekly"] == "firstpart_secondpart"


@patch("maas_cds.model.CdsEdrsAcquisitionPassStatus.mget_by_ids")
def test_edrs_aps_product_consolidation_daily(mock_mget_by_ids, raw_data_aps_edrs):
    """Check consolidation of aps EDRS product raw data (daily)"""

    mock_mget_by_ids.return_value = [None]

    EDRSAcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = EDRSAcquisitionPassStatusConsolidatorEngine()

    consolidated_documents = engine.consolidate_from_raw_data([raw_data_aps_edrs])

    md5 = hashlib.md5()
    for name in ["link_session_id", "ground_station"]:
        md5.update(str(raw_data_aps_edrs[name]).encode())

    assert consolidated_documents[0].meta.id == md5.hexdigest()
    res = consolidated_documents[0].to_dict()

    assert res["link_session_id"] == "ABC"
    assert res["geo_satellite_id"] == "DEF"
    assert res["satellite_id"] == "GHI"
    assert res["mission"] == "JKL"
    assert res["doy"] == 123
    assert res["planned_link_session_start"] == "1999-08-09T14:51:40.100Z"
    assert res["planned_link_session_stop"] == "1999-09-09T14:51:40.100Z"
    assert res["moc_accept_status"] == "MNO"
    assert res["uplink_status"] == "PQR"
    assert res["spacecraft_execution"] == "STU"
    assert res["edte_acquisition_status"] == "VWX"
    assert res["dcsu_archive_status"] == "YZA"
    assert res["sfdap_dissem_status"] == "BCD"
    assert res["ground_station"] == "EFG"
    assert res["dissemination_start"] == "1999-10-11T14:51:40.100Z"
    assert res["dissemination_stop"] == "1999-11-12T14:51:40.100Z"
    assert res["cadus"] == 45670000
    assert res["fer"] == 891000000
    assert res["archived_data_size"] == 12.3
    assert res["disseminated_data"] == 45.6
    assert res["notes"] == "HIJ"
    assert res["report_type"] == "daily"
    assert res["report_name_daily"] == "reportNameEDRS"
    assert "report_name_weekly" not in res
    assert "report_name_monthly" not in res


@patch("maas_cds.model.CdsEdrsAcquisitionPassStatus.mget_by_ids")
def test_edrs_aps_product_consolidation_weekly(mock_mget_by_ids, raw_data_aps_edrs):
    """Check consolidation of aps EDRS product raw data (weekly)"""

    mock_mget_by_ids.return_value = [None]

    EDRSAcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = EDRSAcquisitionPassStatusConsolidatorEngine()

    raw_data_aps_edrs.report_type = "weekly"
    consolidated_documents = engine.consolidate_from_raw_data([raw_data_aps_edrs])

    md5 = hashlib.md5()
    for name in ["link_session_id", "ground_station"]:
        md5.update(str(raw_data_aps_edrs[name]).encode())

    assert consolidated_documents[0].meta.id == md5.hexdigest()
    res = consolidated_documents[0].to_dict()

    assert res["link_session_id"] == "ABC"
    assert res["geo_satellite_id"] == "DEF"
    assert res["satellite_id"] == "GHI"
    assert res["mission"] == "JKL"
    assert res["doy"] == 123
    assert res["planned_link_session_start"] == "1999-08-09T14:51:40.100Z"
    assert res["planned_link_session_stop"] == "1999-09-09T14:51:40.100Z"
    assert res["moc_accept_status"] == "MNO"
    assert res["uplink_status"] == "PQR"
    assert res["spacecraft_execution"] == "STU"
    assert res["edte_acquisition_status"] == "VWX"
    assert res["dcsu_archive_status"] == "YZA"
    assert res["sfdap_dissem_status"] == "BCD"
    assert res["ground_station"] == "EFG"
    assert res["dissemination_start"] == "1999-10-11T14:51:40.100Z"
    assert res["dissemination_stop"] == "1999-11-12T14:51:40.100Z"
    assert res["cadus"] == 45670000
    assert res["fer"] == 891000000
    assert res["archived_data_size"] == 12.3
    assert res["disseminated_data"] == 45.6
    assert res["notes"] == "HIJ"
    assert res["report_type"] == "weekly"
    assert res["report_name_weekly"] == "reportNameEDRS"
    assert "report_name_daily" not in res
    assert "report_name_monthly" not in res


@patch("maas_cds.model.CdsEdrsAcquisitionPassStatus.mget_by_ids")
@patch("opensearchpy.Search.execute")
def test_edrs_aps_product_consolidation_with_missing_ground_station_db_test(
    mock_search, mock_mget_by_ids, raw_data_aps_edrs
):
    """Check that edrs try to retrieve its ground_data field by
    analysing other apsedrs already in db"""

    mock_mget_by_ids.return_value = [None]

    other_aps_product = ApsEdrs()
    other_aps_product.ground_station = "BFLGS"
    mock_search.return_value = [other_aps_product]

    EDRSAcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = EDRSAcquisitionPassStatusConsolidatorEngine()

    delattr(raw_data_aps_edrs, "ground_station")
    engine.input_documents = [raw_data_aps_edrs]
    consolidated_documents = engine.consolidate_from_raw_data([raw_data_aps_edrs])

    md5 = hashlib.md5()
    for name in ["ABC", "FLGS"]:  # link_session_id and ground station
        md5.update(str(name).encode())

    assert consolidated_documents[0].meta.id == md5.hexdigest()
    res = consolidated_documents[0].to_dict()
    assert res["ground_station"] == "FLGS"


@patch("maas_cds.model.CdsEdrsAcquisitionPassStatus.mget_by_ids")
def test_edrs_aps_product_consolidation_with_missing_ground_station_chunk_test(
    mock_mget_by_ids, raw_data_aps_edrs
):
    """Check that edrs try to retrieve its ground_data field by
    analysing other apsedrs in chunk"""

    mock_mget_by_ids.return_value = [None, None]

    EDRSAcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = EDRSAcquisitionPassStatusConsolidatorEngine()

    # Create a second raw document using the first one
    raw_data_aps_edrs_bis = copy.deepcopy(raw_data_aps_edrs)

    # Set ground station of second doc to RDGS, so we expect that our engine deduce
    # that the first one will be HDGS
    raw_data_aps_edrs_bis["ground_station"] = "RDGS"
    raw_data_aps_edrs_bis.meta.id = "other_id_key"

    deduced_ground_station = "HDGS"

    # Remove the ground_station from the first one
    delattr(raw_data_aps_edrs, "ground_station")

    engine.input_documents = [raw_data_aps_edrs, raw_data_aps_edrs_bis]
    consolidated_documents = engine.consolidate_from_raw_data(
        [raw_data_aps_edrs, raw_data_aps_edrs_bis]
    )

    md5 = hashlib.md5()
    for name in [raw_data_aps_edrs["link_session_id"], deduced_ground_station]:
        md5.update(str(name).encode())

    res = [x for x in consolidated_documents if x.meta.id == md5.hexdigest()]
    assert res[0]["ground_station"] == deduced_ground_station


@patch("maas_cds.model.CdsEdrsAcquisitionPassStatus.mget_by_ids")
def test_edrs_aps_product_consolidation_check_daily_weekly_merge(
    mock_mget_by_ids, raw_data_aps_edrs, cds_edrs_acquisition_pass_status
):
    """Check that when a daily edrs aps product raw data is received and there is
    already a weekly with the same id in db, the
    report_name_daily field of the document in db is updated but not the rest of the data
    """

    mocked_data = copy.deepcopy(cds_edrs_acquisition_pass_status)
    mocked_data["report_type"] = "weekly"
    mocked_data["report_name_weekly"] = "RNWEEK"
    mocked_data["report_name_daily"] = ""
    mocked_data["notes"] = "NOTESWEEK"
    mock_mget_by_ids.return_value = [mocked_data]

    EDRSAcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = EDRSAcquisitionPassStatusConsolidatorEngine()

    consolidated_documents = engine.consolidate_from_raw_data([raw_data_aps_edrs])
    res = consolidated_documents[0].to_dict()

    for key, val in mocked_data.to_dict().items():
        assert res[key] == val

    assert res["report_name_daily"] == "reportNameEDRS"
    assert res["report_name_weekly"] == "RNWEEK"


@patch("maas_cds.model.CdsEdrsAcquisitionPassStatus.mget_by_ids")
def test_edrs_aps_product_consolidation_check_daily_monthly_merge(
    mock_mget_by_ids, raw_data_aps_edrs, cds_edrs_acquisition_pass_status
):
    """Check that when a daily edrs aps product raw data is received and there is
    already a monthly with the same id, the
    report_name_daily field of the document in db is updated but not the rest of the data
    """

    mocked_data = copy.deepcopy(cds_edrs_acquisition_pass_status)
    mocked_data["report_type"] = "monthly"
    mocked_data["report_name_monthly"] = "RNMONTH"
    mocked_data["report_name_daily"] = ""
    mocked_data["notes"] = "NOTESMONTH"
    mock_mget_by_ids.return_value = [mocked_data]

    EDRSAcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = EDRSAcquisitionPassStatusConsolidatorEngine()

    consolidated_documents = engine.consolidate_from_raw_data([raw_data_aps_edrs])
    res = consolidated_documents[0].to_dict()

    for key, val in mocked_data.to_dict().items():
        assert res[key] == val

    assert res["report_name_daily"] == "reportNameEDRS"
    assert res["report_name_monthly"] == "RNMONTH"


@patch("maas_cds.model.CdsEdrsAcquisitionPassStatus.mget_by_ids")
def test_edrs_aps_product_consolidation_check_weekly_monthly_merge(
    mock_mget_by_ids, raw_data_aps_edrs, cds_edrs_acquisition_pass_status
):
    """Check that when a weekly edrs aps product raw data is received and there is
    already a monthly with the same id in db, the
    report_name_weekly field of the document in db is updated but not the rest of the data
    """

    raw_data_aps_edrs["report_type"] = "weekly"

    mocked_data = copy.deepcopy(cds_edrs_acquisition_pass_status)
    mocked_data["report_type"] = "monthly"
    mocked_data["report_name_monthly"] = "RNMONTH"
    mocked_data["report_name_weekly"] = ""
    mocked_data["notes"] = "NOTESWEEK"
    mock_mget_by_ids.return_value = [mocked_data]

    EDRSAcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
    engine = EDRSAcquisitionPassStatusConsolidatorEngine()

    consolidated_documents = engine.consolidate_from_raw_data([raw_data_aps_edrs])
    res = consolidated_documents[0].to_dict()

    for key, val in mocked_data.to_dict().items():
        assert res[key] == val

    assert res["report_name_weekly"] == "reportNameEDRS"
    assert res["report_name_monthly"] == "RNMONTH"


@patch("maas_cds.model.CdsEdrsAcquisitionPassStatus.get_by_id")
@patch("maas_cds.model.CdsEdrsAcquisitionPassStatus.mget_by_ids")
@patch("opensearchpy.Search.execute")
def test_edrs_deduce_ground_station_when_no_info_available(
    mock_search, mock_mget_by_ids, mock_get_by_id, raw_data_aps_edrs
):
    """Check that when we cannot deduce the ground station of a document using another
    document we try to guess it using the satellite id and create the document for
    the nominal and backup station
    """
    mock_search.return_value = []
    sat = ("S1A", "S1B", "S2A", "S2B")
    res_1 = ("RDGS", "RDGS", "FLGS", "FLGS")
    res_2 = ("HDGS", "HDGS", "BFLGS", "BFLGS")

    for i, sat_id in enumerate(sat):
        raw_data_aps_edrs["satellite_id"] = sat_id

        raw_data_aps_edrs_monthly = copy.deepcopy(raw_data_aps_edrs)
        raw_data_aps_edrs_monthly["report_type"] = "monthly"
        raw_data_aps_edrs_monthly["doy"] = 999

        # Remove the ground_station field
        delattr(raw_data_aps_edrs, "ground_station")
        delattr(raw_data_aps_edrs_monthly, "ground_station")

        mock_mget_by_ids.return_value = [None, None]
        mock_get_by_id.return_value = None

        EDRSAcquisitionPassStatusConsolidatorEngine.MODEL_MODULE = model
        engine = EDRSAcquisitionPassStatusConsolidatorEngine()
        engine.input_documents = [raw_data_aps_edrs]

        consolidated_documents = engine.consolidate_from_raw_data(
            [raw_data_aps_edrs_monthly, raw_data_aps_edrs]
        )

        # We ingested twice the same document except 1 is monthly and has a different doy
        # We check that only 2 document were created ( bak and nom station of monthly)
        assert len(consolidated_documents) == 2

        # Because of set() in engine code, we test both order
        assert (
            consolidated_documents[0]["ground_station"] == res_1[i]
            and consolidated_documents[1]["ground_station"] == res_2[i]
        ) or (
            consolidated_documents[1]["ground_station"] == res_1[i]
            and consolidated_documents[0]["ground_station"] == res_2[i]
        )

        for key, val in consolidated_documents[0].to_dict().items():
            if key not in ("ground_station", "updateTime"):
                assert consolidated_documents[1].to_dict()[key] == val

        assert consolidated_documents[0].report_type == "monthly"
        assert consolidated_documents[1].report_type == "monthly"

        assert (
            consolidated_documents[0].doy == 999
        )  # This check prove that the monthly has been taken into account
        assert consolidated_documents[1].doy == 999

        # Verify id
        for j in range(2):
            md5 = hashlib.md5()
            for name in ["link_session_id", "ground_station"]:
                md5.update(str(consolidated_documents[j][name]).encode())
            assert consolidated_documents[j].meta.id == md5.hexdigest()
