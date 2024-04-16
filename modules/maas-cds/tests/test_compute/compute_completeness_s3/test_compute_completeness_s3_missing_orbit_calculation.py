from _pytest.logging import caplog
from copy import deepcopy
import logging
import datetime

from unittest.mock import patch
import pytest
from maas_model.date_utils import datestr_to_utc_datetime, datetime_to_zulu
from opensearchpy import MultiSearch
from maas_cds.lib.parsing_name.utils import DATATAKE_ID_MISSING_VALUE
from maas_cds.model.cds_s3_completeness import CdsS3Completeness
from maas_cds.model.product_s3 import CdsProductS3
from maas_cds.engines.compute.compute_s3_completeness import ComputeS3CompletenessEngine
import maas_cds.model

LOGGER = logging.getLogger("test_compute_completeness_s3_missing_orbit_calculation")


@pytest.fixture
def expected_nb_of_completeness_doc_for_one_datake():
    counter = 0
    for _, v in CdsS3Completeness.S3_PRODUCTS_TYPES.items():
        if v["active"]:
            for _ in v["timeliness"]:
                counter += 1
    return counter

@pytest.fixture
def cds_s3_completeness_dict():
    """Get a basic cds_s3_completeness_dict
    matching
        mission:S3
        satellite_unit:S3B
        datatake_id:S3B-069-007
        product_type:OL_2_LFR___
        timeliness:NT

    Usefull to recreate a CdsS3Completeness
    Returns:
        dict: return a dict of a CdsS3Completeness
    """
    return {
        "key": "S3B-069-007#OL_2_LFR___#NT",
        "datatake_id": "S3B-069-007",
        "mission": "S3",
        "satellite_unit": "S3B",
        "timeliness": "NT",
        "product_type": "OL_2_LFR___",
        "product_level": "L2_",
        "observation_time_start": datestr_to_utc_datetime("2022-08-01T08:26:53.661Z"),
        "observation_time_stop": datestr_to_utc_datetime("2022-08-01T09:11:11.332Z"),
        "value": 2657671000,
        "expected": 2640000000,
        "value_adjusted": 2640000000,
        "percentage": 100,
        "status": "Complete",
        "updateTime": datestr_to_utc_datetime("2022-08-02T00:05:30.143Z"),
    }


@pytest.fixture
def product_s3_dict():
    """Get a basic s3 product dict
        matching
        mission:S3
        satellite_unit:S3B
        datatake_id:S3B-069-007
        product_type:OL_2_LFR___
        timeliness:NT

    Usefull to recreate a CdsProduct

    Returns:
        dict: return a dict of a CdsProduct
    """
    return {
        "datatake_id": "S3B-069-007",
        "key": "19a0270ee034fa34a17d4a8022c0b1a0",
        "mission": "S3",
        "name": "S3B_OL_2_LFR____20220801T090240_20220801T090540_20220801T231518_0179_069_007_3420_PS2_O_NT_002.SEN3.zip",
        "product_level": "L2_",
        "product_type": "OL_2_LFR___",
        "satellite_unit": "S3B",
        "sensing_start_date": datestr_to_utc_datetime("2022-08-01T09:02:40.151Z"),
        "sensing_end_date": datestr_to_utc_datetime("2022-08-01T09:05:40.151Z"),
        "sensing_duration": 180000000,
        "timeliness": "NT",
        "prip_id": "3c6cc078-a7b4-48f8-9bca-fa7d9a88801f",
        "prip_publication_date": datestr_to_utc_datetime("2022-08-01T23:19:42.543Z"),
        "prip_service": "PRIP_S3B_SERCO",
        "updateTime": datestr_to_utc_datetime("2022-08-01T23:52:36.109Z"),
        "ddip_name": "S3B_OL_2_LFR____20220801T090240_20220801T090540_20220801T231518_0179_069_007_3420_PS2_O_NT_002",
        "ddip_publication_date": datestr_to_utc_datetime("2022-08-01T23:23:06.268Z"),
    }


