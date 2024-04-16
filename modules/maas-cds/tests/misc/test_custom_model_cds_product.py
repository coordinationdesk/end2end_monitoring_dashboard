import datetime
from unittest.mock import patch


from maas_cds.model.product_s2 import CdsProductS2
from maas_cds.model.cds_s3_completeness import CdsS3Completeness
from maas_cds.model.product_s5 import CdsProductS5
from maas_model import datestr_to_utc_datetime
from maas_cds.lib.queryutils.find_datatake_from_product_group_id import (
    extract_data_from_product_id,
)
import pytest


@patch("maas_cds.model.product_s2.CdsProductS2.find_datatake_id")
def test_cds_s2_custom_model_part1(mock_find_dtk, s2_product_olqc_report):
    product = s2_product_olqc_report

    # Case wrong product type defined
    product.product_type = "WRONGVAL"
    assert s2_product_olqc_report.get_compute_key() is None

    # Check get_datatake_id return None if datatake_id has not been found
    assert s2_product_olqc_report.get_datatake_id() is None

    # Check get_compute_key return NONE if datatake_id not available
    for x in ["testGR", "testTL", "testTC", "testDS"]:
        product.product_type = x
        assert s2_product_olqc_report.get_compute_key() is None

    # Check get_datatake_id return the datatake_id is it has already been found previously
    product.datatake_id = "1234"
    assert (
        s2_product_olqc_report.get_datatake_id()
        == f"{product.satellite_unit}-{product.datatake_id}"
    )

    # Check get_compute_key return a tuple with the datatake_id and the product type
    # when datatake_id and product_type are valid
    for x in ["testGR", "testTL", "testTC", "testDS"]:
        product.product_type = x
        assert s2_product_olqc_report.get_compute_key() == (
            f"{product.satellite_unit}-{product.datatake_id}",
            product.product_type,
        )


@patch("opensearchpy.Search.execute")
def test_cds_s2_custom_model_part2(
    find_mock,
    s2_product_olqc_report,
    s2_product_l0_gr,
    s2_datatake_S2A_38107_1,
    s2_datatake_dark_o,
):
    # Check find_datatake_id does not perform search for product
    #  that are not attached to any datastrip
    for x in CdsProductS2.NO_DATATAKE_PRODUCT_TYPES:
        product = s2_product_olqc_report
        product.product_type = x
        product.datatake_id = None
        product.find_datatake_id()
        assert product.datatake_id is None

    # Check no datake_id is defined if find_datatake_from_sensing return empty list
    find_mock.return_value = []
    product = s2_product_l0_gr
    product.datatake_id = "AZERTY"
    product.find_datatake_id()
    assert product.datatake_id is None
    assert product.nb_datatake_document_that_match == 0

    # Check that when multiple document are found using find_datatake_from_sensing then only the
    # first one returned is used for datatake_id
    out_dtk_1 = s2_datatake_S2A_38107_1
    out_dtk_1.datatake_id = "out_dtk_1"
    out_dtk_2 = s2_datatake_dark_o
    out_dtk_2.datatake_id = "out_dtk_2"

    find_mock.return_value = [out_dtk_2, out_dtk_1]
    product = s2_product_l0_gr
    product.datatake_id = "AZERTY"
    product.find_datatake_id()

    assert product.nb_datatake_document_that_match == 2
    assert product.datatake_id == "out_dtk_2"


def test_cds_s2_product_group_data_extraction():

    # Check no datake_id is defined if find_datatake_from_sensing return empty list

    data_dict = extract_data_from_product_id("GS2A_20240207T101201_045064_N05.10")

    assert data_dict == {
        "satellite_unit": "S2A",
        "date": datetime.datetime(2024, 2, 7, 10, 12, 1),
        "absolute_orbit": "45064",
        "instrument": "N05.10",
    }

    # Check exception triggered with bad date
    with pytest.raises(ValueError):
        extract_data_from_product_id("GS2A_20x240207T101201_045064_N05.10")

    # Check exception triggered with bad format
    with pytest.raises(ValueError):
        extract_data_from_product_id("GS2A_20240207T101201045064_N05.10")

    with pytest.raises(ValueError):
        extract_data_from_product_id("GS2A_aa_20240207T101201045064_N05.10")

    with pytest.raises(ValueError):
        extract_data_from_product_id("GS2A_aa_20240207T101201045064")

    with pytest.raises(ValueError):
        extract_data_from_product_id("20240207T101201_GS2A_045064_N05.10")


