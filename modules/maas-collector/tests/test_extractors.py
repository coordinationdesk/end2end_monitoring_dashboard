"""
Test extractor classes with first bunch of data provided by Cap Gemini Italy.

Data format will surely change and some rewrite of the tests will happen.
"""
import os

from maas_collector.rawdata.extractor.base import BaseExtractor, get_hash_func

from maas_collector.rawdata.extractor import (
    XMLExtractor,
    JSONExtractor,
    JSONExtractorExtended,
    LogExtractor,
    CSVExtractor,
    XLSXExtractor,
)

# import logging
import pytest

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

TEST_DICT = {"attr1": "value1", "attr2": "value2", "attr3": "value3"}


def test_get_hash_func():
    func = get_hash_func("attr1", "attr2")
    assert callable(func)
    assert func(TEST_DICT) == "b63d4be92e3bcf7a039e795a6d44e262"


def test_convert_data_extract_values():
    class DumbExtractor(BaseExtractor):
        def extract(self, path, report_folder: str = ""):
            yield self.convert_data_extract_values(TEST_DICT)

    extractor = DumbExtractor(converter_map={"attr1": lambda value: value * 2})
    data = list(extractor.extract(None))[0]
    assert data["attr1"] == "value1value1"


def test_json_extractor():
    jext = JSONExtractor(
        attr_map={
            "productName": "$.Quality_report.Processing_data.Input_PDI",
            "globalStatus": "$.Quality_report.Quality_cheks.'-global_status'",
        }
    )
    extract = list(
        jext.extract(
            os.path.join(
                DATA_DIR,
                "PRIP_QA_20200714144443_S2B_OPER_MSI_L2A_TL_SGS__20200714T120236_A015250_T26QPE_N02.14_report.json",
            )
        )
    )[0]
    assert (
        extract["productName"]
        == "S2B_OPER_MSI_L2A_TL_SGS__20200714T120236_A015250_T26QPE_N02.14"
    )
    assert extract["globalStatus"] == "FAILED"


def test_json_extractor_conv():
    jext = JSONExtractor(
        attr_map={
            "productName": "$.Quality_report.Processing_data.Input_PDI",
            "productDate": "$.Quality_report.Processing_data.Input_PDI",
        },
        converter_map={
            "productDate": {
                "type": "regex",
                "expression": r".*_(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(\d{2})_.*",
                "format": "{}-{}-{}T:{}:{}:{}.00Z",
            }
        },
    )
    extract = list(
        jext.extract(
            os.path.join(
                DATA_DIR,
                "PRIP_QA_20200714144443_S2B_OPER_MSI_L2A_TL_SGS__20200714T120236_A015250_T26QPE_N02.14_report.json",
            )
        )
    )[0]
    assert (
        extract["productName"]
        == "S2B_OPER_MSI_L2A_TL_SGS__20200714T120236_A015250_T26QPE_N02.14"
    )
    assert extract["productDate"] == "2020-07-14T:12:02:36.00Z"


def test_json_iterate():
    jext = JSONExtractor(
        attr_map={
            "jiraKey": "`this`.id",
            "author": "`this`.author.emailAddress",
            "creationDate": "`this`.created"
            # "globalStatus": "$.Quality_report.Quality_cheks.'-global_status'",
        },
        iterate_nodes="$.changelog.histories",
    )
    extract = list(
        jext.extract(
            os.path.join(
                DATA_DIR,
                "jira_like_json_iterate_test.json",
            )
        )
    )[0]

    assert extract["jiraKey"] == "1656614"
    assert extract["author"] == "yvan.lebras@airbus.com"
    assert extract["creationDate"] == "2020-04-03T09:27:54.000+0200"


def test_json_iterate_partial():
    jext = JSONExtractor(
        attr_map={
            "jiraKey": "`this`.id",
            "author": "`this`.author.emailAddress",
            "creationDate": "`this`.created",
            "doesNotExists": "`this`.doesNotExists",
        },
        iterate_nodes="$.changelog.histories",
        allow_partial=True,
    )

    extract = list(
        jext.extract(
            os.path.join(
                DATA_DIR,
                "jira_like_json_iterate_test.json",
            )
        )
    )[0]

    assert extract["jiraKey"] == "1656614"
    assert extract["author"] == "yvan.lebras@airbus.com"
    assert extract["creationDate"] == "2020-04-03T09:27:54.000+0200"
    assert extract["doesNotExists"] is None

    jext = JSONExtractor(
        attr_map={
            "jiraKey": "`this`.id",
            "author": "`this`.author.emailAddress",
            "creationDate": "`this`.created",
            "doesNotExists": "`this`.doesNotExists",
        },
        iterate_nodes="$.changelog.histories",
    )

    # test no partial
    with pytest.raises(IndexError):
        list(
            jext.extract(
                os.path.join(
                    DATA_DIR,
                    "jira_like_json_iterate_test.json",
                )
            )
        )


