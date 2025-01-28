"""Module to operate geo feature """

import logging
import json

import pkgutil

from maas_cds.lib.config import get_good_threshold_config_from_value
from shapely.wkt import loads
from shapely.geometry import GeometryCollection, shape
from shapely.errors import ShapelyError
import pyproj

from maas_model import datetime_to_zulu, ZuluDate
from maas_cds.model.datatake_s1 import CdsDatatakeS1

from opensearchpy.helpers.utils import AttrDict


class GeoMaskUtils:
    """Class to manage mask and intersection"""

    OVER_SPECIFIC_AREA_GEOJSON = {
        "OCN": {
            "0": "ne_110m_ocean.geojson",
            "2024-06-06T13:20:00.000Z": "simplified_sea_cls.geojson",
        },
        "SLC": {
            "0": "EW_SLC_area.geojson",
            "2024-01-29T22:47:05.000Z": "EW_SLC_area_v2.geojson",
        },
        "EU": {"0": "EU_area.json"},
    }

    COVERING_AREA_FIELD = "_coverage_percentage"

    CACHED_MASK = {}

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

    def load_mask(self, mask_name, nearest_time_indicators="0"):
        """Load mask from his identifier (his name)

        Args:
            mask_name (str): identifier of the mask
        """

        config_mask = self.OVER_SPECIFIC_AREA_GEOJSON.get(mask_name, None)

        if config_mask is None:
            self.logger.warning(
                "[%s] - Mask not found",
                config_mask,
            )

            return

        mask_filename = config_mask.get(nearest_time_indicators, None)

        if mask_filename is None:
            self.logger.warning(
                "[%s] - Mask not found",
                mask_filename,
            )

            return

        self.logger.debug(
            "[%s] - Loaded mask",
            mask_name,
        )

        geojson_data = {}
        try:
            geojson_data = json.loads(
                pkgutil.get_data("maas_cds", f"resources/masks/{mask_filename}")
            )

        except FileNotFoundError as file_error:
            self.logger.error("[%s] - Mask path invalid : %s", mask_name, mask_filename)
            raise file_error

        mask_shapes = GeometryCollection(
            [
                shape(feature["geometry"]).buffer(0)
                for feature in geojson_data["features"]
            ]
        )

        self.CACHED_MASK[mask_filename] = mask_shapes

    def get_mask(self, mask_name, time_indicator="0"):
        """Get mask from his identifier (his name)

        Args:
            mask_name (str): identifier of the mask

        Returns:
            Polygons: The mask with shapely format (Polygons)
        """
        (nearest_time_indicator, file_name) = get_good_threshold_config_from_value(
            self.OVER_SPECIFIC_AREA_GEOJSON.get(mask_name, {}), time_indicator
        )

        if file_name not in self.CACHED_MASK:
            self.load_mask(mask_name, nearest_time_indicator)
        else:
            self.logger.debug(
                "[%s] - Mask already loaded (%s)", mask_name, nearest_time_indicator
            )

        return self.CACHED_MASK.get(file_name, None)

    def load_area_shape_from_footprint(self, footprint):
        """Load shapely object from footprint

        Args:
            footprint (any): Footprint to convert

        Returns:
            Geometry: Shapely geometry object
        """

        product_shape = None
        # Geojson
        if isinstance(footprint, AttrDict):
            footprint = footprint.to_dict()

        if isinstance(footprint, dict):
            feature_type = footprint.get("type")

            if feature_type != "Polygon":
                self.logger.warning(
                    "[FOOTPRINT] - Given footprint isn't a polygon : %s",
                    feature_type,
                )

            else:
                product_shape = shape(footprint)

        elif isinstance(footprint, str):
            try:
                # Reformat footprint
                if ";" in footprint and footprint.startswith("geography"):
                    footprint = footprint.split(";")[1]
                product_shape = loads(footprint)

            except ShapelyError:
                self.logger.warning(
                    "[FOOTPRINT] - Cannot load str footprint : %s", footprint
                )

        else:
            self.logger.warning(
                "[FOOTPRINT] - Unhandle footprint format  : %s",
                footprint,
            )

        return product_shape

    def area_coverage(self, footprint, mask_name, date_indicator="0"):
        """Get the coverage of the footprint on the mask identified by the mask_name

        Area is calculated in square meters to match products calculus method.

        https://pyproj4.github.io/pyproj/stable/api/geod.html#pyproj.Geod.polygon_area_perimeter
        https://en.wikipedia.org/wiki/Geodesics_on_an_ellipsoid#Area_of_a_geodesic_polygon

        Args:
            footprint (str | dict): The footprint (ex: "Polygon((..., ...))" or GeoJSON)
            mask_name (str):identifier of the mask

        Returns:
            float: the percentage of the footprint in the mask
        """

        mask = self.get_mask(mask_name, date_indicator)

        if mask is None:
            self.logger.warning("[%s] - Cannot intersect with this mask", mask_name)

            return 0

        product_shape = self.load_area_shape_from_footprint(footprint)
        if product_shape is None:
            return 0

        # Use geodesic projection
        geod = pyproj.Geod(ellps="WGS84")

        product_area = abs(geod.geometry_area_perimeter(product_shape)[0])

        mask = self.get_mask(mask_name, date_indicator)
        intersection = mask.intersection(product_shape)
        intersection_area = abs(geod.geometry_area_perimeter(intersection)[0])

        total_coverage = intersection_area / product_area * 100

        return min(total_coverage, 100)

    def intersect_with_masks(self, footprint, masks_name, date_indicator="0"):
        """Intersect a footprint with several masks

        Args:
            footprint (str): Footprint
            masks_name (list(str)): The list of the desired masks

        Returns:
            dict: the coverage of the footprint over the different masks
        """
        result_coverage = {}

        for mask_name in masks_name:
            total_coverage = self.area_coverage(footprint, mask_name, date_indicator)

            self.logger.debug(
                "[%s] - Footprint intersect of %s %%", mask_name, total_coverage
            )

            result_coverage[f"{mask_name}{self.COVERING_AREA_FIELD}"] = total_coverage

        return result_coverage

    def coverage_over_specific_area_s1(
        self, instrument_mode: str, footprint: str, start_date: ZuluDate
    ):
        """Coverage method specific for sentinel 1

        Args:
            instrument_mode (str): The product instrument mode
            footprint (str): The product footprint

        Returns:
            dict: the coverage of the footprint required for compute completeness over specific area
        """

        masks_name = []

        masks_name_for_instrument = CdsDatatakeS1.PRODUCT_TYPES_OVER_SPECIFIC_AREA.get(
            instrument_mode
        )

        if masks_name_for_instrument:
            masks_name.extend(masks_name_for_instrument)

        masks_name.append(CdsDatatakeS1.DEFAULT_MASKS_APPLIED)

        intersection_data = {}
        if masks_name:
            intersection_data = self.intersect_with_masks(
                footprint, masks_name, datetime_to_zulu(start_date)
            )

        return intersection_data
