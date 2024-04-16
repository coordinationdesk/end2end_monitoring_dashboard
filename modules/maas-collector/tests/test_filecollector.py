"""some file collector testing"""
import datetime
import os
import logging
import sys

import pytest

from maas_collector.rawdata.collector.filecollector import (
    CollectorArgs,
    FileCollectorConfiguration,
    FileCollector,
)

from conftest import mock_client

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

TEST_CONF = os.path.join(
    os.path.dirname(__file__), "conf", "test-maas-filecollector.json"
)


def test_filecollector_init(monkeypatch):

    args = CollectorArgs(rawdata_config=TEST_CONF)

    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    collector = FileCollector(args)

    # ignore setup
    monkeypatch.setattr(collector, "setup", lambda: True)
    collector.setup()

    print(collector.configs)

    # tada try ingest something and have the mock classes AHAH
    collector.ingest(
        os.path.join(
            DATA_DIR,
            "S2A_OPER_PRD_L0__DS_SGS__20200420T205828_S20200322T173347_SIZE.xml",
        )
    )


def test_get_date_dirname():
    d = datetime.datetime(1977, 1, 23)
    assert FileCollector.get_date_dirname(d) == "1977/01/23"
