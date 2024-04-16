import pytest
import logging
import datetime

from unittest.mock import patch
from dateutil.tz import tzutc
from maas_model.date_utils import datestr_to_utc_datetime
from maas_cds.model.cds_s5_completeness import CdsS5Completeness
from maas_cds.model.product_s5 import CdsProductS5

from maas_cds.model.datatake import Period


LOGGER = logging.getLogger("test_compute_completeness")


@pytest.fixture
def cds_s5_completeness_dict():
    """Get a basic cds_s5_completeness_dict
    matching
        matching
        mission:S5
        satellite_unit:S5P
        datatake_id:S5P-25100
        product_type:NRTI_L1B_ENG_DB
        timeliness:NRTI

    Usefull to recreate a CdsS5Completeness
    Returns:
        dict: return a dict of a CdsS5Completeness
    """
    return {
        "key": "S5P-25100-NRTI_L1B_ENG_DB",
        "datatake_id": "S5P-25100",
        "absolute_orbit": 25100,
        "mission": "S5",
        "satellite_unit": "S5P",
        "timeliness": "NRTI",
        "product_type": "NRTI_L1B_ENG_DB",
        "product_level": "L1_",
        "observation_time_start": datestr_to_utc_datetime("2022-08-17T13:16:13.000Z"),
        "observation_time_stop": datestr_to_utc_datetime("2022-08-17T14:58:23.000Z"),
        "value": 6130000000,
        "expected": 6000000000,
        "value_adjusted": 6000000000,
        "percentage": 100,
        "status": "Complete",
        "slice_value": 20,
        "slice_expected": 21,
    }


@pytest.fixture
def product_s5_dict():
    """Get a basic s5 product dict
    matching
        mission:S5
        satellite_unit:S5P
        datatake_id:S5P-25100
        product_type:NRTI_L1B_ENG_DB
        timeliness:NRTI

    Usefull to recreate a CdsProduct

    Returns:
        dict: return a dict of a CdsProduct
    """
    return {
        "absolute_orbit": 25100,
        "datatake_id": "S5P-25100",
        "key": "fce60c4156201436b2a90ed3da60f021",
        "mission": "S5",
        "name": "S5P_NRTI_L1B_ENG_DB_20220817T134212_20220817T134724_25100_03_020100_20220817T143010.nc",
        "product_level": "L1_",
        "product_type": "NRTI_L1B_ENG_DB",
        "satellite_unit": "S5P",
        "collection_number": "03",
        "processor_version": "020100",
        "sensing_start_date": datestr_to_utc_datetime("2022-08-17T13:41:19.000Z"),
        "sensing_end_date": datestr_to_utc_datetime("2022-08-17T13:48:23.000Z"),
        "sensing_duration": 424000000,
        "timeliness": "NRTI",
        "prip_id": "50cadbdb-a1e0-48f9-b678-38d75f0bc8bd",
        "prip_publication_date": datestr_to_utc_datetime("2022-08-17T14:37:11.877Z"),
        "prip_service": "PRIP_S5P_DLR",
        "updateTime": datestr_to_utc_datetime("2022-08-17T15:13:44.937Z"),
    }


