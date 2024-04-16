"""Extractor class for ESIP files """
import os
import typing
import xml.etree.ElementTree as ET

from maas_collector.rawdata.extractor.base import BaseExtractor


class ProductExtractor(BaseExtractor):
    """
    Specific extractor for Product file because of the limitation of the implementation of xpath in
    elementtree: ancestor cannot be selected from a child node. This made a pythonista cry :'|
    """

    def extract(self, path: str, report_folder: str = "") -> typing.Iterator[dict]:
        """override"""
        tree = ET.parse(path)

        root = tree.getroot()

        basepath = os.path.basename(path)

        for product in root.findall("./Products/Product"):

            for cadu_content in product.findall("./CADU_Contents/CADU_Content"):

                if self.should_stop:
                    break

                yield {
                    "productName": product.attrib["name"],
                    "CADUContent": cadu_content.text,
                    "reportName": basepath,
                }
