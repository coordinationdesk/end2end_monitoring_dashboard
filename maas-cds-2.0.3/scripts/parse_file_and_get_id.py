#!/usr/bin/env python3

import csv

import requests
import json
import sys


# Usage: parse_file_and_get_id.py p a (p for preprod and a for acri) need payload/notacri.csv

document_class = {
    "LTA": "LtaProduct",
    "PRIP": "PripProduct",
    "DD": "DdProduct",
}


def find_matching_pattern(value, validator, env="LOCAL", index="LTA"):
    envs = {
        "LOCAL": "http://localhost:9200",
        "PREPROD": "http://monitoring.omcs.telespazio.corp/search",
    }

    indexes = {"LTA": "raw-data-lta-product", "PRIP": "raw-data-prip-product"}

    url = f"{envs.get(env)}/{indexes.get(index)}/_search"

    payload = json.dumps(
        {
            "query": {
                "match": {
                    "product_name": value,
                    # "name": value,
                }
            },
            "fields": [
                "_id",
                "interface_name",
                "http.response.*",
                {"field": "@timestamp", "format": "epoch_millis"},
            ],
            "_source": False,
        }
    )
    headers = {
        "Authorization": "Basic YWRtaW46YWRtaW4=",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    res = response.json()

    for matched in res["hits"]["hits"]:
        if validator(matched["fields"]["interface_name"]):
            return matched["_id"]


def format_rabbit_payload(ids, index):
    print(
        "{"
        f'"document_class": "{document_class.get(index)}",'
        f'"document_ids": {json.dumps(ids)},'
        '"date": "2022-02-11T13:56:55.730Z"'
        "}"
    )


seek_field = "name"

ids = []
nb_ids = 0
skip_first = True
key_field = None

exprivia_validator = (
    lambda x: "LTA_Exprivia_S1" in x or "LTA_Exprivia_S2" in x or "LTA_Exprivia_S3" in x
)

werum_validator = lambda x: "LTA_Werum" in x
acri_validator = lambda x: "LTA_Acri" in x
ferro_validator = lambda x: "LTA_CloudFerro" in x

prip_validator = lambda x: (
    lambda x: "PRIP_S1_Legacy" in x or "PRIP_S2_Legacy" in x or "PRIP_S3_Legacy" in x
)

validator_dict = {
    "LTA_WERUM": werum_validator,
    "LTA_ACRI": acri_validator,
    "LTA_CLOUDFERRO": ferro_validator,
    "LTA_EXPRIVIA": exprivia_validator,
    "PRIP": prip_validator,
}

filepath_dict = {
    "LTA_WERUM": "payload/notwerum.csv",
    "LTA_ACRI": "payload/notacri.csv",
    "LTA_CLOUDFERRO": "payload/notcloudferro.csv",
    "LTA_EXPRIVIA": "payload/notexprivia.csv",
    "PRIP": "payload/notprip.csv",
}

alias_interface = {
    "w": "LTA_WERUM",
    "a": "LTA_ACRI",
    "c": "LTA_CLOUDFERRO",
    "e": "LTA_EXPRIVIA",
    "p": "PRIP",
}

alias_env = {"p": "PREPROD", "l": "LOCAL"}

u_env = sys.argv[1]
u_interface = sys.argv[2]

interface_name = alias_interface.get(u_interface)
filepath = filepath_dict.get(interface_name)
current_validator = validator_dict.get(interface_name)
env = alias_env.get(u_env)
index = interface_name.split("_")[0]

with open(filepath, newline="") as csvfile:
    spamreader = csv.reader(csvfile, delimiter=",")
    for row in spamreader:
        if skip_first:
            key_field = row.index(seek_field)
            skip_first = False
            print(env, index, interface_name)
            continue
        if len(row) - 1 > key_field:
            id_doc = find_matching_pattern(
                row[key_field], current_validator, env, index
            )
            if id_doc:
                nb_ids += 1
                # print(id_doc)
            # print(f"Found {nb_ids}")
            ids.append(id_doc)


format_rabbit_payload(ids, index)
