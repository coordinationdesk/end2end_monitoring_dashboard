import pytest
from maas_cds.model.datatake_s2 import CdsDatatakeS2

from maas_cds.model import DdProduct, DasProduct, CreodiasProduct
from maas_cds.model.generated import PripProduct, SatUnavailabilityProduct
from maas_cds.model.product_s2 import CdsProductS2

__all__ = [
    "s2_product_hktm",
    "s2_product_olqc_report",
    "s2_product_l2a_tc",
    "s2_product_l0_gr",
    "s2_product_gip",
    "s2_raw_l2a_tc",
    "s2_product_l1c_ds",
    "s2_raw_product_l1c_container",
    "s2_raw_product_l1c_container_das",
    "s2_datatake_nobs",
    "s2_sat_unavailability_product",
    "s2_datatake_dark_o",
    "s2_datatake_S2A_38107_1",
    "s2_l1c_ds_product_S2A_38107_1",
    "s2_l1c_tl_products_S2A_38107_1",
    "s2_l2a_ds_product_S2A_38107_1",
    "s2_l2a_tc_products_S2A_38107_1",
    "s2_product_without_datatake",
    "s2_creodias_product_1",
]

product_hktm_dict = {
    "key": "002411deb16f0a98f794d19d89cbbe68",
    "mission": "S2",
    "name": "S2A_OPER_PRD_HKTM___20220612T192024_20220612T192100_0001.tar",
    "product_level": "L__",
    "product_type": "PRD_HKTM__",
    "satellite_unit": "S2A",
    "sensing_start_date": "2022-06-12T19:20:24.000Z",
    "sensing_end_date": "2022-06-12T19:21:00.000Z",
    "sensing_duration": 36000000,
    "timeliness": "_",
    "prip_id": "04bfe682-6f42-4df5-9621-7d14dd544986",
    "prip_publication_date": "2022-06-12T19:42:50.271Z",
    "prip_service": "PRIP_S2A_ATOS",
    "updateTime": "2022-06-12T20:37:23.280Z",
    "expected_lta_number": 4,
    "LTA_Acri_is_published": True,
    "LTA_Acri_publication_date": "2022-06-12T19:49:18.331000+00:00",
    "nb_lta_served": 4,
    "LTA_CloudFerro_is_published": True,
    "LTA_CloudFerro_publication_date": "2022-06-12T19:49:56.769000+00:00",
    "LTA_Werum_is_published": True,
    "LTA_Werum_publication_date": "2022-06-12T19:53:02.043000+00:00",
    "LTA_Exprivia_S2_is_published": True,
    "LTA_Exprivia_S2_publication_date": "2022-06-12T20:02:19.207000+00:00",
}


@pytest.fixture
def s2_product_hktm():
    product = CdsProductS2(**product_hktm_dict)
    product.full_clean()
    return product


product_olqc_report_dict = {
    "key": "000000e79a56a814db0e357dd3878a2d",
    "mission": "S2",
    "name": "S2B_OPER_MSI_L1B_GR_2BPS_20220603T011522_S20220602T232745_D06_SENSOR_QUALITY_report.xml",
    "product_level": "L1B",
    "product_type": "OLQC_REPORT",
    "satellite_unit": "S2B",
    "site_center": "2BPS",
    "sensing_start_date": "2022-06-02T23:27:36.455Z",
    "sensing_end_date": "2022-06-02T23:28:48.611Z",
    "sensing_duration": 72156000,
    "timeliness": "_",
    "detector_id": "06",
    "prip_id": "bf7f38f2-4845-41af-aa58-16edb63d4b7c",
    "prip_publication_date": "2022-06-03T01:34:50.017Z",
    "prip_service": "PRIP_S2B_CAPGEMINI",
    "updateTime": "2022-06-03T02:03:40.733Z",
}


@pytest.fixture
def s2_product_olqc_report():
    product = CdsProductS2(**product_olqc_report_dict)
    product.full_clean()
    return product


product_l2a_tc_dict = {
    "absolute_orbit": "36312",
    "key": "00000498248b6695705f2c8f7e8ab372",
    "mission": "S2",
    "name": "S2A_OPER_MSI_L2A_TC_ATOS_20220605T110112_A036312_T43XDG_N04.00.jp2",
    "product_level": "L2A",
    "product_type": "MSI_L2A_TC",
    "satellite_unit": "S2A",
    "site_center": "ATOS",
    "sensing_start_date": "2022-06-05T09:25:57.000Z",
    "sensing_end_date": "2022-06-05T09:29:19.000Z",
    "sensing_duration": 202000000,
    "timeliness": "NOMINAL",
    "tile_number": "43XDG",
    "prip_id": "1d3c9b81-990b-44a0-b306-3ef104896de8",
    "prip_publication_date": "2022-06-05T11:45:37.934Z",
    "prip_service": "PRIP_S2A_ATOS",
    "ddip_id": "d6b27e2c-01c2-4df8-854e-480105d67c29",
    "ddip_container_name": "S2A_MSIL2A_20220605T092601_N0400_R136_T43XDG_20220605T110112",
    "ddip_publication_date": "2022-06-05T12:02:36.124Z",
    "updateTime": "2022-06-08T11:06:16.038Z",
    "nb_datatake_document_that_match": 0,
    "instrument_mode": "NOBS",
    "datatake_id": "36312-1",
}


