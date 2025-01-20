"""Discosweb v2 implementation"""

import time
from requests import RequestException
from maas_collector.rawdata.collector.discosweb.query_strategy import (
    AbstractDiscoswebQueryStrategy,
)

# pylint: disable=line-too-long / C0301


class DiscoswebQueryV2Implementation(AbstractDiscoswebQueryStrategy):
    """AbstractDiscoswebQueryStrategy implementation for V2 version"""

    FILE_NAME_PATTERN = (
        "{interface_name}_PS{page_size:06}_PN{page_nb:06}_{collect_date}.json"
    )

    def __iter__(self):
        """yields pages of data

        Raises:
            RequestException: when HTTP request fails
        """
        total_entities = 0
        error_retry_number = 0

        start_page_number = self._get_start_page_number()
        current_page = start_page_number

        self.logger.debug(
            "[__ITER__][MAIN] Start collecting from page %d", current_page
        )

        nb_entities = self.page_size
        # Main loop over each page
        # If response is not equal to the page size we request, it means that it is the last page
        while nb_entities == self.page_size:
            if self.collector.should_stop_loop:
                break

            self.logger.debug(
                "Querying page %d for %s", current_page, self.interface_name
            )

            try:
                entities = self._get_entities(current_page)
                yield entities

                nb_entities = self._count_item_payload(entities)
                total_entities += nb_entities
                self.logger.debug(
                    "[__ITER__][STATS] Collected %s entities from page %d",
                    nb_entities,
                    current_page,
                )

                # Update journal with last collected page
                self.journal.document.last_collected_page = current_page
                self.journal.document.save(refresh=True)

                error_retry_number = 0
                current_page += 1

            except RequestException as e:
                error_retry_number += 1
                self.logger.error(
                    "[%s][SKIP] Request Error on page %d : %s",
                    self.interface_name,
                    current_page,
                    e,
                )
                time.sleep(60)  # API rate limit
                if error_retry_number > 2:
                    break

        self.logger.debug("[__ITER__][END] Finished data collection")

        self.logger.info(
            "[%s] Collected a total of [%d] entities from page [%d] to page [%d] for a total of [%d] pages",
            self.interface_name,
            total_entities,
            start_page_number,
            current_page,
            current_page - start_page_number,
        )

    def _get_entities(self, page_number):
        """Get entities from the URL in config for a given page number

        Args:
            page (int): page number to query

        Raises:
            RequestException: if response status is not 200

        Returns:
            dict: JSON response containing page data
        """

        query_params = (
            self.http_query_params.format(
                page_size=self.page_size,
                page_number=page_number,
            )
            if self.http_query_params
            else ""
        )

        headers = self.authentication.get_headers()
        headers["DiscosWeb-Api-Version"] = "2"

        query_url = f"{self.product_url}?{query_params}"

        self.logger.debug("Requesting page url %s", query_url)

        # query_params = {
        #     "page[size]": self.page_size,
        #     "page[number]": page_number,
        # }

        response = self.http_session.get(
            query_url,
            headers=headers,
            # params=query_params,
            timeout=self.collector.http_config.timeout,
        )

        # response = self.http_session.get(
        #     f"{self.product_url}{self.query_prefix}",
        #     headers=headers,
        #     params=query_params,
        #     timeout=self.collector.http_config.timeout,
        # )

        if not response.ok:
            self.logger.error(
                "Error querying %s %d: %s",
                query_url,
                response.status_code,
                response.content,
            )
            raise RequestException(f"Error querying {query_url}")

        return self._deserialize_response(response)

    def _count_item_payload(self, payload):
        """Counts the number of items in a payload

        Args:
            payload (dict): JSON payload

        Returns:
            int: number of items
        """
        return len(payload.get("data", []))

    def _deserialize_response(self, response):
        """Deserialize the JSON response

        Args:
            response (requests.Response): HTTP response object

        Returns:
            dict: JSON data
        """
        return response.json()

    def _get_start_page_number(self):
        """Get the start page number from which to start to collect"""

        try:
            start_page_number = self.journal.document.last_collected_page
        except AttributeError as e:
            self.logger.warning(
                "No journal.document.last_collected_page: %s so take the first one from configration",
                e,
            )
            start_page_number = self._iter_start_index

        return start_page_number
