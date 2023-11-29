""" Custom method to extract data from sentinel 5 product name"""

import logging
from maas_model import datestr_to_utc_datetime

LOGGER = logging.getLogger("ParsingNameS5")


def extract_data_from_product_name_s5(product_name):
    """Method to extract data from a sentinel 5 product name

    Args:
        product_name (str): name of a sentinel 5 product

    Returns:
        dict: dict with all data extracted from the name
    """
    # legitimate long comment
    # pylint: disable=C0301

    # Classic Product format
    # MMM_<FileClass>_L__TTTTTT_YYYYMMDDTHHMMSS_YYYYMMDDTHHMMSS_<Absolute_Orbit>_<Collection_number>_<Processor_Version>_YYYYMMDDTHHMMSS.XXX

    data = {}

    try:

        data["mission"] = product_name[:2]

        data["satellite_unit"] = product_name[:3]

        data["timeliness"] = product_name[4:8]

        data["product_type"] = product_name[4:19]

        data["start_sensing_time"] = datestr_to_utc_datetime(product_name[20:35])

        data["end_sensing_time"] = datestr_to_utc_datetime(product_name[36:51])

        product_level = product_name[10:12]
        if product_level[0] not in ["0", "1", "2"]:

            # Maybe aux or something
            product_level = "__"

            data["production_start_date"] = datestr_to_utc_datetime(product_name[52:67])

        else:
            data["absolute_orbit_number"] = product_name[52:57]

            data["collection_number"] = product_name[58:60]

            # To skip product with shoter name
            if len(product_name.split(".")[0]) > 61:

                data["processor_version"] = product_name[61:67]

                data["production_start_date"] = datestr_to_utc_datetime(
                    product_name[68:83]
                )

            # S5 products don't have mission planning with datatakes. Though, to ease later
            # calculation, a pseudo datatake identifier is generated.
            #
            # this pseudo datatake shall match the orbit, which is the base for S5 completeness
            #
            data[
                "datatake_id"
            ] = f"{data['satellite_unit']}-{data['absolute_orbit_number']}"

        data["product_level"] = f"L{product_level}"

    except (ValueError, IndexError) as error:

        LOGGER.warning(
            "Failed to extract data from S5 name %s: %s", product_name, error
        )

    return data
