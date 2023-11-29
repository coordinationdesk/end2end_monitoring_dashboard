"""Update entities after some datatake creation or update"""

import maas_model
from maas_engine.engine.base import EngineReport
from maas_engine.engine.rawdata import DataEngine


class ComputeDatatakeRelatedEngine(DataEngine):
    """Update documents related to datatake creation or update"""

    ENGINE_ID = "COMPUTE_DATATAKE_RELATED"

    def __init__(
        self, args=None, target_model: str = None, send_reports=True, chunk_size=0
    ):
        """constructor

        Args:
            args (namespace, optional): cli options. Defaults to None.
            target_model (str, optional): Model class name. Defaults to None.
            send_reports (bool, optional): flag. Defaults to True.
        """

        super().__init__(args, send_reports=send_reports, chunk_size=chunk_size)

        self.target_model = target_model

    def run(self, routing_key: str, message: maas_model.MAASMessage):
        """Override to forward unique message for completeness compute from datatake"""

        # don't yield any report from database create or update in parent method
        for _ in super().run(routing_key, message):
            pass

        # instead yield a specific message for product, even if any product has been
        # updated, to trigger completeness compute
        if self.target_model.startswith("CdsProduct"):
            yield EngineReport(
                "compute.cds-datatake",
                message.document_ids,
                document_class=message.document_class,
                document_indices=message.document_indices,
                chunk_size=self.chunk_size,
            )

    def action_iterator(self):
        """override

        Yields:
            Iterator[typing.Generator]: bulk actions
        """

        target_class = self.get_model(self.target_model)

        for datatake in self.input_documents:
            search_request = (
                target_class.search()
                .query(datatake.get_related_documents_query())
                .params(ignore=404, version=True, seq_no_primary_term=True)
            )

            for document in search_request.scan():
                initial_dict = document.to_dict()

                if datatake.timeliness:
                    document.timeliness = datatake.timeliness

                document.absolute_orbit = datatake.absolute_orbit

                document.instrument_mode = datatake.instrument_mode

                document.datatake_id = datatake.datatake_id
                if document.mission == "S1":
                    document.hex_datatake_id = (
                        hex(int(datatake.datatake_id, 10)).replace("0x", "").upper()
                    )

                if initial_dict | document.to_dict() != initial_dict:
                    yield document.to_bulk_action()
