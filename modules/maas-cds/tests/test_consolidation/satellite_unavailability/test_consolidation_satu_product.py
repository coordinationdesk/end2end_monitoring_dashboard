from unittest.mock import patch

import maas_cds.model as model
from maas_cds.engines.reports.sat_unavailabilty import (
    SatUnavailabilityConsolidatorEngine,
)


def test_action(s2_sat_unavailability_product):

    engine = SatUnavailabilityConsolidatorEngine()

    satu_product = engine.consolidate_from_SatUnavailabilityProduct(
        s2_sat_unavailability_product, model.CdsSatUnavailability()
    )

    assert satu_product.to_dict() == {
        "comment": "Outage due to GS2_OCP-41 OCP FPA Optical Range Violation, "
        "interrupting a link, 1 link affected. Outage due to GS2_OCP-41 "
        "OCP FPA Optical Range Violation, interrupting a link, 1 link "
        "affected.",
        "end_anx_offset": 5646,
        "end_orbit": "37591",
        "end_time": "2022-09-02T21:25:44.000Z",
        "file_name": "S2A_OPER_REP__SUP___20220902T211217_20220902T212544_0001",
        "key": "620f65f2818f1cfdd4e38e052f94e633",
        "mission": "S2",
        "raw_data_ingestion_time": "2022-09-05T16:10:47.970Z",
        "satellite_unit": "S2A",
        "start_anx_offset": 4839,
        "start_orbit": "37591",
        "start_time": "2022-09-02T21:12:17.000Z",
        "subsystem": "OCP",
        "type": "UNPLANNED",
        "unavailability_duration": 807000000.0,
        "unavailability_reference": "11101",
        "unavailability_type": "Return to Operations",
    }


def test_no_end_update(s2_sat_unavailability_product):

    engine = SatUnavailabilityConsolidatorEngine()

    # Consolidate unavailability with no end-time
    s2_sat_unavailability_product.end_time = ""
    satu_product_no_end = engine.consolidate_from_SatUnavailabilityProduct(
        s2_sat_unavailability_product, model.CdsSatUnavailability()
    )

    assert satu_product_no_end.end_time is None

    assert satu_product_no_end.to_dict() == {
        "comment": "Outage due to GS2_OCP-41 OCP FPA Optical Range Violation, "
        "interrupting a link, 1 link affected. Outage due to GS2_OCP-41 "
        "OCP FPA Optical Range Violation, interrupting a link, 1 link "
        "affected.",
        "end_anx_offset": 5646,
        "end_orbit": "37591",
        "file_name": "S2A_OPER_REP__SUP___20220902T211217_20220902T212544_0001",
        "key": "620f65f2818f1cfdd4e38e052f94e633",
        "mission": "S2",
        "raw_data_ingestion_time": "2022-09-05T16:10:47.970Z",
        "satellite_unit": "S2A",
        "start_anx_offset": 4839,
        "start_orbit": "37591",
        "start_time": "2022-09-02T21:12:17.000Z",
        "subsystem": "OCP",
        "type": "UNPLANNED",
        "unavailability_reference": "11101",
        "unavailability_type": "Return to Operations",
    }

    s2_sat_unavailability_product.end_time = "UTC=2022-09-02T21:25:44"

    # Store no-end-time
    engine._existing = {"620f65f2818f1cfdd4e38e052f94e633": satu_product_no_end}

    # Consolidate unavailability with end-time, must update
    satu_product = engine.consolidate_from_SatUnavailabilityProduct(
        s2_sat_unavailability_product, model.CdsSatUnavailability()
    )

    # Check updated product
    assert satu_product.to_dict() == {
        "comment": "Outage due to GS2_OCP-41 OCP FPA Optical Range Violation, "
        "interrupting a link, 1 link affected. Outage due to GS2_OCP-41 "
        "OCP FPA Optical Range Violation, interrupting a link, 1 link "
        "affected.",
        "end_anx_offset": 5646,
        "end_orbit": "37591",
        "end_time": "2022-09-02T21:25:44.000Z",
        "file_name": "S2A_OPER_REP__SUP___20220902T211217_20220902T212544_0001",
        "key": "620f65f2818f1cfdd4e38e052f94e633",
        "mission": "S2",
        "raw_data_ingestion_time": "2022-09-05T16:10:47.970Z",
        "satellite_unit": "S2A",
        "start_anx_offset": 4839,
        "start_orbit": "37591",
        "start_time": "2022-09-02T21:12:17.000Z",
        "subsystem": "OCP",
        "type": "UNPLANNED",
        "unavailability_duration": 807000000.0,
        "unavailability_reference": "11101",
        "unavailability_type": "Return to Operations",
    }

    engine._existing = {"620f65f2818f1cfdd4e38e052f94e633": satu_product}

    # Check that consolidating same product is skipped
    satu_product = engine.consolidate_from_SatUnavailabilityProduct(
        s2_sat_unavailability_product, model.CdsSatUnavailability()
    )

    assert satu_product is None


