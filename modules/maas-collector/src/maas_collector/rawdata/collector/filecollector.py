"""Data file collector 天気はいいです"""

from collections.abc import Iterable
import dataclasses
import datetime
import fnmatch
import gc
import logging
import os
import signal
import time
import traceback
import typing
import socket

from urllib.parse import urlparse

from functools import cached_property

from opensearchpy.helpers import parallel_bulk
from opensearchpy.connection.connections import connections as es_connections

from maas_model import MAASRawDocument, MAASMessage

from maas_collector.health import health
from maas_collector.health.serverthread import ServerThread

from maas_collector.rawdata.model import ActionIterator
from maas_collector.rawdata import extractor
from maas_collector.rawdata.configuration import (
    load_json as load_configuration_json,
    get_model,
    find_configurations,
)

from maas_collector.rawdata.backup import (
    BackupArgs,
    instanciate_collector_backup,
)
from maas_collector.rawdata.messenger import Messenger
from maas_collector.rawdata.replay import ReplayArgs

from maas_collector.rawdata.collector.credentialmixin import CredentialMixin

from maas_collector.rawdata.meta import IngestionMeta


# collector classes need many attributes
# pylint: disable=R0902
@dataclasses.dataclass
class CollectorArgs:
    """Collector base arguments"""

    amqp_url: str = ""

    es_url: str = ""

    es_timeout: int = 120

    rawdata_config: str = ""

    rawdata_config_dir: str = ""

    force: bool = False

    working_directory: str = "/tmp"

    healthcheck_hostname: str = "0.0.0.0"

    healthcheck_port: int = 8080

    watch_period: int = 60

    v1_compatibility: bool = False

    force_message: bool = False

    backup: BackupArgs = None

    es_retries: int = 3

    amqp_retries: int = 0

    credential_file: str = ""

    amqp_priority: int = 0

    replay: ReplayArgs = None

    healthcheck_timeout: int = None

    es_ignore_certs_verification: bool = False


