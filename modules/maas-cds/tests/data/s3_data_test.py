import pytest
from maas_cds.model.cds_s3_completeness import CdsS3Completeness

from maas_cds.model.product_s3 import CdsProductS3

__all__ = [
    "s3_product_old",
    "s3_product_aux",
    "s3_product_aux_1",
    "s3_product_aux_2",
    "s3_product_aux_without_sep",
    "cds_s3_completeness_do_0_nav",
    "cds_s3_completeness_sr_0_sra___",
    "cds_s3_completeness_ol_0_efr",
]


product_old_dict = {
    "key": "e8852dab981374bf4f966e70699e2cb0",
    "mission": "S3",
    "name": "S3A_SR_1_USO_AX_20160223T195017_20220611T021821_20220611T084649___________________CNE_O_AL_001.SEN3.zip",
    "product_level": "AUX",
    "product_type": "SR_1_USO_AX",
    "satellite_unit": "S3A",
    "sensing_start_date": "2016-02-23T19:50:17.000Z",
    "sensing_end_date": "2022-06-11T02:18:21.000Z",
    "sensing_duration": 198656884000000,
    "timeliness": "AL",
    "auxip_id": "2ab71ce8-e964-11ec-9f39-fa163e7968e5",
    "auxip_publication_date": "2022-06-11T08:54:56.426Z",
    "updateTime": "2022-06-11T09:15:55.833Z",
}


@pytest.fixture
def s3_product_old():
    product = CdsProductS3(**product_old_dict)
    product.full_clean()
    return product


product_aux_dict = {
    "key": "323da53790489f00873d462e32a444d0",
    "mission": "S3",
    "name": "S3A_OPER_AUX_GNSSRD_POD__20220410T033343_V20220402T235942_20220403T235941.TGZ",
    "product_type": "OPER_AUX_GN",
    "satellite_unit": "S3A",
    "product_level": "___",
    "sensing_start_date": "2022-04-02T23:59:42.000Z",
    "sensing_end_date": "2022-04-03T23:59:41.000Z",
    "sensing_duration": 86399000000,
    "auxip_id": "f19805e2-b89b-11ec-8928-fa163e7968e5",
    "auxip_publication_date": "2022-04-10T07:00:45.433Z",
    "updateTime": "2022-04-12T19:25:25.595Z",
}


@pytest.fixture
def s3_product_aux():
    product = CdsProductS3(**product_aux_dict)
    product.full_clean()
    return product


product_aux_2_dict = {
    "key": "94e6c5d97644a4a998feeb39219ce9f5",
    "mission": "S3",
    "name": "S3A_MW_1_DNB_AX_20000101T000000_20220519T174752_20220519T181546___________________PS1_O_AL____.SEN3.zip",
    "product_level": "AUX",
    "product_type": "MW_1_DNB_AX",
    "satellite_unit": "S3A",
    "sensing_start_date": "2000-01-01T00:00:00.000Z",
    "sensing_end_date": "2022-05-19T17:47:52.000Z",
    "sensing_duration": 706297672000000,
    "timeliness": "AL",
    "expected_lta_number": 4,
    "LTA_CloudFerro_is_published": True,
    "LTA_CloudFerro_publication_date": "2022-05-19T18:24:37.039000+00:00",
    "nb_lta_served": 1,
}


@pytest.fixture
def s3_product_aux_2():
    product = CdsProductS3(**product_aux_2_dict)
    product.full_clean()
    return product


product_aux_dict_1 = {
    "key": "667a53ed930e3588d07c317ee6b3911f",
    "mission": "S3",
    "name": "S3__SR_2_POL_AX_19870101T000000_20230602T000000_20220606T214738___________________CNE_O_AL_001.SEN3.zip",
    "product_level": "AUX",
    "product_type": "SR_2_POL_AX",
    "satellite_unit": "S3_",
    "sensing_start_date": "1987-01-01T00:00:00.000Z",
    "sensing_end_date": "2023-06-02T00:00:00.000Z",
    "sensing_duration": 1149206400000000,
    "timeliness": "AL",
    "auxip_id": "6451801c-e5e3-11ec-bd08-fa163e7968e5",
    "auxip_publication_date": "2022-06-06T21:55:34.501Z",
    "updateTime": "2022-06-08T14:45:11.919Z",
}


