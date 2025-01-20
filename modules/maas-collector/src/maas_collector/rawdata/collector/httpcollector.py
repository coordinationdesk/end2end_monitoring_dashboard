"""Extract files from HTTP rest API"""

from dataclasses import dataclass, field
import datetime
import gc
import json
import os
from time import sleep
import typing


from urllib3.util.retry import Retry


from requests.adapters import HTTPAdapter

from maas_collector.rawdata.collector.filecollector import (
    CollectorArgs,
    FileCollector,
    FileCollectorConfiguration,
)

from maas_collector.rawdata.collector.httpmixin import HttpMixin

from maas_collector.rawdata.collector.journal import (
    CollectorJournal,
    CollectorReplayJournal,
    CollectingInProgressError,
    NoRefreshException,
)

from maas_collector.rawdata.replay import ReplayArgs

from maas_collector.rawdata.collector.http.abstract_query_strategy import (
    AbstractHttpQueryStrategy,
)

from maas_collector.rawdata.collector.http.authentication import build_authentication


# Désactive la génération automatique de __repr__ pour pouvoir utiliser
# celui du parent qui masque les données sensible comme les mot de passe
@dataclass(repr=False)
class HttpCollectorConfiguration(FileCollectorConfiguration):
    """Configuration for Http collection"""

    disable_insecure_request_warning: bool = False

    protocol_version: str = ""

    product_url: str = ""

    auth_method: str = ""

    token: str = field(default="", metadata={"sensitive": True})

    token_field_header: str = ""

    http_query_params: str = ""

    auth_timeout: int = 120

    def get_config_product_url(self):
        """Retrieve the product_url field from the collector configuration

        This function can be overloaded by child class in case their product url
        field is named differently and we do not want to break retrocompatibiliy

        Returns:
            str: product url field
        """
        return self.product_url

    def get_config_protocol_version(self):
        """Retrieve the version of the protocol (eg:odata_version : 'v4')
          field from the collector configuration

        This function can be overloaded by child class in case their
          protocol version fieldis named differently and we do not want to break retrocompatibiliy

        Returns:
            str: protocol_version field
        """
        return self.protocol_version


@dataclass
class HttpConfiguration:
    """Store Http configuration vars"""

    timeout: int = 120

    keep_files: bool = False


