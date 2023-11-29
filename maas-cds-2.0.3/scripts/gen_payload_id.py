#!/usr/bin/env python3

"""
debug tool to generate raw identifier list

"""


import csv
import datetime
import hashlib
import os
import json
import sys

INTERFACES = [
    "PRIP_S2B_CAPGEMINI",
    "PRIP_S1B_DLR",
    "PRIP_S3A_ACRI",
    "LTA_CloudFerro",
    "LTA_Acri",
    "PRIP_S3_Legacy",
    "LTA_Exprivia_S3",
    "PRIP_S3B_SERCO",
    "PRIP_S1_Legacy",
    "PRIP_S2A_ATOS",
    "PRIP_S2_Legacy_2",
    "LTA_Werum",
    "PRIP_S2_Legacy_1",
    "DD_DHUS",
]


def datetime_to_zulu(datetime_object: datetime.datetime) -> str:
    """Format a dateime object to ZULU format

    Args:
        datetime_object (datetime.datetime): datetime to format

    Returns:
        str: zulu formatted string
    """
    if datetime_object is None:
        return None
    return datetime_object.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def get_product_class(interface):
    "generate DAO class name from interface name"
    return f"{interface.split('_')[0].capitalize()}Product"


def gen_id(interface, name):
    "identifier generation"
    md5 = hashlib.md5()
    for value in (interface, name):
        md5.update(value.encode())
    return md5.hexdigest()


if __name__ == "__main__":

    if len(sys.argv) != 3:
        basename = os.path.basename(__file__)
        print(
            f"""Usage:
        {basename} INTERFACE_NAME CSV_PATH

        {basename} INTERFACE_NAME PRODUCT_NAME
        """
        )
        sys.exit(1)

    interface_name = sys.argv[1]

    if not interface_name in INTERFACES:
        INTERFACES.sort()
        print(
            f"""Unknown interface: {interface_name}

Available interfaces: {" ".join(INTERFACES)}
"""
        )
        sys.exit(1)

    if os.path.isfile(sys.argv[2]):

        ids = []

        with open(sys.argv[2], encoding="UTF-8") as csv_fd:
            for csv_dict in csv.DictReader(csv_fd):
                ids.append(gen_id(interface_name, csv_dict["name"]))

        payload = {
            "document_class": get_product_class(interface_name),
            "document_ids": ids,
            "date": datetime_to_zulu(datetime.datetime.utcnow()),
        }

        print(json.dumps(payload, indent=4))

    else:

        print(gen_id(interface_name, sys.argv[2]))
