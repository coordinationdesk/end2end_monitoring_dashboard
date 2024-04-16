"""features a custom excel extractor for files attached to CAMS anomalies"""
import datetime
import hashlib
import os
import typing
import sys

import xlrd3

from maas_collector.rawdata.extractor.base import BaseExtractor


class AnomalyCorrelationExtractor(BaseExtractor):
    """

    A custom extractor for cams tickets impact report
    """

    # TODO put that in json config for codeless evolution ;) !

    IMPACT_CONFIG = [
        {
            "name": "datatake_ids",
            "sh_number": 2,
            "row_offset": 2,
            "column_ids": [0],
        },
        {
            "name": "acquisition_pass",
            "sh_number": 3,
            "row_offset": 2,
            "column_ids": [0, 1, 2, 3],
        },
        {
            "name": "products",
            "sh_number": 4,
            "row_offset": 2,
            "column_ids": [0],
        },
    ]

    def extract(self, path: str, report_folder: str = "") -> typing.Iterator[dict]:
        """override"""
        self.logger.info("Extracting from %s", path)

        md5 = hashlib.md5()
        md5.update(path.encode())
        md5.update(str(datetime.datetime.utcnow()).encode())

        correlation_id = md5.hexdigest()

        datetime.datetime.utcnow()

        # TODO build a unique report name with last update time
        report_name = os.path.basename(path)

        workbook = xlrd3.open_workbook(path)

        general_sheet = workbook.get_sheet(1)

        # pick global informations in header page
        data_dict = {
            "cams_issue": general_sheet.cell(2, 1).value.strip(),
            "origin": general_sheet.cell(3, 1).value.strip(),
            "description": general_sheet.cell(4, 1).value.strip(),
            "reportName": report_name,
            "correlation_id": correlation_id,
        }

        for config in self.IMPACT_CONFIG:

            sheet = workbook.get_sheet(config["sh_number"])

            data_dict[config["name"]] = [
                row
                for row in self.get_rows_data_from(
                    sheet, config["row_offset"], column_ids=config["column_ids"]
                )
            ]

        yield data_dict

    def get_rows_data_from(
        self, sheet: xlrd3.sheet.Sheet, row_offset: int, column_ids: list[int]
    ) -> typing.Iterator[list]:
        """Extract rows from a sheet

        Args:
            sheet (xlrd3.sheet.Sheet): sheet to extract from
            row_offset (int): row where data starts
            column_ids (list[int]): list of columns numbers to populate the row


        Yields:
            Iterator[list]: rows from the input sheet
        """

        # this method is so generic it could be placed inside xlsx extractor, or even
        # csv if a common abstraction exists (TabularExtract ?)

        has_data = True

        single_column = len(column_ids) == 1

        while has_data:

            try:
                row = [
                    value.strip() if isinstance(value, str) else value
                    for value in [
                        sheet.cell(row_offset, colx).value for colx in column_ids
                    ]
                ]
            except IndexError:
                self.logger.debug("No more data at row %s", row_offset)
                has_data = False
                continue

            if any(row):
                if single_column:
                    yield row[0]
                else:
                    yield row

            else:
                self.logger.debug("Skipping empty row: %s", row_offset)

            row_offset += 1

        self.logger.debug("Completed: %s rows were processed", row_offset)


if __name__ == "__main__":
    extractor = AnomalyCorrelationExtractor()
    print(next(extractor.extract(sys.argv[1])))
