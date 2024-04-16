import logging
from unittest.mock import patch
from maas_cds.lib.dateutils import get_microseconds_delta
import maas_cds.model
from maas_cds.engines.compute.compute_container_related import (
    ComputeContainerRelatedEngine,
)
from opensearchpy import MultiSearch
import pytest


@pytest.fixture
def ddattr():
    return {
        "DAS": {
            "raw_data_model": "DasProduct",
            "publication_date": "dddas_publication_date",
            "from_prip_timeliness": "from_prip_dddas_timeliness",
            "product_name": "dddas_name",
            "container_id": "dddas_id",
            "container_name": "dddas_container_name",
        },
    }


@patch("opensearchpy.MultiSearch.add")
@patch("opensearchpy.MultiSearch.execute")
@patch("maas_cds.model.CdsProductS2.mget_by_ids")
def test_action_iterator(
    mock_getids,
    mock_msearch_execute,
    mock_msearch_add,
    s2_raw_product_l1c_container_das,
    s2_l1c_ds_product_S2A_38107_1,
    ddattr,
):
    """Check nominal work of action iterator with a valid input document"""
    s2prod = s2_l1c_ds_product_S2A_38107_1
    s2prod.meta.id = "s2prodmetaid"

    mock_msearch_add.return_value = MultiSearch()
    mock_msearch_execute.return_value = [[s2_l1c_ds_product_S2A_38107_1]]
    mock_getids.return_value = [s2_l1c_ds_product_S2A_38107_1]

    ComputeContainerRelatedEngine.MODEL_MODULE = maas_cds.model
    engine = ComputeContainerRelatedEngine(target_model="DdProduct", dd_attrs=ddattr)
    engine.input_documents = [s2_raw_product_l1c_container_das]
    out = list(engine.action_iterator())
    assert len(out) == 1
    assert out[0]["_source"]["dddas_id"] == s2_raw_product_l1c_container_das.product_id
    assert (
        out[0]["_source"]["dddas_container_name"]
        == s2_raw_product_l1c_container_das.product_name
    )
    assert (
        out[0]["_source"]["dddas_publication_date"]
        == s2_raw_product_l1c_container_das.to_dict()["publication_date"]
    )
    assert out[0]["_source"]["from_prip_dddas_timeliness"] == get_microseconds_delta(
        s2_raw_product_l1c_container_das.publication_date,
        s2_l1c_ds_product_S2A_38107_1.prip_publication_date,
    )


@patch("opensearchpy.MultiSearch.add")
@patch("opensearchpy.MultiSearch.execute")
@patch("maas_cds.model.CdsProductS2.mget_by_ids")
def test_action_iterator_case_no_ddattr(
    mock_getids,
    mock_msearch_execute,
    mock_msearch_add,
    s2_raw_product_l1c_container_das,
    s2_l1c_ds_product_S2A_38107_1,
    ddattr,
    caplog,
):
    """Check action iterator behavior when dd_attrs has no key for the production service
    name of the input document"""

    # Set a bad production service name in the input document so that dd_attrs has not related key
    inp = s2_raw_product_l1c_container_das
    inp.production_service_name = "BADPRODNAME"

    s2prod = s2_l1c_ds_product_S2A_38107_1
    s2prod.meta.id = "s2prodmetaid"

    mock_msearch_add.return_value = MultiSearch()
    mock_msearch_execute.return_value = [[s2prod]]
    mock_getids.return_value = [s2_l1c_ds_product_S2A_38107_1]

    ComputeContainerRelatedEngine.MODEL_MODULE = maas_cds.model
    engine = ComputeContainerRelatedEngine(target_model="DdProduct", dd_attrs=ddattr)
    engine.input_documents = [inp]

    with caplog.at_level(logging.WARNING):
        assert len(list(engine.action_iterator())) == 0
        assert (
            "Unhandle dd config for service BADPRODNAME" in caplog.records[-1].message
        )


@patch("opensearchpy.MultiSearch.add")
@patch("opensearchpy.MultiSearch.execute")
@patch("maas_cds.model.CdsProductS2.mget_by_ids")
def test_action_iterator_case_no_S2_product_found(
    mock_getids,
    mock_msearch_execute,
    mock_msearch_add,
    s2_raw_product_l1c_container_das,
    ddattr,
    caplog,
):
    mock_msearch_add.return_value = MultiSearch()
    mock_msearch_execute.return_value = [[]]
    mock_getids.return_value = []

    ComputeContainerRelatedEngine.MODEL_MODULE = maas_cds.model
    engine = ComputeContainerRelatedEngine(target_model="DdProduct", dd_attrs=ddattr)
    engine.input_documents = [s2_raw_product_l1c_container_das]

    with caplog.at_level(logging.WARNING):
        assert len(list(engine.action_iterator())) == 0
        assert "No S2 product found container" in caplog.records[-1].message


def test_action_iterator_case_bad_product_name(
    s2_raw_product_l1c_container_das,
    ddattr,
    caplog,
):
    inp = s2_raw_product_l1c_container_das
    inp.product_name = "BAD PRODUCT NAME"

    ComputeContainerRelatedEngine.MODEL_MODULE = maas_cds.model
    engine = ComputeContainerRelatedEngine(target_model="DdProduct", dd_attrs=ddattr)
    engine.input_documents = [s2_raw_product_l1c_container_das]

    with caplog.at_level(logging.WARNING):
        assert len(list(engine.action_iterator())) == 0
        assert (
            f"Cannot parse product name: {inp.product_name}"
            in caplog.records[-2].message
        )
        assert "No valid input documents" in caplog.records[-1].message


@pytest.mark.parametrize(
    "prod_level",
    [
        ("L1C", True),
        ("L2A", True),
        ("L4A", False),
        ("L3A", False),
    ],
)
@patch("opensearchpy.MultiSearch.add")
@patch("opensearchpy.MultiSearch.execute")
@patch("maas_cds.model.CdsProductS2.mget_by_ids")
def test_action_iterator_bad_product_level(
    mock_getids,
    mock_msearch_execute,
    mock_msearch_add,
    s2_raw_product_l1c_container_das,
    s2_l1c_ds_product_S2A_38107_1,
    ddattr,
    prod_level,
    caplog,
):
    inp = s2_raw_product_l1c_container_das
    inp.product_name = inp.product_name.replace("L1C", prod_level[0])
    s2prod = s2_l1c_ds_product_S2A_38107_1
    s2prod.meta.id = "prodId"

    mock_msearch_add.return_value = MultiSearch()
    mock_msearch_execute.return_value = [[s2prod]]
    mock_getids.return_value = []

    ComputeContainerRelatedEngine.MODEL_MODULE = maas_cds.model
    engine = ComputeContainerRelatedEngine(target_model="DdProduct", dd_attrs=ddattr)
    engine.input_documents = [s2_raw_product_l1c_container_das]

    with caplog.at_level(logging.WARNING):
        list(engine.action_iterator())
        if prod_level[1]:
            assert len(caplog.records) == 0
        else:
            assert (
                f"Product level {prod_level[0]} is not handled by S2_CONTAINED_TYPE"
                in caplog.records[-2].message
            )
            assert "No valid input documents" in caplog.records[-1].message
