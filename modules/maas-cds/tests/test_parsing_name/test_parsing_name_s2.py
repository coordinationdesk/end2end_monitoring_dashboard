from unittest import result
from unittest.mock import patch
from maas_cds.lib.parsing_name.parsing_name_s2 import extract_data_from_product_name_s2
from maas_model import datestr_to_utc_datetime


# # compact
# "S2B_MSIL2A_20211206T073209_N0301_R049_T39UWP_20211206T090000"
# "S2A_MSIL2A_20211206T070051_N0301_R120_T39LTE_20211206T075909"
# "S2A_MSIL1C_20210927T081721_N0301_R121_T35MKR_20211208T143513"


# # PARSER ARGS

# # GRANULES (GR|DS)_S(.*)_D(.*)
# # GR
# "S2B_OPER_MSI_L0__GR_MPS__20170728T232806_S20170728T183039_D03_N02.05.tar"
# "S2A_OPER_MSI_L1A_GR_VGS2_20211205T154907_S20211205T140633_D02_N03.01.tar"
# "S2A_OPER_MSI_L1B_GR_VGS4_20211206T092539_S20211206T083941_D12_N03.01.tar"
# # Datastrip
# "S2A_OPER_MSI_L0__DS_SGS__20170124T014632_S20170124T003025_N02.04.tar"
# "S2A_OPER_MSI_L2A_DS_VGS1_20211207T102540_S20211207T081144_N03.01.tar"

# # TILES (TL|TC)_A(.*)_T(.*)
# # TL tiles
# "S2B_OPER_MSI_L2A_TL_VGS4_20211209T113514_A024858_T34SDJ_N03.01.tar"
# # TC true colour
# "S2B_OPER_MSI_L1C_TC_VGS1_20211206T062120_A024812_T47RMP_N03.01.tar"


# # ?
# "S2B_OPER_PRD_HKTM___20211208T181105_20211208T181147_0001.tar"
# "S2__OPER_AUX_CAMSFO_PDMC_20211207T120000_V20211207T120000_20211209T130000.TGZ"


def test_s2_product_name_low_data():
    product_name = "S2B_OPER_PRD_HKTM___20211208T181105_20211208T181147_0001.tar"

    expected_result = {
        "mission": "S2",
        "satellite_unit": "S2B",
        "product_level": "L__",
        "file_class": "OPER",
        "file_category": "PRD_",
        "product_type": "PRD_HKTM__",
    }

    result = extract_data_from_product_name_s2(product_name)

    assert result == expected_result


def test_s2_product_name_extra_data_0():
    product_name = (
        "S2__OPER_AUX_CAMSFO_PDMC_20211207T120000_V20211207T120000_20211209T130000.TGZ"
    )

    expected_result = {
        "mission": "S2",
        "satellite_unit": "S2_",
        "file_class": "OPER",
        "file_category": "AUX_",
        "product_level": "L__",
        "product_type": "AUX_CAMSFO",
        "site_center": "PDMC",
        "creation_date": datestr_to_utc_datetime("20211207T120000"),
        "start_applicability_time_period": datestr_to_utc_datetime("20211207T120000"),
        "end_applicability_time_period": datestr_to_utc_datetime("20211209T130000"),
    }

    result = extract_data_from_product_name_s2(product_name)

    assert result | expected_result == result


def test_s2_product_name_extra_data_1():
    product_name = "S2A_OPER_GIP_R2ABCA_MPC__20211207T093600_V20211208T003000_21000101T000000_B00.TGZ"

    expected_result = {
        "mission": "S2",
        "satellite_unit": "S2A",
        "file_class": "OPER",
        "product_level": "L__",
        "product_type": "GIP_R2ABCA",
        "file_category": "GIP_",
        "site_center": "MPC_",
        "creation_date": datestr_to_utc_datetime("20211207T093600"),
        "start_applicability_time_period": datestr_to_utc_datetime("20211208T003000"),
        "end_applicability_time_period": datestr_to_utc_datetime("21000101T000000"),
        "band_index_id": "00",
    }

    result = extract_data_from_product_name_s2(product_name)

    assert result | expected_result == result


def test_s2_product_name_extra_data_2():
    product_name = "S2A_OPER_AUX_SADATA_EPAE_20190627T104830_V20190627T055919_20190627T074000_A020952_WF_LN.tar"

    expected_result = {
        "mission": "S2",
        "satellite_unit": "S2A",
        "file_class": "OPER",
        "product_level": "L__",
        "product_type": "AUX_SADATA",
        "file_category": "AUX_",
        "site_center": "EPAE",
        "creation_date": datestr_to_utc_datetime("20190627T104830"),
        "start_applicability_time_period": datestr_to_utc_datetime("20190627T055919"),
        "end_applicability_time_period": datestr_to_utc_datetime("20190627T074000"),
        "absolute_orbit_number": "020952",
        "completeness_id": "F",
        "degradation_id": "N",
    }

    result = extract_data_from_product_name_s2(product_name)

    assert result | expected_result == result


