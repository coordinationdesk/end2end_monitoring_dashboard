"""
A engine to automate attribute copy from raw data to consolidated data
"""
from typing import Optional, List, Set

from maas_model import MAASDocument, MAASRawDocument

from maas_engine.engine.rawdata import RawDataEngine


class ReplicatorEngine(RawDataEngine):
    """
    An engine that simply copy raw data attributes to consolidated documents

    Requires a target model name in the configuration for a stand-alone usage, or add
    it in the call of the parent constructor in case of inheritance.

    Input type is not necessary because if is expressed in the collector payload.


    Possible evolution ideas: include attribute list, field mapping
    """

    ENGINE_ID = "CONSOLIDATE_REPLICATE"

    EXCLUDE_FIELDS: Set[str] = {"ingestionTime"}

    # pylint: disable=R0913
    # legit: constructors have many argument for configuration
    def __init__(
        self,
        args=None,
        send_reports=True,
        min_doi=None,
        chunk_size=0,
        target_model: Optional[str] = None,
        exclude_fields: Optional[List[str]] = None,
        include_fields: Optional[List[str]] = None,
    ):
        super().__init__(
            args, send_reports=send_reports, min_doi=min_doi, chunk_size=chunk_size
        )

        if not target_model:
            raise ValueError(
                f"target_model for {self.__class__.__name__}"
                " is missing in configuration file"
            )

        self.include_fields = include_fields

        # volontary affectation to an instance attribute instead of class attribute
        # to be cleaner in the symbol resolution

        # pylint: disable=C0103
        self.CONSOLIDATED_MODEL = self.get_model(target_model)
        # pylint: enable=C0103

        self.exclude_fields = self.EXCLUDE_FIELDS

        if exclude_fields:
            # add more fields to exclude
            self.exclude_fields |= set(exclude_fields)

        self._fields: List[str] = []

    # pylint: enable=R0913

    def get_consolidated_id(self, raw_document: MAASRawDocument) -> str:
        """
        Consolidated id is the same as raw data

        Args:
            raw_document (MAASRawDocument): raw document

        Returns:
            str: consolidated identifier
        """
        return raw_document.meta.id

    def consolidate(
        self, raw_document: MAASRawDocument, document: MAASDocument
    ) -> MAASDocument:
        """
        Copy all attributes from raw document to consolidated document

        Args:
            raw_document (MAASRawDocument): raw document
            document (MAASDocument): document to consolidate

        Returns:
            MAASDocument: consolidated document
        """
        if not self._fields:
            self._fields = [
                name
                for name in MAASDocument.get_initial_field_names(raw_document.__class__)
                if name not in self.exclude_fields
            ]
            if self.include_fields:
                self._fields += self.include_fields

        for name in self._fields:
            setattr(document, name, getattr(raw_document, name))

        return document
