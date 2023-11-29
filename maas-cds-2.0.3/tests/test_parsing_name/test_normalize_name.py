from maas_cds.lib.parsing_name.utils import normalize_product_name


def test_normalize_container_name():

    name = "S2B_OPER_MSI_L2A_TL_2BPS_20221119T100525_A029791_T35QPV_N04.00"

    normalized_name = (
        "S2B_OPER_MSI_L2A_TL_2BPS_20221119T100525_A029791_T35QPV_N04.00.tar"
    )

    # check .tar extension is added
    assert normalize_product_name(name) == normalized_name

    # check name is untouched if it has extension
    assert normalize_product_name(normalized_name) == normalized_name

    non_s2_name = "S5P_OPER_L0__SAT_A__20211102T085051_20211102T091050_21012_05.RAW"

    assert normalize_product_name(non_s2_name) == non_s2_name
