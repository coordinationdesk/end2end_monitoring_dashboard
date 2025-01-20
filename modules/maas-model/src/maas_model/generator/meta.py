"""Basic meta for maas-model"""

import dataclasses
import json
import logging
import os
from typing import List, Set


@dataclasses.dataclass
class FieldMeta:
    """
    dataclass for field metadata

    may have additionnal argument later
    """

    name: str

    type_name: str

    properties: List["FieldMeta"]


# pylint: disable=R0902
# meta has necessarly lot of attributes
class ModelClassMeta:
    """Stores meta data to generate the class"""

    RAW_DATA_PREFIX = "raw-data-"

    RAW_DATA_FIELDS = ("ingestionTime", "reportName")

    INDEX_SUFFIX = "_template.json"

    def __init__(self, path):
        if not path.endswith(self.INDEX_SUFFIX):
            raise ValueError(
                f"{path} is not a file name ending with {self.INDEX_SUFFIX}"
            )

        self.path = path

        self.index_name = os.path.basename(path)[: -len(self.INDEX_SUFFIX)]

        self.is_raw_data = self.index_name.startswith(self.RAW_DATA_PREFIX)

        if self.is_raw_data:
            self.base_class_str = self.index_name[len(self.RAW_DATA_PREFIX) :]
        else:
            self.base_class_str = self.index_name

        # default class name
        self.class_name = "".join(
            [token.capitalize() for token in self.base_class_str.split("-")]
        )

        self.partition_field = None

        self.partition_format = None

        self.fields = []

        self.field_names = []

        self.field_types = set()

    def add_field(self, parent: List[FieldMeta], name: str, prop: dict) -> None:
        """
        Add a field to a class meta

        Args:
            parent (list): _description_
            name (_type_): _description_
            prop (_type_): _description_
        """
        # camel case transform
        type_name = "".join(word.title() for word in prop["type"].split("_"))
        # inspect recursively sub properties on object type
        properties: list = []
        if type_name == "Object":
            for inner_name, inner_prop in prop["properties"].items():
                self.add_field(properties, inner_name, inner_prop)

        parent.append(FieldMeta(name, type_name, properties))

        self.field_types.add(type_name)

    def load(self) -> None:
        """load the index  template file"""
        with open(self.path, encoding="UTF-8") as tpl_fp:
            logging.info("Processing %s", self.path)
            tpl = json.load(tpl_fp)

        if "_meta" in tpl["mappings"]:
            meta = tpl["mappings"]["_meta"]
            self.partition_field = meta.get("partition_field")
            self.partition_format = meta.get("partition_format")
            self.class_name = meta.get("class_name", self.class_name)

        if "properties" in tpl["mappings"]:
            for name, prop in tpl["mappings"]["properties"].items():
                self.add_field(self.fields, name, prop)

                self.field_names.append(name)

        if self.partition_field and (
            (
                isinstance(self.partition_field, str)
                and not self.partition_field in self.field_names
            )
            or (
                isinstance(self.partition_field, list)
                and not set(self.partition_field).issubset(set(self.field_names))
            )
        ):
            raise ValueError(
                f"Partition field { self.partition_field} "
                f"does not exist in {self.index_name}"
            )

    @property
    def es_types(self) -> Set:
        """
        return the es field types used by the class.

        Omit Date because replaced by ZuluDate !
        """
        return self.field_types - {"Date"}


# pylint: enable=R0902
