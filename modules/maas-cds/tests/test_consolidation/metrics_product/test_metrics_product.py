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


def test_consolidate_s1(s1_product_metrics, init_engine):
    engine = init_engine

    metrics = engine.consolidate(s1_product_metrics, model.CdsMetricsProduct())
    metrics.full_clean()
    metrics_dict = metrics.to_dict()

    expected_metrics = {
        "name": "Archived.WV_RAW__0N.SENTINEL-1.A.size",
        "timestamp": "2023-04-06T08:30:00.560Z",
        "counter": 6446299846,
        "metric_type": "Counter",
        "metric_sub_type": "size",
        "product_type": "WV_RAW__0N",
        "mission": "S1",
        "satellite_unit": "S1A",
        "production_service_name": "Exprivia",
    }

    assert metrics_dict == expected_metrics


def test_consolidate_s5p(s5p_product_metrics, init_engine):
    engine = init_engine

    metrics = engine.consolidate(s5p_product_metrics, model.CdsMetricsProduct())
    metrics.full_clean()
    metrics_dict = metrics.to_dict()

    expected_metrics = {
        "name": "Archived.VIIRS_CM._.size",
        "timestamp": "2023-04-06T08:30:00.560Z",
        "counter": 6446299846,
        "metric_type": "Counter",
        "metric_sub_type": "size",
        "product_type": "VIIRS_CM",
        "mission": "S5",
        "satellite_unit": "S5P",
        "production_service_name": "S5P_DLR",
    }

    assert metrics_dict == expected_metrics
