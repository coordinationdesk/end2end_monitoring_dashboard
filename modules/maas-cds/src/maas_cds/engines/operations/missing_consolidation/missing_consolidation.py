"""missing consolidation engine"""

import dataclasses
from maas_engine.engine.query import QueryEngine

from maas_model import MAASQueryMessage
from maas_cds.engines.operations.missing_consolidation import INTERFACE_STRATEGY_DICT


@dataclasses.dataclass
class MAASMissingConsolidationMessage(MAASQueryMessage):
    """Custom message model to run MissingConsolidationEngine"""

    service_types: list = None

    service_ids: list = None

    product_check: bool = True

    publication_check: bool = True


class MissingConsolidationEngine(QueryEngine):
    """Class for Missing Consolidation Engine base on QueryEngine

    This engine allow us to retrieve some raw-data that have not been
    consolidated into cds-publication or cds-product
    """

    ENGINE_ID = "MISSING_CONSOLIDATION"

    BUFFER_SIZE = 500

    PAYLOAD_MODEL = MAASMissingConsolidationMessage

    DEFAULT_INTERFACE_DICT_PER_TYPE = {
        "LTA": [
            "CloudFerro",
            "Werum",
            "Acri",
            "S5P_DLR",
            "Exprivia_S1",
            "Exprivia_S2",
            "Exprivia_S3",
        ],
        "PRIP": [
            "S1A-Serco",
            "S1B-DLR",
            "S2_REPRO",
            "S2A-ATOS",
            "S2B-CAPGEMINI",
            "S3A-ACRI",
            "S3B-SERCO",
            "S5P_DLR",
        ],
        "DD": ["DHUS", "DHUS_S5P", "DAS", "CREODIAS"],
        "AUXIP": ["Exprivia"],
    }

    def __init__(self, args=None, send_reports=True, chunk_size=128, dd_attrs = None):
        super().__init__(args, send_reports, chunk_size)
        self.dd_attrs = dd_attrs or {}

    @staticmethod
    def filter_interface_dict(service_types=None, service_ids=None):
        """Filter the default interface dict by service_type or service_id

        Limitation:
            Can't cross filter by service_type and service_id
            service_types=["LTA", "PRIP"]
            service_ids=["Werum", "S1B-DLR"]

        Example 1 (default behaviour):
            No filter
            service_types=None
            service_ids=None

        Example 2:
            Filter two services_ids
            service_types=["LTA"]
            service_ids=["Werum", "Acri"]

        Example 3:
            Filter two services_types
            service_types=["LTA", "PRIP"]
            service_ids=None

        Args:
            service_types (str, optional): _description_. Defaults to None.
            service_ids (str, optional): _description_. Defaults to None.

        Returns:
            dict: _description_
        """
        # default: all interface (Example 1)
        if service_types is None and service_ids is None:
            return MissingConsolidationEngine.DEFAULT_INTERFACE_DICT_PER_TYPE

        # one service and multi service_ids (Example 2) and check existence of both
        if (
            service_types is not None
            and len(service_types) == 1
            and isinstance(service_ids, list)
            and service_types[0]
            in MissingConsolidationEngine.DEFAULT_INTERFACE_DICT_PER_TYPE
            and all(
                service_id
                in MissingConsolidationEngine.DEFAULT_INTERFACE_DICT_PER_TYPE[
                    service_types[0]
                ]
                for service_id in service_ids
            )
        ):
            return {service_types[0]: service_ids}

        # multi service and all of their service_ids (Example 3)
        if (
            service_types is not None
            and service_ids is None
            and all(
                service_type
                in MissingConsolidationEngine.DEFAULT_INTERFACE_DICT_PER_TYPE
                for service_type in service_types
            )
        ):
            return {
                service_type: MissingConsolidationEngine.DEFAULT_INTERFACE_DICT_PER_TYPE[
                    service_type
                ]
                for service_type in service_types
            }

        raise ValueError(
            f"Wrong parameters can't filter with {service_types} and {service_ids}"
        )

    def process_buffer(self, interface_query_builder, products_buffer):
        """Process the given products list to verify with the given query builder,
        if all products was consolidated

        Args:
            interface_query_builder (_type_): interface that provide some prepared
                query abstract by method
            products_buffer (list): a list of product
        """

        missing_raw_product_ids = interface_query_builder.analyse_products_for_service(
            products_buffer
        )

        self.logger.info(
            "Retrieve %s missing consolidation",
            len(missing_raw_product_ids),
        )
        self.logger.debug("Missing ids : %s", missing_raw_product_ids)

        missing_documents = [
            document
            for document in products_buffer
            if document.meta.id in missing_raw_product_ids
        ]

        for document in missing_documents:
            self._push_report_data(document, "created")

    def flush_report_cache(self):
        for report in self._generate_reports():
            self.reports.append(report)
            yield report

        # purge report data to avoid duplciate reiteration on generate_reports
        self._report_data = {}

    def run(self, routing_key: str, payload: MAASMissingConsolidationMessage):
        """override run method data engine"""

        interfaces_to_inspect_dict = self.filter_interface_dict(
            service_types=payload.service_types, service_ids=payload.service_ids
        )

        for interface_type, interface_ids in interfaces_to_inspect_dict.items():

            interface_query_builder = INTERFACE_STRATEGY_DICT.get(interface_type)(self.dd_attrs)

            for interface_id in interface_ids:

                self.logger.info("[INTERFACE] - %s : %s", interface_type, interface_id)

                interface_query_builder.load_interface(interface_id)

                full_raw_query = f"{interface_query_builder.produce_raw_data_query()} AND {payload.query_string}"

                interface_query = (
                    interface_query_builder.MODEL_CLASS.search()
                    .query("query_string", query=full_raw_query)
                    .params(ignore=404)
                )

                self.logger.debug("[RAW-QUERY] - %s", interface_query)

                count = interface_query.count()
                self.logger.info("Matched raw %s entities", count)

                products_buffer = []
                for product in interface_query.scan():

                    products_buffer.append(product)

                    if len(products_buffer) < self.BUFFER_SIZE:
                        continue

                    self.process_buffer(interface_query_builder, products_buffer)
                    products_buffer = []

                    # yield reports so they can be emitted on the bus run on the river
                    self.flush_report_cache()

                self.process_buffer(interface_query_builder, products_buffer)
                # finally yield remaining reports
                self.flush_report_cache()
