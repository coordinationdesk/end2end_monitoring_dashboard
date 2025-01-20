"""
A custom extractor for EDRS Acquisition Passes Status
"""

import datetime
import os
import re
import sys
import typing

import xlrd3

from maas_collector.rawdata.extractor.base import BaseExtractor


class EDRSApsExtractor(BaseExtractor):
    """

    Custom extractor for EDRS Acquisition Passes Status Reports (xlsx).
    """

    INGESTION_META_DATA = {
        "interface_name": "Jira_EDRS",
        "production_service_name": "EDRS-Operations",
        "production_service_type": "EDRS",
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._doy = None

        self._base_date = None

    def extract(self, path: str, report_folder: str = "") -> typing.Iterator[dict]:
        """override"""

        report_name = os.path.basename(path)

        workbook = xlrd3.open_workbook(path)

        sheet = workbook.get_sheet(0)

        # try to find the year. may file naming be safer ?
        date_cell = sheet.cell(6, 17)

        if isinstance(date_cell.value, str):
            # Look like '52-1 / 2023-2024 or '52-1 / 2023
            match = re.search(r"20\d{2}", date_cell.value)

            if not match:
                raise ValueError(
                    f"No year in DATE cell R7: {date_cell.value} in {path}"
                )

            # calculate current year for the report, used as base for later date compute
            # as day of the year is the only information in the report
            self._base_date = datetime.datetime(
                year=int(match.group(0)),
                month=1,
                day=1,
                tzinfo=datetime.timezone.utc,
            )
        elif date_cell.ctype is xlrd3.XL_CELL_DATE:
            # keep only the year to later add doy
            self._base_date = datetime.datetime(
                year=xlrd3.xldate.xldate_as_datetime(
                    date_cell.value, workbook.date_mode
                ).year,
                month=1,
                day=1,
            )

        else:
            raise TypeError(
                "Temptation to guess date from "
                f"{date_cell.value} ({date_cell.ctypes}) failed"
            )

        self.logger.debug("Extracted base date is %s", self._base_date)

        # the index of the row where effective data starts
        start_index = None

        # as common cells are merged, reference to the previous row is need for second
        # line ingestion
        previous_row = None

        for index, row in enumerate(sheet.get_rows()):
            if self.should_stop:
                break

            # guess the beginning of data, quite empirical ...
            if start_index is None:
                if row[1].value == "LINK SESSIONS DETAILS":
                    start_index = index
                continue

            # skip header on 2 lines
            if index <= start_index + 2:
                continue

            if not previous_row and not any([cell.value for cell in row]):
                # skip empty line
                continue

            if row[1].value:
                # data_row is the first row of the group, holding the common attributes
                data_row = row
            else:
                data_row = previous_row

            if not previous_row:
                previous_row = row
            else:
                previous_row = None

            try:
                data = self.extract_row(data_row, row)

                data["reportName"] = report_name

                for substring, report_type in [
                    (" DOR ", "daily"),
                    (" WOR ", "weekly"),
                    (" MOR ", "monthly"),
                ]:
                    if substring in report_name:
                        data["report_type"] = report_type
                        break
                yield data

            # catch broad exception to not break the loop
            # pylint: disable=W0703
            except Exception as error:
                self.logger.error("Error at row %s in %s: %s", index, path, error)

    def extract_row(self, data_row, row) -> dict:
        """extract data from row

        Args:
            data_row (row): the common attribute row
            row (row): the current row, same as data_row for first of the group

        Returns:
            dict: extracted dictionnary
        """

        data = {}

        data["link_session_id"] = data_row[1].value

        data["geo_satellite_id"] = data_row[2].value

        data["satellite_id"] = data_row[3].value

        data["mission"] = data_row[3].value[:2]

        data["doy"] = doy = int(data_row[4].value)

        if self._doy is not None and self._doy != doy and doy == 1:
            # handle year change: change base date
            self._base_date = datetime.datetime(
                year=self._base_date.year + 1, month=1, day=1
            )
            self.logger.info("Detect change of year: %s - %s", self._doy, doy)

        self._doy = doy

        data["planned_link_session_start"] = self.calculate_datetime_from_delta_cell(
            doy, data_row[5]
        )

        data["planned_link_session_stop"] = self.calculate_datetime_from_delta_cell(
            doy, data_row[6]
        )

        if data["planned_link_session_stop"] < data["planned_link_session_start"]:
            # session starts before midnight and ends after midnight
            data["planned_link_session_stop"] += datetime.timedelta(days=1)

        assert data["planned_link_session_start"] < data["planned_link_session_stop"]

        data["moc_accept_status"] = data_row[7].value

        data["uplink_status"] = data_row[8].value

        data["spacecraft_execution"] = data_row[9].value

        data["edte_acquisition_status"] = data_row[10].value

        data["dcsu_archive_status"] = data_row[11].value

        data["sfdap_dissem_status"] = data_row[12].value

        data["total_status"] = data_row[13].value

        # next, station specific attributes that depend on row, not common data_row

        data["ground_station"] = row[14].value

        if row[15].value:
            # field may be missing if NOK status
            try:
                data["dissemination_start"] = self.calculate_datetime_from_delta_cell(
                    doy, data_row[15]
                )

            # catch broad exception to not break the loop and set default value
            # pylint: disable=W0703
            except Exception as exception:
                self.logger.exception(exception)
                data["dissemination_start"] = None

        if row[16].value:
            # field may be missing if NOK status
            try:
                data["dissemination_stop"] = self.calculate_datetime_from_delta_cell(
                    doy, data_row[16]
                )

            # catch broad exception to not break the loop and set default value
            # pylint: disable=W0703
            except Exception as exception:
                self.logger.exception(exception)
                data["dissemination_stop"] = None
            else:
                if data["dissemination_stop"] < data["dissemination_start"]:
                    # dissemination starts before midnight and ends after midnight
                    data["dissemination_stop"] += datetime.timedelta(days=1)

        data["cadus"] = row[17].value

        data["fer"] = row[18].value

        data["archived_data_size"] = row[19].value

        data["disseminated_data"] = row[20].value

        data["notes"] = data_row[21].value

        data.update(self.INGESTION_META_DATA)

        self.clean_up_strings(data)

        return data

    @staticmethod
    def clean_up_strings(data_dict: dict()):
        """Set empty string values to None to prevent number parsing errors

        Args:
            data_dict (dict): data dictionnary
        """
        for key, value in data_dict.items():
            if isinstance(value, str):
                value = value.strip()
                if value == "":
                    data_dict[key] = None
                else:
                    data_dict[key] = value

    def calculate_datetime_from_delta_cell(
        self, doy: int, delta_cell
    ) -> datetime.datetime:
        """calculate a datetime from a base date, day of the year and a cell containing
        a time delta

        Args:
            doy (int): day of the year
            delta_cell (xlrd cell): a cell from a xlrd sheet

        Raises:
            ValueError: when calculation is impossible

        Returns:
            datetime.datetime: the calculated datetime
        """

        if delta_cell.ctype is xlrd3.XL_CELL_DATE:
            delta = datetime.timedelta(days=doy - 1 + delta_cell.value)

        elif delta_cell.ctype is xlrd3.XL_CELL_TEXT:
            try:
                hours, minutes, seconds = [
                    int(token) for token in delta_cell.value.split(":")
                ]
                delta = datetime.timedelta(
                    days=doy - 1, hours=hours, minutes=minutes, seconds=seconds
                )
            except ValueError as error:
                raise ValueError(
                    f"Cannot extract time from string '{delta_cell.value}'"
                ) from error

        else:
            raise ValueError(
                f"Cannot calculate time delta from {delta_cell} ({delta_cell.ctype})"
            )

        return self._base_date + delta


if __name__ == "__main__":
    extractor = EDRSApsExtractor()

    for extract_data in extractor.extract(sys.argv[1]):
        print(extract_data)
