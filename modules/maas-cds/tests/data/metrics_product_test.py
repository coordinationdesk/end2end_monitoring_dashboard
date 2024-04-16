import pytest
from maas_cds.model import MetricsProduct

s1_product_metrics_dict = {
    "name": "Archived.WV_RAW__0N.SENTINEL-1.A.size",
    "timestamp": "2023-04-06T08:30:00.560000Z",
    "metric_type": "Counter",
    "counter": 6446299846,
    "production_service_name": "Exprivia",
}


s5p_product_metrics_dict = {
    "name": "Archived.VIIRS_CM._.size",
    "timestamp": "2023-04-06T08:30:00.560000Z",
    "metric_type": "Counter",
    "counter": 6446299846,
    "production_service_name": "S5P_DLR",
}


@pytest.fixture
def s1_product_metrics():
    return MetricsProduct(**s1_product_metrics_dict)


@pytest.fixture
def s5p_product_metrics():
    return MetricsProduct(**s5p_product_metrics_dict)
