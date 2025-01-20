"""Extract mission planning files"""

from dataclasses import dataclass, field
import fnmatch

from maas_collector.rawdata.collector.httpcollector import (
    HttpCollector,
    HttpCollectorConfiguration,
    HttpConfiguration,
)

from maas_collector.rawdata.collector.httpmixin import HttpMixin

from maas_collector.rawdata.collector.mpip.v1_impl import (
    MpipQueryV1Implementation,
)

from maas_collector.rawdata.collector.http.authentication import build_authentication

import maas_collector.rawdata.collector.tools.archivetools as achivetools
import os


@dataclass
class MpipCollectorConfiguration(HttpCollectorConfiguration):
    """Configuration for Mpip Collector Configuration"""

    date_attr: str = "ingestion_date"

    refresh_interval: int = 10

    file_list_url: str = ""

    probe_url: str = ""

    mpip_start_offset: int = 0

    end_date_time_offset: int = 0

    protocol_version: str = "v1"

    product_per_page: int = 20

    download_file_pattern: str = None

    # Query filters

    filetypes: list = None

    extensions: list = None

    platforms: list = None

    fileclasses: list = None

    filenames: list = None

    session_ids: list = None

    versions: list = None

    actives: list = field(default_factory=lambda: ["true"])

    edrs_creation_date: str = None

    ingestion_date: str = None

    # auth argument

    client_username: str = ""

    client_password: str = ""

    token_url: str = ""

    client_id: str = ""

    client_secret: str = ""

    scope: str = None

    grant_type: str = "password"


@dataclass
class MpipConfiguration(HttpConfiguration):
    """Store Mpip configuration vars"""


class MpipCollector(HttpCollector, HttpMixin):
    """A Mpip collector that collect from the mpip interface."""

    CONFIG_CLASS = MpipCollectorConfiguration

    IMPL_DIR = {"v1": MpipQueryV1Implementation}

    def post_process_data(self, data, filename, config, http_session):
        if config.download_file_pattern:
            url_list = []

            for product in data:
                # check file pattern is matched

                if fnmatch.fnmatch(product["filename"], config.download_file_pattern):
                    self.logger.debug(
                        "Download File pattern find : %s", product["filename"]
                    )

                    url_list.append(
                        (
                            product["filename"],
                            config.get_config_product_url(),
                        )
                    )
            if len(url_list) > 0:
                # download file
                result_download_files = self.download_product(
                    config,
                    self.args.working_directory,
                    http_session,
                    url_list,
                )

                self.extract_from_file_download(result_download_files)

    # pylint: disable=R0913
    # Parameters must be mandatory
    def download_product(
        self, config, working_directory, http_session, url_list
    ) -> list:
        """download file from product

        Args:
            logger (Logger): collector logger
            working_directory (str):  working directory path
            config (MpipCollectorConfiguration): config of the collector
            http_session (Session): http session
            headers (_type_): authentication header
            product (dict): product

        Raises:
            ValueError: _description_

        Returns:
            list: path list of file downloaded
        """

        extract_files_and_config = []

        authentication = build_authentication(config.auth_method, config, http_session)

        headers = authentication.get_headers()

        for name, url in url_list:
            self.logger.debug("Download file in interface : %s", url)
            # Get file product
            response = http_session.get(
                f"{url}{name}", headers=headers, timeout=self.http_config.timeout
            )

            if not 200 <= response.status_code <= 300:
                # serious problem
                self.logger.error(
                    "Error querying %s %d: %s",
                    url,
                    response.status_code,
                    response.content,
                )
                raise ValueError(f"Error querying {url}")

            # put data in file at working_directory
            filepath = os.path.join(working_directory, name)

            # plus
            with open(filepath, "bw") as file_desc:
                file_desc.write(response.content)

            extract_files = achivetools.extract_files_in_tar(
                self.logger,
                filepath,
                working_directory,
                config.file_pattern,
            )

            for path_file in extract_files:
                extract_files_and_config.append((path_file, config))

            # remove tgz
            os.remove(filepath)

            return extract_files_and_config

    @classmethod
    def build_probe_query(cls, config: MpipCollectorConfiguration):
        """Creation of a query which will be sent to the mpip API to check if it is online

        Args:
            config (MpipCollectorConfiguration): Configuration of the collector

        Returns:
            str: query
        """

        return config.probe_url

    @classmethod
    def attributs_url(cls):
        return super().attributs_url() + ["file_list_url"]

    @classmethod
    def document(cls, config: MpipCollectorConfiguration):
        information = super().document(config)

        return information
