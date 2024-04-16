""" Custom method to extract data from sentinel 1 product name"""
import re

from maas_model import datestr_to_utc_datetime


def extract_data_from_product_name_s1(product_name):
    """Method to extract data from a sentinel 1 product name

    Args:
        product_name (str): name of a sentinel 1 product

    Returns:
        dict: dict with all data extracted from the name
    """

    # Report product
    if re.match(".*-report-[0-9]{8}T[0-9]{6}.xml$", product_name):
        product_type = "AMALFI_REPORT"
    else:
        product_type = product_name[4:14]

        if product_type.startswith("OPER"):
            product_type = product_name[9:19]

        elif "AUX" in product_type:
            splitted_name = product_name.split("_")
            product_type = f"AUX_{splitted_name[splitted_name.index('AUX')+1]}"

        elif product_type.startswith('MP'):
            splitted_name = product_name.split("_")
            product_type = f"MP_{splitted_name[splitted_name.index('MP')+1]}"

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

    if product_level in ["0", "1", "2"] or ( product_type[3:] == "ETA__AX"):

        extra_data_from_parsing = {}

        try:

            extra_data_from_parsing["product_level"] = f"L{product_level}_"

            # BB
            extra_data_from_parsing["instrument_mode"] = product_name[4:6]  # IW-EW-VW-RF-SM

            # TTT
            extra_data_from_parsing["type"] = product_name[7:10]

            # R
            extra_data_from_parsing["resolution_class"] = product_name[10]

            # F
            extra_data_from_parsing["product_class"] = product_name[13]

            # PP
            extra_data_from_parsing["polarization"] = product_name[14:16]

            # first date
            extra_data_from_parsing["start_date"] = datestr_to_utc_datetime(product_name[17:32])

            # second date
            extra_data_from_parsing["stop_date"] = datestr_to_utc_datetime(product_name[33:48])

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
