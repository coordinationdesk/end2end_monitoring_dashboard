"""Product consolidation"""

from datetime import timedelta

from maas_engine.engine.rawdata import DataEngine

from maas_cds.engines.reports.anomaly_impact import AnomalyImpactMixinEngine

from maas_cds.model.cds_s5_completeness import CdsS5Completeness


class ComputeS5CompletenessEngine(AnomalyImpactMixinEngine, DataEngine):
    """Consolidate cds S5 completeness"""

    ENGINE_ID = "COMPUTE_S5_COMPLETENESS"
    ORBIT_DURATION_IN_MINUTES = 101

    def __init__(self, args=None, completeness_tolerance=None):

        super().__init__(args)

        CdsS5Completeness.COMPLETENESS_TOLERANCE = completeness_tolerance

        self.local_cache_completeness = {}

    def load_completeness_doc(self, compute_key, product_document):
        """Load a completeness document in the local cache

        Args:
            compute_key: The completenes compute key (ie datatake#product_type#timeliness)
            default_args_if_not_exists (dict, optional): If the completeness doesn't exist this dict
                allow us to create it with default values. Defaults to None.
        """
        self.logger.debug("[CACHE] - Trying to add in cache: %s", compute_key)

        target_model_class = f"Cds{product_document.mission.upper()}Completeness"

        self.logger.debug(
            "[CACHE] - Search custom mission class %s", target_model_class
        )

        specific_model_class = DataEngine.get_model(target_model_class)

        if specific_model_class is None:
            raise KeyError(f"The target model doesn't exist: {specific_model_class}")

        completeness_doc = specific_model_class.get_by_id(compute_key)

        #  creation
        if completeness_doc is None:
            self.logger.debug(
                "[CACHE] - key not found in cds-s5-completeness index, create a new one %s",
                compute_key,
            )

            # create the specific completeness for this type (with the products infos)
            self.create_completeness_doc(
                compute_key, product_document, specific_model_class
            )
        else:
            original_completeness_doc = completeness_doc.to_dict()
            self.local_cache_completeness[compute_key] = (
                completeness_doc,
                original_completeness_doc,
            )

        # create default completeness for previous and next orbit if they are not present
        absolute_orbit = product_document.absolute_orbit
        if not absolute_orbit:
            self.logger.warning(
                "Skipping check of orbit gaps of invalid orbit '%s'", absolute_orbit
            )
            return

        for delta in (-1, 1):
            neighbor_orbit = int(absolute_orbit) + delta
            neighbor_compute_key = f"{product_document.satellite_unit}-{neighbor_orbit:05}-{product_document.product_type}"
            self.logger.debug(
                "Checking orbit gaps of %s -> %s",
                compute_key,
                neighbor_compute_key,
            )
            if specific_model_class.get_by_id(neighbor_compute_key) is None:
                product_document.absolute_orbit = f"{neighbor_orbit:05}"
                product_document.datatake_id = (
                    f"{product_document.satellite_unit}-{neighbor_orbit:05}"
                )
                self.create_completeness_doc(
                    neighbor_compute_key,
                    product_document,
                    specific_model_class,
                    delta * timedelta(minutes=self.ORBIT_DURATION_IN_MINUTES),
                )

    def create_completeness_doc(
        self,
        compute_key: str,
        product_document,
        model_class,
        time_offset: timedelta = None,
    ):
        """Create a completeness doc

        Args:
            compute_key (str): _description_
            product_document: the origin document
            model_class: the DAO class
            time_offset(timedelta): shift observation times
        Returns:
            Nothing
        """

        completeness_doc = model_class(**product_document.data_for_completeness())
        completeness_doc.meta.id = compute_key
        self.local_cache_completeness[compute_key] = (
            completeness_doc,
            None,
        )
        # init all others completeness for this datatake_id(s5 orbit)
        # (if the specific completeness for the compute key doesnt exist
        # it means that its the first time we encouter this datatake_id)
        self.logger.debug(
            "[CACHE] - key : %s not found in cds-s5-completeness index, create all completeness for %s",
            compute_key,
            product_document.datatake_id,
        )

        datas_for_completnesses = completeness_doc.init_completenesses()

        # create all completeness
        for key, data_for_completeness in datas_for_completnesses.items():
            if key != compute_key:
                # create all others completeness and store it in the local cache
                self.logger.debug("Creating completeness: %s", key)
                completeness_doc = model_class(**data_for_completeness)
                completeness_doc.meta.id = data_for_completeness["key"]
                if time_offset:
                    completeness_doc.observation_time_start += time_offset
                    completeness_doc.observation_time_stop += time_offset
                self.local_cache_completeness[key] = (
                    completeness_doc,
                    None,
                )

    def get_completeness_doc(self, compute_key):
        """Get a completenes doc from the local cache

        Args:
            compute_key (str): _description_

        Returns:
            Cds*completeness: The cds*completeness doc associate to the asked compute_key
        """
        return self.local_cache_completeness[compute_key][0]

    def action_iterator(self):
        """Compute completeness from CdsProduct

        Yields:
            dict: bulk action
        """

        self.logger.info("[ITER][Product] - start")

        # TODO FIXME MAAS_CDS-1236: make a single query to find all the datatake

        for product_document in self.input_documents:

            self.logger.debug(
                "[ITER][Product] - Compute completeness for %s", product_document.name
            )

            # group compute to avoid duplicate and save computation
            compute_key = product_document.get_compute_key()

            self.logger.debug("[ITER][Product] - Compute Key : %s", compute_key)

            if compute_key and compute_key not in self.local_cache_completeness:
                self.load_completeness_doc(compute_key, product_document)

                self.logger.debug(
                    "[ITER][Product] - Added key to compute : %s", compute_key
                )

        self.logger.info("[ITER][Product] - end")

        self._populate_ticket_cache()

        self.logger.info("[ITER][Completeness] - start")

        # compute completeness
        for compute_key, (
            completeness_doc,
            original_completeness_doc_dict,
        ) in self.local_cache_completeness.items():

            sensing_value, slice_value, observation_period = completeness_doc.compute()

            completeness_doc.set_completeness(
                sensing_value,
                slice_value,
                observation_period,
            )

            self.logger.info(
                "[ITER][Completeness][%s] - Computed sensing value : %s slice value : %s for period : %s",
                compute_key,
                sensing_value,
                slice_value,
                observation_period,
            )

            # link cams tickets
            if completeness_doc.datatake_id in self._cams_tickets_dict:
                self._apply_anomalies(completeness_doc, key="datatake_id")

            new_doc_dict = completeness_doc.to_dict()

            # update was made
            if original_completeness_doc_dict != new_doc_dict:

                # convert dao to bulk payload
                completeness_doc_dict = completeness_doc.to_bulk_action()

                self.logger.info(
                    "[ITER][Completeness][%s] - Pushing update", compute_key
                )

                # go feed parallel_bulk
                yield completeness_doc_dict

            else:
                self.logger.debug(
                    "[ITER][Completeness][%s] - Nothing to do", compute_key
                )

        self.logger.info("[ITER][Completeness] - end")

    def _populate_ticket_cache(self):

        self._cams_tickets_dict = {}

        # generate pseudo datatake list
        datatake_ids_set = set()

        for compute_key, (
            completeness_doc,
            original_completeness_doc_dict,
        ) in self.local_cache_completeness.items():
            datatake_ids_set.add(completeness_doc.datatake_id)

        self._populate_by_Datatake(list(datatake_ids_set))
