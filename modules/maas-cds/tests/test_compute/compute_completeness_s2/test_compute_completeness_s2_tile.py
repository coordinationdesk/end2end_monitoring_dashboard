import datetime
from unittest.mock import patch
from maas_cds.model.datatake import Period
from maas_model.date_utils import datestr_to_utc_datetime
import pytest

from maas_cds.model.datatake_s2 import CdsDatatakeS2
from maas_cds.model.product import CdsProduct
from maas_cds.model.product_s2 import CdsProductS2
from maas_cds.model.enumeration import CompletenessScope, CompletenessStatus


@patch("maas_cds.model.datatake_s2.CdsDatatakeS2.search_expected_tiles")
@patch("maas_cds.model.datatake.CdsDatatake.find_brother_products_scan")
def test_compute_local_value_tiles_l1c(
    mock_find_brother_products_scan,
    mock_search_expected_tiles,
    s2_datatake_S2A_38107_1,
    s2_l1c_tl_products_S2A_38107_1,
    s2_l1c_ds_product_S2A_38107_1,
):
    """Test compute_local_value with product type TL L1C"""

    assert s2_datatake_S2A_38107_1.number_of_expected_tiles == 0

    mock_find_brother_products_scan.return_value = s2_l1c_tl_products_S2A_38107_1

    assert s2_datatake_S2A_38107_1.compute_local_value("MSI_L1C_TL") == 10

    mock_search_expected_tiles.return_value = set(
        s2_l1c_ds_product_S2A_38107_1.expected_tiles
    )

    # fake ingestion of l1c ds
    s2_datatake_S2A_38107_1.impact_other_calculation(
        s2_l1c_ds_product_S2A_38107_1.get_compute_key()
    )
    assert s2_datatake_S2A_38107_1.number_of_expected_tiles == 10

    assert s2_datatake_S2A_38107_1.evaluate_local_expected("MSI_L1C_TL") == 10


@patch("maas_cds.model.datatake_s2.CdsDatatakeS2.search_expected_tiles")
@patch("maas_cds.model.datatake.CdsDatatake.find_brother_products_scan")
def test_compute_local_value_tiles_l2a(
    mock_find_brother_products_scan,
    mock_search_expected_tiles,
    s2_datatake_S2A_38107_1,
    s2_l2a_tc_products_S2A_38107_1,
    s2_l1c_ds_product_S2A_38107_1,
):
    """Test tiles expected with product type"""

    assert s2_datatake_S2A_38107_1.number_of_expected_tiles == 0

    mock_find_brother_products_scan.return_value = s2_l2a_tc_products_S2A_38107_1

    assert s2_datatake_S2A_38107_1.compute_local_value("MSI_L2A_TC") == 10

    mock_search_expected_tiles.return_value = set(
        s2_l1c_ds_product_S2A_38107_1.expected_tiles
    )

    # fake ingestion of l1c ds
    s2_datatake_S2A_38107_1.impact_other_calculation(
        s2_l1c_ds_product_S2A_38107_1.get_compute_key()
    )
    assert s2_datatake_S2A_38107_1.number_of_expected_tiles == 10

    assert s2_datatake_S2A_38107_1.evaluate_local_expected("MSI_L2A_TC") == 10


@patch("maas_cds.model.datatake_s2.CdsDatatakeS2.search_expected_tiles")
@patch("maas_cds.model.datatake.CdsDatatake.find_brother_products_scan")
def test_compute_completeness_global(
    mock_find_brother_products_scan,
    mock_search_expected_tiles,
    s2_datatake_S2A_38107_1,
    s2_l2a_tc_products_S2A_38107_1,
    s2_l1c_ds_product_S2A_38107_1,
):

    # 1. empty completeness
    mock_find_brother_products_scan.return_value = []

    s2_datatake_S2A_38107_1.compute_all_local_completeness()
    s2_datatake_S2A_38107_1.compute_global_completeness()

    datatake_dict = s2_datatake_S2A_38107_1.to_dict()

    assert "MSI_L1C_DS_local_expected" in datatake_dict

    assert "MSI_L1C_TL_local_expected" not in datatake_dict
    assert "MSI_L1C_TC_local_expected" not in datatake_dict
    assert "MSI_L2A_TL_local_expected" not in datatake_dict
    assert "MSI_L2A_TC_local_expected" not in datatake_dict

    # 2. ingestion L1C DS update expected tiles

    mock_search_expected_tiles.return_value = set(
        s2_l1c_ds_product_S2A_38107_1.expected_tiles
    )

    s2_datatake_S2A_38107_1.impact_other_calculation(
        s2_l1c_ds_product_S2A_38107_1.get_compute_key()
    )

    assert s2_datatake_S2A_38107_1.number_of_expected_tiles == 10

    assert s2_datatake_S2A_38107_1.evaluate_local_expected("MSI_L1C_TL") == 10
    assert s2_datatake_S2A_38107_1.evaluate_local_expected("MSI_L1C_TC") == 10
    assert s2_datatake_S2A_38107_1.evaluate_local_expected("MSI_L2A_TL") == 10
    assert s2_datatake_S2A_38107_1.evaluate_local_expected("MSI_L2A_TC") == 10

    # 3. previous ingestion start completeness L2A TC/TC

    assert s2_datatake_S2A_38107_1.evaluate_local_expected("MSI_L2A_TC") == 10

    mock_find_brother_products_scan.return_value = s2_l2a_tc_products_S2A_38107_1

    local_value = s2_datatake_S2A_38107_1.compute_local_value("MSI_L2A_TC")
    s2_datatake_S2A_38107_1.set_completeness(
        CompletenessScope.LOCAL,
        "MSI_L2A_TC",
        local_value,
    )

    # 4. Recompute global completeness
    s2_datatake_S2A_38107_1.compute_global_completeness()

    datatake_dict = s2_datatake_S2A_38107_1.to_dict()
    assert datatake_dict["MSI_L2A_TC_local_value"] == 10

    assert datatake_dict["number_of_expected_tiles"] == 10