def test_get_datatake_ids_previous_orbits_logic():
    """Check that the function which return all datatake_ids betwen 2 ids is working as expected"""
    assert not ComputeS3CompletenessEngine.generate_datatake_ids_list_between_2_ids(
        "S3B-069-007", "S3B-069-007"
    )

    assert ComputeS3CompletenessEngine.generate_datatake_ids_list_between_2_ids(
        "S3B-069-002", "S3B-068-380"
    ) == [
        "S3B-069-001",
        "S3B-068-385",
        "S3B-068-384",
        "S3B-068-383",
        "S3B-068-382",
        "S3B-068-381",
    ]
    assert ComputeS3CompletenessEngine.generate_datatake_ids_list_between_2_ids(
        "S3B-068-380", "S3B-069-002"
    ) == [
        "S3B-069-001",
        "S3B-068-385",
        "S3B-068-384",
        "S3B-068-383",
        "S3B-068-382",
        "S3B-068-381",
    ]

    assert not ComputeS3CompletenessEngine.generate_datatake_ids_list_between_2_ids(
        "S3B-069-001", "S3B-068-385"
    )
    assert ComputeS3CompletenessEngine.generate_datatake_ids_list_between_2_ids(
        "S3B-069-001", "S3B-068-384"
    ) == [
        "S3B-068-385",
    ]

    # Check function raise exception with bad datatake_id formats
    with pytest.raises(ValueError):
        assert not ComputeS3CompletenessEngine.generate_datatake_ids_list_between_2_ids(
            "Sj3B-069-001", "S3B-068-385"
        )

    with pytest.raises(ValueError):
        assert not ComputeS3CompletenessEngine.generate_datatake_ids_list_between_2_ids(
            "S3B-069-001", "S3B-08-385"
        )

    with pytest.raises(ValueError):
        assert not ComputeS3CompletenessEngine.generate_datatake_ids_list_between_2_ids(
            "S3B-069-001", "S3B-08-45"
        )


@patch("opensearchpy.MultiSearch.add")
@patch("opensearchpy.MultiSearch.execute")
def test_missing_orbit_identification_case_no_previous_orbit_product(
    mock_msearch_execute, mock_msearch_add, product_s3_dict
):
    """Check that when no other product is found in the past for the specific product
    type used to find missing orbit then no missing orbit calculation is performed"""
    mock_msearch_add.return_value = MultiSearch()

    ComputeS3CompletenessEngine.MODEL_MODULE = maas_cds.model
    engine = ComputeS3CompletenessEngine()

    prod_1 = CdsProductS3(**product_s3_dict)
    prod_1.datatake_id = "S3B-069-003"
    prod_1.product_type = engine.PRODUCT_TYPE_TO_USE_FOR_MISSING_ORBIT_DETECTION
    prod_1.full_clean()

    mock_msearch_execute.return_value = [[]]

    engine.products_to_consider_for_missing_orbits = [prod_1]
    result = engine.identify_missing_datatakes_ids()
    assert not result


@patch("opensearchpy.MultiSearch.add")
@patch("opensearchpy.MultiSearch.execute")
def test_missing_orbit_identification_complex_case(
    mock_msearch_execute, mock_msearch_add, product_s3_dict
):
    """Check that when searching for missing datatake_id/orbit completeness document,
    the function is able to find the suitable closest document in past by using both local cache and db
    """
    mock_msearch_add.return_value = MultiSearch()

    ComputeS3CompletenessEngine.MODEL_MODULE = maas_cds.model
    engine = ComputeS3CompletenessEngine()

    prod = []
    for i in range(20):
        prod.append(CdsProductS3(**product_s3_dict))
        prod[-1].datatake_id = f"S3B-069-0{i:02d}"
        prod[-1].product_type = engine.PRODUCT_TYPE_TO_USE_FOR_MISSING_ORBIT_DETECTION
        prod[-1].sensing_start_date = datestr_to_utc_datetime(
            f"2020-01-01T00:00:{i:02d}.000Z"
        )
        prod[-1].sensing_end_date = datestr_to_utc_datetime(
            f"2020-01-01T00:00:{i:02d}.001Z"
        )
        prod[-1].full_clean()

    engine.products_to_consider_for_missing_orbits = [
        prod[3],
        prod[8],
        prod[10],
        prod[11],
        prod[18],
    ]

    mock_msearch_execute.return_value = [
        [prod[1]],
        [prod[6]],
        [prod[7]],
        [
            prod[15]
        ],  # Only 4 db request because case with successive datatake_id product have been
        # filtered without asking db ( prod[10]/prod[11] )
    ]

    result = engine.identify_missing_datatakes_ids()

    # between 3 and 1 => 1 missing datatake (2) => closest is db
    # between 8 and 6 => 1 missing datatake (7) => closest is db
    # between 10 and 8 => 1 missing datatake (9) => closest is local
    # between 11 and 10 => 0 missing => closest is local
    # between 18 and 15 => 2 missing datatake (16 & 17) => cloest is db

    assert len(result) == 5
    assert result[0][0] == prod[2].datatake_id
    assert result[0][1] == prod[3].sensing_start_date - datetime.timedelta(
        minutes=engine.ORBIT_DURATION_IN_MINUTES
    )
    assert result[0][2] == prod[3].sensing_end_date - datetime.timedelta(
        minutes=engine.ORBIT_DURATION_IN_MINUTES
    )

    assert result[1][0] == prod[7].datatake_id
    assert result[1][1] == prod[8].sensing_start_date - datetime.timedelta(
        minutes=engine.ORBIT_DURATION_IN_MINUTES
    )
    assert result[1][2] == prod[8].sensing_end_date - datetime.timedelta(
        minutes=engine.ORBIT_DURATION_IN_MINUTES
    )

    assert result[2][0] == prod[9].datatake_id
    assert result[2][1] == prod[10].sensing_start_date - datetime.timedelta(
        minutes=engine.ORBIT_DURATION_IN_MINUTES
    )
    assert result[2][2] == prod[10].sensing_end_date - datetime.timedelta(
        minutes=engine.ORBIT_DURATION_IN_MINUTES
    )

    assert result[3][0] == prod[17].datatake_id
    assert result[3][1] == prod[18].sensing_start_date - datetime.timedelta(
        minutes=engine.ORBIT_DURATION_IN_MINUTES
    )
    assert result[3][2] == prod[18].sensing_end_date - datetime.timedelta(
        minutes=engine.ORBIT_DURATION_IN_MINUTES
    )

    assert result[4][0] == prod[16].datatake_id
    assert result[4][1] == prod[18].sensing_start_date - 2 * datetime.timedelta(
        minutes=engine.ORBIT_DURATION_IN_MINUTES
    )
    assert result[4][2] == prod[18].sensing_end_date - 2 * datetime.timedelta(
        minutes=engine.ORBIT_DURATION_IN_MINUTES
    )