def get_implied_products():
    """Mock cds_s5_completeness.get_implied_products()
    matching
        mission:S5
        satellite_unit:S5P
        datatake_id:S5P-25100
        product_type:NRTI_L1B_ENG_DB
        timeliness:NRTI

        Min start : 2022-08-01T08:26:53.661Z   Max end :2022-08-01T09:11:11.332Z => observation_period completeness_value
        All periods continuous duration = 2022-08-01T09:11:11.332Z - 2022-08-01T08:26:53.661Z = 2657671000 => completeness_value

    Returns:
        dict: return a list of maas_cds.model.datatake.Period Period(start=datetime,end=datetime)
    )
    """
    # pseudo sub set of products
    product_list = [
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "19b68040ba998a46bd02b2854c4dde81",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T142212_20220817T142724_25100_03_020100_20220817T160407.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T14:21:29.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T14:28:23.000Z"),
            "sensing_duration": 414000000,
            "timeliness": "NRTI",
            "prip_id": "b52d82cb-bbbd-4bcd-9a3c-b9817d73ba0c",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T16:10:16.643Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T16:38:32.727Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "fce60c4156201436b2a90ed3da60f021",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T134212_20220817T134724_25100_03_020100_20220817T143010.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T13:41:19.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T13:48:23.000Z"),
            "sensing_duration": 424000000,
            "timeliness": "NRTI",
            "prip_id": "50cadbdb-a1e0-48f9-b678-38d75f0bc8bd",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T14:37:11.877Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T15:13:44.937Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "5e3d23581430d24c2dd7e4c332207c17",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T135212_20220817T135724_25100_03_020100_20220817T143024.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T13:51:13.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T13:58:23.000Z"),
            "sensing_duration": 430000000,
            "timeliness": "NRTI",
            "prip_id": "730b7c68-e6ce-4137-917e-66fb8147f344",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T14:38:06.448Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T15:13:44.963Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "33a9733a309a5613e0da18ecb54d8fc4",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T140212_20220817T140724_25100_03_020100_20220817T143259.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T14:01:19.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T14:08:23.000Z"),
            "sensing_duration": 424000000,
            "timeliness": "NRTI",
            "prip_id": "bec4eddb-f574-40f2-a474-f7097d41d8b3",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T14:39:40.325Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T15:13:44.989Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "301de14d05d778224d9f8e85bbb0a2b9",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T140712_20220817T141224_25100_03_020100_20220817T143308.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T14:06:13.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T14:13:23.000Z"),
            "sensing_duration": 430000000,
            "timeliness": "NRTI",
            "prip_id": "66278793-3d31-48ee-9319-a84a5ee6ee43",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T14:39:52.341Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T15:13:45.007Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "c93d62f12b3266a8d97747b839810815",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T131712_20220817T132224_25100_03_020100_20220817T142746.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T13:16:13.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T13:23:23.000Z"),
            "sensing_duration": 430000000,
            "timeliness": "NRTI",
            "prip_id": "584c6fd1-f9e0-46d2-bd89-b60b630c62eb",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T14:29:57.067Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T14:55:25.667Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "a64da37d3ba106924cb34fcfd91e990c",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T132712_20220817T133224_25100_03_020100_20220817T142806.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T13:26:13.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T13:33:23.000Z"),
            "sensing_duration": 430000000,
            "timeliness": "NRTI",
            "prip_id": "64096578-4683-4529-9b5d-873e02f8b92c",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T14:30:27.070Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T14:55:25.673Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "e674f700440651397b575f9ae71d239a",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T134712_20220817T135224_25100_03_020100_20220817T143017.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T13:46:13.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T13:53:23.000Z"),
            "sensing_duration": 430000000,
            "timeliness": "NRTI",
            "prip_id": "1ac7a545-3acf-483b-85f8-63699006bd1b",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T14:37:39.113Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T15:13:44.947Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "bfa6e1d8a898be3f4229a5cb8503eb42",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T143212_20220817T143724_25100_03_020100_20220817T160421.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T14:31:13.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T14:38:23.000Z"),
            "sensing_duration": 430000000,
            "timeliness": "NRTI",
            "prip_id": "b1be6f37-0bc9-4795-b7a9-95c55ac90aef",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T16:06:28.568Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T16:23:05.405Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "fb8fd2bc1108b3e615fd26cd19ab1baa",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T143712_20220817T144224_25100_03_020100_20220817T160544.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T14:36:13.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T14:43:23.000Z"),
            "sensing_duration": 430000000,
            "timeliness": "NRTI",
            "prip_id": "de314423-9282-4c1c-9265-7c807fb6ff59",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T16:07:27.216Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T16:38:32.675Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "a9ea40d98c737c1aae154afcb64e2e77",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T144212_20220817T144724_25100_03_020100_20220817T160552.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T14:41:27.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T14:48:23.000Z"),
            "sensing_duration": 416000000,
            "timeliness": "NRTI",
            "prip_id": "f7ba5cff-07c4-4007-ab1a-65267f05334c",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T16:08:57.131Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T16:38:32.681Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "9acecb99d571e6f7d280f3d3ed5fa86b",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T145212_20220817T145724_25100_03_020100_20220817T160604.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T14:51:13.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T14:58:23.000Z"),
            "sensing_duration": 430000000,
            "timeliness": "NRTI",
            "prip_id": "186b4f5b-12a3-4ab2-9d09-e050157c8ee7",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T16:08:57.152Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T16:38:32.683Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "b80eb5debaa98b8d7d2e00d4a0aab93d",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T142712_20220817T143224_25100_03_020100_20220817T160414.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T14:26:13.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T14:33:23.000Z"),
            "sensing_duration": 430000000,
            "timeliness": "NRTI",
            "prip_id": "adb21037-05a0-4fd8-9a0a-dc979dcf0682",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T16:10:22.286Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T16:38:32.735Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "26796c3955ecf923d2fce2c510b0a0a5",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T132212_20220817T132724_25100_03_020100_20220817T142755.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T13:21:19.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T13:28:23.000Z"),
            "sensing_duration": 424000000,
            "timeliness": "NRTI",
            "prip_id": "1e0eed0b-f680-41f5-8fbe-ee82be81a3c8",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T14:29:57.125Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T14:55:25.670Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "ff7541b7bc67f9037a90da2e6eafb882",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T133212_20220817T133724_25100_03_020100_20220817T142814.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T13:31:13.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T13:38:23.000Z"),
            "sensing_duration": 430000000,
            "timeliness": "NRTI",
            "prip_id": "87576c1a-73ac-4d8d-882d-d54f75b69bc0",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T14:32:00.623Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T14:55:25.718Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "6615fe4064b79836e532a9949a8b4cd7",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T133712_20220817T134224_25100_03_020100_20220817T143001.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T13:36:13.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T13:43:23.000Z"),
            "sensing_duration": 430000000,
            "timeliness": "NRTI",
            "prip_id": "65e88791-fbd8-44e6-a211-9604be3f0efb",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T14:37:08.829Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T15:13:44.930Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "6feeb3793d19c595d967de04fe96ef29",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T135712_20220817T140224_25100_03_020100_20220817T143250.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T13:56:13.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T14:03:23.000Z"),
            "sensing_duration": 430000000,
            "timeliness": "NRTI",
            "prip_id": "5fd8b86f-74d1-4a40-a793-a0715805e2fd",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T14:39:37.643Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T15:13:44.978Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "a664df83067425c8c8994915a499afc7",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T141212_20220817T141724_25100_03_020100_20220817T143317.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T14:11:13.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T14:18:23.000Z"),
            "sensing_duration": 430000000,
            "timeliness": "NRTI",
            "prip_id": "cea8546b-1379-4098-84df-3b6f4414dc42",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T14:39:49.088Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T15:13:44.996Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "63507364810f72def9983d406e79dbf8",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T144712_20220817T145224_25100_03_020100_20220817T160559.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T14:46:13.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T14:53:23.000Z"),
            "sensing_duration": 430000000,
            "timeliness": "NRTI",
            "prip_id": "25d02f04-75ae-4382-af0d-4a08c8101411",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T16:08:57.205Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T16:38:32.686Z"),
        },
        {
            "absolute_orbit": 25100,
            "datatake_id": "S5P-25100",
            "key": "78144f7cbe0b730545a128d44f2d055a",
            "mission": "S5",
            "name": "S5P_NRTI_L1B_ENG_DB_20220817T141712_20220817T142224_25100_03_020100_20220817T160401.nc",
            "product_level": "L1_",
            "product_type": "NRTI_L1B_ENG_DB",
            "satellite_unit": "S5P",
            "collection_number": "03",
            "processor_version": "020100",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-17T14:16:13.000Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-17T14:23:23.000Z"),
            "sensing_duration": 430000000,
            "timeliness": "NRTI",
            "prip_id": "f04d3430-1263-4c15-aab0-f2841595b0fa",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-17T16:10:13.174Z"
            ),
            "prip_service": "PRIP_S5P_DLR",
            "updateTime": datestr_to_utc_datetime("2022-08-17T16:38:32.714Z"),
        },
    ]

    implied_documents = []

    for prod in product_list:
        implied_documents.append(CdsProductS5(**prod))

    return implied_documents


