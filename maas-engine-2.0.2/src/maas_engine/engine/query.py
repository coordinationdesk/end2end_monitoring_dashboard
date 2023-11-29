"""
Usefull for consolidation missing data
Can be easily overrides to specific behavior
Can be easily use for cron also
"""

from typing import ClassVar, Iterator, Type

from maas_model.message import MAASQueryMessage

from maas_engine.engine.base import EngineReport
from maas_engine.engine.data import DataEngine


class QueryEngine(DataEngine):
    """An engine that request from query string payload
    and emit creation message for targetted entities
    """

    ENGINE_ID = "QUERY_ENGINE"

    PAYLOAD_MODEL: ClassVar[Type[MAASQueryMessage]] = MAASQueryMessage

    def run(
        self, routing_key: str, payload: MAASQueryMessage
    ) -> Iterator[EngineReport]:
        """overide"""

        model_class = self.get_model(payload.document_class)

        # build request
        search_request = (
            model_class.search()
            .query("query_string", query=payload.query_string)
            .params(ignore=404)
        )

        # scan result to simulate creation report data
        for document in search_request.scan():
            self._push_report_data(document, "created")

        # finally yield reports so they can be emitted on the bus
        for report in self._generate_reports():
            if payload.output_routing_key:
                report.action = payload.output_routing_key
            self.reports.append(report)
            yield report

    def action_iterator(self):
        """Empty generator"""
        yield from []
