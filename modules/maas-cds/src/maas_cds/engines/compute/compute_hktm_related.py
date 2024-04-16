"""Update hktm completeness after related products are ingested"""

from typing import Callable, List, Dict, Tuple, Generator
from datetime import timedelta

from opensearchpy import MultiSearch

from maas_engine.engine.rawdata import DataEngine

from maas_cds.model import CdsHktmProductionCompleteness, CdsHktmAcquisitionCompleteness

from maas_cds import model


class ComputeHktmRelatedEngine(DataEngine):
    """Update documents related to hktm creation or update"""

    ENGINE_ID = "COMPUTE_HKTM_RELATED"
    SESSION_ID_META = {
        "CdsEdrsAcquisitionPassStatus": {
            "session_id_attr": "link_session_id",
            "hktm_completeness": "edrs_completeness",
            "status": "total_status",
        },
        "CdsCadipAcquisitionPassStatus": {
            "session_id_attr": "session_id",
            "hktm_completeness": "cadip_completeness",
            "status": "global_status",
        },
    }

    def __init__(
        self,
        args=None,
        target_model: str = None,
        send_reports=False,
        tolerance_value: int = 30,
        chunk_size=0,
        dd_attrs=None,
    ):
        """constructor

        Args:
            args (namespace, optional): cli options. Defaults to None.
            target_model (str, optional): Model class name. Defaults to None.
            send_reports (bool, optional): flag. Defaults to False.
        """
        super().__init__(args, send_reports=send_reports, chunk_size=chunk_size)

        self.target_model: (
            CdsHktmAcquisitionCompleteness | CdsHktmProductionCompleteness
        ) = target_model

        self.tolerance_value = tolerance_value

        self.dd_attrs = dd_attrs or {}

    def update_hktm_factory(self) -> Callable:
        """
        Factory that returns the hktm update method for each
        valid target model

        Args:
            document : target document that need to be updated

        Returns:
            callable: update hktm method
        """
        if self.target_model == "CdsHktmProductionCompleteness":
            return self.update_hktm_production
        elif self.target_model == "CdsHktmAcquisitionCompleteness":
            return self.update_hktm_acquisition
        else:
            raise ValueError(f"Unexpected target model : {self.target_model}")

    def search_hktm_factory(self) -> Callable:
        """
        Factory that returns the hktm search method for each
        valid target model

        Args:
            document : target document that need to be updated

        Returns:
            callable: search hktm method
        """
        if self.target_model == "CdsHktmProductionCompleteness":
            return self.search_hktm_production
        elif self.target_model == "CdsHktmAcquisitionCompleteness":
            return self.search_hktm_acquisition
        else:
            raise ValueError(f"Unexpected target model : {self.target_model}")

    def update_hktm_production(
        self, document: CdsHktmProductionCompleteness
    ) -> CdsHktmProductionCompleteness:
        """Sets the completeness attribute to 1

        Args:
            document (CdsHktmProductionCompleteness): input document

        Returns:
            CdsHktmProductionCompleteness: updated document
        """
        setattr(document, "completeness", 1)

        return document

    def update_hktm_acquisition(
        self, document: CdsHktmAcquisitionCompleteness
    ) -> CdsHktmAcquisitionCompleteness:
        """Sets the completeness attribute to 1

        Args:
            document (CdsHktmAcquisitionCompleteness): input document

        Returns:
            CdsHktmAcquisitionCompleteness: updated document
        """
        setattr(
            document,
            self.SESSION_ID_META[self.input_model.__name__]["hktm_completeness"],
            1,
        )

        return document

    def search_hktm_production(self, documents) -> Tuple[MultiSearch, List[Dict]]:
        """
        Search for HKTM information within a tolerance window.

        This method performs an HKTM search based on a list of input documents and applies
        a tolerance window to match effective downlink start dates.

        Args:
        - documents: A list of raw documents for HKTM search.

        Returns:
        - msearch: An Elasticsearch MultiSearch object containing search queries.
        - valid_input_documents: A list of valid input documents used for the search.
        """
        msearch = MultiSearch()

        tolerance_value = timedelta(minutes=self.tolerance_value)

        valid_input_documents = []
        for raw_document in documents:
            sensing_start_date = getattr(raw_document, "sensing_start_date")

            msearch = msearch.add(
                CdsHktmProductionCompleteness.search()
                .filter(
                    "range",
                    effective_downlink_start={
                        "lte": sensing_start_date + tolerance_value
                    },
                )
                .filter(
                    "range",
                    effective_downlink_start={
                        "gte": sensing_start_date - tolerance_value
                    },
                )
            )

            valid_input_documents.append(raw_document)

        return msearch, valid_input_documents

    def search_hktm_acquisition(self, documents) -> Tuple[MultiSearch, List[Dict]]:
        """
        Search for HKTM information within a tolerance window.

        This method performs an HKTM search based on a list of input documents and applies
        a tolerance window to match effective downlink start dates.

        Args:
        - documents: A list of raw documents for HKTM search.

        Returns:
        - msearch: An Elasticsearch MultiSearch object containing search queries.
        - valid_input_documents: A list of valid input documents used for the search.
        """
        msearch = MultiSearch()

        valid_input_documents = []
        session_id_meta = self.SESSION_ID_META[self.input_model.__name__]

        for raw_document in documents:
            if raw_document[session_id_meta["status"]] == "OK":
                # Construct the session_id based on document class and metadata.
                session_id = getattr(raw_document, session_id_meta["session_id_attr"])

                msearch = msearch.add(
                    CdsHktmAcquisitionCompleteness.search().filter(
                        "term", session_id=session_id
                    )
                )

                valid_input_documents.append(raw_document)

        return msearch, valid_input_documents

    def action_iterator(self) -> Generator:
        """overridee

        Iter throught input documents and find products who are inside
        Then add informations on these products

        Yields:
            Iterator[Generator]: bulk actions
        """
        search_method = self.search_hktm_factory()
        msearch, valid_input_documents = search_method(self.input_documents)

        if valid_input_documents:
            # contained identifier to container instance as MultiSearch does not support
            # metadata like params(version=True, seq_no_primary_term=True)
            result_map = {}

            for raw_document, response in zip(valid_input_documents, msearch.execute()):
                if not response:
                    self.logger.warning("No hktm found %s", raw_document)
                    continue

                for document in response:
                    # store link between content and container
                    result_map[document.meta.id] = raw_document

            # retrieve again targeted documents as msearch does not support versionning :'(
            for document in getattr(model, self.target_model).mget_by_ids(
                list(result_map.keys())
            ):
                initial_dict = document.to_dict()

                update_method = self.update_hktm_factory()
                document = update_method(document)

                if initial_dict | document.to_dict() != initial_dict:
                    self.logger.debug(
                        "[%s] - Update : %s",
                        document.meta.id,
                        document.reportName,
                    )
                    yield document.to_bulk_action()

                else:
                    self.logger.debug(
                        "[%s] - Nothing to do : %s",
                        document.meta.id,
                        document.reportName,
                    )
        else:
            self.logger.debug(
                "[SKIPPING] - Nothing to do : no acquisition have an OK status",
            )
