from maas_cds.lib.parsing_name import extract_data_from_product_name


def test_das_whitelisting():
    product_names = (
        "S10E022_2023_01_03_059632",
        "S21E055_2023_01_02_05959F",
        "N12E002_2023_02_20_05AE08",
        "S6A_MW_2_AMR___20230101T004528_20230101T014140_20230101T075246_3373_079_025_012_EUM_OPE_ST_F07.SEN6",
    )

    for product_name in product_names:

        result = extract_data_from_product_name(product_name)

        assert result == {}
