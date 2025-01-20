"""Extract Discosweb JSON files from HTTP REST API"""

from dataclasses import dataclass

from maas_collector.rawdata.collector.httpcollector import (
    HttpCollector,
    HttpCollectorConfiguration,
    HttpConfiguration,
)

from maas_collector.rawdata.collector.httpmixin import HttpMixin

from maas_collector.rawdata.collector.discosweb.v2_impl import (
    DiscoswebQueryV2Implementation,
)


@dataclass
class DiscoswebCollectorConfiguration(HttpCollectorConfiguration):
    """Configuration for Discosweb Collector"""

    refresh_interval: int = 86400  # 24 hours

    protocol_version: str = "v2"

    discosweb_timeout: int = 120

    end_date_time_offset: int = 0

    discosweb_keep_files: bool = False

    discosweb_page_size: int = 100

    discosweb_first_page_index: int = 1

    # Used for the last_date in journal
    date_attr: str = "ingestionTime"


@dataclass
class DiscoswebConfiguration(HttpConfiguration):
    """Store Discosweb configuration variables"""


class DiscoswebCollector(HttpCollector, HttpMixin):
    """A Discosweb collector that collects data from a Discosweb HTTP API."""

    CONFIG_CLASS = DiscoswebCollectorConfiguration

    IMPL_DIR = {"v2": DiscoswebQueryV2Implementation}

    @classmethod
    def build_probe_query(cls, config: DiscoswebCollectorConfiguration):
        """Creation of a probe query to check if the Discosweb API is online

        Args:
            config (DiscoswebCollectorConfiguration): Configuration of the collector

        Returns:
            str: Probe query URL
        """
        return f"{config.product_url}"
