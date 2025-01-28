import datetime
from unittest.mock import patch
from maas_cds.model.datatake import CdsDatatake

from maas_cds.lib.periodutils import compute_total_sensing_product, Period

from maas_model.date_utils import datestr_to_utc_datetime
import pytest

from maas_cds.model.datatake_s2 import CdsDatatakeS2
from maas_cds.model.product import CdsProduct
from maas_cds.model.product_s2 import CdsProductS2
from maas_cds.model.enumeration import CompletenessStatus


@pytest.fixture
def datatake_s2_dict():
    """Get a basic s2 datatake dict

    Usefull to recreate a CdsDatatakeS2

    Returns:
        dict: return a dict of a CdsDatatakeS2
    """
    return {
        "name": "S2B_MP_ACQ__MTL_20220317T120000_20220404T150000.csv",
        "key": "26434-3",
        "datatake_id": "26434-3",
        "satellite_unit": "S2B",
        "mission": "S2",
        "observation_time_start": datetime.datetime(
            2022, 3, 29, 14, 37, 22, 7000, tzinfo=datetime.timezone.utc
        ),
        "observation_duration": 100000000,  # 1201464000
        "observation_time_stop": datetime.datetime(
            2022, 3, 29, 14, 57, 23, 471000, tzinfo=datetime.timezone.utc
        ),
        "number_of_scenes": 5,  # 333
        "absolute_orbit": "26434",
        "relative_orbit": "96",
        "timeliness": "NOMINAL",
        "instrument_mode": "NOBS",
        "application_date": "2022-03-17T12:00:00.000Z",
        "updateTime": "2022-03-30T12:14:29.408Z",
    }


@pytest.fixture
def product_s2_dict():
    """Get a basic s2 product dict

    Usefull to recreate a CdsProduct

    Returns:
        dict: return a dict of a CdsProduct
    """
    return {
        "key": "775f0604c418c9a48f229e7b07b66281",
        "mission": "S2",
        "name": "S2B_OPER_AUX_PREORB_OPOD_20200511T204859_V20200511T222603_20200512T014727.EOF",
        "product_level": "L0_",
        "product_type": "AUX_PREORB",
        "satellite_unit": "S2B",
        "site_center": "OPOD",
        "sensing_start_date": datetime.datetime(
            2022, 3, 29, 14, 37, 22, 7000, tzinfo=datetime.timezone.utc
        ),
        "sensing_end_date": datetime.datetime(
            2022, 3, 29, 14, 57, 47, 471000, tzinfo=datetime.timezone.utc
        ),
        "detector_id": "01",
        "sensing_duration": 12084000000.0,
        "expected_lta_number": 4,
        "LTA_Werum_is_published": True,
        "LTA_Werum_publication_date": datetime.datetime(
            2022, 1, 12, 7, 11, 53, 994000, tzinfo=datetime.timezone.utc
        ),
        "nb_lta_served": 1,
        "product_group_id": "GS2A_20240124T140451_044866_N05.10",
        "datastrip_id": "S2A_OPER_MSI_L1C_DS_2APS_20240124T155206_S20240124T140447_N05.10",
        "quality_status": "NOMINAL",
        "cloud_cover": 10.2811222880479,
    }


@patch(
    "maas_cds.model.datatake.CdsDatatake.find_brother_products_scan", return_value=[]
)
def test_all_expected_nobs(mock_find_brother_products_scan, datatake_s2_dict):
    """Test nobs expected get different value"""

    datatake = CdsDatatakeS2(**datatake_s2_dict)

    datatake.compute_all_local_completeness()
    datatake.compute_global_completeness()

    datatake_dict = datatake.to_dict()

    assert datatake_dict["MSI_L0__GR_local_value"] == 0
    assert datatake_dict["MSI_L1B_DS_local_value"] == 0
    assert datatake_dict["MSI_L1C_DS_local_value"] == 0

    assert datatake_dict["L0__local_value"] == 0

    assert datatake_dict["GR_global_value"] == 0
    assert datatake_dict["final_completeness_value"] == 0


