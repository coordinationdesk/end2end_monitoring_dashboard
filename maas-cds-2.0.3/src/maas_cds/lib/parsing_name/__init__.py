"""data extraction from product name"""
from maas_cds.lib.parsing_name.parsing_name_s1 import extract_data_from_product_name_s1
from maas_cds.lib.parsing_name.parsing_name_s2 import extract_data_from_product_name_s2
from maas_cds.lib.parsing_name.parsing_name_s3 import extract_data_from_product_name_s3
from maas_cds.lib.parsing_name.parsing_name_s5 import extract_data_from_product_name_s5

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
    "S2A",
    "S2B",
    "S3A",
    "S3B",
    "S5P",
)


def extract_data_from_product_name(product_name):
    """extract data from product name"""
    # white listing first
    if not product_name[:3] in PREFIX_WHITE_LIST:
        return {}

    func = EXTRACT_FUNC_DICT.get(product_name[:2], lambda name: {})

    return func(product_name)
