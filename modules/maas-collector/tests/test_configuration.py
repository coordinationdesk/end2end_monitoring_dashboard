import os

from maas_collector.rawdata import configuration
from maas_collector.rawdata.extractor.base import BaseExtractor

from maas_collector.rawdata.collector.filecollector import (
    FileCollector,
    FileCollectorConfiguration,
    CollectorArgs,
)

CURRENT_DIR = os.path.dirname(__file__)

CONF_DIR = os.path.join(CURRENT_DIR, "conf", "collector.d")

CONF1 = os.path.join(CONF_DIR, "conf1.json")

RESOLVE_DIR = os.path.join(CURRENT_DIR, "conf", "model_resolve")


def test_configuration():
    class MockDocument:
        pass

    class DumbExtractor(BaseExtractor):
        def extract(self, path, report_folder: str = ""):
            yield {}

    colconf = FileCollectorConfiguration(
        model=MockDocument,
        id_field="id_field",
        extractor=DumbExtractor,
        routing_key="routing.key",
        model_meta={},
    )
    assert colconf.name == "MockDocumentConfiguration"


def test_load_configuration():
    c = FileCollector(CollectorArgs(rawdata_config=CONF1))

    c.load_config()

    assert len(c.configs) == 1

    assert c.configs[0].name == "EmptyModel1Configuration"


def test_load_configuration_dir():
    c = FileCollector(CollectorArgs(rawdata_config_dir=CONF_DIR))

    c.load_config()

    assert len(c.configs) == 5

    # the sort behavior of os.walk is NOT determinist
    assert set(config.name for config in c.configs) == set(
        [
            "EmptyModel1Configuration",
            "EmptyModel2Configuration",
            "EmptyModel3Configuration",
            "EmptyModel4Configuration",
            "EmptyModel5Configuration",
        ]
    )


def test_postponed_models():
    c = FileCollector(CollectorArgs(rawdata_config_dir=RESOLVE_DIR))

    c.load_config()

    assert len(c.configs) == 2

    assert set(config.name for config in c.configs) == set(
        ["PostPonedModel1Configuration", "PostPonedModel2Configuration"]
    )
