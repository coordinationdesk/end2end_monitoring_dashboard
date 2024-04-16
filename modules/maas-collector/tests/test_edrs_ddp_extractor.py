"""EISPExtractor tests"""
import datetime
from dateutil import tz
import os
from maas_collector.rawdata.extractor import EdrsDdpExtractor


def test_edrs_ddp_extractor():
    xext = EdrsDdpExtractor(
        attr_map={
            "session_id": "session_id",
            "time_start": "time_start",
            "time_stop": "time_stop",
            "time_created": "time_created",
            "time_finished": "time_finished",
            "data_size": "data_size",
            "interface_name": {"python": "lambda root: 'DDP_EDRS_EDIP'"},
            "production_service_type": {"python": "lambda root: 'DDP'"},
            "production_service_name": {"python": "lambda root: 'EDRS_EDIP'"},
        }
    )
    DSIB_FILE = os.path.join(
        os.path.dirname(__file__),
        "data",
        "DCS_02_L20191003131732787001008_ch1_DSIB.xml",
    )

    extract_dict = next(
        xext.extract(DSIB_FILE, report_folder="/NOMINAL/S1A", modify_rawdata=False)
    )

    assert extract_dict["session_id"] == "S1A_L20191003131732787001008"

    extract_dict = next(
        xext.extract(DSIB_FILE, report_folder="/NOMINAL/DUCK", modify_rawdata=False)
    )

    assert extract_dict["session_id"] == "L20191003131732787001008"
