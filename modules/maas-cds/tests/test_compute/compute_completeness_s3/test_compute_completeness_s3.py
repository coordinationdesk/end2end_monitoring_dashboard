from maas_cds.model.product_s3 import CdsProductS3
import pytest
import logging
import datetime

from unittest.mock import PropertyMock, patch
from dateutil.tz import tzutc
from maas_model.date_utils import datestr_to_utc_datetime
from maas_cds.model.cds_s3_completeness import CdsS3Completeness
from maas_cds.model.datatake import Period
from maas_cds.engines.compute.compute_s3_completeness import ComputeS3CompletenessEngine

# from collections import namedtuple

LOGGER = logging.getLogger("test_compute_completeness")

# Period = namedtuple("Period", ("start", "end"))


@pytest.fixture
def cds_s3_completeness_dict():
    """Get a basic cds_s3_completeness_dict
    matching
        mission:S3
        satellite_unit:S3B
        datatake_id:S3B-069-007
        product_type:OL_2_LFR___
        timeliness:NT

    Usefull to recreate a CdsS3Completeness
    Returns:
        dict: return a dict of a CdsS3Completeness
    """
    return {
        "key": "S3B-069-007#OL_2_LFR___#NT",
        "datatake_id": "S3B-069-007",
        "mission": "S3",
        "satellite_unit": "S3B",
        "timeliness": "NT",
        "product_type": "OL_2_LFR___",
        "product_level": "L2_",
        "observation_time_start": datestr_to_utc_datetime("2022-08-01T08:26:53.661Z"),
        "observation_time_stop": datestr_to_utc_datetime("2022-08-01T09:11:11.332Z"),
        "value": 2657671000,
        "expected": 2640000000,
        "value_adjusted": 2640000000,
        "percentage": 100,
        "status": "Complete",
        "updateTime": datestr_to_utc_datetime("2022-08-02T00:05:30.143Z"),
    }


@pytest.fixture
def product_s3_dict():
    """Get a basic s3 product dict
        matching
        mission:S3
        satellite_unit:S3B
        datatake_id:S3B-069-007
        product_type:OL_2_LFR___
        timeliness:NT

    Usefull to recreate a CdsProduct

    Returns:
        dict: return a dict of a CdsProduct
    """
    return {
        "datatake_id": "S3B-069-007",
        "key": "19a0270ee034fa34a17d4a8022c0b1a0",
        "mission": "S3",
        "name": "S3B_OL_2_LFR____20220801T090240_20220801T090540_20220801T231518_0179_069_007_3420_PS2_O_NT_002.SEN3.zip",
        "product_level": "L2_",
        "product_type": "OL_2_LFR___",
        "satellite_unit": "S3B",
        "sensing_start_date": datestr_to_utc_datetime("2022-08-01T09:02:40.151Z"),
        "sensing_end_date": datestr_to_utc_datetime("2022-08-01T09:05:40.151Z"),
        "sensing_duration": 180000000,
        "timeliness": "NT",
        "prip_id": "3c6cc078-a7b4-48f8-9bca-fa7d9a88801f",
        "prip_publication_date": datestr_to_utc_datetime("2022-08-01T23:19:42.543Z"),
        "prip_service": "PRIP_S3B_SERCO",
        "updateTime": datestr_to_utc_datetime("2022-08-01T23:52:36.109Z"),
        "ddip_name": "S3B_OL_2_LFR____20220801T090240_20220801T090540_20220801T231518_0179_069_007_3420_PS2_O_NT_002",
        "ddip_publication_date": datestr_to_utc_datetime("2022-08-01T23:23:06.268Z"),
    }


