"""Configuration related functions"""

import re

import logging

from maas_cds.model.enumeration import CompletenessScope

LOGGER = logging.getLogger("Tolerance")


def get_completeness_tolerance(
    completeness_tolerance: dict,
    mission: str,
    scope: CompletenessScope,
    product_type=None,
) -> int:
    """Get completeness tolerance in configuration

    Args:
        completeness_tolerance (dict): completeness tolerance from configuration
        mission (str): the mission selected
        scope (CompletenessScope): the scope that we want to get the tolerance
                                    (local, global or final)
        product_type (str, optional): product_type that we want to get the tolerance.
                                    Defaults to None.

    Returns:
        int: tolerance value
    """
    LOGGER.debug("find tolerance for %s %s %s", mission, scope.value, product_type)
    tolerance = 0

    if (
        completeness_tolerance
        and mission
        and product_type
        and scope in CompletenessScope
    ):

        try:
            scoped_tolerance = completeness_tolerance[mission][scope.value]

            tolerance = get_tolerance_from_scope(scoped_tolerance, product_type)

        except KeyError:
            LOGGER.debug("tolerance for %s %s not found", mission, scope.value)

    else:
        LOGGER.debug("no tolerance or mission in configuration")

    return tolerance


def get_tolerance_from_scope(scope_tolerance: dict, product_type: str) -> int:
    """Get all completeness tolerance in scope completeness tolerance configuration

    Args:
        scope_tolerance (dict): scope completeness tolerance from configuration
        product_type (str): product_type that we want to get the tolerance.

    Returns:
        int: the tolerance
    """
    if scope_tolerance:
        for product_type_pattern in scope_tolerance:
            try:
                if re.match(product_type_pattern, product_type):
                    LOGGER.debug(
                        "matching tolerance for %s with %s",
                        product_type,
                        product_type_pattern,
                    )
                    return scope_tolerance[product_type_pattern]
            except re.error:
                LOGGER.warning("bad regular expression %s", product_type_pattern)
                return 0

        if "default" in scope_tolerance:
            return scope_tolerance["default"]

        LOGGER.debug(
            "no key match configuration [%s] in the given scope tolerance", product_type
        )
        return 0

    LOGGER.debug(
        "no configuration find for this parameter %s with %s",
        product_type,
        scope_tolerance,
    )
    return 0
