import datetime
from unittest.mock import patch
from maas_cds.model.datatake import CdsDatatake

from maas_cds.model.enumeration import CompletenessScope

from maas_cds.model.datatake_s1 import (
    CdsDatatakeS1,
)

from maas_cds.model import CdsProduct


def test_evaluate_all_global_expected(s1_datatake_wv):
    """test evaluate_all_global_expected"""

    setattr(s1_datatake_wv, "l0_sensing_duration", 20)
    setattr(s1_datatake_wv, "observation_duration", 30)

    global_expected = s1_datatake_wv.evaluate_all_global_expected()

    assert global_expected == {"sensing": 160}


def test_evaluate_all_global_expected_no_instrument_mode():
    """test evaluate_all_global_expected with unknow instrument"""
    datatake_doc = CdsDatatakeS1()

    datatake_doc.instrument_mode = "AA"

    setattr(datatake_doc, "l0_sensing_duration", 20)
    setattr(datatake_doc, "observation_duration", 30)

    global_expected = datatake_doc.evaluate_all_global_expected()

    assert global_expected == {}


def test_evaluate_all_global_expected_new_instrument_mode_zi():
    """test evaluate_all_global_expected with unknow instrument"""
    datatake_doc = CdsDatatakeS1()

    datatake_doc.instrument_mode = "ZI"

    setattr(datatake_doc, "l0_sensing_duration", 61627000)
    setattr(datatake_doc, "observation_duration", 60050000)

    global_expected = datatake_doc.evaluate_all_global_expected()

    assert global_expected == {"sensing": 61627000}


@patch("maas_cds.model.datatake_s1.CdsDatatakeS1.get_slc_1s_count")
@patch("maas_cds.model.datatake_s1.CdsDatatakeS1.find_brother_products_scan")
@patch("maas_cds.model.datatake_s1.CdsDatatakeS1.compute_local_value")
def test_bug_expected_wrong_value(
    mock_compute_local_value,
    mock_find_brother_products_scan,
    mock_get_slc_1s_count,
):
    mock_compute_local_value.side_effect = [
        30580000,
        30580000,
        30580000,
        30580000,
        29369000,
        29369000,
        29369000,
        29369000,
        0,
        0,
        0,
    ]

    mock_get_slc_1s_count.return_value = 1

    datatake_doc = CdsDatatakeS1(
        **{
            "name": "S1A_MP_ACQ__L0__20220406T160000_20220418T180000.csv",
            "key": "S1A-333628",
            "datatake_id": "333628",
            "satellite_unit": "S1A",
            "mission": "S1",
            "updateTime": "2022-04-08T14:13:24.020Z",
            "observation_time_start": datetime.datetime(
                2022, 4, 7, 12, 11, 39, 958000, tzinfo=datetime.timezone.utc
            ),
            "observation_duration": 30005000,
            "observation_time_stop": datetime.datetime(
                2022, 4, 7, 12, 12, 9, 963000, tzinfo=datetime.timezone.utc
            ),
            "l0_sensing_duration": 31600000,
            "l0_sensing_time_start": "2022-04-07T12:11:38.657Z",
            "l0_sensing_time_stop": "2022-04-07T12:12:10.257Z",
            "absolute_orbit": "42667",
            "relative_orbit": "70",
            "polarization": "DH",
            "timeliness": "NTC",
            "instrument_mode": "SM",
            "instrument_swath": "1",
            "application_date": "2022-04-06T16:00:00.000Z",
            "S1_RAW__0A_local_value": 30580000,
            "S1_RAW__0S_local_value": 30580000,
            "S1_RAW__0N_local_value": 30580000,
            "S1_RAW__0C_local_value": 30580000,
            "S1_GRDH_1A_local_value": 29369000,
            "S1_GRDH_1S_local_value": 29369000,
            "S1_SLC__1A_local_value": 29393000,
            "S1_SLC__1S_local_value": 29393000,
        }
    )

    datatake_doc.compute_all_local_completeness()
    datatake_doc.compute_global_completeness()

    expected_value = datatake_doc.get_expected_value(
        CompletenessScope.GLOBAL, "sensing"
    )

    assert expected_value == 252800000

    assert datatake_doc.sensing_global_value == 239796000


def test_completeness_tolerance():
    datatake_doc = CdsDatatakeS1(
        **{
            "name": "S1A_MP_ACQ__L0__20220406T160000_20220418T180000.csv",
            "key": "S1A-333628",
            "datatake_id": "333628",
            "satellite_unit": "S1A",
            "mission": "S1",
            "updateTime": "2022-04-08T14:13:24.020Z",
            "observation_time_start": "2022-04-07T12:11:39.958Z",
            "observation_duration": 30005000,
            "observation_time_stop": "2022-04-07T12:12:09.963Z",
            "l0_sensing_duration": 31600000,
            "l0_sensing_time_start": "2022-04-07T12:11:38.657Z",
            "l0_sensing_time_stop": "2022-04-07T12:12:10.257Z",
            "absolute_orbit": "42667",
            "relative_orbit": "70",
            "polarization": "DH",
            "timeliness": "NTC",
            "instrument_mode": "SM",
            "instrument_swath": "1",
            "application_date": "2022-04-06T16:00:00.000Z",
        }
    )
    datatake_doc.full_clean()

    completeness_tolerance = {
        "S1": {
            "global": 0,
            "local": {
                "WV.*0.": 759000,
                "WV.*1.": 13500000,
                "S.*0.": 1000000,
                "S.*1.": -2400000,
                "EW.*0.": 135000,
                "EW.*1.": 230000,
                "IW.*0.": 512000,
                "IW.*1.": 150000,
                ".*2.*": 0,
                "default": 0,
            },
        },
    }

    expected_value = datatake_doc.get_expected_from_product_type("S1_SLC__1A")

    assert expected_value == {"sensing": 31600000}

    # Add tolerance to see the diff
    CdsDatatake.COMPLETENESS_TOLERANCE = completeness_tolerance

    # negative tolerance
    expected_value = datatake_doc.get_expected_from_product_type("S1_SLC__1A")

    assert expected_value == {"sensing": 31600000 - 2400000}

    # positive tolerance
    expected_value = datatake_doc.get_expected_from_product_type("S1_SLC__0A")

    assert expected_value == {"sensing": 31600000 + 1000000}

    datatake_dict_action = datatake_doc.to_bulk_action()

    assert "completeness_tolerance" not in datatake_dict_action["_source"]

    # Reset completeness tolerance to not impact other test
    CdsDatatake.COMPLETENESS_TOLERANCE = {}


