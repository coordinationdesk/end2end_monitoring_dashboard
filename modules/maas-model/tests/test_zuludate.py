import datetime

from maas_model import ZuluDate


def test_zulu_date():
    zd = ZuluDate()

    now = datetime.datetime.now()

    serialized = zd.serialize(now)

    assert serialized == now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    deserialized = zd.deserialize(serialized)

    assert deserialized.year == now.year
    assert deserialized.month == now.month
    assert deserialized.day == now.day
    assert deserialized.hour == now.hour
    assert deserialized.minute == now.minute

    # compare milliseconds as microseconds are ignored in ZuluDate implementation
    assert deserialized.microsecond // 1000 == now.microsecond // 1000

    # compare reversibility of serialize/deserialize
    serialized2 = zd.serialize(deserialized)

    assert serialized == serialized2

    # test utc zone convertion

    date_str = "2021-10-05T12:00:41.000+0200"

    zulu_str = "2021-10-05T10:00:41.000Z"

    serialized2 = zd.serialize(date_str)

    assert serialized2 == zulu_str

    # test if a zulu date is serialized without any modification
    serialized2 = zd.serialize(zulu_str)

    assert serialized2 == zulu_str

    # test time zone deserialisation
    now = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(minutes=120)))
    deserialized = zd.deserialize(now)

    assert deserialized.tzname() == "UTC"

    assert deserialized == now


def test_zulu_before_year_1000():

    zd = ZuluDate()
    d = datetime.datetime(1, 1, 1, tzinfo=datetime.timezone.utc)
    serialized = zd.serialize(d)
    assert serialized == "0001-01-01T00:00:00.000Z"
    assert zd.deserialize(serialized) == d