@pytest.fixture
def s3_product_aux_1():
    product = CdsProductS3(**product_aux_dict_1)
    product.full_clean()
    return product


product_aux_without_sep_dict = {
    "key": "d7f1a22535ecb6f27432e84eabf368c2",
    "mission": "S3",
    "name": "S3A_GN_1_MANHAX_20160222T092935_20220614T093007_20220607T142547___________________EUM_O_NR_001.SEN3.zip",
    "product_level": "___",
    "product_type": "GN_1_MANHAX",
    "satellite_unit": "S3A",
    "sensing_start_date": "2016-02-22T09:29:35.000Z",
    "sensing_end_date": "2022-06-14T09:30:07.000Z",
    "sensing_duration": 199065632000000,
    "timeliness": "NR",
    "auxip_id": "9235a0fe-e66e-11ec-b5ee-fa163e7968e5",
    "auxip_publication_date": "2022-06-07T14:31:51.538Z",
    "updateTime": "2022-06-21T11:55:15.115Z",
}


@pytest.fixture
def s3_product_aux_without_sep():
    product = CdsProductS3(**product_aux_without_sep_dict)
    product.full_clean()
    return product


cds_s3_completeness_sr_0_sra____dict = {
    "key": "S3B-072-276#SR_0_SRA___#ST",
    "datatake_id": "S3B-072-276",
    "mission": "S3",
    "satellite_unit": "S3B",
    "timeliness": "ST",
    "product_type": "SR_0_SRA___",
    "product_level": "L0_",
    "observation_time_start": "2022-11-09T05:13:32.938Z",
    "observation_time_stop": "2022-11-09T06:55:58.592Z",
    "value": 0,
    "expected": 5460000000,
    "value_adjusted": 0,
    "percentage": 0,
    "status": "Missing",
    "updateTime": "2022-11-30T13:04:31.750Z",
}


@pytest.fixture
def cds_s3_completeness_sr_0_sra___():
    s3_completeness = CdsS3Completeness(**cds_s3_completeness_sr_0_sra____dict)
    s3_completeness.full_clean()
    return s3_completeness


cds_s3_completeness_ol_0_efr_dict = {
    "key": "S3A-090-242#OL_0_EFR___#NR",
    "datatake_id": "S3A-090-242",
    "mission": "S3",
    "satellite_unit": "S3A",
    "timeliness": "NR",
    "product_type": "OL_0_EFR___",
    "product_level": "L0_",
    "observation_time_start": "2022-09-30T20:03:35.820Z",
    "observation_time_stop": "2022-09-30T20:47:51.340Z",
    "value": 0,
    "expected": 2640000000,
    "value_adjusted": 0,
    "percentage": 100,
    "status": "Complete",
    "updateTime": "2022-09-30T22:22:20.844Z",
}


@pytest.fixture
def cds_s3_completeness_ol_0_efr():
    s3_completeness = CdsS3Completeness(**cds_s3_completeness_ol_0_efr_dict)
    s3_completeness.full_clean()
    return s3_completeness


cds_s3_completeness_do_0_nav_dict = {
    "key": "S3A-086-281#DO_0_NAV___#AL",
    "datatake_id": "S3A-086-281",
    "mission": "S3",
    "satellite_unit": "S3A",
    "timeliness": "AL",
    "product_type": "DO_0_NAV___",
    "product_level": "L0_",
    "observation_time_start": "2022-06-17T13:39:22.942Z",
    "observation_time_stop": "2022-06-17T14:29:52.469Z",
    "value": 0,
    "expected": 6060000000,
    "value_adjusted": 0,
    "percentage": 0,
    "status": "Missing",
    "updateTime": "2022-07-18T14:52:03.292Z",
}


@pytest.fixture
def cds_s3_completeness_do_0_nav():
    s3_completeness = CdsS3Completeness(**cds_s3_completeness_do_0_nav_dict)
    s3_completeness.full_clean()
    return s3_completeness