def get_implied_products():
    """Mock cds_s3_completeness.get_implied_products()
    matching
        mission:S3
        satellite_unit:S3B
        datatake_id:S3B-069-007
        product_type:OL_2_LFR___
        timeliness:NT

        Min start : 2022-08-01T08:26:53.661Z   Max end :2022-08-01T09:11:11.332Z => observation_period completeness_value
        All periods continuous duration = 2022-08-01T09:11:11.332Z - 2022-08-01T08:26:53.661Z = 2657671000 => completeness_value

    Returns:
        dict: return a list of maas_cds.model.datatake.Period Period(start=datetime,end=datetime)
    )
    """
    # pseudo sub set of products
    product_list = [
        {
            "datatake_id": "S3B-069-007",
            "key": "295999736c3fd24fdedfd9a108b43e1b",
            "mission": "S3",
            "name": "S3B_OL_2_LFR____20220801T085340_20220801T085640_20220801T231456_0179_069_007_2880_PS2_O_NT_002.SEN3.zip",
            "product_level": "L2_",
            "product_type": "OL_2_LFR___",
            "satellite_unit": "S3B",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-01T08:53:40.151Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-01T08:56:40.151Z"),
            "sensing_duration": 180000000,
            "timeliness": "NT",
            "prip_id": "0d474843-c874-4a92-9cd0-b29541a9f193",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:19:43.799Z"
            ),
            "prip_service": "PRIP_S3B_SERCO",
            "updateTime": datestr_to_utc_datetime("2022-08-01T23:52:35.966Z"),
            "ddip_name": "S3B_OL_2_LFR____20220801T085340_20220801T085640_20220801T231456_0179_069_007_2880_PS2_O_NT_002",
            "ddip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:23:05.574Z"
            ),
        },
        {
            "datatake_id": "S3B-069-007",
            "key": "19a0270ee034fa34a17d4a8022c0b1a0",
            "mission": "S3",
            "name": "S3B_OL_2_LFR____20220801T090240_20220801T090540_20220801T231518_0179_069_007_3420_PS2_O_NT_002.SEN3.zip",
            "product_level": "L2_",
            "product_type": "OL_2_LFR___",
            "satellite_unit": "S3B",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-01T09:02:40.151Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-01T09:05:40.151Z"),
            "sensing_duration": 180000000,
            "timeliness": "NT",
            "prip_id": "3c6cc078-a7b4-48f8-9bca-fa7d9a88801f",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:19:42.543Z"
            ),
            "prip_service": "PRIP_S3B_SERCO",
            "updateTime": datestr_to_utc_datetime("2022-08-01T23:52:36.109Z"),
            "ddip_name": "S3B_OL_2_LFR____20220801T090240_20220801T090540_20220801T231518_0179_069_007_3420_PS2_O_NT_002",
            "ddip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:23:06.268Z"
            ),
        },
        {
            "datatake_id": "S3B-069-007",
            "key": "07a40cbb5b78c6d935c0bc109cd09a90",
            "mission": "S3",
            "name": "S3B_OL_2_LFR____20220801T083840_20220801T084140_20220801T231420_0179_069_007_1980_PS2_O_NT_002.SEN3.zip",
            "product_level": "L2_",
            "product_type": "OL_2_LFR___",
            "satellite_unit": "S3B",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-01T08:38:40.151Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-01T08:41:40.151Z"),
            "sensing_duration": 180000000,
            "timeliness": "NT",
            "prip_id": "6190e96c-5a61-4c7b-b0ab-37e259bdb64c",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:19:43.538Z"
            ),
            "prip_service": "PRIP_S3B_SERCO",
            "updateTime": datestr_to_utc_datetime("2022-08-01T23:52:36.280Z"),
            "ddip_name": "S3B_OL_2_LFR____20220801T083840_20220801T084140_20220801T231420_0179_069_007_1980_PS2_O_NT_002",
            "ddip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:23:07.925Z"
            ),
        },
        {
            "datatake_id": "S3B-069-007",
            "key": "0623bebca03b309573441e7cc5f03225",
            "mission": "S3",
            "name": "S3B_OL_2_LFR____20220801T090540_20220801T090840_20220801T231525_0179_069_007_3600_PS2_O_NT_002.SEN3.zip",
            "product_level": "L2_",
            "product_type": "OL_2_LFR___",
            "satellite_unit": "S3B",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-01T09:05:40.151Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-01T09:08:40.151Z"),
            "sensing_duration": 180000000,
            "timeliness": "NT",
            "prip_id": "94e215f6-4c74-475a-821a-4489e6cdf2f7",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:19:42.912Z"
            ),
            "prip_service": "PRIP_S3B_SERCO",
            "updateTime": datestr_to_utc_datetime("2022-08-01T23:52:35.861Z"),
            "ddip_name": "S3B_OL_2_LFR____20220801T090540_20220801T090840_20220801T231525_0179_069_007_3600_PS2_O_NT_002",
            "ddip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:23:04.393Z"
            ),
        },
        {
            "datatake_id": "S3B-069-007",
            "key": "24e61b81c60c06036fa02d9d8434dcb6",
            "mission": "S3",
            "name": "S3B_OL_2_LFR____20220801T085940_20220801T090240_20220801T231511_0179_069_007_3240_PS2_O_NT_002.SEN3.zip",
            "product_level": "L2_",
            "product_type": "OL_2_LFR___",
            "satellite_unit": "S3B",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-01T08:59:40.151Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-01T09:02:40.151Z"),
            "sensing_duration": 180000000,
            "timeliness": "NT",
            "prip_id": "0228038b-4ebe-466e-a965-fadabe2a9b19",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:19:43.127Z"
            ),
            "prip_service": "PRIP_S3B_SERCO",
            "updateTime": datestr_to_utc_datetime("2022-08-01T23:52:35.915Z"),
            "ddip_name": "S3B_OL_2_LFR____20220801T085940_20220801T090240_20220801T231511_0179_069_007_3240_PS2_O_NT_002",
            "ddip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:23:04.821Z"
            ),
        },
        {
            "datatake_id": "S3B-069-007",
            "key": "bad2cfbd84752c4b30f935d724e49ea4",
            "mission": "S3",
            "name": "S3B_OL_2_LFR____20220801T084740_20220801T085040_20220801T231442_0179_069_007_2520_PS2_O_NT_002.SEN3.zip",
            "product_level": "L2_",
            "product_type": "OL_2_LFR___",
            "satellite_unit": "S3B",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-01T08:47:40.151Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-01T08:50:40.151Z"),
            "sensing_duration": 180000000,
            "timeliness": "NT",
            "prip_id": "c1a2ee66-a04f-43de-9e2e-c247d27b15ba",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:19:43.410Z"
            ),
            "prip_service": "PRIP_S3B_SERCO",
            "updateTime": datestr_to_utc_datetime("2022-08-01T23:52:36.374Z"),
            "ddip_name": "S3B_OL_2_LFR____20220801T084740_20220801T085040_20220801T231442_0179_069_007_2520_PS2_O_NT_002",
            "ddip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:23:08.346Z"
            ),
        },
        {
            "datatake_id": "S3B-069-007",
            "key": "36c27abb9b6a13c80303b76e8f15958b",
            "mission": "S3",
            "name": "S3B_OL_2_LFR____20220801T083240_20220801T083540_20220801T231405_0179_069_007_1620_PS2_O_NT_002.SEN3.zip",
            "product_level": "L2_",
            "product_type": "OL_2_LFR___",
            "satellite_unit": "S3B",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-01T08:32:40.151Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-01T08:35:40.151Z"),
            "sensing_duration": 180000000,
            "timeliness": "NT",
            "prip_id": "6f394fba-a6f1-4d80-9596-829cdf2fb2c1",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:19:43.001Z"
            ),
            "prip_service": "PRIP_S3B_SERCO",
            "updateTime": datestr_to_utc_datetime("2022-08-01T23:52:36.403Z"),
            "ddip_name": "S3B_OL_2_LFR____20220801T083240_20220801T083540_20220801T231405_0179_069_007_1620_PS2_O_NT_002",
            "ddip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:23:08.803Z"
            ),
        },
        {
            "datatake_id": "S3B-069-007",
            "key": "a518eba6237a201c0b4b1d8d3683e0b4",
            "mission": "S3",
            "name": "S3B_OL_2_LFR____20220801T083540_20220801T083840_20220801T231412_0179_069_007_1800_PS2_O_NT_002.SEN3.zip",
            "product_level": "L2_",
            "product_type": "OL_2_LFR___",
            "satellite_unit": "S3B",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-01T08:35:40.151Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-01T08:38:40.151Z"),
            "sensing_duration": 180000000,
            "timeliness": "NT",
            "prip_id": "f1714b5a-cac8-49b4-b5d7-71be4447da8a",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:19:43.787Z"
            ),
            "prip_service": "PRIP_S3B_SERCO",
            "updateTime": datestr_to_utc_datetime("2022-08-01T23:52:36.495Z"),
            "ddip_name": "S3B_OL_2_LFR____20220801T083540_20220801T083840_20220801T231412_0179_069_007_1800_PS2_O_NT_002",
            "ddip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:23:09.505Z"
            ),
        },
        {
            "datatake_id": "S3B-069-007",
            "key": "d59b89989cd3a67cafe12f1442d5c53b",
            "mission": "S3",
            "name": "S3B_OL_2_LFR____20220801T084140_20220801T084440_20220801T231427_0179_069_007_2160_PS2_O_NT_002.SEN3.zip",
            "product_level": "L2_",
            "product_type": "OL_2_LFR___",
            "satellite_unit": "S3B",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-01T08:41:40.151Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-01T08:44:40.151Z"),
            "sensing_duration": 180000000,
            "timeliness": "NT",
            "prip_id": "46afb2ab-87cf-4164-8c32-236dd6458117",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:19:44.214Z"
            ),
            "prip_service": "PRIP_S3B_SERCO",
            "updateTime": datestr_to_utc_datetime("2022-08-01T23:52:36.595Z"),
            "ddip_name": "S3B_OL_2_LFR____20220801T084140_20220801T084440_20220801T231427_0179_069_007_2160_PS2_O_NT_002",
            "ddip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:24:00.852Z"
            ),
        },
        {
            "datatake_id": "S3B-069-007",
            "key": "772e436a71042b0b9d4bbda2c9449139",
            "mission": "S3",
            "name": "S3B_OL_2_LFR____20220801T082654_20220801T082940_20220801T233942_0166_069_007_1260_PS2_O_NT_002.SEN3.zip",
            "product_level": "L2_",
            "product_type": "OL_2_LFR___",
            "satellite_unit": "S3B",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-01T08:26:53.661Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-01T08:29:40.151Z"),
            "sensing_duration": 166490000,
            "timeliness": "NT",
            "prip_id": "d896c8e1-df74-4e59-b712-80e2a9045c42",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:41:11.700Z"
            ),
            "prip_service": "PRIP_S3B_SERCO",
            "updateTime": datestr_to_utc_datetime("2022-08-02T00:07:19.410Z"),
            "ddip_name": "S3B_OL_2_LFR____20220801T082654_20220801T082940_20220801T233942_0166_069_007_1260_PS2_O_NT_002",
            "ddip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:47:01.988Z"
            ),
        },
        {
            "datatake_id": "S3B-069-007",
            "key": "d391789ab1af4daa82dafc40aee8ef36",
            "mission": "S3",
            "name": "S3B_OL_2_LFR____20220801T084440_20220801T084740_20220801T231434_0179_069_007_2340_PS2_O_NT_002.SEN3.zip",
            "product_level": "L2_",
            "product_type": "OL_2_LFR___",
            "satellite_unit": "S3B",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-01T08:44:40.151Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-01T08:47:40.151Z"),
            "sensing_duration": 180000000,
            "timeliness": "NT",
            "prip_id": "43066ec9-df91-4cdf-ba6b-d9bf69ea7c00",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:19:43.181Z"
            ),
            "prip_service": "PRIP_S3B_SERCO",
            "updateTime": datestr_to_utc_datetime("2022-08-01T23:52:35.934Z"),
            "ddip_name": "S3B_OL_2_LFR____20220801T084440_20220801T084740_20220801T231434_0179_069_007_2340_PS2_O_NT_002",
            "ddip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:23:05.158Z"
            ),
        },
        {
            "datatake_id": "S3B-069-007",
            "key": "a448de91259b6ceca3218bafd4143cea",
            "mission": "S3",
            "name": "S3B_OL_2_LFR____20220801T085040_20220801T085340_20220801T231449_0180_069_007_2700_PS2_O_NT_002.SEN3.zip",
            "product_level": "L2_",
            "product_type": "OL_2_LFR___",
            "satellite_unit": "S3B",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-01T08:50:40.151Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-01T08:53:40.151Z"),
            "sensing_duration": 180000000,
            "timeliness": "NT",
            "prip_id": "4f686d9c-a388-41a2-8767-372cf1a8ecd9",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:19:43.186Z"
            ),
            "prip_service": "PRIP_S3B_SERCO",
            "updateTime": datestr_to_utc_datetime("2022-08-01T23:52:36.084Z"),
            "ddip_name": "S3B_OL_2_LFR____20220801T085040_20220801T085340_20220801T231449_0180_069_007_2700_PS2_O_NT_002",
            "ddip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:23:05.904Z"
            ),
        },
        {
            "datatake_id": "S3B-069-007",
            "key": "fe702f9b0aeb94a69beb04bef539b87a",
            "mission": "S3",
            "name": "S3B_OL_2_LFR____20220801T082940_20220801T083240_20220801T231357_0180_069_007_1440_PS2_O_NT_002.SEN3.zip",
            "product_level": "L2_",
            "product_type": "OL_2_LFR___",
            "satellite_unit": "S3B",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-01T08:29:40.151Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-01T08:32:40.151Z"),
            "sensing_duration": 180000000,
            "timeliness": "NT",
            "prip_id": "457aae1f-80f9-4c60-858a-12926024b541",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:19:42.994Z"
            ),
            "prip_service": "PRIP_S3B_SERCO",
            "updateTime": datestr_to_utc_datetime("2022-08-01T23:52:36.203Z"),
            "ddip_name": "S3B_OL_2_LFR____20220801T082940_20220801T083240_20220801T231357_0180_069_007_1440_PS2_O_NT_002",
            "ddip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:23:06.684Z"
            ),
        },
        {
            "datatake_id": "S3B-069-007",
            "key": "d10875e7d75fbfa83e2a667218a01d9b",
            "mission": "S3",
            "name": "S3B_OL_2_LFR____20220801T085640_20220801T085940_20220801T231503_0179_069_007_3060_PS2_O_NT_002.SEN3.zip",
            "product_level": "L2_",
            "product_type": "OL_2_LFR___",
            "satellite_unit": "S3B",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-01T08:56:40.151Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-01T08:59:40.151Z"),
            "sensing_duration": 180000000,
            "timeliness": "NT",
            "prip_id": "6f9baf9b-70df-4053-bbbe-bf52fab65193",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:20:11.507Z"
            ),
            "prip_service": "PRIP_S3B_SERCO",
            "updateTime": datestr_to_utc_datetime("2022-08-01T23:52:36.557Z"),
            "ddip_name": "S3B_OL_2_LFR____20220801T085640_20220801T085940_20220801T231503_0179_069_007_3060_PS2_O_NT_002",
            "ddip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:23:09.976Z"
            ),
        },
        {
            "datatake_id": "S3B-069-007",
            "key": "97a465525a968138e156edbb8a3463d2",
            "mission": "S3",
            "name": "S3B_OL_2_LFR____20220801T090840_20220801T091111_20220801T233954_0151_069_007_3780_PS2_O_NT_002.SEN3.zip",
            "product_level": "L2_",
            "product_type": "OL_2_LFR___",
            "satellite_unit": "S3B",
            "sensing_start_date": datestr_to_utc_datetime("2022-08-01T09:08:40.151Z"),
            "sensing_end_date": datestr_to_utc_datetime("2022-08-01T09:11:11.332Z"),
            "sensing_duration": 151181000,
            "timeliness": "NT",
            "prip_id": "c151bea9-7159-4694-b702-0995727093d5",
            "prip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:41:11.285Z"
            ),
            "prip_service": "PRIP_S3B_SERCO",
            "updateTime": datestr_to_utc_datetime("2022-08-02T00:07:19.299Z"),
            "ddip_name": "S3B_OL_2_LFR____20220801T090840_20220801T091111_20220801T233954_0151_069_007_3780_PS2_O_NT_002",
            "ddip_publication_date": datestr_to_utc_datetime(
                "2022-08-01T23:47:01.402Z"
            ),
        },
    ]
    # get an iterator using iter()
    product_iter = iter(product_list)

    implied_documents = [
        Period(product["sensing_start_date"], product["sensing_end_date"])
        for product in product_iter
    ]

    # Sort document by sensing date
    implied_documents.sort(key=lambda product: product.start)

    return implied_documents


