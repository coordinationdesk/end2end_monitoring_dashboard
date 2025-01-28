from maas_cds.lib.parsing_name.parsing_name_s1 import extract_data_from_product_name_s1
from maas_model import datestr_to_utc_datetime

# Export this function
validate_orbit = lambda x: 1 <= int(x) <= 999999
validate_product_unique_id = lambda x: 0x1 <= int(f"0x{x}", 16) <= 0xFFFF
validate_datatake_id = lambda x: 0x1 <= int(f"0x{x}", 16) <= 0xFFFFFF
validate_product_level = lambda x: x in ["L__", "L0_", "L1_", "L2_"]


def test_s1_product_name_l0():
    product_name = (
        "S1B_EW_RAW__0NDH_20211206T121955_20211206T122150_029904_0391E7_D00D.SAFE.zip"
    )
    expected_result = {
        "mission": "S1",
        "satellite_unit": "S1B",
        "instrument_mode": "EW",
        "type": "RAW",
        "resolution_class": "_",
        "product_type": "EW_RAW__0N",
        "product_level": "L0_",
        "product_class": "N",
        "polarization": "DH",
        "start_date": datestr_to_utc_datetime("20211206T121955"),
        "stop_date": datestr_to_utc_datetime("20211206T122150"),
        "absolute_orbit_number": "029904",
        "datatake_id": "0391E7",
        "product_unique_id": "D00D",
    }

    result = extract_data_from_product_name_s1(product_name)

    assert result == expected_result


def test_s1_product_name_l1_1():
    product_name = "S1A_IW_SLC__1SSH_20211206T145442_20211206T145509_040889_04DAF2_D98A"
    expected_result = {
        "mission": "S1",
        "satellite_unit": "S1A",
        "instrument_mode": "IW",
        "type": "SLC",
        "resolution_class": "_",
        "product_type": "IW_SLC__1S",
        "product_level": "L1_",
        "product_class": "S",
        "polarization": "SH",
        "start_date": datestr_to_utc_datetime("20211206T145442"),
        "stop_date": datestr_to_utc_datetime("20211206T145509"),
        "absolute_orbit_number": "040889",
        "datatake_id": "04DAF2",
        "product_unique_id": "D98A",
    }

    result = extract_data_from_product_name_s1(product_name)

    assert result == expected_result


def test_s1_product_name_l1_2():
    product_name = "S1A_IW_GRDH_1SDV_20211214T155446_20211214T155514_041007_04DF02_A693"
    expected_result = {
        "mission": "S1",
        "satellite_unit": "S1A",
        "instrument_mode": "IW",
        "type": "GRD",
        "resolution_class": "H",
        "product_type": "IW_GRDH_1S",
        "product_level": "L1_",
        "product_class": "S",
        "polarization": "DV",
        "start_date": datestr_to_utc_datetime("20211214T155446"),
        "stop_date": datestr_to_utc_datetime("20211214T155514"),
        "absolute_orbit_number": "041007",
        "datatake_id": "04DF02",
        "product_unique_id": "A693",
    }

    result = extract_data_from_product_name_s1(product_name)

    assert result == expected_result


def test_s1_product_name_l2():
    product_name = (
        "S1B_EW_OCN__2SDH_20211207T152344_20211207T152444_029921_03926C_A509.SAFE.zip"
    )

    expected_result = {
        "mission": "S1",
        "satellite_unit": "S1B",
        "instrument_mode": "EW",
        "type": "OCN",
        "resolution_class": "_",
        "product_type": "EW_OCN__2S",
        "product_level": "L2_",
        "product_class": "S",
        "polarization": "DH",
        "start_date": datestr_to_utc_datetime("20211207T152344"),
        "stop_date": datestr_to_utc_datetime("20211207T152444"),
        "absolute_orbit_number": "029921",
        "datatake_id": "03926C",
        "product_unique_id": "A509",
    }

    result = extract_data_from_product_name_s1(product_name)

    assert result == expected_result


