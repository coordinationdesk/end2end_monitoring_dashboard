import datetime
import os

import opensearchpy

from maas_collector.rawdata.configuration import (
    build_model_class,
    build_extractor,
    build_collector_configuration,
)

from maas_model import ZuluDate

from maas_collector.rawdata.collector.filecollector import FileCollectorConfiguration

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def test_build_model_class():
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

    # class name check
    assert DSIB.__name__ == meta_dict["name"]

    # class attribute check
    for field_meta in meta_dict["fields"]:
        if field_meta["type"] == "Date":
            class_obj = ZuluDate
        else:
            class_obj = getattr(opensearchpy, field_meta["type"])
        es_field = DSIB._ObjectBase__get_field(field_meta["name"])
        assert isinstance(es_field, class_obj)

    # instance attribute check
    now = datetime.datetime.now()

    dsib = DSIB(sessionID="42", timeFinished=now, dataSize=23)

    assert dsib.sessionID == "42"
    assert dsib.timeFinished == now
    assert dsib.dataSize == 23


def test_build_xml_extractor():
    meta = {
        "class": "XMLExtractor",
        "args": {
            "attr_map": {
                "sessionID": "session_id",
                "dataSize": "data_size",
                "timeFinished": "time_finished",
            }
        },
    }

    xext = build_extractor(meta)
    extract = list(
        xext.extract(
            os.path.join(
                DATA_DIR,
                "DCS_02_L20191003131732787001008_ch1_DSIB.xml",
            )
        )
    )[0]

    assert extract == {
        "sessionID": "L20191003131732787001008",
        "dataSize": "8819975080",
        "timeFinished": "2019-12-08T05:12:27Z",
        "reportName": "DCS_02_L20191003131732787001008_ch1_DSIB.xml",
    }


def test_build_collector_configuration():
    meta = {
        "model": {
            "index": "raw-data-dsib",
            "name": "DSIB",
            "fields": [
                {"name": "sessionID", "type": "Keyword"},
                {"name": "timeFinished", "type": "Date"},
                {"name": "dataSize", "type": "Long"},
            ],
        },
        "extractor": {
            "class": "XMLExtractor",
            "args": {
                "attr_map": {
                    "sessionID": "session_id",
                    "dataSize": "data_size",
                    "timeFinished": "time_finished",
                }
            },
        },
        "id_field": "sessionID",
        "file_pattern": "*_DSIB.xml",
        "routing_key": "new.raw.data.dsib",
    }

    config = build_collector_configuration(meta, FileCollectorConfiguration)

    extract = list(
        config.extractor.extract(
            os.path.join(
                DATA_DIR,
                "DCS_02_L20191003131732787001008_ch1_DSIB.xml",
            )
        )
    )[0]

    assert extract == {
        "sessionID": "L20191003131732787001008",
        "dataSize": "8819975080",
        "timeFinished": "2019-12-08T05:12:27Z",
        "reportName": "DCS_02_L20191003131732787001008_ch1_DSIB.xml",
    }
