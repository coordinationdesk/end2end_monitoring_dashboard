from maas_cds.engines.reports.sat_unavailabilty import (
    SatUnavailabilityConsolidatorEngine,
)

import maas_cds.model as model


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
        "end_time": "2022-09-02T19:25:44.000Z",
        "file_name": "S2A_OPER_REP__SUP___20220902T211217_20220902T212544_0001",
        "key": "635e6d01d2239e3f885a036c48944e9b",
        "mission": "S2",
        "satellite_unit": "S2A",
        "start_anx_offset": 4839,
        "start_orbit": "37591",
        "start_time": "2022-09-02T19:12:17.000Z",
        "subsystem": "OCP",
        "type": "UNPLANNED",
        "unavailability_duration": 807000000.0,
        "unavailability_reference": "11101",
        "unavailability_type": "Return to Operations",
    }
