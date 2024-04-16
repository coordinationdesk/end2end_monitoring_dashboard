"""Package for consolidation engines"""

from maas_engine.engine.replicate import ReplicatorEngine

from maas_cds.engines.reports.product import ProductConsolidatorEngine
from maas_cds.engines.reports.publication import PublicationConsolidatorEngine
from maas_cds.engines.reports.dd_product import DDProductConsolidatorEngine
from maas_cds.engines.reports.sat_unavailabilty import (
    SatUnavailabilityConsolidatorEngine,
)
from maas_cds.engines.reports.consolidate_mp_file import ConsolidateMpFileEngine

from maas_cds.engines.reports.consolidate_hktm import HktmConsolidatorEngine


from maas_cds.engines.reports.product_deletion import (
    DeletionConsolidatorEngine,
)

from maas_cds.engines.reports.lta_product import LTAProductConsolidatorEngine

from maas_cds.engines.reports.interface_status import InterfaceStatusConsolidatorEngine
from maas_cds.engines.reports.ddp_data_available import (
    DdpDataAvailableConsolidatorEngine,
)
from maas_cds.engines.reports.anomaly_correlation_file import (
    ConsolidateAnomalyCorrelationFileEngine,
)


from maas_cds.engines.reports.acquisition_pass_status import (
    CdsAcquisitionPassStatus,
    CdsCadipAcquisitionPassStatus,
)

from maas_cds.engines.reports.acquisition_pass_status_s5_edrs import (
    EDRSAcquisitionPassStatusConsolidatorEngine,
    S5AcquisitionPassStatusConsolidatorEngine,
)

from maas_cds.engines.reports.metrics_product import MetricsProductConsolidatorEngine
from maas_cds.engines.reports.grafana_usage import GrafanaUsageConsolidatorEngine
from maas_cds.engines.reports.consolidate_databudget import ConsolidateDatabudget
