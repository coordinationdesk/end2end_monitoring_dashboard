"""Extractor class for SpaceOpsServer OEM files"""

import os
import typing
import xml.etree.ElementTree as ET

from maas_collector.rawdata.extractor.base import BaseExtractor


class OrbitEphemerisMessageExtractor(BaseExtractor):
    """OEM Extractor"""

    def extract(self, path: str, report_folder: str = "") -> typing.Iterator[dict]:
        """override"""

        root = ET.parse(path).getroot()

        basepath = os.path.basename(path)

        creation_date = root.findtext("header/CREATION_DATE")
        originator = root.findtext("header/ORIGINATOR")
        message_id = root.findtext("header/MESSAGE_ID")
        segment_object_name = root.findtext("body/segment/metadata/OBJECT_NAME")
        segment_object_id = root.findtext("body/segment/metadata/OBJECT_ID")
        segment_center_name = root.findtext("body/segment/metadata/CENTER_NAME")
        segment_data_mode = root.findtext("body/segment/metadata/CENTER_NAME")
        segment_ref_frame = root.findtext("body/segment/metadata/REF_FRAME")
        segment_time_system = root.findtext("body/segment/metadata/TIME_SYSTEM")
        segment_start_time = root.findtext("body/segment/metadata/START_TIME")
        segment_stop_time = root.findtext("body/segment/metadata/STOP_TIME")

        metadata = {
            "header_creation_date": creation_date,
            "header_originator": originator,
            "header_message_id": message_id,
            "object_name": segment_object_name,
            "object_id": segment_object_id,
            "center_name": segment_center_name,
            "data_mode": segment_data_mode,
            "ref_frame": segment_ref_frame,
            "time_system": segment_time_system,
            "start_time": segment_start_time,
            "stop_time": segment_stop_time,
            "reportName": basepath,
        }

        state_vectors_list = list(self.generate_statevectors(root))
        covariance_list = list(self.generate_covariances(root))
        yield {
            **metadata,
            "total_statevector": len(state_vectors_list),
            "total_covariance": len(covariance_list),
            "statevectors": state_vectors_list,
            "covariances": covariance_list,
        }

    def generate_statevectors(self, root: ET.Element) -> typing.Iterator[dict]:
        """Generate statevectors incrementally

        Args:
            root (ET.Element): _description_

        Returns:
            typing.Iterator[dict]: _description_

        Yields:
            Iterator[typing.Iterator[dict]]: _description_
        """
        all_statevector_items = root.findall("body/segment/data/stateVector")
        for statevector in all_statevector_items:
            if self.should_stop:
                break
            yield {
                "epoch": statevector.findtext("EPOCH", default="").strip(),
                "x": statevector.findtext("X", default="").strip(),
                "y": statevector.findtext("Y", default="").strip(),
                "z": statevector.findtext("Z", default="").strip(),
                "x_dot": statevector.findtext("X_DOT", default="").strip(),
                "y_dot": statevector.findtext("Y_DOT", default="").strip(),
                "z_dot": statevector.findtext("Z_DOT", default="").strip(),
            }

    def generate_covariances(self, root: ET.Element) -> typing.Iterator[dict]:
        """Generate covariances incrementally

        Args:
            root (ET.Element): _description_

        Returns:
            typing.Iterator[dict]: _description_

        Yields:
            Iterator[typing.Iterator[dict]]: _description_
        """
        all_covariances_items = root.findall("body/segment/data/covarianceMatrix")
        for covariance in all_covariances_items:
            if self.should_stop:
                break
            yield {
                "epoch": covariance.findtext("EPOCH", default="").strip(),
                "ref_frame": covariance.findtext("COV_REF_FRAME", default="").strip(),
                "cx_x": covariance.findtext("CX_X", default="").strip(),
                "cy_x": covariance.findtext("CY_X", default="").strip(),
                "cz_x": covariance.findtext("CZ_X", default="").strip(),
                "cx_dot_x": covariance.findtext("CX_DOT_X", default="").strip(),
                "cy_dot_x": covariance.findtext("CY_DOT_X", default="").strip(),
                "cz_dot_x": covariance.findtext("CZ_DOT_X", default="").strip(),
                "cy_y": covariance.findtext("CY_Y", default="").strip(),
                "cz_y": covariance.findtext("CZ_Y", default="").strip(),
                "cx_dot_y": covariance.findtext("CX_DOT_Y", default="").strip(),
                "cy_dot_y": covariance.findtext("CY_DOT_Y", default="").strip(),
                "cz_dot_y": covariance.findtext("CZ_DOT_Y", default="").strip(),
                "cz_z": covariance.findtext("CZ_Z", default="").strip(),
                "cx_dot_z": covariance.findtext("CX_DOT_Z", default="").strip(),
                "cy_dot_z": covariance.findtext("CY_DOT_Z", default="").strip(),
                "cz_dot_z": covariance.findtext("CZ_DOT_Z", default="").strip(),
                "cx_dot_x_dot": covariance.findtext("CX_DOT_X_DOT", default="").strip(),
                "cy_dot_x_dot": covariance.findtext("CY_DOT_X_DOT", default="").strip(),
                "cz_dot_x_dot": covariance.findtext("CZ_DOT_X_DOT", default="").strip(),
                "cy_dot_y_dot": covariance.findtext("CY_DOT_Y_DOT", default="").strip(),
                "cz_dot_y_dot": covariance.findtext("CZ_DOT_Y_DOT", default="").strip(),
                "cz_dot_z_dot": covariance.findtext("CZ_DOT_Z_DOT", default="").strip(),
            }
