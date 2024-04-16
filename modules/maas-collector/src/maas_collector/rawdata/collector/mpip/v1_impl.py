"""Mpip v1 implementation"""

from requests.exceptions import RequestException
from maas_collector.rawdata.collector.mpip.query_strategy import (
    AbstractMpipQueryStrategy,
)
from maas_model.date_utils import datestr_to_zulu


class MpipQueryV1Implementation(AbstractMpipQueryStrategy):
    """AbstractMpipQueryStrategy implementation for V1 version"""

    FILE_NAME_PATTERN = (
        "{interface_name}_" "{start_date}_" "{end_date}_" "P{current_page:06}.json"
    )

    def __iter__(self):
        """yields downloaded files"""

        current_page = 0
        total_files = 0
        need_more_request = True

        while need_more_request:
            if self.collector.should_stop_loop:
                break

            self.logger.debug(
                "Fetching File List Page %d for %s", current_page, self.interface_name
            )

            try:
                file_list_json = self._get_file_list(current_page)

            except RequestException as connection_error:
                self.logger.error(
                    "[%s][SKIP] Request Error querying file list : %s -> %s",
                    self.interface_name,
                    self.config.file_list_url,
                    connection_error,
                )
                break

            except ValueError as value_error:
                self.logger.error(
                    "[%s][SKIP] Value error querying file list : %s -> %s",
                    self.interface_name,
                    self.config.file_list_url,
                    value_error,
                )
                self.logger.exception(value_error)
                break

            yield file_list_json

            nb_entities = self._count_item_payload(file_list_json)

            total_files += nb_entities
            if nb_entities < self.product_per_page:
                need_more_request = False

            current_page += 1

        self.logger.info(
            "[%s] Finally retrieved %d files ", self.interface_name, total_files
        )

    def _count_item_payload(self, payload):
        return len(payload["value"])

    def _get_file_list(self, page):
        """Get the list of available files for a specific page"""
        # filtering parameters
        filter_attributes = [
            "filetypes",
            "extensions",
            "platforms",
            "fileclasses",
            "filenames",
            "sessionIds",
            "versions",
            "actives",
            "edrsCreationDate",
            "ingestionDate",
        ]

        # camelCase to snake_case lamda
        camel_to_snake = lambda name: "".join(
            f"_{char.lower()}" if char.isupper() else char for char in name
        )

        # Create the filtering data to be sent through the POST request
        # None attributes need to be filtered out or else the interface send a 500 error
        data = {
            attr: getattr(self.config, camel_to_snake(attr))
            for attr in filter_attributes
            if getattr(self.config, camel_to_snake(attr)) is not None
        }

        # Pagination is also in the filtering data
        data["pageNumber"] = page

        # Date filtering
        # MPIP interface sort in REVERSE (because why not ?) so we need to do some magic tricks 🧙‍♂️
        data["ingestionDate"] = datestr_to_zulu(str(self.mpip_start_date))

        headers = self.authentication.get_headers()
        response = self.http_session.post(
            self.config.file_list_url,
            json=data,
            headers=headers,
            timeout=self.collector.http_config.timeout,
        )

        # analyze request
        if not 200 <= response.status_code <= 300:
            self.logger.error(
                "Error querying %s %d: %s",
                self.config.file_list_url,
                response.status_code,
                response.content,
            )
            raise ValueError(f"Error querying {self.config.file_list_url}")

        file_list_json = response.json()
        # correct format to iterate through nodes with json extractor
        return_dict = {"value": file_list_json}
        return return_dict
