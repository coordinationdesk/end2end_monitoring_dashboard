def test_get_all_product_types_iw(s1_datatake_iw):
    """get_all_product_types test for IW instrument mode"""

    list_product_type = s1_datatake_iw.get_all_product_types()

    assert list_product_type == [
        "IW_RAW__0A",
        "IW_RAW__0C",
        "IW_RAW__0N",
        "IW_RAW__0S",
        "IW_SLC__1A",
        "IW_SLC__1S",
        "IW_GRDH_1A",
        "IW_GRDH_1S",
        "IW_OCN__2A",
        "IW_OCN__2S",
        "IW_ETA__AX",
    ]


def test_get_all_product_types_ew(s1_datatake_ew):
    """get_all_product_types test for EW instrument mode"""

    list_product_type = s1_datatake_ew.get_all_product_types()

    assert list_product_type == [
        "EW_RAW__0A",
        "EW_RAW__0C",
        "EW_RAW__0N",
        "EW_RAW__0S",
        "EW_SLC__1A",
        "EW_SLC__1S",
        "EW_GRDM_1A",
        "EW_GRDM_1S",
        "EW_OCN__2A",
        "EW_OCN__2S",
        "EW_ETA__AX",
    ]


def test_get_all_product_types_sm(s1_datatake_sm):
    """get_all_product_types test for SM instrument mode"""

    list_product_type = s1_datatake_sm.get_all_product_types()

    assert list_product_type == [
        "S5_RAW__0A",
        "S5_RAW__0C",
        "S5_RAW__0N",
        "S5_RAW__0S",
        "S5_SLC__1A",
        "S5_SLC__1S",
        "S5_GRDH_1A",
        "S5_GRDH_1S",
        "S5_OCN__2A",
        "S5_OCN__2S",
        "S5_ETA__AX",
    ]


def test_get_all_product_types_wv(s1_datatake_wv):
    """get_all_product_types test for WV instrument mode"""

    list_product_type = s1_datatake_wv.get_all_product_types()

    assert list_product_type == [
        "WV_RAW__0A",
        "WV_RAW__0C",
        "WV_RAW__0N",
        "WV_RAW__0S",
        "WV_SLC__1A",
        "WV_SLC__1S",
        "WV_OCN__2A",
        "WV_OCN__2S",
    ]


def test_get_all_product_types_rfc(s1_datatake_rfc):
    """get_all_product_types test for RFC instrument mode"""

    list_product_type = s1_datatake_rfc.get_all_product_types()

    assert list_product_type == ["RF_RAW__0S"]


def test_get_all_product_types_s1_not_exist(s1_datatake_ew):
    s1_datatake_ew.instrument_mode = "YOLO"

    product_type = s1_datatake_ew.get_all_product_types()

    assert product_type == []


def test_add_prefix_instrument(
    s1_datatake_ew, s1_datatake_iw, s1_datatake_rfc, s1_datatake_sm, s1_datatake_wv
):
    assert s1_datatake_ew.add_prefix_instrument("RAW__0S") == "EW_RAW__0S"
    assert s1_datatake_iw.add_prefix_instrument("RAW__0S") == "IW_RAW__0S"
    assert s1_datatake_rfc.add_prefix_instrument("RAW__0S") == "RF_RAW__0S"
    assert s1_datatake_sm.add_prefix_instrument("RAW__0S") == "S5_RAW__0S"
    assert s1_datatake_wv.add_prefix_instrument("RAW__0S") == "WV_RAW__0S"


def test_impact_other_calculation_s1(s1_product_ew, s1_datatake_ew):
    compute_key = s1_product_ew.get_compute_key()

    assert compute_key == ("S1A-332942", "EW_RAW__0S")

    assert s1_datatake_ew.impact_other_calculation(compute_key) == [
        ("S1A-332942", "EW_SLC__1A"),
        ("S1A-332942", "EW_SLC__1S"),
        ("S1A-332942", "EW_OCN__2A"),
        ("S1A-332942", "EW_OCN__2S"),
    ]


def test_impact_other_calculation_s1_iw(s1_datatake_iw):
    compute_key = ("S1A-336894", "IW_RAW__0S")

    assert s1_datatake_iw.impact_other_calculation(compute_key) == [
        ("S1A-336894", "IW_OCN__2A"),
        ("S1A-336894", "IW_OCN__2S"),
    ]


def test_rf_compute_key(s1_product_rfc):
    compute_key = s1_product_rfc.get_compute_key()
    assert compute_key == ("S1A-358847", "RF_RAW__0S")


def test_amalfi_compute_key(s1_product_amalfi):
    """amalfi repport should be excluded of completeness computation"""
    compute_key = s1_product_amalfi.get_compute_key()
    assert compute_key is None