class HttpCollector(FileCollector, HttpMixin):
    """A collector that collect from a Http API.

    Could be one day refactored to more generic REST api collector.

    Warning: does not support redirect
    """

    CONFIG_CLASS = HttpCollectorConfiguration

    IMPL_DIR = {}

    def __init__(
        self,
        args: CollectorArgs,
        config: HttpConfiguration,
    ):
        super().__init__(args)
        self.http_config: HttpConfiguration = config

    def build_query_implementation(
        self, config, session, start_date, end_date, journal
    ) -> AbstractHttpQueryStrategy:
        """Factory method that builds the query implementation depending the version

        Args:
            config (HttpCollectorConfiguration): [description]
            session (Session): session for request
            start_date (Date): Begin date to query
            end_date (Date): Late date to query

        Raises:
            KeyError: If value not supported

        Returns:
            AbstractHttpQueryStrategy: Return the implementation of the http query API version
        """

        try:
            return self.IMPL_DIR[config.get_config_protocol_version()](
                self, config, session, start_date, end_date, journal
            )
        except KeyError as error:
            raise KeyError(
                f"Cannot find query query implementation for "
                f"version {config.get_config_protocol_version()}"
            ) from error

    def ingest(self, path=None, configs=None, force_update=None, report_folder=None):
        """Ingest from Http. All arguments are ignored so defaults to None"""
        if self.args.replay:
            self.ingest_replay(self.args.replay)
        else:
            self.ingest_all_interfaces()

    def ingest_replay(self, replay_args: ReplayArgs):
        """

        Re-run collect for an interface.

        Args:
            replay_args (ReplayArgs): replay options
        """
        # disable loop
        self.args.watch_period = 0

        configs = []

        # check the existence of the interfaces in the arguments and break if they are
        # not all defined
        for interface_name in replay_args.interface_name:
            config = self.get_configuration_by_interface_name(interface_name)

            if not config:
                raise ValueError(
                    f"Interface {interface_name} does not exists. "
                    f"Available interfaces: {self.get_interface_names()}"
                )

            configs.append(config)

        # ingest all wanted configurations
        for config in configs:
            self.logger.info(
                "Start replay for %s between %s and %s",
                config.interface_name,
                replay_args.start_date_arg,
                replay_args.end_date_arg,
            )

            finished_without_errors = False
            nb_retries = 0
            while not finished_without_errors:
                self._healthcheck.tick()

                try:
                    journal = CollectorReplayJournal(
                        config,
                        replay_args.start_date,
                        replay_args.end_date,
                        replay_args.suffix,
                        nb_of_retry=nb_retries,
                    )

                    start_date = replay_args.start_date

                    if journal.last_date and replay_args.start_date < journal.last_date:
                        self.logger.info(
                            "Journal replay last date %s is more recent than the replay "
                            "start date %s for interface %s, replay start date is now set"
                            " to the journal last date",
                            journal.last_date,
                            replay_args.start_date,
                            config.interface_name,
                        )
                        start_date = journal.last_date

                    self.ingest_interface(
                        journal, config, start_date, replay_args.end_date
                    )

                    finished_without_errors = True

                    journal.complete()
                except Exception as error:
                    self.logger.error(
                        "Replay error: %s Nb Of Retries:%s", error, nb_retries
                    )

                    if nb_retries >= replay_args.retry:
                        self.logger.error(
                            "Number of retry exhausted (%s): exiting",
                            nb_retries,
                        )
                        journal.nb_of_retry = nb_retries
                        break

                    nb_retries += 1
                    self.logger.info("Waiting 10s before retrying the replay")
                    sleep(10)

            if finished_without_errors:
                self.logger.info(
                    "Completed replay for %s between %s and %s",
                    config.interface_name,
                    replay_args.start_date_arg,
                    replay_args.end_date_arg,
                )
            else:
                self.logger.error(
                    "Failed replay for %s between %s and %s",
                    config.interface_name,
                    replay_args.start_date_arg,
                    replay_args.end_date_arg,
                )

            if self.should_stop_loop:
                break

    def ingest_all_interfaces(self):
        """Nominal ingestion from Http: collect all the Http configurations"""
        # iterate over all Http collector configurations
        for config in self.configs:
            self.ingest_interface(CollectorJournal(config), config)

            if self.should_stop_loop:
                break

    def ingest_interface(
        self,
        journal: typing.Union[CollectorJournal, CollectorReplayJournal],
        config: HttpCollectorConfiguration,
        start_date: datetime.datetime = None,
        end_date: datetime.datetime = None,
    ):
        """Ingest an interface

        Args:
            journal (typing.Union[CollectorJournal, CollectorReplayJournal]): journal
            config (HttpCollectorConfiguration): configuration
            start_date (datetime.datetime, optional): min date. Defaults to None.
            end_date (datetime.datetime, optional): max date. Defaults to None.
        """

        try:
            # use the journal as context to secure the concurent collect
            with journal:
                self._healthcheck.tick()
                self.ingest_http(config, journal, start_date, end_date)

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
            gc.collect()

    def ingest_http(
        self,
        config: HttpCollectorConfiguration,
        journal: CollectorJournal,
        start_date=None,
        end_date=None,
    ):
        """Ingest api

        Args:
            config (HttpCollectorConfiguration): configuration to ingest
        """

        with self.create_http_session(config) as http_session:
            http_implementation = self.build_query_implementation(
                config, http_session, start_date, end_date, journal
            )

            for page, products in enumerate(http_implementation):
                if self.should_stop_loop:
                    break

                self._healthcheck.tick()

                filename = http_implementation.get_filename(page)

                try:
                    self.save_in_file_and_extract(
                        products, filename, config, http_session, journal.iter_callback
                    )

                except RuntimeError as runtime_error:
                    # FIXME too abstract error: dig about network or data extraction
                    self.logger.error(
                        "[SKIP] Error during extract for page %s in %s: %s",
                        page,
                        config.interface_name,
                        runtime_error,
                    )
                    break

                # Conflict error can happen here: it will break current loop turn and
                # move to next interface as expected.
                # however, raw documents are saved and messages are sent even if partial
                # breaking here will provoke recollect of only one page
                journal.tick()

    def extract_from_file_download(
        self,
        result_download_files: list,
    ):
        """collect raw data from file downloaded and write to raw data database

        Args:
            result_download_files (list): list of download files
        Raises:
            RuntimeError: Extractor could not extract data from the file
        """

        for file_path, config_download in result_download_files:
            try:
                self.extract_from_file(
                    file_path,
                    config_download,
                    report_name=os.path.basename(file_path),
                )
            except Exception as error:
                self.logger.error(
                    "[EXTRACTOR-ERROR]: fail to extract data from file downloaded: %s",
                    error,
                )
                raise RuntimeError("Extractor fail to ingest data") from error
            finally:
                # remove temporary file
                os.remove(file_path)

    # Template method: child class may override and use argument and self
    # pylint: disable=unused-argument,no-self-use
    def post_process_data(
        self,
        data: typing.Union[dict, bytes],
        filename: str,
        config: HttpCollectorConfiguration,
        http_session: HttpMixin,
    ):
        """Function which can be rewritten by child class of http collector
        in order to perform additional operation after data collection and before data extraction

        Args:
            data (typing.Union[dict, bytes]): data collected from interface
            filename (str): name of the file which will be used when dumping collected data
            config (HttpCollectorConfiguration): configuration of the collector
            http_session (HttpMixin): initialized http session
        """

    def save_in_file_and_extract(
        self,
        data: typing.Union[dict, bytes],
        filename: str,
        config: HttpCollectorConfiguration,
        http_session: AbstractHttpQueryStrategy,
        iter_callback,
    ):
        """Save data in file, extract, and remove the file

        Args:
            data (Union[dict, bytes]): Data to store in a file and to be extracted
            filename (str): Name of the file which will contain the extracted data
            config (HttpCollectorConfiguration): config of the collector
        """

        self.post_process_data(data, filename, config, http_session)

        filepath = os.path.join(
            self.args.working_directory,
            filename,
        )

        try:
            with open(filepath, "w", encoding="UTF-8") as file_desc:
                if isinstance(data, bytes):
                    file_desc.write(data.decode("utf-8"))
                elif isinstance(data, dict):
                    json.dump(data, file_desc)
                else:
                    file_desc.write(data)

            # force report name as base url
            self.extract_from_file(
                filepath,
                config,
                report_name=config.get_config_product_url(),
                iter_callback=iter_callback,
            )

        except Exception as error:
            self.logger.error(
                "[EXTRACTOR-ERROR]: fail to extract data from file: %s", error
            )
            raise RuntimeError("Extractor fail to ingest data") from error

        finally:
            # Clear file
            if not self.http_config.keep_files:
                self.logger.debug("Deleting %s", filepath)
                os.remove(filepath)

    @classmethod
    def build_probe_query(cls, config: HttpCollectorConfiguration):
        """Build a query which will be used by the probe to check if collector is operational

        Args:
            config (HttpCollectorConfiguration): Collector configuration

        """
        # Abstract Class
        raise NotImplementedError()

    @classmethod
    def probe(
        cls, config: HttpCollectorConfiguration, probe_data: "InterfaceProbeData"
    ):
        """_summary_

        Args:
            config (HttpCollectorConfiguration): configuration of the collector
            probe_data (InterfaceProbeData): data to fill

        Raises:
            ValueError: The query of the interface led to a code not in range 200-300

        Returns:
            str: Returns OK string if query succeeded
        """
        with cls.create_http_session(config) as http_session:
            # no retry for probing
            retry = Retry(total=0, connect=0, backoff_factor=0)

            http_session.mount("http://", HTTPAdapter(max_retries=retry))
            http_session.mount("https://", HTTPAdapter(max_retries=retry))

            authentication = build_authentication(
                config.auth_method, config, http_session
            )

            headers = authentication.get_headers()

            response = http_session.get(
                cls.build_probe_query(config),
                headers=headers,
                timeout=config.auth_timeout,
            )

            probe_data.status_code = response.status_code

            if not 200 <= response.status_code < 300:
                raise ValueError(
                    f"Error {config.interface_name} returned {response.status_code}"
                )

        return "OK"

    @classmethod
    def attributs_url(cls):
        return super().attributs_url() + ["product_url", "token_url"]

    @classmethod
    def document(cls, config: HttpCollectorConfiguration):
        information = super().document(config)
        information |= {
            "protocol": "HTTP(S)",
            "auth_method": getattr(config, "auth_method", "No auth"),
        }

        if hasattr(config, "auth_method") and getattr(config, "auth_method"):
            information |= {"auth_user": getattr(config, "client_username")}

        return information
