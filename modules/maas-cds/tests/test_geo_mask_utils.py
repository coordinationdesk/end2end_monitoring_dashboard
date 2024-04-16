""" Module to test GeoMaskUtils class"""

from unittest.mock import patch
import unittest
from maas_cds.lib.geo_mask_utils import GeoMaskUtils
from opensearchpy.helpers.utils import AttrDict


def test_geo_cache():
    geo_mask_utils = GeoMaskUtils()

    geo_mask_utils.load_mask("OCN")

    assert "OCN" in GeoMaskUtils.CACHED_MASK


def test_s1_ew(s1_product_ew):
    geo_mask_utils = GeoMaskUtils()

    result = geo_mask_utils.coverage_over_specific_area_s1(
        s1_product_ew.instrument_mode, s1_product_ew.footprint
    )

    result_keys = result.keys()

    assert "SLC_coverage_percentage" in result_keys
    assert "OCN_coverage_percentage" in result_keys
    assert "EU_coverage_percentage" in result_keys


def test_s1_wv(s1_product_wv):
    geo_mask_utils = GeoMaskUtils()

    result = geo_mask_utils.coverage_over_specific_area_s1(
        s1_product_wv.instrument_mode, s1_product_wv.footprint
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
        GeoMaskUtils.OVER_SPECIFIC_AREA_GEOJSON["WRONGPATH"] = "resources/masks/YOLO"

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
    intersect = GeoMaskUtils().area_coverage(footprint, "SLC")

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
    intersect = GeoMaskUtils().area_coverage(footprint, "SLC")
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
