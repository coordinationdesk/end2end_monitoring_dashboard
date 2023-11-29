""" WebDAV Client """
import fnmatch
import logging
import os
from urllib.parse import urljoin
import urllib
from xml.dom.minidom import Element
import xml.etree.ElementTree as ET

import requests

import dateutil.tz
from dateutil import parser

from maas_collector.rawdata.collector.http.authentication import build_authentication


class WebDAVClient:
    """Webdav client to find and get file"""

    def __init__(
        self,
        timeout,
        config,
        http_session=None,
    ) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

        self.timeout = timeout

        self.client_url = config.client_url

        self.file_pattern = config.file_pattern

        self.depth = config.depth

        self.directories = config.directories

        self.http_session = http_session

        self.authentication = build_authentication(
            config.auth_method, config, self.http_session
        )

    def get_file(self, filename):
        """GET WebDAV method

        Args:
            filename (str): File to retrieve

        Returns:
            bytes: response content
        """

        file_url = urljoin(self.client_url, filename)

        headers = self.authentication.get_headers()

        self.logger.debug("http_session.get(): %s", file_url)

        response = self.http_session.get(
            file_url, headers=headers, timeout=self.timeout
        )

        return response.content

    def propfind(
        self,
        modification_date=None,
    ):
        """PROPFIND WebDAV method

        Args:
            modification_date (date, optional): Older modification date. Defaults to None.

        Returns:
            iterator: List of filename fitting date and pattern
        """
        propfind_headers = {"Depth": self.depth}

        headers = propfind_headers | self.authentication.get_headers()

        namespaces = {"D": "DAV:", "lp1": "DAV:"}

        all_files = self.get_all_files(headers, namespaces)

        for file_el in all_files:
            propstat = file_el.find("D:propstat", namespaces)
            href = file_el.find("D:href", namespaces)

            href_value = href.text

            filename = href_value.rsplit("/", 1)[-1]

            if filename.startswith("."):
                self.logger.debug("Ignoring file starting with dot: %s", filename)
                continue

            self.logger.debug(
                "Testing if %s matches %s base: %s",
                href_value,
                self.file_pattern,
                filename,
            )

            if fnmatch.fnmatch(filename, self.file_pattern):
                self.logger.debug("Extracting %s from %s", href_value, self.client_url)

                prop = propstat.find("D:prop", namespaces)

                file_modification_date_d = prop.find("D:modificationdate", namespaces)
                file_modification_date_lp1 = prop.find(
                    "lp1:getlastmodified", namespaces
                )

                file_modification_date = None

                if not file_modification_date_d:
                    file_modification_date = file_modification_date_d

                if not file_modification_date_lp1:
                    file_modification_date = file_modification_date_lp1

                if not file_modification_date:
                    file_modification_date_parse = parser.parse(
                        file_modification_date.text
                    )

                    # Add file : No filter date or newer than modification date
                    if (
                        modification_date is None
                        or file_modification_date_parse
                        > modification_date.replace(tzinfo=dateutil.tz.UTC)
                    ):
                        yield (href_value, file_modification_date_parse)
                else:
                    yield (href_value, None)

            else:
                self.logger.debug(
                    "%s does not match %s base: %s",
                    href_value,
                    self.file_pattern,
                    href_value.rsplit("/", 1)[-1],
                )

    def get_all_files(
        self,
        headers: dict,
        namespaces: dict,
    ) -> list:
        """Get all file in directory

        Args:
            headers (dict): headers for http connection
            namespaces (dict): namespaces webdav

        Returns:
            list: files
        """

        all_files = []

        if self.depth != "infinity":
            if self.directories is None:
                all_files = self.get_files_in_directory_depth_1(
                    headers,
                    namespaces,
                    "",
                )
            else:
                for directory in self.directories:
                    all_files += self.get_files_in_directory_depth_1(
                        headers,
                        namespaces,
                        directory,
                    )
        else:
            if self.directories is None:
                all_files = self.get_files_in_directory_depth_infinity(
                    headers, namespaces, ""
                )
            else:
                for directory in self.directories:
                    all_files += self.get_files_in_directory_depth_infinity(
                        headers, namespaces, directory
                    )

        return all_files

    def get_files_in_directory_depth_infinity(
        self,
        headers: dict,
        namespaces: dict,
        directory: str,
    ) -> list:
        """Get all file in directory for depth infinity

        Args:
            headers (dict): headers for http connection
            namespaces (dict): namespaces webdav
            directory (list): list of directory
        Raises:
            ValueError: error query
        Returns:
            list: list of file
        """

        # Prepped request to set custom HTTPVERB

        req = requests.Request(
            "PROPFIND", os.path.join(self.client_url, directory), headers=headers
        )

        prepped_req = req.prepare()

        response = self.http_session.send(prepped_req, timeout=self.timeout)

        if not 200 <= response.status_code < 300:
            # serious problem
            self.logger.error(
                "Error querying %s %d: %s",
                self.client_url,
                response.status_code,
                response.content,
            )
            raise ValueError(f"Error querying {self.client_url}")

        root = ET.fromstring(response.text)

        return root.findall("D:response", namespaces)

    def get_files_in_directory_depth_1(
        self,
        headers: dict,
        namespaces: dict,
        directory: str,
    ) -> list:
        """Get all file in directory for depth 1

        Args:
            headers (dict): headers for http connection
            namespaces (dict): namespaces webdav
            directory (str): directory

        Returns:
            list: list of file
        """
        list_file_el = []
        list_directory = [directory]

        path_url = urllib.parse.urlparse(self.client_url)[2]

        # get all file in directory list
        while list_directory:
            # pop the directory and inspect them
            directory_el = list_directory.pop()

            root = self.get_root_depth_1(headers, directory_el)

            # get all file or directory in directory

            for file_or_directory in root.findall("D:response", namespaces):
                propstat = file_or_directory.find("D:propstat", namespaces)

                prop = propstat.find("D:prop", namespaces)
                resourcetype = prop.find("lp1:resourcetype", namespaces)

                collection = resourcetype.find("D:collection", namespaces)

                # check element is directory or file
                if collection is not None:
                    # add new directory
                    href = file_or_directory.find("D:href", namespaces).text

                    new_directory = os.path.relpath(href, path_url)

                    if (
                        new_directory != "."
                        and new_directory != directory_el
                        and new_directory != f"{directory_el}/"
                        and f"{new_directory}/" != directory_el
                    ):
                        list_directory.append(new_directory)
                    else:
                        self.logger.debug(
                            "Skip this directory: it is like the current %s : %s",
                            directory_el,
                            new_directory,
                        )
                else:
                    href = file_or_directory.find("D:href", namespaces)

                    self.logger.debug(
                        "WEBDAV DEPTH 1: file added to treatemment : %s", href.text
                    )
                    # add new file
                    list_file_el.append(file_or_directory)

        return list_file_el

    def get_root_depth_1(
        self,
        headers: dict,
        directory_el: str,
    ) -> Element:
        """Get root directory

        Args:
            headers (dict): headers for http connection
            directory_el (str): directory

        Raises:
            ValueError: error query request

        Returns:
            Elemennt: root
        """

        new_url = os.path.join(self.client_url, directory_el)

        req = requests.Request("PROPFIND", new_url, headers=headers)

        prepped_req = req.prepare()

        response = self.http_session.send(prepped_req, timeout=self.timeout)

        if not 200 <= response.status_code < 300:
            # serious problem
            self.logger.error(
                "Error querying %s %d: %s",
                self.client_url,
                response.status_code,
                response.content,
            )
            raise ValueError(f"Error querying {self.client_url}")

        return ET.fromstring(response.text)