def test_json_extractor_evil_python():
    jext = JSONExtractor(
        attr_map={
            "satellite": {
                "python": "lambda c: c['Quality_report']['Processing_data']['Input_PDI'][:3]"
            },
        }
    )
    extract = list(
        jext.extract(
            os.path.join(
                DATA_DIR,
                "PRIP_QA_20200714144443_S2B_OPER_MSI_L2A_TL_SGS__20200714T120236_A015250_T26QPE_N02.14_report.json",
            )
        )
    )[0]
    assert extract["satellite"] == "S2B"


def test_xml_extractor():
    xext = XMLExtractor(
        attr_map={
            # handle callable case
            "productNameLambda": lambda root: root.find("Product").attrib["name"],
            # handle attribue value
            "productNameDict": {
                "path": "Product",
                "attr": "name",
            },
            # handle simple path
            "size": "Product/Size",
        }
    )
    extract = list(
        xext.extract(
            os.path.join(
                DATA_DIR,
                "S2A_OPER_PRD_L0__DS_SGS__20200420T205828_S20200322T173347_SIZE.xml",
            )
        )
    )[0]

    assert (
        extract["productNameLambda"]
        == "S2A_OPER_PRD_L0__DS_SGS__20201201T141044_S20191208T030316"
    )
    assert extract["productNameLambda"] == extract["productNameDict"]
    assert extract["size"] == "132456789"


def test_xml_partial():
    xext = XMLExtractor(
        attr_map={"size": "Product/Size", "doesNotExist": "I/Dont/Exist"},
        allow_partial=True,
    )
    extract = list(
        xext.extract(
            os.path.join(
                DATA_DIR,
                "S2A_OPER_PRD_L0__DS_SGS__20200420T205828_S20200322T173347_SIZE.xml",
            )
        )
    )[0]

    assert extract["size"] == "132456789"
    assert extract["doesNotExist"] is None


def test_xml_root_attr():
    xext = XMLExtractor(
        attr_map={"datastripIdentifier": {"attr": "datastripIdentifier"}}
    )
    extract = list(
        xext.extract(
            os.path.join(
                DATA_DIR,
                "S2A_OPER_MTD_L0U_DS_SGS__20201201T141044_S20191208T030316.xml",
            )
        )
    )[0]
    assert (
        extract["datastripIdentifier"]
        == "S2A_OPER_MSI_L0U_DS_SGS__20201201T141044_S20191208T030316_N00.00"
    )


def test_xml_bad_attr_map():
    with pytest.raises(ValueError):
        XMLExtractor(attr_map={"some_attr": False})


def test_xml_conv():
    """"""
    xext = XMLExtractor(
        attr_map={"orbit_number": "General_Info/Downlink_Info/DOWNLINK_ORBIT_NUMBER"},
        converter_map={"orbit_number": int},
    )
    extract = list(
        xext.extract(
            os.path.join(
                DATA_DIR,
                "S2A_OPER_MTD_L0U_DS_SGS__20201201T141044_S20191208T030316.xml",
            )
        )
    )[0]
    assert isinstance(extract["orbit_number"], int)
    assert extract["orbit_number"] == 22357

    # def test_xml_iterate_nodes_w_path():
    xext = XMLExtractor(
        attr_map={"dsdb_name": None},
        iterate_nodes="dsdb_list/dsdb_name",
    )
    extract_list = list(
        xext.extract(
            os.path.join(
                DATA_DIR,
                "DCS_02_L20191003131732787001008_ch1_DSIB.xml",
            )
        )
    )

    assert len(extract_list) == 9
    assert (
        extract_list[0]["dsdb_name"]
        == "DCS_02_L20191003131732787001008_ch1_DSDB_00001.raw"
    )


def test_xml_iterate_nodes_w_lambda():
    xext = XMLExtractor(
        attr_map={"dsdb_name": lambda element: element.text},
        iterate_nodes=lambda root: root.findall("dsdb_list/dsdb_name"),
    )
    extract_list = list(
        xext.extract(
            os.path.join(
                DATA_DIR,
                "DCS_02_L20191003131732787001008_ch1_DSIB.xml",
            )
        )
    )

    assert len(extract_list) == 9
    assert (
        extract_list[0]["dsdb_name"]
        == "DCS_02_L20191003131732787001008_ch1_DSDB_00001.raw"
    )


