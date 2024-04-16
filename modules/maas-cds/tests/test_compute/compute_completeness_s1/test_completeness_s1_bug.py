from unittest.mock import patch

import pytest

from maas_engine.engine.base import EngineSession

import maas_cds.model as model

from maas_cds.engines.compute import ComputeCompletenessEngine

from maas_cds.model.datatake import CdsDatatake


@pytest.fixture
def product_s1_doc_wv_raw_0s():
    product_s1_doc_wv_raw_0s_dict = {
        "absolute_orbit": "53074",
        "datatake_id": "421247",
        "key": "3f7a0d740a03bd1f5b5ee1926eea0b2a",
        "instrument_mode": "WV",
        "mission": "S1",
        "name": "S1A_WV_RAW__0NSV_20240321T032946_20240321T033933_053074_066D7F_E00A.SAFE.zip",
        "polarization": "SV",
        "product_class": "N",
        "product_type": "WV_RAW__0N",
        "product_level": "L0_",
        "satellite_unit": "S1A",
        "sensing_start_date": "2024-03-21T03:29:46.859Z",
        "sensing_end_date": "2024-03-21T03:39:33.837Z",
        "sensing_duration": 586978000,
        "timeliness": "NTC",
        "content_length": 216489,
        "updateTime": "2024-03-21T06:05:49.047Z",
        "prip_id": "683731f4-4afe-46ef-9533-1406e8acfe57",
        "prip_publication_date": "2024-03-21T05:06:18.694Z",
        "prip_service": "PRIP_S1A_Serco",
        "dddas_name": "S1A_WV_RAW__0NSV_20240321T032946_20240321T033933_053074_066D7F_E00A.SAFE",
        "dddas_publication_date": "2024-03-21T05:12:03.865Z",
        "from_prip_dddas_timeliness": 345171000,
    }
    product = model.CdsProductS1(**product_s1_doc_wv_raw_0s_dict)
    product.meta.id = "3f7a0d740a03bd1f5b5ee1926eea0b2a"
    product.full_clean()
    return product


@pytest.fixture
def product_s1_doc_ew_raw_0s():
    product_s1_doc_ew_raw_0s_dict = {
        "absolute_orbit": "53075",
        "datatake_id": "421250",
        "key": "a4e4e9071da68b7192a56dda98d5b5e5",
        "instrument_mode": "EW",
        "mission": "S1",
        "name": "S1A_EW_RAW__0SDH_20240321T043631_20240321T043739_053075_066D82_A0DE.SAFE.zip",
        "polarization": "DH",
        "product_class": "S",
        "product_type": "EW_RAW__0S",
        "product_level": "L0_",
        "satellite_unit": "S1A",
        "sensing_start_date": "2024-03-21T04:36:31.246Z",
        "sensing_end_date": "2024-03-21T04:37:39.446Z",
        "sensing_duration": 68200000,
        "timeliness": "NRT",
        "content_length": 1124037037,
        "updateTime": "2024-03-21T06:05:49.044Z",
        "prip_id": "867d2e09-58da-4f29-ab7b-817ca5354b43",
        "prip_publication_date": "2024-03-21T05:06:38.128Z",
        "prip_service": "PRIP_S1A_Serco",
        "OCN_coverage_percentage": 97.03476969808617,
        "SLC_coverage_percentage": 0,
        "dddas_name": "S1A_EW_RAW__0SDH_20240321T043631_20240321T043739_053075_066D82_A0DE.SAFE",
        "dddas_publication_date": "2024-03-21T05:12:39.344Z",
        "from_prip_dddas_timeliness": 361216000,
    }
    product = model.CdsProductS1(**product_s1_doc_ew_raw_0s_dict)
    product.meta.id = "a4e4e9071da68b7192a56dda98d5b5e5"
    product.full_clean()
    return product


@pytest.fixture
def product_s1_doc_wv_raw_0s_bis():
    product_s1_doc_wv_raw_0s_bis_dict = {
        "absolute_orbit": "53074",
        "datatake_id": "421247",
        "key": "0a2e7f7b8c40ea68802a8cf3650736ea",
        "instrument_mode": "WV",
        "mission": "S1",
        "name": "S1A_WV_RAW__0SSV_20240321T032946_20240321T033933_053074_066D7F_0735.SAFE.zip",
        "polarization": "SV",
        "product_class": "S",
        "product_type": "WV_RAW__0S",
        "product_level": "L0_",
        "satellite_unit": "S1A",
        "sensing_start_date": "2024-03-21T03:29:46.859Z",
        "sensing_end_date": "2024-03-21T03:39:33.837Z",
        "sensing_duration": 586978000,
        "timeliness": "NTC",
        "content_length": 1450109757,
        "updateTime": "2024-03-21T05:51:50.679Z",
        "prip_id": "f085a490-0813-4d32-8049-a0d051e2c2a2",
        "prip_publication_date": "2024-03-21T05:06:41.103Z",
        "prip_service": "PRIP_S1A_Serco",
        "dddas_name": "S1A_WV_RAW__0SSV_20240321T032946_20240321T033933_053074_066D7F_0735.SAFE",
        "dddas_publication_date": "2024-03-21T05:12:37.855Z",
        "from_prip_dddas_timeliness": 356752000,
    }
    product = model.CdsProductS1(**product_s1_doc_wv_raw_0s_bis_dict)
    product.meta.id = "0a2e7f7b8c40ea68802a8cf3650736ea"
    product.full_clean()
    return product