@patch(
    "maas_cds.model.datatake.CdsDatatake.find_brother_products_scan", return_value=[]
)
def test_all_expected_darko(mock_compute_local_value, s2_datatake_dark_o):
    """Test DARK-O expected get different value"""

    s2_datatake_dark_o.compute_all_local_completeness()
    s2_datatake_dark_o.compute_global_completeness()
    s2_datatake_dark_o.compute_extra_completeness()

    datatake_dict = s2_datatake_dark_o.to_dict()

    level_expected = s2_datatake_dark_o.get_expected_product_level()

    assert level_expected == ["L0_", "L1A"]

    assert datatake_dict["MSI_L0__GR_local_expected"] == 156
    assert datatake_dict["MSI_L0__DS_local_expected"] == 46904000
    assert datatake_dict["MSI_L1A_GR_local_expected"] == 132
    assert datatake_dict["MSI_L1A_DS_local_expected"] == 39688000

    assert datatake_dict["L0__local_expected"] == 93808000
    assert datatake_dict["L1A_local_expected"] == 79376000

    assert datatake_dict["GR_global_value"] == 0
    assert datatake_dict["final_completeness_value"] == 0


def test_expected_product_level_0_nobs(datatake_s2_dict):
    """Test expected for product level 0 with nobs"""

    datatake = CdsDatatakeS2(**datatake_s2_dict)

    level0_expected = datatake.get_expected_from_product_level("L0_")
    assert level0_expected == {"DS": 100000000, "GR": 60}


def test_expected_product_level_nobs(datatake_s2_dict):
    """Test expected product level for nobs"""

    datatake = CdsDatatakeS2(**datatake_s2_dict)

    level_expected = datatake.get_expected_product_level()
    assert level_expected == ["L0_", "L1B", "L1C", "L2A"]


def test_expected_product_level_number_scene_under_3(datatake_s2_dict):
    """Test expected product level where the number of scene is under 3"""
    datatake_s2_dict["number_of_scenes"] = 1
    datatake = CdsDatatakeS2(**datatake_s2_dict)

    level_expected = datatake.get_expected_product_level()
    assert level_expected == ["L0_"]


@patch("maas_cds.model.datatake_s2.CdsDatatakeS2.compute_local_value", return_value=0)
def test_all_expected_number_scene_under_3(mock_compute_local_value, datatake_s2_dict):
    """Test all expected where the number of scene is under 3"""

    datatake_s2_dict["number_of_scenes"] = 1
    datatake_s2_dict["instrument_mode"] = "NOBS"
    datatake = CdsDatatakeS2(**datatake_s2_dict)

    datatake.compute_all_local_completeness()
    datatake.compute_global_completeness()

    datatake_dict = datatake.to_dict()

    assert datatake_dict["GR_global_expected"] == 12
    assert datatake_dict["MSI_L0__GR_local_expected"] == 12

    assert datatake_dict.get("TL_global_expected") is None
    assert datatake_dict.get("MSI_L1C_TC_local_expected") is None


@patch("maas_cds.model.datatake.CdsDatatake.find_brother_products_scan")
def test_compute_local_value_1(
    mock_find_brother_products_scan, product_s2_dict, datatake_s2_dict
):
    """Test compute_local_value with produc type GR"""

    product = CdsProduct(**product_s2_dict)

    mock_find_brother_products_scan.return_value = [product]

    datatake_s2_dict["number_of_scenes"] = 1
    datatake = CdsDatatakeS2(**datatake_s2_dict)

    value = datatake.compute_local_value("MSI_L0__GR")

    assert value == 1


@patch("maas_cds.model.datatake.CdsDatatake.find_brother_products_scan")
def test_compute_local_value_2(
    mock_find_brother_products_scan,
    product_s2_dict,
    datatake_s2_dict,
):
    """Test compute_local_value with produc type DS"""

    product = CdsProduct(**product_s2_dict)

    mock_find_brother_products_scan.return_value = [product]

    datatake = CdsDatatakeS2(**datatake_s2_dict)

    value = datatake.compute_local_value("MSI_L0__DS")

    result = (
        (
            datetime.datetime(
                2022, 3, 29, 14, 57, 47, 471000, tzinfo=datetime.timezone.utc
            )
            - datetime.datetime(
                2022, 3, 29, 14, 37, 22, 7000, tzinfo=datetime.timezone.utc
            )
        ).total_seconds()
        * 1000000
        + 3608000
        + 1000000
    )

    assert value == result