@dataclasses.dataclass
class FileCollectorConfiguration:
    """
    Configuration for data collection

    Args:
        model (Document): Document class implementation to store the
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

    interface_credentials: str = ""

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

    def __repr__(self):
        # Liste pour stocker les éléments de représentation
        repr_parts = []
        # Parcours de tous les champs définis dans la classe
        for field in dataclasses.fields(self):
            # Récupère la valeur du champ
            field_value = (
                "*******"  # Si le champ est marqué comme sensible, afficher "*******"
                if field.metadata.get(
                    "sensitive", False
                )  # Vérifie si le champ est sensible via les métadonnées
                else getattr(
                    self, field.name
                )  # Sinon, récupérer la valeur réelle du champ
            )

            # Ajouter la représentation du champ à la liste
            repr_parts.append(f"{field.name}={field_value!r}")

        # Retourne la représentation de l'objet sous forme de chaîne de caractères
        return f"{self.__class__.__name__}({', '.join(repr_parts)})"

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


@dataclasses.dataclass
class EntityStats:
    """dataclass for per entity statistics"""

    name: str

    inserts: int = 0

    updates: int = 0

    errors: int = 0

    last_ingest: str = None

    last_error: str = None


@dataclasses.dataclass
class CollectorStats:
    """dataclass for whole collector statistics"""

    entities: typing.Dict[str, EntityStats]


# collector has too many method because of the number of template methods
# pylint: disable=R0904
class FileCollector(CredentialMixin):
    """
    Collect files from local filesystem, also base class for other implementations
    like S3 or SFTP by providing methods and template methods to override.
    """

    CONFIG_CLASS = FileCollectorConfiguration

    LOOP_PRECISION_FACTOR = 10

    def __init__(self, args: CollectorArgs):
        self.args = args

        # collector configurations
        self.configs = []

        # logger instance
        self.logger = logging.getLogger(self.__class__.__name__)

        # flag to tell setup() method has successfully been called
        self._initialized = False

        # flag to stop the calling loop_body() in run() method
        self.should_stop_loop = False

        # time the loop has start
        self.loop_start_time = None

        # path to a local error log containing the latest error report
        self.error_log = None

        self.stats = CollectorStats(entities={})

        # health check status: not very useful now except for rabbitmq state
        self.is_ok = True

        # health check instance containing flask app
        self._healthcheck = None

        # thread running the werkzeug server
        self._health_thread = None

        # deal with rabbitmq
        self._messenger: Messenger = Messenger(
            url=self.args.amqp_url,
            v1_compatibility=self.args.v1_compatibility,
            priority=self.args.amqp_priority,
            max_retries=self.args.amqp_retries,
            pipeline_name=self.__class__.__name__,
        )

        # action iterator reference so it can be found to be stopped
        self._action_iterator = None
        self.action_iterator_errors = []

        # list of configuration files
        self.__config_files = None

        if args.backup:
            self._backup = instanciate_collector_backup(args.backup)
        else:
            self._backup = None

    def get_configs(self, path: str):
        """get configurations of a given class from a json file

        Args:
            path ([str]): path of the configuration file
            config_class ([type]): config class object

        Raises:
            ValueError: when no configuration is available

        Returns:
            [type]: list of configuration objects
        """
        # load raw data mapping
        configs = load_configuration_json(path, self.CONFIG_CLASS)

        if not configs:
            msg = f"No config declared in {path}"
            self.logger.error(msg)
            raise ValueError(msg)

        return configs

    def load_config(self):
        """populate configuration for pattern matching and routing configuration"""
        self.configs.clear()
        for path in self.config_files:
            self.configs.extend(self.get_configs(path))

            self._messenger.load_config_file(path)

        # resolve model
        for config in self.configs:
            if isinstance(config.model, str) and config.model:
                if config.model:
                    self.logger.info("Resolving model class: %s", config.model)
                    config.model = get_model(config.model)
            else:
                self.logger.debug("No model declared in config %s", config)

        # handle optionnal credential file
        if self.args.credential_file:
            self.load_credentials(self.args.credential_file)

    @property
    def config_files(self) -> list[str]:
        """lazy create  the list of configuration files

        Returns:
            list[str]: list of path
        """
        if self.__config_files is None:
            # lazy create the list
            self.__config_files = []

            # single file
            if self.args.rawdata_config:
                self.__config_files.append(self.args.rawdata_config)

            # directory
            if self.args.rawdata_config_dir:
                self.__config_files.extend(
                    find_configurations(self.args.rawdata_config_dir)
                )

        return self.__config_files

    def setup(self):
        """Load rawdata extraction configuration, connect to AMQP and opensearch"""
        # load json configuration
        self.load_config()

        # connect to amqp
        # self._messenger.setup()

        self.logger.info(
            "Setup connection to opensearch to with %d max retries / timeout=%s",
            self.args.es_retries,
            self.args.es_timeout,
        )
        es_connections.create_connection(
            hosts=[self.args.es_url],
            retry_on_timeout=True,
            max_retries=self.args.es_retries,
            timeout=self.args.es_timeout,
            verify_certs=not self.args.es_ignore_certs_verification,
            ssl_show_warn=not self.args.es_ignore_certs_verification,
        )

        # connect signal to exit gracefully
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

        self._initialized = True

    def teardown(self):
        """Template method to finalize the instance"""

    def get_configurations(
        self, filename: str
    ) -> typing.List[FileCollectorConfiguration]:
        """Get the FileCollectorConfiguration instances that can handle a file

        Args:
            path ([filename]): filename

        Returns:
            [typing.List[FileCollectorConfiguration]]: list of configuration that can extract
        """
        basename = os.path.basename(filename)
        return [config for config in self.configs if config.filename_match(basename)]

    def get_configuration_by_interface_name(
        self, interface_name: str
    ) -> FileCollectorConfiguration:
        """Get a configuration instance named interface_name

        Args:
            interface_name (str): interface name

        Returns:
            FileCollectorConfiguration: configuration
        """
        results = [
            config for config in self.configs if config.interface_name == interface_name
        ]

        if not results:
            return None

        if len(results) == 1:
            return results[0]

        raise ValueError(
            f"Configuration has many interfaces ({len(results)}) "
            f"with same name: {interface_name}"
        )

    def get_interface_names(self) -> list[str]:
        """Get the list of the interface name

        Returns:
            list[str]: interface names
        """
        names = [config.interface_name for config in self.configs]
        names.sort()
        return names

    def extract_from_file(
        self,
        path: str,
        config: FileCollectorConfiguration,
        force_update=False,
        report_name="",
        report_folder="",
        iter_callback=None,
    ) -> None:
        """collect raw data from file and write to raw data database"""
        # shortcut for logging
        document_class_name = config.model.__name__

        self.logger.debug("Extracting %s from %s", document_class_name, path)

        self.logger.info(
            "Extracting %s to ingest %s instances", path, document_class_name
        )

        if not document_class_name in self.stats.entities:
            # populate stats
            self.stats.entities[document_class_name] = EntityStats(document_class_name)

        # handle force update argument, default to configuration
        if self.args.force:
            force_update = self.args.force

        # initialize action dictionnary generator
        self._action_iterator = ActionIterator(
            path,
            config,
            force_update=force_update,
            report_name=report_name,
            report_folder=report_folder,
            iter_callback=iter_callback,
        )
        self.action_iterator_errors = []
        try:
            # feed parallel_bulk with action iterator
            for success, info in parallel_bulk(
                es_connections.get_connection(),
                self._action_iterator,
                refresh=True,
                raise_on_exception=False,
                request_timeout=self.args.es_timeout,
            ):
                self._healthcheck.tick()

                if not success:
                    self.logger.error("Error pushing to database: %s", info)
                    self.on_document_error(path, config, info)
                    continue

                document_id = info["index"]["_id"]

                index = info["index"]["_index"]
                result = info["index"]["result"]

                if result == "created":
                    self.logger.info(
                        "Created %s %s from %s", document_class_name, document_id, path
                    )

                    self._messenger.handle_message(config, document_id, index)
                    if iter_callback:
                        self._action_iterator.execute_callback(
                            info["index"]["_index"], info["index"]["_id"]
                        )

                    self.on_document_insert(path, config, document_id)

                elif result == "updated":
                    self.logger.info(
                        "Updated %s %s from %s", document_class_name, document_id, path
                    )

                    self._messenger.handle_message(config, document_id, index)

                    if iter_callback:
                        self._action_iterator.execute_callback(
                            info["index"]["_index"], info["index"]["_id"]
                        )

                    self.on_document_update(path, config, document_id)

                else:
                    self.logger.error("Unexpected result: %s", result)
        finally:
            if self.args.force_message and self._action_iterator.unmodified_ids:
                # publish the untouched document identifier (hole filling)
                self.logger.info(
                    "Notifiying %d unmodified documents from %s",
                    len(self._action_iterator.unmodified_ids),
                    path,
                )

                for document_id in self._action_iterator.unmodified_ids:
                    self._messenger.handle_message(config, document_id)

            if self._action_iterator.document_count == 0:
                self.logger.info("No data published to database from %s", path)
            else:
                self.logger.info(
                    "%d documents published to database from %s",
                    self._action_iterator.document_count,
                    path,
                )

            if self._backup:
                self._backup.backup_file(config, path)

                # handle meta
                if IngestionMeta.has_meta_file(path):
                    self._backup.backup_file(config, IngestionMeta.get_meta_path(path))

            self.action_iterator_errors = self._action_iterator.action_iterator_errors
            self._action_iterator = None

    def ingest(
        self,
        path: str,
        configs: typing.List[FileCollectorConfiguration] = None,
        force_update=False,
        report_folder=None,
    ) -> None:
        """Ingest a file or a directory

        Child classes can download files before calling super().ingest(path) with a local path

        Args:
            path ([str]): local file or directory.
        """
        if os.path.isfile(path):
            self.logger.debug("Ingest single file %s", path)
            path_list = [path]

        elif os.path.isdir(path):
            # build path list omitting hidden files and error logs
            path_list = [
                os.path.join(path, entry)
                for entry in os.listdir(path)
                if not (entry.startswith(".") or entry.endswith(".err.log"))
            ]
            if not path_list:
                self.logger.error("%s: empty directory", path)
                return
            self.logger.debug(
                "Ingest directory %s with %d entries", path, len(path_list)
            )
        else:
            raise ValueError(
                f"path to ingest is neither a file path or a directory path: {path}"
            )

        errors = []

        # process files
        for path_entry in path_list:
            if self.should_stop_loop:
                break

            report_name = os.path.basename(path_entry)

            if report_folder is None:
                report_folder = os.path.abspath(os.path.dirname(path_entry))

            if configs is None:
                found_configs = self.get_configurations(report_name)
            else:
                found_configs = configs

            if not found_configs:
                self.logger.debug(
                    "Unknown file type : no file pattern matches path: %s", path_entry
                )
                continue

            for config in found_configs:
                try:
                    self.extract_from_file(
                        path_entry,
                        config,
                        force_update,
                        report_name=report_name,
                        report_folder=report_folder,
                    )

                    self.on_ingest_success(path_entry, config)

                    if len(self.action_iterator_errors) > 0:
                        raise ValueError("\n".join(self.action_iterator_errors))

                # catch broad exception to not break the loop
                # pylint: disable=W0703
                except Exception as error:
                    self.logger.error(
                        "Error extracting from %s with %s", path_entry, config.name
                    )
                    self.logger.exception(error)
                    error_traceback = traceback.format_exc()
                    errors.append((path_entry, config, error, error_traceback))

                    self.on_ingest_error(path_entry, config, error)

        if not self.should_stop_loop:
            self.on_ingest_finish(path, errors)

    def build_healthcheck(self) -> health.ServiceHealthCheck:
        """Factory function to create an ServiceHealthCheck service to be used by the collector

        Returns:
            health.ServiceHealthCheck: HealthCheck service to be used by the collector
        """
        return health.ServiceHealthCheck(self, self.args.healthcheck_timeout)

    def start_healthcheck(self):
        """create healthcheck object and start the healthcheck server thread"""
        self._healthcheck = self.build_healthcheck()
        self._healthcheck.tick()

        self._health_thread = ServerThread(
            self._healthcheck.app,
            self.args.healthcheck_hostname,
            self.args.healthcheck_port,
        )
        self._health_thread.start()

    def stop_healthcheck(self):
        """stop the healthcheck server thread"""
        self._health_thread.shutdown()
        self._health_thread.join()

    def run(self, path_list: typing.List[str]) -> None:
        """ingest a list of path periodically. entry point for CLI collectors.

        Args:
            path ([str]): path to watch. Can be directory of filename.
            watch_period (int, optional): call time period in seconds. Defaults to 60.
                Zero value runs the loop only once.
        """
        self.logger.info("Starting collector")

        self.start_healthcheck()

        try:
            while not self.should_stop_loop:
                self.loop_start_time = time.time()
                self._healthcheck.tick()

                # call template method
                self.on_loop_start()

                # do the job
                self.loop_body(path_list)

                self.post_loop()

                # flush remaining message chunks
                self._flush_message_groups()

                # close message bus connection
                self._messenger.close()

                # call template method
                self.on_loop_end()

                # one-shot run with zero period
                if self.should_stop_loop or self.args.watch_period == 0:
                    self.logger.info("Exiting")
                    break

                # calculate sleep time
                end_time = time.time()

                delta = end_time - self.loop_start_time

                if self.args.watch_period > delta:
                    self.logger.debug(self.stats)

                    sleep_time = self.args.watch_period - delta

                    self.logger.info("Loop finished. Sleeping %fs", sleep_time)

                    # sleep by small step to answer rather quickly to signal shutdown
                    for _ in range(round(sleep_time) * self.LOOP_PRECISION_FACTOR):
                        if self.should_stop_loop:
                            break
                        time.sleep(1 / self.LOOP_PRECISION_FACTOR)
                else:
                    self.logger.info(
                        "Loop took too much time: total %.2f / exceed %.2f seconds.",
                        delta,
                        delta - self.args.watch_period,
                    )

        finally:
            # in case some message remains in cache, typically when errors happen
            self.stop_healthcheck()
            self.logger.info("Exiting run()")
            self.logger.debug(self.stats)
            self._flush_message_groups()

    def create_report(self, path: str, errors):
        """write an ingestion error report

        Args:
            path ([str]): report path
            errors ([list]): list of tuples (path_entry, config, error)
        """
        entry_dict = {}
        for path_entry, config, error, error_traceback in errors:
            if not path_entry in entry_dict:
                entry_dict[path_entry] = []
            entry_dict[path_entry].append((config, error, error_traceback))

        for path_entry, log_tuple in entry_dict.items():
            self.error_log = f"{path_entry}.{int(time.time())}.err.log"

            with open(self.error_log, "w", encoding="UTF-8") as report_file:
                report_file.writelines(
                    [f"{path}{os.linesep}{os.linesep}", f"==={os.linesep}{os.linesep}"]
                    + [
                        f"{config.name}: {path_entry}{os.linesep}{error}{os.linesep}{os.linesep}"
                        + f"{error_traceback}{os.linesep}{os.linesep}"
                        for config, error, error_traceback in log_tuple
                    ]
                    + [f"==={os.linesep}"]
                )
            self.logger.info("Error report written to %s", self.error_log)

    def on_ingest_success(self, path: str, config):
        """emit message whit RK file.* if file_routing_key setted in config

        Args:
            path (str): the file path
            config (_type_): the collector config
        """
        if config.file_routing_key:
            self._messenger.send_to_queue(
                config.file_routing_key,
                MAASMessage(
                    document_class=config.model_name,
                    document_ids=[os.path.basename(path)],
                    pipeline=[self.__class__.__name__],
                ),
            )

    def on_ingest_error(self, path: str, config, error):
        """Template method"""

    def on_ingest_finish(self, path: str, errors):
        """Post-ingestion callback for the whole file"""
        if errors:
            error_log = f"{path}{time.time()}.err.log"
            self.create_report(error_log, errors)

    # template callbacks do not use all arguments
    # pylint: disable=W0613

    def on_document_insert(
        self, path: str, config: FileCollectorConfiguration, document_id: str
    ):
        """Post-insert callback"""
        stats = self.entity_stats(config)
        stats.inserts += 1
        stats.last_ingest = datetime.datetime.utcnow()

    def on_document_update(
        self, path: str, config: FileCollectorConfiguration, document_id: str
    ):
        """Post-update callback"""
        stats = self.entity_stats(config)
        stats.updates += 1
        stats.last_ingest = datetime.datetime.utcnow()

    def on_document_error(
        self,
        path: str,
        config: FileCollectorConfiguration,
        info: dict,
    ):
        """Post-error callback"""
        stats = self.entity_stats(config)
        stats.errors += 1
        stats.last_error = datetime.datetime.utcnow()

    def entity_stats(self, config: FileCollectorConfiguration):
        """Get the EntityStats instance for a FileCollectorConfiguration"""
        return self.stats.entities[config.model.__name__]

    @staticmethod
    def get_date_dirname(dirdatetime: datetime.datetime = None):
        """build a sub path from a datetime object.

        Args:
            dirdatetime (datetime.datetime, optional): Date to generate the path from.
            Defaults to now if None.

        Returns:
            [type]: sub path
        """
        if dirdatetime is None:
            dirdatetime = datetime.datetime.utcnow()

        return os.path.join(
            f"{dirdatetime.year:04d}",
            f"{dirdatetime.month:02d}",
            f"{dirdatetime.day:02d}",
        )

    def on_loop_start(self):
        """Template method called at loop start"""

    def on_loop_end(self):
        """Template method called at loop end"""

    def loop_body(self, path_list: typing.List[str]):
        """iterate over path list and ingest items

        Args:
            path_list (typing.List[str]): a list of file path
        """
        for path in path_list:
            if self.should_stop_loop:
                break

            self._healthcheck.tick()

            try:
                self.ingest(path)

            # catch broad exception to not break the loop
            # pylint: disable=W0703
            except Exception as error:
                # won't break
                self.logger.error("Cannot ingest from %s", path)
                self.logger.exception(error)

    def exit_gracefully(self, signum, frame):
        """callback for SIGINT and SIGTERM

        Args:
            signum ([int]): Signal number
            frame ([frame]): bytecode frame
        """
        self.logger.info("Caught signal %s", signum)

        self.logger.info("Telling loop and ingestion to stop")

        self.should_stop_loop = True

        if self._action_iterator:
            self.logger.info("Stopping ES action iterator")

            self._action_iterator.stop()

        self._flush_message_groups()

    def _flush_message_groups(self):
        """clear the document identifier cache hold in the Messenger instance"""
        self._messenger.flush_message_groups()

    def post_loop(self):
        """
        Post ingestion loop execution, resilient to any error so next loop could
        encounter better conditions if any failure
        """
        callables = [self._flush_message_groups]

        if self._backup:
            callables.append(self._backup.close)

        for post_loop_callable in callables:
            try:
                post_loop_callable()

            # catch broad exception to not break the loop
            # pylint: disable=W0703
            except Exception as exception:
                self.logger.error(
                    "Failed to execute post loop callable: %s due to %s",
                    post_loop_callable.__name__,
                    exception,
                )
                self.logger.exception(exception)
            # pylint: enable=W0703
        gc.collect()

    def get_pending_document_count(self) -> int:
        return len(self._messenger)

    @classmethod
    def probe(cls, config, probe_data):
        """Default probe: returns a negative result

        Args:
            config: configuration
            probe_data: data to fill
        """
        probe_data.status = "KO"
        probe_data.details = (
            f"Probing {config.interface_name} "
            f"({cls.__name__}) is not yet implemented"
        )
        probe_data.status_code = -1

    @classmethod
    def attributs_url(cls):
        return []

    @classmethod
    def document(cls, config: FileCollectorConfiguration):
        information = {
            "__documentation__": "Only used on manual operation",
            "maas_collector": cls.__name__,
            "maas_collector_config": config.__class__.__name__,
            "maas_interface_name": config.interface_name,
            "maas_interface_model": config.model,
            "protocol": "Filesystem",
        }

        attributs_url = cls.attributs_url()
        for attribut_url in attributs_url:
            url = getattr(config, attribut_url, None)
            if url:

                parsed_url = urlparse(url)

                hostname = parsed_url.netloc

                # Résoudre les adresses IP
                information[attribut_url] = url
                url_ip_field_name = f"{attribut_url}_ip"

                # bypass kube svc
                if hostname.endswith(".svc.cluster.local"):
                    information[url_ip_field_name] = "Internal services"
                    continue

                information[url_ip_field_name] = "Faile to retrieve this"

                try:
                    host_info = socket.gethostbyname_ex(hostname)
                    ip_addresses = host_info[2]
                    information[url_ip_field_name] = ip_addresses
                except socket.error as err:
                    print(f"Erreur lors de la résolution des adresses IP : {err}")

        return information