datatake_s1_doc_ew_dict = {
    "name": "S1A_MP_ACQ__L0__20240319T173959_20240331T194102.csv",
    "key": "S1A-421250",
    "datatake_id": "421250",
    "hex_datatake_id": "66D82",
    "satellite_unit": "S1A",
    "mission": "S1",
    "observation_time_start": "2024-03-21T04:36:36.922Z",
    "observation_duration": 127612000,
    "observation_time_stop": "2024-03-21T04:38:44.534Z",
    "l0_sensing_duration": 129937000,
    "l0_sensing_time_start": "2024-03-21T04:36:35.757Z",
    "l0_sensing_time_stop": "2024-03-21T04:38:45.694Z",
    "absolute_orbit": "53075",
    "relative_orbit": "153",
    "polarization": "DH",
    "timeliness": "NRT",
    "instrument_mode": "EW",
    "instrument_swath": "0",
    "application_date": "2024-03-19T17:39:59.000Z",
    "updateTime": "2024-03-21T05:50:01.121Z",
    "EW_RAW__0A_local_value": 129935000,
    "EW_RAW__0A_local_expected": 129802000,
    "EW_RAW__0A_local_value_adjusted": 129802000,
    "EW_RAW__0A_local_percentage": 100,
    "EW_RAW__0A_local_status": "Complete",
    "EW_RAW__0C_local_value": 129935000,
    "EW_RAW__0C_local_expected": 129802000,
    "EW_RAW__0C_local_value_adjusted": 129802000,
    "EW_RAW__0C_local_percentage": 100,
    "EW_RAW__0C_local_status": "Complete",
    "EW_RAW__0N_local_value": 129935000,
    "EW_RAW__0N_local_expected": 129802000,
    "EW_RAW__0N_local_value_adjusted": 129802000,
    "EW_RAW__0N_local_percentage": 100,
    "EW_RAW__0N_local_status": "Complete",
    "EW_RAW__0S_local_value": 129935000,
    "EW_RAW__0S_local_expected": 129802000,
    "EW_RAW__0S_local_value_adjusted": 129802000,
    "EW_RAW__0S_local_percentage": 100,
    "EW_RAW__0S_local_status": "Complete",
    "EW_GRDM_1A_local_value": 130317000,
    "EW_GRDM_1A_local_expected": 130167000,
    "EW_GRDM_1A_local_value_adjusted": 130167000,
    "EW_GRDM_1A_local_percentage": 100,
    "EW_GRDM_1A_local_status": "Complete",
    "EW_GRDM_1S_local_value": 130317000,
    "EW_GRDM_1S_local_expected": 130167000,
    "EW_GRDM_1S_local_value_adjusted": 130167000,
    "EW_GRDM_1S_local_percentage": 100,
    "EW_GRDM_1S_local_status": "Complete",
    "sensing_global_value": 1023010000,
    "sensing_global_expected": 1023010000,
    "sensing_global_value_adjusted": 1023010000,
    "sensing_global_percentage": 100,
    "sensing_global_status": "Complete",
    "EW_OCN__2A_local_value": 130307000,
    "EW_OCN__2A_local_expected": 121734000,
    "EW_OCN__2A_local_value_adjusted": 121734000,
    "EW_OCN__2A_local_percentage": 100,
    "EW_OCN__2A_local_status": "Complete",
    "EW_OCN__2S_local_value": 130307000,
    "EW_OCN__2S_local_expected": 121734000,
    "EW_OCN__2S_local_value_adjusted": 121734000,
    "EW_OCN__2S_local_percentage": 100,
    "EW_OCN__2S_local_status": "Complete",
}

datatake_s1_doc_ew = model.CdsDatatakeS1(**datatake_s1_doc_ew_dict)
datatake_s1_doc_ew.meta.id = "S1A-421250"
datatake_s1_doc_ew.full_clean()

