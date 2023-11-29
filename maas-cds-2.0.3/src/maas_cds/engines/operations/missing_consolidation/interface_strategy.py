from abc import ABC, abstractmethod
from maas_cds.lib.parsing_name.parsing_name_s2 import is_compact

from maas_cds.model import (
    AuxipProduct,
    DdProduct,
    LtaProduct,
    PripProduct,
    DasProduct,
    CdsProduct,
    CdsPublication,
)
from maas_model import MAASRawDocument


class InterfaceStrategy(ABC):

    MODEL_CLASS = NotImplemented

    @abstractmethod
    def produce_raw_data_query(self) -> None:
        pass

    @abstractmethod
    def produce_product_query(self) -> None:
        pass

    @abstractmethod
    def produce_publication_query(self) -> None:
        pass


class BaseStrategy(InterfaceStrategy):

    MODEL_CLASS = MAASRawDocument

    SERVICE_TYPE = None

    DD_ATTRS = {}

    def __init__(self, dd_attrs = None) -> None:
        super().__init__()
        self.service_id = None
        self.service_type = self.SERVICE_TYPE
        self.DD_ATTRS = dd_attrs or {}

    def load_interface(self, service_id):
        self.service_id = service_id

    def produce_raw_data_query(self) -> str:
        return f"production_service_type: {self.service_type} AND production_service_name: {self.service_id}"

    def produce_product_query(self) -> str:
        return f"{self.service_type.lower()}_id: *"

    def produce_publication_query(self) -> str:
        return f"service_type: {self.service_type} AND service_id: {self.service_id}"

    def get_product_result(self, products, lookup_field="name"):

        if len(products) == 0:
            return []

        full_query_product = f"{self.produce_product_query()} AND {lookup_field}: ({' OR '.join([i.product_name for i in products])})"

        producted = (
            CdsProduct.search()
            .query(
                "query_string",
                query=full_query_product,
            )
            .params(ignore=404, size=2 * len(products) + 1)
        ).execute()

        return producted

    def get_missing_product_id(self, products):
        producted_name = [i.name for i in self.get_product_result(products)]

        id_not_producted = [
            i.meta.id for i in products if i.product_name not in producted_name
        ]
        return id_not_producted

    def get_publication_result(self, products):

        if len(products) == 0:
            return []

        full_query_publication = f"{self.produce_publication_query()} AND name: ({' OR '.join([i.product_name for i in products])})"
        published = (
            CdsPublication.search()
            .query(
                "query_string",
                query=full_query_publication,
            )
            .params(size=len(products) + 1)
        ).execute()

        return published

    def get_missing_publication_id(self, products):

        published_name = [i.name for i in self.get_publication_result(products)]

        id_not_published = [
            i.meta.id for i in products if i.product_name not in published_name
        ]

        return id_not_published

    def analyse_products_for_service(self, products):

        ids_not_producted = self.get_missing_product_id(products)

        ids_not_published = self.get_missing_publication_id(products)

        return list(set(ids_not_producted + ids_not_published))


class DdStrategy(BaseStrategy):

    SERVICE_TYPE = "DD"

    @property
    def MODEL_CLASS(self):
        config = self.DD_ATTRS.get(self.service_id.split("_")[0])
        return config.get("raw_data_model")

    def produce_raw_data_query(self) -> str:
        return f"production_service_type: {self.service_type} AND interface_name: {self.service_type}_{self.service_id}"

    def produce_product_query(self) -> str:
        config = self.DD_ATTRS.get(self.service_id.split("_")[0])
        return f"{config.get('publication_date')}: *"

    def produce_publication_query(self) -> str:
        return f"service_type: {self.service_type} AND service_id: {self.service_id.split('_')[0]}"

    def get_missing_product_id(self, products):
        config = self.DD_ATTRS.get(self.service_id.split("_")[0])

        product_name_field = config.get("product_name")
        container_name_field = config.get("container_name")

        id_not_producted = []

        # Classic product
        classic_products = [i for i in products if not is_compact(i.product_name)]
        classic_products_name = [
            i.product_name for i in products if not is_compact(i.product_name)
        ]
        if classic_products:

            producted = self.get_product_result(classic_products, product_name_field)
            producted_name = [i[product_name_field] for i in producted]

            id_not_producted_s1_s3 = [
                i.meta.id
                for i in products
                if i.product_name not in producted_name
                and i.product_name in classic_products_name
            ]

            id_not_producted += id_not_producted_s1_s3

        # Container
        container_products = [i for i in products if is_compact(i.product_name)]
        container_product_names = [
            i.product_name for i in products if is_compact(i.product_name)
        ]
        if container_product_names:
            producted = self.get_product_result(
                container_products, container_name_field
            )

            producted_name = [i[container_name_field] for i in producted]

            id_not_producted_s2 = [
                i.meta.id
                for i in products
                if producted_name.count(i.product_name) < 2
                and i.product_name in container_product_names
            ]

            id_not_producted += id_not_producted_s2
        return id_not_producted


class LtaStrategy(BaseStrategy):

    MODEL_CLASS = LtaProduct

    SERVICE_TYPE = "LTA"

    def produce_raw_data_query(self) -> str:
        return f"production_service_type: {self.service_type} AND interface_name: {self.service_type}_{self.service_id}"

    def produce_product_query(self) -> str:
        return f"{self.service_type}_{self.service_id}_is_published: *"

    def produce_publication_query(self) -> str:
        return f"service_type: {self.service_type} AND service_id: {self.service_id.split('_S')[0]}"


class AuxipStrategy(BaseStrategy):

    MODEL_CLASS = AuxipProduct

    SERVICE_TYPE = "AUXIP"


class PripStrategy(BaseStrategy):

    MODEL_CLASS = PripProduct

    SERVICE_TYPE = "PRIP"
