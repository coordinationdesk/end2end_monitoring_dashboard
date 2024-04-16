"""Query to find datatake"""

import datetime
import logging
import typing

from maas_cds.model.datatake import CdsDatatake

__all__ = ["find_datatake_from_product_group_id"]

LOGGER = logging.getLogger("QueryUtils")


def find_datatake_from_product_group_id(
    mission: str, satellite: str, product_group_id: str
) -> typing.List[CdsDatatake]:
    """find datatake_doc function using a product group id identifier

    Args:
        mission (str): the mission of the searched datatake
        satellite (str): the satellite of the searched datatake
        product_group_id (str): datastrip id used to search in db

    Returns:
        list(CdsDatatake): the list of the datatake that match the input
    """
    if not product_group_id:
        return []

    try:
        product_id_data = extract_data_from_product_id(product_group_id)
    except ValueError:
        LOGGER.debug(
            "Could not use the product_group_id %s to rattach the product to a datatake",
            product_group_id,
        )
        return []

    # nominal use for search datake with product date information expected one datatake only
    search_request = (
        CdsDatatake.search()
        .filter("term", mission=mission)
        .filter("term", satellite_unit=satellite)
        .filter("term", absolut_orbit=product_id_data["absolute_orbit"])
        .filter(
            "range",
            observation_time_start={
                "lte": product_id_data["date"] + datetime.timedelta(seconds=15)
            },
        )
        .filter(
            "range",
            observation_time_stop={
                "gte": product_id_data["date"] - datetime.timedelta(seconds=15)
            },
        )
        .params(ignore=404)
    )

    res = search_request.execute()

    if not res:
        LOGGER.debug(
            "No datatake found yet for %s: which contain product_group_id : %s",
            satellite,
            product_group_id,
        )
        return []

    return list(res)


def extract_data_from_product_id(
    product_group_id: str,
) -> typing.Dict[str, str | datetime.datetime]:
    """Function which retrieve the different info contained in the product group id string and return a dict with them

    Args:
        product_group_id (str): _description_

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    try:
        # Expecting the following format GS2A_20240207T101201_045064_N05.10"
        sat_unit, date_str, absolut_orbit, instrument = product_group_id.split("_")

        # Remove G prefix in front of sat unit
        sat_unit = sat_unit[1:]

        # Remove trailing 0
        absolut_orbit = str(int(absolut_orbit))

        product_id_date = datetime.datetime.strptime(date_str, r"%Y%m%dT%H%M%S")

    except (IndexError, ValueError) as exc:
        raise ValueError(
            f"Could not extract data from the following product_group_id {product_group_id}."
        ) from exc
    else:
        return {
            "satellite_unit": sat_unit,
            "date": product_id_date,
            "absolute_orbit": absolut_orbit,
            "instrument": instrument,
        }