@patch(
    "maas_cds.model.cds_s3_completeness.CdsS3Completeness.is_exclude_for_completeness"
)
def test_cds_s3_custom_model(mock_exclude, s3_product_aux_2):
    product = s3_product_aux_2
    product.meta.id = "test_meta_id_value"
    # Check get_datatake_id return field datatake_id if it exist else None
    product.datatake_id = "TESTVAL"
    assert product.get_datatake_id() == "TESTVAL"
    del product.datatake_id
    assert product.get_datatake_id() is None

    # Check if datatake_id or product_type or timeliness is None then compute key returned is None
    mock_exclude.return_value = False
    for x in (("a", "b", None), ("a", None, "c"), (None, "b", "c")):
        product.product_type = x[0]
        product.timeliness = x[1]
        product.datatake_id = x[2]
        assert product.get_compute_key() is None

    # Check nominal case get_compute_key with valid inputs
    product.product_type = "test_production_type"
    product.timeliness = "test_timeliness"
    product.datatake_id = "test_datatake_id"
    assert (
        product.get_compute_key()
        == f"{product.datatake_id}#{product.product_type}#{product.timeliness}"
    )

    # Check that the compute key returned is None for product_type in exclude list
    mock_exclude.return_value = True
    assert product.get_compute_key() is None
    mock_exclude.return_value = False

    # Check data_for_completeness return a subset of keys
    res = product.data_for_completeness()
    assert res == {
        "key": f"{product.datatake_id}#{product.product_type}#{product.timeliness}",
        "datatake_id": product["datatake_id"],
        "mission": product["mission"],
        "satellite_unit": product["satellite_unit"],
        "timeliness": product["timeliness"],
        "product_type": product["product_type"],
        "product_level": product["product_level"],
        "observation_time_start": product["sensing_start_date"],
        "observation_time_stop": product["sensing_end_date"],
    }


@patch(
    "maas_cds.model.cds_s5_completeness.CdsS5Completeness.is_exclude_for_completeness"
)
def test_cds_s5_custom_model(
    mock_exclude,
):
    dict_data = {
        "absolute_orbit": 25100,
        "datatake_id": "S5P-25100",
        "key": "fce60c4156201436b2a90ed3da60f021",
        "mission": "S5",
        "name": "S5P_NRTI_L1B_ENG_DB_20220817T134212_20220817T134724_25100_03_020100_20220817T143010.nc",
        "product_level": "L1_",
        "product_type": "NRTI_L1B_ENG_DB",
        "satellite_unit": "S5P",
        "collection_number": "03",
        "processor_version": "020100",
        "sensing_start_date": datestr_to_utc_datetime("2022-08-17T13:41:19.000Z"),
        "sensing_end_date": datestr_to_utc_datetime("2022-08-17T13:48:23.000Z"),
        "sensing_duration": 424000000,
        "timeliness": "NRTI",
        "prip_id": "50cadbdb-a1e0-48f9-b678-38d75f0bc8bd",
        "prip_publication_date": datestr_to_utc_datetime("2022-08-17T14:37:11.877Z"),
        "prip_service": "PRIP_S5P_DLR",
        "updateTime": datestr_to_utc_datetime("2022-08-17T15:13:44.937Z"),
    }

    product = CdsProductS5(**dict_data)
    product.meta.id = "test_meta_id_value"

    # Check get_datatake_id return field datatake_id
    product.datatake_id = "TESTVAL"
    assert product.get_datatake_id() == "TESTVAL"

    # Check if datatake_id or product_type or timeliness is None then compute key returned is None
    mock_exclude.return_value = False

    for x in (
        ("a", "b", "c", None),
        ("a", "b", None, "d"),
        ("a", None, "c", "d"),
        (None, "b", "c", "d"),
    ):
        product.product_type = x[0]
        product.mission = x[1]
        product.datatake_id = x[2]
        product.absolute_orbit = x[3]
        assert product.get_compute_key() is None

    # Check nominal case get_compute_key with valid inputs
    product.product_type = "test_production_type"
    product.absolute_orbit = "test_absolut_orbit"
    product.mission = "test_mission"
    product.datatake_id = "test_datatake_id"
    assert product.get_compute_key() == f"{product.datatake_id}-{product.product_type}"

    # Check that the compute key returned is None for product_type in exclude list
    mock_exclude.return_value = True
    assert product.get_compute_key() is None
    mock_exclude.return_value = False

    # Check data_for_completeness return a subset of keys
    res = product.data_for_completeness()
    assert res == {
        "key": f"{product.datatake_id}-{product.product_type}",
        "datatake_id": product["datatake_id"],
        "mission": product["mission"],
        "absolute_orbit": product["absolute_orbit"],
        "satellite_unit": product["satellite_unit"],
        "timeliness": product["timeliness"],
        "product_type": product["product_type"],
        "product_level": product["product_level"],
        "observation_time_start": product["sensing_start_date"],
        "observation_time_stop": product["sensing_end_date"],
    }
