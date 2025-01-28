"""Tests for MP consolidation into datatake"""

import datetime
from unittest.mock import patch

import maas_cds.model as model
from maas_cds.model.datatake import CdsDatatake


from maas_cds.model.datatake_s1 import (
    CdsDatatakeS1,
)
from maas_cds.model.product_s1 import CdsProductS1


def test_fill_global_completeness_1():
    """fill_global_completeness test"""

    datatake_doc = CdsDatatakeS1()

    datatake_doc.global_sensing_duration = 0
    datatake_doc.sensing_global_percentage = 0
    datatake_doc.sensing_global_status = model.CompletenessStatus.MISSING.value

    datatake_doc.instrument_mode = "RFC"

    setattr(
        datatake_doc,
        "RF_RAW__0S_local_value",
        1400000,
    )

    setattr(
        datatake_doc,
        "RF_RAW__0S_local_value_adjusted",
        1400000,
    )

    datatake_doc.compute_global_completeness()

    assert datatake_doc.sensing_global_expected == 2800000

    assert datatake_doc.sensing_global_percentage == 50

    assert datatake_doc.sensing_global_status == model.CompletenessStatus.PARTIAL.value


@patch("maas_cds.model.datatake_s1.CdsDatatakeS1.get_datatake_product_type_brother")
@patch("maas_cds.model.datatake_s1.compute_total_sensing_product")
def test_compute_local_sensing_duration(
    mock_compute_total_sensing_product, mock_get_datatake_product_type_brother
):
    """compute_local_sensing_duration test"""

    mock_get_datatake_product_type_brother.return_value = []
    mock_compute_total_sensing_product.return_value = 10

    datatake_doc = CdsDatatakeS1()

    value = datatake_doc.compute_local_value("PRODUCT_TYPE")

    assert value == 10


@patch("maas_cds.model.datatake_s1.CdsDatatakeS1.get_datatake_product_type_brother")
@patch("maas_cds.model.datatake_s1.compute_total_sensing_product")
@patch("maas_cds.model.datatake_s1.CdsDatatakeS1.evaluate_local_expected")
def test_compute_missing_periods(
    mock_evaluate_local_expected,
    mock_compute_total_sensing_product,
    mock_get_datatake_product_type_brother,
):
    """compute_local_sensing_duration test"""

    mock_get_datatake_product_type_brother.return_value = []
    mock_compute_total_sensing_product.return_value = 10
    mock_evaluate_local_expected.return_value = 0

    datatake_doc = CdsDatatakeS1(
        **{
            "name": "S1A_MP_ACQ__L0__20220406T160000_20220418T180000.csv",
            "key": "S1A-333628",
            "datatake_id": "333628",
            "satellite_unit": "S1A",
            "mission": "S1",
            "observation_time_start": datetime.datetime(
                2022, 4, 7, 12, 11, 39, 958000, tzinfo=datetime.timezone.utc
            ),
            "observation_duration": 30005000,
            "observation_time_stop": datetime.datetime(
                2022, 4, 7, 12, 12, 9, 963000, tzinfo=datetime.timezone.utc
            ),
            "instrument_mode": "IW",
            "timeliness": "NTC",
        }
    )

    CdsDatatake.MISSING_PERIODS_MAXIMAL_OFFSET = {
        "S1": {
            "global": 0,
            "local": {
                "default": 6000000,
            },
        },
    }

    related_documents = []
    datatake_doc.compute_local_value("IW_RAW__0S", related_documents)
    datatake_doc.compute_all_local_completeness()

    # No products, so we have the whole datatake missing
    assert related_documents == []
    assert [p.to_dict() for p in datatake_doc.missing_periods] == [
        {
            "name": "Missing Product",
            "product_type": "IW_RAW__0S",
            "sensing_start_date": "2022-04-07T12:11:39.958Z",
            "sensing_end_date": "2022-04-07T12:12:09.963Z",
            "duration": 30005000,
        }
    ]


