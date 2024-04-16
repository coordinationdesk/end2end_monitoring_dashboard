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
import os
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

    # dictionnary loaded from json configurations
    CONFIG_DICT: ClassVar[Dict[str, Any]] = {"amqp": []}

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

    @staticmethod
    def find_configurations(directory_path: str, ext=".json") -> List[str]:
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

    @classmethod
    def load_config_file(cls, file_path):
        """load json configuration file :
         - import modules
         - import model
         - import default config
         - import logging config
        then:
         - import engines (could need modules imported)

        Args:
            path (str): configuration file path
        """
        logging.info("Importing configuration from file: %s", file_path)
        config_dict = json.load(file_path)
        cls.import_general_config(config_dict)
        # load exchanges at the end (may need modules and model imported) 
        cls.import_exchanges_config(config_dict)

    @classmethod
    def load_config_directory(cls, directory_path: str):
        """Load all configurations files recurssively in a directory tree
         - import modules files
         - import model files
         - import default config files
         - import logging config files
        then:
         - import engines files (could need modules imported)

        Args:
            directory_path (str): path to directory
        """
        
        logging.info("Importing configuration from directory: %s", directory_path)
        #Store config in a "buffer" minimize fs access for multiples access
        config_files=cls.find_configurations(directory_path)
        config_dicts_from_files={}
        for path in config_files:
            with open(path, "r", encoding="utf-8") as config_file:
                config_file_dict = json.load(config_file)
                config_dicts_from_files[path]=config_file_dict
        for path,config_dict in config_dicts_from_files.items():
            logging.info("Loading modules, model, defaults, logging configs from file: %s", path)
            cls.import_general_config(config_dict)
        # load exchanges at the end (may need modules and model imported) 
        for path,config_dict in config_dicts_from_files.items():
            logging.info("Loading exchange configs from file: %s", path)
            cls.import_exchanges_config(config_dict)

    @classmethod
    def import_general_config(cls,config_dict):
        if "modules" in config_dict:
            cls.import_modules(config_dict)
        if "model" in config_dict:
            cls.import_models(config_dict) 
        if "defaults" in config_dict:
            cls.import_defaults(config_dict)
        if "logging" in config_dict:
            cls.import_logging(config_dict)

    @classmethod
    def import_exchanges_config(cls, config_dict):
        if "amqp" in config_dict:
            cls.import_exchanges(config_dict)

    @classmethod
    def import_modules(cls, config_dict):
        logging.info("Importing modules.")
        # load engine implementations
        for name in config_dict.get("modules", []):
            logging.info(" - importing module: %s", name)
            importlib.import_module(name)

    @classmethod
    def import_models(cls, config_dict):
        logging.info("Importing models.")
        logging.info(" - importing model: %s", config_dict["model"])
        cls.MODEL_MODULE = importlib.import_module(config_dict["model"])
        
    
    @classmethod
    def import_defaults(cls, config_dict):
        logging.info("Importing default configuration.")
        cls.set_default_arguments(config_dict["defaults"])
        
    @classmethod
    def import_logging(cls, config_dict):
        logging.info("Importing logging.")
        # override some logger verbosity level
        for name, level_name in config_dict["logging"].items():
            if not hasattr(logging, level_name):
                raise ValueError(
                    f"Invalid logging level for {name} : {level_name}"
                )
            logging.debug("Set logging level of %s to %s", name, level_name)
            logging.getLogger(name).setLevel(getattr(logging, level_name))
            
    @classmethod
    def import_exchanges(cls, config_dict):
        """
        import engine module implementation

        Raises:
            ValueError: if some implementations are missing
        """
        logging.info("Importing exchanges.")
        for exchange_dict in config_dict["amqp"]:
            configured_exchange = None
            logging.info(" - importing/ merging exchange: %s",exchange_dict["name"])
            
            for exchange in cls.CONFIG_DICT["amqp"]:
                if exchange_dict["name"] == exchange["name"]:
                    # the exchange has already been added so should be "configured" avoid queue multiple definition  
                    configured_exchange = exchange
                    break
                
            if not configured_exchange:
                # if there is no exchange to "configure" adding it as is 
                cls.CONFIG_DICT["amqp"].append(exchange_dict)
            else:
                # queue updates
                existing_queues = {
                    queue["name"]: queue for queue in configured_exchange["queues"]
                }
                
                for queue in exchange_dict["queues"]:
                    if queue["name"] in existing_queues:
                        logging.warning(
                            "Overriding queue %s in %s",
                            queue["name"],
                            exchange_dict["name"],
                        )
                        existing_queues[queue["name"]].update(queue)
                    else:
                        logging.debug("Add queue: %s", queue["name"])
                        configured_exchange["queues"].append(queue)
                        
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
