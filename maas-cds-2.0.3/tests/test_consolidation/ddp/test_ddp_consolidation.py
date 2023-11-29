""" Tests for ddp_consolidation engine"""

import pytest

from maas_cds import model
from maas_cds.engines.reports.ddp_data_available import (
    DdpDataAvailableConsolidatorEngine,
)


@pytest.fixture
def ddp_data_1():
    """raw data from a ingested DSIB file

    Returns:
        (DdpDataAvailable): raw data ddp data available
    """
    data_dict = {
        "reportName": "_sentinel_SVL_SENTINEL2_NOMINAL_S2A_DCS_05_S2A_20220802202126037148_dat_ch_1_DCS_05_S2A_20220802202126037148_ch1_DSIB.xml",
        "session_id": "S2A_20220802202126037148",
        "time_start": "2022-08-02T20:21:26.000Z",
        "time_stop": "2022-08-02T20:30:05.000Z",
        "time_created": "2022-08-02T20:21:47.000Z",
        "time_finished": "2022-08-02T20:32:15.000Z",
        "data_size": 18133697568,
        "interface_name": "DDP_SGS-Svalbard",
        "production_service_type": "DDP",
        "production_service_name": "SGS-Svalbard",
        "ingestionTime": "2022-08-09T14:51:40.100Z",
    }
    raw_document = model.DdpDataAvailable(**data_dict)
    raw_document.meta.id = "S2A_20220802202126037148"
    raw_document.full_clean()
    return raw_document


def test_ddp_data_available_consolidation(ddp_data_1):
    """test consolidation of a ddp data available nominal case

    Args:
        ddp_data_1 (DdpDataAvailable): raw data
    """

    engine = DdpDataAvailableConsolidatorEngine()

    cds_data_aivalable = engine.consolidate_from_DdpDataAvailable(
        ddp_data_1, model.CdsDdpDataAvailable()
    )

    cds_data_aivalable.full_clean()

    assert cds_data_aivalable.to_dict() == {
        "session_id": "S2A_20220802202126037148",
        "time_start": "2022-08-02T20:21:26.000Z",
        "time_stop": "2022-08-02T20:30:05.000Z",
        "time_created": "2022-08-02T20:21:47.000Z",
        "time_finished": "2022-08-02T20:32:15.000Z",
        "data_size": 18133697568,
        "interface_name": "DDP_SGS-Svalbard",
        "production_service_type": "DDP",
        "production_service_name": "SGS-Svalbard",
        "mission": "S2",
        "satellite_unit": "S2A",
        "transfer_time": 649000000,
    }
