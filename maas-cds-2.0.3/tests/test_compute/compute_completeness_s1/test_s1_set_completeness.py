"""Tests for MP consolidation into datatake"""


from unittest.mock import patch

import maas_cds.model as model

from maas_cds.model.enumeration import CompletenessScope


from maas_cds.model.datatake_s1 import (
    CdsDatatakeS1,
)


def test_set_completeness_1():
    """fill_local_completeness test"""

    product_type = "PRODUCT_TYPE_0"

    sensing_duration = 10

    datatake_doc = CdsDatatakeS1(l0_sensing_duration=20)

    datatake_doc.set_completeness(
        CompletenessScope.LOCAL, product_type, sensing_duration
    )

    assert datatake_doc.PRODUCT_TYPE_0_local_expected == 20

    assert datatake_doc.PRODUCT_TYPE_0_local_value_adjusted == 10

    assert datatake_doc.PRODUCT_TYPE_0_local_percentage == 50

    assert (
        datatake_doc.PRODUCT_TYPE_0_local_status
        == model.CompletenessStatus.PARTIAL.value
    )


def test_set_completeness_2():
    "fill_local_completeness test with excluted produt type"

    product_type = "WV_OCN_0"

    sensing_duration = 10

    datatake_doc = CdsDatatakeS1(l0_sensing_duration=20)

    datatake_doc.set_completeness(
        CompletenessScope.LOCAL, product_type, sensing_duration
    )

    assert datatake_doc.WV_OCN_0_local_expected == 20

    assert datatake_doc.WV_OCN_0_local_value_adjusted == 10

    assert datatake_doc.WV_OCN_0_local_percentage == 50

    assert datatake_doc.WV_OCN_0_local_status == model.CompletenessStatus.PARTIAL.value


def test_fill_global_completeness_1():
    """fill_global_completeness test"""

    datatake_doc = CdsDatatakeS1()

    datatake_doc.IW_OCN__2S_local_value = 10

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
