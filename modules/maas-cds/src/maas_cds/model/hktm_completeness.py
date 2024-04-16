"""Custom consolidated acquisition pass status"""
from opensearchpy import Keyword

from maas_cds.model import generated

from maas_cds.model.anomaly_mixin import AnomalyMixin

__all__ = [
    "CdsHktmAcquisitionCompleteness",
]


class CdsHktmAcquisitionCompleteness(
    generated.CdsHktmAcquisitionCompleteness, AnomalyMixin
):
    """overide to add cams_tickets as a multi keyword"""

    cams_tickets = Keyword(multi=True)
