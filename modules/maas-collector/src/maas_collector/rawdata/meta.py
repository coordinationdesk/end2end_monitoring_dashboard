"""

Tools for meta data
"""
import json
import logging
import os


class IngestionMeta:
    """

    Encapsulate logic about file metadata
    """

    SUFFIX = "-maas-meta.json"

    def __init__(self, config, path=""):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.config = config

        if path and self.has_meta_file(path):
            self.load_meta(path)
        else:
            self.meta_dict = {}

    def load_meta(self, path: str):
        """
        Fill meta_dict with a json file content

        Args:
            path (str): path to an file to ingest
        """
        meta_path = self.get_meta_path(path)

        self.logger.info("Loading metadata: %s", meta_path)

        with open(meta_path, encoding="utf-8") as meta_fd:
            self.meta_dict = json.load(meta_fd)

    def populate(self, document_dict: dict):
        """
        Fill document dict with loaded meta

        Args:
            document_dict (dict): elastic search document dict
        """

        document_dict["_source"].update(self.meta_dict)

    def update(self, document_dict: dict):
        """Update meta data from a document dict

        Args:
            document_dict (dict): a full blown document
        """
        if not self.config.store_meta:
            self.logger.warning("No meta to store for configuration")
            return

        self.meta_dict.update(
            {key: document_dict["_source"].get(key) for key in self.config.store_meta}
        )

    @classmethod
    def get_meta_path(cls, path: str) -> str:
        """return the path of a meta data file

        Args:
            path (str): file path

        Returns:
            str: meta data path
        """
        return f"{path}{cls.SUFFIX}"

    @classmethod
    def has_meta_file(cls, path: str) -> bool:
        """
        Tell if an entry path has a meta data file

        Args:
            path (str): file to ingest

        Returns:
            bool: True if a meta data file exists
        """
        return os.path.isfile(cls.get_meta_path(path))

    def dump(self, path: str):
        """
        Store meta data to file (adds suffix)

        Args:
            path (str): ingested file path
        """
        meta_path = self.get_meta_path(path)

        with open(meta_path, "w", encoding="utf-8") as meta_fd:
            self.logger.debug("Saving meta data %s to %s", self.meta_dict, meta_path)
            json.dump(self.meta_dict, meta_fd, indent=4)
