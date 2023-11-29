"""Module to operate geo feature """

import logging
import json

import pkgutil

from shapely.wkt import loads
from shapely.geometry import GeometryCollection, shape
from shapely.errors import ShapelyError

from maas_cds.model.datatake_s1 import CdsDatatakeS1


class GeoMaskUtils:
    """Class to manage mask and intersection"""

    OVER_SPECIFIC_AREA_GEOJSON = {
        "OCN": "ne_110m_ocean.geojson",
        "SLC": "EW_SLC_area.geojson",
    }

    COVERING_AREA_FIELD = "_coverage_percentage"

    CACHED_MASK = {}

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

    def load_mask(self, mask_name):
        """Load mask from his identifier (his name)

        Args:
            mask_name (str): identifier of the mask
        """

        mask_filename = self.OVER_SPECIFIC_AREA_GEOJSON.get(mask_name, None)

        if mask_filename is None:
            self.logger.warning(
                "[%s] - Mask not found",
                mask_name,
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

        mask_ocn_shapes = GeometryCollection(
            [
                shape(feature["geometry"]).buffer(0)
                for feature in geojson_data["features"]
            ]
        )

        self.CACHED_MASK[mask_name] = mask_ocn_shapes

    def get_mask(self, mask_name):
        """Get mask from his identifier (his name)

        Args:
            mask_name (str): identifier of the mask

        Returns:
            Polygons: The mask with shapely format (Polygons)
        """

        if mask_name not in self.CACHED_MASK:
            self.load_mask(mask_name)

        else:
            self.logger.debug(
                "[%s] - Mask already loaded",
                mask_name,
            )

        return self.CACHED_MASK.get(mask_name, None)

    def load_area_shape_from_footprint(self, footprint):
        """Load shapely object from footprint

        Args:
            footprint (any): Footprint to convert

        Returns:
            Geometry: Shapely geometry object
        """

        product_shape = None

        # Geojson
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

    def area_coverage(self, footprint, mask_name):
        """Get the coverage of the footprint on the mask identified by the mask_name

        Args:
            footprint (str | dict): The footprint (ex: "Polygon((..., ...))" or GeoJSON)
            mask_name (str):identifier of the mask

        Returns:
            float: the percentage of the footprint in the mask
        """

        mask = self.get_mask(mask_name)

        if mask is None:
            self.logger.warning("[%s] - Cannot intersect with this mask", mask_name)

            return 0

        product_shape = self.load_area_shape_from_footprint(footprint)

        if product_shape is None:
            return 0

        total_intersect = self.get_mask(mask_name).intersection(product_shape).area
        total_coverage = total_intersect / product_shape.area * 100

        # FIXME to pass tests: something is wrong in data provided to intersection
        #
        #         tests/test_geo_mask_utils.py::test_intersect_specific_product
        #   /home/fgirault/Code/MAAS/venvX/lib/python3.11/site-packages/shapely/set_operations.py:133: RuntimeWarning: invalid value encountered in intersection
        #     return lib.intersection(a, b, **kwargs)

        return min(total_coverage, 100)

    def intersect_with_masks(self, footprint, masks_name):
        """Intersect a footprint with several masks

        Args:
            footprint (str): Footprint
            masks_name (list(str)): The list of the desired masks

        Returns:
            dict: the coverage of the footprint over the different masks
        """
        result_coverage = {}

        for mask_name in masks_name:
            total_coverage = self.area_coverage(footprint, mask_name)

            self.logger.debug(
                "[%s] - Footprint intersect of %s %%", mask_name, total_coverage
            )

            result_coverage[f"{mask_name}{self.COVERING_AREA_FIELD}"] = total_coverage

        return result_coverage

    def coverage_over_specific_area_s1(self, instrument_mode: str, footprint: str):
        """Coverage method specific for sentinel 1

        Args:
            instrument_mode (str): The product instrument mode
            footprint (str): The product footprint

        Returns:
            dict: the coverage of the footprint required for compute completeness over specific area
        """

        product_types_to_verify = CdsDatatakeS1.PRODUCT_TYPES_OVER_SPECIFIC_AREA.get(
            instrument_mode
        )

        intersection_data = {}

        if product_types_to_verify:
            intersection_data = self.intersect_with_masks(
                footprint, product_types_to_verify
            )

        return intersection_data
