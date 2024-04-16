"""Tests for MP consolidation into datatake"""


import datetime
from unittest.mock import patch

import maas_cds.model as model
from maas_cds.model.datatake import CdsDatatake


from maas_cds.model.datatake_s1 import (
    CdsDatatakeS1,
)


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
