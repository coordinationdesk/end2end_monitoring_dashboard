"""Contain base class for Loki implementations"""
import datetime
import typing

from maas_collector.rawdata.collector.http.abstract_query_strategy import (
    AbstractHttpQueryStrategy,
)
from maas_collector.rawdata.collector.httpmixin import HttpMixin
from maas_collector.rawdata.collector.journal import (
    CollectorJournal,
    CollectorReplayJournal,
)


class AbstractLokiQueryStrategy(AbstractHttpQueryStrategy):
    """Base class for Loki query implementation"""

    FILE_NAME_PATTERN = None

    def __init__(
        self,
        collector: "LokiCollector",
        config: "LokiCollectorConfiguration",
        http_session: HttpMixin,
        start_date: datetime.datetime,
        end_date_without_offset: datetime.datetime,
        journal: typing.Union[CollectorJournal, CollectorReplayJournal],
    ):
        """Perform query initialization using first the default HTTP query init
        then overload with specific Loki query configuration

        Args:
            collector (LokiCollector): collector object
            config (LokiCollectorConfiguration):
                configuration of the Loki collector
            http_session (HttpMixin): Initialized http session
            start_date (datetime.datetime): start date of collection
            end_date_without_offset (datetime.datetime): end date of collection
            journal (typing.Union[CollectorJournal, CollectorReplayJournal]):
                        journal used to check if collection shall start or
                        if data to collect are too old or parsed too recently
        """
        super().__init__(
            collector,
            config,
            http_session,
            start_date,
            end_date_without_offset,
            journal,
        )

        self.query_limit = config.query_limit
        self.query = config.query
        self.query_prefix = config.query_prefix
        self.max_time_window = config.max_time_window
        self.product_url = config.product_url
        self.protocol_version = config.protocol_version

        self._iter_start_date = self.start_date
        self._iter_end_date = min(
            self.start_date + datetime.timedelta(minutes=self.max_time_window),
            self.end_date,
        )

    def get_filename(self, page: int) -> str:
        """get file name of a page for download

        Args:
            page (int): Page number, used when there is multiple json file to retrieve

        Returns:
            str: generated filename
        """
        return self.FILE_NAME_PATTERN.format(
            interface_name=self.interface_name,
            start_date=self.start_date.strftime("%Y%m%dT%H%M%S"),
            end_date=self.end_date.strftime("%Y%m%dT%H%M%S"),
            page_nb=page,
        )

    def __iter__(self):
        """yields pages of product

        Raises:
            NotImplemented: abstract methods
        """
        raise NotImplementedError()

    def _deserialize_response(self, response):
        raise NotImplementedError()

    def _count_item_payload(self, payload):
        raise NotImplementedError()
