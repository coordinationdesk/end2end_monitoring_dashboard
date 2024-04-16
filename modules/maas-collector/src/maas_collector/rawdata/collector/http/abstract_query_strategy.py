"""Contain base class for OData implementations"""
import datetime
import logging
import typing

from maas_collector.rawdata.collector.http.authentication import build_authentication

from maas_collector.rawdata.collector.httpmixin import HttpMixin
from maas_collector.rawdata.collector.journal import (
    CollectorJournal,
    CollectorReplayJournal,
)


class AbstractHttpQueryStrategy:
    """Base class for Http query implementation"""

    FILE_NAME_PATTERN = None

    def __init__(
        self,
        collector: "HttpCollector",
        config: "HttpCollectorConfiguration",
        http_session: HttpMixin,
        start_date: datetime.datetime,
        end_date_without_offset: datetime.datetime,
        journal: typing.Union[CollectorJournal, CollectorReplayJournal],
    ):
        """Perform generic http query initialization, collector which inherit
        from the HTTP collector first execute this init then execute theirs

        Args:
            collector (HttpCollector): collector object
            config (HttpCollectorConfiguration): configuration of collector
            http_session (HttpMixin): Initialized http session
            start_date (datetime.datetime): start date of collection
            end_date_without_offset (datetime.datetime): end date of collection
            journal (typing.Union[CollectorJournal, CollectorReplayJournal]):
                        journal used to check if collection shall start or
                        if data to collect are too old or parsed too recently
        """
        self.logger = logging.getLogger(self.__class__.__name__)

        self.collector = collector
        self.config = config
        self.http_session = http_session

        self.interface_name = config.interface_name
        self.product_url = config.get_config_product_url()

        if not end_date_without_offset:
            end_date_without_offset = datetime.datetime.now(datetime.timezone.utc)
        self.end_date = end_date_without_offset - datetime.timedelta(
            minutes=config.end_date_time_offset
        )

        self.journal = journal

        if journal.last_date:
            self.start_date = journal.last_date
        elif not start_date:
            # first run: collect from the past following the refresh interval
            self.start_date = self.end_date - datetime.timedelta(
                minutes=config.refresh_interval
            )
        else:
            self.start_date = start_date

        try:
            self.authentication = build_authentication(
                config.auth_method, config, self.http_session
            )
        except KeyError as error:
            raise KeyError(f"Not supported auth method {config.auth_method}") from error

    def get_filename(self, page: int) -> str:
        """get file name of a page for download

        Args:
            page (int): Page number, used when there is multiple json file to retrieve

        Returns:
            str: generated filename
        """
        raise NotImplementedError()

    def __iter__(self):
        """yields pages of product

        Args:
            args (dict): query arguments

        Raises:
            NotImplemented: abstract methods
        """
        raise NotImplementedError()
