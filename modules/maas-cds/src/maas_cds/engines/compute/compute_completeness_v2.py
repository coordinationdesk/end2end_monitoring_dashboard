"""Publication consolidation"""

from maas_cds.engines.compute.compute_completeness import ComputeCompletenessEngine
from maas_engine.engine.rawdata import DataEngine
from maas_cds.model.cds_completeness import CdsCompleteness

from maas_cds.model.enumeration import CompletenessScope

from maas_cds import model


class ComputeCompletenessEngineV2(ComputeCompletenessEngine):
    """Consolidate cds datatake"""

    ENGINE_ID = "COMPUTE_COMPLETENESS_V2"

    def load_datatake_doc(self, datatake_id, satellite_unit, prip_name):
        """Load a datatake in the local cache

        Args:
            datatake_id (str): The datatake to load
            mission (str, optional): The mission of the datatake. Defaults to "".
        """

        target_model_class = f"CdsCompleteness{satellite_unit[:2].upper()}"

        # Fake doc to get index
        # Maybe externalise this
        target_index = CdsCompleteness(
            satellite_unit=satellite_unit, prip_name=prip_name
        ).partition_index_name

        self.logger.debug(
            "[CACHE] - Trying to add in cache: %s from %s as %s",
            datatake_id,
            target_index,
            target_model_class,
        )

        # TODO FIXME MAAS_CDS-1236: single query !!
        datatake_doc = getattr(
            model, target_model_class, model.CdsCompleteness
        ).get_by_id(datatake_id, [target_index])

        original_datatake_doc = None

        if datatake_doc is not None:
            original_datatake_doc = datatake_doc.to_dict()

        else:
            self.logger.warning(
                "[CACHE] - Datatake id not found in cds-datatake index "
                "can't load it into local cache: %s",
                datatake_id,
            )
        key = f"{datatake_id}-{satellite_unit}-{prip_name}"

        self.local_cache_datatake[key] = (
            datatake_doc,
            original_datatake_doc,
        )

    def get_datatake_doc(self, datatake_id, satellite_unit, prip_name):
        """Get a datatake doc from the local cache

        Args:
            datatake_id (str): _description_

        Returns:
            CdsDatatake: The cds-datatake doc associate to the asked datatake_id
        """

        if datatake_id not in self.local_cache_datatake:
            self.load_datatake_doc(datatake_id, satellite_unit, prip_name)
        key = f"{datatake_id}-{satellite_unit}-{prip_name}"
        return self.local_cache_datatake[key][0]

    def action_iterator(self):
        # get the specific bulk action iterator
        document_class = self.payload.document_class

        if document_class.startswith("CdsPublication"):
            iterator = self.action_iterator_from_publication()
        elif document_class.startswith("CdsCompleteness"):
            iterator = self.action_iterator_from_datatake()
        else:
            raise TypeError(
                f"Unexpected input document class for completeness: {document_class}"
            )

        # bulk feed
        for action in iterator:
            yield action

    def action_iterator_from_datatake(self):
        """Compute completeness from CdsDataTake

        Yields:
            dict: bulk action
        """

        self.logger.info("[ITER][Datatake] - start")

        # TODO add a cache to load completeness config

        for datatake_doc in self.input_documents:

            original_datatake_dict = datatake_doc.to_dict()

            # reset all field not mapped
            datatake_doc.purge_dynamic_fields()

            # TODO for s2
            datatake_doc.load_data_before_compute()

            self.logger.error("INSTANCE IS %s", type(datatake_doc))

            datatake_doc.compute_all_local_completeness()

            datatake_doc.compute_global_completeness()

            if original_datatake_dict != datatake_doc.to_dict():
                self.logger.info("[ITER][Datatake] - Pushing update %s", datatake_doc)

                yield datatake_doc.to_bulk_action()

            else:
                self.logger.info(
                    "[ITER][Datatake] - Nothing to do for %s", datatake_doc
                )

        self.logger.info("[ITER][Datatake] - end")

    def load_compute_keys_from_input_documents(self):
        """Load unique compute_key from input documents

        Yields:
            dict: bulk action with publications
        """

        self.logger.info("[ITER][Publication] - start")
        # input document can be CdsPublication or CdsPublication

        for publication_document in self.input_documents:
            self.logger.debug(
                "[ITER][Publication] - Compute completeness for %s",
                publication_document.name,
            )
            original_dict = publication_document.to_dict()

            # group compute to avoid duplicate and save computation
            key = publication_document.get_compute_key()

            self.logger.debug("[ITER][Publication] - Key : %s", key)

            # add the document in parrallel
            if original_dict != publication_document.to_dict():
                # convert dao to bulk payload
                # TODO for s2 mainly
                publication_document_dict = publication_document.to_bulk_action()

                yield publication_document_dict

            if key:
                # TODO refactor this in a signle indentifier
                datatake_id = publication_document.get_datatake_id()
                if datatake_id not in self.local_cache_datatake:
                    self.load_datatake_doc(
                        datatake_id,
                        publication_document.satellite_unit,
                        publication_document.service_id,
                    )

                datatake_doc = self.get_datatake_doc(
                    datatake_id,
                    publication_document.satellite_unit,
                    publication_document.service_id,
                )
                if datatake_doc:
                    # TODO for s2
                    # initially for retrieve_additional_fields_from_product
                    datatake_doc.retrieve_additional_fields_from_publication(
                        publication_document
                    )

                if key not in self.tuples_to_compute:
                    if datatake_doc is None:
                        self.logger.debug(
                            "[ITER][Publication] - Datatake is missing skip this key : %s",
                            key,
                        )
                        continue

                    self.logger.debug(
                        "[ITER][Publication] - Added key to compute : %s", key
                    )
                    self.tuples_to_compute.append(key)

                    other_calculations = datatake_doc.impact_other_calculation(key)
                    for other_calculation in other_calculations:
                        if other_calculation in self.tuples_to_compute:
                            continue

                        self.logger.debug(
                            "[ITER][Publication] - Added extra key to compute : %s",
                            other_calculation,
                        )

                        self.tuples_to_compute.append(other_calculation)

    def action_iterator_from_publication(self):
        """Compute completeness from CdsPublication

        Yields:
            dict: bulk action
        """

        # Update publications sometime s2 xctx
        yield from self.load_compute_keys_from_input_documents()

        # compute local completeness
        for datatake_id, publication_type, prip_name in self.tuples_to_compute:
            # There is a way to not find a datatake before ?
            datatake_doc = self.get_datatake_doc(
                datatake_id, datatake_id[:3], prip_name
            )

            if datatake_doc is None:
                self.logger.info(
                    "[ITER][Publication][%s][%s] - Datatake not find - skipping",
                    datatake_id,
                    publication_type,
                )
                continue

            related_publications = []

            local_value = datatake_doc.compute_local_value(
                publication_type, related_publications
            )

            datatake_doc.set_completeness(
                CompletenessScope.LOCAL,
                publication_type,
                local_value,
            )

            datatake_doc.compute_missing_production(
                publication_type, related_publications
            )

            datatake_doc.compute_duplicated(publication_type, related_publications)

            self.logger.info(
                "[ITER][Publication][%s] - Compute local value : %s -> %s",
                datatake_id,
                publication_type,
                local_value,
            )

        # compute global completeness for all datatake in cache
        for datatake_id, (
            datatake_doc,
            original_datatake_doc_dict,
        ) in self.local_cache_datatake.items():
            if datatake_doc is None:
                self.logger.info(
                    "[ITER][Publication][%s] - Datatake not find - skipping",
                    datatake_id,
                )
                continue

            self.logger.info(
                "[ITER][Publication][%s] - Compute global value", datatake_id
            )

            datatake_doc.compute_global_completeness()

            new_doc_dict = datatake_doc.to_dict()

            # update was made
            if original_datatake_doc_dict != new_doc_dict:
                # convert dao to bulk payload
                datatake_doc_dict = datatake_doc.to_bulk_action()

                self.logger.info(
                    "[ITER][Publication][%s] - Pushing update", datatake_id
                )

                # go feed parallel_bulk
                yield datatake_doc_dict

            else:
                self.logger.debug(
                    "[ITER][Publication][%s] - Nothing to do", datatake_id
                )

        self.logger.info("[ITER][Publication] - end")