@pytest.fixture
def s2_product_l2a_tc():
    product = CdsProductS2(**product_l2a_tc_dict)
    product.full_clean()
    return product


product_l0_gr_dict = {
    "key": "00000b11b16cc863b04582fa66bd4c2b",
    "mission": "S2",
    "name": "S2A_OPER_MSI_L0__GR_ATOS_20220603T221050_S20220603T185059_D05_N04.00.tar",
    "product_level": "L0_",
    "product_type": "MSI_L0__GR",
    "satellite_unit": "S2A",
    "site_center": "ATOS",
    "sensing_start_date": "2022-06-03T18:50:59.265Z",
    "sensing_end_date": "2022-06-03T18:50:59.265Z",
    "sensing_duration": 0,
    "timeliness": "NOMINAL",
    "detector_id": "05",
    "prip_id": "d688fe5a-52c4-4f93-8218-124204b63619",
    "prip_publication_date": "2022-06-03T22:29:13.891Z",
    "prip_service": "PRIP_S2A_ATOS",
    "updateTime": "2022-06-09T01:15:54.629Z",
    "nb_datatake_document_that_match": 0,
    "expected_lta_number": 4,
    "LTA_Acri_is_published": True,
    "LTA_Acri_publication_date": "2022-06-03T22:47:55.852000+00:00",
    "nb_lta_served": 3,
    "LTA_CloudFerro_is_published": True,
    "LTA_CloudFerro_publication_date": "2022-06-03T22:56:23.694000+00:00",
    "LTA_Werum_is_published": True,
    "LTA_Werum_publication_date": "2022-06-03T22:41:50.649000+00:00",
    "absolute_orbit": "36289",
    "instrument_mode": "NOBS",
    "datatake_id": "36289-1",
}


@pytest.fixture
def s2_product_l0_gr():
    product = CdsProductS2(**product_l0_gr_dict)
    product.full_clean()
    return product


product_gip_dict = {
    "key": "96b788645b8a5cabc10c8cdca965e5f3",
    "mission": "S2",
    "name": "S2B_OPER_GIP_PROBAS_MPC__20220609T000400_V20150622T000000_21000101T000000_B00.TGZ",
    "product_level": "L__",
    "product_type": "GIP_PROBAS",
    "satellite_unit": "S2B",
    "site_center": "MPC_",
    "sensing_start_date": "2015-06-22T00:00:00.000Z",
    "sensing_end_date": "2100-01-01T00:00:00.000Z",
    "sensing_duration": 2667513600000000,
    "timeliness": "_",
    "auxip_id": "c2842a90-eae8-11ec-8393-fa163e7968e5",
    "auxip_publication_date": "2022-06-13T07:16:35.837Z",
    "updateTime": "2022-06-13T07:33:17.928Z",
}


@pytest.fixture
def s2_product_gip():
    product = CdsProductS2(**product_gip_dict)
    product.full_clean()
    return product


raw_l2a_tc_dict = {
    "reportName": "http://prip.s2a.atos.copernicus.eu",
    "product_id": "1d3c9b81-990b-44a0-b306-3ef104896de8",
    "product_name": "S2A_OPER_MSI_L2A_TC_ATOS_20220605T110112_A036312_T43XDG_N04.00.jp2",
    "content_length": 93419,
    "publication_date": "2022-06-05T11:45:37.934Z",
    "start_date": "2022-06-05T09:25:57.000Z",
    "end_date": "2022-06-05T09:29:19.000Z",
    "origin_date": "2022-06-05T09:35:40.080Z",
    "interface_name": "PRIP_S2A_ATOS",
    "production_service_type": "PRIP",
    "production_service_name": "S2A-ATOS",
    "ingestionTime": "2022-06-05T12:08:43.400Z",
}


@pytest.fixture
def s2_raw_l2a_tc():
    product = PripProduct(**raw_l2a_tc_dict)
    product.full_clean()
    return product


product_l1c_ds_dict = {
    "absolute_orbit": "36678",
    "datatake_id": "36678-7",
    "key": "fafba3ef1188ced69f0004a0e00f1b5a",
    "instrument_mode": "NOBS",
    "mission": "S2",
    "name": "S2A_OPER_MSI_L1C_DS_ATOS_20220701T011249_S20220701T000744_N04.00.tar",
    "product_level": "L1C",
    "product_type": "MSI_L1C_DS",
    "satellite_unit": "S2A",
    "site_center": "ATOS",
    "sensing_start_date": "2022-07-01T00:07:44.000Z",
    "sensing_end_date": "2022-07-01T00:10:26.000Z",
    "sensing_duration": 162000000,
    "timeliness": "NOMINAL",
    "prip_id": "f5f096f8-460a-452c-91b9-c8a6ff621fff",
    "prip_publication_date": "2022-07-01T02:18:07.022Z",
    "prip_service": "PRIP_S2A_ATOS",
    "updateTime": "2022-07-01T02:43:49.688Z",
}


