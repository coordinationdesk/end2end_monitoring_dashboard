""" Module to test GeoMaskUtils class"""

from unittest.mock import patch
import unittest
from maas_cds import model
from maas_cds.lib.geo_mask_utils import GeoMaskUtils
from opensearchpy.helpers.utils import AttrDict


def test_geo_cache():
    geo_mask_utils = GeoMaskUtils()

    # Purge cache for test purpose
    GeoMaskUtils.CACHED_MASK = {}

    assert len(GeoMaskUtils.CACHED_MASK) == 0

    geo_mask_utils.load_mask("OCN")

    assert len(GeoMaskUtils.CACHED_MASK) > 0


def test_s1_ew(s1_product_ew):
    geo_mask_utils = GeoMaskUtils()

    result = geo_mask_utils.coverage_over_specific_area_s1(
        s1_product_ew.instrument_mode,
        s1_product_ew.footprint,
        s1_product_ew.sensing_start_date,
    )

    result_keys = result.keys()

    assert "SLC_coverage_percentage" in result_keys
    assert "OCN_coverage_percentage" in result_keys
    assert "EU_coverage_percentage" in result_keys


def test_s1_wv(s1_product_wv):
    geo_mask_utils = GeoMaskUtils()

    result = geo_mask_utils.coverage_over_specific_area_s1(
        s1_product_wv.instrument_mode,
        s1_product_wv.footprint,
        s1_product_wv.sensing_start_date,
    )

    assert result == {"EU_coverage_percentage": 0.0}


@patch("logging.Logger.warning")
def test_load_invalid_mask_name(logger_mock):
    geo_mask_utils = GeoMaskUtils()

    geo_mask_utils.load_mask("YOLO")

    logger_mock.assert_called_once()

    assert "YOLO" not in GeoMaskUtils.CACHED_MASK


@patch("logging.Logger.warning")
def test_load_all_mask(logger_mock):
    geo_mask_utils = GeoMaskUtils()

    for mask_name in GeoMaskUtils.OVER_SPECIFIC_AREA_GEOJSON:
        geo_mask_utils.load_mask(mask_name)

    assert logger_mock.call_count == 0


class MyTestCase(unittest.TestCase):
    def test_load_invalid_mask_path(self):

        GeoMaskUtils.OVER_SPECIFIC_AREA_GEOJSON["WRONGPATH"] = {
            "0": "resources/masks/YOLO"
        }

        with self.assertRaises(FileNotFoundError):
            GeoMaskUtils().load_mask("WRONGPATH")


@patch("logging.Logger.error")
def test_load_invalid_mask_path(logger_mock):
    MyTestCase().test_load_invalid_mask_path()

    logger_mock.assert_called_once()

    assert "WRONGPATH" not in GeoMaskUtils.CACHED_MASK


@patch("logging.Logger.warning")
def test_mask_not_loaded_coverage(logger_mock, s1_product_wv):
    GeoMaskUtils().area_coverage(s1_product_wv.footprint, "MASKNOTLOAD")

    assert logger_mock.call_count == 2


@patch("logging.Logger.warning")
def test_invalid_footprint_coverage(logger_mock, s1_product_wv):
    GeoMaskUtils().area_coverage(s1_product_wv.footprint[0:-5], "SLC")

    logger_mock.assert_called_once()


def test_intersect_svalbard():
    footprint = "Polygon((15 79, 15 80, 16 80, 16 79, 15 79))"

    intersect = GeoMaskUtils().area_coverage(
        footprint, "SLC", "2024-04-02T12:12:12.000Z"
    )

    assert intersect == 100


def test_intersect_format_geojson():
    footprint = {
        "type": "Polygon",
        "coordinates": [
            [
                [15, 79],
                [15, 80],
                [16, 80],
                [16, 79],
                [15, 79],
            ]
        ],
    }
    intersect = GeoMaskUtils().area_coverage(footprint, "SLC")

    assert intersect == 100


