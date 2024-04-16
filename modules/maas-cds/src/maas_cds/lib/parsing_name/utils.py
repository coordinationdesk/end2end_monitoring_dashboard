"""Utils function for parsing name"""

import os
import re
import typing

STRIPPED_EXTENSIONS = [".SAFE", ".SEN3", ".EOF", ".nc", ".h5", ".RAW"]
COMPRESION_EXTENSIONS = [".zip", ".tar", ".tgz"]

STRIPPED_EXTENSIONS_REGEX = "|".join(
    [f"\{STRIPPED_EXT}$" for STRIPPED_EXT in STRIPPED_EXTENSIONS]
)

TIMELINESS_NULL_VALUE = "_"

PRODUCT_LEVEL_MISSING_VALUE = "___"

DATATAKE_ID_MISSING_VALUE = "______"


def remove_extension_from_product_name(product_name):
    """Remove common extension from the given product_name

    Args:
        product_name (str): the product name that we want to remove common extension

    Returns:
        str: the given product_name whithout extension
    """
    product_without_file_extension = os.path.splitext(product_name)[0]
    return re.sub(STRIPPED_EXTENSIONS_REGEX, "", product_without_file_extension)


def normalize_product_name(name: str) -> str:
    """
    Normalize a product name so S2 container will be added .tar extension.

    Names with existing extension will be kept unmodified

    Args:
        name (str): product name

    Returns:
        str: normalized product name
    """
    if name[:2] == "S2":
        base, ext = os.path.splitext(name)
        # without extension, S2 containers end with digits
        if ext.replace(".", "").isdigit():
            # no functionnal extension, add .tar as DD publishes only container
            name += ".tar"
    return name


def normalize_product_name_list(name_list: typing.List[str]) -> typing.List[str]:
    """
    Normalize a list of product names so S2 container will be added .tar extension.

    Names with existing extension will be kept unmodified

    Args:
        name_list (list): list to normalize

    Returns:
        list: normalized list
    """
    if name_list is None:
        return []
    return [normalize_product_name(name) for name in name_list]


def generate_publication_names(product_name: str) -> list[str]:
    """Generate variations of product names extension wise
    ex: product_1.SAFE.zip -> product_1.SAFE.zip, product_1.SAFE, product_1

    Args:
        product_names ([str]): product name with extensions

    Returns:
        list[str]: product name variations
    """

    products_list = set()
    for short_product_name in [
        remove_extension_from_product_name(product_name.rsplit(".", 1)[0]),
    ]:
        products_list.add(short_product_name)
        for extension in STRIPPED_EXTENSIONS:
            products_list.add(short_product_name + extension)

            for compression in COMPRESION_EXTENSIONS:
                products_list.add(short_product_name + compression)
                products_list.add(short_product_name + extension + compression)

    return products_list
