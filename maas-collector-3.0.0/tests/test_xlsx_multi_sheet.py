import os

from maas_collector.rawdata.extractor import (
    XLSXExtractor,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def test_xlsx_extractor_sheet_selection():
    extractor = XLSXExtractor(
        {
            "field1": "Header1",
            "field2": "Header2",
        },
        allow_partial=True,
        sheet_id=0,
    )

    extract = list(
        extractor.extract(
            os.path.join(
                DATA_DIR,
                "xlsx_multi_sheet.xlsx",
            )
        )
    )

    assert extract[0] == {
        "field1": 1,
        "field2": "A",
        "reportName": "xlsx_multi_sheet.xlsx",
    }

    extractor = XLSXExtractor(
        {
            "field1": "Header1",
            "field2": "Header2",
        },
        allow_partial=True,
        sheet_id="Sheet1",
    )

    extract = list(
        extractor.extract(
            os.path.join(
                DATA_DIR,
                "xlsx_multi_sheet.xlsx",
            )
        )
    )

    assert extract[0] == {
        "field1": 1,
        "field2": "A",
        "reportName": "xlsx_multi_sheet.xlsx",
    }

    extractor = XLSXExtractor(
        {
            "field1": "Header3",
            "field2": "Header4",
        },
        allow_partial=True,
        sheet_id=1,
    )

    extract = list(
        extractor.extract(
            os.path.join(
                DATA_DIR,
                "xlsx_multi_sheet.xlsx",
            )
        )
    )

    assert extract[0] == {
        "field1": 11,
        "field2": "K",
        "reportName": "xlsx_multi_sheet.xlsx",
    }

    extractor = XLSXExtractor(
        {
            "field1": "Header3",
            "field2": "Header4",
        },
        allow_partial=True,
        sheet_id="Sheet2",
    )

    extract = list(
        extractor.extract(
            os.path.join(
                DATA_DIR,
                "xlsx_multi_sheet.xlsx",
            )
        )
    )

    assert extract[0] == {
        "field1": 11,
        "field2": "K",
        "reportName": "xlsx_multi_sheet.xlsx",
    }
