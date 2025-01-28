"""Maintain cams anomalies impact over entities"""

import datetime
import re
from typing import Any, Dict, List, Iterator
from collections import defaultdict

from opensearchpy import NotFoundError, Keyword

from maas_model import MAASDocument

from maas_engine.engine.rawdata import DataEngine

from maas_cds.lib.parsing_name.utils import (
    normalize_product_name_list,
    generate_publication_names,
)

from maas_cds.model import (
    CamsAnomalyCorrelation,
    CamsCloudAnomalyCorrelation,
    CdsCamsTickets,
    CdsDatatakeS1,
    CdsDatatakeS2,
    CdsS3Completeness,
    CdsS5Completeness,
    CdsAcquisitionPassStatus,
    CdsCadipAcquisitionPassStatus,
    CdsEdrsAcquisitionPassStatus,
    CdsHktmAcquisitionCompleteness,
    CdsProduct,
    CdsPublication,
)
from maas_cds.model.generated import CamsCloudTickets


class ConsolidateAnomalyCorrelationFileEngine(DataEngine):
    """Consolidate anomaly correlation info to various entities"""

    ENGINE_ID = "CONSOLIDATE_ANOMALY_CORRELATION_FILE"

    IMPACTED_CLASSES = (
        CdsDatatakeS1,
        CdsDatatakeS2,
        CdsS3Completeness,
        CdsS5Completeness,
        CdsAcquisitionPassStatus,
        CdsCadipAcquisitionPassStatus,
        CdsEdrsAcquisitionPassStatus,
        CdsHktmAcquisitionCompleteness,
        CdsProduct,
        CdsPublication,
    )

    # this dictionnary maps mission to document class and retrieval method: direct
    # document identifiers for S1 & S2, or search on the datatake_id field for S3 & S5
    DATATAKE_ENTITY_DICT = {
        "S1": (CdsDatatakeS1, "ids"),
        "S2": (CdsDatatakeS2, "ids"),
        "S3": (CdsS3Completeness, "search"),
        "S5": (CdsS5Completeness, "search"),
    }

    # pylint: disable=C0301
    # black formatting makes lambda lines too long
    ACQUISITION_QUERY_DICT = {
        "EDRS": [
            {
                "class": CdsEdrsAcquisitionPassStatus,
                "search": lambda satellite_id, identifier, ground_station: CdsEdrsAcquisitionPassStatus.search()
                .query()
                .filter("term", satellite_id=satellite_id.upper())
                .filter("term", link_session_id=identifier)
                .filter("term", ground_station=ground_station.upper()),
            },
            {
                "class": CdsHktmAcquisitionCompleteness,
                "search": lambda satellite_id, identifier, ground_station: CdsHktmAcquisitionCompleteness.search()
                .query()
                .filter("term", satellite_unit=satellite_id.upper())
                .filter("term", session_id=identifier)
                .filter("term", ground_station=ground_station.upper()),
            },
        ],
        "X-Band": [
            {
                "class": CdsAcquisitionPassStatus,
                "search": lambda satellite_id, identifier, ground_station: CdsAcquisitionPassStatus.search()
                .query()
                .filter("term", satellite_id=satellite_id.upper())
                .filter("term", downlink_orbit=identifier)
                .filter("term", ground_station=ground_station.upper()),
            },
            {
                "class": CdsCadipAcquisitionPassStatus,
                "search": lambda satellite_id, identifier, ground_station: CdsCadipAcquisitionPassStatus.search()
                .query()
                .filter("term", satellite_id=satellite_id.upper())
                .filter("term", downlink_orbit=identifier)
                .filter("term", ground_station=ground_station.upper()),
            },
            {
                "class": CdsHktmAcquisitionCompleteness,
                "search": lambda satellite_id, identifier, ground_station: CdsHktmAcquisitionCompleteness.search()
                .query()
                .filter("term", satellite_unit=satellite_id.upper())
                .filter("term", absolute_orbit=identifier)
                .filter("term", ground_station=ground_station.upper()),
            },
        ],
    }

    INUVIK_STATION = "Inuvik Station"
    NEUSTRELITZ_STATION = "Neustrelitz Station"
    SVALBARD_STATION = "Svalbard Station"

    # pylint: enable=C0301

    PRODUCT_IMPACTED = (CdsProduct, CdsPublication)

    # pylint: disable=R0913
    # engine contructor shall have many arguments
    def __init__(
        self,
        args=None,
        send_reports=False,
        max_datatakes=10000,
        max_acquisitions=10000,
        max_products=10000,
        base_url="https://cams.esa.int/browse/",
    ):
        super().__init__(args, send_reports=send_reports)
        # max_* attribute are here to fill size parameter of search request
        self.max_datatakes = max_datatakes
        self.max_acquisitions = max_acquisitions
        self.max_products = max_products

        # base url for link rendering
        self.base_url: str = base_url

        # a flag to tell to update all entities because source or description changed
        self.update_all_entities = False

    def action_iterator(self) -> Iterator[Dict[str, Any]]:
        # setup specific settings depending input
        match self.payload.document_class:
            case "CamsAnomalyCorrelation":
                consolidate_method = self.consolidate_cams_ticket
                issue_attrname = "cams_issue"
            case "CamsCloudAnomalyCorrelation":
                consolidate_method = self.consolidate_cams_cloud_ticket
                issue_attrname = "issue"
            case _:
                raise TypeError(
                    "Cannot correlate objects of type %s", self.payload.document_class
                )

        for report in self.input_documents:
            ticket_id = getattr(report, issue_attrname, "")

            if not ticket_id:
                self.logger.warning(
                    "No related ticket found for Anomaly Correlation %s",
                    report.reportName,
                )
                continue

            ticket_id = ticket_id.strip()
            ticket = self.get_ticket(ticket_id)

            self.logger.info(
                "Consolidating file %s for ticket %s",
                report.reportName,
                ticket.key,
            )

            initial_ticket_dict = ticket.to_dict()

            # first, consolidate cams ticket
            consolidate_method(report, ticket)

            if not ticket.to_dict() != initial_ticket_dict:
                self.logger.info(
                    "No modification for correlation %s", ticket.correlation_file_id
                )
                return

            yield ticket.to_bulk_action()

            yield from self.correlate_ticket(ticket)

    def get_ticket(self, ticket_id: str | Keyword) -> CdsCamsTickets:
        """
        Get or create a CdsCamsTickets

        Args:
            ticket_id (str): ticket identifier

        Returns:
            CdsCamsTickets: initialized ticket
        """
        ticket = CdsCamsTickets.get_by_id(ticket_id)

        if not ticket:
            self.logger.warning(
                "Creating CamsTickets %s. "
                "In normal flow, the ticket shall be created before correlation !",
                ticket_id,
            )
            ticket = CdsCamsTickets()
            ticket.meta.id = ticket.key = ticket_id

            # fill the created field a value for partitionning, even if static
            ticket.created = datetime.datetime.now(tz=datetime.timezone.utc)
            ticket.updated = datetime.datetime.now(tz=datetime.timezone.utc)
        else:
            self.logger.debug("Search result for %s: %s", ticket_id, ticket)

        return ticket

    def correlate_ticket(self, ticket: CdsCamsTickets) -> Iterator[Dict[str, Any]]:
        """Correlate all entities described in the ticket

        Args:
            ticket (CdsCamsTickets): ticket to correlate

        Yields:
            Iterator[Dict[str, Any]]: bulk action
        """
        # get already linked documents
        linked_documents = self.get_linked_documents(ticket.key)

        for correlate_method, identifiers in [
            (self.correlate_datatakes, ticket.datatake_ids),
            (self.correlate_acquisitions, ticket.acquisition_pass),
            (self.correlate_products, normalize_product_name_list(ticket.products)),
        ]:
            self.logger.debug(
                "Calling %s with args: ids=%s, linked_documents=%s",
                correlate_method.__name__,
                identifiers,
                linked_documents,
            )

            yield from correlate_method(ticket, linked_documents)

    def fill_common_attributes(
        self,
        report: CamsAnomalyCorrelation | CamsCloudAnomalyCorrelation,
        ticket: CdsCamsTickets,
    ):
        """
        Consolidate basic attribute and detect origin or description changes to plan
        attribute updates on impacted entities

        Args:
            report (CamsAnomalyCorrelation | CamsCloudAnomalyCorrelation): input
            ticket (CdsCamsTickets): output
        """
        # consolidate attributes
        ticket.correlation_file_id = report.meta.id

        for attrname, value in (
            ("origin", report.origin),
            ("description", report.description),
        ):
            if getattr(ticket, attrname) != value:
                setattr(ticket, attrname, value)
                # propagated attribute changed: all impacted entities shall be updated
                self.update_all_entities = True

        ticket.url = self.base_url + ticket.meta.id

        ticket.products = normalize_product_name_list(report.products)

        # Depending on the sources, publications will have different file extensions
        # we generate all possible combinations to be able to correlate anomalies with them later

        ticket.publications = [
            publication_name
            for product_name in ticket.products
            for publication_name in generate_publication_names(product_name)
        ]

    def consolidate_cams_cloud_ticket(
        self, report: CamsCloudAnomalyCorrelation, ticket: CdsCamsTickets
    ):
        """Consolidate ticket with report informations

        Args:
            report (CamsCloudAnomalyCorrelation): anam
            ticket (CdsCamsTickets): _description_
        """
        self.fill_common_attributes(report, ticket)

        if (
            "DLR Acquisition Service" == ticket.entity
            and not self.NEUSTRELITZ_STATION in ticket.assigned_element
        ):
            ticket.assigned_element.append(self.NEUSTRELITZ_STATION)

        if (
            "SSC Acquisition Service" == ticket.entity
            and not self.INUVIK_STATION in ticket.assigned_element
        ):
            ticket.assigned_element.append(self.INUVIK_STATION)

        if isinstance(ticket.affected_systems, str):
            ticket.affected_systems = [ticket.affected_systems]

        if "S-5p" in ticket.affected_systems:
            if (
                "INU" in ticket.title
                and self.INUVIK_STATION not in ticket.assigned_element
            ):
                ticket.assigned_element.append(self.INUVIK_STATION)
            if (
                "SGS" in ticket.title
                and self.SVALBARD_STATION not in ticket.assigned_element
            ):
                ticket.assigned_element.append(self.SVALBARD_STATION)

        # consolidate report informations
        ticket.datatake_ids = report.impacted_observations

        if report.impacted_passes:
            acquisition_pass_keys = []
            if not report.station or not report.station_type:
                self.logger.warning(
                    "No station or station type provided in anomaly report %s",
                    report.key,
                )
                ticket.acquisition_pass = []

                return
            # Impacted pass must contains satellite like S1A-orbit
            for impacted_passe in report.impacted_passes:
                try:
                    (satellite, orbit) = impacted_passe.split("-")
                except ValueError as _not_enough_values_to_unpack:
                    self.logger.warning(
                        "Wrong format of passes type provided in anomaly report %s - %s | expected SXX-orbit",
                        report.key,
                        impacted_passe,
                    )
                    continue

                acquisition_pass_keys.append(
                    "_".join([satellite, report.station_type, orbit, report.station])
                )

            # Since the 21/06/2024 we supporte only orbit that are prefix by satellite unit to avoid collision in the futur
            # Keep it to be retroactive
            if report.created < datetime.datetime(
                2024, 7, 1, tzinfo=datetime.timezone.utc
            ):
                satellite_list = report.sattelite_unit
                if isinstance(report.sattelite_unit, str):
                    satellite_list = [report.sattelite_unit]
                for satellite in satellite_list:
                    for impacted_passe in report.impacted_passes:
                        acquisition_pass_keys.append(
                            "_".join(
                                [
                                    satellite,
                                    report.station_type,
                                    impacted_passe,
                                    report.station,
                                ]
                            )
                        )

            # remove duplicated
            ticket.acquisition_pass = list(dict.fromkeys(acquisition_pass_keys).keys())

        else:
            ticket.acquisition_pass = []

    def consolidate_cams_ticket(self, report: CamsAnomalyCorrelation, ticket):
        """Consolidate correlation info to the matching CdsCamsTickets.

        Args:
            report (CamsAnomalyCorrelation): data to consolidate

        Yields:
            Iterator[Dict]: bulk action
        """

        self.fill_common_attributes(report, ticket)

        # consolidate report informations
        ticket.datatake_ids = report.datatake_ids

        if report.acquisition_pass:
            acquisition_pass_keys = []

            for satellite, acq_type, orbit, station in report.acquisition_pass:
                if not all((satellite, acq_type, orbit, station)):
                    self.logger.warning(
                        "Imcompleted pass data: %s",
                        (satellite, acq_type, orbit, station),
                    )
                    continue

                if not isinstance(orbit, str) and isinstance(orbit, float):
                    orbit = str(int(orbit))

                # create a key for further search as opensearchpy does not allow to search
                # for array in array field
                acquisition_pass_keys.append(
                    "_".join([satellite, acq_type, orbit, station])
                )
            # remove duplicated
            ticket.acquisition_pass = list(dict.fromkeys(acquisition_pass_keys).keys())

        else:
            ticket.acquisition_pass = []

    def get_linked_documents(self, ticket_id: str | Keyword) -> dict:
        """Search all impacted entities that are linked to a ticket

        Args:
            ticket_id (str): ticket identifier

        Returns:
            dict: a dictionnary where keys are class names and values are documents
        """

        document_dict = {}

        for document_class in self.IMPACTED_CLASSES:
            self.logger.debug("%s: searching for linked %s", ticket_id, document_class)

            try:
                documents = (
                    document_class.search()
                    .query("term", cams_tickets=ticket_id)
                    .params(
                        version=True, seq_no_primary_term=True, size=self.max_datatakes
                    )
                    .execute()
                )

                if documents:
                    self.logger.debug("%s: found %s", ticket_id, documents)

                    document_dict[document_class.__name__] = documents

                else:
                    self.logger.debug(
                        "%s: no %s were found (%s)",
                        ticket_id,
                        document_class,
                        documents,
                    )

            except NotFoundError as error:
                self.logger.debug("%s: %s", error.__class__.__name__, error)

        self.logger.debug("Found linked documents for %s: %s", ticket_id, document_dict)

        return document_dict

    def apply_correlation(
        self,
        ticket: CdsCamsTickets,
        class_obj,
        linked_documents: list[MAASDocument],
        target_ids_or_documents: list,
    ) -> Iterator[Dict[str, Any]]:
        """
        Correlate ticket to document from a given class

        Args:
            ticket.key (str): ticket identifier
            class_obj (_type_): the impacted document class object
            linked_documents (list[MAASDocument]): list of documents ob
            target_ids_or_documents (list): a list of documents or
                indentifiers to impact

        Yields:
            Dict[str, Any]: bulk actions
        """

        self.logger.debug(
            "apply correlation for ticket %s to %s. linked: %s target: %s",
            ticket.key,
            class_obj.__name__,
            linked_documents,
            target_ids_or_documents,
        )

        if not (linked_documents or target_ids_or_documents):
            self.logger.warning(
                "No modification to apply to %s for %s", class_obj.__name__, ticket.key
            )
            return

        existing_ids = {document.meta.id for document in linked_documents}

        has_documents_arg = False

        if target_ids_or_documents:
            if isinstance(target_ids_or_documents[0], MAASDocument):
                # a list of instances have been provided
                target_ids = {document.meta.id for document in target_ids_or_documents}
                has_documents_arg = True
            elif isinstance(target_ids_or_documents[0], str):
                target_ids = set(target_ids_or_documents)
            else:
                raise TypeError(
                    f"Cannot use "
                    f"{target_ids_or_documents[0].__class__.__name__}"
                    " as target_ids_or_documents argument"
                )
        else:
            target_ids = set()

        if self.update_all_entities:
            to_link_ids = target_ids
        else:
            to_link_ids = target_ids - existing_ids

        to_unlink_ids = existing_ids - target_ids

        self.logger.debug("to link: %s ; to unlink: %s", to_link_ids, to_unlink_ids)

        if has_documents_arg:
            target_documents = [
                document
                for document in target_ids_or_documents
                if document.meta.id in to_link_ids
            ]
        elif to_link_ids:
            to_link_ids_list = list(to_link_ids)

            target_documents = list(
                class_obj.mget_by_ids(to_link_ids_list, ignore_missing_index=True)
            )

            if not all(target_documents):
                self.logger.warning(
                    "Some %s are missing in %s", class_obj.__name__, to_link_ids
                )
                # recover to known documents
                target_documents = [
                    document for document in target_documents if document
                ]
                self.logger.debug("target restricted to %s", target_documents)
        else:
            target_documents = []

        for to_link_document in target_documents:
            if not ticket.key in to_link_document.cams_tickets:
                self.logger.debug("Linking %s to %s", ticket.key, to_link_document)
                to_link_document.cams_tickets.append(ticket.key)
            else:
                self.logger.debug(
                    "%s Already linked to %s", ticket.key, to_link_document
                )

            to_link_document.set_last_attached_ticket(ticket)

            yield to_link_document.to_bulk_action()

        for to_unlink_document in [
            document
            for document in linked_documents
            if document.meta.id in to_unlink_ids
        ]:
            self.logger.debug("Unlinking %s from %s", ticket.key, to_unlink_document)

            to_unlink_document.cams_tickets.remove(ticket.key)

            to_unlink_document.unset_last_attached_ticket()

            yield to_unlink_document.to_bulk_action()

    def correlate_datatakes(
        self, ticket: CdsCamsTickets, linked_documents: list[MAASDocument]
    ) -> Iterator[Dict[str, Any]]:
        """
        Handle correlation for datatakes from any mission

        Args:
            report (CamsAnomalyCorrelation): raw data
            linked_documents (dict): current impact of the anomaly

        Yields:
            Iterator[typing.Generator]: bulk actions
        """

        mission_datatake_dict = defaultdict(list)

        if ticket.datatake_ids:
            # group by mission for robustness
            for datatake_id in ticket.datatake_ids:
                mission = datatake_id[:2]
                mission_datatake_dict[mission].append(datatake_id)

        self.logger.debug("mission_datatake_dict: %s", mission_datatake_dict)

        for (
            mission,
            (class_obj, retrieve_method_type),
        ) in self.DATATAKE_ENTITY_DICT.items():
            existing_documents = []

            if class_obj.__name__ in linked_documents:
                mission_linked_list = linked_documents[class_obj.__name__]

                # filter by mission because of S1 / S2 datatakes are in the same index
                existing_documents.extend(
                    [
                        document
                        for document in mission_linked_list
                        if document.meta.id.startswith(mission)
                    ]
                )
                if existing_documents:
                    self.logger.debug("Found linked: %s", existing_documents)

            target_ids = mission_datatake_dict.get(mission, [])

            if not (existing_documents or target_ids):
                self.logger.debug("nothing to do for mission %s", mission)
                # nothing to do for this mission
                continue

            if retrieve_method_type == "ids":
                correlate_arg = target_ids

            elif retrieve_method_type == "search":
                search = class_obj.search().filter("terms", datatake_id=target_ids)

                results = search.params(
                    version=True,
                    seq_no_primary_term=True,
                    size=self.max_datatakes,
                ).execute()

                correlate_arg = list(results)

            else:
                raise ValueError(
                    f"Invalid retrieve_method_type:  {retrieve_method_type}"
                )

            yield from self.apply_correlation(
                ticket,
                class_obj,
                existing_documents,
                correlate_arg,
            )

    def correlate_acquisitions(
        self, ticket: CdsCamsTickets, linked_documents: dict
    ) -> Iterator[Dict[str, Any]]:
        """
        Handle correlation for x-band, edrs acquisition pass status.

        Args:
            report (CamsAnomalyCorrelation): raw data
            linked_documents (dict): current impact of the anomaly

        Yields:
            Iterator[typing.Generator]: bulk actions
        """

        target_documents = {"EDRS": {}, "X-Band": {}}

        if ticket.acquisition_pass:
            for pass_key in ticket.acquisition_pass:
                satellite_id, station_type, identifier, ground_station = pass_key.split(
                    "_"
                )

                if not station_type in self.ACQUISITION_QUERY_DICT:
                    self.logger.warning("Unknown station type: %s", station_type)
                    continue

                if not isinstance(identifier, str):
                    if isinstance(identifier, float):
                        identifier = f"{int(identifier)}"
                    elif identifier:
                        identifier = str(identifier)
                    else:
                        self.logger.warning(
                            "No identifier found in %s",
                            (satellite_id, station_type, identifier, ground_station),
                        )
                        continue

                for interface in self.ACQUISITION_QUERY_DICT[station_type]:
                    search = interface["search"](
                        satellite_id,
                        identifier,
                        ground_station,
                    )

                    results = search.params(
                        version=True,
                        seq_no_primary_term=True,
                        size=self.max_acquisitions,
                    ).execute()

                    if not results:
                        self.logger.warning(
                            "No results for Acquisition: %s %s %s %s",
                            satellite_id,
                            station_type,
                            identifier,
                            ground_station,
                        )
                        continue

                    classname = interface["class"].__name__

                    if classname not in target_documents[station_type]:
                        target_documents[station_type][classname] = []

                    target_documents[station_type][classname].extend(results)

        for station_type, station_type_documents in target_documents.items():
            for interface in self.ACQUISITION_QUERY_DICT[station_type]:
                class_obj = interface["class"]

                linked_acquisitions = linked_documents.get(class_obj.__name__, [])

                target_documents = station_type_documents.get(class_obj.__name__, [])

                yield from self.apply_correlation(
                    ticket,
                    class_obj,
                    linked_acquisitions,
                    target_documents,
                )

    def correlate_products(
        self, ticket: CdsCamsTickets, linked_documents: dict
    ) -> Iterator[Dict[str, Any]]:
        """
        Handle correlation for products and publication.

        Args:
            report (CamsAnomalyCorrelation): raw data
            linked_documents (dict): current impact of the anomaly

        Yields:
            Iterator[typing.Generator]: bulk actions
        """

        for class_obj in self.PRODUCT_IMPACTED:
            self.logger.debug(
                "Correlate %s:  %s - %s",
                class_obj.__name__,
                ticket.products,
                ticket.publications,
            )

            # Search through all publication name combinations
            if ticket.publications:
                results = (
                    class_obj.search()
                    .query()
                    .filter("terms", name=ticket.publications)
                    .params(
                        version=True,
                        seq_no_primary_term=True,
                        size=self.max_products,
                    )
                    .execute()
                )
            else:
                results = []

            linked_products = linked_documents.get(class_obj.__name__, [])

            yield from self.apply_correlation(
                ticket,
                class_obj,
                linked_products,
                results,
            )
