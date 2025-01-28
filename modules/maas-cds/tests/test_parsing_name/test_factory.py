from maas_cds.lib.parsing_name import extract_data_from_product_name
from pytest import mark


@mark.parametrize(
    "expected_product_type,name",
    [
        ("AUX_NISE", "NISE_SSMISF18_20240221.HDFEOS"),
        ("AUX_NISE", "NISE_SSMISF18_20230123.HDFEOS"),
        ("AUX_IERS_B", "bulletinb-432.txt"),
        ("AUX_IERS_C", "bulletinc-067.txt"),
        ("AUX_IERS_C", "bulletinc-001.txt"),
        (
            "VIIRS_CM",
            "JRR-CloudMask_v3r2_npp_s202401270347403_e202401270349045_c202401270452268.tar",
        ),
        (
            "VIIRS_L1B_GEO",
            "GMODO_npp_d20240123_t2020515_e2022157_b63425_c20240124015115973212_oeac_ops.h5",
        ),
        (
            "VIIRS_L1B_RR",
            "SVM07_npp_d20240201_t1642109_e1643351_b63550_c20240201222939066041_oeac_ops.h5",
        ),
        (
            "VIIRS_L1B_RR",
            "SVM09_npp_d20240131_t2236497_e2238138_b63539_c20240201225829763103_oeac_ops.h5",
        ),
        (
            "VIIRS_L1B_RR",
            "SVM11_npp_d20240123_t1908194_e1909436_b63424_c20240124002748522455_oeac_ops.h5",
        ),
        (
            "VIIRS_CP",
            "JRR-CloudPhase_v3r2_npp_s202401240118105_e202401240122255_c202401240231234.tar",
        ),
        (
            "VIIRS_DCOMP",
            "JRR-CloudDCOMP_v3r2_npp_s202401232338357_e202401232339599_c202401240051218.tar",
        ),
        (
            "VIIRS_CTH",
            "JRR-CloudHeight_v3r2_npp_s202401232338357_e202401232339599_c202401240048534.tar",
        ),
        (
            "VIIRS_DCOMP",
            "JRR-CloudDCOMP_v3r2_npp_s202312130241404_e202312130250098_c202312130359132.tar",
        ),
    ],
)
def test_s5_product_name_non_standard(expected_product_type, name):

    expected_result = {
        "mission": "S5",
        "satellite_unit": "S5P",
        "product_type": expected_product_type,
    }

    result = extract_data_from_product_name(name)

    assert result == expected_result


@mark.parametrize(
    "expected_product_type,expected_product_level,name",
    [
        ("AUX_ML2", "L__", "S1A_AUX_ML2_V20190228T032500_G20230301T012345.SAFE"),
        (
            "OUT_OF_MONITORING",
            "L1_",
            "S1B_EW_GRDM_1SDH_20161119T211944_20161119T212044_003033_005280_2167_COG.SAFE",
        ),
        (
            "OUT_OF_MONITORING",
            "L1_",
            "S1A_IW_GRDH_1SDV_20141220T083036_20141220T083106_003800_00489B_48B7_CARD_BS",
        ),
    ],
)
def test_s1_new_product(expected_product_type, expected_product_level, name):
    assert expected_product_type == extract_data_from_product_name(name)["product_type"]
    assert (
        expected_product_level == extract_data_from_product_name(name)["product_level"]
    )
