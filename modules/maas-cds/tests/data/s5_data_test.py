import pytest

from maas_cds.model import DdArchive, LtaProduct

__all__ = ["s5_lta_product_l0", "s5_dd_archive_product"]

raw_doc_product_l0 = {
    "reportName": "https://s5p.clas-aip.de",
    "product_id": "501e0178-5a04-4ada-8beb-d04094bebb24",
    "product_name": "S5P_OPER_L0__SAT_A__20220701T051131_20220701T053148_24429_05.RAW",
    "content_length": 384888,
    "publication_date": "2022-07-01T13:41:03.872Z",
    "start_date": "2022-07-01T05:11:31.000Z",
    "end_date": "2022-07-01T05:31:48.000Z",
    "origin_date": "2022-07-01T05:51:05.303Z",
    "modification_date": "2022-07-01T13:48:17.253Z",
    "eviction_date": "2022-07-06T13:48:17.252Z",
    "interface_name": "LTA_S5P_DLR",
    "production_service_type": "LTA",
    "production_service_name": "S5P_DLR",
    "ingestionTime": "2022-07-01T13:56:26.630Z",
}


@pytest.fixture
def s5_lta_product_l0():
    lta_product = LtaProduct(**raw_doc_product_l0)
    lta_product.full_clean()
    lta_product.meta.id = "random-id"

    return lta_product


s5_dd_archive_product_dict = {
    "product_id": "5299172b-eb68-4102-ae13-2cbc841c9081",
    "product_name": "S5P_OPER_AUX_CTMANA_20211220T000000_20211221T000000_20211228T124359",
    "content_length": 1717233115,
    "ingestion_date": "2021-12-28T18:10:54.124Z",
    "start_date": "2021-12-20T00:00:00.000Z",
    "end_date": "2021-12-21T00:00:00.000Z",
    "reportName": "S5P_20211220_OPENHUB_catalogue_20220930235959.csv",
    "ingestionTime": "2022-10-18T03:16:41.986Z",
}


@pytest.fixture
def s5_dd_archive_product():
    product = DdArchive(**s5_dd_archive_product_dict)
    product.meta.index = "raw-data-dd-archive-2021"
    product.meta.id = "5299172b-eb68-4102-ae13-2cbc841c9081"
    product.full_clean()

    return product