def test_completeness_init(cds_s5_completeness_dict):
    """Test Expected completeness creation list"""
    completeness_doc = CdsS5Completeness(**cds_s5_completeness_dict)
    datas_for_completnesses = completeness_doc.init_completenesses()
    assert key_exist(datas_for_completnesses, "S5P-25100-OPER_L0__SAT_A_")
    assert key_exist(datas_for_completnesses, "S5P-25100-OPER_L0__PDQ___")
    assert key_exist(datas_for_completnesses, "S5P-25100-OPER_L0__ODB_8_")
    assert key_exist(datas_for_completnesses, "S5P-25100-OPER_L0__ODB_7_")
    assert key_exist(datas_for_completnesses, "S5P-25100-OPER_L0__ODB_6_")
    assert key_exist(datas_for_completnesses, "S5P-25100-OPER_L0__ODB_5_")
    assert key_exist(datas_for_completnesses, "S5P-25100-OPER_L0__ODB_4_")
    assert key_exist(datas_for_completnesses, "S5P-25100-OPER_L0__ODB_3_")
    assert key_exist(datas_for_completnesses, "S5P-25100-OPER_L0__ODB_2_")
    assert key_exist(datas_for_completnesses, "S5P-25100-OPER_L0__ODB_1_")
    assert key_exist(datas_for_completnesses, "S5P-25100-OPER_L0__ENG_A_")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L2__SO2___")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L2__O3____")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L2__O3__PR")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L2__NP_BD7")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L2__NP_BD6")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L2__NP_BD3")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L2__NO2___")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L2__HCHO__")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L2__FRESCO")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L2__CO____")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L2__CLOUD_")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L2__CH4___")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L2__AER_LH")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L2__AER_AI")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L1__CA_UVN")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L1__CA_SIR")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L1B_RA_BD8")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L1B_RA_BD7")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L1B_RA_BD6")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L1B_RA_BD5")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L1B_RA_BD4")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L1B_RA_BD3")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L1B_RA_BD2")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L1B_RA_BD1")
    assert key_exist(datas_for_completnesses, "S5P-25100-OFFL_L1B_ENG_DB")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L2__SO2___")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L2__O3____")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L2__O3__PR")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L2__NO2___")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L2__HCHO__")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L2__FRESCO")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L2__CO____")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L2__CLOUD_")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L2__AER_LH")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L2__AER_AI")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L1B_RA_BD8")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L1B_RA_BD7")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L1B_RA_BD6")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L1B_RA_BD5")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L1B_RA_BD4")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L1B_RA_BD3")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L1B_RA_BD2")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L1B_RA_BD1")
    assert key_exist(datas_for_completnesses, "S5P-25100-NRTI_L1B_ENG_DB")


