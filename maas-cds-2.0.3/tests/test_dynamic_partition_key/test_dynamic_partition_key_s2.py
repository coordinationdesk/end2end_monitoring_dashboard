def test_s2_product_gip(s2_product_gip):
    assert s2_product_gip.partition_index_name == "cds-product-2022-06"


def test_s2_product_hktm(s2_product_hktm):
    assert s2_product_hktm.partition_index_name == "cds-product-2022-06"


def test_s2_product_l0_gr(s2_product_l0_gr):
    assert s2_product_l0_gr.partition_index_name == "cds-product-2022-06"


def test_s2_product_l2a_tc(s2_product_l2a_tc):
    assert s2_product_l2a_tc.partition_index_name == "cds-product-2022-06"


def test_s2_product_olqc_report(s2_product_olqc_report):
    assert s2_product_olqc_report.partition_index_name == "cds-product-2022-06"
