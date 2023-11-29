"""
Weather v1 implementation

https://open-meteo.com/en/docs
"""
import typing
import datetime
from maas_collector.rawdata.collector.weather.query_strategy import (
    AbstractWeatherQueryStrategy,
)


class WeatherQueryV1Implementation(AbstractWeatherQueryStrategy):
    """AbstractWeatherQueryStrategy implementation for V1 version (json)"""

    FILE_NAME_PATTERN = "{interface_name}_{start_date}_{end_date}_{page_nb:06}.json"

    def __iter__(self):
        """yields weather data which were queried on the API

        Args:
            args (dict): query arguments

        """

        # In archive mode, you can retrieve data per slice of X days for each request
        #  (configurable through config param max_number_day_to_retrieve_per_request)

        # in forecast mode, you can only retrieve from some days in the recent past...
        # ... till some days in future so there is only 1 request needed in forecast

        total_request_needed = 1
        date_interval_per_request_list = [None]

        if self.config.query_type == "archive":
            date_interval_per_request_list = self.split_date_request_in_interval(
                self.start_date,
                self.end_date,
                self.config.max_number_day_to_retrieve_per_request,
            )
            total_request_needed = len(date_interval_per_request_list)

        for cur_request_nb in range(total_request_needed):
            if self.collector.should_stop_loop:
                break

            try:
                products_json = self._get_entities(
                    date_interval_per_request_list[cur_request_nb]
                )
            except ConnectionError as connection_error:
                self.logger.error(
                    "[%s][SKIP] Connection error querying products : %s -> %s",
                    self.interface_name,
                    self.product_url,
                    connection_error,
                )
                break
            except ValueError as value_error:
                self.logger.error(
                    "[%s][SKIP] Value error querying products : %s -> %s",
                    self.interface_name,
                    self.product_url,
                    value_error,
                )
                break
            yield products_json

    def split_date_request_in_interval(
        self,
        start_date: datetime,
        end_date: datetime,
        max_number_day_to_retrieve_per_request: int,
    ) -> typing.List[typing.Tuple[datetime.datetime, datetime.datetime]]:
        """Create list of date tuple which split a large time interval between 2 date
        in smaller time interval configurable through max_number_day_to_retrieve_per_request
        eg in pseudo-code: start : monday  + end : friday + max_number.. 2
             [(monday,tuesday),(tuesday,wednesday),(wednesday,tuesday),(tuesday,friday)]

        Args:
            start_date (datetime): start date of interval
            end_date (datetime): end date of interval
            max_number_day_to_retrieve_per_request (int):
                                        number of day max per interval in the returned list

        Returns:
            List[Tuple(datetime.datetime, datetime.datetime)]: list of date interval tuple
        """
        split_list = []
        current_date_ref = start_date

        while current_date_ref <= end_date:
            if end_date - current_date_ref <= datetime.timedelta(
                days=max_number_day_to_retrieve_per_request - 1
            ):
                split_list.append((current_date_ref, end_date))
                break
            else:
                start_current_interval = current_date_ref
                end_current_interval = start_current_interval + datetime.timedelta(
                    days=max_number_day_to_retrieve_per_request - 1
                )
                split_list.append((start_current_interval, end_current_interval))
                current_date_ref = end_current_interval + datetime.timedelta(days=1)

        return split_list

    def _get_entities(
        self,
        date_interval: typing.List[typing.Tuple[datetime.datetime, datetime.datetime]],
    ) -> typing.Dict:
        """This function will query the weather API using the parameter given in the
        collector configuration and then return back the weather data

        Args:
            date_interval (List[Tuple[datetime.datetime, datetime.datetime]]):
            list of datetime tuple

        Raises:
            ValueError: If no status code 200

        Returns:
            typing.Dict: weather data retrieved from the API
        """
        query_url = (
            f"{self.product_url}/{self.weather_query_type}?latitude={self.latitude}"
            f"&longitude={self.longitude}{self.weather_additional_url_parameters}"
        )

        if date_interval:
            self.logger.debug(
                "Retrieve Weather products between %s and %s from %s for %s",
                date_interval[0],
                date_interval[1],
                self.product_url,
                self.interface_name,
            )

            start_date_str = date_interval[0].strftime("%Y-%m-%d")
            end_date_str = date_interval[1].strftime("%Y-%m-%d")
            query_url = (
                query_url + f"&start_date={start_date_str}&end_date={end_date_str}"
            )
        else:
            self.logger.debug(
                "Retrieve Weather and Forecast from %s for %s",
                self.product_url,
                self.interface_name,
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

        product_json = response.content

        return product_json