@patch("opensearchpy.MultiSearch.add")
@patch("opensearchpy.MultiSearch.execute")
def test_missing_orbit_identification_case_no_orbit_missing(
    mock_msearch_execute, mock_msearch_add, product_s3_dict
):
    """Check that the missing datatake_id completeness is not triggered when no datatake_id gap are found"""
    mock_msearch_add.return_value = MultiSearch()

    ComputeS3CompletenessEngine.MODEL_MODULE = maas_cds.model
    engine = ComputeS3CompletenessEngine()

    prod_1 = CdsProductS3(**product_s3_dict)
    prod_1.datatake_id = "S3B-069-003"
    prod_1.product_type = engine.PRODUCT_TYPE_TO_USE_FOR_MISSING_ORBIT_DETECTION
    prod_1.full_clean()

    prod_2 = CdsProductS3(**product_s3_dict)
    prod_2.datatake_id = "S3B-069-002"
    prod_2.product_type = engine.PRODUCT_TYPE_TO_USE_FOR_MISSING_ORBIT_DETECTION
    prod_2.full_clean()

    mock_msearch_execute.return_value = [
        [
            prod_2,
        ]
    ]

    engine.products_to_consider_for_missing_orbits = [prod_1]
    result = engine.identify_missing_datatakes_ids()
    assert not result


@patch(
    "maas_cds.model.CdsS3Completeness.mget_by_ids",
)
def test_add_missing_completeness_documents(mock_getids,expected_nb_of_completeness_doc_for_one_datake):
    """Test that the function used to create empty completeness documents for missing datatake_id is working as expected"""
    ComputeS3CompletenessEngine.MODEL_MODULE = maas_cds.model
    engine = ComputeS3CompletenessEngine()
    mock_getids.side_effect=[[[], []],[[] for _ in range(expected_nb_of_completeness_doc_for_one_datake)],[[] for _ in range(expected_nb_of_completeness_doc_for_one_datake)]]


    dtk_ids_tuples = [
        (
            "S3B-069-003",
            datestr_to_utc_datetime("2021-01-02T00:00:00.000Z"),
            datestr_to_utc_datetime("2022-01-02T00:00:00.000Z"),
        ),
        (
            "S3B-069-002",
            datestr_to_utc_datetime("2023-01-02T00:00:00.000Z"),
            datestr_to_utc_datetime("2024-01-02T00:00:00.000Z"),
        ),
    ]

    assert len(engine.local_cache_completeness) == 0

    engine.add_missing_completeness_documents(dtk_ids_tuples)

    # We added 2 datatake_id so the expected nb of doc is expected *2
    assert len(engine.local_cache_completeness) == expected_nb_of_completeness_doc_for_one_datake * 2

    for i, datatake_id in enumerate(("S3B-069-003", "S3B-069-002")):
        for prod_type, v in CdsS3Completeness.S3_PRODUCTS_TYPES.items():
            if v["active"]:
                for timeliness in v["timeliness"]:
                    key = datatake_id + "#" + prod_type + "#" + timeliness
                    assert key in engine.local_cache_completeness

                    if (
                        prod_type
                        == engine.PRODUCT_TYPE_TO_USE_FOR_MISSING_ORBIT_DETECTION
                    ):
                        assert engine.local_cache_completeness[key][0].to_dict() == {
                            "datatake_id": datatake_id,
                            "key": key,
                            "mission": "S3",
                            "observation_time_start": datetime_to_zulu(
                                dtk_ids_tuples[i][1]
                            ),
                            "observation_time_stop": datetime_to_zulu(
                                dtk_ids_tuples[i][2]
                            ),
                            "product_level": "L0_",
                            "product_type": "TM_0_NAT___",
                            "satellite_unit": "S3B",
                            "timeliness": "AL",
                        }