@patch("maas_cds.model.datatake.CdsDatatake.find_brother_products_scan")
def test_compute_related_products(
    mock_find_brother_products_scan,
    product_s2_dict,
    datatake_s2_dict,
):
    """Test compute_local_value with produc type DS"""

    product = CdsProduct(**product_s2_dict)

    mock_find_brother_products_scan.return_value = [product]

    datatake = CdsDatatakeS2(**datatake_s2_dict)

    related_products_arg = []
    datatake.compute_local_value("MSI_L0__DS", related_products_arg)

    assert related_products_arg == [
        Period(
            start=datetime.datetime(
                2022, 3, 29, 14, 37, 22, 7000, tzinfo=datetime.timezone.utc
            ),
            end=datetime.datetime(
                2022, 3, 29, 14, 57, 47, 471000, tzinfo=datetime.timezone.utc
            ),
        )
    ]

    datatake.observation_time_start = datatake.observation_time_start.replace(second=12)

    missing_periods_maximal_offset = {
        "S2": {
            "global": 0,
            "local": {
                "MSI_L0__DS": 6000000,
                "default": 0,
            },
        },
    }
    CdsDatatake.MISSING_PERIODS_MAXIMAL_OFFSET = missing_periods_maximal_offset

    datatake.compute_missing_production("MSI_L0__DS", related_products_arg)

    assert datatake.missing_periods[0].to_dict() == {
        "name": "Missing Product",
        "product_type": "MSI_L0__DS",
        "sensing_start_date": "2022-03-29T14:37:12.007Z",
        "sensing_end_date": "2022-03-29T14:37:22.007Z",
        "duration": 10000000,
    }

    missing_periods_maximal_offset = {
        "S2": {
            "global": 0,
            "local": {
                "MSI_L0__DS": 20000000,
                "default": 0,
            },
        },
    }
    CdsDatatake.MISSING_PERIODS_MAXIMAL_OFFSET = missing_periods_maximal_offset

    datatake.compute_missing_production("MSI_L0__DS", related_products_arg)

    assert datatake.missing_periods == []

    CdsDatatake.MISSING_PERIODS_MAXIMAL_OFFSET = None


@patch("maas_cds.lib.periodutils.compute_total_sensing_product")
def test_get_compute_method(mock_compute_total_sensing_product, datatake_s2_dict):
    """Test get_compute_method function"""

    mock_compute_total_sensing_product.return_value = []

    datatake_s2_dict["number_of_scenes"] = 1
    datatake = CdsDatatakeS2(**datatake_s2_dict)

    compute_method = datatake.get_compute_method("MSI_L0__DS")

    assert compute_method is not None


def test_get_compute_method_bad_key(datatake_s2_dict):
    """Test get_compute_method function bad key"""

    datatake_s2_dict["number_of_scenes"] = 1
    datatake = CdsDatatakeS2(**datatake_s2_dict)

    compute_method = datatake.get_compute_method("MSI_L0__AA")

    assert compute_method is None


def test_compute_extra_completeness_1(datatake_s2_dict):
    """Test compute_extra_completeness"""

    datatake_s2_dict["number_of_scenes"] = 1
    datatake = CdsDatatakeS2(**datatake_s2_dict)

    setattr(datatake, "MSI_L0__DS_local_value_adjusted", 1)
    setattr(datatake, "MSI_L0__GR_local_value_adjusted", 1)
    setattr(datatake, "MSI_L0__DS_local_expected", 1)
    setattr(datatake, "MSI_L0__GR_local_expected", 1)

    datatake.compute_extra_completeness()

    assert datatake.L0__local_expected == 2
    assert datatake.L0__local_percentage == 100.0
    assert datatake.L0__local_value == 2
    assert datatake.L0__local_status == CompletenessStatus.COMPLETE.value

    assert datatake.final_completeness_expected == 2
    assert datatake.final_completeness_percentage == 100.0
    assert datatake.final_completeness_value == 2
    assert datatake.final_completeness_status == CompletenessStatus.COMPLETE.value