def test_completeness_init(cds_s3_completeness_dict):
    """Test Expected completeness creation list"""
    completeness_doc = CdsS3Completeness(**cds_s3_completeness_dict)
    datas_for_completnesses = completeness_doc.init_completenesses()
    assert key_exist(datas_for_completnesses, "S3B-069-007#DO_0_DOP___#NR")
    assert key_exist(datas_for_completnesses, "S3B-069-007#DO_0_NAV___#AL")
    assert key_exist(datas_for_completnesses, "S3B-069-007#GN_0_GNS___#NR")
    assert key_exist(datas_for_completnesses, "S3B-069-007#MW_0_MWR___#NR")
    assert key_exist(datas_for_completnesses, "S3B-069-007#MW_1_CAL___#NR")
    assert key_exist(datas_for_completnesses, "S3B-069-007#MW_1_MWR___#NR")
    assert key_exist(datas_for_completnesses, "S3B-069-007#MW_1_MWR___#NT")
    assert key_exist(datas_for_completnesses, "S3B-069-007#MW_1_MWR___#ST")
    assert key_exist(datas_for_completnesses, "S3B-069-007#OL_1_EFR___#NR")
    assert key_exist(datas_for_completnesses, "S3B-069-007#OL_1_EFR___#NT")
    assert key_exist(datas_for_completnesses, "S3B-069-007#OL_1_ERR___#NR")
    assert key_exist(datas_for_completnesses, "S3B-069-007#OL_1_ERR___#NT")
    assert key_exist(datas_for_completnesses, "S3B-069-007#OL_2_LFR___#NR")
    assert key_exist(datas_for_completnesses, "S3B-069-007#OL_2_LFR___#NT")
    assert key_exist(datas_for_completnesses, "S3B-069-007#OL_2_LRR___#NR")
    assert key_exist(datas_for_completnesses, "S3B-069-007#OL_2_LRR___#NT")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SL_1_RBT___#NR")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SL_1_RBT___#NT")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SL_2_LST___#NR")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SL_2_LST___#NT")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SR_0_SRA___#NR")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SR_0_SRA___#ST")
    assert not key_exist(datas_for_completnesses, "S3B-069-007#SR_1_SRA___#NR")
    assert not key_exist(datas_for_completnesses, "S3B-069-007#SR_1_SRA___#NT")
    assert not key_exist(datas_for_completnesses, "S3B-069-007#SR_1_SRA___#ST")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SY_1_MISR__#NT")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SY_1_MISR__#ST")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SY_2_AOD___#NT")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SY_2_SYN___#NT")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SY_2_SYN___#ST")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SY_2_VGK___#NT")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SY_2_VGK___#ST")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SY_2_VGP___#NT")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SY_2_VGP___#ST")
    assert key_exist(datas_for_completnesses, "S3B-069-007#TM_0_HKM2__#NR")
    assert key_exist(datas_for_completnesses, "S3B-069-007#TM_0_HKM___#NR")
    assert key_exist(datas_for_completnesses, "S3B-069-007#TM_0_NAT___#AL")

    # since maas_cds-777
    assert key_exist(datas_for_completnesses, "S3B-069-007#OL_0_EFR___#NR")
    assert not key_exist(datas_for_completnesses, "S3B-069-007#OL_0_EFR___#NT")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SL_0_SLT___#NR")
    assert not key_exist(datas_for_completnesses, "S3B-069-007#SL_0_SLT___#NT")
    assert not key_exist(datas_for_completnesses, "S3B-069-007#SL_2_FRP___#NR")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SL_2_FRP___#NT")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SR_1_SRA_A_#NR")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SR_1_SRA_A_#NT")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SR_1_SRA_A_#ST")
    assert not key_exist(datas_for_completnesses, "S3B-069-007#SR_1_SRA_BS#NR")
    assert not key_exist(datas_for_completnesses, "S3B-069-007#SR_1_SRA_BS#NT")
    assert not key_exist(datas_for_completnesses, "S3B-069-007#SR_1_SRA_BS#ST")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SR_1_LAN_RD#NT")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SR_1_LAN_RD#NR")
    assert key_exist(datas_for_completnesses, "S3B-069-007#SR_1_LAN_RD#ST")