def test_no_end_no_update(s2_sat_unavailability_product):

    engine = SatUnavailabilityConsolidatorEngine()

    # Consolidate unavailability with end-time
    satu_product_with_end = engine.consolidate_from_SatUnavailabilityProduct(
        s2_sat_unavailability_product, model.CdsSatUnavailability()
    )

    assert satu_product_with_end.to_dict() == {
        "comment": "Outage due to GS2_OCP-41 OCP FPA Optical Range Violation, "
        "interrupting a link, 1 link affected. Outage due to GS2_OCP-41 "
        "OCP FPA Optical Range Violation, interrupting a link, 1 link "
        "affected.",
        "end_anx_offset": 5646,
        "end_orbit": "37591",
        "end_time": "2022-09-02T21:25:44.000Z",
        "file_name": "S2A_OPER_REP__SUP___20220902T211217_20220902T212544_0001",
        "key": "620f65f2818f1cfdd4e38e052f94e633",
        "mission": "S2",
        "raw_data_ingestion_time": "2022-09-05T16:10:47.970Z",
        "satellite_unit": "S2A",
        "start_anx_offset": 4839,
        "start_orbit": "37591",
        "start_time": "2022-09-02T21:12:17.000Z",
        "subsystem": "OCP",
        "type": "UNPLANNED",
        "unavailability_duration": 807000000.0,
        "unavailability_reference": "11101",
        "unavailability_type": "Return to Operations",
    }

    engine._existing = {"620f65f2818f1cfdd4e38e052f94e633": satu_product_with_end}
    s2_sat_unavailability_product.end_time = ""
    s2_sat_unavailability_product.ingestionTime = "2023-09-05T16:10:47.970Z"

    # Consolidate unavailability with no end-time, must skip update
    satu_product = engine.consolidate_from_SatUnavailabilityProduct(
        s2_sat_unavailability_product, model.CdsSatUnavailability()
    )

    assert satu_product is None


def test_update(s2_sat_unavailability_product):

    engine = SatUnavailabilityConsolidatorEngine()

    satu_product = engine.consolidate_from_SatUnavailabilityProduct(
        s2_sat_unavailability_product, model.CdsSatUnavailability()
    )

    assert satu_product.to_dict() == {
        "comment": "Outage due to GS2_OCP-41 OCP FPA Optical Range Violation, "
        "interrupting a link, 1 link affected. Outage due to GS2_OCP-41 "
        "OCP FPA Optical Range Violation, interrupting a link, 1 link "
        "affected.",
        "end_anx_offset": 5646,
        "end_orbit": "37591",
        "end_time": "2022-09-02T21:25:44.000Z",
        "file_name": "S2A_OPER_REP__SUP___20220902T211217_20220902T212544_0001",
        "key": "620f65f2818f1cfdd4e38e052f94e633",
        "mission": "S2",
        "raw_data_ingestion_time": "2022-09-05T16:10:47.970Z",
        "satellite_unit": "S2A",
        "start_anx_offset": 4839,
        "start_orbit": "37591",
        "start_time": "2022-09-02T21:12:17.000Z",
        "subsystem": "OCP",
        "type": "UNPLANNED",
        "unavailability_duration": 807000000.0,
        "unavailability_reference": "11101",
        "unavailability_type": "Return to Operations",
    }

    engine._existing = {"620f65f2818f1cfdd4e38e052f94e633": satu_product}
    s2_sat_unavailability_product.end_time = "UTC=2022-09-12T19:25:44"

    satu_product = engine.consolidate_from_SatUnavailabilityProduct(
        s2_sat_unavailability_product, model.CdsSatUnavailability()
    )

    assert satu_product is None

    s2_sat_unavailability_product.end_time = "UTC=2022-09-12T19:25:44"
    s2_sat_unavailability_product.ingestionTime = "2023-09-05T16:10:47.970Z"

    satu_product = engine.consolidate_from_SatUnavailabilityProduct(
        s2_sat_unavailability_product, model.CdsSatUnavailability()
    )

    assert satu_product.to_dict() == {
        "comment": "Outage due to GS2_OCP-41 OCP FPA Optical Range Violation, "
        "interrupting a link, 1 link affected. Outage due to GS2_OCP-41 "
        "OCP FPA Optical Range Violation, interrupting a link, 1 link "
        "affected.",
        "end_anx_offset": 5646,
        "end_orbit": "37591",
        "end_time": "2022-09-12T19:25:44.000Z",
        "file_name": "S2A_OPER_REP__SUP___20220902T211217_20220902T212544_0001",
        "key": "620f65f2818f1cfdd4e38e052f94e633",
        "mission": "S2",
        "raw_data_ingestion_time": "2023-09-05T16:10:47.970Z",
        "satellite_unit": "S2A",
        "start_anx_offset": 4839,
        "start_orbit": "37591",
        "start_time": "2022-09-02T21:12:17.000Z",
        "subsystem": "OCP",
        "type": "UNPLANNED",
        "unavailability_duration": 857607000000,
        "unavailability_reference": "11101",
        "unavailability_type": "Return to Operations",
    }