def test_intersect_specific_product():
    footprint = "POLYGON((128.563 -8.7541,129.2694 -8.6452,128.854 -6.8028,128.1508 -6.9098,128.563 -8.7541))"
    intersect = GeoMaskUtils().area_coverage(footprint, "SLC")
    assert intersect == 0
    intersect = GeoMaskUtils().area_coverage(footprint, "OCN")
    assert intersect == 100


def test_from_raw_product_footprint_geo(s1_raw_geopolygon):
    assert isinstance(s1_raw_geopolygon.footprint, AttrDict)
    intersect = GeoMaskUtils().area_coverage(s1_raw_geopolygon.footprint, "OCN")
    assert intersect == 100


def test_new_masks():
    footprint = {
        "type": "Polygon",
        "coordinates": [
            [
                [-68, -5.1],
                [-66, -5.1],
                [-66, -4.9],
                [-68, -4.9],
                [-68, -5.1],
            ]
        ],
    }

    intersect = GeoMaskUtils().area_coverage(
        footprint, "SLC", "2024-04-02T12:12:12.000Z"
    )

    assert intersect == 100


def test_intersect_format_geojson_eu_mask():

    # 🥐🥖
    footprint = {
        "coordinates": [
            [
                [-2, 49],
                [-2, 44],
                [6, 44],
                [6, 49],
                [-2, 49],
            ]
        ],
        "type": "Polygon",
    }
    intersect = GeoMaskUtils().area_coverage(footprint, "EU")

    assert intersect == 100


def test_groenland_coverage():

    footprint = "Polygon((-39.9765 80.9498,-17.6093 82.9458,-21.0764 83.8781,-44.8408 81.6605,-39.9765 80.9498))"
    intersect = GeoMaskUtils().area_coverage(footprint, "OCN")

    assert 19.46 < intersect < 19.47


def test_date_masks_impact_bug():
    raw_data_product_dict = {
        "reportName": "https://s1a.prip.copernicus.eu",
        "product_id": "9e839192-d960-4c1b-97b5-515cb46b95d2",
        "product_name": "S1A_IW_RAW__0SDV_20240705T235557_20240705T235629_054632_06A68B_D824.SAFE.zip",
        "content_length": 1604002216,
        "publication_date": "2024-07-06T00:47:36.686Z",
        "start_date": "2024-07-05T23:55:57.545Z",
        "end_date": "2024-01-05T23:56:29.944Z",  # fake previous date
        "origin_date": "2024-07-06T00:37:12.000Z",
        "eviction_date": "2024-07-19T12:47:36.298Z",
        "footprint": {
            "type": "Polygon",
            "coordinates": [
                [
                    [-71.6787, -53.635],
                    [-68.1222, -52.8622],
                    [-69.3888, -51.0393],
                    [-72.8177, -51.7742],
                    [-71.6787, -53.635],
                ]
            ],
        },
        "interface_name": "PRIP_S1A_Serco",
        "production_service_type": "PRIP",
        "production_service_name": "S1A-Serco",
        "ingestionTime": "2024-07-06T01:10:52.044Z",
    }
    raw_document = model.PripProduct(**raw_data_product_dict)
    raw_document.meta.id = "39f5dc8ab626c24fbd12e138679bf2bf"
    raw_document.full_clean()

    # OLD mask 12.7% NEW mask 20.883%
    geo_mask_utils = GeoMaskUtils()

    # OLD
    result = geo_mask_utils.coverage_over_specific_area_s1(
        "IW",
        raw_document.footprint,
        raw_document.end_date,  # fake previous date
    )

    assert result == {
        "OCN_coverage_percentage": 12.711695280606387,
        "EU_coverage_percentage": 0.0,
    }

    # NEW
    result = geo_mask_utils.coverage_over_specific_area_s1(
        "IW",
        raw_data_product_dict.get("footprint"),
        raw_document.start_date,
    )

    assert result == {
        "OCN_coverage_percentage": 20.870232761754124,
        "EU_coverage_percentage": 0.0,
    }
