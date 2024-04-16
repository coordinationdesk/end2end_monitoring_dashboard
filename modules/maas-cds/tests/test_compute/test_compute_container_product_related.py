import datetime
import logging
from unittest.mock import patch
from maas_cds.engines.compute.compute_container_products import (
    ComputeContainerProductsEngine,
)
import maas_cds.model
from maas_cds.model.generated import CdsProduct, CdsPublication
from opensearchpy import MultiSearch
import pytest


@pytest.fixture
def s2_cdspublication():
    datadict = {
        "service_id": "DAS",
        "sensing_start_date": datetime.datetime(
            2022, 12, 7, 15, 0, 30, 000000, tzinfo=datetime.timezone.utc
        ),
        "publication_date": datetime.datetime(
            2032, 12, 7, 15, 0, 30, 000000, tzinfo=datetime.timezone.utc
        ),
        "name": "S2CDSPUBLINAME",
    }
    publi = CdsPublication(**datadict)
    publi.full_clean()
    publi.meta.id = "publimetaid"
    return publi


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
        }
    }


@patch("opensearchpy.MultiSearch.add")
@patch("opensearchpy.MultiSearch.execute")
def test_action_iterator(
    mock_msearch_execute,
    mock_msearch_add,
    s2_cdspublication,
    ddattr,
):
    """Check nominal work of action iterator with a valid input document"""

    mock_msearch_add.return_value = MultiSearch()
    mock_msearch_execute.return_value = [[s2_cdspublication]]

    inp = CdsProduct()
    inp.sensing_start_date = datetime.datetime(
        2023, 12, 7, 15, 0, 30, 000000, tzinfo=datetime.timezone.utc
    )

    ComputeContainerProductsEngine.MODEL_MODULE = maas_cds.model
    engine = ComputeContainerProductsEngine(dd_attrs=ddattr)
    engine.input_documents = [inp]

    out = list(engine.action_iterator())[0]
    assert (
        out["_source"]["dddas_publication_date"]
        == s2_cdspublication.to_dict()["publication_date"]
    )
    assert out["_source"]["dddas_id"] == s2_cdspublication.meta.id
    assert out["_source"]["dddas_container_name"] == s2_cdspublication.name


@patch("opensearchpy.MultiSearch.add")
@patch("opensearchpy.MultiSearch.execute")
def test_action_iterator_case_no_doc_found(
    mock_msearch_execute, mock_msearch_add, ddattr, caplog
):
    """Test action iterator case where no publication is found"""

    mock_msearch_add.return_value = MultiSearch()
    mock_msearch_execute.return_value = [[]]

    inp = CdsProduct()
    inp.sensing_start_date = datetime.datetime(
        2023, 12, 7, 15, 0, 30, 000000, tzinfo=datetime.timezone.utc
    )
    inp.name = "input_doc_name"
    ComputeContainerProductsEngine.MODEL_MODULE = maas_cds.model
    engine = ComputeContainerProductsEngine(dd_attrs=ddattr)
    engine.input_documents = [inp]

    with caplog.at_level(logging.DEBUG):
        assert len(list(engine.action_iterator())) == 0
        assert (
            f"document: no container found yet for {inp.name}"
            in caplog.records[-1].message
        )


@patch("opensearchpy.MultiSearch.add")
@patch("opensearchpy.MultiSearch.execute")
def test_action_iterator_case_no_dd_attr_avail(
    mock_msearch_execute, mock_msearch_add, s2_cdspublication, caplog
):
    """Check action iterator when ddattr is None"""

    s2_cdspublication.service_id = "ContainerServId"

    mock_msearch_add.return_value = MultiSearch()
    mock_msearch_execute.return_value = [[s2_cdspublication]]

    inp = CdsProduct()
    inp.name = "InpDocName"
    inp.sensing_start_date = datetime.datetime(
        2023, 12, 7, 15, 0, 30, 000000, tzinfo=datetime.timezone.utc
    )

    ComputeContainerProductsEngine.MODEL_MODULE = maas_cds.model
    engine = ComputeContainerProductsEngine(dd_attrs=None)
    engine.input_documents = [inp]

    with caplog.at_level(logging.ERROR):
        assert len(list(engine.action_iterator())) == 0
        assert (
            f"Unknown dd service_id name : {s2_cdspublication.service_id}. "
            f"Cannot associate with container for product : {inp.name}."
            in caplog.records[-1].message
        )
