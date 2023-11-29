"""EISPExtractor tests"""
import datetime
from dateutil import tz
import os
from maas_collector.rawdata.extractor import EISPExtractor


def test_eisp_extractor():
    xext = EISPExtractor()
    EISP_FILE = os.path.join(
        os.path.dirname(__file__),
        "data",
        "EISP",
        "S2A_OPER_REP_PASS_E_CGS2_20201202T083041_V20200322T214114_20200322T215214.EOF",
    )
    extract = list(xext.extract(EISP_FILE))


    assert extract == [
        {
            "satellite": "S2A",
            "downlinkOrbit": "24808",
            "station": "CGS2",
            "reportName": "S2A_OPER_REP_PASS_E_CGS2_20201202T083041_V20200322T214114_20200322T215214.EOF",
            "dataStripSensingStart": datetime.datetime(
                2020, 3, 22, 17, 33, 47, 72000, tzinfo=tz.UTC
            ),
            "dataStripSensingStop": datetime.datetime(
                2020, 3, 22, 17, 36, 29, 421000, tzinfo=tz.UTC
            ),
            "granuleCount": 552,
        },
        {
            "satellite": "S2A",
            "downlinkOrbit": "24808",
            "station": "CGS2",
            "reportName": "S2A_OPER_REP_PASS_E_CGS2_20201202T083041_V20200322T214114_20200322T215214.EOF",
            "dataStripSensingStart": datetime.datetime(
                2020, 3, 22, 18, 40, 30, 458000, tzinfo=tz.UTC
            ),
            "dataStripSensingStop": datetime.datetime(
                2020, 3, 22, 18, 49, 6, 369000, tzinfo=tz.UTC
            ),
            "granuleCount": 1728,
        },
    ]


