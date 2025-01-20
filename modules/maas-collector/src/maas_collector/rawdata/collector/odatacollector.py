"""Extract files from OData rest API"""

from dataclasses import dataclass, field
import datetime
import fnmatch
import os
import typing
from maas_model import datetime_to_zulu

from maas_collector.rawdata.collector.httpcollector import (
    HttpCollector,
    HttpConfiguration,
    HttpCollectorConfiguration,
)

from maas_collector.rawdata.collector.httpmixin import HttpMixin

from maas_collector.rawdata.collector.journal import (
    CollectorJournal,
)

from maas_collector.rawdata.collector.filecollector import FileCollectorConfiguration


from maas_collector.rawdata.collector.odata.v3impl import ODataQueryV3Implementation
from maas_collector.rawdata.collector.odata.v4impl import ODataQueryV4Implementation

from maas_collector.rawdata.collector.http.authentication import build_authentication

import maas_collector.rawdata.collector.tools.archivetools as archivetools


# Désactive la génération automatique de __repr__ pour pouvoir utiliser
# celui du parent qui masque les données sensible comme les mot de passe
@dataclass(repr=False)
class ODataCollectorConfiguration(HttpCollectorConfiguration):
    """Configuration for OData collection"""

    # product_url is now the generic product ....
    # ... url field for collector inherited from HTTCollectorConfiguration..
    # ... but for retrocompatibility, we check if odata_product_url is defined
    odata_product_url: str = ""

    odata_entities: str = "Products"

    # protocol_version is now the generic protocol version field ....
    # ... for collector inherited from HTTCollectorConfiguration..
    # ... but for retrocompatibility, we check if odata_version is defined
    odata_version: str = "v4"

    product_per_page: int = 1000

    odata_query_order_by: str = "PublicationDate asc"

    # ge for great equal : redundancy on the latest products but necessary to ensure continuity
    odata_query_filter: str = (
        "PublicationDate ge {publication_start_date} and "
        "PublicationDate le {publication_end_date}"
    )

    disable_insecure_request_warning: bool = False

    # the time interval between two refresh for this interface
    refresh_interval: int = 10

    odata_start_offset: int = 0

    odata_entity_location: str = "/odata/v1/"

    date_attr: str = "publication_date"

    filter_date_v3: str = "CreationDate"

    filter_date_v4: str = "PublicationDate"

    custom_query_suffix: str = ""

    # time offset in minutes
    end_date_time_offset: int = 15

    # Maximum time window in minutes
    max_time_window: int = 15

    # auth argument

    client_username: str = ""

    client_password: str = field(default="", metadata={"sensitive": True})

    token_url: str = ""

    client_id: str = ""

    client_secret: str = field(default="", metadata={"sensitive": True})

    scope: str = None

    grant_type: str = "password"

    download_file_pattern: list = field(default_factory=lambda: [])

    parent_file_pattern: str = None

    no_credential: bool = False

    oauth_basic_credential: str = ""

    list_of_files_to_retrieve: typing.List[str] = field(default_factory=lambda: [])

    list_of_files_to_retrieve_per_query: int = 10

    list_of_files_to_retrieve_query: str = ""

    def get_config_product_url(self):
        """Retrieve the product_url field from the collector configuration

        This function can be overloaded by child class in case their
        product url field is named differently and we do not want to break retrocompatibiliy

        Args:
            config (HttpConfiguration): dict of all collector configuration

        Raises:
            ValueError: The product url field either does not exist in configuration or several
            product url were founs

        Returns:
            str: value of the product_url field
        """
        if self.odata_product_url and not self.product_url:
            return self.odata_product_url
        elif self.product_url and not self.odata_product_url:
            return self.product_url
        else:
            raise ValueError(
                "Configuration file from collector shall either contain"
                " field odata_product_url or product_url and not both"
            )

    def get_config_protocol_version(self):
        """Retrieve the protocol version (eg:odata_version : 'v4')
        field from the collector configuration

        This function can be overloaded by child class in case their protocol
        version field is named differently
        and we do not want to break retrocompatibiliy

        Args:
            config (HttpConfiguration): dict of all collector configuration

        Raises:
            ValueError: The protocol version field either does not exist in
            configuration or several protocol version were founs

        Returns:
            str: value of the protocol version field
        """
        if self.protocol_version and not self.odata_version:
            return self.protocol_version
        elif self.odata_version and not self.protocol_version:
            return self.odata_version
        else:
            raise ValueError(
                "Configuration file from collector shall either contain"
                " field protocol_version or odata_version and not both"
            )

    def filename_match(self, name: str) -> bool:
        """Check if a filename matches the configuration

        parent_file_pattern is used to link a sub config to its main
        config without altering the file_pattern attribute.

        It allows to test independant parts of the collect pipeline
        (list files, d/l & untar, extract) without having to replay the whole pipeline

        Args:
            name ([str]): name of a file

        Returns:
            bool: True if the file is ok to be processed by the configuration extractor
        """
        if self.parent_file_pattern:
            return fnmatch.fnmatch(name, self.parent_file_pattern)
        elif self.file_pattern:
            return fnmatch.fnmatch(name, self.file_pattern)
        return False


