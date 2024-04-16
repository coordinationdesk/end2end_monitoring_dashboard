from unittest.mock import patch
from maas_cds.lib.parsing_name.parsing_name_s3 import extract_data_from_product_name_s3
from maas_model import datestr_to_utc_datetime

# "S3__AX___MF2_AX_20211215T120000_20211216T000000_20211215T060148___________________ECW_O_NR_001.SEN3.zip",
# "S3B_SR___ROE_AX_20211214T175244_20211214T193434_20211214T195247___________________LN3_O_NR____.SEN3.zip",
# "S3A_TM_0_NAT____20211214T151253_20211214T165228_20211214T165453_5974_079_339______LN3_O_AL_002.SEN3.zip",
# "S3A_GN_0_GNS____20211214T151252_20211214T165235_20211214T170215_5983_079_339______LN3_O_NR_002.SEN3.zip",
# "S3A_OL_0_EFR____20211214T154348_20211214T154548_20211214T170411_0119_079_339______LN1_O_NR_002.SEN3.zip",
# "S3A_MW_1_NIR_AX_20000101T000000_20211214T165225_20211214T171248___________________LN3_O_AL____.SEN3.zip",
# "S3B_OL_1_EFR____20211214T153000_20211214T153038_20211214T165214_0037_060_196_4680_LN1_O_NR_002",
# "S3__GN_1_GSVMAX_20211214T195947_20211214T201447_20211214T201638___________________LND_O_NR_001.SEN3.zip",
# "S3B_OL_1_EFR____20211214T152700_20211214T153000_20211214T165213_0179_060_196_4500_LN1_O_NR_002",
# "S3__GN_1_GSVMAX_20211215T065947_20211215T071447_20211215T071632___________________LND_O_NR_001.SEN3.zip"
# "S3A_SR_1_CA1SAX_20000101T000000_20211214T181842_20211214T184246___________________LN3_O_AL____.SEN3.zip",
# "S3__GN_1_NAV_AX_20211215T012918_20211215T072918_20211215T010216___________________LND_O_NR_001.SEN3.zip",
# "S3__GN_1_GSVMAX_20211214T185947_20211214T191447_20211214T191631___________________LND_O_NR_001.SEN3.zip",
# "S3__GN_1_GSVHAX_20211214T105947_20211216T105947_20211215T110113___________________LND_O_NR_001.SEN3.zip"
# "S3B_SY_2_VGP____20211214T025935_20211214T034343_20211214T091801_2648_060_189______LN2_O_ST_002",
# "S3A_SY_2_SYN____20211214T002428_20211214T002728_20211214T155957_0179_079_330_2520_LN2_O_ST_002",
# "S3B_SR_2_LAN____20211214T152018_20211214T152405_20211214T165111_0227_060_196______LN3_O_NR_004",
# "S3B_SR_2_NRPPAX_20211215T054413_20211215T072723_20211215T074246___________________LN3_O_NR____.SEN3.zip",


def test_s3_product_name_no_level_1():
    product_name = "S3__AX___MF2_AX_20211215T120000_20211216T000000_20211215T060148___________________ECW_O_NR_001.SEN3.zip"

    expected_result = {
        "mission": "S3",
        "satellite_unit": "S3_",
        "instrument": "AX",
        "product_level": "L__",
        "file_type_function": "MF2_AX",
        "product_type": "AX___MF2_AX",
        "start_sensing_time": datestr_to_utc_datetime("20211215T120000"),
        "end_sensing_time": datestr_to_utc_datetime("20211216T000000"),
        "creation_time": datestr_to_utc_datetime("20211215T060148"),
        "instance_id": "_________________",
        "centre": "ECW",
        "platform": "O",
        "timeliness": "NR",
        "baseline_collection": "001",
        "class_id": "O_NR_001",
    }

    result = extract_data_from_product_name_s3(product_name)

    assert result == expected_result


def test_s3_product_name_l0_1():
    product_name = "S3A_TM_0_NAT____20211214T151253_20211214T165228_20211214T165453_5974_079_339______LN3_O_AL_002.SEN3.zip"

    expected_result = {
        "mission": "S3",
        "satellite_unit": "S3A",
        "instrument": "TM",
        "product_level": "L0_",
        "file_type_function": "NAT___",
        "product_type": "TM_0_NAT___",
        "start_sensing_time": datestr_to_utc_datetime("20211214T151253"),
        "end_sensing_time": datestr_to_utc_datetime("20211214T165228"),
        "creation_time": datestr_to_utc_datetime("20211214T165453"),
        "instance_id": "5974_079_339_____",
        "relative_orbit_number": "339",
        "centre": "LN3",
        "platform": "O",
        "timeliness": "AL",
        "baseline_collection": "002",
        "class_id": "O_AL_002",
        "cycle_number": "079",
        "datatake_id": "S3A-079-339",
    }

    result = extract_data_from_product_name_s3(product_name)

    assert result == expected_result


