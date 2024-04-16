"""

Engine and consolidation decorator to update cams issues impact in consolidation
"""

from functools import wraps
import logging
import typing

from maas_model import MAASDocument

from maas_cds.lib.parsing_name.utils import generate_publication_names

from maas_cds.model.anomaly_mixin import AnomalyMixin

from maas_cds.model import CdsCamsTickets


def anomaly_link(method):
    """
    A decorator that populate anomaly related fields using AnomalyImpactMixinEngine

    Args:
        method (callable): a engine method that produces consolidated entities

    Returns:
        callable: decorated method
    """

    @wraps(method)
    def _impl(self, *method_args, **method_kwargs) -> AnomalyMixin:
        logging.debug(
            "anomaly_link calls %s args=%s kw=%s", method, method_args, method_kwargs
        )
        output_entity = method(self, *method_args, **method_kwargs)

        logging.debug("Result: %s", output_entity)

        if output_entity:
            self._apply_anomalies(output_entity)

        return output_entity

    return _impl


class AnomalyImpactMixinEngine:
    """

    Engine Mixin to handle links to to cams tickets and correlation file

    It preload cams tickets related to entities
    """

    _cams_tickets_dict = {}

    def get_consolidated_documents(self) -> typing.List[MAASDocument]:
        """

        Override to populate the ticket cache

        Returns:
            list: consolidated documents
        """
        # reset the cache at consolidated document search
        self._cams_tickets_dict = {}

        consolidated_documents = super().get_consolidated_documents()

        if consolidated_documents:
            self._populate_ticket_cache(consolidated_documents)

        return consolidated_documents

    def _populate_ticket_cache(self, consolidated_documents: typing.List[MAASDocument]):
        """
        Fill the ticket cache with a dedicated method

        Args:
            consolidated_documents (List[MAASDocument]): consolidated documents

        Raises:
            NotImplementedError: if entity is not handled
        """
        method_name = f"_populate_by_{consolidated_documents[0].__class__.__name__}"
        if hasattr(self, method_name):
            self.logger.debug("Found %s for ticket search", method_name)
            cams_search = getattr(self, method_name)
            cams_search(consolidated_documents)
        else:
            raise NotImplementedError(
                f"No method AnomalyImpactMixinEngine.{method_name} found to link anomalies"
            )

        self.logger.debug("_cams_tickets_dict: %s", self._cams_tickets_dict)

    def _apply_anomalies(self, entity: AnomalyMixin, key="key"):
        """link entity to tickets"""

        if isinstance(key, str):
            key_value = getattr(entity, key)

        elif callable(key):
            try:
                key_value = key(entity)
            except Exception as error:
                self.logger.error(
                    "Cannot compute anomaly key for %s : %s", entity, entity.to_dict()
                )
                return
        else:
            raise TypeError(f"wrong type for key parameter {key}")
        if key_value in self._cams_tickets_dict:
            self.logger.info(
                "AnomalyLink %s to %s", entity, self._cams_tickets_dict[key_value]
            )
            for ticket in self._cams_tickets_dict[key_value]:
                entity.set_last_attached_ticket(ticket)

    def _populate_by_CdsProduct(self, consolidated_documents):
        """Populate ticket cache for products"""

        products = {}

        for raw_document in self.input_documents:
            for product_name in generate_publication_names(raw_document.product_name):
                products[product_name] = raw_document

        tickets = (
            CdsCamsTickets()
            .search()
            .filter(
                "terms",
                products=list(products.keys()),
            )
            .sort({"updated": {"order": "asc"}})
            .params(size=10000)
            .execute()
        )

        for ticket in tickets:
            for product_name in ticket.products:
                if product_name not in products:
                    continue

                if product_name in self._cams_tickets_dict:
                    self._cams_tickets_dict[
                        self.get_consolidated_id(products[product_name])
                    ].append(ticket)
                else:
                    self._cams_tickets_dict[
                        self.get_consolidated_id(products[product_name])
                    ] = [ticket]

    def _populate_by_CdsPublication(self, consolidated_documents):
        """Populate ticket cache for publications"""

        publications = {}

        for raw_document in self.input_documents:
            for publication_name in generate_publication_names(
                raw_document.product_name
            ):
                publications[publication_name] = raw_document

        tickets = (
            CdsCamsTickets()
            .search()
            .filter(
                "terms",
                publications=list(publications.keys()),
            )
            .sort({"updated": {"order": "asc"}})
            .params(size=10000)
            .execute()
        )

        for ticket in tickets:
            for publication in ticket.publications:
                if publication not in publications:
                    continue

                if publication in self._cams_tickets_dict:
                    self._cams_tickets_dict[
                        self.get_consolidated_id(publications[publication])
                    ].append(ticket)
                else:
                    self._cams_tickets_dict[
                        self.get_consolidated_id(publications[publication])
                    ] = [ticket]

    def _populate_by_Datatake(self, datatake_ids):
        """Populate ticket cache for datakes"""
        self._find_and_populate({"datatake_ids": datatake_ids}, "datatake_ids")

    def _populate_by_CdsAcquisitionPassStatus(self, consolidated_documents):
        """Populate ticket cache for x-band acquisition status"""

        acquisition_pass = []

        for raw_pass in self.input_documents:
            orbit = raw_pass.downlink_orbit
            if not isinstance(orbit, str):
                orbit = str(int(orbit))

            if raw_pass.satellite_id.startswith("S5"):
                # handle special case for S5 where ground station is not in the doc
                ground_station = raw_pass.reportName.split("_")[0]
            else:
                ground_station = raw_pass.ground_station

            acquisition_pass.append(
                "_".join([raw_pass.satellite_id, "X-Band", orbit, ground_station])
            )

        self.logger.debug("acquisition_pass criteria: %s", acquisition_pass)

        self._find_and_populate(
            {"acquisition_pass": acquisition_pass}, "acquisition_pass"
        )

    def _populate_by_CdsCadipAcquisitionPassStatus(self, consolidated_documents):
        """Populate ticket cache for cadip acquisition status"""

        acquisition_pass = []

        for raw_pass in self.input_documents:
            orbit = raw_pass.downlink_orbit
            if not isinstance(orbit, str):
                orbit = str(int(orbit))

            acquisition_pass.append(
                "_".join(
                    [raw_pass.satellite_id, "X-Band", orbit, raw_pass.ground_station]
                )
            )

        self.logger.debug("acquisition_pass criteria: %s", acquisition_pass)

        self._find_and_populate(
            {"acquisition_pass": acquisition_pass}, "acquisition_pass"
        )

    def _populate_by_CdsHktmAcquisitionCompleteness(self, consolidated_documents):
        """Populate ticket cache for cadip acquisition status"""

        acquisition_pass = []

        for raw_pass in consolidated_documents:
            orbit = raw_pass.absolute_orbit
            if not isinstance(orbit, str):
                orbit = str(int(orbit))

            if "EDRS" in raw_pass.production_service_name:
                acquisition_pass.append(
                    "_".join(
                        [
                            raw_pass.satellite_id,
                            "EDRS",
                            raw_pass.session_id,
                            raw_pass.ground_station,
                        ]
                    )
                )
            else:
                acquisition_pass.append(
                    "_".join(
                        [
                            raw_pass.satellite_id,
                            "X-Band",
                            orbit,
                            raw_pass.ground_station,
                        ]
                    )
                )

        self.logger.debug("acquisition_pass criteria: %s", acquisition_pass)

        self._find_and_populate(
            {"acquisition_pass": acquisition_pass}, "acquisition_pass"
        )

    def _populate_by_CdsEdrsAcquisitionPassStatus(self, consolidated_documents):
        """Populate ticket cache for edrs acquisition status"""

        acquisition_pass = []

        for raw_pass in self.input_documents:
            if not all(
                [
                    raw_pass.satellite_id,
                    raw_pass.link_session_id,
                    raw_pass.ground_station,
                ]
            ):
                self.logger.error(
                    "Cannot generate pass identifier for %s", raw_pass.to_dict()
                )
                continue

            acquisition_pass.append(
                "_".join(
                    [
                        raw_pass.satellite_id,
                        "EDRS",
                        raw_pass.link_session_id,
                        raw_pass.ground_station,
                    ]
                )
            )

        self.logger.debug("acquisition_pass criteria: %s", acquisition_pass)

        self._find_and_populate(
            {"acquisition_pass": acquisition_pass}, "acquisition_pass"
        )

    def _find_and_populate(self, criteria, field):
        tickets = (
            CdsCamsTickets()
            .search()
            .filter("terms", **criteria)
            .sort({"updated": {"order": "asc"}})
            .params(size=10000)
            .execute()
        )

        for ticket in tickets:
            for row in getattr(ticket, field):
                if row in self._cams_tickets_dict:
                    self._cams_tickets_dict[row].append(ticket)
                else:
                    self._cams_tickets_dict[row] = [ticket]
