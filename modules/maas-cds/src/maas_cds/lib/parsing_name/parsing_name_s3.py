""" Custom method to extract data from sentinel 3 product name"""

import logging
from maas_model import datestr_to_utc_datetime

LOGGER = logging.getLogger("ParsingNameS3")


def extract_data_from_product_name_s3(product_name):
    """Method to extract data from a sentinel 3 product name

    Args:
        product_name (str): name of a sentinel 3 product

    Returns:
        dict: dict with all data extracted from the name
    """
    # legitimate long comment
    # pylint: disable=C0301

    # Classic Product format
    # MMM_SS_L_TTTTTT_yyyymmddThhmmss_YYYYMMDDTHHMMSS_YYYYMMDDTHHMMSS_<instanceID>_GGG_<class ID>.(.SEN3(.zip)?)?

    data = {}

    # MMM
    data["mission"] = product_name[:2]

    data["satellite_unit"] = product_name[:3]

    product_type = product_name[4:15]

    if "AUX" in product_type:
        splitted_name = product_name.split("_")
        product_type = f"AUX_{splitted_name[splitted_name.index('AUX')+1]}"

    data["product_type"] = product_type

    product_level = product_name[7]

    if not product_level in ["_", "0", "1", "2"]:
        # skip AUX product
        data["extended_product_type"] = product_name[4:24]
        return data

    try:
        # SS
        data["instrument"] = product_name[4:6]

        # L
        data["product_level"] = f"L{product_level}_"

        # TTTTTT
        data["file_type_function"] = product_name[9:15]

        # yyyymmddThhmmss
        data["start_sensing_time"] = datestr_to_utc_datetime(product_name[16:31])

        # YYYYMMDDTHHMMSS
        data["end_sensing_time"] = datestr_to_utc_datetime(product_name[32:47])

        # YYYYMMDDTHHMMSS
        data["creation_time"] = datestr_to_utc_datetime(product_name[48:63])

        # instanceID
        data["instance_id"] = product_name[64:81]

        ######### INSTANCE ID #########
        # Complexe mapping depend of product
        # DDD_CCC_LLL_____
        # # disseminated in STRIPE L0 - L2
        # # duration_time
        # data["duration_time"] = product_name[64:68]

        # # cycle number
        # data["cycle_number"] = product_name[69:72]

        # # classic product L0
        # # duration_time
        # data["duration_time"] = product_name[64:68]

        # cycle number candidate
        cycle_number = product_name[69:72]

        # # frame along track coordinate
        # data["frame_along_track_coordinate"] = product_name[77:81]

        # relative_orbit_number candidate
        relative_orbit_number = product_name[73:76]

        # some product names do not match the rule to get relative_orbit_number and
        # cycle_number, i.e. tile products with instance ID like GLOBAL___________
        # this prevents type coerce errors.
        if relative_orbit_number.isdigit() and cycle_number.isdigit():
            data["cycle_number"] = cycle_number
            data["relative_orbit_number"] = relative_orbit_number
            # S3 products don't have mission planning with datatakes. Though, to ease later
            # calculation, a pseudo datatake identifier is generated.
            #
            # this pseudo datatake shall match the orbit, which is the base for S3 completeness
            #
            data[
                "datatake_id"
            ] = f"{data['satellite_unit']}-{data['cycle_number']}-{data['relative_orbit_number']}"
        else:
            LOGGER.debug(
                "S3 product %s has no valid cycle_number or relative_orbit_number",
                product_name,
            )

        # GGG
        data["centre"] = product_name[82:85]

        # classID
        data["class_id"] = product_name[86:94]

        ########## CLASS ID #########
        # P_XX_NNN

        # platform
        data["platform"] = product_name[86]

        # timeliness
        data["timeliness"] = product_name[88:90]

        # baseline collection
        data["baseline_collection"] = product_name[91:94]

    except (ValueError, IndexError) as error:

        LOGGER.warning(
            "Failed to extract data from S3 name %s: %s", product_name, error
        )

    return data
