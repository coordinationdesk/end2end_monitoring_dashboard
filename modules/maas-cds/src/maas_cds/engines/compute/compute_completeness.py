"""Product consolidation"""

from maas_engine.engine.rawdata import DataEngine
from maas_cds.model.datatake import CdsDatatake

from maas_cds.model.enumeration import CompletenessScope

from maas_cds import model


class ComputeCompletenessEngine(DataEngine):
    """Consolidate cds datatake"""

    ENGINE_ID = "COMPUTE_COMPLETENESS"

    def __init__(
        self,
        args=None,
        completeness_tolerance=None,
        send_reports=False,
        generate_missing_periods=False,
        missing_periods_maximal_offset=None,
    ):
        super().__init__(args, send_reports=send_reports)

        CdsDatatake.COMPLETENESS_TOLERANCE = completeness_tolerance

        CdsDatatake.MISSING_PERIODS_MAXIMAL_OFFSET = (
            missing_periods_maximal_offset if generate_missing_periods else None
        )

        self.local_cache_datatake = {}

        self.tuples_to_compute = []

    def load_datatake_doc(self, datatake_id, mission=""):
        """Load a datatake in the local cache

        Args:
            datatake_id (str): The datatake to load
            mission (str, optional): The mission of the datatake. Defaults to "".
        """
        self.logger.debug("[CACHE] - Trying to add in cache: %s", datatake_id)

        target_model_class = f"CdsDatatake{mission.upper()}"

        self.logger.debug(
            "[CACHE] - Search custom mission class %s", target_model_class
        )

        # TODO FIXME MAAS_CDS-1236: single query !!
        datatake_doc = getattr(model, target_model_class, model.CdsDatatake).get_by_id(
            datatake_id
        )

        original_datatake_doc = None

        if datatake_doc is not None:
            original_datatake_doc = datatake_doc.to_dict()

        else:
            self.logger.warning(
                "[CACHE] - Datatake id not found in cds-datatake index "
                "can't load it into local cache: %s",
                datatake_id,
            )

        self.local_cache_datatake[datatake_id] = (
            datatake_doc,
            original_datatake_doc,
        )

    def get_datatake_doc(self, datatake_id):
        """Get a datatake doc from the local cache

        Args:
            datatake_id (str): _description_

        Returns:
            CdsDatatake: The cds-datatake doc associate to the asked datatake_id
        """

        if datatake_id not in self.local_cache_datatake:
            self.load_datatake_doc(datatake_id)

        return self.local_cache_datatake[datatake_id][0]

    def action_iterator(self):
        # get the specific bulk action iterator
        document_class = self.payload.document_class

        if document_class.startswith("CdsProduct"):
            iterator = self.action_iterator_from_product()

        elif document_class.startswith("CdsDatatake"):
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

        for datatake_doc in self.input_documents:
            original_datatake_dict = datatake_doc.to_dict()

            datatake_doc.purge_dynamic_fields()

            datatake_doc.load_data_before_compute()

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
            dict: bulk action with products
        """

        self.logger.info("[ITER][Product] - start")

        for product_document in self.input_documents:
            self.logger.debug(
                "[ITER][Product] - Compute completeness for %s", product_document.name
            )
            original_dict = product_document.to_dict()

            # group compute to avoid duplicate and save computation
            key = product_document.get_compute_key()

            self.logger.debug("[ITER][Product] - Key : %s", key)

            # add the document in parrallel
            if original_dict != product_document.to_dict():
                # convert dao to bulk payload
                product_document_dict = product_document.to_bulk_action()

                yield product_document_dict

            if key:
                datatake_id = product_document.get_datatake_id()
                if datatake_id not in self.local_cache_datatake:
                    self.load_datatake_doc(
                        datatake_id,
                        product_document.mission,
                    )

                datatake_doc = self.get_datatake_doc(datatake_id)
                if datatake_doc:
                    datatake_doc.retrieve_additional_fields_from_product(
                        product_document
                    )

                if key not in self.tuples_to_compute:
                    if datatake_doc is None:
                        self.logger.debug(
                            "[ITER][Product] - Datatake is missing skip this key : %s",
                            key,
                        )
                        continue

                    self.logger.debug(
                        "[ITER][Product] - Added key to compute : %s", key
                    )
                    self.tuples_to_compute.append(key)

                    other_calculations = datatake_doc.impact_other_calculation(key)
                    for other_calculation in other_calculations:
                        if other_calculation in self.tuples_to_compute:
                            continue

                        self.logger.debug(
                            "[ITER][Product] - Added extra key to compute : %s",
                            other_calculation,
                        )

                        self.tuples_to_compute.append(other_calculation)

    def action_iterator_from_product(self):
        """Compute completeness from CdsProduct

        Yields:
            dict: bulk action
        """

        # Update products sometime
        yield from self.load_compute_keys_from_input_documents()

        # compute local completeness
        for (
            datatake_id,
            product_type,
        ) in self.tuples_to_compute:
            datatake_doc = self.get_datatake_doc(datatake_id)

            if datatake_doc is None:
                self.logger.info(
                    "[ITER][Product][%s][%s] - Datatake not find - skipping",
                    datatake_id,
                    product_type,
                )
                continue

            related_products = []

            local_value = datatake_doc.compute_local_value(
                product_type, related_products
            )

            datatake_doc.set_completeness(
                CompletenessScope.LOCAL,
                product_type,
                local_value,
            )

            datatake_doc.compute_missing_production(product_type, related_products)

            datatake_doc.compute_duplicated(product_type, related_products)

            self.logger.info(
                "[ITER][Product][%s] - Compute local value : %s -> %s",
                datatake_id,
                product_type,
                local_value,
            )

        # compute global completeness for all datatake in cache
        for datatake_id, (
            datatake_doc,
            original_datatake_doc_dict,
        ) in self.local_cache_datatake.items():
            if datatake_doc is None:
                self.logger.info(
                    "[ITER][Product][%s] - Datatake not find - skipping", datatake_id
                )
                continue

            self.logger.info("[ITER][Product][%s] - Compute global value", datatake_id)

            datatake_doc.compute_global_completeness()

            new_doc_dict = datatake_doc.to_dict()

            # update was made
            if original_datatake_doc_dict != new_doc_dict:
                # convert dao to bulk payload
                datatake_doc_dict = datatake_doc.to_bulk_action()

                self.logger.info("[ITER][Product][%s] - Pushing update", datatake_id)

                # go feed parallel_bulk
                yield datatake_doc_dict

            else:
                self.logger.debug("[ITER][Product][%s] - Nothing to do", datatake_id)

        self.logger.info("[ITER][Product] - end")
