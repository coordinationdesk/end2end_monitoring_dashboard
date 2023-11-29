"""Tests for tolerance configuration"""


import pytest

from maas_cds.lib import tolerance

from maas_cds.model.enumeration import CompletenessScope


@pytest.fixture
def tolerance_config():
    """tolerance configuration"""
    completeness_tolerance = {
        "S1": {
            "global": {"sensing": 1},
            "local": {".*0.*": 2, ".*1.*": 3, ".*2.*": 4, "default": 5},
        },
        "S2": {
            "global": {"DS.*": 15, "GR.*": 16, "TL.*": 17, "TC.*": 18, "default": 19},
            "local": {".*0.*": 7, ".*1.*": 8, ".*2.*": 9, "default": 10},
        },
        "S3": {
            "global": 11,
            "local": {".*0.*": 11, ".*1.*": 12, ".*2.*": 13, "default": 14},
        },
    }

    return completeness_tolerance


def test_get_completeness_mission_tolerance_no_mission():
    """test get_completeness_mission_tolerance : no mission"""
    completeness_tolerance = {
        "S1": {
            "global": {"sensing": 1},
            "local": {".*0.*": 2, ".*1.*": 3, ".*2.*": 4, "default": 5},
        },
        "S2": {
            "global": 6,
            "local": {".*0.*": 7, ".*1.*": 8, ".*2.*": 9, "default": 10},
        },
        "S3": {
            "global": 11,
            "local": {".*0.*": 11, ".*1.*": 12, ".*2.*": 13, "default": 14},
        },
    }

    mission_tolerance = tolerance.get_completeness_tolerance(
        completeness_tolerance, "S4", CompletenessScope.GLOBAL, "sensing"
    )

    assert mission_tolerance == 0


def test_get_completeness_mission_tolerance_no_completeness():
    """test get_completeness_mission_tolerance : no completeness tolerance"""
    completeness_tolerance = {}

    mission_tolerance = tolerance.get_completeness_tolerance(
        completeness_tolerance, "S2", CompletenessScope.GLOBAL, "sensing"
    )

    assert mission_tolerance == 0


def test_get_completeness_mission_tolerance_bad_key(tolerance_config):
    """test get_completeness_mission_tolerance : bad key"""

    mission_tolerance = tolerance.get_completeness_tolerance(
        tolerance_config, "S4", CompletenessScope.GLOBAL, "sensing"
    )

    assert mission_tolerance == 0


def test_get_completeness_mission_scope_tolerance_global():
    """test get_completeness_mission_tolerance : bad key"""
    mission_tolerance = {
        "S1": {
            "global": {"sensing": 1},
            "local": {"*0": 2, ".*1.*": 3, ".*2.*": 4, "default": 5},
        }
    }

    scope_tolerance = tolerance.get_completeness_tolerance(
        mission_tolerance, "S1", CompletenessScope.GLOBAL, "sensing"
    )

    assert scope_tolerance == 1


def test_get_completeness_mission_scope_tolerance_bad_scope():
    """test get_completeness_mission_tolerance : bad key"""
    mission_tolerance = {
        "S1": {"local": {"*0": 2, ".*1.*": 3, ".*2.*": 4, "default": 5}}
    }

    scope_tolerance = tolerance.get_completeness_tolerance(
        mission_tolerance, "S1", CompletenessScope.GLOBAL, "sensing"
    )

    assert scope_tolerance == 0


def test_get_completeness_mission_scope_with_product_type_tolerance():

    """test get_completeness_mission_tolerance : bad key"""
    scope_tolerance = {
        "S1": {"local": {".*0.*": 2, ".*1.*": 3, ".*2.*": 4, "default": 5}}
    }

    tolerance_value = tolerance.get_completeness_tolerance(
        scope_tolerance,
        "S1",
        CompletenessScope.LOCAL,
        "IW_RAW__0A",
    )

    assert tolerance_value == 2


def test_get_completeness_mission_scope_with_product_type_tolerance_default():

    """test get_completeness_mission_tolerance : bad key"""
    scope_tolerance = {
        "S1": {"local": {".*0.*": 2, ".*1.*": 3, ".*2.*": 4, "default": 5}}
    }

    tolerance_value = tolerance.get_completeness_tolerance(
        scope_tolerance,
        "S1",
        CompletenessScope.LOCAL,
        "IW_RAW___A",
    )

    assert tolerance_value == 5


def test_get_completeness_mission_scope_with_product_type_tolerance_no_default():

    """test get_completeness_mission_tolerance : bad key"""
    scope_tolerance = {"S1": {"local": {".*0.*": 2, ".*1.*": 3, ".*2.*": 4}}}

    tolerance_value = tolerance.get_completeness_tolerance(
        scope_tolerance, "S1", CompletenessScope.LOCAL, "IW_RAW___A"
    )

    assert tolerance_value == 0


def test_get_completeness_mission_scope_with_product_type_tolerance_bad_re():

    """test get_completeness_mission_tolerance : bad key"""
    scope_tolerance = {"S1": {"local": {"*0.*": 2, ".*1.*": 3, ".*2.*": 4}}}

    tolerance_value = tolerance.get_completeness_tolerance(
        scope_tolerance, "S1", CompletenessScope.GLOBAL, "IW_RAW___A"
    )

    assert tolerance_value == 0


def test_get_completeness_mission_tolerance_1(tolerance_config):
    """test get_completeness_mission_tolerance : nominal"""

    tolerance_value = tolerance.get_completeness_tolerance(
        tolerance_config, "S1", CompletenessScope.GLOBAL, "sensing"
    )

    assert tolerance_value == 1


def test_get_completeness_mission_tolerance_2(tolerance_config):
    """test get_completeness_mission_tolerance : nominal"""

    tolerance_value = tolerance.get_completeness_tolerance(
        tolerance_config, "S2", CompletenessScope.LOCAL, "IW_RAW__2A"
    )

    assert tolerance_value == 9


def test_get_completeness_mission_tolerance_no_conf():
    """test get_completeness_mission_tolerance : nominal"""

    tolerance_value = tolerance.get_completeness_tolerance(
        None, "S2", CompletenessScope.LOCAL, "IW_RAW__2A"
    )

    assert tolerance_value == 0
