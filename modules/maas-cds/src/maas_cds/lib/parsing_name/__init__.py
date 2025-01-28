"""data extraction from product name"""

from maas_cds.lib.parsing_name.parsing_name_s1 import extract_data_from_product_name_s1
from maas_cds.lib.parsing_name.parsing_name_s2 import extract_data_from_product_name_s2
from maas_cds.lib.parsing_name.parsing_name_s3 import extract_data_from_product_name_s3
from maas_cds.lib.parsing_name.parsing_name_s5 import extract_data_from_product_name_s5

import re

EXTRACT_FUNC_DICT = {
    "S1": extract_data_from_product_name_s1,
    "S2": extract_data_from_product_name_s2,
    "S3": extract_data_from_product_name_s3,
    "S5": extract_data_from_product_name_s5,
}

# white listing shall allow 'mission'_ or 'satellite' prefix, i.e. :
# S1_, S2_, S3_, S5_
# S1A, S1B, S2A, S2B, S3A, S3B, S5P
# so test products, like for DAS, are not parsed with some curious satellite like S10

PREFIX_WHITE_LIST = (
    "S1_",
    "S2_",
    "S3_",
    "S5_",
    "S1A",
    "S1B",
    "S1C",
    "S1D",
    "S2A",
    "S2B",
    "S2C",
    "S3A",
    "S3B",
    "S5P",
)

DEFAULT_S5P_DICT = {"mission": "S5", "satellite_unit": "S5P"}

CUSTOM_REGEX_DICT = [
    (
        "^NISE_SSMISF18_[0-9]{8}.HDFEOS$",
        {**DEFAULT_S5P_DICT, "product_type": "AUX_NISE"},
    ),
    ("^bulletinb-[0-9]{3}.txt$", {**DEFAULT_S5P_DICT, "product_type": "AUX_IERS_B"}),
    ("^bulletinc-[0-9]{3}.txt$", {**DEFAULT_S5P_DICT, "product_type": "AUX_IERS_C"}),
    (
        "^JRR-CloudMask_[a-zA-Z0-9_]{4}_[a-zA-Z0-9_]{3}_[a-zA-Z0-9_]{16}_[a-zA-Z0-9_]{16}_[a-zA-Z0-9_]{16}.(tar|nc)$",
        {**DEFAULT_S5P_DICT, "product_type": "VIIRS_CM"},
    ),
    (
        "^JRR-CloudPhase_[a-zA-Z0-9_]{4}_[a-zA-Z0-9_]{3}_[a-zA-Z0-9_]{16}_[a-zA-Z0-9_]{16}_[a-zA-Z0-9_]{16}.(tar|nc)$",
        {**DEFAULT_S5P_DICT, "product_type": "VIIRS_CP"},
    ),
    (
        "^JRR-CloudDCOMP_[a-zA-Z0-9_]{4}_[a-zA-Z0-9_]{3}_[a-zA-Z0-9_]{16}_[a-zA-Z0-9_]{16}_[a-zA-Z0-9_]{16}.(tar|nc)$",
        {**DEFAULT_S5P_DICT, "product_type": "VIIRS_DCOMP"},
    ),
    (
        "^JRR-CloudHeight_[a-zA-Z0-9_]{4}_[a-zA-Z0-9_]{3}_[a-zA-Z0-9_]{16}_[a-zA-Z0-9_]{16}_[a-zA-Z0-9_]{16}.(tar|nc)$",
        {**DEFAULT_S5P_DICT, "product_type": "VIIRS_CTH"},
    ),
    (
        "^GMODO_[a-zA-Z0-9_]{3}_[a-zA-Z0-9_]{9}_[a-zA-Z0-9_]{8}_[a-zA-Z0-9_]{8}_[a-zA-Z0-9_]{6}_[a-zA-Z0-9_]{21}_[a-zA-Z0-9_]{4}_[a-zA-Z0-9_]{3}.h5$",
        {**DEFAULT_S5P_DICT, "product_type": "VIIRS_L1B_GEO"},
    ),
    (
        "^SVM[0-9]{2}_[a-zA-Z0-9_]{3}_[a-zA-Z0-9_]{9}_[a-zA-Z0-9_]{8}_[a-zA-Z0-9_]{8}_[a-zA-Z0-9_]{6}_[a-zA-Z0-9_]{21}_[a-zA-Z0-9_]{4}_[a-zA-Z0-9_]{3}.h5$",
        {**DEFAULT_S5P_DICT, "product_type": "VIIRS_L1B_RR"},
    ),
]


def extract_data_from_product_name(product_name):
    """extract data from product name"""
    # white listing first
    if not product_name[:3] in PREFIX_WHITE_LIST:
        for regex_schema, regex_data_dict in CUSTOM_REGEX_DICT:
            if re.match(regex_schema, product_name):
                return regex_data_dict.copy()
        return {}

    func = EXTRACT_FUNC_DICT.get(product_name[:2], lambda name: {})

    return func(product_name)
