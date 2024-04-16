"""Extract weather json files from HTTP rest API open-meteo.com"""
from dataclasses import dataclass
import datetime

from maas_collector.rawdata.collector.httpcollector import (
    HttpCollector,
    HttpCollectorConfiguration,
    HttpConfiguration,
)

from maas_collector.rawdata.collector.httpmixin import HttpMixin

from maas_collector.rawdata.collector.weather.v1_impl import (
    WeatherQueryV1Implementation,
)


@dataclass
class WeatherCollectorConfiguration(HttpCollectorConfiguration):
    """Configuration for Weather Collector Configuration"""

    date_attr: str = "ingestion_date"

    # the time interval between two refresh for this interface
    refresh_interval: int = 720

    query_type: str = ""

    end_date_time_offset: int = 0

    additional_url_parameters: str = ""

    max_number_day_to_retrieve_per_request: int = 15

    protocol_version: str = "v1"

    latitude: str = ""

    longitude: str = ""


@dataclass
class WeatherConfiguration(HttpConfiguration):
    """Store Weather configuration vars"""


class WeatherCollector(HttpCollector, HttpMixin):
    """A Weather collector that collect from a Weather Http API."""

    CONFIG_CLASS = WeatherCollectorConfiguration

    IMPL_DIR = {"v1": WeatherQueryV1Implementation}

    @classmethod
    def build_probe_query(cls, config: WeatherCollectorConfiguration):
        """Creation of a query which will be sent to the weather API to check if it is online

        Args:
            config (WeatherCollectorConfiguration): Configuration of the collector

        Returns:
            str: query
        """
        str_v1 = (
            f"{config.get_config_product_url()}{config.query_type}"
            f"{config.additional_url_parameters}"
        )

        probe_query_dict = {"v1": str_v1}
        # When querying archive data, a start and end date are mandatory
        if config.query_type == "archive":
            start_date = (datetime.datetime.now() - datetime.timedelta(2)).strftime(
                "%Y-%m-%d"
            )
            start_date_query = f"start_date={start_date}&"

            end_date = (datetime.datetime.now() - datetime.timedelta(1)).strftime(
                "%Y-%m-%d"
            )
            end_date_query = f"end_date={end_date}"

            probe_query_dict["v1"] += start_date_query + "&" + end_date_query

        return probe_query_dict[config.version]
