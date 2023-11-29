"""Extractor class for Sat unavailability files """
import os
import typing
import xml.etree.ElementTree as ET

from maas_collector.rawdata.extractor.base import BaseExtractor


class SatUnavailabilityExtractor(BaseExtractor):
    """SATU extractor"""

    def extract(self, path: str, report_folder: str = "") -> typing.Iterator[dict]:
        """override"""
        tree = ET.parse(path)

        root = tree.getroot()

        basepath = os.path.basename(path)

        file_name = root.findtext("Earth_Explorer_Header/Fixed_Header/File_Name")
        mission = root.findtext("Earth_Explorer_Header/Fixed_Header/Mission")
        unavailability_reference = root.findtext("Data_Block/Unavailability_Reference")
        unavailability_type = root.findtext("Data_Block/Unavailability_Type")

        for product in root.findall("Data_Block/List_Of_Subsystem_Unavailabilities/"):

            if self.should_stop:
                break

            # findtext remost in almost case "" if the case are empty
            # it's why default is not None
            start_orbit = product.findtext("StartOrbit", default="").strip()
            if not start_orbit.isdigit():
                self.logger.info("StartOrbit is not an number: '%s'", start_orbit)
                start_orbit = None
            else:
                # shift 0 and allow to check if it is really a number
                start_orbit = str(int(start_orbit))

            end_orbit = product.findtext("EndOrbit", default="").strip()
            if not end_orbit.isdigit():
                self.logger.info("EndOrbit is not an number: '%s'", end_orbit)
                end_orbit = None
            else:
                end_orbit = str(int(end_orbit))

            start_anx_offset = product.findtext("StartAnxOffset", default="").strip()
            if not start_anx_offset.isdigit():
                self.logger.info(
                    "StartAnxOffset is not an number: '%s'", start_anx_offset
                )
                start_anx_offset = None

            end_anx_offset = product.findtext("EndAnxOffset", default="").strip()
            if not end_anx_offset.isdigit():
                self.logger.info("EndAnxOffset is not an number: '%s'", end_anx_offset)
                end_anx_offset = None

            yield {
                "file_name": file_name,
                "mission": mission,
                "unavailability_reference": unavailability_reference,
                "unavailability_type": unavailability_type,
                "subsystem": product.findtext("Subsystem"),
                "start_time": product.findtext("StartTime"),
                "start_orbit": start_orbit,
                "start_anx_offset": start_anx_offset,
                "end_time": product.findtext("EndTime"),
                "end_orbit": end_orbit,
                "end_anx_offset": end_anx_offset,
                "type": product.findtext("Type"),
                "comment": product.findtext("Comment"),
                "interface_name": "Satellite-Unavailability",
                "production_service_type": "AUXIP",
                "production_service_name": "Exprivia",
                "reportName": basepath,
            }