duplicated_s1_products_dict = [
    {
        "DD_CDSE_deletion_cause": "Duplicated product",
        "DD_CDSE_deletion_date": "2023-12-04T11:22:57.243000+00:00",
        "DD_CDSE_deletion_issue": "SOA-123",
        "DD_CDSE_is_deleted": True,
        "DD_DAS_deletion_cause": "Duplicated product",
        "DD_DAS_deletion_date": "2023-12-04T11:22:57.243000+00:00",
        "DD_DAS_deletion_issue": "OMCS-2103",
        "DD_DAS_is_deleted": True,
        "DD_DHUS_deletion_cause": "Duplicated product",
        "DD_DHUS_deletion_date": "2023-12-04T11:22:57.243000+00:00",
        "DD_DHUS_deletion_issue": "SOA-123",
        "DD_DHUS_is_deleted": True,
        "_id": "9d745769cf5430cf05211303c8bfae0b",
        "_index": "cds-product-2023-06",
        "absolute_orbit": "48804",
        "content_length": 243761367,
        "datatake_id": "384640",
        "dddas_name": "S1A_EW_GRDM_1SDH_20230602T074820_20230602T074920_048804_05DE80_FFA8.SAFE",
        "dddas_publication_date": "2023-06-02T10:18:12.970Z",
        "ddip_name": "S1A_EW_GRDM_1SDH_20230602T074820_20230602T074920_048804_05DE80_FFA8",
        "ddip_publication_date": "2023-06-02T10:09:02.405Z",
        "from_prip_dddas_timeliness": 786236000,
        "from_prip_ddip_timeliness": 235671000,
        "hex_datatake_id": "5DE80",
        "instrument_mode": "EW",
        "key": "9d745769cf5430cf05211303c8bfae0b",
        "mission": "S1",
        "name": "S1A_EW_GRDM_1SDH_20230602T074820_20230602T074920_048804_05DE80_FFA8.SAFE.zip",
        "nb_dd_deleted": 3,
        "polarization": "DH",
        "prip_id": "77adc6a9-02bd-4187-ab98-343b2d720e0a",
        "prip_publication_date": "2023-06-02T10:05:06.734Z",
        "prip_service": "PRIP_S1A_Serco",
        "product_class": "S",
        "product_level": "L1_",
        "product_type": "EW_GRDM_1S",
        "satellite_unit": "S1A",
        "sensing_duration": 59998000,
        "sensing_end_date": datetime.datetime(
            2023, 6, 2, 7, 49, 20, 980000, tzinfo=datetime.timezone.utc
        ),
        "sensing_start_date": datetime.datetime(
            2023, 6, 2, 7, 48, 20, 982000, tzinfo=datetime.timezone.utc
        ),
        "timeliness": "NRT-PT",
        "updateTime": "2024-04-25T16:26:44.703Z",
    },
    {
        "DD_CDSE_deletion_cause": "Duplicated product",
        "DD_CDSE_deletion_date": "2023-12-04T11:22:57.243000+00:00",
        "DD_CDSE_deletion_issue": "SOA-123",
        "DD_CDSE_is_deleted": True,
        "DD_DAS_deletion_cause": "Duplicated product",
        "DD_DAS_deletion_date": "2023-12-04T11:22:57.243000+00:00",
        "DD_DAS_deletion_issue": "OMCS-2103",
        "DD_DAS_is_deleted": True,
        "DD_DHUS_deletion_cause": "Duplicated product",
        "DD_DHUS_deletion_date": "2023-12-04T11:22:57.243000+00:00",
        "DD_DHUS_deletion_issue": "SOA-123",
        "DD_DHUS_is_deleted": True,
        "_id": "5f9194b3b085f88df2f436683b70374f",
        "_index": "cds-product-2023-06",
        "absolute_orbit": "48804",
        "content_length": 244153172,
        "datatake_id": "384640",
        "dddas_name": "S1A_EW_GRDM_1SDH_20230602T074720_20230602T074820_048804_05DE80_A00E.SAFE",
        "dddas_publication_date": "2023-06-02T10:11:53.992Z",
        "ddip_name": "S1A_EW_GRDM_1SDH_20230602T074720_20230602T074820_048804_05DE80_A00E",
        "ddip_publication_date": "2023-06-02T10:09:04.124Z",
        "from_prip_dddas_timeliness": 347463000,
        "from_prip_ddip_timeliness": 177595000,
        "hex_datatake_id": "5DE80",
        "instrument_mode": "EW",
        "key": "5f9194b3b085f88df2f436683b70374f",
        "mission": "S1",
        "name": "S1A_EW_GRDM_1SDH_20230602T074720_20230602T074820_048804_05DE80_A00E.SAFE.zip",
        "nb_dd_deleted": 3,
        "polarization": "DH",
        "prip_id": "d3372497-ef9f-4c57-a358-f4b667cc8126",
        "prip_publication_date": "2023-06-02T10:06:06.529Z",
        "prip_service": "PRIP_S1A_Serco",
        "product_class": "S",
        "product_level": "L1_",
        "product_type": "EW_GRDM_1S",
        "satellite_unit": "S1A",
        "sensing_duration": 59992000,
        "sensing_end_date": datetime.datetime(
            2023, 6, 2, 7, 48, 20, 976000, tzinfo=datetime.timezone.utc
        ),
        "sensing_start_date": datetime.datetime(
            2023, 6, 2, 7, 47, 20, 984000, tzinfo=datetime.timezone.utc
        ),
        "timeliness": "NRT-PT",
        "updateTime": "2024-04-25T16:26:44.680Z",
    },
    {
        "DD_CDSE_deletion_cause": "Duplicated product",
        "DD_CDSE_deletion_date": "2023-12-04T11:22:57.243000+00:00",
        "DD_CDSE_deletion_issue": "SOA-123",
        "DD_CDSE_is_deleted": True,
        "DD_DAS_deletion_cause": "Duplicated product",
        "DD_DAS_deletion_date": "2023-12-04T11:22:57.243000+00:00",
        "DD_DAS_deletion_issue": "OMCS-2103",
        "DD_DAS_is_deleted": True,
        "DD_DHUS_deletion_cause": "Duplicated product",
        "DD_DHUS_deletion_date": "2023-12-04T11:22:57.243000+00:00",
        "DD_DHUS_deletion_issue": "SOA-123",
        "DD_DHUS_is_deleted": True,
        "_id": "3e830c026f9464216ec8d28c29a8eff2",
        "_index": "cds-product-2023-06",
        "absolute_orbit": "48804",
        "content_length": 197361173,
        "datatake_id": "384640",
        "dddas_name": "S1A_EW_GRDM_1SDH_20230602T075020_20230602T075110_048804_05DE80_1B3B.SAFE",
        "dddas_publication_date": "2023-06-02T10:10:00.538Z",
        "ddip_name": "S1A_EW_GRDM_1SDH_20230602T075020_20230602T075110_048804_05DE80_1B3B",
        "ddip_publication_date": "2023-06-02T10:07:02.071Z",
        "from_prip_dddas_timeliness": 383375000,
        "from_prip_ddip_timeliness": 204908000,
        "hex_datatake_id": "5DE80",
        "instrument_mode": "EW",
        "key": "3e830c026f9464216ec8d28c29a8eff2",
        "mission": "S1",
        "name": "S1A_EW_GRDM_1SDH_20230602T075020_20230602T075110_048804_05DE80_1B3B.SAFE.zip",
        "nb_dd_deleted": 3,
        "polarization": "DH",
        "prip_id": "bd90d6a0-0c3e-41fb-8e7a-8e52f6d7e5d5",
        "prip_publication_date": "2023-06-02T10:03:37.163Z",
        "prip_service": "PRIP_S1A_Serco",
        "product_class": "S",
        "product_level": "L1_",
        "product_type": "EW_GRDM_1S",
        "satellite_unit": "S1A",
        "sensing_duration": 49401000,
        "sensing_end_date": datetime.datetime(
            2023, 6, 2, 7, 51, 10, 384000, tzinfo=datetime.timezone.utc
        ),
        "sensing_start_date": datetime.datetime(
            2023, 6, 2, 7, 50, 20, 983000, tzinfo=datetime.timezone.utc
        ),
        "timeliness": "NRT-PT",
        "updateTime": "2024-04-25T16:26:44.667Z",
    },
    {
        "DD_CDSE_deletion_cause": "Duplicated product",
        "DD_CDSE_deletion_date": "2023-12-04T11:22:57.243000+00:00",
        "DD_CDSE_deletion_issue": "SOA-123",
        "DD_CDSE_is_deleted": True,
        "DD_DAS_deletion_cause": "Duplicated product",
        "DD_DAS_deletion_date": "2023-12-04T11:22:57.243000+00:00",
        "DD_DAS_deletion_issue": "OMCS-2103",
        "DD_DAS_is_deleted": True,
        "DD_DHUS_deletion_cause": "Duplicated product",
        "DD_DHUS_deletion_date": "2023-12-04T11:22:57.243000+00:00",
        "DD_DHUS_deletion_issue": "SOA-123",
        "DD_DHUS_is_deleted": True,
        "_id": "14b741b35b7705c9b82cd3f8758cfde2",
        "_index": "cds-product-2023-06",
        "absolute_orbit": "48804",
        "content_length": 258872152,
        "datatake_id": "384640",
        "dddas_name": "S1A_EW_GRDM_1SDH_20230602T074615_20230602T074720_048804_05DE80_457E.SAFE",
        "dddas_publication_date": "2023-06-02T10:12:15.623Z",
        "ddip_name": "S1A_EW_GRDM_1SDH_20230602T074615_20230602T074720_048804_05DE80_457E",
        "ddip_publication_date": "2023-06-02T10:09:03.184Z",
        "from_prip_dddas_timeliness": 368363000,
        "from_prip_ddip_timeliness": 175924000,
        "hex_datatake_id": "5DE80",
        "instrument_mode": "EW",
        "key": "14b741b35b7705c9b82cd3f8758cfde2",
        "mission": "S1",
        "name": "S1A_EW_GRDM_1SDH_20230602T074615_20230602T074720_048804_05DE80_457E.SAFE.zip",
        "nb_dd_deleted": 3,
        "polarization": "DH",
        "prip_id": "4180769d-3457-4095-b279-9d1a5a73101d",
        "prip_publication_date": "2023-06-02T10:06:07.260Z",
        "prip_service": "PRIP_S1A_Serco",
        "product_class": "S",
        "product_level": "L1_",
        "product_type": "EW_GRDM_1S",
        "satellite_unit": "S1A",
        "sensing_duration": 65084000,
        "sensing_end_date": datetime.datetime(
            2023, 6, 2, 7, 47, 20, 978000, tzinfo=datetime.timezone.utc
        ),
        "sensing_start_date": datetime.datetime(
            2023, 6, 2, 7, 46, 15, 894000, tzinfo=datetime.timezone.utc
        ),
        "timeliness": "NRT-PT",
        "updateTime": "2024-04-25T16:26:44.665Z",
    },
    {
        "DD_CDSE_deletion_cause": "Duplicated product",
        "DD_CDSE_deletion_date": "2023-12-04T11:22:57.243000+00:00",
        "DD_CDSE_deletion_issue": "SOA-123",
        "DD_CDSE_is_deleted": True,
        "DD_DAS_deletion_cause": "Duplicated product",
        "DD_DAS_deletion_date": "2023-12-04T11:22:57.243000+00:00",
        "DD_DAS_deletion_issue": "OMCS-2103",
        "DD_DAS_is_deleted": True,
        "DD_DHUS_deletion_cause": "Duplicated product",
        "DD_DHUS_deletion_date": "2023-12-04T11:22:57.243000+00:00",
        "DD_DHUS_deletion_issue": "SOA-123",
        "DD_DHUS_is_deleted": True,
        "_id": "1870c9628704132ea96282d4e6564ab1",
        "_index": "cds-product-2023-06",
        "absolute_orbit": "48804",
        "content_length": 240028727,
        "datatake_id": "384640",
        "dddas_name": "S1A_EW_GRDM_1SDH_20230602T074920_20230602T075020_048804_05DE80_E942.SAFE",
        "dddas_publication_date": "2023-06-02T10:18:32.230Z",
        "ddip_name": "S1A_EW_GRDM_1SDH_20230602T074920_20230602T075020_048804_05DE80_E942",
        "ddip_publication_date": "2023-06-02T10:09:01.556Z",
        "from_prip_dddas_timeliness": 805339000,
        "from_prip_ddip_timeliness": 234665000,
        "hex_datatake_id": "5DE80",
        "instrument_mode": "EW",
        "key": "1870c9628704132ea96282d4e6564ab1",
        "mission": "S1",
        "name": "S1A_EW_GRDM_1SDH_20230602T074920_20230602T075020_048804_05DE80_E942.SAFE.zip",
        "nb_dd_deleted": 3,
        "polarization": "DH",
        "prip_id": "72f9d9a6-0703-492a-9b72-f5b178f9d863",
        "prip_publication_date": "2023-06-02T10:05:06.891Z",
        "prip_service": "PRIP_S1A_Serco",
        "product_class": "S",
        "product_level": "L1_",
        "product_type": "EW_GRDM_1S",
        "satellite_unit": "S1A",
        "sensing_duration": 59991000,
        "sensing_end_date": datetime.datetime(
            2023, 6, 2, 7, 50, 20, 977000, tzinfo=datetime.timezone.utc
        ),
        "sensing_start_date": datetime.datetime(
            2023, 6, 2, 7, 49, 20, 986000, tzinfo=datetime.timezone.utc
        ),
        "timeliness": "NRT-PT",
        "updateTime": "2024-04-25T16:26:44.665Z",
    },
    {
        "_id": "c8b01268c217582fb36ceb7dbdab5765",
        "_index": "cds-product-2023-06",
        "absolute_orbit": "48804",
        "content_length": 242164718,
        "datatake_id": "384640",
        "dddas_name": "S1A_EW_GRDM_1SDH_20230602T074838_20230602T074938_048804_05DE80_82AF.SAFE",
        "dddas_publication_date": "2023-06-02T08:10:51.746Z",
        "ddip_name": "S1A_EW_GRDM_1SDH_20230602T074838_20230602T074938_048804_05DE80_82AF",
        "ddip_publication_date": "2023-06-02T08:07:07.536Z",
        "from_prip_dddas_timeliness": 375557000,
        "from_prip_ddip_timeliness": 151347000,
        "hex_datatake_id": "5DE80",
        "instrument_mode": "EW",
        "key": "c8b01268c217582fb36ceb7dbdab5765",
        "mission": "S1",
        "name": "S1A_EW_GRDM_1SDH_20230602T074838_20230602T074938_048804_05DE80_82AF.SAFE.zip",
        "polarization": "DH",
        "prip_id": "c52c2f40-6833-4ac5-80f6-eb3109490e45",
        "prip_publication_date": "2023-06-02T08:04:36.189Z",
        "prip_service": "PRIP_S1A_Serco",
        "product_class": "S",
        "product_level": "L1_",
        "product_type": "EW_GRDM_1S",
        "satellite_unit": "S1A",
        "sensing_duration": 59997000,
        "sensing_end_date": datetime.datetime(
            2023, 6, 2, 7, 49, 38, 915000, tzinfo=datetime.timezone.utc
        ),
        "sensing_start_date": datetime.datetime(
            2023, 6, 2, 7, 48, 38, 918000, tzinfo=datetime.timezone.utc
        ),
        "timeliness": "NRT-PT",
        "updateTime": "2023-06-28T13:34:27.625Z",
    },
    {
        "_id": "20f35c51581127eddc98866f6187bfdf",
        "_index": "cds-product-2023-06",
        "absolute_orbit": "48804",
        "content_length": 242856599,
        "datatake_id": "384640",
        "dddas_name": "S1A_EW_GRDM_1SDH_20230602T074638_20230602T074738_048804_05DE80_C32D.SAFE",
        "dddas_publication_date": "2023-06-02T08:09:46.286Z",
        "ddip_name": "S1A_EW_GRDM_1SDH_20230602T074638_20230602T074738_048804_05DE80_C32D",
        "ddip_publication_date": "2023-06-02T08:07:03.551Z",
        "from_prip_dddas_timeliness": 340528000,
        "from_prip_ddip_timeliness": 177793000,
        "hex_datatake_id": "5DE80",
        "instrument_mode": "EW",
        "key": "20f35c51581127eddc98866f6187bfdf",
        "mission": "S1",
        "name": "S1A_EW_GRDM_1SDH_20230602T074638_20230602T074738_048804_05DE80_C32D.SAFE.zip",
        "polarization": "DH",
        "prip_id": "4070afe4-248e-4aea-ad6b-8f160f731ecc",
        "prip_publication_date": "2023-06-02T08:04:05.758Z",
        "prip_service": "PRIP_S1A_Serco",
        "product_class": "S",
        "product_level": "L1_",
        "product_type": "EW_GRDM_1S",
        "satellite_unit": "S1A",
        "sensing_duration": 59997000,
        "sensing_end_date": datetime.datetime(
            2023, 6, 2, 7, 47, 38, 915000, tzinfo=datetime.timezone.utc
        ),
        "sensing_start_date": datetime.datetime(
            2023, 6, 2, 7, 46, 38, 918000, tzinfo=datetime.timezone.utc
        ),
        "timeliness": "NRT-PT",
        "updateTime": "2023-06-28T14:21:37.723Z",
    },
    {
        "_id": "0dfa5719da0c0018c7283ebc0c950b34",
        "_index": "cds-product-2023-06",
        "absolute_orbit": "48804",
        "content_length": 243949357,
        "datatake_id": "384640",
        "dddas_name": "S1A_EW_GRDM_1SDH_20230602T074738_20230602T074838_048804_05DE80_BE99.SAFE",
        "dddas_publication_date": "2023-06-02T08:12:17.457Z",
        "ddip_name": "S1A_EW_GRDM_1SDH_20230602T074738_20230602T074838_048804_05DE80_BE99",
        "ddip_publication_date": "2023-06-02T08:07:06.414Z",
        "from_prip_dddas_timeliness": 460032000,
        "from_prip_ddip_timeliness": 148989000,
        "hex_datatake_id": "5DE80",
        "instrument_mode": "EW",
        "key": "0dfa5719da0c0018c7283ebc0c950b34",
        "mission": "S1",
        "name": "S1A_EW_GRDM_1SDH_20230602T074738_20230602T074838_048804_05DE80_BE99.SAFE.zip",
        "polarization": "DH",
        "prip_id": "11c6a28f-2fdf-4c9d-aa03-743ae48104bf",
        "prip_publication_date": "2023-06-02T08:04:37.425Z",
        "prip_service": "PRIP_S1A_Serco",
        "product_class": "S",
        "product_level": "L1_",
        "product_type": "EW_GRDM_1S",
        "satellite_unit": "S1A",
        "sensing_duration": 59991000,
        "sensing_end_date": datetime.datetime(
            2023, 6, 2, 7, 48, 38, 912000, tzinfo=datetime.timezone.utc
        ),
        "sensing_start_date": datetime.datetime(
            2023, 6, 2, 7, 47, 38, 921000, tzinfo=datetime.timezone.utc
        ),
        "timeliness": "NRT-PT",
        "updateTime": "2023-06-28T14:21:37.726Z",
    },
    {
        "_id": "ef7e242cb9fbb42d788e1ef83c1a409f",
        "_index": "cds-product-2023-06",
        "absolute_orbit": "48804",
        "content_length": 122551560,
        "datatake_id": "384640",
        "dddas_name": "S1A_EW_GRDM_1SDH_20230602T075038_20230602T075111_048804_05DE80_2C4F.SAFE",
        "dddas_publication_date": "2023-06-02T08:06:36.204Z",
        "ddip_name": "S1A_EW_GRDM_1SDH_20230602T075038_20230602T075111_048804_05DE80_2C4F",
        "ddip_publication_date": "2023-06-02T08:03:00.772Z",
        "from_prip_dddas_timeliness": 361865000,
        "from_prip_ddip_timeliness": 146433000,
        "hex_datatake_id": "5DE80",
        "instrument_mode": "EW",
        "key": "ef7e242cb9fbb42d788e1ef83c1a409f",
        "mission": "S1",
        "name": "S1A_EW_GRDM_1SDH_20230602T075038_20230602T075111_048804_05DE80_2C4F.SAFE.zip",
        "polarization": "DH",
        "prip_id": "cd4ee350-a8b6-409b-bc06-39e4f9493ea3",
        "prip_publication_date": "2023-06-02T08:00:34.339Z",
        "prip_service": "PRIP_S1A_Serco",
        "product_class": "S",
        "product_level": "L1_",
        "product_type": "EW_GRDM_1S",
        "satellite_unit": "S1A",
        "sensing_duration": 32628000,
        "sensing_end_date": datetime.datetime(
            2023, 6, 2, 7, 51, 11, 546000, tzinfo=datetime.timezone.utc
        ),
        "sensing_start_date": datetime.datetime(
            2023, 6, 2, 7, 50, 38, 918000, tzinfo=datetime.timezone.utc
        ),
        "timeliness": "NRT-PT",
        "updateTime": "2023-06-28T14:21:37.722Z",
    },
    {
        "_id": "5adcf768037f8171d41250f9d90c2aef",
        "_index": "cds-product-2023-06",
        "absolute_orbit": "48804",
        "content_length": 247117731,
        "datatake_id": "384640",
        "dddas_name": "S1A_EW_GRDM_1SDH_20230602T074938_20230602T075038_048804_05DE80_51B2.SAFE",
        "dddas_publication_date": "2023-06-02T08:12:49.416Z",
        "ddip_name": "S1A_EW_GRDM_1SDH_20230602T074938_20230602T075038_048804_05DE80_51B2",
        "ddip_publication_date": "2023-06-02T08:07:02.802Z",
        "from_prip_dddas_timeliness": 461913000,
        "from_prip_ddip_timeliness": 115299000,
        "hex_datatake_id": "5DE80",
        "instrument_mode": "EW",
        "key": "5adcf768037f8171d41250f9d90c2aef",
        "mission": "S1",
        "name": "S1A_EW_GRDM_1SDH_20230602T074938_20230602T075038_048804_05DE80_51B2.SAFE.zip",
        "polarization": "DH",
        "prip_id": "05de6e12-2b9d-40b7-833f-15cecfd7f005",
        "prip_publication_date": "2023-06-02T08:05:07.503Z",
        "prip_service": "PRIP_S1A_Serco",
        "product_class": "S",
        "product_level": "L1_",
        "product_type": "EW_GRDM_1S",
        "satellite_unit": "S1A",
        "sensing_duration": 59991000,
        "sensing_end_date": datetime.datetime(
            2023, 6, 2, 7, 50, 38, 912000, tzinfo=datetime.timezone.utc
        ),
        "sensing_start_date": datetime.datetime(
            2023, 6, 2, 7, 49, 38, 921000, tzinfo=datetime.timezone.utc
        ),
        "timeliness": "NRT-PT",
        "updateTime": "2023-06-28T14:21:37.727Z",
    },
    {
        "_id": "641dc7e3789bb6e540d7df7ef8b1f646",
        "_index": "cds-product-2023-06",
        "absolute_orbit": "48804",
        "content_length": 262087887,
        "datatake_id": "384640",
        "dddas_name": "S1A_EW_GRDM_1SDH_20230602T074534_20230602T074638_048804_05DE80_C804.SAFE",
        "dddas_publication_date": "2023-06-02T08:11:45.739Z",
        "ddip_name": "S1A_EW_GRDM_1SDH_20230602T074534_20230602T074638_048804_05DE80_C804",
        "ddip_publication_date": "2023-06-02T08:07:05.402Z",
        "from_prip_dddas_timeliness": 428890000,
        "from_prip_ddip_timeliness": 148553000,
        "hex_datatake_id": "5DE80",
        "instrument_mode": "EW",
        "key": "641dc7e3789bb6e540d7df7ef8b1f646",
        "mission": "S1",
        "name": "S1A_EW_GRDM_1SDH_20230602T074534_20230602T074638_048804_05DE80_C804.SAFE.zip",
        "polarization": "DH",
        "prip_id": "d87efc0b-855f-4cfa-9501-2fed657e9cb0",
        "prip_publication_date": "2023-06-02T08:04:36.849Z",
        "prip_service": "PRIP_S1A_Serco",
        "product_class": "S",
        "product_level": "L1_",
        "product_type": "EW_GRDM_1S",
        "satellite_unit": "S1A",
        "sensing_duration": 64302000,
        "sensing_end_date": datetime.datetime(
            2023, 6, 2, 7, 46, 38, 912000, tzinfo=datetime.timezone.utc
        ),
        "sensing_start_date": datetime.datetime(
            2023, 6, 2, 7, 45, 34, 610000, tzinfo=datetime.timezone.utc
        ),
        "timeliness": "NRT-PT",
        "updateTime": "2023-06-28T14:21:37.726Z",
    },
]


