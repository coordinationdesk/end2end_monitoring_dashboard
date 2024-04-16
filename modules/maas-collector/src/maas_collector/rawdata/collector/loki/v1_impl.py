"""
Loki v1 implementation

"""
import datetime
from maas_collector.rawdata.collector.loki.query_strategy import (
    AbstractLokiQueryStrategy,
)
from requests import RequestException


class LokiQueryV1Implementation(AbstractLokiQueryStrategy):
    """AbstractLokiQueryStrategy implementation for V1 version"""

    FILE_NAME_PATTERN = "{interface_name}_{start_date}_{end_date}_{page_nb:06}.json"

    def __iter__(self):
        """yields pages of product

        Args:
            args (dict): query arguments

        Raises:
            NotImplemented: abstract methods
        """
        total_entities = 0

        current_query_index = 0

        self.logger.debug(
            "[__ITER__][MAIN] FROM %s TO %s", self.start_date, self.end_date
        )

        while self._iter_start_date < self.end_date:
            if self.collector.should_stop_loop:
                break

            self.logger.debug(
                "[__ITER__][LOCAL] FROM %s TO %s",
                self._iter_start_date,
                self._iter_end_date,
            )

            self.logger.debug(
                "Query n°%d for %s", current_query_index, self.interface_name
            )

            try:
                entities = self._get_entities()

            except RequestException as connection_error:
                self.logger.error(
                    "[%s][SKIP] Request Error querying products : %s -> %s",
                    self.interface_name,
                    self.product_url,
                    connection_error,
                )
            except ValueError as value_error:
                self.logger.error(
                    "[%s][SKIP] Value error querying products : %s -> %s",
                    self.interface_name,
                    self.product_url,
                    value_error,
                )
                break

            yield entities

            nb_entities = self._count_item_payload(entities)

            total_entities += nb_entities

            self.logger.debug(
                "[__ITER__][LOCAL][STATS] Collected %s entities",
                nb_entities,
            )

            if self.collector.get_pending_document_count() == 0:
                # preserve time window so it can continue after restart, as no callback
                # will set the last date.
                self.logger.debug(
                    "Keep time window start in journal: %s", self._iter_start_date
                )
                self.journal.document.last_date = self._iter_start_date
                self.journal.document.save(refresh=True)

            self._iter_start_date = self._iter_end_date
            self._iter_end_date = min(
                self._iter_start_date
                + datetime.timedelta(minutes=self.config.max_time_window),
                self.end_date,
            )

            self.logger.debug(
                "[__ITER__][LOCAL] NEXT FROM %s TO %s",
                self._iter_start_date,
                self._iter_end_date,
            )

            current_query_index += 1

        self.logger.debug("[__ITER__][MAIN][END]")
        self.logger.info(
            "[%s] Finally retrieve %d products in %s queries",
            self.interface_name,
            total_entities,
            current_query_index,
        )

    def _get_entities(self):
        """Get entities from the url in config between the start_date and the end_date

        Raises:
            ValueError: If no status code 200

        Returns:
            Object: an object who contains the json response between the given date
        """

        self.logger.debug(
            "Retrieve entities between %s and %s on %s",
            self._iter_start_date,
            self._iter_end_date,
            self.product_url,
        )

        start = str(int(datetime.datetime.timestamp(self._iter_start_date)))
        end = str(int(datetime.datetime.timestamp(self._iter_end_date)))

        query_params = {
            "query": self.config.query,
            "limit": self.config.query_limit,
            "start": start,
            "end": end,
        }

        query_url = f"{self.product_url}{self.config.query_prefix}"

        self.logger.debug("URL : %s", query_url)

        headers = self.authentication.get_headers()

        response = self.http_session.get(
            query_url,
            headers=headers,
            params=query_params,
            timeout=self.collector.http_config.timeout,
        )

        if not 200 <= response.status_code < 300:
            # serious problem
            self.logger.error(
                "Error querying %s %d: %s",
                query_url,
                response.status_code,
                response.content,
            )
            raise ValueError(f"Error querying {query_url}")

        return self._deserialize_response(response)

    def _count_item_payload(self, payload):
        return len(payload["data"]["result"])

    def _deserialize_response(self, response):
        return response.json()
