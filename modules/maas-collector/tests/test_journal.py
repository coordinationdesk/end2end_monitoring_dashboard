from datetime import timedelta
from maas_collector.rawdata.collector.journal import CollectorJournal, CollectorReplayJournal
from maas_collector.rawdata.collector.odatacollector import (
    ODataCollectorConfiguration
)

CONF3 = {
    "id_field": "",
    "routing_key": "",
    "interface_name": "face_palm",
    "refresh_interval": 10,
    "model": {
        "fields": [],
        "index": "",
        "name": "EmptyModel2"
    },
    "model_meta": {},
    "extractor": {
        "class": "LogExtractor",
        "args": {
            "pattern": ".*"
        }
    }
}

def test_journal():

    config = ODataCollectorConfiguration(**CONF3)

    journal = CollectorJournal(config)

    assert journal.id == "face_palm"

def test_replay_journal():

    start_date = timedelta(days=1)
    end_date = timedelta(weeks=40, days=84, hours=23, minutes=50, seconds=600)

    config = ODataCollectorConfiguration(**CONF3)
    
    journal = CollectorReplayJournal(config, start_date, end_date)

    assert journal.id == "face_palm"

    journal = CollectorReplayJournal(config, start_date, end_date, suffix="scissors")

    assert journal.id == "face_palm_scissors"
