"""Extract files from Webdav"""

from dataclasses import dataclass, field
import json
import os
import requests

from requests.adapters import HTTPAdapter

from maas_collector.rawdata.collector.journal import (
    CollectorJournal,
    CollectingInProgressError,
    NoRefreshException,
)

from maas_collector.rawdata.collector.webdav.webdavclient import WebDAVClient
from maas_collector.rawdata.collector.filecollector import (
    CollectorArgs,
    FileCollector,
    FileCollectorConfiguration,
)

from maas_collector.rawdata.collector.httpmixin import HttpMixin

from maas_collector.rawdata.collector.http.authentication import build_authentication


# Désactive la génération automatique de __repr__ pour pouvoir utiliser
# celui du parent qui masque les données sensible comme les mot de passe
@dataclass(repr=False)
class WebDAVCollectorConfiguration(FileCollectorConfiguration):
    """Configuration for Webdav collector"""

    client_url: str = ""

    file_pattern: str = "*"

    depth: str = "infinity"

    auth_method: str = ""

    token_field_header: str = ""

    client_username: str = ""

    client_password: str = field(default="", metadata={"sensitive": True})

    interface_name: str = ""

    directories: list = None

    disable_insecure_request_warning: bool = False

    refresh_interval: int = 0


@dataclass
class WebDAVConfiguration:
    """Store WebDav configuration vars"""

    timeout: int


class WebDAVCollector(FileCollector, HttpMixin):
    """A collector who collect file from a webdav server"""

    CONFIG_CLASS = WebDAVCollectorConfiguration

    def __init__(
        self,
        args: CollectorArgs,
        webdav_config: WebDAVConfiguration,
    ):
        super().__init__(args)
        self.webdav_config: WebDAVConfiguration = webdav_config

    def ingest(self, path=None, configs=None, force_update=None):
        """Ingest from WebDAV. All arguments are ignored so defaults to None
        @
                Args:
                    path (_type_, optional): _description_. Defaults to None.
                    configs (_type_, optional): _description_. Defaults to None.
                    force_update (_type_, optional): _description_. Defaults to None.
        """
        # iterate over all WebDAV collector configurations
        for config in self.configs:
            if self.should_stop_loop:
                break

            try:
                # use the journal as context to secure the concurent collect
                with CollectorJournal(config) as journal:
                    self.ingest_webdav(config, journal)

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
            # Don't break the loop
            # pylint: disable=W0703
            except Exception as error:
                self.logger.exception(error)
            finally:
                # flush messages between interfaces as they don't ingest the same data
                self._flush_message_groups()

    def ingest_webdav(
        self, config: WebDAVCollectorConfiguration, journal: CollectorJournal
    ):
        """Ingest webdav file

        Args:
            config (WebDAVCollectorConfiguration): configuration to use
        """
        self._healthcheck.tick()
        local_session = self.create_http_session(config)

        webdav_client = WebDAVClient(self.webdav_config.timeout, config, local_session)

        nb_file_to_ingest = 0
        nb_ingested_file = 0

        try:
            new_last_date = None

            for filename, last_date in webdav_client.propfind(journal.last_date):
                if self.should_stop_loop:
                    break

                file_content = webdav_client.get_file(filename)

                self._healthcheck.tick()

                self.logger.debug(
                    "[%s] Find file %s",
                    config.interface_name,
                    filename,
                )

                nb_file_to_ingest += 1

                try:
                    report_name = os.path.basename(filename)
                    report_folder = os.path.abspath(os.path.dirname(filename))

                    self.save_in_file_and_extract(
                        file_content,
                        report_name,
                        config,
                        None,
                        report_folder=report_folder,
                    )
                    nb_ingested_file += 1
                except RuntimeError as runtime_error:
                    self.logger.error(
                        "[%s][CONTINUE] Error during extract for file %s: %s",
                        config.interface_name,
                        filename,
                        runtime_error,
                    )
                    continue

                if new_last_date is None or last_date > new_last_date:
                    new_last_date = last_date

                journal.tick()

            # set last date
            if new_last_date is not None:
                journal.last_date = new_last_date

        except ConnectionError as connection_error:
            self.logger.error(
                "[%s][SKIP] Connection error : %s -> %s",
                config.interface_name,
                config.client_url,
                connection_error,
            )

        except ValueError as value_error:
            self.logger.error(
                "[%s][SKIP] Value error : %s -> %s",
                config.interface_name,
                config.client_url,
                value_error,
            )

        finally:
            local_session.close()
            self.logger.info(
                "[%s][STATS] Ingested : %d / %d",
                config.interface_name,
                nb_file_to_ingest,
                nb_ingested_file,
            )

    def save_in_file_and_extract(
        self, data, report_name, config, iter_callback, report_folder=""
    ):
        """Save data in file

        Args:
            data (bytes|str|dict): Data to safe in file
            report_name (str): report_name of the data stored
            config (WebDAVCollectorConfiguration): Collector config

        Raises:
            RuntimeError: If extractor crash during extraction
        """

        filepath = os.path.join(
            self.args.working_directory,
            report_name,
        )

        try:
            if isinstance(data, bytes):
                with open(filepath, "wb") as file_desc:
                    file_desc.write(data)
            else:
                with open(filepath, "w", encoding="utf-8") as file_desc:
                    if isinstance(data, dict):
                        json.dump(data, file_desc)
                    else:
                        file_desc.write(data)

            # force report name as base url
            self.extract_from_file(
                filepath,
                config,
                report_name=report_name,
                report_folder=report_folder,
                iter_callback=iter_callback,
            )

        except Exception as error:
            self.logger.error(
                "[EXTRACTOR-ERROR]: fail to extract data from file: %s", error
            )
            raise RuntimeError("Extractor fail to ingest data") from error

        finally:
            # Clear file
            os.remove(filepath)

    @classmethod
    def probe(cls, config: WebDAVCollectorConfiguration, probe_data):
        with cls.create_http_session(config) as http_session:
            http_session.mount("https://", HTTPAdapter(max_retries=0))
            http_session.mount("http://", HTTPAdapter(max_retries=0))

            authentication = build_authentication(
                config.auth_method, config, http_session
            )
            target_urls = []
            if config.directories:
                for directory in config.directories:
                    target_urls.append(f"{config.client_url}/{directory}")
            else:
                target_urls.append(config.client_url)

            for target_url in target_urls:
                prepared_request = requests.Request(
                    "PROPFIND",
                    target_url,
                    headers=authentication.get_headers() | {"Depth": "0"},
                ).prepare()

                response = http_session.send(prepared_request, timeout=120)

                probe_data.status_code = response.status_code

                if not 200 <= response.status_code < 300:
                    raise ValueError(f"{response.content}")

    @classmethod
    def attributs_url(cls):
        return super().attributs_url() + ["client_url", "token_url"]

    @classmethod
    def document(cls, config: WebDAVClient):
        information = super().document(config)
        information |= {
            "protocol": "HTTP(S) - WebDAV",
            "auth_method": getattr(config, "auth_method", "No auth"),
            "auth_user": getattr(config, "client_username"),
        }
        return information
