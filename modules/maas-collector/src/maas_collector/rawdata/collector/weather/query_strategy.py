"""Contain base class for Weather implementations"""
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


class AbstractWeatherQueryStrategy(AbstractHttpQueryStrategy):
    """Base class for Weather query implementation"""

    FILE_NAME_PATTERN = None

    def __init__(
        self,
        collector: "WeatherCollector",
        config: "WeatherCollectorConfiguration",
        http_session: HttpMixin,
        start_date: datetime.datetime,
        end_date_without_offset: datetime.datetime,
        journal: typing.Union[CollectorJournal, CollectorReplayJournal],
    ):
        """Perform query initialization using first the default HTTP query init
        then overload with specific weather query configuration

        Args:
            collector (WeatherCollector): collector object
            config (WeatherCollectorConfiguration):
                configuration of the weather collector
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

        # When retrieving archive weather data, the end date cannot be more recent ...
        # ... than the last 15days before else the api will not empty data
        if config.query_type == "archive":
            if self.end_date.date() == datetime.datetime.utcnow().date():
                self.end_date = (
                    (self.end_date - datetime.timedelta(days=15))
                    .replace(hour=23)
                    .replace(minute=59)
                )

            if self.start_date.date() == datetime.datetime.utcnow().date():
                self.start_date = (
                    (self.start_date - datetime.timedelta(days=14))
                    .replace(hour=0)
                    .replace(minute=0)
                )

        # When retrieving forecast weather data, you cannot choose the timeframe...
        # ... it is always from 31 in the past till some days in future in an unique json file ...
        # .... start date and end_date does not matter
        else:
            self.start_date = datetime.datetime.utcnow().date()
            self.end_date = datetime.datetime.utcnow().date()

        self.weather_query_type = config.query_type
        self.weather_additional_url_parameters = config.additional_url_parameters
        self.latitude = config.latitude
        self.longitude = config.longitude

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