def test_s1_product_name_aux():
    product_name = "S1__AUX_WND_V20211212T210000_G20211209T061237.SAFE.zip"

    expected_result = {
        "mission": "S1",
        "satellite_unit": "S1_",
        "product_level": "L__",
        "product_type": "AUX_WND",
    }

    result = extract_data_from_product_name_s1(product_name)

    assert result == expected_result


def test_s1_product_name_obs():
    product_name = "S1A____OBS__SS___20211208T014130_20211208T032014_040911_018A.zip"

    expected_result = {
        "mission": "S1",
        "satellite_unit": "S1A",
        "product_level": "L__",
        "product_type": "___OBS__SS",
    }

    result = extract_data_from_product_name_s1(product_name)

    assert result == expected_result


def test_s1_products_name_result_value_global_compatibility_no_level():

    products_name = [
        "S1B_OPER_AUX_RESORB_OPOD_20211209T151701_V20211209T112457_20211209T144227.EOF.zip",
        "S1B_OPER_REP_QCDAIL_MPC__20211207T052605_V20211206T000000_20211207T000000.zip",
        "S1B_OPER_MPL_ORBPRE_20211208T021227_20211215T021227_0001.EOF.zip",
        "S1__OPER_REP_QCPERF_MPC__20211207T060014_V20211206T060000_20211207T060000.zip",
        "S1__AUX_WAV_V20211210T180000_G20211209T043157.SAFE.zip",
        "S1B____OBS__SS___20211207T163743_20211207T181627_029922_A073.zip",
    ]

    value_possibility = {
        "satellite_unit": (lambda x: x in ["S1_", "S1A", "S1B"]),
        "product_level": validate_product_level,
    }
    for product_name in products_name:
        result = extract_data_from_product_name_s1(product_name)
        for k, f in value_possibility.items():
            assert f(result[k]) == True


def test_s1_oper_file_product_type():
    product_name = "S1B_OPER_AUX_RESORB_OPOD_20211209T151701_V20211209T112457_20211209T144227.EOF.zip"

    data_dict = extract_data_from_product_name_s1(product_name)

    assert data_dict["product_type"] == "AUX_RESORB"


def test_s1_l0_product_name():
    products_name = [
        "S1A_IW_RAW__0SDV_20211206T102150_20211206T102222_040887_04DADC_1063",
        "S1B_WV_RAW__0ASV_20211209T011243_20211209T012950_029941_039310_E36E.SAFE.zip"
        "S1B_IW_RAW__0SDV_20211209T003037_20211209T003110_029941_03930D_13F9",
        "S1B_EW_RAW__0SDH_20211206T112430_20211206T112538_029904_0391E5_D517.SAFE.zip",
    ]

    value_possibility = {
        "satellite_unit": lambda x: x in ["S1_", "S1A", "S1B"],
        "type": lambda x: x in ["RAW"],
        "product_level": validate_product_level,
        "resolution_class": lambda x: x in ["F", "H", "M", "_"],
        "product_class": lambda x: x in ["S", "A", "N", "C"],
        "polarization": lambda x: x in ["SH", "SV", "DH", "DV"],
        # "start_date": "",
        # "stop_date": "",
        "absolute_orbit_number": validate_orbit,
        "datatake_id": validate_datatake_id,
        "product_unique_id": validate_product_unique_id,
    }

    l0_allow_product_family = [
        "SM_RAW__0S",
        "SM_RAW__0C",
        "SM_RAW__0N",
        "SM_RAW__0A",
        "IW_RAW__0S",
        "IW_RAW__0C",
        "IW_RAW__0N",
        "IW_RAW__0A",
        "EW_RAW__0S",
        "EW_RAW__0C",
        "EW_RAW__0N",
        "EW_RAW__0A",
        "WV_RAW__0S",
        "WV_RAW__0C",
        "WV_RAW__0N",
        "WV_RAW__0A",
        "RF_RAW__0S",
    ]

    for product_name in products_name:
        result = extract_data_from_product_name_s1(product_name)
        for k, f in value_possibility.items():
            assert f(result[k]) == True

        assert result["product_type"] in l0_allow_product_family


