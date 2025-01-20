"""Generate mdoel definition for maas-collector"""

import json
import logging
import sys

from maas_model.generator.meta import ModelClassMeta

IGNORED_FIELD_NAMES = ["ingestionTime", "reportName"]


def generate_class(meta: ModelClassMeta) -> dict:
    """generate collector compatible model dictionnary"""
    model = {"index": meta.index_name, "name": meta.class_name, "fields": []}

    if meta.partition_field:
        model["partition_field"] = meta.partition_field
    else:
        logging.info("no partition_field defined for index: %s", meta.index_name)

    if meta.partition_format:
        model["partition_format"] = meta.partition_format

    for field in meta.fields:
        if meta.is_raw_data and field.name in meta.RAW_DATA_FIELDS:
            continue
        model["fields"].append({"name": field.name, "type": field.type_name})

    return model


def generate(*path_list: str) -> str:
    """generate the code of a module containing generated documents
    from index template files

    Args:
        path_list (list[str]): list of index template path

    Returns:
        str: the json file content
    """
    base_dict: dict = {"models": []}

    class_metas = [ModelClassMeta(path) for path in path_list]

    for meta in class_metas:
        meta.load()
        base_dict["models"].append(generate_class(meta))

    return json.dumps(base_dict, indent=4)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(generate(*sys.argv[1:]))