def test_s2_product_name_extra_data_3():
    product_name = (
        "S2__OPER_AUX_ECMWFD_PDMC_20211210T000000_V20211210T090000_20211212T030000.TGZ"
    )

    expected_result = {
        "mission": "S2",
        "satellite_unit": "S2_",
        "file_class": "OPER",
        "product_level": "L__",
        "product_type": "AUX_ECMWFD",
        "file_category": "AUX_",
        "site_center": "PDMC",
        "creation_date": datestr_to_utc_datetime("20211210T000000"),
        "start_applicability_time_period": datestr_to_utc_datetime("20211210T090000"),
        "end_applicability_time_period": datestr_to_utc_datetime("20211212T030000"),
    }

    result = extract_data_from_product_name_s2(product_name)

    assert result | expected_result == result


def test_s2_product_name_l0_0():
    product_name = (
        "S2A_OPER_MSI_L0__DS_SGS__20170124T014632_S20170124T003025_N02.04.tar"
    )

    expected_result = {
        "mission": "S2",
        "satellite_unit": "S2A",
        "file_class": "OPER",
        "product_type": "MSI_L0__DS",
        "file_category": "MSI_",
        "product_level": "L0_",
        "site_center": "SGS_",
        "creation_date": datestr_to_utc_datetime("20170124T014632"),
        "applicability_start_time": datestr_to_utc_datetime("20170124T003025"),
        "processing_baseline_number": "0204",
    }

    result = extract_data_from_product_name_s2(product_name)

    assert result | expected_result == result


def test_s2_product_name_l0_1():
    product_name = (
        "S2B_OPER_MSI_L0__GR_MPS__20170728T232806_S20170728T183039_D03_N02.05.tar"
    )

    expected_result = {
        "mission": "S2",
        "satellite_unit": "S2B",
        "file_class": "OPER",
        "product_type": "MSI_L0__GR",
        "file_category": "MSI_",
        "product_level": "L0_",
        "site_center": "MPS_",
        "creation_date": datestr_to_utc_datetime("20170728T232806"),
        "applicability_start_time": datestr_to_utc_datetime("20170728T183039"),
        "detector_id": "03",
        "processing_baseline_number": "0205",
    }

    result = extract_data_from_product_name_s2(product_name)

    assert result | expected_result == result


def test_s2_product_name_l1a():
    product_name = (
        "S2A_OPER_MSI_L1A_GR_VGS2_20211205T154907_S20211205T140633_D02_N03.01.tar"
    )

    expected_result = {
        "mission": "S2",
        "satellite_unit": "S2A",
        "file_class": "OPER",
        "product_type": "MSI_L1A_GR",
        "file_category": "MSI_",
        "product_level": "L1A",
        "site_center": "VGS2",
        "creation_date": datestr_to_utc_datetime("20211205T154907"),
        "applicability_start_time": datestr_to_utc_datetime("20211205T140633"),
        "detector_id": "02",
        "processing_baseline_number": "0301",
    }

    result = extract_data_from_product_name_s2(product_name)

    assert result | expected_result == result


def test_s2_product_name_l1b():
    product_name = (
        "S2A_OPER_MSI_L1B_GR_VGS4_20211206T092539_S20211206T083941_D12_N03.01.tar"
    )

    expected_result = {
        "mission": "S2",
        "satellite_unit": "S2A",
        "file_class": "OPER",
        "product_type": "MSI_L1B_GR",
        "file_category": "MSI_",
        "product_level": "L1B",
        "site_center": "VGS4",
        "creation_date": datestr_to_utc_datetime("20211206T092539"),
        "applicability_start_time": datestr_to_utc_datetime("20211206T083941"),
        "detector_id": "12",
        "processing_baseline_number": "0301",
    }

    result = extract_data_from_product_name_s2(product_name)

    assert result | expected_result == result


def test_s2_product_name_l1c():
    product_name = "S2B_OPER_MSI_L1C_TC_VGS1_20211206T062120_A024812_T47RMP_N03.01.tar"

    expected_result = {
        "mission": "S2",
        "satellite_unit": "S2B",
        "file_class": "OPER",
        "product_type": "MSI_L1C_TC",
        "file_category": "MSI_",
        "product_level": "L1C",
        "site_center": "VGS1",
        "creation_date": datestr_to_utc_datetime("20211206T062120"),
        "absolute_orbit_number": "024812",
        "tile_number": "47RMP",
        "processing_baseline_number": "0301",
    }

    result = extract_data_from_product_name_s2(product_name)

    assert result | expected_result == result


def test_s2_product_name_l2a_0():
    product_name = (
        "S2B_OPER_MSI_L0__GR_MPS__20170728T232806_S20170728T183039_D03_N02.05.tar"
    )

    expected_result = {
        "mission": "S2",
        "satellite_unit": "S2B",
        "file_class": "OPER",
        "product_type": "MSI_L0__GR",
        "file_category": "MSI_",
        "product_level": "L0_",
        "site_center": "MPS_",
        "creation_date": datestr_to_utc_datetime("20170728T232806"),
        "applicability_start_time": datestr_to_utc_datetime("20170728T183039"),
        "detector_id": "03",
        "processing_baseline_number": "0205",
    }

    result = extract_data_from_product_name_s2(product_name)

    assert result | expected_result == result


