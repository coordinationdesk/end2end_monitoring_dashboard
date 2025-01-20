"""Extract files from FTP server"""

import datetime
import fnmatch
import ftplib
import os
import time
import typing
from collections import namedtuple
from dataclasses import dataclass, field

import dateutil.parser
import maas_collector.rawdata.collector.tools.archivetools as achivetools
from dateutil.relativedelta import relativedelta
from maas_collector.rawdata.collector.filecollector import (
    CollectorArgs,
    FileCollector,
    FileCollectorConfiguration,
)
from maas_collector.rawdata.collector.journal import (
    CollectingInProgressError,
    CollectorJournal,
    NoRefreshException,
)


# Désactive la génération automatique de __repr__ pour pouvoir utiliser
# celui du parent qui masque les données sensible comme les mot de passe
@dataclass(repr=False)
class FTPCollectorConfiguration(FileCollectorConfiguration):
    """Configuration for FTP collection"""

    directories: list = None

    refresh_interval: int = 10

    ftp_hostname: str = ""

    client_port: int = 21

    client_username: str = ""

    client_password: str = field(default="", metadata={"sensitive": True})

    timeout: int = 120

    recurse: bool = False


# collector configuration class needs many attributes
@dataclass
class FTPConfiguration:
    """Store FTP configuration vars"""

    credential_file: str = ""


# a named tuple to describe remote file entries for ingestion
FTPIngestionEntry = namedtuple(
    "FTPIngestionEntry", ("path", "modification_date", "configs", "is_archive")
)


