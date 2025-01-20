"""Base classes for maas elastic search documents"""

__all__ = ["MAASDocument", "MAASRawDocument"]

import datetime
import logging
from typing import (
    Any,
    Dict,
    FrozenSet,
    Iterable,
    Iterator,
    List,
    Optional,
    Type,
    Self,
    Union,
)


from opensearchpy import (
    AttrList,
    Document,
    Keyword,
    Object,
    Field,
    NotFoundError,
)
from opensearchpy.helpers.response import Response
import opensearchpy.helpers.utils

from maas_model.zulu_date import ZuluDate

# META_FIELDS has no type definition, so mypy triggers error: solution is to get
# the symbol dynamically
META_FIELDS: FrozenSet[str] = getattr(opensearchpy.helpers.utils, "META_FIELDS")


LOGGER = logging.getLogger(__name__)


class MAASDocument(Document):
    """
    Base document for MAAS DAS

    TODO upgrade with compute-engine features
    """

    _PARTITION_FIELD: Union[str, List[str]] = ""

    _PARTITION_FIELD_FORMAT: str = "%Y"

    _INITIAL_FIELDS: Dict[str, Field]

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        # cache attribute list
        cls._INITIAL_FIELDS = cls.get_initial_field_names(cls)

    # pylint: disable=too-few-public-methods
    class Index:
        """stub to override"""

        name = ""

    # pylint: enable=too-few-public-methods

    @classmethod
    def _get_sort(cls) -> List[str] | None:
        """Default sort for search

        Returns:
            List[str]: list of sort rules
        """
        return None

    @property
    def partition_index_name(self) -> str:
        """return the name of the index to store the document depending of the
        partionning rules:
            - no specific setup: year of the ingestion time
            - year of specific field if no format provided
            - formated value of specific field if both provided

        Returns:
            [str]: index name
        """

        index_name = getattr(self, "Index").name

        if not self._PARTITION_FIELD:
            return index_name

        partionned_values = self.partition_field_value

        template_string = self._PARTITION_FIELD_FORMAT

        # Keep retro compatibility with previous way
        if not isinstance(partionned_values, dict):
            template_string = (
                f"{{{self._PARTITION_FIELD}:{self._PARTITION_FIELD_FORMAT}}}"
            )
            partionned_values = {self._PARTITION_FIELD: partionned_values}

        partionned_values = {
            key: value.lower() if isinstance(value, str) else value
            for key, value in partionned_values.items()
        }

        return f"{index_name}-{template_string.format(**partionned_values)}"

    @property
    def partition_field_value(
        self,
    ) -> Any:
        """get the values of the partition field

        Returns:
            datetime.datetime | int | None | list | str : all values of all partition field
        """

        if not self._PARTITION_FIELD:
            return
        elif isinstance(self._PARTITION_FIELD, str):
            return getattr(self, self._PARTITION_FIELD)
        elif isinstance(self._PARTITION_FIELD, list):
            return {field: getattr(self, field) for field in self._PARTITION_FIELD}
        else:
            raise TypeError(
                "Unsupported type of partition %s", type(self._PARTITION_FIELD)
            )

    @property
    def has_partition_field_value(self) -> bool:
        """tell if all partition field has a value

        Returns:
            bool: flag
        """
        # If we haven't partition field it is correct to haven't value
        if not self._PARTITION_FIELD:
            return True
        elif isinstance(self._PARTITION_FIELD, str):
            return getattr(self, self._PARTITION_FIELD, None) is not None
        elif isinstance(self._PARTITION_FIELD, list):
            return all([getattr(self, field) for field in self._PARTITION_FIELD])
        else:
            raise TypeError(
                "Unsupported type of partition %s", type(self._PARTITION_FIELD)
            )

    @classmethod
    def get_by_id(
        cls,
        document_id: str,
        document_index: str | None = None,
        ignore_missing_index=False,
    ) -> Optional["MAASDocument"]:
        """get a document by id in the index or alias

        Args:
            document_id (str): document identifier

        Raises:
            Exception: if there is multiple documents with the same id in the alias

        Returns:
            [MAASRawDocument]: the concrete MAASRawDocument found, or None if not found
        """
        try:

            response: Iterator[MAASDocument | None] = cls.mget_by_ids(
                [document_id], [document_index] if document_index else None
            )

        except ValueError as error:
            LOGGER.warning(
                "Cannot retrieve document %s on alias %s : %s",
                document_id,
                cls.Index.name,
                error.with_traceback,
            )
        except NotFoundError as error:
            if (
                error.status_code == 404
                and error.error == "index_not_found_exception"
                and ignore_missing_index
            ):
                # index may have not been yet initialized, continue so first insert
                # will solve the case
                LOGGER.info(
                    "Search failed: a yearly index for %s have not been yet populated",
                    cls.Index.name,
                )
                return None

            raise

        # add a cardinality check like before ? really necessary ?

        try:
            return next(response)
        except (StopIteration, NotFoundError):
            return None

    @classmethod
    def mget_by_ids(
        cls,
        document_ids: List[str],
        document_indices: List[str] | None = None,
        ignore_missing_index: bool = False,
        log_missing: bool = False,
    ) -> Iterator[Optional["MAASDocument"]]:
        """get documents by id in the alias

        Args:
            document_ids (list): document identifiers
            document_indices (list): document indices

        Raises:
            Exception: if there is multiple documents with the same id in the alias

        Returns:
            [MAASRawDocument]: the concrete MAASRawDocument found, or None if not found
        """

        index = document_indices if document_indices else cls.Index.name

        try:
            max_size = min(len(document_ids) * 2, 10000)
            response: Response = (
                cls.search(index=index)
                .query("ids", values=document_ids)
                .params(
                    version=True,
                    seq_no_primary_term=True,
                    size=max_size,
                )
                .execute()
            )

        except ValueError as error:
            LOGGER.warning(
                "Cannot retrieve documents %s on indices %s : %s",
                document_ids,
                index,
                error.with_traceback,
            )
            raise
        except NotFoundError as error:
            if (
                error.status_code == 404
                and error.error == "index_not_found_exception"
                and ignore_missing_index
            ):
                # index may have not been yet initialized, continue so first insert
                # will solve the case
                LOGGER.info(
                    "Search failed: a yearly index for %s have not been yet populated",
                    index,
                )
                # yield Nones to not break
                for _ in document_ids:
                    yield None

            else:
                raise

        response_dict = {}

        if response.hits.total.value > len(document_ids):
            LOGGER.warning("Anormal usage of mget : find more document than input ids")

        if log_missing and response.hits.total.value < len(document_ids):
            LOGGER.warning(
                "Anormal behaviour of mget : find less document than input ids"
            )

        for document in response:
            if document.meta.id in response_dict:
                LOGGER.error("mget retrieve duplicate _id %s", document)

            response_dict[document.meta.id] = document

        LOGGER.debug(
            "Query %d %s, found %d", len(document_ids), cls, len(response_dict)
        )

        for document_id in document_ids:
            # mimic nice mget behavior:
            # return None if document_id is not found in the indices
            yield response_dict.get(document_id, None)

    def to_bulk_action(
        self, op_type: str | None = None, _id: str | None = None
    ) -> Dict[str, Any]:
        """JSON serialization specific for index - create bulk action

        The JSON include all metadata, this allow bulk operation
        to raise conflict error from seq_no

        Args:
            op_type (str, optional): optional bulk operation. Defaults to None.

        Returns:
            dict: dictionnary suitable to feed bulk
        """
        # handle explicit actions
        if op_type == "delete":
            return {
                "_id": self.meta.id,
                "_index": self.meta.index,
                "_op_type": "delete",
            }
        if hasattr(self, "updateTime"):
            setattr(self, "updateTime", datetime.datetime.now(tz=datetime.timezone.utc))

        if op_type == "create":
            if _id is None:
                new_id = self.meta.id
            else:
                new_id = _id

            return {
                "_id": new_id,
                "_index": self.partition_index_name,
                "_source": self.to_dict(),
                "_op_type": "create",
            }

        # else determine what to do: create update/index

        # use default to dict
        document_dict = self.to_dict(include_meta=True)

        # Determine the op_type
        if op_type is not None:
            document_dict["_op_type"] = op_type

        # extract all metadata
        meta = {"_" + k: self.meta[k] for k in META_FIELDS if k in self.meta}

        # optimistic concurrency control need two more field and can't use _version field
        # for new document some meta aren't present
        if "_seq_no" in meta:
            meta["if_seq_no"] = meta["_seq_no"]

        if "_primary_term" in meta:
            meta["if_primary_term"] = meta["_primary_term"]
            document_dict["_op_type"] = "index"

        elif "_version" in meta:
            # index document again because bulk update does not allow dynamic fields
            document_dict["_op_type"] = "index"

        else:
            # no version: it's a creation
            document_dict["_op_type"] = "create"

        # post processing
        if document_dict["_op_type"] == "create":
            # apply partitionning rule
            document_dict["_index"] = self.partition_index_name

        elif document_dict["_op_type"] == "index" and "_version" in meta:
            # remove version info for update
            del meta["_version"]

        # append metadata to dict
        document_dict |= meta

        return document_dict

    @classmethod
    def get_initial_field_names(
        cls, doc_class: Type["MAASDocument"]
    ) -> Dict[str, Field]:
        """property the list of the field name originaly defined for the document class

        Returns:
            Dict[str, Field]: dictionnary field name -> field instance
        """
        # pylint: disable=protected-access
        return {
            def_tuple[0]: def_tuple[1]
            for def_tuple in doc_class._ObjectBase__list_fields()
        }
        # pylint: enable=protected-access

    def purge_dynamic_fields(self) -> None:
        """remove all fields that don't appear in the initial model definition"""
        MAASDocument._purge_dynamic_fields_from_object(self)

    @classmethod
    def _purge_dynamic_fields_from_object(cls, obj: Self) -> None:
        """
        Remove all fields of an object that don't appear in the initial model definition

        Recurve throug Object tree, this is why it is a class method.

        Args:
            obj (MAASDocument): document to purge
        """

        # listing the attribute names requires bypassing protected access
        # pylint: disable=protected-access

        if hasattr(obj, "_INITIAL_FIELDS"):
            field_names = obj._INITIAL_FIELDS
        else:
            field_names = cls.get_initial_field_names(obj.__class__)

        for attrname in list(obj._d_):
            if attrname not in field_names:
                delattr(obj, attrname)

            elif isinstance(field_names[attrname], Object):
                # recurse through inner document

                # object can hide list (multiple=True)
                if isinstance(getattr(obj, attrname), AttrList):
                    # iter throught all item in list
                    for child in getattr(obj, attrname):
                        cls._purge_dynamic_fields_from_object(child)
                else:
                    # recurse
                    cls._purge_dynamic_fields_from_object(getattr(obj, attrname))

        # pylint: enable=protected-access

    def fill_common_fields(
        self,
        document: Self,
        include: Optional[Iterable[str]] = None,
        exclude: Optional[Iterable[str]] = None,
    ):
        """
        Copy common attributes from a document to current instance

        Args:
            document (Document): document to copy from
            include (Optional[List[str]], optional):
                a list of field to include. All other ignored. Defaults to None.
            exclude (Optional[List[str]], optional): a list of field to exclude.
                Defaults to None.
        """

        # listing the attribute names requires bypassing protected access
        # pylint: disable=protected-access
        if include:
            # limit to include attribute list
            final_field_names = set(include)
        else:
            field_names = set(self._INITIAL_FIELDS.keys())
            final_field_names = field_names.intersection(
                document._INITIAL_FIELDS.keys()
            )

            if exclude:
                final_field_names = final_field_names.difference(set(exclude))

        for attrname in final_field_names:
            setattr(self, attrname, getattr(document, attrname))

        # pylint: enable=protected-access


class MAASRawDocument(MAASDocument):
    """
    Base class for ingested raw documents.

    Handle ingestionTime and reportName attributes automatically for all child classes
    """

    # default partitionning for raw documents
    _PARTITION_FIELD = "ingestionTime"

    reportName: Field = Keyword()

    reportFolder: Field = Keyword()

    ingestionTime: Field = ZuluDate()

    # commented out but left if any need comes in, as save strategy if bulk-based
    # Document.save has too many arguments to report: use of **kwargs
    # pylint: disable=W0221
    # def save(self, **kwargs):
    #     """override to fill ingestionTime automatically"""
    #     now = datetime.datetime.utcnow()

    #     # MAAS document models use camel case naming
    #     # pylint: disable=C0103
    #     self.ingestionTime = datetime_to_zulu(now)

    #     # buggy date reformat forced to deactivate local validation. To investigate
    #     kwargs["validate"] = False

    #     # index partition per year
    #     kwargs["index"] = self.get_yearly_index()

    #     # force refresh for data availability when sending message
    #     kwargs["refresh"] = True

    #     return super().save(**kwargs)