@patch("maas_cds.model.datatake_s1.CdsDatatakeS1.find_brother_products_scan")
@patch("maas_cds.model.datatake_s1.CdsDatatakeS1.evaluate_local_expected")
def test_compute_duplicated_periods(
    mock_evaluate_local_expected,
    mock_get_datatake_product_type_brother,
):
    """compute_local_sensing_duration test"""

    duplicated_s1_products_clean = []
    for product_dict in duplicated_s1_products_dict:
        product = CdsProductS1(**product_dict)
        product.meta.id = product_dict["_id"]
        product.meta.index = product_dict["_index"]

        product.full_clean()

        duplicated_s1_products_clean.append(product)

    mock_get_datatake_product_type_brother.return_value = duplicated_s1_products_clean

    mock_evaluate_local_expected.return_value = 336776000.0

    datatake_doc = CdsDatatakeS1(
        **{
            "EW_ETA__AX_local_expected": 1,
            "EW_ETA__AX_local_percentage": 100,
            "EW_ETA__AX_local_status": "Complete",
            "EW_ETA__AX_local_value": 1,
            "EW_ETA__AX_local_value_adjusted": 1,
            "EW_GRDM_1A_local_expected": 336776000,
            "EW_GRDM_1A_local_percentage": 100,
            "EW_GRDM_1A_local_status": "Complete",
            "EW_GRDM_1A_local_value": 336936000,
            "EW_GRDM_1A_local_value_adjusted": 336776000,
            "EW_GRDM_1S_local_expected": 336776000,
            "EW_GRDM_1S_local_percentage": 100,
            "EW_GRDM_1S_local_status": "Complete",
            "EW_GRDM_1S_local_value": 336936000,
            "EW_GRDM_1S_local_value_adjusted": 336776000,
            "EW_OCN__2A_local_expected": 614621000,
            "EW_OCN__2A_local_percentage": 54.81931141304967,
            "EW_OCN__2A_local_status": "Partial",
            "EW_OCN__2A_local_value": 336931000,
            "EW_OCN__2A_local_value_adjusted": 336931000,
            "EW_OCN__2S_local_expected": 614621000,
            "EW_OCN__2S_local_percentage": 54.81931141304967,
            "EW_OCN__2S_local_status": "Partial",
            "EW_OCN__2S_local_value": 336931000,
            "EW_OCN__2S_local_value_adjusted": 336931000,
            "EW_RAW__0A_local_expected": 336411000,
            "EW_RAW__0A_local_percentage": 100,
            "EW_RAW__0A_local_status": "Complete",
            "EW_RAW__0A_local_value": 336546000,
            "EW_RAW__0A_local_value_adjusted": 336411000,
            "EW_RAW__0C_local_expected": 336411000,
            "EW_RAW__0C_local_percentage": 100,
            "EW_RAW__0C_local_status": "Complete",
            "EW_RAW__0C_local_value": 336546000,
            "EW_RAW__0C_local_value_adjusted": 336411000,
            "EW_RAW__0N_local_expected": 336411000,
            "EW_RAW__0N_local_percentage": 100,
            "EW_RAW__0N_local_status": "Complete",
            "EW_RAW__0N_local_value": 336546000,
            "EW_RAW__0N_local_value_adjusted": 336411000,
            "EW_RAW__0S_local_expected": 336411000,
            "EW_RAW__0S_local_percentage": 100,
            "EW_RAW__0S_local_status": "Complete",
            "EW_RAW__0S_local_value": 336546000,
            "EW_RAW__0S_local_value_adjusted": 336411000,
            "EW_SLC__1A_local_expected": 60230000,
            "EW_SLC__1A_local_percentage": 100,
            "EW_SLC__1A_local_status": "Complete",
            "EW_SLC__1A_local_value": 65980000.00000001,
            "EW_SLC__1A_local_value_adjusted": 60230000,
            "EW_SLC__1S_local_expected": 60230000,
            "EW_SLC__1S_local_percentage": 100,
            "EW_SLC__1S_local_status": "Complete",
            "EW_SLC__1S_local_value": 65980000.00000001,
            "EW_SLC__1S_local_value_adjusted": 60230000,
            "_id": "S1A-384640",
            "_index": "cds-datatake-s1-s2",
            "absolute_orbit": "48804",
            "application_date": "2023-06-01T17:42:07.000Z",
            "cams_description": "SDuplicated DTs due to unplanned session over NSG",
            "cams_origin": "Acquisition",
            "cams_tickets": ["GSANOM-12846"],
            "datatake_id": "384640",
            "etad_global_expected": 1,
            "etad_global_percentage": 100,
            "etad_global_status": "Complete",
            "etad_global_value": 1,
            "etad_global_value_adjusted": 1,
            "hex_datatake_id": "5DE80",
            "instrument_mode": "EW",
            "instrument_swath": "0",
            "key": "S1A-384640",
            "l0_sensing_duration": 336546000,
            "l0_sensing_time_start": "2023-06-02T07:45:37.715Z",
            "l0_sensing_time_stop": "2023-06-02T07:51:14.261Z",
            "last_attached_ticket": "GSANOM-12846",
            "last_attached_ticket_url": "https://esa-cams.atlassian.net/browse/GSANOM-12846",
            "mission": "S1",
            "name": "S1A_MP_ACQ__L0__20230601T174207_20230613T195516.csv",
            "observation_duration": 334221000,
            "observation_time_start": "2023-06-02T07:45:38.880Z",
            "observation_time_stop": "2023-06-02T07:51:13.101Z",
            "polarization": "DH",
            "relative_orbit": "82",
            "satellite_unit": "S1A",
            "sensing_global_expected": 3368896000,
            "sensing_global_percentage": 83.51454007484944,
            "sensing_global_status": "Partial",
            "sensing_global_value": 2813518000,
            "sensing_global_value_adjusted": 2813518000,
            "sort": [53236, 1706097514546],
            "timeliness": "NRT-PT",
            "updateTime": ["2024-01-24T11:58:34.546Z"],
        }
    )

    CdsDatatake.MISSING_PERIODS_MAXIMAL_OFFSET = {
        "S1": {
            "global": 0,
            "local": {
                "default": 6000000,
            },
        },
    }
    test_related_documents = []

    local_value = datatake_doc.compute_local_value("EW_GRDM_1S", test_related_documents)

    # No reg value
    assert local_value == 336936000.0

    assert test_related_documents

    datatake_doc.compute_duplicated("EW_GRDM_1S", test_related_documents)

    assert datatake_doc.EW_GRDM_1S_duplicated_max_percentage == 70.1056701890063
    assert datatake_doc.EW_GRDM_1S_duplicated_max_duration == 42062