class FTPCollector(FileCollector):
    """A collector that collect from a FTP server"""

    CONFIG_CLASS = FTPCollectorConfiguration

    def __init__(
        self,
        args: CollectorArgs,
        ftp_config: FTPConfiguration,
    ):
        super().__init__(args)

        self.ftp_config: FTPConfiguration = ftp_config

        # pyftp connection
        self._ftp: ftplib.FTP_TLS = None

    @classmethod
    def build_connection(cls, config: FTPCollectorConfiguration) -> ftplib.FTP_TLS:
        """Create a ftp transport

        Args:
            config (FTPCollectorConfiguration): configuration

        Returns:
            ftplib.FTP_TLS: connection
        """
        ftp = ftplib.FTP_TLS()

        ftp.connect(
            config.ftp_hostname,
            config.client_port,
            timeout=config.timeout,
        )

        ftp.login(config.client_username, config.client_password)

        return ftp

    def clear_ftp_connection(self):
        """Explicit connection shutdown"""
        if self._ftp:
            try:
                self._ftp.quit()
            except ftplib.all_errors as error:
                self.logger.error("Error FTP quit : %s", error)

            self._ftp = None

    def ingest(self, path=str, configs=None, force_update=None):
        """Ingest from ftp server. All arguments are ignored so defaults to None"""
        # iterate over collector configurations

        for config in self.configs:
            # handle termination
            if self.should_stop_loop:
                break

            if not config.ftp_hostname:
                # auxiliary configuration
                continue

            self._healthcheck.tick()

            try:
                self._ftp = self.build_connection(config)
            except ftplib.all_errors as error:
                self.logger.error(
                    "Cannot build FTP connection. interface_name=%s ; error: %s",
                    config.interface_name,
                    error,
                )
                continue

            try:
                # use the journal as context to secure the concurent collect
                with CollectorJournal(config) as journal:
                    entries = []

                    journal.tick()

                    self._healthcheck.tick()

                    # retrieve all entries in all directories
                    for directory in config.directories:
                        if self.should_stop_loop:
                            break

                        entries.extend(
                            self.get_remote_file_list(
                                directory, journal.last_date, config.recurse
                            )
                        )

                    # sort by modification time asc to handle
                    entries.sort(key=lambda entry: entry.modification_date)

                    self.logger.info(
                        "Found %d FTP entries to ingest from last date %s",
                        len(entries),
                        journal.last_date,
                    )

                    for entry in entries:
                        # handle termination
                        if self.should_stop_loop:
                            break

                        self._healthcheck.tick()

                        self.ingest_ftp_file(config, entry.path, force_update)

                        journal.last_date = entry.modification_date

                        journal.tick()

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
            except Exception as error:
                self.logger.error(
                    "Failed get file list in FTP server %s : %s",
                    config.interface_name,
                    error,
                )
                raise

            finally:
                self.clear_ftp_connection()

    def ingest_ftp_file(self, config, remote_path: str, force_update=False):
        """Ingest a remote file

        Args:
            config (FTPCollectorConfiguration): config of the collector
            remote_path (str): remote file path
            force_update (bool, optional): force new document. Defaults to False.
        """

        try:
            basename = os.path.basename(remote_path)

            dest_url = os.path.join(self.args.working_directory, basename)

            try:
                self.download(remote_path, dest_url)
            except BrokenPipeError:
                self.logger.warning("BrokenPipeError while downloading %s", remote_path)
                self.clear_ftp_connection()
                self._ftp = self.build_connection(config)
                self.logger.info("Trying to dowload %s again", remote_path)
                # try again
                self.download(remote_path, dest_url)

            except Exception as error:
                self.logger.error("Failed do download file FTP server : %s", error)
                raise

            extract_files = []

            ext = os.path.splitext(dest_url)[1].lower()
            if ext == ".tgz":
                # extract only files that respect the file pattern
                extract_files = achivetools.extract_files_in_tar(
                    self.logger,
                    dest_url,
                    self.args.working_directory,
                    config.file_pattern,
                )
                # remove tgz
                os.remove(dest_url)
            elif ext == ".zip":
                # extract only files that respect the file pattern
                extract_files = achivetools.extract_files_in_zip(
                    self.logger,
                    dest_url,
                    self.args.working_directory,
                    config.file_pattern,
                )
                # remove zip
                os.remove(dest_url)
            else:
                if fnmatch.fnmatch(dest_url, config.file_pattern):
                    extract_files.append(dest_url)
                else:
                    os.remove(dest_url)

            # ingest the parent file using FileCollector
            for file_name in extract_files:
                # Ingest file
                try:
                    # force report name as base url
                    self.extract_from_file(
                        file_name,
                        config,
                        report_name=os.path.basename(file_name),
                        report_folder=os.path.abspath(os.path.dirname(remote_path)),
                        force_update=force_update,
                    )

                    self.on_ingest_success(file_name, config)

                except RuntimeError as runtime_error:
                    self.logger.error(
                        "[SKIP] Error during extract for file  %s in %s: %s",
                        file_name,
                        config.interface_name,
                        runtime_error,
                    )
                    break

                finally:
                    # remove temporary file
                    os.remove(file_name)

        # catch broad exception to not break the file processing loop
        # pylint: disable=W0703
        except Exception as error:
            self.logger.error("Cannot ingest %s", remote_path)
            self.logger.exception(error)
        finally:
            self._flush_message_groups()

    def get_remote_file_list(
        self, path: str, min_date=None, recurse=False
    ) -> typing.Generator[FTPIngestionEntry, None, None]:
        """generator of FTPIngestionEntry instances using DIR on current ftp

        A ftp dir entry looks like:
        'drwxr-xr-x    4 1001     1001     42 Nov 22 08:47 DCS_01_L20220922133921691000230_dat'

        Args:
            path (str): path on the current ftp server
            min_date (datetime): minimum date of the entries
            recurse (bool): recurse through sub directories

        """

        lines = []

        try:
            self.logger.debug("CWD %s", path)
            self._ftp.cwd(path)

            self.logger.debug("DIR %s", path)
            self._ftp.dir(path, lines.append)
        except ftplib.all_errors as error:
            self.logger.error("Error FTP directory listing %s: %s", path, error)
            raise

        self.logger.debug("Found %d entries in %s", len(lines), path)

        for line in lines:
            tokens = line.split(maxsplit=9)

            # get file name
            filename = tokens[8]

            # get modification date
            time_str = tokens[5] + " " + tokens[6] + " " + tokens[7]

            modification_date = dateutil.parser.parse(time_str).astimezone(
                dateutil.tz.UTC
            )

            # Some servers send time only for file newer than 6 months
            if ":" in tokens[7]:
                if modification_date >= datetime.datetime.now(datetime.timezone.utc):
                    modification_date = modification_date - relativedelta(years=1)

            if min_date:
                if modification_date <= min_date:
                    # logging is commented out because of the potential large volume
                    # self.logger.debug("Skipping too old entry: %s", filename)
                    continue
            else:
                self.logger.info(
                    "get_remote_file_list: no minimum date provided for %s", path
                )

            path_file = os.path.join(path, filename)

            if line[0] == "d":
                self.logger.debug("Found directory: %s", path_file)
                if recurse:
                    self.logger.debug("Recurse through directory: %s", path_file)
                    yield from self.get_remote_file_list(path_file, min_date, recurse)
                else:
                    self.logger.debug(
                        "Won't recurse through directory %s: recurse flag not set",
                        path_file,
                    )
                    continue

            if os.path.splitext(filename)[1].lower() in (".tgz", ".zip"):
                # FIXME filter out archive
                self.logger.debug(
                    "Adding %s because mtime %s > journal %s",
                    path_file,
                    modification_date,
                    min_date,
                )
                yield FTPIngestionEntry(path_file, modification_date, [], True)

            else:
                # check file validate the file pattern
                found_configs = self.get_configurations(filename)
                if found_configs:
                    yield FTPIngestionEntry(
                        path_file, modification_date, found_configs, False
                    )

    def download(self, remote_path: str, local_path: str):
        """Download remote file and log network speed

        Args:
            remote_path ([str]): file path on ftp
            local_path ([str]): file path on local storage
        """

        self.logger.debug("Downloading %s to %s ", remote_path, local_path)

        start_time = time.time()

        # DownLoads file
        with open(local_path, "wb") as file:
            self._ftp.retrbinary(f"RETR {remote_path}", file.write)

        dowload_duration = time.time() - start_time

        size = os.path.getsize(local_path)

        self.logger.info(
            "Downloaded %s %d bytes in %f seconds at %.2fKB/s",
            remote_path,
            size,
            dowload_duration,
            size / 1024 / dowload_duration,
        )

    @classmethod
    def probe(cls, config: FTPCollectorConfiguration, probe_data):
        # test connection
        try:
            ftp = cls.build_connection(config)
            config.status = "OK"

            # list directories
            for directory in config.directories:
                # just check if directory exists by CWD
                ftp.cwd(directory)

            ftp.quit()

        except ftplib.all_errors as error:
            config.status = "KO"
            raise error

    @classmethod
    def attributs_url(cls):
        return super().attributs_url() + ["ftp_hostname"]

    @classmethod
    def document(cls, config: FTPCollectorConfiguration):
        information = super().document(config)
        information |= {
            "protocol": "FTP",
            "auth_user": getattr(config, "client_username"),
        }
        return information
