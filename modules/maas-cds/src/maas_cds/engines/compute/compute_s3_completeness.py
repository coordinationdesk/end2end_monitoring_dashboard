"""S3 Completeness calculation"""

from datetime import timedelta
import re
import typing
from maas_engine.engine.rawdata import DataEngine
from maas_model import ZuluDate
from opensearchpy import Q, MultiSearch
from maas_cds.engines.reports.anomaly_impact import AnomalyImpactMixinEngine
from maas_cds.lib.parsing_name.utils import DATATAKE_ID_MISSING_VALUE
from maas_cds.model.cds_s3_completeness import CdsS3Completeness
from maas_cds.model.product_s3 import CdsProductS3


class ComputeS3CompletenessEngine(AnomalyImpactMixinEngine, DataEngine):
    """Consolidate cds S3 completeness"""

    ENGINE_ID = "COMPUTE_S3_COMPLETENESS"
    ORBIT_DURATION_IN_MINUTES = 101
    PRODUCT_TYPE_TO_USE_FOR_MISSING_ORBIT_DETECTION = "TM_0_NAT___"
    TARGET_MODEL = "CdsS3Completeness"
    DATATAKE_ID_REGEX_FORMAT = r"S3[A-Z]-\d+-\d\d\d"

    def __init__(self, args=None, completeness_tolerance=None):

        super().__init__(args)

        CdsS3Completeness.COMPLETENESS_TOLERANCE = completeness_tolerance

        self.local_cache_completeness = {}
        self.products_to_consider_for_missing_orbits = []

        self.target_model = self.get_model(ComputeS3CompletenessEngine.TARGET_MODEL)

        if self.target_model is None:
            raise KeyError(f"The target model doesn't exist: {self.target_model }")

    def create_completeness_doc(
        self,
        compute_key: str,
        product_document,
        model_class,
    ):
        """Create a completeness doc

        Args:
            compute_key (str): _description_
            product_document: the origin document
            model_class: the DAO class
        Returns:
            Nothing
        """

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
        # We do it only when the
        if (
            product_document.product_type
            and product_document.product_type
            == ComputeS3CompletenessEngine.PRODUCT_TYPE_TO_USE_FOR_MISSING_ORBIT_DETECTION
        ):

            self.logger.debug(
                "[CACHE] - key : %s not found in cds-s3-completeness index, "
                "create all completeness for %s",
                compute_key,
                product_document.datatake_id,
            )

            datas_for_completnesses = completeness_doc.init_completenesses()

            self.logger.debug("DATA4COMPLETENESS %s", datas_for_completnesses)

            # create all completeness
            docs_in_db = CdsS3Completeness.mget_by_ids(list(datas_for_completnesses.keys()))

            for (key, data_for_completeness),doc_in_db in zip(datas_for_completnesses.items(),docs_in_db):
                if key != compute_key and key not in self.local_cache_completeness and not doc_in_db:
                    # create all others completeness and store it in the local cache
                    self.logger.debug("Creating completeness: %s", key)
                    completeness_doc = model_class(**data_for_completeness)
                    completeness_doc.meta.id = data_for_completeness["key"]

                    self.local_cache_completeness[key] = (
                        completeness_doc,
                        None,
                    )

    def action_iterator(self):
        """Compute completeness from CdsProduct

        Yields:
            dict: bulk action
        """

        self.logger.info("[ITER][Product] - start")

        # Load all completeness documents using info from input document
        self.load_all_completeness_doc(self.input_documents)
        self.logger.info("[ITER][Product] - end")

        # load related tickets
        self._populate_ticket_cache()

        self.logger.info("[ITER][Missing Orbit search] - start")

        # Handle missing datatake_id
        # If we received products from datatake_id X and Z but not Y
        # we shall still create a completeness doc for each Y related products
        # so that user can see that it is equal to 0.

        if self.products_to_consider_for_missing_orbits:
            identified_missing_datatakes_ids = self.identify_missing_datatakes_ids()
            if identified_missing_datatakes_ids:
                self.add_missing_completeness_documents(
                    identified_missing_datatakes_ids
                )

        self.logger.info("[ITER][Missing Orbit search] - end")

        self.logger.info("[ITER][Completeness] - start")

        # compute completeness
        for compute_key, (
            completeness_doc,
            original_local_cache_completeness,
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
            if (
                not original_local_cache_completeness
                or original_local_cache_completeness | new_doc_dict
                != original_local_cache_completeness
            ):

                # convert dao to bulk payload
                local_cache_completeness = completeness_doc.to_bulk_action()

                self.logger.info(
                    "[ITER][Completeness][%s] - Pushing update", compute_key
                )

                # go feed parallel_bulk
                yield local_cache_completeness

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
            original_local_cache_completeness,
        ) in self.local_cache_completeness.items():
            datatake_ids_set.add(completeness_doc.datatake_id)

        self._populate_by_Datatake(list(datatake_ids_set))

    def load_all_completeness_doc(self, products: typing.List[CdsProductS3]) -> None:
        """This function parse all input CdsProductS3 and generate a
        completeness doc for it if this doc does not already exist in db

        It also keep in a list all products of a specific product_type
        which are used to find missing orbits in the S3 completeness database

        Args:
            products (typing.List[CdsProductS3]): List of CdsProductS3 given in input to the engine
        """

        compute_keys = []
        considered_products = []

        # Filter the input documents to keep only the ones
        # which are taken into account for completeness calculation
        for product in products:

            # We only calculate consolidation for a subset of products
            # If the product is not in S3_PRODUCTS_TYPES, we ignore it
            if (
                product.datatake_id in ("", None, DATATAKE_ID_MISSING_VALUE)
                or product.product_type not in CdsS3Completeness.S3_PRODUCTS_TYPES
                or product.timeliness
                not in CdsS3Completeness.S3_PRODUCTS_TYPES[product.product_type][
                    "timeliness"
                ]
            ):
                self.logger.info(
                    "The following product%s with type: %s and timeliness:"
                    "%s will not be taken into account for timeliness. Either"
                    "it has an invalid datatake_id or its product_type/timeliness"
                    "  is not configured to be parsed by the engine",
                    product.datatake_id,
                    product.product_type,
                    product.timeliness,
                )
                continue

            key = product.get_compute_key()

            if key is None:
                self.logger.warning(
                    "Cannot generate compute key for product %s", product.name
                )
                continue

            # Case where we receive several product with same
            # product type,timeliness for same datatake
            if key in compute_keys:
                continue

            compute_keys.append(key)
            considered_products.append(product)
            if (
                product.product_type
                == ComputeS3CompletenessEngine.PRODUCT_TYPE_TO_USE_FOR_MISSING_ORBIT_DETECTION
            ):
                self.products_to_consider_for_missing_orbits.append(product)

        if considered_products:
            # For each input product taken into account,
            # we create the completeness doc if it is not already in DB
            for key, doc, product in zip(
                compute_keys,
                CdsS3Completeness.mget_by_ids(compute_keys),
                considered_products,
            ):
                if not doc and key not in self.local_cache_completeness:
                    self.logger.debug("[CACHE] - key neither found in db nor in local cache, create a new one : %s",key,)
                    self.create_completeness_doc(key, product, self.target_model)
                elif key in self.local_cache_completeness:
                    self.logger.debug(
                        "[CACHE] - key found in local cache, no document to create for %s",
                        key,
                    )
                elif doc:
                    self.logger.debug(
                        "[CACHE] - key found in cds-s3-completeness index, using the one from DB : %s",
                        key,
                    )
                    original_completeness_doc = doc.to_dict()
                    self.local_cache_completeness[key] = (
                        doc,
                        original_completeness_doc,
                )


    def identify_missing_datatakes_ids(
        self,
    ) -> typing.List[typing.Tuple[str, ZuluDate, ZuluDate]]:
        """This function will parse a list of CDSProductS3 and for each element
        it will :
         1) retrieve it's datatake id
         2)a retrieve the closest product in the past of same type in local cache or in db
         2)b retrieve the closest completeness doc in the past of same product type/timeliness in db
         3) analyse the gap between itself and the closest in the past (2a or 2b)
         4) If there is a datatake_id gap,
            it will add to a list all datatake_ids missing between them
            for each missing datatake_id we also save the  sensing dates of 1) product
         5) return the list created in 4)

        Returns:
            typing.List[typing.Tuple[str, ZuluDate, ZuluDate]]:
                  A list of tuple containingthe missing datatake_id and
                  its associated supposed sensing_start_date & sensing_end_date
        """

        identified_missing_previous_orbits = []
        msearch = MultiSearch()

        filtered_products = self.filter_products_list_used_for_missing_orbit_detection(
            self.products_to_consider_for_missing_orbits
        )

        for product, _ in filtered_products:
            msearch = msearch.add(
                self.target_model.search()
                .filter("term", mission=product.mission)
                .filter("term", satellite_unit=product.satellite_unit)
                .filter("term", product_type=product.product_type)
                .filter("term", timeliness=product.timeliness)
                .filter("bool", must_not=Q("term", datatake_id=product.datatake_id))
                .filter(
                    "range",
                    observation_time_start={"lt": product.sensing_start_date},
                )
                .sort({"observation_time_start": {"order": "desc"}})
            )

        for (product, closest_local), response in zip(
            filtered_products, msearch.execute()
        ):

            # For each considered product, look for the closest completeness doc in the past  (DB)
            closest_db = None
            response = list(response)
            if response:
                closest_db = response[0]

            # Keep the closest between local and db
            if closest_local and closest_db:
                closest_dtk_id = ComputeS3CompletenessEngine.sort_datatake_id(
                    closest_local.datatake_id, closest_db.datatake_id
                )[1]
            elif closest_local:
                closest_dtk_id = closest_local.datatake_id
            elif closest_db:
                closest_dtk_id = closest_db.datatake_id
            else:
                self.logger.warning(
                    "Could not find any previous datatake_id for product"
                    " of type %s with datatake id %s. No missing orbit"
                    " check can be performed for this datatake_id",
                    self.PRODUCT_TYPE_TO_USE_FOR_MISSING_ORBIT_DETECTION,
                    product.datatake_id,
                )
                continue

            missing_dtk_list = self.generate_datatake_ids_list_between_2_ids(
                closest_dtk_id, product.datatake_id
            )
            identified_missing_previous_orbits.extend(
                (
                    dtk,
                    product.sensing_start_date
                    - i * timedelta(minutes=self.ORBIT_DURATION_IN_MINUTES),
                    product.sensing_end_date
                    - i * timedelta(minutes=self.ORBIT_DURATION_IN_MINUTES),
                )
                for i, dtk in enumerate(missing_dtk_list, 1)
            )

        return identified_missing_previous_orbits

    def filter_products_list_used_for_missing_orbit_detection(
        self,
        products: typing.List[CdsProductS3],
    ) -> typing.List[typing.Tuple[CdsProductS3, CdsProductS3]]:
        """This function filter the list of product given in argument so that
        all product which have a direct predecessor are ignored in the return list

        Args:
            products (typing.List[CdsProductS3]): The list of CdsProduct to filter for analysis

        Returns:
            typing.List[typing.Tuple[CdsProductS3, CdsProductS3]]:
            list of tuple containing a product which has not a direct predecessor ( datatake_id-1) in the local cache
            and its closest predecessor in local if any
        """
        # In the products_to_consider_for_missing_orbits list,
        # we filter so that there is only 1 element per datatake_id
        # We take the longest sensing duration.
        filtered_map = {}
        filtered_list = []
        for product in products:
            if (
                product.datatake_id not in filtered_map
                or filtered_map[product.datatake_id].sensing_duration
                < product.sensing_duration
            ):
                filtered_map[product.datatake_id] = product

        filtered_list = list(filtered_map.values())

        # Sort in sensing start date order
        filtered_list.sort(key=lambda doc: doc.sensing_start_date)

        # We shall eliminate from our analysis the product which have
        # an immediate precedent product in the list
        # Indeed there can be no missing datatake_id in this case

        # For each remaining possible problematic case,
        # we keep the closest local product in the past
        products_for_gap_analysis = []
        for i, _ in enumerate(filtered_list):
            if i == 0:
                products_for_gap_analysis.append((filtered_list[i], None))
            elif self.generate_datatake_ids_list_between_2_ids(
                filtered_list[i].datatake_id,
                filtered_list[i - 1].datatake_id,
            ):
                products_for_gap_analysis.append(
                    (filtered_list[i], filtered_list[i - 1])
                )

        return products_for_gap_analysis

    @staticmethod
    def generate_datatake_ids_list_between_2_ids(
        datatake_ref_1: str, datatake_ref_2: str
    ) -> typing.List[str]:
        """Function which return a list of all S3 datatakes_id string which are
        between 2 S3 datatake_ids given as arguments

        Args:
            datatake_ref_1 (str): 1st datatake_id reference
            datatake_ref_2 (str): 2nd datatake_id reference

        Raises:
            ValueError: ValueError raised if datatake_ids does not respect the expected format

        Returns:
            typing.List[str]: The list of datatake_ids between the 2 references
        """
        datatake_list = []

        if not re.search(
            ComputeS3CompletenessEngine.DATATAKE_ID_REGEX_FORMAT, datatake_ref_1
        ) or not re.search(
            ComputeS3CompletenessEngine.DATATAKE_ID_REGEX_FORMAT, datatake_ref_2
        ):
            raise ValueError("Inputs arguments does not respect the expected format")

        if datatake_ref_1 == datatake_ref_2:
            return []
        minref, maxref = ComputeS3CompletenessEngine.sort_datatake_id(
            datatake_ref_1, datatake_ref_2
        )
        while True:
            satellite, cycle_count, relative_orbit = maxref.split("-")
            cycle_count = int(cycle_count)
            relative_orbit = int(relative_orbit)

            relative_orbit -= 1
            if relative_orbit < 1:
                relative_orbit = 385
                cycle_count -= 1
            maxref = f"{satellite}-{cycle_count:03}-{relative_orbit:03}"
            if maxref == minref:
                break
            datatake_list.append(maxref)

        return datatake_list

    def add_missing_completeness_documents(
        self, datatake_ids_tuples: typing.List[typing.Tuple[str, ZuluDate, ZuluDate]]
    ) -> None:
        """Function which create empty completeness documents for all missing product
        type and each timeliness of a datatakes id list given in input

        Args:
            datatake_ids_tuples (List[Tuple[str, ZuluDate, ZuluDate]]):
               list of tuples containing a datatake_id and a start and an end
               date which is used to determine the compute key to create in db

        """
        key_dict = {}
        ref_prod_type = self.PRODUCT_TYPE_TO_USE_FOR_MISSING_ORBIT_DETECTION
        ref_prod_level = CdsS3Completeness.S3_PRODUCTS_TYPES[
            self.PRODUCT_TYPE_TO_USE_FOR_MISSING_ORBIT_DETECTION
        ]["level"]

        ref_timeliness = CdsS3Completeness.S3_PRODUCTS_TYPES[
            self.PRODUCT_TYPE_TO_USE_FOR_MISSING_ORBIT_DETECTION
        ]["timeliness"][0]

        # Transform a datatake_id list into a dictionnary of compute_key
        # Indeed for 1 missing datatake_id, there is multiple completeness doc to create
        # Each timeliness of each product type has its own completeness doc
        key_dict = {
            CdsProductS3.calculate_compute_key(
                datatake_id,
                ref_prod_type,
                ref_timeliness,
            ): {
                "datatake_id": datatake_id,
                "sensing_start_date": sensing_start_date,
                "sensing_end_date": sensing_end_date,
            }
            for datatake_id, sensing_start_date, sensing_end_date in datatake_ids_tuples
        }

        # If compute key not in cache and not in db, create a default empty completeness doc
        for compute_key, db_response in zip(
            key_dict.keys(), self.target_model.mget_by_ids(list(key_dict.keys()))
        ):
            if not db_response and compute_key not in self.local_cache_completeness:
                prod = CdsProductS3()
                prod.datatake_id = key_dict[compute_key]["datatake_id"]
                prod.sensing_start_date = key_dict[compute_key]["sensing_start_date"]
                prod.sensing_end_date = key_dict[compute_key]["sensing_end_date"]
                prod.product_type = ref_prod_type
                prod.product_level = "L" + str(ref_prod_level) + "_"
                prod.timeliness = ref_timeliness
                prod.mission = "S3"
                prod.satellite_unit = compute_key[:3]
                self.logger.info(
                    "The S3 completeness doc with compute key %s has been determined"
                    " as missing in the database and will now be created",
                    compute_key,
                )
                self.create_completeness_doc(compute_key, prod, self.target_model)

    @staticmethod
    def sort_datatake_id(
        datatake_id_1: str, datatake_id_2: str
    ) -> typing.Tuple[str, str]:
        """This function sort 2 datatake ids in ascending order

        Args:
            datatake_id_1 (str): datatake_id string nb1
            datatake_id_2 (str): datatake_id string nb2

        Raises:
            ValueError: ValueError raised if datatake_id does not respect the expected format

        Returns:
            Tuple[str, str]: The 2 datatake_ids string sorted in ascending order in a tuple
        """
        if not re.search(
            ComputeS3CompletenessEngine.DATATAKE_ID_REGEX_FORMAT, datatake_id_1
        ) or not re.search(
            ComputeS3CompletenessEngine.DATATAKE_ID_REGEX_FORMAT, datatake_id_2
        ):
            raise ValueError("Inputs arguments does not respect the expected format")

        ref_part_1 = datatake_id_1.split("-")
        ref_part_2 = datatake_id_2.split("-")
        val1 = int(ref_part_1[1]) * 10000 + int(ref_part_1[2])
        val2 = int(ref_part_2[1]) * 10000 + int(ref_part_2[2])
        return (
            (datatake_id_1, datatake_id_2)
            if val2 >= val1
            else (datatake_id_2, datatake_id_1)
        )
