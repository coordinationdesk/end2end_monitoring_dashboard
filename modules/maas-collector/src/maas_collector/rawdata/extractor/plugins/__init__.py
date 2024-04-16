"""Plugin package contains custom extractor implementations"""

__all__ = [
    "EISPExtractor",
    "ProductExtractor",
    "SatUnavailabilityExtractor",
    "EDRSApsExtractor",
    "AnomalyCorrelationExtractor",
    "EdrsDdpExtractor",
]

# import custom extractor classes
from .esip import ProductExtractor

from .eisp import EISPExtractor

from .satunavailability import SatUnavailabilityExtractor

from .edrs_aps import EDRSApsExtractor

from .anomaly_correlation import AnomalyCorrelationExtractor

from .edrs_ddp import EdrsDdpExtractor