def test_eisp_extractor2():
    xext = EISPExtractor()
    EISP_FILE = os.path.join(
        os.path.dirname(__file__),
        "data",
        "EISP",
        "S2B_OPER_REP_PASS_E_CGS2_20211008T135116_V20211006T075428_20211006T075757.EOF",
    )
    extract = list(xext.extract(EISP_FILE))

    assert extract == [
        {
            "satellite": "S2B",
            "downlinkOrbit": "23942",
            "station": "CGS2",
            "reportName": "S2B_OPER_REP_PASS_E_CGS2_20211008T135116_V20211006T075428_20211006T075757.EOF",
            "dataStripSensingStart": datetime.datetime(
                2021, 10, 6, 6, 30, 16, 519000, tzinfo=tz.UTC
            ),
            "dataStripSensingStop": datetime.datetime(
                2021, 10, 6, 6, 30, 34, 558000, tzinfo=tz.UTC
            ),
            "granuleCount": 72,
        },
        {
            "satellite": "S2B",
            "downlinkOrbit": "23942",
            "station": "CGS2",
            "reportName": "S2B_OPER_REP_PASS_E_CGS2_20211008T135116_V20211006T075428_20211006T075757.EOF",
            "dataStripSensingStart": datetime.datetime(
                2021, 10, 6, 6, 30, 45, 382000, tzinfo=tz.UTC
            ),
            "dataStripSensingStop": datetime.datetime(
                2021, 10, 6, 6, 31, 50, 321000, tzinfo=tz.UTC
            ),
            "granuleCount": 228,
        },
        {
            "satellite": "S2B",
            "downlinkOrbit": "23942",
            "station": "CGS2",
            "reportName": "S2B_OPER_REP_PASS_E_CGS2_20211008T135116_V20211006T075428_20211006T075757.EOF",
            "dataStripSensingStart": datetime.datetime(
                2021, 10, 6, 6, 32, 11, 968000, tzinfo=tz.UTC
            ),
            "dataStripSensingStop": datetime.datetime(
                2021, 10, 6, 6, 32, 40, 830000, tzinfo=tz.UTC
            ),
            "granuleCount": 108,
        },
        {
            "satellite": "S2B",
            "downlinkOrbit": "23942",
            "station": "CGS2",
            "reportName": "S2B_OPER_REP_PASS_E_CGS2_20211008T135116_V20211006T075428_20211006T075757.EOF",
            "dataStripSensingStart": datetime.datetime(
                2021, 10, 6, 6, 40, 17, 458000, tzinfo=tz.UTC
            ),
            "dataStripSensingStop": datetime.datetime(
                2021, 10, 6, 6, 41, 29, 613000, tzinfo=tz.UTC
            ),
            "granuleCount": 252,
        },
        {
            "satellite": "S2B",
            "downlinkOrbit": "23942",
            "station": "CGS2",
            "reportName": "S2B_OPER_REP_PASS_E_CGS2_20211008T135116_V20211006T075428_20211006T075757.EOF",
            "dataStripSensingStart": datetime.datetime(
                2021, 10, 6, 6, 43, 44, 463000, tzinfo=tz.UTC
            ),
            "dataStripSensingStop": datetime.datetime(
                2021, 10, 6, 6, 44, 2, 502000, tzinfo=tz.UTC
            ),
            "granuleCount": 72,
        },
        {
            "satellite": "S2B",
            "downlinkOrbit": "23942",
            "station": "CGS2",
            "reportName": "S2B_OPER_REP_PASS_E_CGS2_20211008T135116_V20211006T075428_20211006T075757.EOF",
            "dataStripSensingStart": datetime.datetime(
                2021, 10, 6, 7, 22, 5, 460000, tzinfo=tz.UTC
            ),
            "dataStripSensingStop": datetime.datetime(
                2021, 10, 6, 7, 22, 34, 322000, tzinfo=tz.UTC
            ),
            "granuleCount": 108,
        },
        {
            "satellite": "S2B",
            "downlinkOrbit": "23942",
            "station": "CGS2",
            "reportName": "S2B_OPER_REP_PASS_E_CGS2_20211008T135116_V20211006T075428_20211006T075757.EOF",
            "dataStripSensingStart": datetime.datetime(
                2021, 10, 6, 7, 58, 18, 287000, tzinfo=tz.UTC
            ),
            "dataStripSensingStop": datetime.datetime(
                2021, 10, 6, 7, 58, 21, 895000, tzinfo=tz.UTC
            ),
            "granuleCount": 24,
        },
        {
            "satellite": "S2B",
            "downlinkOrbit": "23942",
            "station": "CGS2",
            "reportName": "S2B_OPER_REP_PASS_E_CGS2_20211008T135116_V20211006T075428_20211006T075757.EOF",
            "dataStripSensingStart": datetime.datetime(
                2021, 10, 6, 7, 58, 54, 365000, tzinfo=tz.UTC
            ),
            "dataStripSensingStop": datetime.datetime(
                2021, 10, 6, 7, 59, 48, 481000, tzinfo=tz.UTC
            ),
            "granuleCount": 192,
        },
        {
            "satellite": "S2B",
            "downlinkOrbit": "23942",
            "station": "CGS2",
            "reportName": "S2B_OPER_REP_PASS_E_CGS2_20211008T135116_V20211006T075428_20211006T075757.EOF",
            "dataStripSensingStart": datetime.datetime(
                2021, 10, 6, 8, 0, 13, 736000, tzinfo=tz.UTC
            ),
            "dataStripSensingStop": datetime.datetime(
                2021, 10, 6, 8, 0, 38, 990000, tzinfo=tz.UTC
            ),
            "granuleCount": 96,
        },
        {
            "satellite": "S2B",
            "downlinkOrbit": "23942",
            "station": "CGS2",
            "reportName": "S2B_OPER_REP_PASS_E_CGS2_20211008T135116_V20211006T075428_20211006T075757.EOF",
            "dataStripSensingStart": datetime.datetime(
                2021, 10, 6, 8, 0, 49, 813000, tzinfo=tz.UTC
            ),
            "dataStripSensingStop": datetime.datetime(
                2021, 10, 6, 8, 1, 29, 499000, tzinfo=tz.UTC
            ),
            "granuleCount": 144,
        },
    ]
