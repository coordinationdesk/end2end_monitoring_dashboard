from maas_cds.engines.reports import MetricsProductConsolidatorEngine
from maas_cds import model
from maas_engine.engine import Engine
from maas_cds import model
import pytest


@pytest.fixture
def init_engine(monkeypatch):
    def get_model_mock(*args, **kwargs):
        return model.CdsMetricsProduct

    monkeypatch.setattr(Engine, "get_model", get_model_mock)
    engine = MetricsProductConsolidatorEngine(target_model="CdsMetricsProduct")

    return engine


def test_consolidate_s1(s1_archived_product_metrics, init_engine):
    engine = init_engine

    metrics = engine.consolidate(s1_archived_product_metrics, model.CdsMetricsProduct())
    metrics.full_clean()
    metrics_dict = metrics.to_dict()

    expected_metrics = {
        "name": "Archived.WV_RAW__0N.SENTINEL-1.A.size",
        "timestamp": "2023-04-06T08:30:00.560Z",
        "counter": 6446299846,
        "metric_name": "archived",
        "metric_type": "Counter",
        "metric_sub_type": "size",
        "product_type": "WV_RAW__0N",
        "mission": "S1",
        "satellite_unit": "S1A",
        "production_service_name": "Exprivia",
    }

    assert metrics_dict == expected_metrics


def test_consolidate_s2(s2_download_product_metrics, init_engine):
    engine = init_engine

    metrics = engine.consolidate(s2_download_product_metrics, model.CdsMetricsProduct())
    metrics.full_clean()
    metrics_dict = metrics.to_dict()

    expected_metrics = {
        "counter": 36208640,
        "interface_name": "metrics_LTA_Exprivia_S2",
        "metric_type": "Counter",
        "name": "Download.MSI_L0__DS.SENTINEL-2.A.s2b_ps_cap.size",
        "production_service_name": "Exprivia",
        "production_service_type": "LTA",
        "timestamp": "2024-09-05T11:30:00.581Z",
        "metric_name": "download",
        "metric_sub_type": "size",
        "product_type": "MSI_L0__DS",
        "satellite_unit": "S2A",
        "service_name": "s2b_ps_cap",
        "mission": "S2",
    }

    assert metrics_dict == expected_metrics


def test_consolidate_s5p(s5p_archived_product_metrics, init_engine):
    engine = init_engine

    metrics = engine.consolidate(
        s5p_archived_product_metrics, model.CdsMetricsProduct()
    )

    assert metrics is None

    # metrics.full_clean()
    # metrics_dict = metrics.to_dict()

    # expected_metrics = {
    #     "name": "Archived.VIIRS_CM._.size",
    #     "timestamp": "2023-04-06T08:30:00.560Z",
    #     "counter": 6446299846,
    #     "metric_name": "archived",
    #     "metric_type": "Counter",
    #     "metric_sub_type": "size",
    #     "product_type": "VIIRS_CM",
    #     "mission": "S5",
    #     "satellite_unit": "S5P",
    #     "production_service_name": "S5P_DLR",
    # }

    # assert metrics_dict == expected_metrics


def test_consolidate_s5p_exprivia(s5p_product_metrics_exprivia, init_engine):
    engine = init_engine

    metrics = engine.consolidate(
        s5p_product_metrics_exprivia, model.CdsMetricsProduct()
    )
    metrics.full_clean()
    metrics_dict = metrics.to_dict()

    expected_metrics = {
        "name": "Archived._AUX_CTM_CO.SENTINEL-5P.P.count",
        "timestamp": "2023-04-06T08:30:00.560Z",
        "counter": 6446299846,
        "metric_name": "archived",
        "metric_type": "Counter",
        "metric_sub_type": "count",
        "product_type": "_AUX_CTM_CO",
        "mission": "S5",
        "satellite_unit": "S5P",
        "production_service_name": "Exprivia",
    }

    assert metrics_dict == expected_metrics