@pytest.fixture
def s2_product_l1c_ds():
    product = CdsProductS2(**product_l1c_ds_dict)
    product.full_clean()
    return product


s2_datatake_nobs_dict = {
    "name": "S2A_MP_ACQ__MTL_20220630T120000_20220718T150000.csv",
    "key": "S2A-36678-7",
    "datatake_id": "36678-7",
    "satellite_unit": "S2A",
    "mission": "S2",
    "observation_time_start": "2022-07-01T00:07:25.962Z",
    "observation_duration": 165968000,
    "observation_time_stop": "2022-07-01T00:10:11.930Z",
    "number_of_scenes": 46,
    "absolute_orbit": "36678",
    "relative_orbit": "73",
    "timeliness": "NOMINAL",
    "instrument_mode": "NOBS",
    "application_date": "2022-06-30T12:00:00.000Z",
}


@pytest.fixture
def s2_datatake_nobs():
    datatake = CdsDatatakeS2(**s2_datatake_nobs_dict)
    datatake.full_clean()
    return datatake


s2_sat_unavailability_product_raw_dict = {
    "file_name": "S2A_OPER_REP__SUP___20220902T211217_20220902T212544_0001",
    "mission": "Sentinel-2A",
    "unavailability_reference": "11101",
    "unavailability_type": "Return to Operations",
    "subsystem": "OCP",
    "start_time": "UTC=2022-09-02T21:12:17",
    "start_orbit": 37591,
    "start_anx_offset": 4839,
    "end_time": "UTC=2022-09-02T21:25:44",
    "end_orbit": 37591,
    "end_anx_offset": 5646,
    "type": "UNPLANNED",
    "comment": "Outage due to GS2_OCP-41 OCP FPA Optical Range Violation, interrupting a link, 1 link affected. Outage due to GS2_OCP-41 OCP FPA Optical Range Violation, interrupting a link, 1 link affected.",
    "interface_name": "Satellite-Unavailability",
    "production_service_type": "AUXIP",
    "production_service_name": "Exprivia",
    "reportName": "S2A_OPER_REP__SUP___20220902T211217_20220902T212544_0001.EOF",
    "ingestionTime": "2022-09-05T16:10:47.970Z",
}


@pytest.fixture
def s2_sat_unavailability_product():
    satu = SatUnavailabilityProduct(**s2_sat_unavailability_product_raw_dict)
    satu.full_clean()
    satu.meta.id = "635e6d01d2239e3f885a036c48944e9b"
    satu.meta.index = "raw-data-sat-unavailability-product-2022-09"
    return satu


datatake_s2_darko_dict = {
    "name": "S2B_MP_ACQ__MTL_20220707T120000_20220725T150000.csv",
    "key": "S2B-28060-2",
    "datatake_id": "28060-2",
    "satellite_unit": "S2B",
    "mission": "S2",
    "observation_time_start": "2022-07-21T08:21:10.079Z",
    "observation_duration": 46904000,
    "observation_time_stop": "2022-07-21T08:21:56.983Z",
    "number_of_scenes": 13,
    "absolute_orbit": "28060",
    "relative_orbit": "6",
    "timeliness": "NOMINAL",
    "instrument_mode": "DARK-O",
    "application_date": "2022-07-07T12:00:00.000Z",
    "updateTime": "2022-08-29T15:15:20.518Z",
}


@pytest.fixture
def s2_datatake_dark_o():
    datatake = CdsDatatakeS2(**datatake_s2_darko_dict)
    datatake.full_clean()
    datatake.meta.id = "S2B-28060-2"
    datatake.meta.index = "cds-datatake-s1-s2"
    return datatake


s2_raw_product_l1c_container_dict = {
    "reportName": "https://apihub.copernicus.eu/apihub",
    "product_id": "d373c28d-7eac-481a-aa84-0da6ad177bc4",
    "product_name": "S2B_MSIL1C_20221108T090059_N0400_R007_T38WNV_20221108T092119",
    "content_length": 590026204,
    "ingestion_date": "2022-11-08T10:30:42.011Z",
    "modification_date": "2022-11-08T10:31:04.199Z",
    "creation_date": "2022-11-08T10:31:04.199Z",
    "start_date": "2022-11-08T09:00:59.024Z",
    "end_date": "2022-11-08T09:00:59.024Z",
    "interface_name": "DD_DHUS",
    "production_service_type": "DD",
    "production_service_name": "DHUS",
    "ingestionTime": "2022-11-08T10:48:04.226Z",
}


@pytest.fixture
def s2_raw_product_l1c_container():
    product = DdProduct(**s2_raw_product_l1c_container_dict)

    product.full_clean()

    product.meta.id = "343b2c4a6aaf254f821b0b509ef3345f"
    product.meta.index = "raw-data-dd-product-2022"
    return product


