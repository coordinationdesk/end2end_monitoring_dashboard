"""classes for amqp messenging"""

import dataclasses
import datetime
import enum
import uuid
from typing import List, Dict

from maas_model.date_utils import datestr_to_utc_datetime, datetime_to_zulu


class DataAction(enum.Enum):
    """

    Enumeration to describe actions on data. Used in routing key generation.
    """

    NEW = "new"

    UPDATE = "update"

    DELETE = "delete"


@dataclasses.dataclass
class MAASBaseMessage:
    """A dataclass to deserialize body of AMQP payload

    The base message that contains the date of the instanciation

    Must be override
    """

    date: str = dataclasses.field(
        default_factory=lambda: datetime_to_zulu(datetime.datetime.utcnow())
    )

    message_id: str = dataclasses.field(default_factory=lambda: str(uuid.uuid4()))

    ancestor_ids: List[str] = dataclasses.field(default_factory=lambda: [])

    pipeline: List[str] = dataclasses.field(default_factory=lambda: [])

    force: bool = True

    @property
    def msg_datetime(self) -> datetime.datetime | None:
        """getter for date as datetime"""
        return datestr_to_utc_datetime(self.date)

    @msg_datetime.setter
    def msg_datetime(self, msg_datetime: datetime.datetime):
        """setter for date as datetime"""
        self.date = datetime_to_zulu(msg_datetime)

    def to_dict(self) -> dict:
        """Convert the message to dictionnary for json message body"""
        return dataclasses.asdict(self)

    def post_deserialization(self) -> None:
        """Perform additional operation after deserialization of payload has occured"""


@dataclasses.dataclass
class MAASMessage(MAASBaseMessage):
    """A dataclass to deserialize body of AMQP payload

    The default message consume by maas-engine

    Main usecase
        document_ids provides the identifier list of documents
        document_indices provides the indices list of documents
        document_class the name of the class (ie index) of the document

    Alt
        engine can overload the main usecase

    """

    document_ids: List[str] = dataclasses.field(default_factory=lambda: [])

    document_indices: List[str] = dataclasses.field(default_factory=lambda: [])

    document_class: str = ""

    def post_deserialization(self) -> None:
        # remove duplicates but preserve order
        self.document_ids = list(dict.fromkeys(self.document_ids))


@dataclasses.dataclass
class MAASQueryMessage(MAASBaseMessage):
    """A dataclass to deserialize body of AMQP payload

    Should be consume by QueryEngine

    document_class the name of the class (ie index) of the document
    query_string the lucene query that will be execute to select entities
    output_routing_key where the report must be sendend
    chunk_size number of ids in reports
    """

    document_class: str = ""

    query_string: str = "*"

    output_routing_key: str = ""

    chunk_size: int = 0


@dataclasses.dataclass
class MAASOperationMessage(MAASQueryMessage):
    """A dataclass to deserialize body of AMQP payload

    Should be consume by Custom Engine overriding QueryEngine

    operation_name the name of the engine that need to be execute
    operation_args the args for the engine that need to be execute
    send_reports default to false to get dry run behavior
    """

    dry_run: bool = False

    operation_name: str = ""

    operation_args: dict = dataclasses.field(default_factory=lambda: {})

    send_reports: bool = False
