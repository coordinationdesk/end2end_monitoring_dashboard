import datetime

from dateutil.tz import tzutc

from maas_model.date_utils import *


def test_datetime_to_zulu():
    assert (
        datetime_to_zulu(datetime.datetime(2020, 6, 21, 19, 56, 53, 456000))
        == "2020-06-21T19:56:53.456Z"
    )

    assert datetime_to_zulu(None) is None


def test_datestr_to_zulu():
    assert datestr_to_zulu("2020-06-21T21:56:53+02") == "2020-06-21T19:56:53.000Z"

    assert datestr_to_zulu(None) is None


def test_datestr_to_utc_datetime():
    assert datestr_to_utc_datetime("2020-06-21T21:56:53+02") == datetime.datetime(
        2020, 6, 21, 19, 56, 53, tzinfo=tzutc()
    )

    assert datestr_to_utc_datetime(None) is None