s2_raw_product_l1c_container_das_dict = {
    "product_id": "d373c28d-7eac-481a-aa84-0da6ad177bc4",
    "product_name": "S2B_MSIL1C_20221108T090059_N0400_R007_T38WNV_20221108T092119",
    "content_length": 590026204,
    "publication_date": "2022-11-08T10:31:04.199Z",
    "origin_date": "2022-11-08T10:30:42.011Z",
    "eviction_date": "2022-11-08T10:31:04.199Z",
    "start_date": "2022-11-08T09:00:59.024Z",
    "end_date": "2022-11-08T09:00:59.024Z",
    "interface_name": "DD_DAS",
    "production_service_type": "DD",
    "production_service_name": "DAS",
    "ingestionTime": "2022-11-08T10:48:04.226Z",
}


@pytest.fixture
def s2_raw_product_l1c_container_das():
    product = DasProduct(**s2_raw_product_l1c_container_das_dict)

    product.full_clean()

    product.meta.id = "343b2c4a6aaf254f821b0b509ef3345f"
    product.meta.index = "raw-data-das-product-2022"
    return product


s2_datatake_dict_S2A_38107_1 = {
    "name": "S2A_MP_ACQ__MTL_20221006T120000_20221024T150000.csv",
    "key": "S2A-38107-1",
    "datatake_id": "38107-1",
    "satellite_unit": "S2A",
    "mission": "S2",
    "observation_time_start": "2022-10-08T22:04:13.716Z",
    "observation_duration": 18040000,
    "observation_time_stop": "2022-10-08T22:04:31.756Z",
    "number_of_scenes": 5,
    "absolute_orbit": "38107",
    "relative_orbit": "72",
    "timeliness": "NOMINAL",
    "instrument_mode": "NOBS",
    "application_date": "2022-10-06T12:00:00.000Z",
    "updateTime": "2022-10-17T14:28:05.091Z",
}


@pytest.fixture
def s2_datatake_S2A_38107_1():
    datatake = CdsDatatakeS2(**s2_datatake_dict_S2A_38107_1)
    datatake.full_clean()

    return datatake


s2_l1c_ds_product_dict_S2A_38107_1 = {
    "product_level": "L1_",
    "datatake_id": "38107-1",
    "sensing_end_date": "2022-10-08T22:04:28.000Z",
    "expected_tiles": [
        "07XDE",
        "07XEE",
        "06XWK",
        "08XMH",
        "08XMJ",
        "07XDD",
        "07XED",
        "06XWJ",
        "08XNH",
        "07XEC",
    ],
    "sensing_start_date": "2022-10-08T22:04:17.000Z",
    "prip_publication_date": "2022-10-08T22:53:03.966Z",
    "updateTime": "2022-10-08T23:22:30.783Z",
    "prip_service": "PRIP_S2A_ATOS",
    "instrument_mode": "NOBS",
    "prip_id": "dcd1b557-ab52-46bb-b7f4-8240c7f4dbe9",
    "mission": "S2",
    "product_type": "MSI_L1C_DS",
    "absolute_orbit": "38107",
    "timeliness": "NOMINAL",
    "name": "S2A_OPER_MSI_L1C_DS_ATOS_20221008T222426_S20221008T220417_N04.00.tar",
    "site_center": "ATOS",
    "satellite_unit": "S2A",
    "key": "2f5eca438436a70e9ab785cfee481bd3",
    "sensing_duration": 11000000,
}


@pytest.fixture
def s2_l1c_ds_product_S2A_38107_1():
    product = CdsProductS2(**s2_l1c_ds_product_dict_S2A_38107_1)
    product.full_clean()

    return product


