"""
Read Only SFTPCollector.

SFTPCollector was design as an inbox, where files where moved to folders after been
ingested or rejected. This module covers the case where no inbox strategy can be applied
due to lake of write permissions on the remote server.

Instead, it behaves like the WebDAV collector, using journal to store the modification
date of the last ingested file to discriminate the new files to ingest.

Also, it does not use the leaky pysftp api but raw paramiko api calls.
"""

import base64
import datetime
import os
from dataclasses import dataclass, field
from io import StringIO

import paramiko
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
class ReadOnlySFTPCollectorConfiguration(FileCollectorConfiguration):
    """Store Read-Only SFTP configuration vars"""

    client_username: str = ""

    client_password: str = field(default="", metadata={"sensitive": True})

    client_keyfile: str = ""

    sftp_hostname: str = ""

    sftp_port: int = 22

    interface_name: str = ""

    directories: list = None

    refresh_interval: int = 10

    timeout: int = 30


class ReadOnlySFTPCollector(FileCollector):
    """A collector that collect from a SFTP server"""

    CONFIG_CLASS = ReadOnlySFTPCollectorConfiguration

    def __init__(
        self,
        args: CollectorArgs,
    ):
        super().__init__(args)

        # modification datetime of the last ingested file
        self.last_date = None

    def ingest(self, path=None, configs=None, force_update=None):
        """Ingest from SFTP. All arguments are ignored so defaults to None

        Args:
            path (_type_, optional): _description_. Defaults to None.
            configs (_type_, optional): _description_. Defaults to None.
            force_update (_type_, optional): _description_. Defaults to None.
        """
        # iterate over all R/O SFTP collector configurations
        for config in self.configs:
            if not config.directories:
                self.logger.debug("Skipping auxiliary config: %s", config)
                continue

            if self.should_stop_loop:
                break

            try:
                # use the journal as context to secure the concurent collect
                with CollectorJournal(config) as journal:
                    self.ingest_rosftp(config, journal)

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

    @staticmethod
    def build_transport(config) -> paramiko.Transport:
        """Build paramiko transport object

        Args:
            config (dict): config with information to build paramiko socket

        Returns:
            paramiko.Transport: paramiko object to interact with sftp server
        """

        transport = paramiko.Transport((config.sftp_hostname, config.sftp_port))

        # support keyfile auth
        if config.client_keyfile:
            keyfile_base64_bytes = config.client_keyfile.encode("ascii")
            keyfile_bytes = base64.b64decode(keyfile_base64_bytes)
            client_keyfile_decoded = keyfile_bytes.decode("ascii")

            file = StringIO(client_keyfile_decoded)
            config_pk = paramiko.RSAKey.from_private_key(file)

            transport.connect(
                username=config.client_username,
                pkey=config_pk,
            )

        else:
            # default method using password
            transport.connect(
                username=config.client_username,
                password=config.client_password,
            )

        # send keep alive packet every 30 seconds
        transport.set_keepalive(30)

        return transport

    def ingest_rosftp(
        self, config: ReadOnlySFTPCollectorConfiguration, journal: CollectorJournal
    ):
        """Process a configuration

        Args:
            config (ReadOnlySFTPCollectorConfiguration): configuration
            journal (CollectorJournal): journal
        """
        if not config.directories:
            self.logger.error(
                "Config %s has no directory to look up. Check configuration"
            )
            return

        self.logger.info("Connecting to sftp host %s", config.sftp_hostname)

        transport = self.build_transport(config)

        try:
            with paramiko.SFTPClient.from_transport(transport) as client:
                client.get_channel().settimeout(config.timeout)

                self.ingest_interface(config, client, journal)

        except (paramiko.SSHException, IOError, OSError) as error:
            self.logger.critical("Cannot ingest %s", config)
            self.logger.exception(error)

        finally:
            if not journal.last_date:
                # first run
                journal.last_date = self.last_date

            elif self.last_date and self.last_date > journal.last_date:
                journal.last_date = self.last_date

            # reset for next usage
            self.last_date = None

            self.logger.debug("Closing transport")
            transport.close()

    def ingest_interface(
        self,
        config: ReadOnlySFTPCollectorConfiguration,
        client: paramiko.SFTPClient,
        journal: CollectorJournal,
    ):
        """Ingest an Read-Only SFTP configuration

        Args:
            config (ReadOnlySFTPCollectorConfiguration): configuration
            client (paramiko.SFTPClient): sftp client
            journal (CollectorJournal): collector journal
        """

        for attrs in self.get_interesting_attrs_list(config, client, journal.last_date):
            if self.should_stop_loop:
                break

            self._healthcheck.tick()

            local_path = os.path.join(
                self.args.working_directory, os.path.basename(attrs.filename)
            )

            self.logger.info("Downloading %s", attrs.filename)

            client.get(attrs.filename, local_path)

            try:
                for found_config in self.get_configurations(
                    os.path.basename(attrs.filename)
                ):
                    self.extract_from_file(
                        local_path,
                        found_config,
                        report_name=os.path.basename(local_path),
                        report_folder=os.path.dirname(attrs.filename),
                        iter_callback=None,
                    )
            # catch any exception about the extraction, not the collect
            # pylint: disable=broad-except
            except Exception as error:
                self.logger.error("Cannot ingest %s", attrs.filename)
                self.logger.exception(error)
            finally:
                os.remove(local_path)
            # pylint: enable=broad-except

            # store modification time
            if not self.last_date:
                self.last_date = attrs.st_mdatetime

            elif self.last_date < attrs.st_mdatetime:
                # a new last date has been found: store the previous in the journal
                # so interupted ingestion can go on nicely again without missing files
                # that have the same modification time
                journal.last_date = self.last_date

                self.last_date = attrs.st_mdatetime

            journal.tick()

    def get_interesting_attrs_list(
        self,
        config: ReadOnlySFTPCollectorConfiguration,
        client: paramiko.SFTPClient,
        min_date: datetime.datetime,
    ) -> list[paramiko.SFTPAttributes]:
        """Create the list of the files to ingest by listing all directories of the
        configuration, filter them on pattern and minimum date, and reorder the whole
        list depending their modification time

        Args:
            config (ReadOnlySFTPCollectorConfiguration): configuration
            client (paramiko.SFTPClient): sftp client
            min_date (datetime.datetime): minimum modification date of the file

        Returns:
            list[paramiko.SFTPAttributes]: list of file metadata with filename
                containing directory, and extra attribute st_mdatetime to store
                modification time as datetime
        """

        # all interesting sftp attributes objets
        all_attrs = []

        # get the interesting files for all directories
        for directory in config.directories:
            if self.should_stop_loop:
                break

            self._healthcheck.tick()

            for attrs in client.listdir_attr(directory):
                if self.should_stop_loop:
                    break

                configurations = self.get_configurations(attrs.filename)

                # filter on name
                if not configurations:
                    continue

                # convert timestamp to datetime with timezone
                st_mdatetime = datetime.datetime.fromtimestamp(
                    attrs.st_mtime, tz=datetime.timezone.utc
                )

                # filter on date
                if min_date and st_mdatetime <= min_date:
                    continue

                # reaffect filename attribute with full path for easier downloading
                # sure, it is not very elegant, like the monkey patch below
                # but it does the job
                attrs.filename = "/".join((directory, attrs.filename))

                # monkey path sftp attributes to keep track of the calculated datetime
                attrs.st_mdatetime = st_mdatetime

                # add it to the final list
                all_attrs.append(attrs)

        # sort all the file so ingestion can be consistent and store the journal
        # last_date at each ingestion
        all_attrs.sort(key=lambda attrs: attrs.st_mtime)

        return all_attrs

    @classmethod
    def probe(cls, config: ReadOnlySFTPCollectorConfiguration, probe_data):
        transport = cls.build_transport(config)

        try:
            with paramiko.SFTPClient.from_transport(transport) as client:
                client.get_channel().settimeout(config.timeout)

                for directory in config.directories:
                    client.listdir_attr(directory)

        finally:
            transport.close()

    @classmethod
    def attributs_url(cls):
        return super().attributs_url() + ["hostname"]

    @classmethod
    def document(cls, config: ReadOnlySFTPCollectorConfiguration):
        information = super().document(config)
        information |= {
            "protocol": "SFTP (readonly)",
            "auth_user": getattr(config, "client_username"),
        }
        return information
