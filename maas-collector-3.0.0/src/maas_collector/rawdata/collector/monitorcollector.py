"""contains a collector for monitoring interfaces"""

import dataclasses
import datetime
import json
import os
import typing

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

    interfaces: list = None

    refresh_interval: int = 300

    extra_http_probes: list = None


@dataclasses.dataclass
class InterfaceMonitorConfiguration:
    """Specific command line arguments"""

    interface_name: str = ""


@dataclasses.dataclass
class InterfaceMeta:
    """Meta information about an interface"""

    name: str = ""

    configuration_path: str = ""

    config: FileCollectorConfiguration = None

    probe_callable: typing.Callable = None


@dataclasses.dataclass
class InterfaceProbeData:
    """store monitoring attributes"""

    interface_name: str

    probe_time_start: str = None

    probe_time_end: str = None

    probe_duration: int = None

    status: str = None

    status_code: int = 0

    details: str = None

    most_recent_modification_date: str = None


class InterfaceMonitor(FileCollector, CredentialMixin):
    """A collector that probes status for interfaces"""

    CONFIG_CLASS = InterfaceMonitorCollectorConfiguration

    def __init__(
        self, args: CollectorArgs, monitor_config: InterfaceMonitorConfiguration
    ):
        super().__init__(args)

        self.monitor_config = monitor_config

        self.meta_list: list[InterfaceMeta] = []

        self.last_modification_date_dict: dict = None

    def setup(self):
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

        # load the configurations of the interfaces to monitor
        for config_path in find_configurations(self.args.rawdata_config_dir):
            with open(config_path, encoding="UTF-8") as conf_obj:
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

                self.meta_list.append(interface_meta)

        # additionnal http probes
        for config in self.configs:
            if not config.extra_http_probes:
                continue

            for http_meta in config.extra_http_probes:
                # generate pseudo interface meta
                self.meta_list.append(
                    InterfaceMeta(
                        name=http_meta["interface_name"],
                        probe_callable=self.build_http_probe_callable(http_meta["url"]),
                    )
                )

        self.meta_list.sort(key=lambda itf: itf.name)

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

        probe_data = InterfaceProbeData(interface_meta.name)

        probe_time_start = datetime.datetime.now(tz=datetime.timezone.utc)

        try:
            interface_meta.probe_callable(interface_meta.config, probe_data)

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

            self.logger.warning("%s: %s", interface_meta.name, error)

        # pylint: enable=W0703

        probe_time_end = datetime.datetime.now(tz=datetime.timezone.utc)

        probe_data.probe_time_start = datetime_to_zulu(probe_time_start)

        probe_data.probe_time_end = datetime_to_zulu(probe_time_end)

        duration = probe_time_end - probe_time_start

        probe_data.probe_duration = duration.total_seconds()

        probe_data.most_recent_modification_date = datetime_to_zulu(
            self.last_modification_date_dict.get(interface_meta.name)
        )

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

        # use a thread pool for parallel probing. As this activity consists in waiting
        # for a response from network, the GIL is release and this does not require
        # real parallel processing
        # max pool size depend of the kernel, but 256 is a common limit
        pool = ThreadPool(min((len(self.meta_list), 256)))

        # create a dictionnary structure to later create json document
        document_dict = {
            "results": [
                dataclasses.asdict(data)
                for data in pool.map(self.run_probe, self.meta_list)
            ]
        }

        # generate a consistant filename
        filename = os.path.join(
            self.args.working_directory,
            "MAAS-Monitoring-"
            f"{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S%f')}.json",
        )

        # save metric dictionnary to file
        with open(filename, "w", encoding="utf-8") as fileobj:
            json.dump(document_dict, fileobj, indent=4)

        # push data to database
        try:
            self.extract_from_file(filename, config)
        finally:
            os.remove(filename)

        self._healthcheck.tick()

        # store the most recent modification date of all interface as global
        # modification date
        last_modification_values = [
            value for value in self.last_modification_date_dict.values() if value
        ]
        if last_modification_values:
            journal.last_date = max(last_modification_values)

    @classmethod
    def build_http_probe_callable(cls, url) -> typing.Callable:
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
