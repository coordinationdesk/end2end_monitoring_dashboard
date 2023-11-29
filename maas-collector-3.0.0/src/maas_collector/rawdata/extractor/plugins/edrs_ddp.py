"""
A custom extractor to ingest DDP data / DSIB files from EDRS.

This extractor modify the raw data to add a data deduced from the folder name. This
is an issue for reprocessing.

This violate the principle of raw data that shall stay as raw as possible, unmodified.

But as special cases are not special enough to break the rules, this exception is
justified because a clean solutiion is not accessible in term of budget.
"""
import re
from typing import Iterator
from xml.etree import ElementTree as ET

from maas_collector.rawdata.extractor.xml import XMLExtractor


class EdrsDdpExtractor(XMLExtractor):
    """Custum DDP DSIB extractor for EDRS"""

    def extract(
        self, path: str, report_folder: str = "", modify_rawdata=True
    ) -> Iterator[dict]:

        for extract_dict in super().extract(path, report_folder):

            if not re.match(r"^S\d\D_.*$", extract_dict["session_id"]):

                self.logger.debug(
                    "Try to find satellite_id in %s for session %s",
                    report_folder,
                    extract_dict["session_id"],
                )

                satellite_id = ""

                for token in report_folder.split("/"):
                    if re.match(r"^S\d\D$", token):
                        self.logger.debug("Found %s", token)
                        satellite_id = token
                        break

                if satellite_id:
                    extract_dict["session_id"] = "_".join(
                        [satellite_id, extract_dict["session_id"]]
                    )
                    self.logger.debug(
                        "session_id renamed to %s", extract_dict["session_id"]
                    )

                    if modify_rawdata:
                        # saving altered data for reprocessing
                        # it is considered very naughty to modify raw data in this etl, but
                        # there is no alternative ...
                        self.logger.debug("Saving back %s", path)
                        tree = ET.parse(path)
                        element = tree.find("session_id")
                        element.text = extract_dict["session_id"]
                        tree.write(path)

                else:
                    self.logger.error("Satellite not found in path: %s", report_folder)

            yield extract_dict