def test_s1_l1_product_name():
    products_name = [
        "S1A_EW_GRDM_1SDH_20211206T081126_20211206T081226_040885_04DAD0_A0E1",
        "S1A_IW_GRDH_1SDH_20211206T090936_20211206T091001_040886_04DAD5_266C",
        "S1B_EW_GRDM_1ADH_20211108T070247_20211108T070347_029493_038514_27DB.SAFE.zip",
        "S1A_IW_GRDH_1SDV_20211214T155446_20211214T155514_041007_04DF02_A693",
        "S1A_IW_SLC__1SDV_20211206T002619_20211206T002646_040881_04DAAF_5649",
        "S1B_IW_GRDH_1SDV_20211206T230645_20211206T230710_029911_03921D_6E47.SAFE.zip",
        "S1B_WV_SLC__1ASV_20211207T030856_20211207T034255_029913_03922E_04F5.SAFE.zip",
        "S1B_IW_SLC__1SDV_20211208T171210_20211208T171237_029936_0392EA_168A",
        "S1B_IW_SLC__1SDH_20211208T071929_20211208T071959_029930_0392B2_1B3C.SAFE.zip",
        "S1B_IW_SLC__1ADV_20211207T004419_20211207T004446_029912_039224_BB51.SAFE.zip",
        "S1B_WV_SLC__1ASV_20211206T232058_20211206T233949_029911_03921E_43D8.SAFE.zip",
    ]

    value_possibility = {
        "satellite_unit": lambda x: x in ["S1A", "S1B"],
        "instrument_mode": lambda x: x in ["IW", "EW", "WV", "RF", "SM"],
        "type": lambda x: x in ["SLC", "GRD"],
        "resolution_class": lambda x: x in ["F", "H", "M", "_"],
        "product_level": validate_product_level,
        "product_class": lambda x: x in ["S", "A"],
        "polarization": lambda x: x in ["SH", "SV", "DH", "DV", "HH", "HV", "VV", "VH"],
        # "start_date": "",
        # "stop_date": "",
        "absolute_orbit_number": validate_orbit,
        "datatake_id": validate_datatake_id,
        "product_unique_id": validate_product_unique_id,
    }

    l1_allow_product_family = [
        "WV_SLC__1A",
        "WV_SLC__1S",
        "WV_GRDM_1A",
        "WV_GRDM_1S",
        "EW_SLC__1A",
        "EW_SLC__1S",
        "EW_GRDH_1A",
        "EW_GRDH_1S",
        "EW_GRDM_1A",
        "EW_GRDM_1S",
        "IW_SLC__1A",
        "IW_SLC__1S",
        "IW_GRDH_1A",
        "IW_GRDH_1S",
        "IW_GRDM_1A",
        "IW_GRDM_1S",
        "SM_SLC__1S",
        "SM_SLC__1A",
        "SM_GRDH_1A",
        "SM_GRDH_1S",
        "SM_GRDM_1A",
        "SM_GRDM_1S",
        "SM_GRDF_1A",
        "SM_GRDF_1S",
    ]

    for product_name in products_name:
        result = extract_data_from_product_name_s1(product_name)
        for k, f in value_possibility.items():
            assert f(result[k]) == True
        assert result["product_type"] in l1_allow_product_family


