"""Extract SimpleHttpCollector JSON files from HTTP REST API"""

from dataclasses import dataclass, field
from typing import Dict

from maas_collector.rawdata.collector.httpcollector import (
    HttpCollector,
    HttpCollectorConfiguration,
    HttpConfiguration,
)

from maas_collector.rawdata.collector.httpmixin import HttpMixin

from maas_collector.rawdata.collector.simplehttp.v1_impl import (
    SimpleHttpQueryV1Implementation,
)

# pylint: disable=line-too-long / C0301


@dataclass
class SimpleHttpCollectorConfiguration(HttpCollectorConfiguration):
    """Configuration for SimpleHttp Collector"""

    refresh_interval: int = 86400  # 24 hours

    protocol_version: str = "v1"

    end_date_time_offset: int = 0

    # # Field name for the user identifier, which may vary by service; for example, "identity" on SpaceTrack
    # client_username_field: str = "username"

    # # Value for the user identifier
    # client_username: str = ""

    # # Field name for the password, which may also vary (e.g., not always "password")
    # client_password_field: str = "password"

    # # Value for the password
    # client_password: str = ""

    credentials: Dict = field(default_factory=lambda: {})

    login_url: str = ""

    http_rest_uri: str = ""

    auth_method: str = "SessionAuth"

    # Used for the last_date in journal
    # date_attr: str = "creation_date"
    date_attr: str = "ingestionTime"


@dataclass
class SimpleHttpConfiguration(HttpConfiguration):
    """Store SimpleHttp configuration variables"""


class SimpleHttpCollector(HttpCollector, HttpMixin):
    """A SimpleHttp collector that collects data from a SimpleHttp HTTP API."""

    CONFIG_CLASS = SimpleHttpCollectorConfiguration

    IMPL_DIR = {"v1": SimpleHttpQueryV1Implementation}

    @classmethod
    def build_probe_query(cls, config: SimpleHttpCollectorConfiguration):
        """Creation of a probe query to check if the SimpleHttp API is online

        Args:
            config (SimpleHttpCollectorConfiguration): Configuration of the collector

        Returns:
            str: Probe query URL
        """
        return f"{config.product_url}"
