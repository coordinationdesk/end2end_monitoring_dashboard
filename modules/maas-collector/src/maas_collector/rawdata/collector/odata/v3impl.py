"""
OData v3 implementation

https://www.odata.org/documentation/odata-version-3-0/odata-version-3-0-core-protocol/
"""
import xml.etree.ElementTree as ET

from maas_collector.rawdata.collector.odata.query_strategy import (
    AbstractODataQueryStrategy,
)

from maas_model import datetime_to_zulu


class ODataQueryV3Implementation(AbstractODataQueryStrategy):
    """AbstractODataQueryStrategy implementation for V3 version (xml)"""

    FILE_NAME_PATTERN = (
        "{interface_name}_"
        "{start_date}_"
        "{end_date}_"
        "{product_per_page}_"
        "P{current_page:06}.xml"
    )

    def _format_date(self, date):
        return datetime_to_zulu(date)[:-1]

    def _deserialize_response(self, response):
        return response.content

    def _count_item_payload(self, payload):
        tree = ET.fromstring(payload)

        namespaces = {
            "": "http://www.w3.org/2005/Atom"
            # "m": "http://schemas.microsoft.com/ado/2007/08/dataservices/metadata",
            # "d": "http://schemas.microsoft.com/ado/2007/08/dataservices",
            # "base": "https://apihub.copernicus.eu/apihub/odata/v1/",
        }
        item_array = tree.findall("entry", namespaces)
        return len(item_array)
