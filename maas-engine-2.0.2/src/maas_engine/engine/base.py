"""
Define base ABC Engine
Implementations dedicated action
"""

from abc import ABC, abstractmethod
from argparse import Namespace
from dataclasses import dataclass, field

import importlib
import json
import logging
from typing import Any, ClassVar, Dict, Iterator, List, Optional, Type
from types import ModuleType

from maas_model import MAASDocument, MAASMessage, MAASBaseMessage

from .report import EngineReport


@dataclass
class EngineSession:
    """
    A base class to share data between engines
    """

    payload: Optional[MAASBaseMessage] = None

    session_dict: Dict[str, Any] = field(default_factory=lambda: {})

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the session dictionnary

        Args:
            key: key
            default (any, optional): Default value if not present. Defaults to None.

        Returns:
            any: value of the key
        """
        return self.session_dict.get(key, default)

    def put(self, key: str, value: Any) -> None:
        """
        Put a value to the session dictionnary

        Args:
            key: key
            value: : matching value
        """
        self.session_dict[key] = value


class Engine(ABC):
    """
    Abstract base class for compute engine
    """

    ENGINE_ID: ClassVar[str] = ""

    # default engine payload model
    PAYLOAD_MODEL: ClassVar[Type[MAASMessage]] = MAASMessage

    # stores all engines indexed by ENGINE_ID
    __ALL_ENGINES: ClassVar[Dict[str, Type["Engine"]]] = {}

    # module containing model referenced in the configuration file
    MODEL_MODULE: ClassVar[ModuleType]

    PAYLOAD_V2: ClassVar[bool] = False

    # default keyword arguments for all engines indexed by ENGINE_ID, populated by
    # the configuration file
    DEFAULT_ARGS_DICT: ClassVar[Dict[str, Any]] = {}

    # dictionnary loaded from json configuration
    CONFIG_DICT: ClassVar[Dict[str, Any]] = {}

    def __init__(
        self,
        args: Optional[Namespace] = None,
        send_reports: bool = True,
        chunk_size: int = 0,
    ):
        """Constructor

        Args:
            args (namespace, optional): namespace object coming from argument parsing.
                Defaults to None.
            send_reports (bool, optional): send reports on the amqp bus.
                Defaults to True.
        """

        self.logger: logging.Logger = logging.getLogger(self.__class__.__name__)

        self.args = args

        self.send_reports = send_reports

        self.chunk_size = chunk_size

        self.reports: List[EngineReport] = []

        self.routing_key = None

        self._session: Optional[EngineSession] = None

    @property
    def session(self) -> EngineSession:
        """
        Lazy build session accessor

        Returns:
            EngineSession: initialized session
        """
        if not self._session:
            self._session = EngineSession(MAASMessage())
        return self._session

    @session.setter
    def session(self, session: EngineSession) -> None:
        """
        session setter

        Args:
            session (EngineSession): session to set
        """
        if self._session is not None and self.logger:
            self.logger.warning("Overwriting session")
        self._session = session

    @property
    def payload(self) -> MAASBaseMessage | None:
        """
        shortcut for session payload

        Returns:
            MAASMessage: message that triggered the engine
        """
        return self.session.payload

    @payload.setter
    def payload(self, payload: MAASBaseMessage) -> None:
        """
        shortcut for session payload
        """
        self.session.payload = payload

    @abstractmethod
    def run(self, routing_key: str, payload: MAASBaseMessage) -> Iterator[EngineReport]:
        """Execute the engine

        Args:
            routing_key (str): type of the data to process
            item_ids (list[str] or MAASMessage): input data identifiers

        Raises:
            NotImplementedError: if the method is not implemented

        Returns:
            Iterator[EngineReport]: engine execution reports
        """
        raise NotImplementedError(
            "In Engine run method: Please implement in concrete class impl"
        )

    @classmethod
    def get(
        cls, engine_args: Dict[str, Any], args: Optional[Namespace] = None
    ) -> "Engine":
        """
        Get an engine instance matching the engine identifier and configure it with
        arguments


        Args:
            engine_id (str or dict): engine id or configuration dictionnary
            args (namespace): command line arguments as a namespace

        Returns:
            Engine: engine instance
        """
        if isinstance(engine_args, str):
            # basic declaration
            engine_id = engine_args
            engine_args = {}

        elif isinstance(engine_args, dict):
            # declaration with arguments
            engine_id = engine_args["id"]
            # populate arguments excluding id key
            engine_args = {
                key: value for key, value in engine_args.items() if not key == "id"
            }

        # override defaults if any
        if engine_id in cls.DEFAULT_ARGS_DICT:
            logging.debug(
                "Found defaults for %s: %s", engine_id, cls.DEFAULT_ARGS_DICT[engine_id]
            )
            engine_args = cls.DEFAULT_ARGS_DICT[engine_id] | engine_args

        try:
            engine_class = cls.__ALL_ENGINES[engine_id]
        except KeyError:
            logging.critical("Unknown engine: %s", engine_id)
            raise

        engine_args["args"] = args

        logging.debug(
            "Instanciating engine: %s with args: %s", engine_class, engine_args
        )

        return cls.__ALL_ENGINES[engine_id](**engine_args)

    @classmethod
    def get_model(cls, model_name: str) -> "MAASDocument":
        """Get a DAO class matching the model name

        Args:
            engine_id (str): engine id

        Returns:
            Document: DAO class
        """
        return getattr(cls.MODEL_MODULE, model_name)

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)

        # ENGINE_ID cannot be mandatory because of intermediate classes
        if not cls.ENGINE_ID:
            return

        # prevent overwrite
        if cls.ENGINE_ID in Engine.__ALL_ENGINES:
            raise ValueError(
                f"ENGINE_ID conflict: {cls.ENGINE_ID} is already registered"
            )

        # register the engine
        Engine.__ALL_ENGINES[cls.ENGINE_ID] = cls

    @classmethod
    def set_default_arguments(cls, args_list: list):
        """Populate DEFAULT_ARGS_DICT

        Args:
            args_list (list): list of object {"id": "ENGINE_ID", "param": "value" }
        """

        for args in args_list:
            engine_id = args["id"]
            if isinstance(engine_id, str):
                engine_id = [engine_id]

            for id_value in engine_id:
                cls.DEFAULT_ARGS_DICT[id_value] = {
                    **cls.DEFAULT_ARGS_DICT.get(id_value, {}),
                    **{key: value for key, value in args.items() if key != "id"},
                }

            logging.debug("Configured %s", args)

    @classmethod
    def load_config(cls, path):
        """load a json configuration file :
         - import engine modules
         - set model module
         - populate default engine args

        Args:
            path (str): configuration file path
        """
        cls.CONFIG_DICT = config_dict = json.load(path)

        cls.import_engines()

        logging.info("Importing model module: %s", config_dict["model"])
        cls.MODEL_MODULE = importlib.import_module(config_dict["model"])

        if "defaults" in config_dict:
            logging.info("Configuring engine defaults")
            cls.set_default_arguments(config_dict["defaults"])

        if "logging" in config_dict:
            # override some logger verbosity level
            for name, level_name in config_dict["logging"].items():
                if not hasattr(logging, level_name):
                    raise ValueError(
                        f"Invalid logging level for {name} in {path}: {level_name}"
                    )

                logging.debug("Set logging level of %s to %s", name, level_name)

                logging.getLogger(name).setLevel(getattr(logging, level_name))

    @classmethod
    def import_engines(cls):
        """
        import engine module implementation

        Raises:
            ValueError: if some implementations are missing
        """
        # load engine implementations
        for name in cls.CONFIG_DICT["modules"]:
            logging.info("Importing engine module: %s", name)
            importlib.import_module(name)

        # a set of all engine identifiers in the configuration
        declared_engine_ids = set()
        for exchange_dict in cls.CONFIG_DICT["amqp"]:
            for queue_dict in exchange_dict["queues"]:
                for event_config in queue_dict["events"]:
                    if isinstance(event_config, str):
                        declared_engine_ids.add(event_config)
                    elif isinstance(event_config, dict):
                        declared_engine_ids.add(event_config["id"])
                    else:
                        raise TypeError(f"{event_config} is not a string or a dict")

        # check all declared engine identifier have implementations
        if not all(name in cls.__ALL_ENGINES for name in declared_engine_ids):
            raise ValueError(
                "Missing engine implementations: "
                f"{' '.join(sorted(declared_engine_ids - set(cls.__ALL_ENGINES)))}"
            )

    @classmethod
    def deserialize_payload(cls, body: dict) -> MAASBaseMessage:
        """create a MAASMessage instance from a dict

        Args:
            body (dict): data dict from bus

        Raises:
            ValueError: if body is not a dict

        Returns:
            MAASMessage: payload message
        """

        if isinstance(body, dict):
            # V2 payload
            payload: MAASMessage = cls.PAYLOAD_MODEL(**body)
            payload.post_deserialization()

        else:
            raise ValueError(f"Message body is not a dictionnary body={body}")

        return payload
