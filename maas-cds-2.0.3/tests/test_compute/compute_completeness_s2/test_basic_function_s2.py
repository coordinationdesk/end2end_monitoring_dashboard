from unittest.mock import patch


def test_product_type_over_specific_area(
    s1_datatake_ew, s1_datatake_iw, s1_datatake_rfc, s1_datatake_sm, s1_datatake_wv
):

    assert s1_datatake_wv.product_type_over_specific_area("OCN__2S") is False
    assert s1_datatake_rfc.product_type_over_specific_area("OCN__2S") is False

    assert s1_datatake_ew.product_type_over_specific_area("OCN__2S") is True
    assert s1_datatake_ew.product_type_over_specific_area("SLC__1S") is True
    assert s1_datatake_ew.product_type_over_specific_area("RAW__0S") is False

    assert s1_datatake_iw.product_type_over_specific_area("OCN__2S") is True
    assert s1_datatake_iw.product_type_over_specific_area("SLC__1S") is False

    assert s1_datatake_sm.product_type_over_specific_area("OCN__2S") is True
    assert s1_datatake_sm.product_type_over_specific_area("SLC__1S") is False


def test_product_type_s2(s2_datatake_nobs):

    assert s2_datatake_nobs.get_expected_product_level() == ["L0_", "L1B", "L1C", "L2A"]

    products_types = s2_datatake_nobs.get_all_product_types()

    assert products_types == [
        "MSI_L0__DS",
        "MSI_L0__GR",
        "MSI_L1B_DS",
        "MSI_L1B_GR",
        "MSI_L1C_DS",
        "MSI_L1C_TL",
        "MSI_L1C_TC",
        "MSI_L2A_DS",
        "MSI_L2A_TL",
        "MSI_L2A_TC",
    ]


@patch(
    "maas_cds.model.datatake_s2.CdsDatatakeS2.search_expected_tiles",
    return_value=["a random tile number"],
)
def test_impact_other_calculation_s2(
    mock_search_expected_tiles, s2_product_l1c_ds, s2_datatake_nobs
):

    compute_key = s2_product_l1c_ds.get_compute_key()

    assert compute_key == ("S2A-36678-7", "MSI_L1C_DS")

    assert s2_datatake_nobs.number_of_expected_tiles == 0

    assert s2_datatake_nobs.impact_other_calculation(compute_key) == [
        ("S2A-36678-7", "MSI_L1C_TL"),
        ("S2A-36678-7", "MSI_L1C_TC"),
        ("S2A-36678-7", "MSI_L2A_TL"),
        ("S2A-36678-7", "MSI_L2A_TC"),
    ]

    # mock is called to update expected tiles
    assert mock_search_expected_tiles.called

    assert s2_datatake_nobs.number_of_expected_tiles == 1
