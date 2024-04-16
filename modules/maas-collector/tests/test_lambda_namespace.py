import datetime
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

from maas_collector.rawdata.extractor import CSVExtractor


def test_regex_in_lambda():
    cext = CSVExtractor(
        [
            "product_id",
            {
                "field": "is_s2b",
                "python": 'lambda row: re.match("^S2B_.*$", row[0]) and True or False',
            },
        ]
    )

    extract = list(
        cext.extract(
            os.path.join(
                DATA_DIR,
                "OMCS-1234_LTA_S2B_DelList_20220830_V20220830_20220830.csv",
            )
        )
    )

    assert extract == [
        {
            "product_id": "S2B_OPER_MSI_L0__DS_2BPS_20220830T122617_S20220830T003155_N04.00.tar",
            "reportName": "OMCS-1234_LTA_S2B_DelList_20220830_V20220830_20220830.csv",
            "is_s2b": True,
        },
        {
            "product_id": "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003217_D11_N04.00.tar",
            "reportName": "OMCS-1234_LTA_S2B_DelList_20220830_V20220830_20220830.csv",
            "is_s2b": True,
        },
        {
            "product_id": "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003213_D12_N04.00.tar",
            "reportName": "OMCS-1234_LTA_S2B_DelList_20220830_V20220830_20220830.csv",
            "is_s2b": True,
        },
    ]


def test_datetime_in_lambda():
    cext = CSVExtractor(
        [
            "product_id",
            {
                "field": "product_date",
                "python": 'lambda row: datetime.datetime.strptime(row[0][25:40], "%Y%m%dT%H%M%S")',
            },
        ]
    )

    extract = list(
        cext.extract(
            os.path.join(
                DATA_DIR,
                "OMCS-1234_LTA_S2B_DelList_20220830_V20220830_20220830.csv",
            )
        )
    )

    assert extract == [
        {
            "product_id": "S2B_OPER_MSI_L0__DS_2BPS_20220830T122617_S20220830T003155_N04.00.tar",
            "reportName": "OMCS-1234_LTA_S2B_DelList_20220830_V20220830_20220830.csv",
            "product_date": datetime.datetime(2022, 8, 30, 12, 26, 17),
        },
        {
            "product_id": "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003217_D11_N04.00.tar",
            "reportName": "OMCS-1234_LTA_S2B_DelList_20220830_V20220830_20220830.csv",
            "product_date": datetime.datetime(2022, 8, 30, 12, 26, 17),
        },
        {
            "product_id": "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003213_D12_N04.00.tar",
            "reportName": "OMCS-1234_LTA_S2B_DelList_20220830_V20220830_20220830.csv",
            "product_date": datetime.datetime(2022, 8, 30, 12, 26, 17),
        },
    ]


def test_dateutils_parser_in_lambda():
    cext = CSVExtractor(
        [
            "product_id",
            {
                "field": "product_date",
                "python": "lambda row: parse_datetime(row[0][25:40])",
            },
        ]
    )

    extract = list(
        cext.extract(
            os.path.join(
                DATA_DIR,
                "OMCS-1234_LTA_S2B_DelList_20220830_V20220830_20220830.csv",
            )
        )
    )

    assert extract == [
        {
            "product_id": "S2B_OPER_MSI_L0__DS_2BPS_20220830T122617_S20220830T003155_N04.00.tar",
            "reportName": "OMCS-1234_LTA_S2B_DelList_20220830_V20220830_20220830.csv",
            "product_date": datetime.datetime(2022, 8, 30, 12, 26, 17),
        },
        {
            "product_id": "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003217_D11_N04.00.tar",
            "reportName": "OMCS-1234_LTA_S2B_DelList_20220830_V20220830_20220830.csv",
            "product_date": datetime.datetime(2022, 8, 30, 12, 26, 17),
        },
        {
            "product_id": "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003213_D12_N04.00.tar",
            "reportName": "OMCS-1234_LTA_S2B_DelList_20220830_V20220830_20220830.csv",
            "product_date": datetime.datetime(2022, 8, 30, 12, 26, 17),
        },
    ]
