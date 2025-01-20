"""contains a collector for monitoring interfaces"""

import dataclasses
import datetime
import json
import logging
import os
from queue import Queue, Empty
import time
from threading import Thread, Event


from typing import Any, Callable, Dict, List

from multiprocessing.pool import ThreadPool

import requests

from maas_model import datetime_to_zulu

from maas_collector.rawdata.collector.journal import (
    JournalDocument,
    CollectorJournal,
    CollectingInProgressError,
    NoRefreshException,
)

from maas_collector.rawdata.collector.filecollector import (
    FileCollector,
    FileCollectorConfiguration,
    CollectorArgs,
)

from maas_collector.rawdata.implementation import (
    get_collector_class_by_config_classname,
)

from maas_collector.rawdata.configuration import (
    load_json as load_configuration_json,
    find_configurations,
)

from maas_collector.rawdata.collector.credentialmixin import CredentialMixin


@dataclasses.dataclass
class InterfaceMonitorCollectorConfiguration(FileCollectorConfiguration):
    """Store monitoring configuration vars"""

    interface_name: str = ""

    interfaces: List[str] = dataclasses.field(default_factory=lambda: [])

    refresh_interval: int = 300

    extra_http_probes: List[str] = dataclasses.field(default_factory=lambda: [])

    max_retry: int = 3

    retry_interval: int = 60

    stuck_timeout: int = 1800


@dataclasses.dataclass
class InterfaceMonitorConfiguration:
    """Specific command line arguments"""

    interface_name: str = ""


@dataclasses.dataclass
class InterfaceMeta:
    """Meta information about an interface"""

    name: str = ""

    configuration_path: str = ""

    config: FileCollectorConfiguration | None = None

    probe_callable: Callable = lambda: True

    retrying: bool = False

    retry_count: int = 0

    logger: logging.Logger = dataclasses.field(
        default_factory=lambda: logging.getLogger("InterfaceMeta")
    )

    def run_probe(
        self, probe_data: "InterfaceProbeData" = None
    ) -> "InterfaceProbeData":
        """Run the probe of the interface

        Args:
            interface_meta (InterfaceMeta): interface meta

        Returns:
            InterfaceProbeData: result of the probe
        """

        self.logger.info("Start probing %s", self.name)

        if probe_data is None:

            probe_data = InterfaceProbeData(self.name)

            probe_data.probe_time_start = datetime.datetime.now(
                tz=datetime.timezone.utc
            )

        try:
            self.probe_callable(self.config, probe_data)

            if not probe_data.status:
                # if status is not filled: a run without exception is OK
                probe_data.status = "OK"

        # catch broad exception to handle any kind of return
        # pylint: disable=W0703
        except Exception as error:
            # Errors should never pass silently.
            probe_data.status = "KO"

            probe_data.status_code = -1

            probe_data.details = str(error)

            self.logger.warning("%s: %s", self.name, error)

        # pylint: enable=W0703

        probe_time_end = probe_data.probe_time_end = datetime.datetime.now(
            tz=datetime.timezone.utc
        )

        duration = probe_time_end - probe_data.probe_time_start

        probe_data.probe_duration = int(duration.total_seconds())

        self.logger.info(
            "End probing %s with status %s in %ss",
            self.name,
            probe_data.status,
            probe_data.probe_duration,
        )

        return probe_data