def test_s1_l2_product_name():
    products_name = [
        "S1A_IW_OCN__2SDH_20211206T090503_20211206T090528_040886_04DAD4_7B79",
        "S1B_EW_OCN__2SDH_20211208T210117_20211208T210217_029939_0392FC_1CD9",
        "S1A_EW_OCN__2SDH_20211206T080921_20211206T081026_040885_04DAD0_E172",
        "S1A_IW_OCN__2SDV_20211206T083004_20211206T083029_040885_04DAD2_BEBF",
        "S1B_IW_OCN__2ADV_20211208T162300_20211208T162329_029936_0392E7_0D62.SAFE.zip",
    ]

    value_possibility = {
        "satellite_unit": lambda x: x in ["S1A", "S1B"],
        "instrument_mode": lambda x: x
        in ["S1", "S2", "S3", "S4", "S5", "S6", "IW", "EW", "WV", "RF", "SM"],
        "type": lambda x: x in ["OCN"],
        "product_level": validate_product_level,
        "resolution_class": lambda x: x in ["_"],
        "product_class": lambda x: x in ["S", "A"],
        "polarization": lambda x: x in ["SH", "SV", "DH", "DV"],
        # "start_date": "",
        # "stop_date": "",
        "absolute_orbit_number": validate_orbit,
        "datatake_id": validate_datatake_id,
        "product_unique_id": validate_product_unique_id,
    }

    for product_name in products_name:
        result = extract_data_from_product_name_s1(product_name)
        for k, f in value_possibility.items():
            assert f(result[k]) == True


def test_s1_report_product_1():

    product_name = "S1A_IW_RAW__0SDV_20220413T113112_20220413T113141_042754_051A30_4104.SAFE-report-20220413T120535.xml"

    result_dict = extract_data_from_product_name_s1(product_name)

    assert result_dict["product_type"] == "AMALFI_REPORT"


def test_s1_report_product_2():

    product_name = "S1A_IW_SLC__1SDV_20220428T215320_20220428T215349_042979_05219D_B02D.SAFE-report-20220429T035633.xml"

    result_dict = extract_data_from_product_name_s1(product_name)

    assert result_dict["product_type"] == "AMALFI_REPORT"


def test_s1_eta_x_product_1():

    product_name = (
        "S1A_EW_ETA__AXDH_20220210T144717_20220210T144920_041852_04FB83_42F3.SAFE.zip"
    )

    result_dict = extract_data_from_product_name_s1(product_name)

    assert result_dict == {
        "satellite_unit": "S1A",
        "mission": "S1",
        "product_type": "EW_ETA__AX",
        "product_level": "LA_",
        "instrument_mode": "EW",
        "type": "ETA",
        "resolution_class": "_",
        "product_class": "X",
        "polarization": "DH",
        "start_date": datestr_to_utc_datetime("20220210T144717"),
        "stop_date": datestr_to_utc_datetime("20220210T144920"),
        "absolute_orbit_number": "041852",
        "datatake_id": "04FB83",
        "product_unique_id": "42F3",
    }


def test_s1_aux_mp_classic_size_10():
    product_name = "S1A_MP_ACQ_B2B_20241111T173809_20241123T192514.csv.zip"

    result_dict = extract_data_from_product_name_s1(product_name)

    assert result_dict == {
        "satellite_unit": "S1A",
        "mission": "S1",
        "product_type": "MP_ACQ_B2B",
        "product_level": "L__",
    }


def test_s1_aux_mp_specific_size_8():

    product_name = "S1C_MP_ALL__MTL_20241021T171016_20241102T193714.tgz"
    result_dict = extract_data_from_product_name_s1(product_name)

    assert result_dict == {
        "satellite_unit": "S1C",
        "mission": "S1",
        "product_type": "MP_ALL__",
        "product_level": "L__",
    }


def test_s1_aux_mp_specific_size_12():
    product_name = "S1A_OPER_MPL_TIMELINE_20241119T171645_20241201T193544.tgz"
    result_dict = extract_data_from_product_name_s1(product_name)

    assert result_dict == {
        "satellite_unit": "S1A",
        "mission": "S1",
        "product_type": "MPL_TIMELINE",
        "product_level": "L__",
    }