@patch("maas_cds.model.CdsS3Completeness.mget_by_ids")
def test_completeness_document_loading(mock_getids, product_s3_dict,expected_nb_of_completeness_doc_for_one_datake,caplog):
    """Test the loading of all completeness document 'creation or loading from db' at the start of the action iterator"""

    ComputeS3CompletenessEngine.MODEL_MODULE = maas_cds.model
    engine = ComputeS3CompletenessEngine()

    prod_length = 10
    prods = []
    for i in range(prod_length):
        prods.append(CdsProductS3(**product_s3_dict))
        prods[-1].datatake_id = f"S3B-069-0{i:02d}"

    prods[-1].product_type = (
        ComputeS3CompletenessEngine.PRODUCT_TYPE_TO_USE_FOR_MISSING_ORBIT_DETECTION
    )
    prods[-1].timeliness = "AL"

    mock_getids.side_effect=[[
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    ],[[] for _ in range(expected_nb_of_completeness_doc_for_one_datake)]]


    engine.load_all_completeness_doc(prods)

    assert engine.products_to_consider_for_missing_orbits == [prods[-1]]

    # The ingestion of a product with type PRODUCT_TYPE_TO_USE_FOR_MISSING_ORBIT_DETECTION lead to creation of a completeness doc for each product of the datatake
    # The ingestion of a product with another type lead to creation of a completeness doc only for itself
    assert len(engine.local_cache_completeness.keys()) == (prod_length - 1) + expected_nb_of_completeness_doc_for_one_datake


    # Check no loading with missing datatake_id
    engine2 = ComputeS3CompletenessEngine()
    assert len(engine2.local_cache_completeness.keys()) == 0
    prods[0].datatake_id = ""
    prods[1].datatake_id = DATATAKE_ID_MISSING_VALUE
    engine2.load_all_completeness_doc(prods[:2])
    assert len(engine2.local_cache_completeness.keys()) == 0

    # Check no loading with wrong product type or wrong timeliness
    prods[2].product_type = "ALPHA"
    prods[3].timeliness = "BRAVO"
    engine2.load_all_completeness_doc([prods[2], prods[3]])
    assert len(engine2.local_cache_completeness.keys()) == 0

    # Check no doc creation if db return a value and is not in local cache
    existing_prod_in_db = CdsProductS3(**product_s3_dict)
    existing_prod_in_db.datatake_id = "S3B-500-000"
    prods[5].datatake_id = "S3B-500-000"
    key = existing_prod_in_db.get_compute_key()
    mock_getids.side_effect = [[existing_prod_in_db]]
    engine3 = ComputeS3CompletenessEngine()

    with caplog.at_level(logging.DEBUG):
        engine3.load_all_completeness_doc([prods[5]])
        assert (
            f"[CACHE] - key found in cds-s3-completeness index, using the one from DB : {existing_prod_in_db.get_compute_key()}"
            in caplog.records[-1].message
        )

    # Check no doc creation if db return a value and is in local cache
    existing_prod_in_db = CdsProductS3(**product_s3_dict)
    existing_prod_in_db.datatake_id = "S3B-500-001"
    local_cache = deepcopy(existing_prod_in_db)
    prods[6].datatake_id = "S3B-500-001"
    key = existing_prod_in_db.get_compute_key()
    mock_getids.side_effect = [[existing_prod_in_db]]
    engine4 = ComputeS3CompletenessEngine()
    engine4.local_cache_completeness[key] = (local_cache, None)

    with caplog.at_level(logging.DEBUG):
        engine4.load_all_completeness_doc([prods[6]])
        assert (
            f"[CACHE] - key found in local cache, no document to create for {existing_prod_in_db.get_compute_key()}"
            in caplog.records[-1].message
        )
