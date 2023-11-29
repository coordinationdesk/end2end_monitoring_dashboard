"""

Engine and consolidation decorator to update cams issues impact in consolidation
"""

from opensearchpy import MultiSearch


from maas_cds.model import CdsHktmAcquisitionCompleteness


class HktmImpactMixinEngine:
    """

    Engine Mixin to handle updates of hktm accquisition completeness
    with new EDRS or CADIP acquisition.


    """

    SESSION_ID_META = {
        "ApsEdrs": {
            "session_id_attr": "link_session_id",
            "hktm_session_id_prefix": "L",
            "hktm_completeness": "edrs_completeness",
            "status": "total_status",
        },
        "ApsSession": {
            "session_id_attr": "session_id",
            "hktm_session_id_prefix": "DCS_0X_",
            "hktm_completeness": "cadip_completeness",
            "status": "global_status",
        },
    }

    def update_hktm(self, document_class, consolidated_documents):
        """
        Update the HKTM completeness when a linked CADIP or EDRS pass is consolidated.

        Args:
            document_class (str): The class of the document (e.g., 'ApsSession' or 'ApsEdrs').

        Yields:
            dict: A dictionary representing the updated HKTM completeness.

        Note:
            - HKTM acquisition can be linked to a CADIP or EDRS acquisition.
            - Each acquisition type has a different name and format for its session_id.
        """

        # Ensure that the provided `document_class` is recognized.
        if document_class not in self.SESSION_ID_META:
            raise ValueError(f"Unknown document class: {document_class}")

        session_id_meta = self.SESSION_ID_META[document_class]

        # Create a list to store valid documents and a dictionary to map documents to HKTM results.
        valid_documents = []
        result_map = {}

        msearch = MultiSearch()

        for doc in consolidated_documents:
            if doc[session_id_meta["status"]] == "OK":
                # Construct the session_id based on document class and metadata.
                session_id = getattr(doc, session_id_meta["session_id_attr"])

                if document_class == "ApsSession":
                    session_id = session_id_meta["hktm_session_id_prefix"] + session_id

                msearch = msearch.add(
                    CdsHktmAcquisitionCompleteness.search().filter(
                        "term", session_id=session_id
                    )
                )

                valid_documents.append(doc)

        if len(msearch._searches) == 0:
            # Every document has a status different than OK
            self.logger.debug(
                "SKIPPING HKTM Update : msearch is empty, no acquisition documents with 'OK' status"
            )
            return

        for raw_document, response in zip(valid_documents, msearch.execute()):
            matched_hktm = list(response)

            if len(matched_hktm) == 0:
                self.logger.debug("%s : No associated HKTM MP found yet", raw_document)
                continue

            for document in response:
                # store link between content and container
                result_map[document.meta.id] = raw_document

        # retrieve again targeted documents as msearch does not support versionning :'(
        for hktm in CdsHktmAcquisitionCompleteness.mget_by_ids(list(result_map.keys())):
            self.logger.debug("Found HKTM: %s", hktm)

            initial_dict = hktm.to_dict()
            # Update the HKTM completeness to 100%
            setattr(hktm, session_id_meta["hktm_completeness"], 1)

            if initial_dict | hktm.to_dict() != initial_dict:
                self.logger.debug(
                    "[%s] - Update : %s",
                    hktm.meta.id,
                    hktm.reportName,
                )
                yield hktm.to_bulk_action()

            else:
                self.logger.debug(
                    "[%s] - Nothing to do : %s",
                    hktm.meta.id,
                    hktm.reportName,
                )