def key_exist(collection, key):
    """utility method for key existence assertion"""
    is_key_exist = True
    try:
        exist = collection[key]
        if not exist:
            is_key_exist = False
    except KeyError:
        is_key_exist = False
    return is_key_exist


@patch(
    "maas_cds.model.cds_s3_completeness.CdsS3Completeness.get_implied_products",
    return_value=get_implied_products(),
)
def test_completeness_compute(cds_s3_completeness_dict):
    """Test completeness and observation period computation"""

    completeness_doc = CdsS3Completeness(**cds_s3_completeness_dict)
    completeness_value = completeness_doc.compute_values()
    observation_period = completeness_doc.compute_observation_period()

    assert completeness_value == 2657671000.0
    assert observation_period == Period(
        start=datetime.datetime(2022, 8, 1, 8, 26, 53, 661000, tzinfo=tzutc()),
        end=datetime.datetime(2022, 8, 1, 9, 11, 11, 332000, tzinfo=tzutc()),
    )


@patch("opensearchpy.Search.scan")
def test_compute_observation_period(
    mock_scan, cds_s3_completeness_dict, product_s3_dict
):
    completeness_doc = CdsS3Completeness(**cds_s3_completeness_dict)

    # Case no implied product found
    mock_scan.return_value = []
    res = completeness_doc.compute_observation_period()
    assert res == Period(
        completeness_doc.observation_time_start, completeness_doc.observation_time_stop
    )

    # Case implied product found
    prod_1 = CdsProductS3(**product_s3_dict)
    prod_2 = CdsProductS3(**product_s3_dict)
    prod_3 = CdsProductS3(**product_s3_dict)

    prod_2.sensing_start_date = datestr_to_utc_datetime("2022-09-01T09:02:40.151Z")
    prod_2.sensing_end_date = datestr_to_utc_datetime("2022-09-01T09:05:40.151Z")
    prod_3.sensing_start_date = datestr_to_utc_datetime("2022-05-01T09:02:40.151Z")
    prod_3.sensing_end_date = datestr_to_utc_datetime("2022-05-01T09:05:40.151Z")

    mock_scan.return_value = [prod_1, prod_2, prod_3]
    completeness_doc = CdsS3Completeness(**cds_s3_completeness_dict)
    assert completeness_doc.compute_observation_period() == Period(
        start=prod_3.sensing_start_date, end=prod_2.sensing_end_date
    )


@patch(
    "maas_cds.model.cds_s3_completeness.CdsS3Completeness.EXCLUDED_TYPES_FOR_COMPLETENESS",
    new_callable=PropertyMock,
    return_value=["ABC", "DEF"],
)
def test_completeness_exclusion(product_s3_dict):
    assert CdsS3Completeness.is_exclude_for_completeness("ABC") is True
    assert CdsS3Completeness.is_exclude_for_completeness("DEF") is True
    assert CdsS3Completeness.is_exclude_for_completeness("GHI") is False
