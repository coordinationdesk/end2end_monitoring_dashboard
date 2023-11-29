import os
import datetime
from maas_collector.rawdata.extractor import XLSXColumnExtractor

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def test_xlsx_column_bank_holidays():
    extractor = XLSXColumnExtractor(header_field="country", column_field="holiday_date")

    extract = list(
        extractor.extract(
            os.path.join(
                DATA_DIR,
                "Bank_Holidays_2023_per_country.xlsx",
            )
        )
    )

    assert extract[0] == {
        "country": "BELGIUM",
        "holiday_date": datetime.datetime(2023, 1, 1, 0, 0),
        "reportName": "Bank_Holidays_2023_per_country.xlsx",
    }

    assert extract[-1] == {
        "country": "ICELAND",
        "holiday_date": datetime.datetime(2023, 12, 31, 0, 0),
        "reportName": "Bank_Holidays_2023_per_country.xlsx",
    }
