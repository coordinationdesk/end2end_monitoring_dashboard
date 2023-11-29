"""
Provides HttpMixin class
"""
import logging
import urllib3
from urllib3.exceptions import InsecureRequestWarning

import requests


LOGGER = logging.getLogger("HttpMixin")

# as HttpMixin provides only a specific function, it is not expected to contain
# lot of methods
# pylint: disable=R0903


class HttpMixin:
    """

    Provides http interaction support
    """

    @classmethod
    def create_http_session(cls, config) -> requests.Session:
        """Create and initialize a HTTP session for a configuration

        Args:
            config: configuration

        Returns:
            requests.Session: initialized http session
        """
        http_session = requests.Session()

        if (
            hasattr(config, "disable_insecure_request_warning")
            and config.disable_insecure_request_warning
        ):
            LOGGER.debug("Disabling insecure warning for %s", config.interface_name)
            urllib3.disable_warnings(category=InsecureRequestWarning)
            http_session.verify = False

        return http_session


# pylint: enable=R0903