@dataclasses.dataclass
class InterfaceProbeData:
    """store monitoring attributes"""

    interface_name: str

    probe_time_start: datetime.datetime = dataclasses.field(
        default_factory=lambda: datetime.datetime.now(tz=datetime.timezone.utc)
    )

    probe_time_end: datetime.datetime | None = None

    probe_duration: int = 0

    status: str = ""

    status_code: int = 0

    details: str = ""

    most_recent_modification_date: datetime.datetime | None = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Return JSON serializable dictionnary with converted datetime to string

        Returns:
            Dict[str, Any]: JSON dictionnary
        """
        data_dict = dataclasses.asdict(self)

        # override dates with string representation
        data_dict["probe_time_start"] = datetime_to_zulu(self.probe_time_start)
        data_dict["probe_time_end"] = datetime_to_zulu(self.probe_time_end)
        data_dict["most_recent_modification_date"] = datetime_to_zulu(
            self.most_recent_modification_date
        )

        return data_dict


@dataclasses.dataclass
class ProbeRetry:
    """

    Encapsulate probe retry
    """

    interface: InterfaceMeta

    probe: InterfaceProbeData


class RetryThread(Thread):
    """

    A thread responsible to accomply the retry logic
    """

    def __init__(
        self, probe_retry: ProbeRetry, count=3, interval=60, stuck_timeout=1800
    ) -> None:
        super().__init__()
        self.probe_retry = probe_retry
        self.probe = probe_retry.probe
        self.logger = logging.getLogger(
            f"{self.__class__.__name__}_{probe_retry.interface.name}"
        )
        self.count = count

        self.interval = interval

        self.stuck_timeout = stuck_timeout

        self.shall_stop_event = Event()

        self.last_start: datetime.datetime

    def run(self):
        """Entry point"""
        for _ in range(self.count):
            if self.shall_stop_event.is_set():
                break

            time.sleep(self.interval)

            self.last_start = datetime.datetime.now(tz=datetime.timezone.utc)

            probe = self.probe_retry.interface.run_probe(self.probe)

            if probe.status == "OK":
                break

        self.probe_retry.interface.retrying = False

    def is_stuck(self) -> bool:
        """
        A retry probe can be stuck

        Returns:
            bool: True if stuck
        """
        delta = datetime.datetime.now(tz=datetime.timezone.utc) - self.last_start
        return delta.seconds >= self.stuck_timeout


class KOManagerThread(Thread):
    """

    Encapsulate probe retry
    """

    def __init__(self, args: InterfaceMonitorCollectorConfiguration) -> None:
        super().__init__()

        self.args = args

        self.retry_threads: List[RetryThread] = []

        self.data: Queue[InterfaceProbeData] = Queue()

        self.run_event = Event()

        self.run_event.set()

    def add_retry(self, probe_retry: ProbeRetry) -> None:
        """
        Add a retry object

        Args:
            probe_retry (ProbeRetry): probe retry
        """
        probe_retry.interface.retrying = True
        thread = RetryThread(
            probe_retry,
            self.args.max_retry,
            self.args.retry_interval,
            self.args.stuck_timeout,
        )
        self.retry_threads.append(thread)
        thread.start()

    def run(self) -> None:
        """Entry point"""
        while self.run_event.is_set():
            # Handle finished threads
            finished_threads = [
                thread for thread in self.retry_threads if not thread.is_alive()
            ]
            if finished_threads:
                for thread in finished_threads:
                    self.data.put(thread.probe)
                    self.retry_threads.remove(thread)
                    thread.join()

            time.sleep(1)

    def stop_retry(self) -> None:
        """
        Tell retry thread to stop and join them
        """
        self.run_event.clear()
        for thread in self.retry_threads:
            thread.shall_stop_event.set()
            thread.join()

    def is_stuck(self) -> bool:
        """
        Tell if any of the retry thread is currently blocking

        Returns:
            bool: True if stuck
        """
        if not self.retry_threads:
            return False

        for thread in self.retry_threads:
            if thread.is_stuck():
                return True

        return False


class InterfaceMonitor(FileCollector, CredentialMixin):
    """A collector that probes status for interfaces"""

    CONFIG_CLASS = InterfaceMonitorCollectorConfiguration

    def __init__(
        self, args: CollectorArgs, monitor_config: InterfaceMonitorConfiguration
    ):
        super().__init__(args)

        self.monitor_config = monitor_config

        self.meta_dict: Dict[str, InterfaceMeta] = {}

        self.last_modification_date_dict: Dict[str, datetime.datetime] = {}

        self.retries: List[ProbeRetry] = []

        self.ko_manager: KOManagerThread

    def setup(self) -> None:
        if not self.monitor_config.interface_name:
            raise ValueError("No monitoring interface name provided")

        super().setup()

        # Filter out configuration to only keep OMCS_Monitoring
        self.configs = [
            config
            for config in self.configs
            if config.interface_name == self.monitor_config.interface_name
        ]

        if not self.configs:
            raise ValueError(
                "No monitoring configuration found"
                f" with name {self.monitor_config.interface_name}"
            )

        credential_dict = self.load_credential_dict(self.args.credential_file)

        meta_list: List[InterfaceMeta] = []

        # load the configurations of the interfaces to monitor
        for config_path in find_configurations(self.args.rawdata_config_dir):
            with open(config_path, mode="r", encoding="UTF-8") as conf_obj:
                conf_dict = json.load(conf_obj)

            self.logger.debug("Looking in %s", config_path)

            for collect_conf_dict in conf_dict.get("collectors", []):
                if not collect_conf_dict.get("class"):
                    self.logger.info(
                        "Class property empty. Ignoring some configuration in %s",
                        config_path,
                    )
                    continue

                if collect_conf_dict["class"] == self.CONFIG_CLASS.__name__:
                    self.logger.debug(
                        "Ignoring InterfaceMonitorConfiguration: %s", config_path
                    )
                    continue

                collector_class = get_collector_class_by_config_classname(
                    collect_conf_dict["class"]
                )

                config = [
                    config
                    for config in load_configuration_json(
                        config_path, collector_class.CONFIG_CLASS
                    )
                    if config.interface_name == collect_conf_dict["interface_name"]
                ][0]

                if config.no_probe:
                    self.logger.info(
                        "Probing is disabled for interface %s", config.interface_name
                    )
                    continue

                self.logger.debug("Applying credentials to %s", config.interface_name)

                try:
                    self.set_credential_attributes(config, credential_dict)
                except KeyError as error:
                    self.logger.warning(error)
                    continue

                interface_meta = InterfaceMeta(
                    name=collect_conf_dict["interface_name"],
                    configuration_path=config_path,
                    config=config,
                    probe_callable=collector_class.probe,
                )

                meta_list.append(interface_meta)

        # additionnal http probes
        for config in self.configs:
            if not config.extra_http_probes:
                continue

            for http_meta in config.extra_http_probes:
                # generate pseudo interface meta
                meta_list.append(
                    InterfaceMeta(
                        name=http_meta["interface_name"],
                        probe_callable=self.build_http_probe_callable(http_meta["url"]),
                    )
                )

        meta_list.sort(key=lambda itf: itf.name)

        self.meta_dict = {meta.name: meta for meta in meta_list}

        self.ko_manager = KOManagerThread(self.configs[0])
        self.ko_manager.start()

    def ingest(self, path=None, configs=None, force_update=None):
        """Ingest from SFTP. All arguments are ignored so defaults to None

        Args:
            path (_type_, optional): _description_. Defaults to None.
            configs (_type_, optional): _description_. Defaults to None.
            force_update (_type_, optional): _description_. Defaults to None.
        """
        # iterate over all configurations
        for config in self.configs:
            if self.should_stop_loop:
                break

            try:
                # use the journal as context to secure the concurent collect
                with CollectorJournal(config) as journal:
                    self.ingest_monitoring(config, journal)

            except CollectingInProgressError:
                # Errors should never pass silently.
                self.logger.info(
                    "On going collection on interface %s: skipping",
                    config.interface_name,
                )
            except NoRefreshException:
                self.logger.info(
                    "Interface %s does not need to be refreshed: skipped",
                    config.interface_name,
                )
            finally:
                # flush messages between interfaces as they don't ingest the same data
                self._flush_message_groups()

    def run_probe(self, interface_meta: InterfaceMeta) -> InterfaceProbeData:
        """Run the probe of the interface

        Args:
            interface_meta (InterfaceMeta): interface meta

        Returns:
            InterfaceProbeData: result of the probe
        """

        self.logger.info("Start probing %s", interface_meta.name)

        probe_data = interface_meta.run_probe()

        self.logger.info(
            "End probing %s with status %s in %ss",
            interface_meta.name,
            probe_data.status,
            probe_data.probe_duration,
        )

        return probe_data

    def ingest_monitoring(
        self, config: InterfaceMonitorCollectorConfiguration, journal: CollectorJournal
    ):
        """Probe all the interface, generate a JSON document and ingest it

        Args:
            config (InterfaceMonitorCollectorConfiguration): monitoring configuration
            journal (CollectorJournal): journal
        """

        # load all journal documents to store interface_name -> last modification date
        search = JournalDocument.search().params(ignore=404, size=1024)

        self.last_modification_date_dict = {
            doc.meta.id: doc.last_date for doc in search.execute()
        }

        # Handle retried probes
        if self.ko_manager.data.qsize() > 0:

            retried_probes = []
            try:
                while retried_probe := self.ko_manager.data.get(block=False):
                    retried_probes.append(retried_probe)
            except Empty:
                self.logger.debug("Empty retried queue")

            self.logger.debug("Found %d retried probes", len(retried_probes))

            if retried_probes:
                self.ingest_probes(config, retried_probes)

        if self.ko_manager.is_stuck():
            self.logger.critical("KOManager is stuck. Sleeping until kube restart")
            time.sleep(self.args.healthcheck_timeout * 4)

        meta_list = [meta for meta in self.meta_dict.values() if not meta.retrying]

        # use a thread pool for parallel probing. As this activity consists in waiting
        # for a response from network, the GIL is release and this does not require
        # real parallel processing
        # max pool size depend of the kernel, but 256 is a common limit
        pool = ThreadPool(min((len(meta_list), 256)))

        # run all
        all_probe_data: List[InterfaceProbeData] = pool.map(self.run_probe, meta_list)

        # ingest ok probes
        ok_probes: List[InterfaceProbeData] = [
            probe_data for probe_data in all_probe_data if probe_data.status == "OK"
        ]

        if ok_probes:
            self.ingest_probes(config, ok_probes)

        # find ko probe for specific process
        ko_probes: List[InterfaceProbeData] = [
            probe_data for probe_data in all_probe_data if probe_data.status == "KO"
        ]

        if ko_probes:
            self.retry_probes(ko_probes)

        self._healthcheck.tick()

        # store the most recent modification date of all interface as global
        # modification date
        last_modification_values = [
            value for value in self.last_modification_date_dict.values() if value
        ]
        if last_modification_values:
            journal.last_date = max(last_modification_values)

    def ingest_probes(
        self,
        config: InterfaceMonitorCollectorConfiguration,
        probes: List[InterfaceProbeData],
    ) -> None:
        """
        Create a json file to ingest from probes

        Args:
            config (InterfaceMonitorCollectorConfiguration): _description_
            probes (List[InterfaceProbeData]): _description_
        """
        # add journal information
        for probe in probes:
            probe.most_recent_modification_date = self.last_modification_date_dict.get(
                probe.interface_name
            )

        # create a dictionnary structure to later create json document
        document_dict = {"results": [probe.to_dict() for probe in probes]}

        # generate a consistant filename
        filename = os.path.join(
            self.args.working_directory,
            "MAAS-Monitoring-"
            f"{datetime.datetime.now(tz=datetime.timezone.utc).strftime('%Y%m%d_%H%M%S%f')}.json",
        )

        # save metric dictionnary to file
        with open(filename, "w", encoding="utf-8") as fileobj:
            json.dump(document_dict, fileobj, indent=4)

        # push data to database
        try:
            self.extract_from_file(filename, config)
        finally:
            os.remove(filename)

    def retry_probes(self, probes: List[InterfaceProbeData]) -> None:
        """Push retry to ko manager

        Args:
            probes (List[InterfaceProbeData]): probes to retry
        """
        for probe in probes:
            self.ko_manager.add_retry(
                ProbeRetry(interface=self.meta_dict[probe.interface_name], probe=probe)
            )

    @classmethod
    def build_http_probe_callable(cls, url) -> Callable:
        """Build a http probe callable

        Args:
            url (str): url to check

        Returns:
            typing.Callable: probe callable
        """

        def probe_callable(_, probe_data):
            cls.probe_http(url, probe_data)

        return probe_callable

    @classmethod
    def probe_http(cls, url, probe_data: InterfaceProbeData):
        """Probe http url

        Args:
            url: configuration
            probe_data: data to fill
        """
        response = requests.get(url, verify=False, timeout=120)

        probe_data.status_code = response.status_code

        if 200 <= response.status_code < 300:
            probe_data.status = "OK"
        else:
            probe_data.status = "KO"

    def exit_gracefully(self, signum, frame):
        super().exit_gracefully(signum, frame)
        self.logger.info("Shutting down KOManager")
        self.ko_manager.stop_retry()
        self.ko_manager.join()
        self.logger.info("KOManager shutdown OK")
