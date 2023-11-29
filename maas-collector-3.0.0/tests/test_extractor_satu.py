"""SatUnavailabilityExtractor tests"""
import os

from opensearchpy import (
    Text,
    Integer,
    Keyword,
)

from maas_model import MAASRawDocument
from maas_collector.rawdata.extractor import SatUnavailabilityExtractor


DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


class SatUnavailabilityProduct(MAASRawDocument):
    class Index:
        name = "raw-data-sat-unavailability-product"

    _PARTITION_FIELD = "ingestionTime"
    _PARTITION_FIELD_FORMAT = "static"

    comment = Text()

    end_anx_offset = Integer()

    end_orbit = Keyword()

    end_time = Text()

    file_name = Text()

    interface_name = Keyword()

    mission = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    start_anx_offset = Integer()

    start_orbit = Keyword()

    start_time = Text()

    subsystem = Keyword()

    type = Keyword()

    unavailability_reference = Keyword()

    unavailability_type = Keyword()


def test_satu_extractor():
    jext = SatUnavailabilityExtractor()

    extract = list(
        jext.extract(
            os.path.join(
                DATA_DIR,
                "S5P_OPER_REP__SUP___20221007T012935_20221007T035455_0001.EOF.xml",
            )
        )
    )[0]

    assert extract["start_orbit"] == "25817"
    assert extract["end_orbit"] == "25818"

    satu_product = SatUnavailabilityProduct(**extract)

    satu_product.full_clean()

    assert satu_product.to_dict() == {
        "comment": "Due to a collision risk identified for Sentinel-5P on 07/10/2022 "
        "a Collision Avoidance Manoeuvre (CAM) has been scheduled. Refer "
        "to event #27468 in SCARF for further details.",
        "end_orbit": "25818",
        "end_time": "UTC=2022-10-07T03:54:55",
        "file_name": "S5P_OPER_REP__SUP___20221007T012935_20221007T035455_0001",
        "interface_name": "Satellite-Unavailability",
        "mission": "Sentinel-5P",
        "production_service_name": "Exprivia",
        "production_service_type": "AUXIP",
        "reportName": "S5P_OPER_REP__SUP___20221007T012935_20221007T035455_0001.EOF.xml",
        "start_orbit": "25817",
        "start_time": "UTC=2022-10-07T01:29:35",
        "subsystem": "S/C Manoeuvre",
        "type": "Planned",
        "unavailability_reference": "S5P-UNA-2022/0009",
        "unavailability_type": "Return to Operations",
    }
