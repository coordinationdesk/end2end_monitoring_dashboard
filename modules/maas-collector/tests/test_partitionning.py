import datetime
import os

from maas_collector.rawdata.configuration import build_model_class

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def test_partition_no_conf():
    """check base behavior of mapping classes building"""
    meta_dict = {
        "index": "raw-data-dsib",
        "name": "DSIB",
        "fields": [
            {"name": "sessionID", "type": "Keyword"},
            {"name": "timeFinished", "type": "Date"},
            {"name": "dataSize", "type": "Long"},
        ],
    }

    DSIB = build_model_class(meta_dict)

    # instance attribute check
    now = datetime.datetime.now()

    dsib = DSIB(
        sessionID="42",
        timeFinished=now - datetime.timedelta(days=10),  # to be != of ingestionTime
        dataSize=23,
        ingestionTime=now,
    )

    assert DSIB._PARTITION_FIELD == "ingestionTime"

    # default behavior
    assert DSIB._PARTITION_FIELD_FORMAT == "%Y"

    assert dsib.partition_index_name == f"raw-data-dsib-{now.strftime('%Y')}"


def test_partition_with_field():
    """check base behavior of mapping classes building"""
    meta_dict = {
        "index": "raw-data-dsib",
        "name": "DSIB",
        "fields": [
            {"name": "sessionID", "type": "Keyword"},
            {"name": "timeFinished", "type": "Date"},
            {"name": "dataSize", "type": "Long"},
        ],
        "partition_field": "timeFinished",
    }

    DSIB = build_model_class(meta_dict)

    # instance attribute check
    now = datetime.datetime.now()

    timeFinished = now - datetime.timedelta(days=60)  # to be != of ingestionTime

    dsib = DSIB(
        sessionID="42",
        timeFinished=timeFinished,
        ingestionTime=now,
        dataSize=23,
    )

    assert DSIB._PARTITION_FIELD == "timeFinished"

    assert DSIB._PARTITION_FIELD_FORMAT == "%Y"

    assert dsib.partition_index_name == f"raw-data-dsib-{timeFinished.strftime('%Y')}"


def test_partition_with_field_format():
    """check base behavior of mapping classes building"""
    meta_dict = {
        "index": "raw-data-dsib",
        "name": "DSIB",
        "fields": [
            {"name": "sessionID", "type": "Keyword"},
            {"name": "timeFinished", "type": "Date"},
            {"name": "dataSize", "type": "Long"},
        ],
        "partition_field": "timeFinished",
        "partition_format": "%Y-%m",
    }

    DSIB = build_model_class(meta_dict)

    # instance attribute check
    now = datetime.datetime.now()

    timeFinished = now - datetime.timedelta(days=60)  # to be != of ingestionTime

    dsib = DSIB(
        sessionID="42", timeFinished=timeFinished, ingestionTime=now, dataSize=23
    )

    assert DSIB._PARTITION_FIELD == "timeFinished"

    assert DSIB._PARTITION_FIELD_FORMAT == "%Y-%m"

    assert (
        dsib.partition_index_name == f"raw-data-dsib-{timeFinished.strftime('%Y-%m')}"
    )