@patch("maas_cds.model.datatake_s2.CdsDatatakeS2.compute_local_value", return_value=0)
def test_compute_extra_completeness_2(mock_return_value, datatake_s2_dict):
    """Test compute_extra_completeness missing attribut"""

    datatake_s2_dict["number_of_scenes"] = 1
    datatake = CdsDatatakeS2(**datatake_s2_dict)

    setattr(datatake, "MSI_L0__DS_local_expected", 1)
    setattr(datatake, "MSI_L0__DS_local_value_adjusted", 1)

    # Create missing GR
    setattr(datatake, "MSI_L0__GR_local_expected", 1)
    setattr(datatake, "MSI_L0__GR_local_value_adjusted", 0)

    datatake.compute_extra_completeness()

    assert datatake.L0__local_expected == 2
    assert datatake.L0__local_percentage == 50.0
    assert datatake.L0__local_value == 1
    assert datatake.L0__local_status == CompletenessStatus.PARTIAL.value

    assert datatake.final_completeness_expected == 2
    assert datatake.final_completeness_percentage == 50.0
    assert datatake.final_completeness_value == 1
    assert datatake.final_completeness_status == CompletenessStatus.PARTIAL.value


def test_compute_extra_completeness_3(datatake_s2_dict):
    """Test compute_extra_completeness missing attribut"""

    datatake_s2_dict["number_of_scenes"] = 1
    datatake = CdsDatatakeS2(**datatake_s2_dict)

    datatake.compute_extra_completeness()

    assert datatake.L0__local_expected == 0
    assert datatake.L0__local_percentage == 0.0
    assert datatake.L0__local_value == 0
    assert datatake.L0__local_status == CompletenessStatus.MISSING.value

    assert datatake.final_completeness_expected == 0
    assert datatake.final_completeness_percentage == 0.0
    assert datatake.final_completeness_value == 0
    assert datatake.final_completeness_status == CompletenessStatus.MISSING.value


@patch("maas_cds.model.datatake_s2.CdsDatatakeS2.compute_local_value", return_value=0)
@patch(
    "maas_cds.model.datatake.CdsDatatake.find_brother_products_scan", return_value=[]
)
def test_compute_extra_completeness_4(
    mock_find_brother_products_scan,
    mock_compute_value,
):
    datatake_s2_dict = {
        "name": "S2B_MP_ACQ__MTL_20220331T120000_20220418T150000.csv",
        "key": "S2B-26586-2",
        "datatake_id": "26586-2",
        "satellite_unit": "S2B",
        "mission": "S2",
        "observation_time_start": datetime.datetime(
            2022, 4, 9, 6, 7, 28, 873000, tzinfo=datetime.timezone.utc
        ),
        "observation_duration": 64944000,
        "observation_time_stop": datetime.datetime(
            2022, 4, 9, 6, 8, 33, 817000, tzinfo=datetime.timezone.utc
        ),
        "number_of_scenes": 18,
        "absolute_orbit": "26586",
        "relative_orbit": "105",
        "timeliness": "NOMINAL",
        "instrument_mode": "NOBS",
    }
    datatake = CdsDatatakeS2(**datatake_s2_dict)
    datatake.compute_all_local_completeness()
    datatake.compute_global_completeness()
    datatake.compute_extra_completeness()

    datatake_dict = datatake.to_dict()

    assert datatake_dict["MSI_L2A_DS_local_expected"] == 57728000


