"""Product consolidation"""

from maas_engine.engine.replicate import ReplicatorEngine
from maas_cds.model import CdsMetricsProduct, MetricsProduct
from typing import Union


class MetricsProductConsolidatorEngine(ReplicatorEngine):
    """Consolidate cds ddp data available"""

    ENGINE_ID = "CONSOLIDATE_METRICS_PRODUCT"

    CONSOLIDATED_MODEL = CdsMetricsProduct

    def __init__(
        self,
        args=None,
        send_reports=False,
        min_doi=None,
        target_model=None,
        exclude_fields=None,
        include_fields=None,
    ):
        if include_fields is None:
            include_fields = [
                "name",
                "interface_name",
                "production_service_name",
                "production_service_type",
                "timestamp",
                "counter",
                "metric_type",
            ]
        if exclude_fields is None:
            exclude_fields = [
                "reportName",
            ]
        super().__init__(
            args,
            target_model=target_model,
            include_fields=include_fields,
            exclude_fields=exclude_fields,
            send_reports=send_reports,
            min_doi=min_doi,
        )

    def get_consolidated_id(self, raw_document: MetricsProduct):
        return raw_document.meta.id

    def consolidate(
        self, raw_document: MetricsProduct, document: CdsMetricsProduct
    ) -> Union[CdsMetricsProduct, None]:
        """consolidate ddp data available

        Args:
            raw_document (MetricsProduct): raw MetricsProduct extracted from DSIB files
            document (CdsMetricsProduct): consolidated data

        Returns:
            CdsMetricsProduct: consolided data
        """
        document = super().consolidate(raw_document, document)

        # Expected name pattern
        # "Name": "Archived.WV_RAW__0N.SENTINEL-1.A.size",

        # For S5P DLR :
        # Archived.L2__FRESCO._.size

        splitted_name = raw_document.name.split(".")

        if len(splitted_name) == 5:
            # Ignoring name patterns without product types like "Archived.SENTINEL-1.A.size",

            document.metric_sub_type = splitted_name[-1]

            full_mission_name = splitted_name[2]

            # WV_RAW__0N
            document.product_type = splitted_name[1]

            # S1B / S1A
            document.satellite_unit = (
                full_mission_name[0] + full_mission_name[-1] + splitted_name[-2]
            )

            # S1, S2 ...
            document.mission = document.satellite_unit[:-1]

            return document

        if (
            raw_document.production_service_name == "S5P_DLR"
            and splitted_name[1] != "SENTINEL-5P"
        ):
            document.mission = "S5"

            document.satellite_unit = "S5P"

            document.product_type = splitted_name[1]

            document.metric_sub_type = splitted_name[-1]

            return document

        self.logger.warning(
            "Document name %s is not in the right format : Archived.<productType>.<platformShortName>.<platformerialIdentifier>.<metricType>",
            raw_document.name,
        )

        return None
