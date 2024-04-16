"""Contain base class for OData implementations"""

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

from maas_model import datetime_to_zulu
from requests.exceptions import RequestException


class AbstractODataQueryStrategy(AbstractHttpQueryStrategy):
    """Base class for OData query implementation"""

    FILE_NAME_PATTERN = None

    def __init__(
        self,
        collector: "ODataCollector",
        config: "ODataCollectorConfiguration",
        http_session: HttpMixin,
        start_date: datetime.datetime,
        end_date_without_offset: datetime.datetime,
        journal: typing.Union[CollectorJournal, CollectorReplayJournal],
    ):
        """Perform query initialization using first the default HTTP query init
        then overload with specific odata query configuration

        Args:
            collector (ODataCollector): collector object
            config (ODataCollectorConfiguration): configuration of collector
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

        if config.odata_start_offset:
            self.start_date = self.start_date - datetime.timedelta(
                minutes=config.odata_start_offset
            )

        self.product_per_page = config.product_per_page
        self.odata_query_filter = config.odata_query_filter
        self.list_of_files_to_retrieve = config.list_of_files_to_retrieve
        self.list_of_files_to_retrieve_per_query = (
            config.list_of_files_to_retrieve_per_query
        )
        # query shall be compatible with 'format' so expecting a single empty {} inside
        self.list_of_files_to_retrieve_query = config.list_of_files_to_retrieve_query

        self._iter_start_date = self.start_date
        self._iter_end_date = min(
            self.start_date + datetime.timedelta(minutes=self.config.max_time_window),
            self.end_date,
        )
        self._skip_number = 0

    def get_filename(self, page: int) -> str:
        """get file name of a page for download"""
        return self.FILE_NAME_PATTERN.format(
            interface_name=self.interface_name,
            start_date=self.start_date.strftime("%Y%m%dT%H%M%S"),
            end_date=self.end_date.strftime("%Y%m%dT%H%M%S"),
            product_per_page=self.product_per_page,
            current_page=page,
        )

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

            # In case we use the collector to retrieve a list of files, then
            # we will exit the loop only when all the files have been queried
            # list_of_files_to_retrieve > 0 means collector is in "files" retrieval mode
            if (
                self.list_of_files_to_retrieve
                and len(self.list_of_files_to_retrieve)
                <= self._skip_number * self.list_of_files_to_retrieve_per_query
            ):
                self.logger.debug(
                    "[__ITER__][LOCAL] All %s files have been queried ",
                    len(self.list_of_files_to_retrieve),
                )
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
                entities = self._get_entities(self._skip_number)

            except RequestException as connection_error:
                self.logger.error(
                    "[%s][SKIP] Request Error querying products : %s -> %s",
                    self.interface_name,
                    self.product_url,
                    connection_error,
                )
                # In case we are trying to collect using a list of files,
                # if the query contains only filename which are unavailable,
                # the request will be stuck. After the timeout we do not
                # want to trigger an exception but try the next filenames
                if self.list_of_files_to_retrieve:
                    self._skip_number += 1
                    current_query_index += 1
                    continue
                raise connection_error
            except ValueError as value_error:
                self.logger.error(
                    "[%s][SKIP] Value error querying products : %s -> %s",
                    self.interface_name,
                    self.product_url,
                    value_error,
                )
                raise value_error

            yield entities

            nb_entities = self._count_item_payload(entities)

            total_entities += nb_entities

            # In case the field 'list_of_files_to_retrieve' is not empty,
            # it means that no checks shall be done on start or end date,
            # we only want to retrieve a specific amount of filename
            if self.list_of_files_to_retrieve:
                self._skip_number += 1
                current_query_index += 1
                self.logger.debug(
                    "[__ITER__][LOCAL][STATS] Collected %s entities",
                    nb_entities,
                )
                continue

            self.logger.debug(
                "[__ITER__][LOCAL][STATS] Collected %s (psize %s) entities",
                nb_entities,
                self.product_per_page,
            )

            if self.collector.get_pending_document_count() == 0:
                # preserve time window so it can continue after restart, as no callback
                # will set the last date.
                self.logger.debug(
                    "Keep time window start in journal: %s", self._iter_start_date
                )
                self.journal.document.last_date = self._iter_start_date
                self.journal.document.save(refresh=True)

            if nb_entities < self.product_per_page:
                # Last iter on the current timerange

                self._iter_start_date = self._iter_end_date
                self._iter_end_date = min(
                    self._iter_start_date
                    + datetime.timedelta(minutes=self.config.max_time_window),
                    self.end_date,
                )

                self._skip_number = 0

                self.logger.debug(
                    "[__ITER__][LOCAL] NEXT FROM %s TO %s",
                    self._iter_start_date,
                    self._iter_end_date,
                )
            else:
                # keep iter in the same time range
                # move start page to continue to collect first page (no skip)

                # if a full page with a same doi use skip
                # delay with journal

                if self.journal.last_date <= self._iter_start_date:
                    self._skip_number += 1
                    self.logger.debug(
                        "[__ITER__][LOCAL] _iter forward last_date, increase skip number (%s) %s TO %s (J: %s)",
                        self._skip_number,
                        self._iter_start_date,
                        self._iter_end_date,
                        self.journal.last_date,
                    )
                else:
                    self._skip_number = 0
                    self.logger.debug(
                        "[__ITER__][LOCAL](OPTI) _iter backward last_date %s TO %s (J: %s) (%s)",
                        self._iter_start_date,
                        self._iter_end_date,
                        self.journal.last_date,
                        self._skip_number,
                    )
                    self._iter_start_date = self.journal.last_date

            current_query_index += 1

        self.logger.debug("[__ITER__][MAIN][END]")
        self.logger.info(
            "[%s] Finally retrieve %d products in %s queries",
            self.interface_name,
            total_entities,
            current_query_index,
        )

    def _get_entities(self, page_number):
        """Get entities from the url in config between the start_date and the end_date

        Args:
            page : page of entities

        Raises:
            ValueError: If no status code 200

        Returns:
            Object: an object who contains the json response between the given date
        """

        # We do not try to query the full list of files in a single GET, we split
        # and retrieve only 'list_of_files_to_retrieve_per_query' at a time
        query_config = ""
        if self.list_of_files_to_retrieve:
            files_to_consider = self.list_of_files_to_retrieve[
                page_number
                * self.list_of_files_to_retrieve_per_query : min(
                    page_number * self.list_of_files_to_retrieve_per_query
                    + self.list_of_files_to_retrieve_per_query,
                    len(self.list_of_files_to_retrieve),
                )
            ]

            query_config = " or ".join(
                [
                    self.list_of_files_to_retrieve_query.format(x)
                    for x in files_to_consider
                ]
            )
            self.logger.debug("Query being built is : %s", query_config)

            full_query = (
                f"$filter={query_config}"
                f"&$orderby={self.config.odata_query_order_by}"
                f"{self.config.custom_query_suffix}"
            )

        else:
            self.logger.debug(
                "Retrieve entities between %s and %s from %s page %s",
                self._iter_start_date,
                self._iter_end_date,
                self.product_url,
                page_number,
            )

            query_config = self.odata_query_filter.format(
                publication_start_date=self._format_date(self._iter_start_date),
                publication_end_date=self._format_date(self._iter_end_date),
            )

            full_query = (
                f"$filter={query_config}"
                f"&$orderby={self.config.odata_query_order_by}"
                f"&$top={self.product_per_page}"
                f"&$skip={self.product_per_page * page_number}"
                f"{self.config.custom_query_suffix}"
            )

        query_url = (
            f"{self.product_url}{self.config.odata_entity_location}"
            f"{self.config.odata_entities}?{full_query}"
        )

        self.logger.debug("URL : %s", query_url)

        headers = self.authentication.get_headers()

        response = self.http_session.get(
            query_url, headers=headers, timeout=self.collector.http_config.timeout
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

    def _format_date(self, date):
        """Default method to insert date in odata query

        Args:
            date (datetime): datetime

        Returns:
            str: the datetime stringify for REST operations
        """
        return datetime_to_zulu(date)

    def _deserialize_response(self, response):
        raise NotImplementedError()

    def _count_item_payload(self, payload):
        raise NotImplementedError()
