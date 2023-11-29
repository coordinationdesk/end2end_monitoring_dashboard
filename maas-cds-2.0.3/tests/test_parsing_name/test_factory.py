from maas_cds.lib.parsing_name import extract_data_from_product_name


def test_s5_product_name_unidentified_flying_object():
    product_names = (
        "SVM09_npp_d20220524_t0435022_e0436264_b54775_c20220524095134452403_oeac_ops.h5",
        "JRR - CloudMask_v2r3_npp_s202206011336244_e202206011337486_c202206011516000.nc",
    )

    for product_name in product_names:

        result = extract_data_from_product_name(product_name)

        assert result == {}