s2_l1c_tl_products_dict_S2A_38107_1 = [
    {
        "product_level": "L1_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "08XMJ",
        "prip_publication_date": "2022-10-08T22:53:05.005Z",
        "from_prip_ddip_timeliness": 716050000,
        "updateTime": "2022-10-08T23:35:11.732Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "5ba55241-42c6-42c2-af5d-fb564e42c329",
        "ddip_container_name": "S2A_MSIL1C_20221008T220421_N0400_R072_T08XMJ_20221008T222426",
        "mission": "S2",
        "product_type": "MSI_L1C_TL",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "ddip_publication_date": "2022-10-08T23:05:01.055Z",
        "name": "S2A_OPER_MSI_L1C_TL_ATOS_20221008T222426_A038107_T08XMJ_N04.00.tar",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "74eeaac7-6f1e-4aed-8f3c-7287dad507ac",
        "key": "0bdc31000e470ce168542f8ef7d5c6a3",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:24:26.000Z",
    },
    {
        "product_level": "L1_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "08XNH",
        "prip_publication_date": "2022-10-08T22:52:59.839Z",
        "from_prip_ddip_timeliness": 722130000,
        "updateTime": "2022-10-08T23:35:12.281Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "463d2c2e-aef5-430c-8c2b-743a01898345",
        "ddip_container_name": "S2A_MSIL1C_20221008T220421_N0400_R072_T08XNH_20221008T222426",
        "mission": "S2",
        "product_type": "MSI_L1C_TL",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "ddip_publication_date": "2022-10-08T23:05:01.969Z",
        "name": "S2A_OPER_MSI_L1C_TL_ATOS_20221008T222426_A038107_T08XNH_N04.00.tar",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "bfa93aef-4286-4f82-80b6-fcca1404656f",
        "key": "c774e0c13bcad46426fcc82605db425a",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:24:26.000Z",
    },
    {
        "product_level": "L1_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "07XED",
        "prip_publication_date": "2022-10-08T22:53:06.281Z",
        "from_prip_ddip_timeliness": 715910000,
        "updateTime": "2022-10-08T23:35:12.435Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "32c96c94-2efc-40a7-a602-22f6f3eb2f72",
        "ddip_container_name": "S2A_MSIL1C_20221008T220421_N0400_R072_T07XED_20221008T222426",
        "mission": "S2",
        "product_type": "MSI_L1C_TL",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "ddip_publication_date": "2022-10-08T23:05:02.191Z",
        "name": "S2A_OPER_MSI_L1C_TL_ATOS_20221008T222426_A038107_T07XED_N04.00.tar",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "64191a6e-38fc-48ed-b965-1d1709f64939",
        "key": "92d7fa5e2741e8343942cb9c95974227",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:24:26.000Z",
    },
    {
        "product_level": "L1_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "07XEE",
        "prip_publication_date": "2022-10-08T22:52:59.925Z",
        "from_prip_ddip_timeliness": 722883000,
        "updateTime": "2022-10-08T23:35:12.754Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "47f0bc1d-3864-41ad-9848-442220fd9f3f",
        "ddip_container_name": "S2A_MSIL1C_20221008T220421_N0400_R072_T07XEE_20221008T222426",
        "mission": "S2",
        "product_type": "MSI_L1C_TL",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "ddip_publication_date": "2022-10-08T23:05:02.808Z",
        "name": "S2A_OPER_MSI_L1C_TL_ATOS_20221008T222426_A038107_T07XEE_N04.00.tar",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "2eb78dff-4db5-45d5-8dbf-1e8a2544cea8",
        "key": "929c6abdd8d378304418868f1a85896c",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:24:26.000Z",
    },
    {
        "product_level": "L1_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "07XDD",
        "prip_publication_date": "2022-10-08T22:53:05.322Z",
        "from_prip_ddip_timeliness": 717723000,
        "updateTime": "2022-10-08T23:35:12.978Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "d4e92dda-0025-4b09-bc24-dbde7c481be6",
        "ddip_container_name": "S2A_MSIL1C_20221008T220421_N0400_R072_T07XDD_20221008T222426",
        "mission": "S2",
        "product_type": "MSI_L1C_TL",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "ddip_publication_date": "2022-10-08T23:05:03.045Z",
        "name": "S2A_OPER_MSI_L1C_TL_ATOS_20221008T222426_A038107_T07XDD_N04.00.tar",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "2d149fe4-30c4-4e0a-9f4d-182c2d1cb5eb",
        "key": "10c4fcd00fa621b01dfc4dff05325de3",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:24:26.000Z",
    },
    {
        "product_level": "L1_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "06XWJ",
        "prip_publication_date": "2022-10-08T22:52:59.825Z",
        "from_prip_ddip_timeliness": 723480000,
        "updateTime": "2022-10-08T23:35:13.237Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "19329c88-48e2-4976-9276-dd27c2d5ff71",
        "ddip_container_name": "S2A_MSIL1C_20221008T220421_N0400_R072_T06XWJ_20221008T222426",
        "mission": "S2",
        "product_type": "MSI_L1C_TL",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "ddip_publication_date": "2022-10-08T23:05:03.305Z",
        "name": "S2A_OPER_MSI_L1C_TL_ATOS_20221008T222426_A038107_T06XWJ_N04.00.tar",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "c77be05a-9d53-4c5a-a5d1-8da63a7dd695",
        "key": "57f5c74bb938f28b46b83c2b8b8fe65f",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:24:26.000Z",
    },
    {
        "product_level": "L1_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "08XMH",
        "prip_publication_date": "2022-10-08T22:53:05.500Z",
        "from_prip_ddip_timeliness": 718728000,
        "updateTime": "2022-10-08T23:35:13.678Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "a29c580c-0555-4f43-bc3d-249d2b0f3a2a",
        "ddip_container_name": "S2A_MSIL1C_20221008T220421_N0400_R072_T08XMH_20221008T222426",
        "mission": "S2",
        "product_type": "MSI_L1C_TL",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "ddip_publication_date": "2022-10-08T23:05:04.228Z",
        "name": "S2A_OPER_MSI_L1C_TL_ATOS_20221008T222426_A038107_T08XMH_N04.00.tar",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "0ac474a3-c3eb-4f92-8a81-fef6a26edc55",
        "key": "2957eddebc03a1d9c627008740adb6e7",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:24:26.000Z",
    },
    {
        "product_level": "L1_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "06XWK",
        "prip_publication_date": "2022-10-08T22:53:04.499Z",
        "from_prip_ddip_timeliness": 716211000,
        "updateTime": "2022-10-08T23:35:11.542Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "d10aacbb-e9e3-498a-86f4-e68e93a4b7a4",
        "ddip_container_name": "S2A_MSIL1C_20221008T220421_N0400_R072_T06XWK_20221008T222426",
        "mission": "S2",
        "product_type": "MSI_L1C_TL",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "ddip_publication_date": "2022-10-08T23:05:00.710Z",
        "name": "S2A_OPER_MSI_L1C_TL_ATOS_20221008T222426_A038107_T06XWK_N04.00.tar",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "95a8dc26-239c-42ec-bdc5-dc22e815a764",
        "key": "ae5d215d9dc7c4cf910d7e771bfd7529",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:24:26.000Z",
    },
    {
        "product_level": "L1_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "07XEC",
        "prip_publication_date": "2022-10-08T22:53:04.168Z",
        "from_prip_ddip_timeliness": 717409000,
        "updateTime": "2022-10-08T23:35:12.093Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "8345d492-e8e0-4dc2-90e0-caeb4971af4f",
        "ddip_container_name": "S2A_MSIL1C_20221008T220421_N0400_R072_T07XEC_20221008T222426",
        "mission": "S2",
        "product_type": "MSI_L1C_TL",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "ddip_publication_date": "2022-10-08T23:05:01.577Z",
        "name": "S2A_OPER_MSI_L1C_TL_ATOS_20221008T222426_A038107_T07XEC_N04.00.tar",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "79df0434-35ff-4dcb-857c-b77a96ecde57",
        "key": "1162922eb13984877e1e2405b05df369",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:24:26.000Z",
    },
    {
        "product_level": "L1_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "07XDE",
        "prip_publication_date": "2022-10-08T22:53:05.327Z",
        "from_prip_ddip_timeliness": 718627000,
        "updateTime": "2022-10-08T23:35:13.436Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "f38ce9da-cfac-4cfd-ba70-600589ab2c73",
        "ddip_container_name": "S2A_MSIL1C_20221008T220421_N0400_R072_T07XDE_20221008T222426",
        "mission": "S2",
        "product_type": "MSI_L1C_TL",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "ddip_publication_date": "2022-10-08T23:05:03.954Z",
        "name": "S2A_OPER_MSI_L1C_TL_ATOS_20221008T222426_A038107_T07XDE_N04.00.tar",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "dc7e7d4a-cb43-4e71-8fb3-153757a9ca8d",
        "key": "098f34664430bd8250bf0ea850d1c3bd",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:24:26.000Z",
    },
]


