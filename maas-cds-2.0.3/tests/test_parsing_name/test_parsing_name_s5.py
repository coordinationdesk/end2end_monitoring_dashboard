from unittest.mock import patch, ANY
from maas_cds.lib.parsing_name.parsing_name_s5 import extract_data_from_product_name_s5
from maas_model import datestr_to_utc_datetime

# "S5P_NRTI_L2__AER_LH_20220401T203521_20220401T204021_23146_02_020301_20220401T213615.XXX",
# "S5P_NRTI_L2__AER_LH_20220401T203521_20220401T204021_23146_02_020301_INVALID1T213615.XXX",
# "S5P_OFFL_L2__NP_BD6_20220401T194416_20220401T212547_23146_02_010300_20220403T093437.XXX",


def test_s5_product_name_nrti():
    product_name = "S5P_NRTI_L2__AER_LH_20220401T203521_20220401T204021_23146_02_020301_20220401T213615.XXX"

    expected_result = {
        "mission": "S5",
        "satellite_unit": "S5P",
        "timeliness": "NRTI",
        "product_type": "NRTI_L2__AER_LH",
        "product_level": "L2_",
        "start_sensing_time": datestr_to_utc_datetime("20220401T203521"),
        "end_sensing_time": datestr_to_utc_datetime("20220401T204021"),
        "absolute_orbit_number": "23146",
        "collection_number": "02",
        "processor_version": "020301",
        "production_start_date": datestr_to_utc_datetime("20220401T213615"),
        "datatake_id": "S5P-23146",
    }

    result = extract_data_from_product_name_s5(product_name)

    assert result == expected_result


@patch("logging.Logger.warning")
def test_s5_product_name_invalid(logger_mock):
    product_name = "S5P_NRTI_L2__AER_LH_20220401T203521_20220401T204021_23146_02_020301_INVALID1T213615.XXX"

    expected_result = {
        "mission": "S5",
        "satellite_unit": "S5P",
        "timeliness": "NRTI",
        "product_type": "NRTI_L2__AER_LH",
        "start_sensing_time": datestr_to_utc_datetime("20220401T203521"),
        "end_sensing_time": datestr_to_utc_datetime("20220401T204021"),
        "absolute_orbit_number": "23146",
        "collection_number": "02",
        "processor_version": "020301",
    }

    result = extract_data_from_product_name_s5(product_name)
    logger_mock.assert_called_with(
        "Failed to extract data from S5 name %s: %s",
        product_name,
        ANY,
    )

    assert result == expected_result


def test_s5_product_name_offl_l1a():
    product_name = "S5P_OFFL_L1A_NP_BD6_20220401T194416_20220401T212547_23146_02_010300_20220403T093437.XXX"

    expected_result = {
        "mission": "S5",
        "satellite_unit": "S5P",
        "timeliness": "OFFL",
        "product_type": "OFFL_L1A_NP_BD6",
        "product_level": "L1A",
        "start_sensing_time": datestr_to_utc_datetime("20220401T194416"),
        "end_sensing_time": datestr_to_utc_datetime("20220401T212547"),
        "absolute_orbit_number": "23146",
        "collection_number": "02",
        "processor_version": "010300",
        "production_start_date": datestr_to_utc_datetime("20220403T093437"),
        "datatake_id": "S5P-23146",
    }

    result = extract_data_from_product_name_s5(product_name)

    assert result == expected_result


def test_s5_product_name_no_product_level():
    product_name = (
        "S5P_NRTI_AUX_MET_2D_20220525T030000_20220526T120000_20220524T120000.nc"
    )

    expected_result = {
        "mission": "S5",
        "satellite_unit": "S5P",
        "timeliness": "NRTI",
        "product_type": "NRTI_AUX_MET_2D",
        "product_level": "L__",
        "start_sensing_time": datestr_to_utc_datetime("20220525T030000"),
        "end_sensing_time": datestr_to_utc_datetime("20220526T120000"),
        "production_start_date": datestr_to_utc_datetime("20220524T120000"),
    }

    result = extract_data_from_product_name_s5(product_name)

    assert result == expected_result
