"""Simple Http v1 implementation"""

from requests import RequestException
from maas_collector.rawdata.collector.simplehttp.query_strategy import (
    AbstractSimpleHttpQueryStrategy,
)

# pylint: disable=line-too-long / C0301


class SimpleHttpQueryV1Implementation(AbstractSimpleHttpQueryStrategy):
    """AbstractSimpleHttpQueryStrategy implementation for V1 version"""

    FILE_NAME_PATTERN = "{interface_name}_PN{page_nb:06}_{collect_date}.json"

    def __iter__(self):
        """yields pages of data

        Raises:
            RequestException: when HTTP request fails
        """

        self.logger.debug("[__ITER__][MAIN] Start collecting simple http")

        try:
            entities, entities_json = self._get_entities()

            yield entities

            nb_entities = self._count_item_payload(entities_json)

        except RequestException as e:
            self.logger.error(
                "[%s] Request Error on %s : %s",
                self.interface_name,
                self._get_request_url(),
                e,
            )
        except ValueError as e:
            self.logger.error(
                "[%s] Request Error on %s : %s",
                self.interface_name,
                self._get_request_url(),
                e,
            )

        self.logger.debug("[__ITER__][END] Finished data collection")

        self.logger.info(
            "[%s] Collected a total of [%d] entities",
            self.interface_name,
            nb_entities,
        )

    def _get_entities(self):
        """
        Retrieves entities from the the URL in config.

        Returns:
            tuple: A tuple containing:
                - response.content (bytes): The raw content of the server response.
                - response.json() (dict): The JSON-parsed content of the server response.

        Raises:
            ValueError: if response status is not 200
            JSONDecodeError: If the response cannot be parsed as JSON.
        """

        headers = self.authentication.get_headers()

        query_url = self._get_request_url()

        self.logger.debug("Requesting url %s", query_url)

        response = self.http_session.get(
            query_url,
            headers=headers,
            timeout=self.collector.http_config.timeout,
        )
        if not response.ok:
            self.logger.error(
                "Error querying %s %d: %s",
                query_url,
                response.status_code,
                response.content,
            )
            raise ValueError(f"Error querying {query_url}")

        return response.content, response.json()

    def _get_request_url(self):
        """
        Constructs and returns the full request URL.

        Concatenates the base product URL with the REST API path to form
        the complete URL needed for the HTTP request.
        If `http_rest_uri` is None or an empty string, returns only `product_url`.
        Returns:
            str: Full URL for the request.
        """

        if not self.http_rest_uri:
            return self.product_url

        # Ensure a single '/' between product_url and http_rest_uri
        if not self.product_url.endswith("/") and not self.http_rest_uri.startswith(
            "/"
        ):
            return f"{self.product_url}/{self.http_rest_uri}"
        if self.product_url.endswith("/") and self.http_rest_uri.startswith("/"):
            return f"{self.product_url}{self.http_rest_uri[1:]}"
        return f"{self.product_url}{self.http_rest_uri}"

    def _count_item_payload(self, payload):
        """Counts the number of items in a payload

        Args:
            payload (dict): JSON payload

        Returns:
            int: number of items
        """
        return len(payload if payload else [])