@pytest.fixture
def s2_l1c_tl_products_S2A_38107_1():
    products = []
    for product_dict in s2_l1c_tl_products_dict_S2A_38107_1:
        product = CdsProductS2(**product_dict)
        product.full_clean()

        products.append(product)

    return products


s2_l2a_ds_product_dict_S2A_38107_1 = {
    "product_level": "L2_",
    "datatake_id": "38107-1",
    "sensing_end_date": "2022-10-08T22:04:28.000Z",
    "sensing_start_date": "2022-10-08T22:04:17.000Z",
    "prip_publication_date": "2022-10-08T23:19:24.933Z",
    "updateTime": "2022-10-08T23:50:21.952Z",
    "prip_service": "PRIP_S2A_ATOS",
    "instrument_mode": "NOBS",
    "prip_id": "5c0a06d8-8df6-4eba-a506-29d7a5e14ce3",
    "mission": "S2",
    "product_type": "MSI_L2A_DS",
    "absolute_orbit": "38107",
    "timeliness": "NOMINAL",
    "name": "S2A_OPER_MSI_L2A_DS_ATOS_20221008T225558_S20221008T220417_N04.00.tar",
    "site_center": "ATOS",
    "satellite_unit": "S2A",
    "key": "030addb6778d1faee99369c26c0fd6c0",
    "sensing_duration": 11000000,
}


@pytest.fixture
def s2_l2a_ds_product_S2A_38107_1():
    product = CdsProductS2(**s2_l2a_ds_product_dict_S2A_38107_1)
    product.full_clean()

    return product