@patch("maas_cds.model.datatake_s1.CdsDatatakeS1.get_slc_1s_count")
@patch("maas_cds.model.datatake_s1.CdsDatatakeS1.find_brother_products_scan")
def test_evaluate_expected_over_specific_area_ocn(
    mock_find_brother_products_scan,
    mock_get_slc_1s_count,
    s1_datatake_ew,
    s1_products_ew_raw__0s_over_specific_area,
):
    """test evaluate all expected over specific area"""

    CdsDatatake.COMPLETENESS_TOLERANCE = {
        "S1": {
            "local": {
                "WV_.*0.": -759000,
                "WV_.*1.": -13500000,
                "WV_.*2.": -12843000,
                "S.*0.": -1000000,
                "S.*1.": -2400000,
                "S.*2.": -2000000,
                "EW_.*0.": -135000,
                "EW_.*1.": 230000,
                "IW_.*0.": -512000,
                "IW_.*1.": 150000,
            },
            "slice": {"IW_OCN__2.": -7400000, "EW_OCN__2.": -8400000},
        }
    }

    mock_find_brother_products_scan.return_value = (
        s1_products_ew_raw__0s_over_specific_area
    )
    mock_get_slc_1s_count.return_value = 1

    global_expected = s1_datatake_ew.evaluate_all_global_expected()

    assert global_expected == {"etad": 1, "sensing": 2370802000}

    all_product_expected = s1_datatake_ew.get_all_product_types()

    assert "EW_OCN__2S" in all_product_expected
    assert "EW_SLC__1S" in all_product_expected

    ocn_expected = s1_datatake_ew.get_expected_from_product_type("EW_OCN__2S")
    assert ocn_expected == {"sensing": 239199000}

    slc_expected = s1_datatake_ew.get_expected_from_product_type("EW_SLC__1S")
    assert slc_expected == {"sensing": 0}

    # Reset completeness tolerance to not impact other test
    CdsDatatake.COMPLETENESS_TOLERANCE = {}


@patch("maas_cds.model.datatake_s1.CdsDatatakeS1.find_brother_products_scan")
def test_get_expected_value_over_speficic_area(mock_find_brother_products_scan):
    product_prip = CdsProduct(
        **{
            "key": "9b644d15eefa49f35179175f90d2b729",
            "mission": "S1",
            "name": "S1B_OPER_REP__MACP__20160429T072531_20220615T224730_0001.TGZ",
            "product_level": "L__",
            "product_type": "REP__MACP_",
            "satellite_unit": "S1B",
            "sensing_start_date": "2016-04-29T07:25:31.000Z",
            "sensing_end_date": "2022-06-15T22:47:30.000Z",
            "sensing_duration": 193418519000000,
            "timeliness": "_",
            "prip_id": "5c7b36c8-ec8a-11ec-a1af-fa163e7968e5",
            "prip_publication_date": "2022-06-15T09:05:54.284Z",
            "updateTime": "2022-06-15T09:21:53.333Z",
        }
    )
    product_prip.full_clean()

    mock_find_brother_products_scan.return_value = [product_prip]

    datatake_doc = CdsDatatakeS1(
        **{
            "name": "S1A_MP_ACQ__L0__20220406T160000_20220418T180000.csv",
            "key": "S1A-333628",
            "datatake_id": "333628",
            "satellite_unit": "S1A",
            "mission": "S1",
            "updateTime": "2022-04-08T14:13:24.020Z",
            "observation_time_start": "2022-04-07T12:11:39.958Z",
            "observation_duration": 30005000,
            "observation_time_stop": "2022-04-07T12:12:09.963Z",
            "l0_sensing_duration": 31600000,
            "l0_sensing_time_start": "2022-04-07T12:11:38.657Z",
            "l0_sensing_time_stop": "2022-04-07T12:12:10.257Z",
            "absolute_orbit": "42667",
            "relative_orbit": "70",
            "polarization": "DH",
            "timeliness": "NTC",
            "instrument_mode": "SM",
            "instrument_swath": "1",
            "application_date": "2022-04-06T16:00:00.000Z",
        }
    )
    datatake_doc.full_clean()

    datatake_doc.get_expected_value_over_speficic_area("S1_OCN")  # fake value
