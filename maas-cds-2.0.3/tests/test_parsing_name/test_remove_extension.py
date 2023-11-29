from maas_cds.lib.parsing_name.utils import (
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
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.SAFE.zip",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674.SAFE",
        "S1A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_4674",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.SEN3.zip",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000.SEN3",
        "S2A_EW_SLC__1SDH_20230411T212252_20230411T212333_048054_05C6CA_0000",
    ]

    publications = [
        publication_name
        for product_name in products
        for publication_name in generate_publication_names(product_name)
    ]

    assert set(publications) == set(correct_variations)