product_datatake_gr_overlaps_dict = [
    {
        "absolute_orbit": "36249",
        "datatake_id": "36249-4",
        "key": "a92e445bc0f2cd276e839792984fff60",
        "instrument_mode": "NOBS",
        "mission": "S2",
        "name": "S2A_OPER_MSI_L1B_GR_ATOS_20220601T011327_S20220601T000444_D12_N04.00.tar",
        "product_level": "L1B",
        "product_type": "MSI_L1B_GR",
        "satellite_unit": "S2A",
        "site_center": "ATOS",
        "sensing_start_date": "2022-06-01T00:04:44.000Z",
        "sensing_end_date": "2022-06-01T00:04:44.000Z",
        "sensing_duration": 0,
        "timeliness": "NOMINAL",
        "detector_id": "12",
        "prip_id": "af928b8d-5d49-406f-b5ba-81ac4a60d90c",
        "prip_publication_date": "2022-06-01T02:04:44.714Z",
        "prip_service": "PRIP_S2A_ATOS",
        "updateTime": "2022-06-01T02:27:15.581Z",
    },
    {
        "absolute_orbit": "36249",
        "datatake_id": "36249-4",
        "key": "a92e445bc0f2cd276e839792984fff60",
        "instrument_mode": "NOBS",
        "mission": "S2",
        "name": "S2A_OPER_MSI_L1B_GR_ATOS_20220601T011327_S20220601T000444_D12_N04.00.tar",
        "product_level": "L1B",
        "product_type": "MSI_L1B_GR",
        "satellite_unit": "S2A",
        "site_center": "ATOS",
        "sensing_start_date": "2022-06-01T00:04:45.000Z",
        "sensing_end_date": "2022-06-01T00:04:45.000Z",
        "sensing_duration": 0,
        "timeliness": "NOMINAL",
        "detector_id": "12",
        "prip_id": "af928b8d-5d49-406f-b5ba-81ac4a60d90c",
        "prip_publication_date": "2022-06-01T02:04:44.714Z",
        "prip_service": "PRIP_S2A_ATOS",
        "updateTime": "2022-06-01T02:27:15.581Z",
    },
    {
        "absolute_orbit": "36249",
        "datatake_id": "36249-4",
        "key": "a92e445bc0f2cd276e839792984fff60",
        "instrument_mode": "NOBS",
        "mission": "S2",
        "name": "S2A_OPER_MSI_L1B_GR_ATOS_20220601T011327_S20220601T000444_D12_N04.00.tar",
        "product_level": "L1B",
        "product_type": "MSI_L1B_GR",
        "satellite_unit": "S2A",
        "site_center": "ATOS",
        "sensing_start_date": "2022-06-01T00:04:44.999Z",
        "sensing_end_date": "2022-06-01T00:04:44.999Z",
        "sensing_duration": 0,
        "timeliness": "NOMINAL",
        "detector_id": "12",
        "prip_id": "af928b8d-5d49-406f-b5ba-81ac4a60d90c",
        "prip_publication_date": "2022-06-01T02:04:44.714Z",
        "prip_service": "PRIP_S2A_ATOS",
        "updateTime": "2022-06-01T02:27:15.581Z",
    },
]


def product_gr_with_overlap():
    for dict_product in product_datatake_gr_overlaps_dict:
        product = CdsProductS2(**dict_product)
        product.full_clean()
        yield product


@patch(
    "maas_cds.model.datatake_s2.CdsDatatakeS2.find_brother_products_scan",
    return_value=product_gr_with_overlap(),
)
def test_compute_overlap_gr(mock_find_brother_products_scan):
    """test that check if granule overlaps are resolved using tolerance on sensing_start_time"""
    datatake_s2_gr_overlap_dict = {
        "name": "S2B_MP_ACQ__MTL_20220331T120000_20220418T150000.csv",
        "key": "S2B-26586-2",
        "datatake_id": "36249-4",
        "satellite_unit": "S2B",
        "mission": "S2",
        "observation_time_start": "2022-06-01T00:04:44.000Z",
        "observation_duration": 64944000,
        "observation_time_stop": "2022-06-01T00:04:45.000Z",
        "number_of_scenes": 18,
        "absolute_orbit": "26586",
        "relative_orbit": "105",
        "timeliness": "NOMINAL",
        "instrument_mode": "NOBS",
    }
    datatake = CdsDatatakeS2(**datatake_s2_gr_overlap_dict)
    assert len(datatake.get_product_compute_brother("GR")) == 2


