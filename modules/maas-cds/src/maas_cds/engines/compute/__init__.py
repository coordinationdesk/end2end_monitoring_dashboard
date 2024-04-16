"""Package for compute engines"""
from maas_cds.engines.compute.compute_completeness import ComputeCompletenessEngine
from maas_cds.engines.compute.compute_datatake_related import (
    ComputeDatatakeRelatedEngine,
)
from maas_cds.engines.compute.compute_container_related import (
    ComputeContainerRelatedEngine,
)

from maas_cds.engines.compute.compute_container_products import (
    ComputeContainerProductsEngine,
)

from maas_cds.engines.compute.compute_s3_completeness import (
    ComputeS3CompletenessEngine,
)
from maas_cds.engines.compute.compute_s5_completeness import (
    ComputeS5CompletenessEngine,
)
from maas_cds.engines.compute.compute_cams_references import ComputeCamsReferencesEngine

from maas_cds.engines.compute.compute_hktm_related import CdsHktmProductionCompleteness

from maas_cds.engines.compute.correlate_acquisitions import (
    CorrelateAcquisitionsEngine,
)
