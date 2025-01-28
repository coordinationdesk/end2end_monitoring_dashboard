import pytest
from maas_cds.model import MetricsProduct

s1_archived_product_metrics_dict = {
    "name": "Archived.WV_RAW__0N.SENTINEL-1.A.size",
    "timestamp": "2023-04-06T08:30:00.560000Z",
    "metric_type": "Counter",
    "counter": 6446299846,
    "production_service_name": "Exprivia",
}

s2_download_product_metrics_dict = {
    "reportName": "https://lta.exprivia.copernicus.eu/s2",
    "name": "Download.MSI_L0__DS.SENTINEL-2.A.s2b_ps_cap.size",
    "timestamp": "2024-09-05T11:30:00.581Z",
    "metric_type": "Counter",
    "counter": 36208640,
    "interface_name": "metrics_LTA_Exprivia_S2",
    "production_service_type": "LTA",
    "production_service_name": "Exprivia",
    "ingestionTime": "2024-09-05T11:54:52.919Z",
}

s5p_archived_product_metrics_dict = {
    "name": "Archived.VIIRS_CM._.size",
    "timestamp": "2023-04-06T08:30:00.560000Z",
    "metric_type": "Counter",
    "counter": 6446299846,
    "production_service_name": "S5P_DLR",
}

s5p_product_metrics_exprivia_dict = {
    "name": "Archived._AUX_CTM_CO.SENTINEL-5P.P.count",
    "timestamp": "2023-04-06T08:30:00.560000Z",
    "metric_type": "Counter",
    "counter": 6446299846,
    "production_service_name": "Exprivia",
}


@pytest.fixture
def s1_archived_product_metrics():
    return MetricsProduct(**s1_archived_product_metrics_dict)


@pytest.fixture
def s2_download_product_metrics():
    return MetricsProduct(**s2_download_product_metrics_dict)


@pytest.fixture
def s5p_archived_product_metrics():
    return MetricsProduct(**s5p_archived_product_metrics_dict)


@pytest.fixture
def s5p_product_metrics_exprivia():
    return MetricsProduct(**s5p_product_metrics_exprivia_dict)
