""" Module to test periodutils function"""

from unittest.mock import patch
import unittest
from maas_cds.lib.periodutils import (
    Period,
    compute_duplicated_indicator,
    reduce_periods,
)
from maas_cds.model.product import CdsProduct
from maas_model import datestr_to_utc_datetime


def test_reduce_periods_same():
    range_list = [
        ["20240205T100000", "20240205T100015"],
        ["20240205T100000", "20240205T100015"],
        ["20240205T100000", "20240205T100015"],
        ["20240205T100000", "20240205T100015"],
        ["20240205T100000", "20240205T100015"],
        ["20240205T100000", "20240205T100015"],
    ]
    periods = [
        Period(datestr_to_utc_datetime(i[0]), datestr_to_utc_datetime(i[1]))
        for i in range_list
    ]

    reduced = reduce_periods(periods)

    assert len(reduced) == 1


def test_reduce_periods_02():
    range_list = [
        ["20240205T100000", "20240205T100015"],
        ["20240205T100000", "20240205T100015"],
        ["20240205T100100", "20240205T100115"],
        ["20240205T100000", "20240205T100015"],
        ["20240205T100000", "20240205T100015"],
        ["20240205T100000", "20240205T100015"],
    ]
    periods = [
        Period(datestr_to_utc_datetime(i[0]), datestr_to_utc_datetime(i[1]))
        for i in range_list
    ]

    reduced = reduce_periods(periods)

    assert len(reduced) == 2


def test_reduce_periods_02_sort():
    range_list = [
        ["20240205T100000", "20240205T100000"],
        ["20240205T100000", "20240205T100100"],
        ["20240205T100001", "20240205T100200"],
        ["20240205T110000", "20240205T110000"],
        ["20240205T110000", "20240205T110100"],
    ]
    periods = [
        Period(datestr_to_utc_datetime(i[0]), datestr_to_utc_datetime(i[1]))
        for i in range_list
    ]

    reduced = reduce_periods(periods)

    assert reduced == [
        Period(
            datestr_to_utc_datetime("20240205T095945"),
            datestr_to_utc_datetime("20240205T100215"),
        ),
        Period(
            datestr_to_utc_datetime("20240205T105945"),
            datestr_to_utc_datetime("20240205T110115"),
        ),
    ]


def test_reduce_periods_03_sort():
    range_list = [
        ["20240205T100000", "20240205T100000"],
        ["20240205T100000", "20240205T100000"],
        ["20240205T100000", "20240205T100000"],
        ["20240205T100000", "20240205T100000"],
        ["20240205T100100", "20240205T100100"],
        ["20240205T100100", "20240205T100100"],
        ["20240205T100100", "20240205T100100"],
        ["20240205T100100", "20240205T100100"],
        ["20240205T100100", "20240205T100100"],
        ["20240205T110000", "20240205T110100"],
        ["20240205T110030", "20240205T110030"],
    ]
    periods = [
        Period(datestr_to_utc_datetime(i[0]), datestr_to_utc_datetime(i[1]))
        for i in range_list
    ]

    reduced = reduce_periods(periods)

    assert reduced == [
        Period(
            datestr_to_utc_datetime("20240205T095945"),
            datestr_to_utc_datetime("20240205T100015"),
        ),
        Period(
            datestr_to_utc_datetime("20240205T100045"),
            datestr_to_utc_datetime("20240205T100115"),
        ),
        Period(
            datestr_to_utc_datetime("20240205T105945"),
            datestr_to_utc_datetime("20240205T110115"),
        ),
    ]


