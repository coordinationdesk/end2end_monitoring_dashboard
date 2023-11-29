"""Product consolidation"""

from datetime import timedelta

from maas_engine.engine.rawdata import DataEngine

from maas_cds.engines.reports.anomaly_impact import AnomalyImpactMixinEngine

from maas_cds.model.cds_s3_completeness import CdsS3Completeness


class ComputeS3CompletenessEngine(AnomalyImpactMixinEngine, DataEngine):
    """Consolidate cds S3 completeness"""

    ENGINE_ID = "COMPUTE_S3_COMPLETENESS"
    ORBIT_DURATION_IN_MINUTES = 101

    def __init__(self, args=None, completeness_tolerance=None):

        super().__init__(args)

        CdsS3Completeness.COMPLETENESS_TOLERANCE = completeness_tolerance

        self.local_cache_completeness = {}

    def load_completeness_doc(self, compute_key, product_document):
        """Load a completeness document in the local cache.
        If the completeness doesn't exist, create all the default ones.

        Args:
            compute_key: The completeness compute key (ie datatake#product_type#timeliness)
            product_document: the origin document
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

        original_completeness_doc = None

        #  creation
        if completeness_doc is None:
            self.logger.debug(
                "[CACHE] - key not found in cds-s3-completeness index, create a new one %s",
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
        if (
            product_document.sensing_end_date - product_document.sensing_start_date
        ).total_seconds() >= 60:
            for delta in (-1, 1):
                datatake_id, product_type, timeliness = compute_key.split("#")
                neighbor_datatake_id = self.change_orbit(datatake_id, delta)
                neighbor_compute_key = (
                    f"{neighbor_datatake_id}#{product_type}#{timeliness}"
                )
                self.logger.debug(
                    "Checking orbit gaps of %s -> %s",
                    compute_key,
                    neighbor_compute_key,
                )
                if specific_model_class.get_by_id(neighbor_compute_key) is None:
                    product_document.datatake_id = neighbor_datatake_id
                    self.create_completeness_doc(
                        neighbor_compute_key,
                        product_document,
                        specific_model_class,
                        delta * timedelta(minutes=self.ORBIT_DURATION_IN_MINUTES),
                    )

    @staticmethod
    def change_orbit(datatake_id, delta):
        """Returns the orbit before/after the given datatake-id

        Args:
            datatake_id (str): the datatake-id
            delta (int): The relative number of orbits to change
        """
        satellite, cycle_count, relative_orbit = datatake_id.split("-")
        cycle_count = int(cycle_count)
        relative_orbit = int(relative_orbit)
        relative_orbit += delta

        if relative_orbit < 1:
            relative_orbit = 385
            cycle_count -= 1

        if relative_orbit > 385:
            relative_orbit = 1
            cycle_count += 1

        return f"{satellite}-{cycle_count:03}-{relative_orbit:03}"

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
        self.logger.debug(
            "[CACHE] - key not found in cds-s3-completeness index, create a new one %s",
            compute_key,
        )
        # create the specific completeness for this type (with the products infos)
        completeness_doc = model_class(**product_document.data_for_completeness())
        completeness_doc.meta.id = compute_key

        self.local_cache_completeness[compute_key] = (
            completeness_doc,
            None,
        )
        # init all others completeness for this datatake_id(s3 orbit)
        # (if the specific completeness for the compute key doesnt exist
        # it means that its the first time we encouter this datatake_id)
        self.logger.debug(
            "[CACHE] - key : %s not found in cds-s3-completeness index, "
            "create all completeness for %s",
            compute_key,
            product_document.datatake_id,
        )

        datas_for_completnesses = completeness_doc.init_completenesses()

        self.logger.debug("DATA4COMPLETENESS %s", datas_for_completnesses)

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

        for product_document in self.input_documents:

            self.logger.debug(
                "[ITER][Product] - Compute completeness for %s", product_document.name
            )

            # group compute to avoid duplicate and save computation
            compute_key = product_document.get_compute_key()

            self.logger.debug("[ITER][Product] - Compute Key : %s", compute_key)

            # TODO FIXME MAAS_CDS-1236: make a single query to find all the datatakes

            if compute_key and compute_key not in self.local_cache_completeness:
                self.load_completeness_doc(compute_key, product_document)

                self.logger.debug(
                    "[ITER][Product] - Added key to compute : %s", compute_key
                )

        self.logger.info("[ITER][Product] - end")

        # load related tickets
        self._populate_ticket_cache()

        self.logger.info("[ITER][Completeness] - start")
        # compute completeness
        for compute_key, (
            completeness_doc,
            original_completeness_doc_dict,
        ) in self.local_cache_completeness.items():

            completeness_value = completeness_doc.compute_values()

            observation_period = completeness_doc.compute_observation_period()

            completeness_doc.set_completeness(
                completeness_value,
                observation_period,
            )

            # link cams tickets
            if completeness_doc.datatake_id in self._cams_tickets_dict:
                self._apply_anomalies(completeness_doc, key="datatake_id")

            self.logger.info(
                "[ITER][Completeness][%s] - Computed value : %s for period : %s",
                compute_key,
                observation_period,
                completeness_value,
            )

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

        # generate pseudo datatake list without duplicates
        datatake_ids_set = set()

        for compute_key, (
            completeness_doc,
            original_completeness_doc_dict,
        ) in self.local_cache_completeness.items():
            datatake_ids_set.add(completeness_doc.datatake_id)

        self._populate_by_Datatake(list(datatake_ids_set))
