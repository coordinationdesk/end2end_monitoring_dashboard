"""Extract files from S3 Bucket"""

from dataclasses import dataclass, field
import datetime
import fnmatch
import gc
import os
import typing

import boto3
from botocore.client import Config


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


# Désactive la génération automatique de __repr__ pour pouvoir utiliser
# celui du parent qui masque les données sensible comme les mot de passe
@dataclass(repr=False)
class S3CollectorConfiguration(FileCollectorConfiguration):
    """Configuration for s3 collection"""

    buckets: list[str] = field(default_factory=lambda: [])

    s3_endpoint_url: str = ""

    s3_access_key: str = field(default="", metadata={"sensitive": True})

    s3_secret_key: str = field(default="", metadata={"sensitive": True})

    s3_max_keys: int = 1000

    s3_initial_timestamp: int = 0

    s3_signature_version: str = "v4"

    s3_region: str = None

    refresh_interval: int = 0


@dataclass
class S3Configuration:
    """Store S3 configuration for the collector"""

    timeout: int = 120

    keep_files: bool = False

    # TODO consumme_files ?


class S3Collector(FileCollector, HttpMixin):
    """A collector that collect from a Http API.

    Could be one day refactored to more generic REST api collector.

    Warning: does not support redirect
    """

    CONFIG_CLASS = S3CollectorConfiguration

    IMPL_DIR = {}

    def __init__(
        self,
        args: CollectorArgs,
        config: S3Configuration,
    ):
        super().__init__(args)
        self.config: S3Configuration = config
        self.s3_config_dict = {}

    def build_query_implementation(
        self, config, session, start_date, end_date, journal
    ) -> AbstractHttpQueryStrategy:
        """Factory method that builds the query implementation depending the version

        Args:
            config (S3CollectorConfiguration): [description]
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

        raise NotImplementedError("Currently not tested and implemented")

    def ingest_all_interfaces(self):
        """Nominal ingestion from s3: collect all the s3 configurations"""
        # iterate over all Http collector configurations
        previous_config_interface_name = None

        self.s3_config_dict = {}

        for config in self.configs:
            if config.interface_name in self.s3_config_dict:
                self.logger.error(
                    "Skiping this duplicated entry for %s", config.interface_name
                )
                continue

            # Single configuration
            if config.buckets and config.extractor:
                self.logger.info("Added %s S3 collector", config.interface_name)
                self.s3_config_dict[config.interface_name] = [config]

            # Init of multiple configuration
            elif config.buckets and not config.extractor:
                self.logger.info(
                    "Init %s S3 collector with multiple configuration",
                    config.interface_name,
                )
                self.s3_config_dict[config.interface_name] = []
                previous_config_interface_name = config.interface_name

            # Herited configuration
            elif not config.buckets and config.extractor:
                self.logger.info(
                    "Init %s S3 collector with multiple configuration (%s)",
                    config.interface_name,
                    previous_config_interface_name,
                )
                self.s3_config_dict[previous_config_interface_name].append(config)
            else:
                self.logger.error(
                    "Invalid entry configuration for %s", config.interface_name
                )

        for interface_name, configs in self.s3_config_dict.items():

            self.logger.info(
                "Start collect of %s with %s configuration",
                interface_name,
                len(configs),
            )

            # Patch journal here to had parrallele bucket collect
            journal = CollectorJournal(
                self.get_configuration_by_interface_name(interface_name)
            )

            self.ingest_interface(
                journal, self.get_configuration_by_interface_name(interface_name)
            )

            if self.should_stop_loop:
                break

    def ingest_interface(
        self,
        journal: typing.Union[CollectorJournal, CollectorReplayJournal],
        config: S3CollectorConfiguration,
        start_date: datetime.datetime = None,
        end_date: datetime.datetime = None,
    ):
        """Ingest an interface

        Args:
            journal (typing.Union[CollectorJournal, CollectorReplayJournal]): journal
            config (S3CollectorConfiguration): configuration
            start_date (datetime.datetime, optional): min date. Defaults to None.
            end_date (datetime.datetime, optional): max date. Defaults to None.
        """

        try:
            # use the journal as context to secure the concurent collect
            with journal:
                self._healthcheck.tick()
                self.ingest_s3(
                    config,
                    journal,
                    start_date,
                    end_date,
                )

        except CollectingInProgressError:
            # Errors should never pass silently.
            self.logger.info(
                "On going collection on interface %s: skipping",
                journal.config.interface_name,
            )
        except NoRefreshException:
            self.logger.info(
                "Interface %s does not need to be refreshed: skipped",
                journal.config.interface_name,
            )
        finally:
            # flush messages between interfaces as they don't ingest the same data
            self._flush_message_groups()
            gc.collect()

    def ingest_s3(
        self,
        config: S3CollectorConfiguration,
        journal: CollectorJournal,
        start_date=None,
        end_date=None,
    ):
        """Ingest api

        Args:
            config (S3CollectorConfiguration): configuration to ingest
        """

        matched_configuration = len(self.s3_config_dict[config.interface_name])
        self.logger.info(
            "[START] Ingestion of %s (%s) between %s and %s with %s configuration",
            config.interface_name,
            config.interface_credentials,
            start_date,
            end_date,
            matched_configuration,
        )

        self.s3_resource = boto3.client(
            "s3",
            endpoint_url=config.s3_endpoint_url,
            aws_access_key_id=config.s3_access_key,
            aws_secret_access_key=config.s3_secret_key,
            config=Config(signature_version=config.s3_signature_version),
            region_name=config.s3_region,
        )

        # need to get the current datetime to avoid to collect data that have been post after the collect but before the end
        # this should come from journal
        __iter_end_date = datetime.datetime.now(tz=datetime.UTC)

        if not start_date:
            # If comes from config then will be the timestamp from config
            # If not configured in the configuration file then it is 0 and 0 is equivalent to 1970-01-01 00:00:00 (Unix epoch)
            __iter_start_date = datetime.datetime.fromtimestamp(
                config.s3_initial_timestamp, tz=datetime.UTC
            )
            self.logger.debug(
                "Start timestamp [%s] date [%s] from configuration",
                config.s3_initial_timestamp,
                __iter_start_date.strftime("%Y-%m-%d %H:%M:%S %Z"),
            )

        else:
            __iter_start_date = journal.document.last_date
            self.logger.debug(
                "Start date %s from journal last_date",
                __iter_start_date.strftime("%Y-%m-%d %H:%M:%S %Z"),
            )
        self.logger.info(
            "Collect data from %s ",
            __iter_start_date.strftime("%Y-%m-%d %H:%M:%S %Z"),
        )
        # Paginate through the objects in the bucket
        # OPTI : get a record for each bucket to allow parralle collect on
        # same interface but different buckets

        # OPTI : to get optimistic resuming we need to keep the last bucket and also the last document
        # journal.document.last_s3_key = None
        # journal.document.last_s3_buckets = None (care about config update)
        # last_item_from_buckets = journal.document.last_s3_buckets

        last_item_from_buckets = None
        for bucket in config.buckets:

            # Currently using StartAfter, depend on the interface it is possible to implement new paginator
            # OPTI switch this to a other paginator way
            # like ContinuationToken but not already implement
            need_next = True
            while need_next:
                self._healthcheck.tick()

                if self.should_stop_loop:
                    break

                # Handling iteration
                if last_item_from_buckets:
                    response = self.s3_resource.list_objects_v2(
                        Bucket=bucket,
                        MaxKeys=config.s3_max_keys,
                        StartAfter=last_item_from_buckets,
                    )
                else:
                    response = self.s3_resource.list_objects_v2(
                        Bucket=bucket, MaxKeys=config.s3_max_keys
                    )

                # Less key count than max keys
                if response["KeyCount"] < config.s3_max_keys:
                    need_next = False

                if "Contents" in response:
                    for obj in response["Contents"]:
                        if self.should_stop_loop:
                            break
                        file_name = obj["Key"]
                        last_modified = obj["LastModified"]

                        self.logger.debug(
                            "File Name: %s, Last Modified: %s", file_name, last_modified
                        )

                        if not (__iter_start_date < last_modified <= __iter_end_date):
                            self.logger.debug(
                                "This file has been already process or will be in the futur %s %s",
                                file_name,
                                last_modified,
                            )

                            last_item_from_buckets = obj["Key"]

                            continue

                        # NEED TO KEEP THIS other stuff may be include in a __iter__ need only filename

                        # try to find a match pattern
                        for extract_config in self.s3_config_dict[
                            config.interface_name
                        ]:
                            if self.should_stop_loop:
                                break
                            # OPTI : Can download 1 time if two config match
                            if fnmatch.fnmatch(
                                file_name.lower(), extract_config.file_pattern.lower()
                            ):
                                filepath = os.path.join(
                                    self.args.working_directory, file_name
                                )
                                directory = os.path.dirname(filepath)
                                # Créer les sous-dossiers nécessaires
                                os.makedirs(directory, exist_ok=True)
                                self.logger.debug(
                                    "Find a match for %s %s (%s)",
                                    extract_config.interface_name,
                                    file_name,
                                    filepath,
                                )

                                self.s3_resource.download_file(
                                    bucket, file_name, filepath
                                )

                                self.extract_from_file(
                                    filepath,
                                    extract_config,
                                    report_name=os.path.basename(filepath),
                                )

                                self.on_ingest_success(filepath, extract_config)
                        # After ingestion keep this id in collector ?

                        #
                        last_item_from_buckets = obj["Key"]
                else:
                    need_next = False
                    self.logger.debug("No objects found in the bucket.")

                journal.tick()

        journal.document.last_date = __iter_end_date
        journal.document.save(refresh=True)

    # Template method: child class may override and use argument and self
    # pylint: disable=unused-argument,no-self-use
    def post_process_data(
        self,
        data: typing.Union[dict, bytes],
        filename: str,
        config: S3CollectorConfiguration,
        http_session: HttpMixin,
    ):
        """Function which can be rewritten by child class of http collector
        in order to perform additional operation after data collection and before data extraction

        Args:
            data (typing.Union[dict, bytes]): data collected from interface
            filename (str): name of the file which will be used when dumping collected data
            config (S3CollectorConfiguration): configuration of the collector
            http_session (HttpMixin): initialized http session
        """

    @classmethod
    def probe(cls, config: S3CollectorConfiguration, probe_data: "InterfaceProbeData"):
        """_summary_

        Args:
            config (S3CollectorConfiguration): configuration of the collector
            probe_data (InterfaceProbeData): data to fill

        Raises:
            ValueError: The query of the interface led to a code not in range 200-300

        Returns:
            str: Returns OK string if query succeeded
        """
        s3_resource = boto3.client(
            "s3",
            endpoint_url=config.s3_endpoint_url,
            aws_access_key_id=config.s3_access_key,
            aws_secret_access_key=config.s3_secret_key,
            config=Config(signature_version=config.s3_signature_version),
            region_name=config.s3_region,
        )

        # If this raise error catched by probe executor
        s3_resource.list_objects_v2(
            Bucket=config.buckets[0], MaxKeys=config.s3_max_keys
        )
        # OPTI: better handling of response

        return "OK"

    @classmethod
    def attributs_url(cls):
        return super().attributs_url() + ["s3_endpoint_url"]

    @classmethod
    def document(cls, config: S3CollectorConfiguration):
        information = super().document(config)
        information |= {
            "protocol": "HTTP(S) - S3",
            "access_key": getattr(config, "s3_access_key"),
        }

        return information
