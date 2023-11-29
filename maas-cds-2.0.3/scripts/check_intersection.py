#!/usr/bin/env python3

from datetime import datetime
from maas_cds.lib.geo_mask_utils import GeoMaskUtils

# footprint_to_intersect = "geography'SRID=4326;Polygon((95.597549 15.290585,95.986031 17.170599,93.623131 17.606874,93.258141 15.731363,95.597549 15.290585))'"
# footprint_to_intersect = footprint_to_intersect.split(";")[1]
## {'OCN_coverage_percentage': 51.30952831502296, 'SLC_coverage_percentage': 0.0}
## No intersect
# footprint_to_intersect = {
#     "type": "Polygon",
#     "coordinates": [
#         [
#             [-107.411835, 37.878963],
#             [-104.561249, 38.274658],
#             [-104.896561, 39.900146],
#             [-107.815651, 39.505627],
#             [-107.411835, 37.878963],
#         ]
#     ],
# }
## Yes intersect
footprint_to_intersect = {
    "type": "Polygon",
    "coordinates": [
        [
            [95.597549, 15.290585],
            [95.986031, 17.170599],
            [93.623131, 17.606874],
            [93.258141, 15.731363],
            [95.597549, 15.290585],
        ]
    ],
}
print("= START")
start = datetime.now()

ocn_intersect = GeoMaskUtils().intersect_with_masks(
    footprint=footprint_to_intersect, masks_name=["OCN", "SLC"]
)

print(ocn_intersect)

end = datetime.now()
print(f"= END in {end - start}")