def test_s3_product_name_l0_2():
    product_name = "S3B_SR___ROE_AX_20211214T175244_20211214T193434_20211214T195247___________________LN3_O_NR____.SEN3.zip"

    expected_result = {
        "mission": "S3",
        "satellite_unit": "S3B",
        "instrument": "SR",
        "product_level": "L__",
        "file_type_function": "ROE_AX",
        "product_type": "SR___ROE_AX",
        "start_sensing_time": datestr_to_utc_datetime("20211214T175244"),
        "end_sensing_time": datestr_to_utc_datetime("20211214T193434"),
        "creation_time": datestr_to_utc_datetime("20211214T195247"),
        "instance_id": "_________________",
        "centre": "LN3",
        "platform": "O",
        "timeliness": "NR",
        "baseline_collection": "___",
        "class_id": "O_NR____",
    }

    result = extract_data_from_product_name_s3(product_name)

    assert result == expected_result


def test_s3_product_name_l1_1():
    product_name = "S3A_TM_0_NAT____20211214T151253_20211214T165228_20211214T165453_5974_079_339______LN3_O_AL_002.SEN3.zip"

    expected_result = {
        "mission": "S3",
        "satellite_unit": "S3A",
        "instrument": "TM",
        "product_level": "L0_",
        "file_type_function": "NAT___",
        "product_type": "TM_0_NAT___",
        "start_sensing_time": datestr_to_utc_datetime("20211214T151253"),
        "end_sensing_time": datestr_to_utc_datetime("20211214T165228"),
        "creation_time": datestr_to_utc_datetime("20211214T165453"),
        "instance_id": "5974_079_339_____",
        "relative_orbit_number": "339",
        "centre": "LN3",
        "platform": "O",
        "timeliness": "AL",
        "baseline_collection": "002",
        "class_id": "O_AL_002",
        "cycle_number": "079",
        "datatake_id": "S3A-079-339",
    }

    result = extract_data_from_product_name_s3(product_name)

    assert result == expected_result


def test_s3_product_name_l1_2():
    product_name = "S3__GN_1_GSVMAX_20211214T195947_20211214T201447_20211214T201638___________________LND_O_NR_001.SEN3.zip"

    expected_result = {
        "mission": "S3",
        "satellite_unit": "S3_",
        "instrument": "GN",
        "product_level": "L1_",
        "file_type_function": "GSVMAX",
        "product_type": "GN_1_GSVMAX",
        "start_sensing_time": datestr_to_utc_datetime("20211214T195947"),
        "end_sensing_time": datestr_to_utc_datetime("20211214T201447"),
        "creation_time": datestr_to_utc_datetime("20211214T201638"),
        "instance_id": "_________________",
        "centre": "LND",
        "platform": "O",
        "timeliness": "NR",
        "baseline_collection": "001",
        "class_id": "O_NR_001",
    }

    result = extract_data_from_product_name_s3(product_name)

    assert result == expected_result


def test_s3_product_name_l2():
    product_name = "S3A_SY_2_SYN____20211214T002428_20211214T002728_20211214T155957_0179_079_330_2520_LN2_O_ST_002"

    expected_result = {
        "mission": "S3",
        "satellite_unit": "S3A",
        "instrument": "SY",
        "product_level": "L2_",
        "file_type_function": "SYN___",
        "product_type": "SY_2_SYN___",
        "start_sensing_time": datestr_to_utc_datetime("20211214T002428"),
        "end_sensing_time": datestr_to_utc_datetime("20211214T002728"),
        "creation_time": datestr_to_utc_datetime("20211214T155957"),
        "instance_id": "0179_079_330_2520",
        "relative_orbit_number": "330",
        "centre": "LN2",
        "platform": "O",
        "timeliness": "ST",
        "baseline_collection": "002",
        "class_id": "O_ST_002",
        "cycle_number": "079",
        "datatake_id": "S3A-079-330",
    }

    result = extract_data_from_product_name_s3(product_name)

    assert result == expected_result


def test_s3_product_name_bug_parsing_litteral_as_int():
    product_name = (
        "S3A_OPER_AUX_POEORB_POD__20220324T071709_V20220226T215942_20220227T235942_DGNS"
    )

    expected_result = {
        "mission": "S3",
        "satellite_unit": "S3A",
        "product_type": "AUX_POEORB",
        "extended_product_type": "OPER_AUX_POEORB_POD_",
    }

    result = extract_data_from_product_name_s3(product_name)

    assert result | expected_result == result


# @patch("logging.Logger.warning")
# def test_s3_product_name_collition_format(logger_mock):
#     product_name = "S3A_SY_2_SYN____imstringnotdate_20211214T002728_20211214T155957_0179_079_330_2520_LN2_O_ST_002"

#     expected_result = {
#         "mission": "S3",
#         "satellite_unit": "S3A",
#         "instrument": "SY",
#         "product_level": "L2_",
#         "file_type_function": "SYN___",
#         "product_type": "SY_2_SYN___",
#     }

#     result = extract_data_from_product_name_s3(product_name)

#     logger_mock.assert_called_with(
#         "Failed to extract data from S3 name %s",
#         "S3A_SY_2_SYN____imstringnotdate_20211214T002728_20211214T155957_0179_079_330_2520_LN2_O_ST_002",
#     )

#     assert result | expected_result == result