s2_l2a_tc_products_dict_S2A_38107_1 = [
    {
        "product_level": "L2_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "07XEE",
        "prip_publication_date": "2022-10-08T23:19:21.240Z",
        "updateTime": "2022-10-08T23:50:21.950Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "3dc2c337-52cd-4713-baff-cb248176ca70",
        "ddip_container_name": "S2A_MSIL2A_20221008T220421_N0400_R072_T07XEE_20221008T225558",
        "mission": "S2",
        "product_type": "MSI_L2A_TC",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "name": "S2A_OPER_MSI_L2A_TC_ATOS_20221008T225558_A038107_T07XEE_N04.00.jp2",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "8b4a3b8d3ca336a301bc2b29fcca7430",
        "key": "6f01ef6da2ae63ff0495dbd95414c1e5",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:55:58.000Z",
    },
    {
        "product_level": "L2_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "06XWJ",
        "prip_publication_date": "2022-10-08T23:19:21.427Z",
        "updateTime": "2022-10-08T23:50:21.951Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "036310ed-2b5c-4d87-8674-8844958a9bb3",
        "ddip_container_name": "S2A_MSIL2A_20221008T220421_N0400_R072_T06XWJ_20221008T225558",
        "mission": "S2",
        "product_type": "MSI_L2A_TC",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "name": "S2A_OPER_MSI_L2A_TC_ATOS_20221008T225558_A038107_T06XWJ_N04.00.jp2",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "12bfe8429f6074a86b7174dcccc9fa9e",
        "key": "9ad8783be588a8729d1f09acba34b9bc",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:55:58.000Z",
    },
    {
        "product_level": "L2_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "07XEC",
        "prip_publication_date": "2022-10-08T23:19:25.354Z",
        "updateTime": "2022-10-08T23:50:21.953Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "968d374a-30cf-40a9-b242-bc9662241abc",
        "ddip_container_name": "S2A_MSIL2A_20221008T220421_N0400_R072_T07XEC_20221008T225558",
        "mission": "S2",
        "product_type": "MSI_L2A_TC",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "name": "S2A_OPER_MSI_L2A_TC_ATOS_20221008T225558_A038107_T07XEC_N04.00.jp2",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "2a4b50e4e321c522e14996a5736d6c93",
        "key": "c8b79abf4e6f5a84cfe5cf39d03d88b5",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:55:58.000Z",
    },
    {
        "product_level": "L2_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "06XWK",
        "prip_publication_date": "2022-10-08T23:19:25.682Z",
        "updateTime": "2022-10-08T23:50:21.954Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "4c1b14fe-fcad-4dd9-9077-908c494035ca",
        "ddip_container_name": "S2A_MSIL2A_20221008T220421_N0400_R072_T06XWK_20221008T225558",
        "mission": "S2",
        "product_type": "MSI_L2A_TC",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "name": "S2A_OPER_MSI_L2A_TC_ATOS_20221008T225558_A038107_T06XWK_N04.00.jp2",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "cf7ca5b21ebf7aea21412dcfbc3f0f6b",
        "key": "90e41e7532f33d141fb92daeb77f8d23",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:55:58.000Z",
    },
    {
        "product_level": "L2_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "08XMJ",
        "prip_publication_date": "2022-10-08T23:19:26.399Z",
        "updateTime": "2022-10-08T23:50:21.956Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "b0b58ed7-131a-4a51-af64-a4582eab0133",
        "ddip_container_name": "S2A_MSIL2A_20221008T220421_N0400_R072_T08XMJ_20221008T225558",
        "mission": "S2",
        "product_type": "MSI_L2A_TC",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "name": "S2A_OPER_MSI_L2A_TC_ATOS_20221008T225558_A038107_T08XMJ_N04.00.jp2",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "73c21647d164f7d5c8547c5d37f2e900",
        "key": "b05eaf6e857e08432ff85368e45beabb",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:55:58.000Z",
    },
    {
        "product_level": "L2_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "07XDD",
        "prip_publication_date": "2022-10-08T23:19:26.425Z",
        "updateTime": "2022-10-08T23:50:21.957Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "a86290b0-9af7-4fac-9730-7844472457bd",
        "ddip_container_name": "S2A_MSIL2A_20221008T220421_N0400_R072_T07XDD_20221008T225558",
        "mission": "S2",
        "product_type": "MSI_L2A_TC",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "name": "S2A_OPER_MSI_L2A_TC_ATOS_20221008T225558_A038107_T07XDD_N04.00.jp2",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "28d4ec23801f94dda03a4b3c9c00359f",
        "key": "2b765ae96a97b3a1271699e89e97a198",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:55:58.000Z",
    },
    {
        "product_level": "L2_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "07XDE",
        "prip_publication_date": "2022-10-08T23:19:26.474Z",
        "updateTime": "2022-10-08T23:50:21.957Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "bc5dc080-43c4-4dde-8b92-1a730b064821",
        "ddip_container_name": "S2A_MSIL2A_20221008T220421_N0400_R072_T07XDE_20221008T225558",
        "mission": "S2",
        "product_type": "MSI_L2A_TC",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "name": "S2A_OPER_MSI_L2A_TC_ATOS_20221008T225558_A038107_T07XDE_N04.00.jp2",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "8741e819fa2a7c6015075c943a304ed4",
        "key": "ea11c4bc32f0cee417aac1d0eba41398",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:55:58.000Z",
    },
    {
        "product_level": "L2_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "08XMH",
        "prip_publication_date": "2022-10-08T23:19:26.681Z",
        "updateTime": "2022-10-08T23:50:21.958Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "9610cbcc-1e7c-43d9-9b54-bafbb1ea72e5",
        "ddip_container_name": "S2A_MSIL2A_20221008T220421_N0400_R072_T08XMH_20221008T225558",
        "mission": "S2",
        "product_type": "MSI_L2A_TC",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "name": "S2A_OPER_MSI_L2A_TC_ATOS_20221008T225558_A038107_T08XMH_N04.00.jp2",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "badb25799ec7f3c82040fd5819fbd911",
        "key": "624a47e0ec9fe11c48fd34491ecfa6fe",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:55:58.000Z",
    },
    {
        "product_level": "L2_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "07XED",
        "prip_publication_date": "2022-10-08T23:19:27.778Z",
        "updateTime": "2022-10-08T23:50:21.959Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "fb777d80-e8b3-4635-875b-d34bb65e0847",
        "ddip_container_name": "S2A_MSIL2A_20221008T220421_N0400_R072_T07XED_20221008T225558",
        "mission": "S2",
        "product_type": "MSI_L2A_TC",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "name": "S2A_OPER_MSI_L2A_TC_ATOS_20221008T225558_A038107_T07XED_N04.00.jp2",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "ed492f1b0aa59c5232ea8667f6b6dfe5",
        "key": "3adc226b3d6b975e1534a85e1674368f",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:55:58.000Z",
    },
    {
        "product_level": "L2_",
        "datatake_id": "38107-1",
        "sensing_end_date": "2022-10-08T22:04:28.000Z",
        "sensing_start_date": "2022-10-08T22:04:17.000Z",
        "tile_number": "08XNH",
        "prip_publication_date": "2022-10-08T23:19:21.222Z",
        "updateTime": "2022-10-08T23:50:21.950Z",
        "prip_service": "PRIP_S2A_ATOS",
        "instrument_mode": "NOBS",
        "prip_id": "6a933577-7d40-4545-a6bb-a23d4ba7b77b",
        "ddip_container_name": "S2A_MSIL2A_20221008T220421_N0400_R072_T08XNH_20221008T225558",
        "mission": "S2",
        "product_type": "MSI_L2A_TC",
        "absolute_orbit": "38107",
        "timeliness": "NOMINAL",
        "name": "S2A_OPER_MSI_L2A_TC_ATOS_20221008T225558_A038107_T08XNH_N04.00.jp2",
        "site_center": "ATOS",
        "satellite_unit": "S2A",
        "ddip_id": "966d525aa3e8540c4dbc6e178a18cd5a",
        "key": "a0f5dae6a80aad0c3360154d30732296",
        "sensing_duration": 11000000,
        "product_discriminator_date": "2022-10-08T22:55:58.000Z",
    },
]