duplicated_s1_rf_products_dict = [
    {
        "absolute_orbit": "55053",
        "datatake_id": "439572",
        "key": "989ab9ce96d9ccdfd9e0d248b2e8cb71",
        "_id": "989ab9ce96d9ccdfd9e0d248b2e8cb71",
        "instrument_mode": "RFC",
        "mission": "S1",
        "polarization": "DV",
        "product_class": "S",
        "product_type": "RF_RAW__0S",
        "product_level": "L0_",
        "satellite_unit": "S1A",
        "sensing_start_date": "2024-08-03T20:39:08.776Z",
        "sensing_end_date": "2024-08-03T20:39:10.184Z",
        "sensing_duration": 1408000,
        "timeliness": "NTC",
        "content_length": 54198690,
        "dddas_name": "S1A_RF_RAW__0SDV_20240803T203908_20240803T203910_055053_06B514_D904.SAFE",
        "dddas_publication_date": "2024-08-03T21:39:33.638Z",
        "updateTime": "2024-08-03T22:32:36.748Z",
        "name": "S1A_RF_RAW__0SDV_20240803T203908_20240803T203910_055053_06B514_D904.SAFE.zip",
        "expected_lta_number": 4,
        "LTA_CloudFerro_is_published": True,
        "LTA_CloudFerro_publication_date": "2024-08-03T21:40:21.106000+00:00",
        "nb_lta_served": 4,
        "prip_id": "9c1954ea-fb38-4ddb-9f30-e07b22cda840",
        "prip_publication_date": "2024-08-03T21:33:38.726Z",
        "prip_service": "PRIP_S1A_Serco",
        "EU_coverage_percentage": 0,
        "from_prip_dddas_timeliness": 354912000,
        "LTA_Werum_is_published": True,
        "LTA_Werum_publication_date": "2024-08-03T21:40:31.496000+00:00",
        "LTA_Acri_is_published": True,
        "LTA_Acri_publication_date": "2024-08-03T22:07:05.745000+00:00",
        "LTA_Exprivia_S1_is_published": True,
        "LTA_Exprivia_S1_publication_date": "2024-08-03T22:03:17.276000+00:00",
        "_index": "cds-product-2024-08",
    },
    {
        "absolute_orbit": "55053",
        "datatake_id": "439572",
        "key": "40354d5c65e3e02e905770f5a6c81e2c",
        "_id": "40354d5c65e3e02e905770f5a6c81e2c",
        "_index": "cds-product-2024-08",
        "instrument_mode": "RFC",
        "mission": "S1",
        "name": "S1A_RF_RAW__0SDV_20240803T203908_20240803T203910_055053_06B514_4380.SAFE.zip",
        "polarization": "DV",
        "product_class": "S",
        "product_type": "RF_RAW__0S",
        "product_level": "L0_",
        "satellite_unit": "S1A",
        "sensing_start_date": "2024-08-03T20:39:08.777Z",
        "sensing_end_date": "2024-08-03T20:39:10.184Z",
        "sensing_duration": 1407000,
        "timeliness": "NTC",
        "content_length": 54198682,
        "prip_id": "3c5aab0f-2f37-4775-acfb-47c60eb97f16",
        "prip_publication_date": "2024-08-03T21:31:09.101Z",
        "prip_service": "PRIP_S1A_Serco",
        "EU_coverage_percentage": 0,
        "updateTime": "2024-08-03T22:32:03.479Z",
        "dddas_name": "S1A_RF_RAW__0SDV_20240803T203908_20240803T203910_055053_06B514_4380.SAFE",
        "dddas_publication_date": "2024-08-03T21:36:30.131Z",
        "from_prip_dddas_timeliness": 321030000,
        "expected_lta_number": 4,
        "LTA_CloudFerro_is_published": True,
        "LTA_CloudFerro_publication_date": "2024-08-03T21:37:08.639000+00:00",
        "nb_lta_served": 4,
        "LTA_Werum_is_published": True,
        "LTA_Werum_publication_date": "2024-08-03T21:40:30.207000+00:00",
        "LTA_Exprivia_S1_is_published": True,
        "LTA_Exprivia_S1_publication_date": "2024-08-03T21:43:00.102000+00:00",
        "LTA_Acri_is_published": True,
        "LTA_Acri_publication_date": "2024-08-03T22:14:05.765000+00:00",
    },
]