@patch("maas_cds.model.datatake_s2.CdsDatatakeS2.search_expected_tiles")
@patch("maas_cds.model.datatake.CdsDatatake.find_brother_products_scan")
def test_compute_from_empty_datatake(
    mock_find_brother_products_scan,
    mock_search_expected_tiles,
    s2_datatake_S2A_38107_1,
):
    mock_find_brother_products_scan.return_value = []
    mock_search_expected_tiles.return_value = []

    s2_datatake_S2A_38107_1.compute_all_local_completeness()

    s2_datatake_S2A_38107_1.compute_global_completeness()

    bulk_action = s2_datatake_S2A_38107_1.to_bulk_action()

    del bulk_action["_source"]["updateTime"]
    assert bulk_action == {
        "_index": "cds-datatake-s1-s2",
        "_op_type": "create",
        "_source": {
            "DS_global_expected": 50512000,
            "DS_global_percentage": 0.0,
            "DS_global_status": "Missing",
            "DS_global_value": 0,
            "DS_global_value_adjusted": 0,
            "GR_global_expected": 96,
            "GR_global_percentage": 0.0,
            "GR_global_status": "Missing",
            "GR_global_value": 0,
            "GR_global_value_adjusted": 0,
            "L0__local_expected": 36080000,
            "L0__local_percentage": 0.0,
            "L0__local_status": "Missing",
            "L0__local_value": 0.0,
            "L1B_local_expected": 21648000,
            "L1B_local_percentage": 0.0,
            "L1B_local_status": "Missing",
            "L1B_local_value": 0.0,
            "L1C_local_expected": 10824000,
            "L1C_local_percentage": 0.0,
            "L1C_local_status": "Missing",
            "L1C_local_value": 0.0,
            "L2A_local_expected": 10824000,
            "L2A_local_percentage": 0.0,
            "L2A_local_status": "Missing",
            "L2A_local_value": 0.0,
            "MSI_L0__DS_duplicated_avg_duration": 0,
            "MSI_L0__DS_duplicated_avg_percentage": 0.0,
            "MSI_L0__DS_duplicated_max_duration": 0,
            "MSI_L0__DS_duplicated_max_percentage": 0.0,
            "MSI_L0__DS_duplicated_min_duration": 0,
            "MSI_L0__DS_duplicated_min_percentage": 0.0,
            "MSI_L0__DS_local_expected": 18040000,
            "MSI_L0__DS_local_percentage": 0.0,
            "MSI_L0__DS_local_status": "Missing",
            "MSI_L0__DS_local_value": 0,
            "MSI_L0__DS_local_value_adjusted": 0,
            "MSI_L0__GR_local_expected": 60,
            "MSI_L0__GR_local_percentage": 0.0,
            "MSI_L0__GR_local_status": "Missing",
            "MSI_L0__GR_local_value": 0,
            "MSI_L0__GR_local_value_adjusted": 0,
            "MSI_L1B_DS_duplicated_avg_duration": 0,
            "MSI_L1B_DS_duplicated_avg_percentage": 0.0,
            "MSI_L1B_DS_duplicated_max_duration": 0,
            "MSI_L1B_DS_duplicated_max_percentage": 0.0,
            "MSI_L1B_DS_duplicated_min_duration": 0,
            "MSI_L1B_DS_duplicated_min_percentage": 0.0,
            "MSI_L1B_DS_local_expected": 10824000,
            "MSI_L1B_DS_local_percentage": 0.0,
            "MSI_L1B_DS_local_status": "Missing",
            "MSI_L1B_DS_local_value": 0,
            "MSI_L1B_DS_local_value_adjusted": 0,
            "MSI_L1B_GR_local_expected": 36,
            "MSI_L1B_GR_local_percentage": 0.0,
            "MSI_L1B_GR_local_status": "Missing",
            "MSI_L1B_GR_local_value": 0,
            "MSI_L1B_GR_local_value_adjusted": 0,
            "MSI_L1C_DS_duplicated_avg_duration": 0,
            "MSI_L1C_DS_duplicated_avg_percentage": 0.0,
            "MSI_L1C_DS_duplicated_max_duration": 0,
            "MSI_L1C_DS_duplicated_max_percentage": 0.0,
            "MSI_L1C_DS_duplicated_min_duration": 0,
            "MSI_L1C_DS_duplicated_min_percentage": 0.0,
            "MSI_L1C_DS_local_expected": 10824000,
            "MSI_L1C_DS_local_percentage": 0.0,
            "MSI_L1C_DS_local_status": "Missing",
            "MSI_L1C_DS_local_value": 0,
            "MSI_L1C_DS_local_value_adjusted": 0,
            "MSI_L2A_DS_duplicated_avg_duration": 0,
            "MSI_L2A_DS_duplicated_avg_percentage": 0.0,
            "MSI_L2A_DS_duplicated_max_duration": 0,
            "MSI_L2A_DS_duplicated_max_percentage": 0.0,
            "MSI_L2A_DS_duplicated_min_duration": 0,
            "MSI_L2A_DS_duplicated_min_percentage": 0.0,
            "MSI_L2A_DS_local_expected": 10824000,
            "MSI_L2A_DS_local_percentage": 0.0,
            "MSI_L2A_DS_local_status": "Missing",
            "MSI_L2A_DS_local_value": 0,
            "MSI_L2A_DS_local_value_adjusted": 0,
            "absolute_orbit": "38107",
            "application_date": "2022-10-06T12:00:00.000Z",
            "datatake_id": "38107-1",
            "final_completeness_expected": 79376000,
            "final_completeness_percentage": 0.0,
            "final_completeness_status": "Missing",
            "final_completeness_value": 0.0,
            "instrument_mode": "NOBS",
            "duplicated_global_max_duration": 0,
            "duplicated_global_max_percentage": 0.0,
            "key": "S2A-38107-1",
            "mission": "S2",
            "name": "S2A_MP_ACQ__MTL_20221006T120000_20221024T150000.csv",
            "number_of_expected_tiles": 0,
            "number_of_scenes": 5,
            "observation_duration": 18040000,
            "observation_time_start": "2022-10-08T22:04:13.716Z",
            "observation_time_stop": "2022-10-08T22:04:31.756Z",
            "relative_orbit": "72",
            "satellite_unit": "S2A",
            "timeliness": "NOMINAL",
        },
    }


