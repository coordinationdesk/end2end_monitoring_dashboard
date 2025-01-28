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
        # Add some default configuration for this replciator engine
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
        """consolidate metrics data

        Args:
            raw_document (MetricsProduct): raw MetricsProduct extracted from metrics api
            document (CdsMetricsProduct): consolidated data

        Returns:
            CdsMetricsProduct: consolided data
        """
        document = super().consolidate(raw_document, document)

        # Expected name pattern
        # "Name": "Archived.WV_RAW__0N.SENTINEL-1.A.size",
        # "Name": "Archived._AUX_CTM_CO.SENTINEL-5P.P.count"",
        # "name": "Download.MSI_L0__DS.SENTINEL-2.A.s2b_ps_cap.size",

        # For S5P DLR :
        # Archived.L2__FRESCO._.size

        splitted_name = raw_document.name.split(".")

        expected_length = {"Archived": 5, "Download": 6}.get(splitted_name[0], 0)

        if len(splitted_name) == expected_length:
            # Ignoring name patterns without product types like "Archived.SENTINEL-1.A.size",

            metric_name = splitted_name[0].lower()
            document.metric_name = metric_name

            document.metric_sub_type = splitted_name[-1]

            full_mission_name = splitted_name[2]
            short_mission_name = (
                # supports "SENTINEL-1.A" & "SENTINEL-5P.P"
                full_mission_name[0]
                + full_mission_name.split("-")[1][0]
            )

            # Product type
            document.product_type = splitted_name[1]

            document.satellite_unit = short_mission_name + splitted_name[3]

            if metric_name == "download":
                document.service_name = splitted_name[4]

            # S1, S2 ...
            document.mission = short_mission_name

            return document

        self.logger.warning(
            "Document name %s is not in the right format : Archived.<productType>.<platformShortName>.<platformerialIdentifier>.<metricType>",
            raw_document.name,
        )

        return None
