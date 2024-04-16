from collections.abc import Iterable
import dataclasses
import fnmatch
import typing

from functools import cached_property

from maas_model import MAASRawDocument

from maas_collector.rawdata import extractor


@dataclasses.dataclass
class FileCollectorConfiguration:
    """
    Configuration for data collection

    Args:
        model (Document): opensearchpy.Document class implementation to store the
            extracted data.
        extractor (BaseExtractor): extractor instance.
        force_update (bool): overwrite existing data in database. Default to False, means error
            for duplicates
        id_field (str, list or callable): primary key, single field name or list
    """

    model: MAASRawDocument

    id_field: typing.Any

    extractor: extractor.base.BaseExtractor

    routing_key: str

    model_meta: dict

    force_update: bool = False

    file_pattern: str = None

    interface_name: str = ""

    file_routing_key: str = ""

    no_probe: bool = False

    store_meta: list = None

    @cached_property
    def name(self) -> str:
        """get the document class name, useful for logs"""
        return f"{self.model_name}Configuration"

    @cached_property
    def model_name(self) -> str:
        """get the model name"""
        if isinstance(self.model, str):
            model_name = self.model
        elif self.model:
            model_name = self.model.__name__
        else:
            model_name = "NoneType"
        return model_name

    def get_id_func(self) -> typing.Callable[[dict], str]:
        """build a callable to generate a unique identifier for a data extract dict

        Raises:
            ValueError: if no parameter can determine how to generate an id

        Returns:
            typing.Callable[[dict], str]: callable that generate a unique identifier
        """
        func = None
        # create a unique identifier getter
        if isinstance(self.id_field, str):
            # single key value

            def get_id_from_extract(data_extract):
                if not self.id_field in data_extract:
                    raise ValueError(
                        f"Field '{self.id_field}' missing in {data_extract}"
                    )
                return data_extract[self.id_field]

            func = get_id_from_extract
        elif callable(self.id_field):
            # lambda or function
            func = self.id_field
        elif isinstance(self.id_field, Iterable):
            # composite key
            func = extractor.get_hash_func(*self.id_field)
        else:
            raise ValueError(
                f"Bad id_field value in {self.name}: {repr(self.id_field)}"
            )
        return func

    def filename_match(self, name: str) -> bool:
        """Check if a filename matches the configuration

        Args:
            name ([str]): name of a file

        Returns:
            bool: True if the file is ok to be processed by the configuration extractor
        """
        if self.file_pattern:
            return fnmatch.fnmatch(name, self.file_pattern)
        return False