def test_xml_default_namespace():
    pass


def test_log_extractor():
    lext = LogExtractor(
        r"\[PRIP-INGESTOR-.+\]"
        + r"\[(?P<publicationDate>\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\.\d{3})\]\[\d+\]"
        + r"\[MON\]PDI:\s+(?P<productName>.+)\s+has.+"
        + r"datatakeIdentifier=\"(?P<datatakeIdentifier>.+)\"\s+"
        + r"RECEPTION_STATION=\"(?P<receptionStation>.+)\"\s+"
        + r"size=\"(?P<size>\d+)\".*",
        # converter_map={"publicationDate": model.PRIPIng.convert_log_date},
    )
    extract = list(
        lext.extract(
            os.path.join(
                DATA_DIR,
                "PRIP_ING_20200714124400.log",
            )
        )
    )[0]
    expected = {
        "publicationDate": "2020-07-14 14:44:44.734",
        "productName": "S2B_OPER_MSI_L2A_TL_SGS__20200714T120236_A015250_T26QPD_N02.14",
        "datatakeIdentifier": "GS2B_20200226T065839_015533_N02.14",
        "receptionStation": "MTI_",
        "size": "12233443545",
        "reportName": "PRIP_ING_20200714124400.log",
    }
    assert extract == expected


def test_csv_extractor_dict():
    cext = CSVExtractor(
        {
            "satellite": "SatelliteID",
            "DownlinkDuration": "DownlinkDuration[msec]",
            "calculated": {"python": "lambda row: 'TEST'"},
        }
    )

    extract = list(
        cext.extract(
            os.path.join(
                DATA_DIR,
                "MP_ALL__MTL_20210722T120000_20210809T150000.csv",
            )
        )
    )

    assert extract[0] == {
        "satellite": "S2B",
        "DownlinkDuration": "283372",
        "reportName": "MP_ALL__MTL_20210722T120000_20210809T150000.csv",
        "calculated": "TEST",
    }

    assert len(extract) == 1354

    assert extract[-1] == {
        "satellite": "S2B",
        "DownlinkDuration": "401444",
        "reportName": "MP_ALL__MTL_20210722T120000_20210809T150000.csv",
        "calculated": "TEST",
    }


def test_csv_extractor_list():
    cext = CSVExtractor(
        ["product_id", {"field": "interface_type", "python": "lambda row: 'LTA'"}]
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
            "interface_type": "LTA",
        },
        {
            "product_id": "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003217_D11_N04.00.tar",
            "reportName": "OMCS-1234_LTA_S2B_DelList_20220830_V20220830_20220830.csv",
            "interface_type": "LTA",
        },
        {
            "product_id": "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003213_D12_N04.00.tar",
            "reportName": "OMCS-1234_LTA_S2B_DelList_20220830_V20220830_20220830.csv",
            "interface_type": "LTA",
        },
    ]


def test_csv_extractor_list_partial():
    cext = CSVExtractor(
        [
            "product_id",
            "missing_field",
            {"field": "interface_type", "python": "lambda row: 'LTA'"},
        ],
        allow_partial=True,
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
            "interface_type": "LTA",
        },
        {
            "product_id": "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003217_D11_N04.00.tar",
            "reportName": "OMCS-1234_LTA_S2B_DelList_20220830_V20220830_20220830.csv",
            "interface_type": "LTA",
        },
        {
            "product_id": "S2B_OPER_MSI_L0__GR_2BPS_20220830T122617_S20220830T003213_D12_N04.00.tar",
            "reportName": "OMCS-1234_LTA_S2B_DelList_20220830_V20220830_20220830.csv",
            "interface_type": "LTA",
        },
    ]


def test_xlsx_extractor_dict():
    cext = XLSXExtractor(
        {
            "satellite_id": "Satellite",
            "doy": "DOY",
            "downlink_orbit": "Downlink Orbit",
            "calculated": {"python": "lambda row: 'TEST'"},
        }
    )

    extract = list(
        cext.extract(
            os.path.join(
                DATA_DIR,
                "S2_COP_REP_PERF_CGS-INS__20220522T122038_V20220521T120000_20220522T115959.xlsx",
            )
        )
    )

    assert extract[0] == {
        "satellite_id": "SENTINEL-2A",
        "doy": 141,
        "downlink_orbit": 36102,
        "reportName": "S2_COP_REP_PERF_CGS-INS__20220522T122038_V20220521T120000_20220522T115959.xlsx",
        "calculated": "TEST",
    }