@dataclass
class ODataConfiguration(HttpConfiguration):
    """Store OData configuration vars"""


class ODataCollector(HttpCollector, HttpMixin):
    """A collector that collect from a OData API.

    Could be one day refactored to more generic REST api collector.

    Warning: does not support redirect
    """

    CONFIG_CLASS = ODataCollectorConfiguration

    IMPL_DIR = {"v3": ODataQueryV3Implementation, "v4": ODataQueryV4Implementation}

    def ingest_all_interfaces(self):
        """Nominal ingestion from OData: collect all the OData configurations"""
        # iterate over all OData collector configurations
        for config in self.configs:
            if config.no_credential:
                # pseudo configuration for auxiliary ingestion, like downloaded files
                continue

            self.ingest_interface(CollectorJournal(config), config)

            if self.should_stop_loop:
                break

    def extract_from_file_download(
        self,
        result_download_files: list,
    ):
        """collect raw data from file downloaded and write to raw data database

        Args:
            result_download_files (list): list of download files
        Raises:
            RuntimeError: _description_
        """
        for file_path, config_download in result_download_files:
            try:
                self.extract_from_file(
                    file_path,
                    config_download,
                    report_name=os.path.basename(file_path),
                )

                self.on_ingest_success(file_path, config_download)

            except Exception as error:
                self.logger.error(
                    "[EXTRACTOR-ERROR]: fail to extract data from file downloaded: %s",
                    error,
                )
                raise RuntimeError("Extractor fail to ingest data") from error
            finally:
                # remove temporary file
                os.remove(file_path)

    def get_product_url(
        self, config: ODataCollectorConfiguration, product: dict
    ) -> str:
        """_summary_

        Args:
            config (ODataCollectorConfiguration): config of the collector
            product (dict): the product to =be downloaded

        Returns:
            str: _description_
        """

        product_id = product["Id"]

        query = (
            f"{config.get_config_product_url()}{config.odata_entity_location}"
            f"{config.odata_entities}('{product_id}')/$value"
        )

        # build query to get file content
        return query

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

    # pylint: disable=R0913
    # Parameters must be mandatory
    def odata_download_product(
        self, config, working_directory, http_session, url_list
    ) -> list:
        """download file from product

        Args:
            logger (Logger): collector logger
            working_directory (str):  working directory path
            config (ODataCollectorConfiguration): config of the collector
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
            self.logger.debug("Download file in odata interface : %s", url)
            self.logger.debug("url_list name %s", name)
            self.logger.debug("url_list url %s", url)

            # Get file product
            response = http_session.get(
                url, headers=headers, timeout=self.http_config.timeout
            )

            if not 200 <= response.status_code < 300:
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

            config_download_list = self.get_configurations(name)
            self.logger.debug("Filepath :%s", filepath)
            self.logger.debug("config download list :%s", config_download_list)
            for config_download in config_download_list:
                self.logger.debug(
                    "config download file_pattern :%s", config_download.file_pattern
                )
                self.logger.debug(
                    "config download file_pattern :%s",
                    config_download.file_pattern,
                )

                with open(filepath, "bw") as file_desc:
                    file_desc.write(response.content)

                # if file is a archive : unarchive
                ext = os.path.splitext(filepath)[1].lower()
                if ext == ".tgz":
                    self.logger.debug("Ext == tgz")
                    extract_files = archivetools.extract_files_in_tar(
                        self.logger,
                        filepath,
                        working_directory,
                        config_download.file_pattern,
                    )
                    self.logger.debug("extract_files :%s", extract_files)

                    for path_file in extract_files:
                        extract_files_and_config.append((path_file, config_download))

                    # remove tgz
                    os.remove(filepath)
                elif ext == ".zip":
                    self.logger.debug("Ext == zip")
                    extract_files = archivetools.extract_files_in_zip(
                        self.logger,
                        filepath,
                        working_directory,
                        config_download.file_pattern,
                    )

                    for path_file in extract_files:
                        extract_files_and_config.append((path_file, config_download))
                    # remove zip
                    os.remove(filepath)
                else:
                    self.logger.debug("Ext == %s", ext)

                    extract_files_and_config.append((filepath, config_download))

        return extract_files_and_config

    def match_file_pattern_with_product_name(self, data, config, file_pattern) -> list:
        """Match product names in the given data against a file pattern and return a list of matched names and URLs.

        Args:
            data (dict): The data containing product information.
            config (HttpCollectorConfiguration): The configuration for the HTTP collector.
            file_pattern (str): The file pattern to match against product names.

        Returns:
            list: A list of tuples containing matched product names and their corresponding URLs.
        """
        url_list = []
        for product in data["value"]:
            # check file pattern is matched
            if fnmatch.fnmatch(product["Name"].lower(), file_pattern.lower()):
                self.logger.debug("Download File pattern find : %s", product["Name"])

                url_list.append(
                    (
                        product["Name"],
                        self.get_product_url(config, product),
                    )
                )
        return url_list

    def post_process_data(self, data, filename, config, http_session) -> None:
        """Heritate from http collector

        Args:
            data (typing.Union[dict, bytes]): data collected from interface
            filename (str): name of the file which will be used when dumping collected data
            config (HttpCollectorConfiguration): configuration of the collector
            http_session (HttpMixin): initialized http session
        """

        if config.download_file_pattern:
            self.logger.debug("file pattern : %s", config.download_file_pattern)

            url_list = []
            if isinstance(config.download_file_pattern, str):
                file_pattern = config.download_file_pattern
                url_list = self.match_file_pattern_with_product_name(
                    data, config, file_pattern
                )
            elif isinstance(config.download_file_pattern, list):
                for file_pattern in config.download_file_pattern:
                    url_list += self.match_file_pattern_with_product_name(
                        data, config, file_pattern
                    )
            self.logger.debug("Url list :%s", url_list)
            # download file
            result_download_files = self.odata_download_product(
                config,
                self.args.working_directory,
                http_session,
                url_list,
            )

            self.extract_from_file_download(result_download_files)

    @classmethod
    def build_probe_query(cls, config: ODataCollectorConfiguration):
        """Heritate from http collector

        This method constructs a probe query URL based on the OData collector configuration,
        which includes the protocol version, entity location, filter criteria, and ordering.

        Args:
            config (ODataCollectorConfiguration): The configuration for the OData collector.

        Returns:
            str: The constructed probe query URL.

        Raises:
            KeyError: If the specified protocol version in the configuration is not recognized.
        """

        now_date = datetime.datetime.now(tz=datetime.UTC)

        previous_day = datetime_to_zulu(now_date - datetime.timedelta(days=1))

        probe_query_dict = {
            "v4": f"{config.get_config_product_url()}{config.odata_entity_location}"
            f"{config.odata_entities}?$filter={config.filter_date_v4} gt {previous_day}"
            f"&$top=1&$orderby={config.odata_query_order_by}",
            "v3": f"{config.get_config_product_url()}/odata/v1/"
            f"{config.odata_entities}?$filter={config.filter_date_v3} gt datetime'"
            f"{previous_day[:-1]}'&$top=1&$orderby=CreationDate desc",
        }

        return probe_query_dict[config.get_config_protocol_version()]

    @classmethod
    def attributs_url(cls):
        return super().attributs_url() + ["odata_product_url"]