datatake_s1_doc_wv_dict = {
    "name": "S1A_MP_ACQ__L0__20240318T180131_20240330T192832.csv",
    "key": "S1A-420975",
    "datatake_id": "420975",
    "hex_datatake_id": "66C6F",
    "satellite_unit": "S1A",
    "mission": "S1",
    "observation_time_start": "2024-03-19T05:17:06.602Z",
    "observation_duration": 1113170000,
    "observation_time_stop": "2024-03-19T05:35:39.772Z",
    "l0_sensing_duration": 1114269000,
    "l0_sensing_time_start": "2024-03-19T05:17:06.059Z",
    "l0_sensing_time_stop": "2024-03-19T05:35:40.328Z",
    "absolute_orbit": "53046",
    "relative_orbit": "124",
    "polarization": "SV",
    "timeliness": "NTC",
    "instrument_mode": "WV",
    "instrument_swath": "0",
    "application_date": "2024-03-18T18:01:31.000Z",
    "updateTime": "2024-03-19T08:37:18.675Z",
    "WV_RAW__0A_local_value": 1114269000,
    "WV_RAW__0A_local_expected": 1113510000,
    "WV_RAW__0A_local_value_adjusted": 1113510000,
    "WV_RAW__0A_local_percentage": 100,
    "WV_RAW__0A_local_status": "Complete",
    "WV_RAW__0C_local_value": 1114269000,
    "WV_RAW__0C_local_expected": 1113510000,
    "WV_RAW__0C_local_value_adjusted": 1113510000,
    "WV_RAW__0C_local_percentage": 100,
    "WV_RAW__0C_local_status": "Complete",
    "WV_RAW__0N_local_value": 1114269000,
    "WV_RAW__0N_local_expected": 1113510000,
    "WV_RAW__0N_local_value_adjusted": 1113510000,
    "WV_RAW__0N_local_percentage": 100,
    "WV_RAW__0N_local_status": "Complete",
    "WV_RAW__0S_local_value": 1114269000,
    "WV_RAW__0S_local_expected": 1113510000,
    "WV_RAW__0S_local_value_adjusted": 1113510000,
    "WV_RAW__0S_local_percentage": 100,
    "WV_RAW__0S_local_status": "Complete",
    "WV_SLC__1A_local_value": 1101442000,
    "WV_SLC__1A_local_expected": 1100769000,
    "WV_SLC__1A_local_value_adjusted": 1100769000,
    "WV_SLC__1A_local_percentage": 100,
    "WV_SLC__1A_local_status": "Complete",
    "WV_SLC__1S_local_value": 1101442000,
    "WV_SLC__1S_local_expected": 1100769000,
    "WV_SLC__1S_local_value_adjusted": 1100769000,
    "WV_SLC__1S_local_percentage": 100,
    "WV_SLC__1S_local_status": "Complete",
    "WV_OCN__2A_local_value": 1102186000,
    "WV_OCN__2A_local_expected": 1101426000,
    "WV_OCN__2A_local_value_adjusted": 1101426000,
    "WV_OCN__2A_local_percentage": 100,
    "WV_OCN__2A_local_status": "Complete",
    "WV_OCN__2S_local_value": 1102186000,
    "WV_OCN__2S_local_expected": 1101426000,
    "WV_OCN__2S_local_value_adjusted": 1101426000,
    "WV_OCN__2S_local_percentage": 100,
    "WV_OCN__2S_local_status": "Complete",
    "sensing_global_value": 8858430000,
    "sensing_global_expected": 8858430000,
    "sensing_global_value_adjusted": 8858430000,
    "sensing_global_percentage": 100,
    "sensing_global_status": "Complete",
    "WV_ETA__AX_local_value": 0,
    "WV_ETA__AX_local_expected": 1,
    "WV_ETA__AX_local_value_adjusted": 0,
    "WV_ETA__AX_local_percentage": 0,
    "WV_ETA__AX_local_status": "Missing",
}

datatake_s1_doc_wv = model.CdsDatatakeS1(**datatake_s1_doc_wv_dict)
datatake_s1_doc_wv.meta.id = "S1A-420975"
datatake_s1_doc_wv.full_clean()


@patch(
    "maas_cds.model.CdsDatatakeS1.get_by_id",
    side_effect=[datatake_s1_doc_wv, datatake_s1_doc_ew],
)
def test_completeness(
    mock_get_by_id,
    product_s1_doc_wv_raw_0s,
    product_s1_doc_ew_raw_0s,
    product_s1_doc_wv_raw_0s_bis,
):
    engine = ComputeCompletenessEngine()

    engine.input_documents = [
        product_s1_doc_wv_raw_0s,
        product_s1_doc_ew_raw_0s,
        product_s1_doc_wv_raw_0s_bis,
    ]

    list(engine.load_compute_keys_from_input_documents())

    assert engine.tuples_to_compute == [
        ("S1A-421247", "WV_RAW__0N"),
        ("S1A-421250", "EW_RAW__0S"),
        ("S1A-421250", "EW_SLC__1A"),
        ("S1A-421250", "EW_SLC__1S"),
        ("S1A-421250", "EW_OCN__2A"),
        ("S1A-421250", "EW_OCN__2S"),
        ("S1A-421247", "WV_RAW__0S"),
    ]
