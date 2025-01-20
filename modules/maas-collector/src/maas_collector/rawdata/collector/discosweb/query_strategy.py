"""Contain base class for Discosweb implementations"""

from datetime import datetime, UTC
import typing

from maas_collector.rawdata.collector.http.abstract_query_strategy import (
    AbstractHttpQueryStrategy,
)
from maas_collector.rawdata.collector.httpmixin import HttpMixin
from maas_collector.rawdata.collector.journal import (
    CollectorJournal,
    CollectorReplayJournal,
)


class AbstractDiscoswebQueryStrategy(AbstractHttpQueryStrategy):
    """Base class for Discosweb query implementation"""

    FILE_NAME_PATTERN = None

    def __init__(
        self,
        collector: "DiscoswebCollector",
        config: "DiscoswebCollectorConfiguration",
        http_session: HttpMixin,
        start_date: datetime,
        end_date_without_offset: datetime,
        journal: typing.Union[CollectorJournal, CollectorReplayJournal],
    ):
        """Initialize Discosweb query configuration

        Args:
            collector (DiscoswebCollector): collector object
            config (DiscoswebCollectorConfiguration): Discosweb collector configuration
            http_session (HttpMixin): Initialized HTTP session
            journal (typing.Union[CollectorJournal, CollectorReplayJournal]): journal for tracking collection
        """
        super().__init__(
            collector,
            config,
            http_session,
            start_date,
            end_date_without_offset,
            journal,
        )

        self.product_url = config.product_url
        self.page_size = config.discosweb_page_size
        self.http_query_params = config.http_query_params

        self._iter_start_index = config.discosweb_first_page_index

    def get_filename(self, page: int) -> str:
        """Generates file name for downloaded page data

        Args:
            page (int): Page number

        Returns:
            str: formatted filename
        """
        return self.FILE_NAME_PATTERN.format(
            interface_name=self.interface_name,
            page_size=self.page_size,
            page_nb=page,
            collect_date=datetime.now(tz=UTC).strftime("%Y%m%dT%H%M%S"),
        )

    def __iter__(self):
        """yields pages of data

        Raises:
            NotImplemented: abstract method
        """
        raise NotImplementedError()

    def _deserialize_response(self, response):
        """Convert response to JSON"""
        raise NotImplementedError()

    def _count_item_payload(self, payload):
        """Count number of items in payload"""
        raise NotImplementedError()