def test_xlsx_extractor_dict_partial():
    cext = XLSXExtractor(
        {
            "satellite_id": "Satellite",
            "doy": "DOY",
            "downlink_orbit": "Downlink Orbit",
            "calculated": {"python": "lambda row: 'TEST'"},
            "missing_field": "Missing",
        },
        allow_partial=True,
    )

    extract = list(
        cext.extract(
            os.path.join(
                DATA_DIR,
                "S2_COP_REP_PERF_CGS-INS__20220522T122038_V20220521T120000_20220522T115959.xlsx",
            )
        )
    )

    assert extract[0] == {
        "satellite_id": "SENTINEL-2A",
        "doy": 141,
        "downlink_orbit": 36102,
        "reportName": "S2_COP_REP_PERF_CGS-INS__20220522T122038_V20220521T120000_20220522T115959.xlsx",
        "calculated": "TEST",
        "missing_field": None,
    }


def test_xlsx_extractor_list():
    cext = XLSXExtractor(
        ["product_id", {"field": "interface_type", "python": "lambda row: 'LTA'"}],
        data_row_offset=0,
    )

    extract = list(
        cext.extract(
            os.path.join(
                DATA_DIR, "OMCS-4321_LTA_S1A__DelList_20220823_V20220818_20220818.xlsx"
            )
        )
    )

    assert extract == [
        {
            "product_id": "S1A_IW_GRDH_1ADV_20220818T185009_20220818T185038_044610_055336_B57B.SAFE.zip",
            "reportName": "OMCS-4321_LTA_S1A__DelList_20220823_V20220818_20220818.xlsx",
            "interface_type": "LTA",
        },
        {
            "product_id": "S1A_IW_GRDH_1ADV_20220818T185038_20220818T185103_044611_055336_CF47.SAFE.zip",
            "reportName": "OMCS-4321_LTA_S1A__DelList_20220823_V20220818_20220818.xlsx",
            "interface_type": "LTA",
        },
    ]


def test_xlsx_extractor_list_partial():
    cext = XLSXExtractor(
        [
            "product_id",
            "missing_field",
            {"field": "interface_type", "python": "lambda row: 'LTA'"},
        ],
        data_row_offset=0,
        allow_partial=True,
    )

    extract = list(
        cext.extract(
            os.path.join(
                DATA_DIR, "OMCS-4321_LTA_S1A__DelList_20220823_V20220818_20220818.xlsx"
            )
        )
    )

    assert extract == [
        {
            "product_id": "S1A_IW_GRDH_1ADV_20220818T185009_20220818T185038_044610_055336_B57B.SAFE.zip",
            "reportName": "OMCS-4321_LTA_S1A__DelList_20220823_V20220818_20220818.xlsx",
            "interface_type": "LTA",
            "missing_field": None,
        },
        {
            "product_id": "S1A_IW_GRDH_1ADV_20220818T185038_20220818T185103_044611_055336_CF47.SAFE.zip",
            "reportName": "OMCS-4321_LTA_S1A__DelList_20220823_V20220818_20220818.xlsx",
            "interface_type": "LTA",
            "missing_field": None,
        },
    ]


def test_json_extraction_with_advanced_extraction_path():
    jext = JSONExtractorExtended(
        attr_map={
            "productGroup_id": '`this`.Attributes[?Name=="productGroupId"].Value',
            "datastrip_id": '`this`.Attributes[?Name=="datastripId"].Value',
            "qualityStatus": '`this`.Attributes[?Name=="qualityStatus"].Value',
            "cloudCover": '`this`.Attributes[?Name=="cloudCover"].Value',
        },
        iterate_nodes="$.value",
        allow_partial=True,
    )
    extract = list(
        jext.extract(
            os.path.join(
                DATA_DIR,
                "PRIP_S2A_ATOS_20240124T162320_20240124T163320_1000_P000000.json",
            )
        )
    )
    assert extract[0] == {
        "productGroup_id": "GS2A_20240124T140451_044866_N05.10",
        "reportName": "PRIP_S2A_ATOS_20240124T162320_20240124T163320_1000_P000000.json",
        "datastrip_id": "S2A_OPER_MSI_L1C_DS_2APS_20240124T155206_S20240124T140447_N05.10",
        "qualityStatus": "NOMINAL",
        "cloudCover": 10.2811222880479,
    }
