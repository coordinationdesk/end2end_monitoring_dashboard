def test_s3_product_aux(s3_product_aux):
    assert s3_product_aux.partition_index_name == "cds-product-2022-04"


def test_s3_product_aux_1(s3_product_aux_1):
    assert s3_product_aux_1.partition_index_name == "cds-product-2022-06"


def test_s3_product_aux_2(s3_product_aux_2):
    assert s3_product_aux_2.partition_index_name == "cds-product-2022-05"


def test_s3_product_old(s3_product_old):
    assert s3_product_old.partition_index_name == "cds-product-2022-06"


def test_s3_product_aux_without_sep(s3_product_aux_without_sep):
    assert s3_product_aux_without_sep.partition_index_name == "cds-product-2022-06"