@pytest.fixture
def s2_l2a_tc_products_S2A_38107_1():
    products = []
    for product_dict in s2_l2a_tc_products_dict_S2A_38107_1:
        product = CdsProductS2(**product_dict)
        product.full_clean()

        products.append(product)

    return products


product_without_datatake_dict = {
    "key": "fafba3ef1188ced69f0004a0e00f1b5a",
    "instrument_mode": "NOBS",
    "mission": "S2",
    "name": "S2A_OPER_MSI_L1C_DS_ATOS_20220701T011249_S20220701T000744_N04.00.tar",
    "product_level": "L1C",
    "product_type": "MSI_L1C_DS",
    "satellite_unit": "S2A",
    "site_center": "ATOS",
    "sensing_start_date": "2022-07-01T00:07:44.000Z",
    "sensing_end_date": "2022-07-01T00:10:26.000Z",
    "sensing_duration": 162000000,
    "prip_id": "f5f096f8-460a-452c-91b9-c8a6ff621fff",
    "prip_publication_date": "2022-07-01T02:18:07.022Z",
    "prip_service": "PRIP_S2A_ATOS",
    "updateTime": "2022-07-01T02:43:49.688Z",
}


@pytest.fixture
def s2_product_without_datatake():
    product = CdsProductS2(**product_without_datatake_dict)
    product.full_clean()
    return product


@pytest.fixture
def s2_creodias_product_1():
    data_dict = {
        "product_id": "9874d06d-f2de-5f46-bb21-b9dac8c95d6c",
        "product_name": "S2A_MSIL2A_20220710T170936_N0204_R112_T23XMG_20220710T170937.SAFE",
        "content_length": 485359842,
        "publication_date": "2023-01-05T01:31:54.673Z",
        "start_date": "2022-07-10T17:09:36.027Z",
        "end_date": "2022-07-10T17:09:36.027Z",
        "origin_date": "2022-11-22T12:25:47.307Z",
        "interface_name": "DD_CREODIAS",
        "production_service_type": "DD",
        "production_service_name": "CREODIAS",
    }

    raw_document = CreodiasProduct(**data_dict)
    raw_document.meta.id = "c43d34bf843b455cdb83505fb49714f2"
    raw_document.full_clean()
    return raw_document