def test_datastrip_retrieval(datatake_s2_dict, product_s2_dict):
    """Test datastrip retrieval using retrieve_additional_fields_from_products function"""

    datatake = CdsDatatakeS2(**datatake_s2_dict)

    prodS2 = CdsProductS2(**product_s2_dict)

    prodS2.datastrip_id = "ALPHA"
    prodS2.product_group_id = "ZULU"

    datatake.retrieve_additional_fields_from_product(prodS2)
    assert datatake.datastrip_ids == ["ALPHA"]
    assert datatake.product_group_ids == ["ZULU"]

    prodS2.datastrip_id = "BRAVO"
    prodS2.product_group_id = "YANKEE"
    datatake.retrieve_additional_fields_from_product(prodS2)
    assert datatake.datastrip_ids == ["ALPHA", "BRAVO"]
    assert datatake.product_group_ids == ["ZULU", "YANKEE"]

    prodS2.datastrip_id = ""
    prodS2.product_group_id = ""
    datatake.retrieve_additional_fields_from_product(prodS2)
    assert datatake.datastrip_ids == ["ALPHA", "BRAVO"]
    assert datatake.product_group_ids == ["ZULU", "YANKEE"]

    prodS2.datastrip_id = "DELTA"
    prodS2.product_group_id = "XRAY"
    datatake.retrieve_additional_fields_from_product(prodS2)
    assert datatake.datastrip_ids == ["ALPHA", "BRAVO", "DELTA"]
    assert datatake.product_group_ids == ["ZULU", "YANKEE", "XRAY"]

    # Check no duplicate
    datatake.retrieve_additional_fields_from_product(prodS2)
    assert datatake.datastrip_ids == ["ALPHA", "BRAVO", "DELTA"]
    assert datatake.product_group_ids == ["ZULU", "YANKEE", "XRAY"]
