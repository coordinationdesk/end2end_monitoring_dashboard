"""Generate DAO Python code from index templates"""

import datetime
import logging
from typing import List, Set, Type
import sys


from black import format_str, FileMode

from maas_model.generator.meta import FieldMeta, ModelClassMeta


# pylint: disable=R0903
# No method: just hold namespace
class PythonCodeTemplate:
    """A namespace that contains"""

    HEADER = '''# pylint: skip-file
"""
DA0 classes generated from index templates.

**DO NOT EDIT, ONLY INHERIT !**

Generated date: {date}

Generated from:
{source_files}
"""

from opensearchpy import {field_classes}, InnerDoc

from maas_model import {base_classes}, ZuluDate

__all__ = [ {all_classes} ]

'''

    CLASS_TPL = '''
class {class_name}({base_class}):
    """
    Mapping class for index: {index_name}
    
    Generated from: {path}
    """

    class Index:
        "inner class for DSL"
        name = "{index_name}"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("{index_name}-")

'''

    INNER_CLASS_TPL = '''
class {class_name}(InnerDoc):
    """
    Inner document class for parent class: {parent_class_name}

    Generated from property: {prop}
    """

'''
    INDENT = " " * 4

    ATTR_TPL = (
        INDENT
        + """{name} = {type_name}()

"""
    )
    INNER_ATTR_TPL = (
        INDENT
        + """{name} = Object({type_name})

"""
    )


# pylint: enable=R0903


class ModelGenerator:
    """

    A class that generate DAO code using opensearchpy types
    """

    def __init__(self, *path_list: str, template: Type[PythonCodeTemplate]):
        self.path_list = path_list
        self.template: Type[PythonCodeTemplate] = template
        self.used_base_classes: Set = set()
        self.inner_doc_classes: List = []

    def generate(self) -> str:
        """generate the code of a module containing generated opensearchpy documents
        from index template files

        Args:
            path_list (list[str]): list of index template path

        Returns:
            str: the module code
        """
        self.used_base_classes.clear()

        es_types: Set[str] = set()

        class_metas = [ModelClassMeta(path) for path in self.path_list]

        class_metas.sort(key=lambda x: x.class_name)

        class_code = []

        for meta in class_metas:
            meta.load()
            es_types = es_types | meta.es_types
            class_code.append(self.generate_class(meta))

        all_classes = sorted(
            set(
                [f'"{meta.class_name}"' for meta in class_metas]
                + [f'"{class_name}"' for class_name in self.inner_doc_classes]
            )
        )

        if len(all_classes) != len(class_metas) + len(self.inner_doc_classes):
            raise ValueError("Duplicated classes")

        module_lines = [
            self.template.HEADER.format(
                field_classes=", ".join(list(sorted(es_types))),
                all_classes=", ".join(all_classes),
                date=datetime.datetime.utcnow().isoformat(),
                source_files="\n".join(
                    [self.template.INDENT + f"- {path}" for path in self.path_list]
                ),
                base_classes=", ".join(sorted(self.used_base_classes)),
            )
        ]

        for meta in class_metas:
            module_lines.append(self.generate_class(meta))

        return "".join(module_lines)

    def generate_class(self, meta: ModelClassMeta) -> str:
        """generate the code of the class"""

        if meta.is_raw_data:
            base_class = "MAASRawDocument"
        else:
            base_class = "MAASDocument"

        self.used_base_classes.add(base_class)

        class_lines = [
            self.template.CLASS_TPL.format(
                class_name=meta.class_name,
                index_name=meta.index_name,
                path=meta.path,
                base_class=base_class,
            )
        ]
        if meta.partition_field:
            if isinstance(meta.partition_field, str):
                class_lines.append(
                    self.template.INDENT
                    + f'_PARTITION_FIELD = "{meta.partition_field}"\n\n'
                )
            elif isinstance(meta.partition_field, list):
                class_lines.append(
                    self.template.INDENT
                    + f"_PARTITION_FIELD = {meta.partition_field}\n\n"
                )
            else:
                raise TypeError("Unsupported type partition field")

        if meta.partition_format:
            class_lines.append(
                self.template.INDENT
                + f'_PARTITION_FIELD_FORMAT = "{meta.partition_format}"\n\n'
            )

        meta.fields.sort(key=lambda x: x.name)

        ordered_lines = []

        for field in meta.fields:
            if field.name in meta.RAW_DATA_FIELDS:
                continue

            attributes_lines, sub_class_lines = self.generate_attributes(
                meta.class_name, field
            )
            class_lines.extend(attributes_lines)

            ordered_lines.extend(sub_class_lines)

        ordered_lines.extend(class_lines)
        return "".join(ordered_lines)

    def generate_attributes(self, class_name: str, field: FieldMeta):
        """
        generate lines for attributes of class_name

        complete ordered_lines with sub class generated as dependencies of attributes
        with type 'object'
        """
        attributes_lines: List[str] = []
        sub_class_lines: List[str] = []
        ordered_lines: List[str] = []

        if field.type_name == "Date":
            type_name = "ZuluDate"
            attributes_lines.extend(
                self.template.ATTR_TPL.format(name=field.name, type_name=type_name)
            )
        elif field.type_name == "Object":
            inner_class_name = "".join(word.title() for word in field.name.split("_"))

            type_name = class_name + inner_class_name

            self.inner_doc_classes.append(type_name)

            # attributes of current class
            attributes_lines.extend(
                self.template.INNER_ATTR_TPL.format(
                    name=field.name, type_name=type_name
                )
            )

            # sub class header for this object
            sub_class_lines.extend(
                self.template.INNER_CLASS_TPL.format(
                    class_name=type_name, parent_class_name=class_name, prop=field.name
                )
            )
            # sub class attributes for this object
            for inner_field in field.properties:
                sub_attributes_lines, sub_sub_class_lines = self.generate_attributes(
                    type_name, inner_field
                )
                sub_class_lines.extend(sub_attributes_lines)

                ordered_lines.extend(sub_sub_class_lines)

        else:
            attributes_lines.extend(
                self.template.ATTR_TPL.format(
                    name=field.name, type_name=field.type_name
                )
            )

        # insert current sub class atfer recurcive sub classes to respect dependency order
        ordered_lines.extend(sub_class_lines)

        return attributes_lines, ordered_lines


def generate(*path_list: str) -> str:
    """generate code from a list of template

    Returns:
        str: DAO code
    """
    python_generator = ModelGenerator(*path_list, template=PythonCodeTemplate)
    return python_generator.generate()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print(format_str(generate(*sys.argv[1:]), mode=FileMode()))
