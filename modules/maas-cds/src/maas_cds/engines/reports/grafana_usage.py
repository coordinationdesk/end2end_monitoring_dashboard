"""Grafana usage consolidation"""

import hashlib
from typing import Union
from maas_engine.engine.replicate import ReplicatorEngine
from maas_cds.model import GrafanaUsage, CdsGrafanaUsage


class GrafanaUsageConsolidatorEngine(ReplicatorEngine):
    """Consolidate grafana usage raw data"""

    ENGINE_ID = "CONSOLIDATE_GRAFANA_USAGE"

    CONSOLIDATED_MODEL = CdsGrafanaUsage

    def __init__(
        self,
        dashboard_id_dict,
        args=None,
        send_reports=False,
        min_doi=None,
        target_model=None,
        exclude_fields=None,
        include_fields=None,
    ):
        if include_fields is None:
            include_fields = [
                "access_date",
                "interface_name",
                "user",
            ]
        if exclude_fields is None:
            exclude_fields = ["reportName", "dashboard"]

        super().__init__(
            args,
            target_model=target_model,
            include_fields=include_fields,
            exclude_fields=exclude_fields,
            send_reports=send_reports,
            min_doi=min_doi,
        )
        self.dashboard_id_dict = dashboard_id_dict

        # Keep track of the home page UID
        home_uid = [
            i for i in self.dashboard_id_dict if self.dashboard_id_dict[i] == "Home"
        ]
        self.home_uid = home_uid[0] if home_uid else ""

    def get_consolidated_id(self, raw_document: GrafanaUsage) -> str:
        """Create a Consolidation ID for the grafana usage raw data
           Grafana generate 2 log for a single access and both logs are in the
           same second so by creating an id which contain the access date
           without the subsecond part we mitigate this issue
        Args:
            raw_document (GrafanaUsage): The raw grafana usage document

        Raises:
            ValueError: Exception raised if field needed to generate the id is
            not present in the raw data

        Returns:
            str: the generated identifier
        """
        for x in ("access_date", "user", "dashboard"):
            if x not in raw_document:
                raise ValueError(f"Field {x} is missing from {raw_document}")

        md5 = hashlib.md5()
        md5.update(str(raw_document.access_date.replace(microsecond=0)).encode())
        md5.update(str(raw_document.user).encode())
        md5.update(str(raw_document.dashboard).encode())
        return md5.hexdigest()

    def consolidate(
        self, raw_document: GrafanaUsage, document: CdsGrafanaUsage
    ) -> Union[CdsGrafanaUsage, None]:
        """Consolidate grafana usage data

        Args:
            raw_document (GrafanaUsage): raw GrafanaUsage extracted from loki
            document (CdsGrafanaUsage): consolidated data

        Returns:
            CdsGrafanaUsage: consolided data
        """
        document = super().consolidate(raw_document, document)

        # Handle Home special case ( it does not respect the /api/dashboards/uid format)
        if raw_document.dashboard == "/api/dashboards/home":
            document.dashboard_title = "Home"
            document.dashboard_uid = self.home_uid

        else:
            # Remove /api/dashboards/uid/ prefix from dashboards name in raw data
            str_id = raw_document.dashboard.replace("/api/dashboards/uid/", "")
            if str_id in self.dashboard_id_dict:
                document.dashboard_title = self.dashboard_id_dict[str_id]
            else:
                document.dashboard_title = str_id

            document.dashboard_uid = str_id
        return document
