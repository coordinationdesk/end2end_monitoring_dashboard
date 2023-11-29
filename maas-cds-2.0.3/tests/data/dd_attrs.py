from unittest.mock import patch
import pytest


__all__ = ["dd_attrs"]


@pytest.fixture
def dd_attrs():
    return {
        "DHUS": {
            "raw_data_model": "DdProduct",
            "publication_date": "ddip_publication_date",
            "from_prip_timeliness": "from_prip_ddip_timeliness",
            "product_name": "ddip_name",
            "container_id": "ddip_id",
            "container_name": "ddip_container_name",
        },
        "DAS": {
            "raw_data_model": "DasProduct",
            "publication_date": "dddas_publication_date",
            "from_prip_timeliness": "from_prip_dddas_timeliness",
            "product_name": "dddas_name",
            "container_id": "dddas_id",
            "container_name": "dddas_container_name",
        },
        "CREODIAS": {
            "raw_data_model": "CreodiasProduct",
            "publication_date": "ddcreodias_publication_date",
            "from_prip_timeliness": "from_prip_ddcreodias_timeliness",
            "product_name": "ddcreodias_name",
            "container_id": "ddcreodias_id",
            "container_name": "ddcreodias_container_name",
        },
    }