@patch("maas_cds.model.datatake_s1.CdsDatatakeS1.find_brother_products_scan")
@patch("maas_cds.model.datatake_s1.CdsDatatakeS1.evaluate_local_expected")
def test_compute_duplicated_periods(
    mock_evaluate_local_expected,
    mock_get_datatake_product_type_brother,
):
    """compute_local_sensing_duration test"""

    duplicated_s1_products_clean = []
    for product_dict in duplicated_s1_rf_products_dict:
        product = CdsProductS1(**product_dict)
        product.meta.id = product_dict["_id"]
        product.meta.index = product_dict["_index"]

        product.full_clean()

        duplicated_s1_products_clean.append(product)

    mock_get_datatake_product_type_brother.return_value = duplicated_s1_products_clean

    mock_evaluate_local_expected.return_value = 336776000.0

    datatake_doc = CdsDatatakeS1(
        **{
            "name": "S1A_MP_ACQ__L0__20240803T171645_20240815T193544.csv",
            "key": "S1A-439572",
            "datatake_id": "439572",
            "hex_datatake_id": "6B514",
            "satellite_unit": "S1A",
            "mission": "S1",
            "observation_time_start": "2024-08-03T20:39:14.983Z",
            "observation_duration": 20000000,
            "observation_time_stop": "2024-08-03T20:39:34.983Z",
            "l0_sensing_duration": 20576000,
            "l0_sensing_time_start": "2024-08-03T20:39:14.701Z",
            "l0_sensing_time_stop": "2024-08-03T20:39:35.277Z",
            "absolute_orbit": "55053",
            "relative_orbit": "31",
            "polarization": "DV",
            "timeliness": "NTC",
            "instrument_mode": "RFC",
            "instrument_swath": "0",
            "application_date": "2024-08-03T17:16:45.000Z",
            "updateTime": "2024-08-06T09:30:29.206Z",
            "RF_RAW__0S_local_value": 2815000,
            "RF_RAW__0S_local_expected": 2800000,
            "RF_RAW__0S_local_value_adjusted": 2800000,
            "RF_RAW__0S_local_percentage": 100,
            "RF_RAW__0S_local_status": "Complete",
            "duplicated_global_max_duration": 0,
            "duplicated_global_max_percentage": 0,
            "sensing_global_value": 2800000,
            "sensing_global_expected": 2800000,
            "sensing_global_value_adjusted": 2800000,
            "sensing_global_percentage": 100,
            "sensing_global_status": "Complete",
            "cams_tickets": ["GSANOM-15862"],
            "last_attached_ticket": "GSANOM-15862",
            "last_attached_ticket_url": "https://esa-cams.atlassian.net/browse/GSANOM-15862",
            "cams_origin": "Acquisition",
            "cams_description": "Unexpected downloaded data - Inuvik not planned",
        }
    )

    CdsDatatake.MISSING_PERIODS_MAXIMAL_OFFSET = {
        "S1": {
            "global": 0,
            "local": {
                "default": 6000000,
            },
        },
    }
    test_related_documents = []

    local_value = datatake_doc.compute_local_value("EW_GRDM_1S", test_related_documents)

    # No reg value
    assert local_value == 1408000.0

    assert test_related_documents

    datatake_doc.compute_duplicated("EW_GRDM_1S", test_related_documents)

    assert datatake_doc.EW_GRDM_1S_duplicated_max_percentage == 99.92897727272727
    assert datatake_doc.EW_GRDM_1S_duplicated_max_duration == 1407
