""" Module to test periodutils function"""

from unittest.mock import patch
import unittest
from maas_cds.lib.periodutils import Period, reduce_periods
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
