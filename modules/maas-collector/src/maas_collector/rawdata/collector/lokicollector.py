"""Extract Loki json files from HTTP rest API"""

from dataclasses import dataclass

from maas_collector.rawdata.collector.httpcollector import (
    HttpCollector,
    HttpCollectorConfiguration,
    HttpConfiguration,
)

from maas_collector.rawdata.collector.httpmixin import HttpMixin

from maas_collector.rawdata.collector.loki.v1_impl import (
    LokiQueryV1Implementation,
)


@dataclass
class LokiCollectorConfiguration(HttpCollectorConfiguration):
    """Configuration for Loki Collector Configuration"""

    date_attr: str = "ingestionTime"

    # the time interval between two refresh for this interface
    refresh_interval: int = 720

    # Max time range in minute to retrieve in a single query
    max_time_window: int = 10

    # Loki query content
    query: str = ""

    # Max number of element which can be retrieved with a single query
    query_limit: int = 5000

    query_prefix: str = ""

    protocol_version: str = "v1"

    end_date_time_offset: int = 0


@dataclass
class LokiConfiguration(HttpConfiguration):
    """Store Loki configuration vars"""


class LokiCollector(HttpCollector, HttpMixin):
    """A Loki collector that collect from a Loki Http API."""

    CONFIG_CLASS = LokiCollectorConfiguration

    IMPL_DIR = {"v1": LokiQueryV1Implementation}

    @classmethod
    def build_probe_query(cls, config: LokiCollectorConfiguration):
        """Creation of a query which will be sent to the Loki API to check if it is online

        Args:
            config (LokiCollectorConfiguration): Configuration of the collector

        Returns:
            str: query
        """
        str_v1 = f"{config.get_config_product_url()}/ready"
        probe_query_dict = {"v1": str_v1}
        return probe_query_dict[config.protocol_version]

    @classmethod
    def attributs_url(cls):
        return super().attributs_url() + ["end_point"]

    @classmethod
    def document(cls, config: LokiCollectorConfiguration):
        information = super().document(config)

        information |= {
            "protocol": "HTTP(S)",
        }
        return information
