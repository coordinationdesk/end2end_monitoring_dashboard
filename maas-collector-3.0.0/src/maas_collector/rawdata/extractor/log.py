"""LogExtractor implementation"""
import os
import re
import typing

from .base import BaseExtractor


class LogExtractor(BaseExtractor):
    """read log text file line per line and extract data using regular expression from one line"""

    def __init__(self, pattern, converter_map: dict = None):
        super().__init__(converter_map=converter_map)
        self.regex = re.compile(pattern)

    def extract(self, path, report_folder: str = "") -> typing.Iterator[dict]:
        """override"""

        basepath = os.path.basename(path)

        with open(path, encoding="UTF-8") as input_fd:

            for line in input_fd:

                if self.should_stop:
                    break

                match = self.regex.match(line)

                if match:
                    extract_dict = self.convert_data_extract_values(match.groupdict())

                    if not "reportName" in extract_dict:
                        extract_dict["reportName"] = basepath

                    yield extract_dict