def key_exist(collection, key):
    """utility method for key existence assertion"""
    key_exist = True
    try:
        exist = collection[key]
        if not exist:
            key_exist = False
    except KeyError:
        key_exist = False
    return key_exist


@patch(
    "maas_cds.model.cds_s5_completeness.CdsS5Completeness.get_implied_products",
    return_value=get_implied_products(),
)
def test_completeness_compute(cds_s5_completeness_dict):
    """Test completeness and observation period computation"""

    completeness_doc = CdsS5Completeness(**cds_s5_completeness_dict)
    sensing_value, slice_value, observation_period = completeness_doc.compute()

    assert sensing_value == 6130000000.0
    assert slice_value == 20
    assert observation_period == Period(
        start=datetime.datetime(2022, 8, 17, 13, 16, 13, tzinfo=tzutc()),
        end=datetime.datetime(2022, 8, 17, 14, 58, 23, tzinfo=tzutc()),
    )


def test_expected_with_tolerence(cds_s5_completeness_dict):
    """Test completeness and observation period computation"""

    completeness_doc = CdsS5Completeness(**cds_s5_completeness_dict)
    completeness_doc.COMPLETENESS_TOLERANCE = {
        "S5": {
            "local": {
                "OPER_L0__(ENG_A_|ODB_[1-8]_|SAT_A)": -180000000,
                "NRTI_L1B_(ENG_DB|RA_BD[1-8])": -180000000,
                "NRTI_L2__(AER_AI|AER_LH|CLOUD_|CO____|FRESCO|HCHO__|NO2___|O3__PR|O3____|SO2___)": -180000000,
                "OFFL_L1B_(ENG_DB|RA_BD[1-8])": -180000000,
                "OFFL_L2__(AER_AI|AER_LH|CH4___|CLOUD_|CO____|FRESCO|HCHO__|NO2___|NP_BD(3|6|7)|O3__PR|O3____|SO2___)": -180000000,
            }
        }
    }
    assert completeness_doc.get_expected_value() == 5820000000
    completeness_doc.product_type = "NRTI_L2__FRESCO"
    assert completeness_doc.get_expected_value() == 3120000000


def test_not_computed_completeness():
    # MAAS_CDS-1105
    assert CdsS5Completeness.is_exclude_for_completeness("OFFL_L1B_CA_SIR") is True

    assert CdsS5Completeness.is_exclude_for_completeness("OPER_L0__ODB_8_") is False
