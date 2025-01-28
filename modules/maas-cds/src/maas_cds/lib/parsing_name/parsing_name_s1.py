""" Custom method to extract data from sentinel 1 product name"""

import re

from maas_model import datestr_to_utc_datetime


def extract_product_type_from_product_name_s1(product_name):
    # TODO Quick win store the next stuff in database
    #! But care to migration

    regex_patterns = {
        "AMALFI_REPORT": r".*-report-[0-9]{8}T[0-9]{6}.xml$",
        "OUT_OF_MONITORING": r"(.*_COG.*)|(.*CARD_BS$)",  # todo verify ut
    } | {
        f"{pattern_type}": r".*{}.*".format(pattern_type)
        for pattern_type in ["AISAUX", "MPL_TIMELINE", "MP_FULL", "MP_ALL__"]
    }

    for product_type, pattern in regex_patterns.items():
        if re.match(pattern, product_name):
            return product_type

    # Handling AUX
    if match := re.search(r"_AUX_([a-zA-Z0-9]*)_", product_name):
        return f"AUX_{match.group(1)}"

    # Handling OPER
    if match := re.search(r"_OPER_([a-zA-Z0-9]*_[a-zA-Z0-9]*)_", product_name):
        return f"{match.group(1)}"

    # 90% product_type is on 10 char
    return product_name[4:14]


def extract_data_from_product_name_s1(product_name):
    """Method to extract data from a sentinel 1 product name

    Args:
        product_name (str): name of a sentinel 1 product

    Returns:
        dict: dict with all data extracted from the name
    """
    # If too much bug extend this to all mission
    product_type = extract_product_type_from_product_name_s1(product_name)

    data = {
        "satellite_unit": product_name[:3],  # S1A / S1B / S1_
        "mission": product_name[:2],
        "product_type": product_type,
        "product_level": "L__",
    }
    # Standart Product format
    # MMM_BB_TTTR_LFPP_YYYYMMDDTHHMMSS_YYYYMMDDTHHMMSS_OOOOOO_DDDDDD_CCCC

    # ensure product get a production level
    # L
    product_level = product_name[12]

    if product_level in ["0", "1", "2"] or (product_type[3:] == "ETA__AX"):

        extra_data_from_parsing = {}

        try:

            extra_data_from_parsing["product_level"] = f"L{product_level}_"

            # BB
            extra_data_from_parsing["instrument_mode"] = product_name[
                4:6
            ]  # IW-EW-VW-RF-SM-AI

            # TTT
            extra_data_from_parsing["type"] = product_name[7:10]

            # R
            extra_data_from_parsing["resolution_class"] = product_name[10]

            # F
            extra_data_from_parsing["product_class"] = product_name[13]

            # PP
            extra_data_from_parsing["polarization"] = product_name[14:16]

            # first date
            extra_data_from_parsing["start_date"] = datestr_to_utc_datetime(
                product_name[17:32]
            )

            # second date
            extra_data_from_parsing["stop_date"] = datestr_to_utc_datetime(
                product_name[33:48]
            )

            # OOOOOO
            extra_data_from_parsing["absolute_orbit_number"] = product_name[49:55]

            # DDDDDD
            extra_data_from_parsing["datatake_id"] = product_name[56:62]

            # CCCC
            extra_data_from_parsing["product_unique_id"] = product_name[63:67]

        except ValueError as _:
            pass
        else:
            data |= extra_data_from_parsing

    return data
