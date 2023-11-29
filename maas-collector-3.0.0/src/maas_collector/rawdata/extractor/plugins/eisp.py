"""Extractor class for EISP files """
import datetime
import os
import typing
import xml.etree.ElementTree as ET

from dateutil.parser import parse

from maas_collector.rawdata.extractor.base import BaseExtractor


class EISPExtractor(BaseExtractor):
    """EISP extractor"""

    SCENE_MIN_SIZE = 3.59

    SCENE_MAX_SIZE = 3.61

    DELTA_TIME_GPS_TO_GROUND = 18

    CUT_DATE_STR_DUE_TO_IPF = 24

    def extract(self, path: str, report_folder: str = "") -> typing.Iterator[dict]:
        """override"""
        basepath = os.path.basename(path)

        tree = ET.parse(path)

        start_scene = None

        end_scene = None

        scene_count = 0

        # base attributes
        extract = {
            "satellite": tree.findtext(".//SatelliteID"),
            "downlinkOrbit": tree.findtext(".//Downlink_Orbit"),
            "station": tree.findtext(".//System"),  # station ??
            "reportName": basepath,
        }

        # this returns the first Gaps element and will iterate over its children
        # it assumes all other Gaps nodes have the same content
        isp_status = tree.find(".//ISP_Status")
        if not isp_status:
            self.logger.warning("No ISP_Status found in %s, skipping.", basepath)
            # no ISP Status found, bail out instead of crashing
            return

        gap_list = isp_status.find(".//Gaps")

        if not gap_list:
            self.logger.warning("No Gaps found in %s, skipping.", basepath)
            # no gaps list found, bail out instead of crashing
            return

        # iterate over the Gaps children, i.e. the Gap elements
        for gap_node in gap_list:

            if self.should_stop:
                break

            # presens / postsens time are formatted like 22-MAR-2020 17:34:05.072183
            # hopefully dateutil parse handle without specifying some strptime format
            presens_datetime = self._parse_time(gap_node, "PreSensTime")

            postsens_datetime = self._parse_time(gap_node, "PostSensTime")

            if not presens_datetime or not postsens_datetime:
                continue

            sens_delta = postsens_datetime - presens_datetime

            if start_scene is None:
                start_scene = presens_datetime

            if self.SCENE_MIN_SIZE < sens_delta.total_seconds() < self.SCENE_MAX_SIZE:

                scene_count += 1

                end_scene = postsens_datetime

                if gap_node == gap_list[-1]:
                    yield extract | self.get_start_end_count_dict(
                        start_scene, end_scene, scene_count
                    )
            else:
                if start_scene and end_scene:
                    yield extract | self.get_start_end_count_dict(
                        start_scene, end_scene, scene_count
                    )
                start_scene = None
                end_scene = None
                scene_count = 0

    def _parse_time(self, node, tag):
        text = node.findtext(tag)
        if text:
            return parse(text[: self.CUT_DATE_STR_DUE_TO_IPF] + "z")

    def get_start_end_count_dict(self, start_scene, end_scene, scene_count):
        """
        Create a dictionnary containing gps-corrected start / end sensing datetime
        and granule count
        """
        # maybe enhance leap seconds support : function, configuration file ...
        start_corrected = start_scene - datetime.timedelta(
            seconds=self.DELTA_TIME_GPS_TO_GROUND
        )

        end_corrected = end_scene - datetime.timedelta(
            seconds=self.DELTA_TIME_GPS_TO_GROUND
        )

        granule_count = (scene_count + 1) * 12

        return {
            "dataStripSensingStart": start_corrected,
            "dataStripSensingStop": end_corrected,
            "granuleCount": granule_count,
        }
