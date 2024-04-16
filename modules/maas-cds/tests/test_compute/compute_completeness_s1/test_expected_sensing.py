"""Tests for MP consolidation into datatake"""


from maas_cds.model.datatake_s1 import (
    CdsDatatakeS1,
)


def test_get_expected_from_product_type_1():
    """test get_expected_value with level 0"""

    datatake_doc = CdsDatatakeS1()

    product_type = "WV_RAW__0A"

    setattr(datatake_doc, "l0_sensing_duration", 20)
    setattr(datatake_doc, "observation_duration", 30)

    expected_value = datatake_doc.get_expected_from_product_type(product_type)

    assert expected_value["sensing"] == 20


def test_get_expected_from_product_type_2():
    """test get_expected_value with not level 0"""

    datatake_doc = CdsDatatakeS1()

    product_type = "WV_OCN__2A"

    setattr(datatake_doc, "l0_sensing_duration", 20)
    setattr(datatake_doc, "observation_duration", 30)

    expected_value = datatake_doc.get_expected_from_product_type(product_type)

    assert expected_value["sensing"] == 20


def test_get_expected_from_product_type_3():
    """test get_expected_value with RFC product"""

    datatake_doc = CdsDatatakeS1()

    product_type = "RF_RAW__0S"

    setattr(datatake_doc, "l0_sensing_duration", 20)
    setattr(datatake_doc, "observation_duration", 30)

    expected_value = datatake_doc.get_expected_from_product_type(product_type)

    assert expected_value["sensing"] == 2800000


def test_get_expected_from_product_type_4():
    """test get_expected_value with  level 0 and no attribut"""

    datatake_doc = CdsDatatakeS1()

    product_type = "WV_RAW__0A"

    setattr(datatake_doc, "observation_duration", 30)

    expected_value = datatake_doc.get_expected_from_product_type(product_type)

    assert expected_value["sensing"] == 0


def test_get_expected_from_product_type_5():
    """test get_expected_value with  not level 0 and no attribut"""

    datatake_doc = CdsDatatakeS1()

    product_type = "WV_OCN__2A"

    setattr(datatake_doc, "l0_sensing_duration", 20)

    expected_value = datatake_doc.get_expected_from_product_type(product_type)

    assert expected_value["sensing"] == 20
