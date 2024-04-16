from maas_cds.lib.parsing_name.utils import (
    normalize_product_name_list,
    remove_extension_from_product_name,
    generate_publication_names,
)


def test_common_extension():
    products_with_common_extension = [
        "test.ZIP",
        "test.jp2",
        "test.TGZ",
        "test.EOF",
        "test.SAFE.zip",
        "test.zip",
        "test.tar",
        "test.SEN3.zip",
        "test.EOF.zip",
    ]

    for product_name in products_with_common_extension:
        product_name_without_extension = remove_extension_from_product_name(
            product_name
        )
        assert product_name_without_extension == "test"


def test_generate_publication_names():
    products = [
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.SAFE.zip",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.SEN3.zip",
    ]

    correct_variations = [
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.EOF",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.EOF.tar",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.EOF.tgz",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.EOF.zip",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.RAW",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.RAW.tar",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.RAW.tgz",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.RAW.zip",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.SAFE",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.SAFE.tar",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.SAFE.tgz",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.SAFE.zip",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.SEN3",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.SEN3.tar",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.SEN3.tgz",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.SEN3.zip",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.h5",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.h5.tar",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.h5.tgz",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.h5.zip",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.nc",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.nc.tar",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.nc.tgz",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.nc.zip",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.tar",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.tgz",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.zip",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.EOF",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.EOF.tar",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.EOF.tgz",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.EOF.zip",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.RAW",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.RAW.tar",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.RAW.tgz",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.RAW.zip",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.SAFE",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.SAFE.tar",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.SAFE.tgz",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.SAFE.zip",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.SEN3",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.SEN3.tar",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.SEN3.tgz",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.SEN3.zip",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.h5",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.h5.tar",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.h5.tgz",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.h5.zip",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.nc",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.nc.tar",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.nc.tgz",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.nc.zip",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.tar",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.tgz",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.zip",
    ]

    publications = [
        publication_name
        for product_name in products
        for publication_name in generate_publication_names(product_name)
    ]

    assert set(publications) == set(correct_variations)


def test_normalize_and_generate():
    products_init = [
        "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.SAFE",
        "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.SAFE",
    ]
    products = normalize_product_name_list(products_init)
    products = normalize_product_name_list(products)

    assert products == [
        "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.SAFE",
        "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.SAFE",
    ]

    publications = [
        publication_name
        for product_name in products
        for publication_name in generate_publication_names(product_name)
    ]

    assert sorted(publications) == sorted(
        [
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.h5",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.tgz",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.RAW.tgz",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.RAW.zip",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.SAFE",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.SEN3.tar",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.SEN3.tgz",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.EOF.tgz",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.RAW.tar",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.h5.zip",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.tar",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.EOF",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.nc.zip",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.SAFE.tgz",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.nc.tgz",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.nc.tar",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.zip",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.RAW",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.SEN3",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.EOF.tar",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.EOF.zip",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.SAFE.tar",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.h5.tgz",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.SAFE.zip",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.h5.tar",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.SEN3.zip",
            "S1A_IW_RAW__0ADV_20240127T052746_20240127T054007_052288_065258_C173.nc",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.h5.zip",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.h5.tgz",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.RAW.tar",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.nc",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.tgz",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.SEN3.tgz",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.EOF.zip",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.RAW.tgz",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.tar",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.SAFE",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.RAW.zip",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.h5.tar",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.nc.zip",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.nc.tgz",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.RAW",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.EOF",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.EOF.tgz",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.SEN3.tar",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.SAFE.zip",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.EOF.tar",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.h5",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.SAFE.tgz",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.SEN3.zip",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.nc.tar",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.SAFE.tar",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.SEN3",
            "S1A_IW_RAW__0SDV_20240127T053156_20240127T053229_052288_065258_64A5.zip",
        ]
    )
