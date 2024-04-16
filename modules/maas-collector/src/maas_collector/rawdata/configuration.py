"""Base classes and factory functions for mass_collector"""
import os
import json
import logging

import opensearchpy

from maas_model import MAASRawDocument, ZuluDate

from maas_collector.rawdata import extractor

LOGGER = logging.getLogger(__name__)

# store all the declared module to allow name resolution after all files
# have been loaded. Would have been better in more OO way, but 'no Ferrari'
MODEL_DICT = {}


def build_model_class(meta: dict) -> MAASRawDocument:
    """opensearch document class factory

    Args:
        meta (dict): meta-information from configuration file

    Returns:
        model.MAASRawDocument: Document class object
    """
    # populate document class attribute dictionnary using opensearchpy types only
    # maybe later add defaults and other raw database properties
    class_dict = {}
    for field_meta in meta["fields"]:
        args = {}
        # replace Date fields by ZuluDate
        if field_meta["type"] == "Date":
            class_obj = ZuluDate
        else:
            try:
                class_obj = getattr(opensearchpy, field_meta["type"])
            except AttributeError:
                LOGGER.critical(
                    "%s: '%s' is not a data type class name of opensearchpy module",
                    meta["name"],
                    field_meta["type"],
                )
                raise
        class_dict[field_meta["name"]] = class_obj(**args)

    # Inner class to declare opensearch index name
    class_dict["Index"] = type("Index", (object,), {"name": meta["index"]})

    # Partitionning optionnal settings
    if "partition_field" in meta:
        if meta["partition_field"] != "ingestionTime":
            # check if partition field is a date field
            assert isinstance(class_dict[meta["partition_field"]], ZuluDate)

        class_dict["_PARTITION_FIELD"] = meta["partition_field"]

    if "partition_format" in meta:
        # override yearly default
        class_dict["_PARTITION_FIELD_FORMAT"] = meta["partition_format"]

    # make search() works with partitions
    class_dict["_matches"] = classmethod(
        lambda cls, hit: hit["_index"].startswith(f"{meta['index']}-")
    )

    # return new document class
    model_class = type(meta["name"], (MAASRawDocument,), class_dict)

    add_model(model_class)

    return model_class


def build_extractor(meta: dict) -> extractor.base.BaseExtractor:
    """build extractor instance from meta data

    Args:
        meta (dict): meta-information from configuration file

    Returns:
        extractor.BaseExtractor: Configured instance of an extrator
    """
    try:
        class_obj = getattr(extractor, meta["class"])
    except AttributeError:
        LOGGER.critical("Extractor class not found: %s", meta["class"])
        raise

    args = {}
    if "args" in meta:
        args.update(meta["args"])
    if "converter_map" in meta:
        args["converter_map"] = meta["converter_map"]
    return class_obj(**args)


def build_collector_configuration(meta: dict, configuration_class):
    """build CollectorConfiguration instance from json dict

    Args:
        meta (dict): configuration meta information

    Returns:
        CollectorConfiguration: build configuration instance
    """

    # copy meta args to leave argument untouched
    args = meta.copy()

    # store model meta for later usage like date convertion

    if "model" in meta:
        # create opensearchpy model class
        if isinstance(meta["model"], dict):
            args["model_meta"] = meta["model"].copy()
            args["model"] = build_model_class(meta["model"])
        else:
            args["model_meta"] = meta["model"]
            LOGGER.debug("Post-poned model resolution: %s", meta["model"])
    else:
        LOGGER.debug("No model declared in : %s", meta)
        args["model"] = None
        args["model_meta"] = None

    if "extractor" in meta:
        # instanciate the extractor
        args["extractor"] = build_extractor(args["extractor"])
    else:
        LOGGER.debug("No extractor declared in : %s", meta)
        args["extractor"] = None

    # instanciate the Configuration instance
    configuration_keys = set(configuration_class.__dataclass_fields__)

    configuration = configuration_class(
        **{name: value for name, value in args.items() if name in configuration_keys}
    )

    extra_keys = set(args) - configuration_keys

    if extra_keys:
        LOGGER.debug("Ignored configuration keys: %s", extra_keys)

    LOGGER.debug(
        "Configuration loaded: %s",
        configuration.name,
    )

    return configuration


def load_json(path: str, configuration_class):
    """load a list of collector configuration from a json file

    Args:
        path (str): path a json file

    Returns:
        typing.List[CollectorConfiguration]: list of configuration instances
    """
    LOGGER.info("Loading configuration file: %s", path)
    with open(path, encoding="UTF-8") as conf_fd:
        json_dict = json.load(conf_fd)

        if "collectors" in json_dict:
            for conf_meta in json_dict["collectors"]:
                try:
                    yield build_collector_configuration(conf_meta, configuration_class)
                except Exception as error:
                    LOGGER.critical("Cannot instanciate configuration: %s", conf_meta)
                    raise error

        if "models" in json_dict:
            for model_meta in json_dict["models"]:
                LOGGER.debug("Registering model %s", model_meta["name"])
                build_model_class(model_meta)


def get_model(name):
    """get a DAO class

    Args:
        name (str): the name of the class

    Returns:
        class: DAO class
    """
    if not name in MODEL_DICT:
        LOGGER.error("No model registed: %s", name)
    return MODEL_DICT[name]


def add_model(model_class):
    """register a new model class

    Args:
        name (str): class name
        model_class (class object): implementation

    Raises:
        ValueError: if class is already registered
    """
    if model_class.__name__ in MODEL_DICT:
        LOGGER.warning("Model %s is already defined", model_class.__name__)

    MODEL_DICT[model_class.__name__] = model_class


def find_configurations(directory_path: str, ext=".json") -> list[str]:
    """Look up a directory recursively for configuration files

    Args:
        directory_path (str): directory
        ext (str, optional): configuration extension. Defaults to ".json".

    Returns:
        list[str]: _description_
    """
    result = []
    for root, dirs, files in os.walk(directory_path):
        # filter out hidden files and dirs
        files = [name for name in files if not name[0] == "."]

        dirs[:] = [name for name in dirs if not name[0] == "."]

        result.extend(
            [
                os.path.join(root, path)
                for path in files
                if os.path.splitext(path)[1] == ext
            ]
        )

    return result
