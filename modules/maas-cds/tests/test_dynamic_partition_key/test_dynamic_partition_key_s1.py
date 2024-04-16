from maas_cds.engines.reports.publication import PublicationConsolidatorEngine
from maas_cds.model import LtaProduct


def test_s1_product_aux(s1_product_macp):
    assert s1_product_macp.partition_index_name == "cds-product-2022-06"

def test_s1_lta_bug_missing_indices():
    data_dict = {
        "reportName": "https://aip.acri-st.fr",
        "product_id": "3755cc3d-6793-4bcd-a3c8-073aade52960",
        "product_name": "S1A_IW_RAW__0SDV_20230630T235307_20230630T235339_049222_05EB2E_7A6F.SAFE.zip",
        "content_length": 1657621777,
        "publication_date": "2023-07-01T09:16:13.326Z",
        "start_date": "2023-06-30T23:53:07.509Z",
        "end_date": "2023-06-30T23:53:39.909Z",
        "origin_date": "2023-07-01T08:53:44.158Z",
        "modification_date": "2023-07-01T09:16:13.326Z",
        "eviction_date": "2199-01-01T00:00:00.000Z",
        "interface_name": "LTA_Acri",
        "production_service_type": "LTA",
        "production_service_name": "Acri",
        "ingestionTime": "2023-07-01T09:43:41.365Z"
    }

    data_dict_2 = {
        "reportName": "https://cf.fr",
        "product_id": "a_different_3755cc3d-6793-4bcd-a3c8-073aade52960",
        "product_name": "S1A_IW_RAW__0SDV_20230630T235307_20230630T235339_049222_05EB2E_7A6F.SAFE.zip",
        "content_length": 1657621777,
        "publication_date": "2023-07-01T09:16:13.326Z",
        "start_date": "2023-07-30T23:53:07.509Z",
        "end_date": "2023-07-30T23:53:39.909Z",
        "origin_date": "2023-07-01T08:53:44.158Z",
        "modification_date": "2023-07-01T09:16:13.326Z",
        "eviction_date": "2199-01-01T00:00:00.000Z",
        "interface_name": "LTA_CF",
        "production_service_type": "LTA",
        "production_service_name": "CF",
        "ingestionTime": "2023-07-01T09:43:41.365Z"
    }

    lta_product = LtaProduct(**data_dict)
    lta_product.full_clean()
    lta_product_2 = LtaProduct(**data_dict_2)
    lta_product_2.full_clean()
    engine = PublicationConsolidatorEngine()
    engine.input_documents = [lta_product, lta_product_2]
    engine.on_pre_consolidate()
    indices = engine.get_consolidated_indices()

    assert indices == ['cds-publication-2023-06', 'cds-publication-2023-07']
