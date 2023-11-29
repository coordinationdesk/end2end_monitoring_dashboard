"""OData v4 implementation"""

from maas_collector.rawdata.collector.odata.query_strategy import (
    AbstractODataQueryStrategy,
)


class ODataQueryV4Implementation(AbstractODataQueryStrategy):
    """AbstractODataQueryStrategy implementation for V4 version (json)"""

    FILE_NAME_PATTERN = (
        "{interface_name}_"
        "{start_date}_"
        "{end_date}_"
        "{product_per_page}_"
        "P{current_page:06}.json"
    )

    def _deserialize_response(self, response):
        return response.json()

    def _count_item_payload(self, payload):
        return len(payload["value"])
