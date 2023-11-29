from unittest.mock import patch

from maas_engine.engine.rawdata import RawDataEngine

from maas_cds.engines.reports.mission_mixin import MissionMixinEngine

from maas_cds import model


class SomeTestEngine(MissionMixinEngine, RawDataEngine):
    pass


def test_mission_mixin():

    engine = SomeTestEngine()

    document = model.CdsProduct(mission="S1")

    assert engine.get_report_action("created", document) == "new.cds-product-s1"

    assert engine.get_report_document_classname(document) == "CdsProductS1"


def test_mission_mixin_no_specifix_model():

    engine = SomeTestEngine()

    class SomeModel:
        mission = "any"

    assert engine.get_report_document_classname(SomeModel()) == "SomeModel"
