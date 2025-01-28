""" Custom method to extract data from sentinel 2 product name"""

import logging
import re

from maas_model import datestr_to_utc_datetime


LOGGER = logging.getLogger("ParsingName")


def is_compact(product_name):
    """Check if a product_name is compat

    Args:
        product_name (str): the name of the product

    Returns:
        bool: true if the given product_name is compact else false
    """
    # Regex on multiline decrease comprehension and readibility
    # pylint: disable=C0301
    is_compact_product = re.match(
        "S2[A|B|C|_]_[A-Z0-9]{6}_[0-9]{8}T[0-9]{6}_N[0-9]{4}_R[0-9]{3}(_T[A-Z0-9]{5})?_[0-9]{8}T[0-9]{6}(.SAFE|.zip)?$",
        product_name,
    )

    return is_compact_product is not None


def extract_data_from_product_name_s2(product_name):
    """Method to extract data from a sentinel 2 product name

    Args:
        product_name (str): name of a sentinel 2 product

    Returns:
        dict: dict with all data extracted from the name
    """

    if is_compact(product_name):
        extract_method = extract_data_from_product_name_s2_compact_naming
    else:
        extract_method = extract_data_from_product_name_s2_granule_tile

    return extract_method(product_name)


def extract_data_from_product_name_s2_compact_naming(product_name):
    """
    Compact naming conventions

    MMM_MSIXXX_YYYYMMDDHHMMSS_Nxxyy_ROOO(_Txxxxx)_<Product Discriminator>(.SAFE|.zip)
    """

    # workaround for specific MPCIP case (no tile in product name)
    if product_name[38] != "T":
        product_name = product_name[:38] + "T_____" + "_" + product_name[38:]

    extracted_data = {
        "mission": product_name[:2],
        "satellite_unit": product_name[:3],
        "product_level": product_name[7:10],
        "datatake_id_sensing_time": datestr_to_utc_datetime(product_name[11:26]),
        "product_discriminator_date": datestr_to_utc_datetime(product_name[45:60]),
        "product_type": f"MSI_{product_name[7:10]}___",
    }

    extracted_data |= extract_optional_char_id(product_name[26:44])

    return extracted_data


def extract_data_from_product_name_s2_granule_tile(product_name):
    """
    Compact naming conventions

    MMM_CCCCC_FFFFDDDDD_ssss_YYYYMMDDTHHMMSS_<>_Nxx.yy.EXT
    """

    # Report product
    if re.match(".*_report\\.(xml|tar)", product_name):
        product_type = "OLQC_REPORT"
    else:
        product_type = product_name[9:19]

        if "AUX" in product_type:
            splitted_name = product_name.split("_")
            product_type = f"AUX_{splitted_name[splitted_name.index('AUX')+1]}"

    extracted_data = {
        "mission": product_name[:2],
        "satellite_unit": product_name[:3],
        "file_class": product_name[4:8],
        "product_type": product_type,
        "file_category": product_name[9:13],
    }

    extra_data_category = extract_file_category_data(
        extracted_data["file_category"], product_name
    )
    if "product_level" not in extra_data_category:
        extra_data_category["product_level"] = "L__"

    extracted_data |= extra_data_category

    extra_data_optionnal_char = extract_optional_char_id(product_name[40:])

    extracted_data |= extra_data_optionnal_char

    for key in (
        "applicability_start_time",
        "start_applicability_time_period",
        "datatake_id_sensing_time",
    ):
        if key in extracted_data:
            extracted_data["sensing_start_date"] = extracted_data[key]
            break

    return extracted_data


def extract_optional_char_id(short_product_name: str):
    """This method extract information by using prefix letter

    Args:
        short_product_name (str): the sentinel 2 product name without the begin (around 40 char)

    Returns:
        dict: dict with some data extracted from the name
    """

    dict_char_label = {
        "_S": lambda x: {"applicability_start_time": datestr_to_utc_datetime(x[:15])},
        "_O": lambda x: (
            {  # specific rule for skip _OLQC
                "first_absolute_orbit_number": datestr_to_utc_datetime(x.split("_")[0]),
                "last_absolute_orbit_number": datestr_to_utc_datetime(
                    x.split("_")[1][:15]
                ),
            }
            if len(x.split("_")[0]) == 15
            else {}
        ),
        "_V": lambda x: {
            "start_applicability_time_period": datestr_to_utc_datetime(x.split("_")[0]),
            "end_applicability_time_period": datestr_to_utc_datetime(
                x.split("_")[1][:15]
            ),
        },
        "_D": lambda x: {"detector_id": x[:2]},
        "_A": lambda x: {"absolute_orbit_number": x[:6]},
        "_R": lambda x: {"relative_orbit_number": x[:3]},
        "_T": lambda x: {"tile_number": x[:5]},
        "_N": lambda x: {
            "processing_baseline_number": x.replace(".", "")[:4],
        },
        "_B": lambda x: {"band_index_id": x[:2]},
        "_W": lambda x: {"completeness_id": x[:1]},
        "_L": lambda x: {"degradation_id": x[:1]},
    }

    optionnal_data = {}

    for key, value in dict_char_label.items():
        try:
            option_index = short_product_name.find(key)

            if option_index == -1:
                continue
            # Remove head and prefix
            char_info = short_product_name[option_index:][2:]

            optionnal_data |= value(char_info)
        except Exception:
            if not short_product_name.endswith("SENSOR_QUALITY_report.xml"):
                LOGGER.warning("Failed to use %s with %s", key, char_info)
            continue

    return optionnal_data


def extract_file_category_data(file_category, product_name):
    """This method extract information by using file category

    Args:
        file_category (str): the fiel category of the product
        product_name (str): the sentinel 2 product name

    Returns:
        dict: dict with some data extracted from the name
    """

    dict_file_category_extract_data = {
        "MSI_": lambda f: {
            "product_level": product_name[13:16],
            "site_center": product_name[20:24],
            "creation_date": datestr_to_utc_datetime(product_name[25:40]),
        },
        "AUX_": lambda f: {
            "site_center": product_name[20:24],
            "creation_date": datestr_to_utc_datetime(product_name[25:40]),
        },
        "GIP_": lambda f: {
            "site_center": product_name[20:24],
            "creation_date": datestr_to_utc_datetime(product_name[25:40]),
        },
    }

    extracted_date = {}
    try:
        extracted_date = dict_file_category_extract_data[file_category](product_name)
    except KeyError:
        pass

    return extracted_date