def test_compute_duplicated_indicator_bug_product():
    product_a_dict = {
        "absolute_orbit": "54184",
        "datatake_id": "431850",
        "key": "8038e36cbdd75391476d09809c8ae3f2",
        "instrument_mode": "IW",
        "mission": "S1",
        "name": "S1A_IW_RAW__0ADV_20240605T054419_20240605T054838_054184_0696EA_0A22.SAFE.zip",
        "polarization": "DV",
        "product_class": "A",
        "product_type": "IW_RAW__0A",
        "product_level": "L0_",
        "satellite_unit": "S1A",
        "sensing_start_date": "2024-06-05T05:44:19.995Z",
        "sensing_end_date": "2024-06-05T05:48:38.226Z",
        "sensing_duration": 258231000,
        "timeliness": "NRT-PT",
        "content_length": 14421351,
        "prip_id": "58ef3889-27d0-40e2-a263-6bc9d3fe3343",
        "prip_publication_date": "2024-06-05T07:40:19.746Z",
        "prip_service": "PRIP_S1A_Serco",
        "updateTime": "2024-06-05T08:23:16.010Z",
        "expected_lta_number": 4,
        "LTA_CloudFerro_is_published": True,
        "LTA_CloudFerro_publication_date": "2024-06-05T07:45:56.793000+00:00",
        "nb_lta_served": 4,
        "LTA_Exprivia_S1_is_published": True,
        "LTA_Exprivia_S1_publication_date": "2024-06-05T07:51:35.488000+00:00",
        "dddas_name": "S1A_IW_RAW__0ADV_20240605T054419_20240605T054838_054184_0696EA_0A22.SAFE",
        "dddas_publication_date": "2024-06-05T07:45:50.983Z",
        "from_prip_dddas_timeliness": 331237000,
        "LTA_Werum_is_published": True,
        "LTA_Werum_publication_date": "2024-06-05T07:48:51.314000+00:00",
        "LTA_Acri_is_published": True,
        "LTA_Acri_publication_date": "2024-06-05T07:53:32.705000+00:00",
    }

    product_b_dict = {
        "absolute_orbit": "54184",
        "datatake_id": "431850",
        "key": "d9c60f574ae81fc17b5b93204efe52a9",
        "instrument_mode": "IW",
        "mission": "S1",
        "name": "S1A_IW_RAW__0ADV_20240605T054419_20240605T055540_054184_0696EA_31CC.SAFE.zip",
        "polarization": "DV",
        "product_class": "A",
        "product_type": "IW_RAW__0A",
        "product_level": "L0_",
        "satellite_unit": "S1A",
        "sensing_start_date": "2024-06-05T05:44:19.994Z",
        "sensing_end_date": "2024-06-05T05:55:40.106Z",
        "sensing_duration": 680112000,
        "timeliness": "NRT-PT",
        "content_length": 38014642,
        "prip_id": "cea62024-7901-4520-82c7-458bdcbbd5d6",
        "prip_publication_date": "2024-06-05T14:07:46.647Z",
        "prip_service": "PRIP_S1A_Serco",
        "updateTime": "2024-06-05T14:53:02.982Z",
        "dddas_name": "S1A_IW_RAW__0ADV_20240605T054419_20240605T055540_054184_0696EA_31CC.SAFE",
        "dddas_publication_date": "2024-06-05T14:13:41.040Z",
        "from_prip_dddas_timeliness": 354393000,
        "expected_lta_number": 4,
        "LTA_Acri_is_published": True,
        "LTA_Acri_publication_date": "2024-06-05T14:18:58.904000+00:00",
        "nb_lta_served": 4,
        "LTA_CloudFerro_is_published": True,
        "LTA_CloudFerro_publication_date": "2024-06-05T14:15:25.146000+00:00",
        "LTA_Werum_is_published": True,
        "LTA_Werum_publication_date": "2024-06-05T14:22:00.341000+00:00",
        "LTA_Exprivia_S1_is_published": True,
        "LTA_Exprivia_S1_publication_date": "2024-06-05T14:34:39.341000+00:00",
    }
    product_a = CdsProduct(**product_a_dict)
    product_a.meta.id = "8038e36cbdd75391476d09809c8ae3f2"
    product_a.meta.index = "cds-product-2024-06"
    product_a.full_clean()

    product_b = CdsProduct(**product_b_dict)
    product_b.meta.id = "d9c60f574ae81fc17b5b93204efe52a9"
    product_b.meta.index = "cds-product-2024-06"
    product_b.full_clean()

    # products_list = [product_b, product_a]
    periods_list = [
        Period(product_a.sensing_start_date, product_a.sensing_end_date),
        Period(product_b.sensing_start_date, product_b.sensing_end_date),
    ]

    # Periods are sorted
    periods_list.sort(key=lambda product: (product.start, product.end))

    assert {
        "avg_duration": 258231,
        "avg_percentage": 37.968893358740914,
        "max_duration": 258231,
        "max_percentage": 37.968893358740914,
        "min_duration": 258231,
        "min_percentage": 37.968893358740914,
    } == compute_duplicated_indicator(periods_list)
