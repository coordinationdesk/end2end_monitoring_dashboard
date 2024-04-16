"""Contain base class for Mpip implementations"""

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


class AbstractMpipQueryStrategy(AbstractHttpQueryStrategy):
    """Base class for Mpip query implementation"""

    FILE_NAME_PATTERN = None

    def __init__(
        self,
        collector: "MpipCollector",
        config: "MpipCollectorConfiguration",
        http_session: HttpMixin,
        start_date: datetime.datetime,
        end_date_without_offset: datetime.datetime,
        journal: typing.Union[CollectorJournal, CollectorReplayJournal],
    ):
        """Perform query initialization using first the default HTTP query init
        then overload with specific mpip query configuration

        Args:
            collector (MpipCollector): collector object
            config (MpipCollectorConfiguration): configuration of collector
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
        # MPIP interface sort in REVERSE (because why not ?) so we need to do some magic tricks 🧙‍♂️
        self.mpip_start_date = self.start_date
        if config.mpip_start_offset:
            self.start_date = self.start_date - datetime.timedelta(
                minutes=config.mpip_start_offset
            )

        self.product_per_page = config.product_per_page

    def get_filename(self, page: int) -> str:
        """get file name of a page for download"""
        return self.FILE_NAME_PATTERN.format(
            interface_name=self.interface_name,
            start_date=self.start_date.strftime("%Y%m%dT%H%M%S"),
            end_date=self.end_date.strftime("%Y%m%dT%H%M%S"),
            current_page=page,
        )

    def __iter__(self):
        """yields pages of product

        Args:
            args (dict): query arguments

        Raises:
            NotImplemented: abstract methods
        """
        raise NotImplementedError()