def test_s2_product_name_l2a_1():
    product_name = (
        "S2A_OPER_MSI_L2A_DS_VGS1_20211207T102540_S20211207T081144_N03.01.tar"
    )

    expected_result = {
        "mission": "S2",
        "satellite_unit": "S2A",
        "file_class": "OPER",
        "product_type": "MSI_L2A_DS",
        "file_category": "MSI_",
        "product_level": "L2A",
        "site_center": "VGS1",
        "creation_date": datestr_to_utc_datetime("20211207T102540"),
        "applicability_start_time": datestr_to_utc_datetime("20211207T081144"),
        "processing_baseline_number": "0301",
    }

    result = extract_data_from_product_name_s2(product_name)

    assert result | expected_result == result


def test_s2_product_name_l1c_compact_name():
    product_name = "S2A_MSIL1C_20211206T182741_N0301_R127_T11SQS_20211206T201831"

    expected_result = {
        "mission": "S2",
        "satellite_unit": "S2A",
        "product_level": "L1C",
        "datatake_id_sensing_time": datestr_to_utc_datetime("20211206T182741"),
        "processing_baseline_number": "0301",
        "relative_orbit_number": "127",
        "tile_number": "11SQS",
        "product_discriminator_date": datestr_to_utc_datetime("20211206T201831"),
        "product_type": "MSI_L1C___",
    }

    result = extract_data_from_product_name_s2(product_name)

    assert result | expected_result == result


def test_s2_product_name_l1b_compact_name():
    product_name = "S2A_MSIL1B_20231020T134701_N0509_R024_20231020T200129.zip"

    expected_result = {
        "mission": "S2",
        "satellite_unit": "S2A",
        "product_level": "L1B",
        "datatake_id_sensing_time": datestr_to_utc_datetime("20231020T134701"),
        "processing_baseline_number": "0509",
        "relative_orbit_number": "024",
        "product_discriminator_date": datestr_to_utc_datetime("20231020T200129"),
        "product_type": "MSI_L1B___",
    }

    result = extract_data_from_product_name_s2(product_name)

    assert result | expected_result == result


def test_s2_product_name_l2a_compact_name():
    product_name = "S2A_MSIL2A_20211210T094411_N0301_R036_T32PQU_20211210T121029"

    expected_result = {
        "mission": "S2",
        "satellite_unit": "S2A",
        "product_level": "L2A",
        "datatake_id_sensing_time": datestr_to_utc_datetime("20211210T094411"),
        "processing_baseline_number": "0301",
        "relative_orbit_number": "036",
        "tile_number": "32PQU",
        "product_discriminator_date": datestr_to_utc_datetime("20211210T121029"),
        "product_type": "MSI_L2A___",
    }

    result = extract_data_from_product_name_s2(product_name)

    assert result | expected_result == result


def test_s2_product_name_parse_iso_bug():
    product_name = (
        "S2A_OPER_MSI_L0__DS_ATOS_20220324T094748_S20220324T080040_OLQC_report.tar"
    )

    expected_result = {
        "mission": "S2",
        "satellite_unit": "S2A",
        "file_class": "OPER",
        "product_type": "OLQC_REPORT",
        "file_category": "MSI_",
        "product_level": "L0_",
        "site_center": "ATOS",
        "creation_date": datestr_to_utc_datetime("20220324T094748"),
        "applicability_start_time": datestr_to_utc_datetime("20220324T080040"),
    }

    result = extract_data_from_product_name_s2(product_name)

    assert result | expected_result == result


@patch("logging.Logger.warning")
def test_s2_product_unexpected_format_collition(logger_mock):
    product_name = "S2A_OPER_MSI_L0__DS_ATOS_20220324T094748_S20220324T080040_Viamastring_report.tar"

    expected_result = {
        "mission": "S2",
        "satellite_unit": "S2A",
        "file_class": "OPER",
        "product_type": "OLQC_REPORT",
        "file_category": "MSI_",
        "product_level": "L0_",
        "site_center": "ATOS",
        "creation_date": datestr_to_utc_datetime("20220324T094748"),
        "applicability_start_time": datestr_to_utc_datetime("20220324T080040"),
    }

    result = extract_data_from_product_name_s2(product_name)

    assert result | expected_result == result
    logger_mock.assert_called_with(
        "Failed to use %s with %s", "_V", "iamastring_report.tar"
    )


def test_s2_report_product():
    report_products = [
        "S2A_OPER_MSI_L2A_DS_ATOS_20220413T124953_S20220413T092031_OLQC_report.tar"
        "S2B_OPER_MSI_L1C_TL_CAPG_20220413T073653_A026643_T43MDR_SENSOR_QUALITY_report.xml"
    ]

    for product_name in report_products:
        result_dict = extract_data_from_product_name_s2(product_name)

        assert result_dict["product_type"] == "OLQC_REPORT"
