"""Custom consolidated acquisition pass status"""
from opensearchpy import Keyword

from maas_cds.model import generated
from maas_cds.model.anomaly_mixin import AnomalyMixin
from maas_cds.model.timeliness_mixin import TimelinessCalculationMixin
from maas_cds.model.bitrate_mixin import BitrateCalculationMixin

__all__ = [
    "CdsAcquisitionPassStatus",
    "CdsCadipAcquisitionPassStatus",
    "CdsEdrsAcquisitionPassStatus",
]


class CdsAcquisitionPassStatus(
    generated.CdsAcquisitionPassStatus, AnomalyMixin, TimelinessCalculationMixin, BitrateCalculationMixin
):
    """overide to add cams_tickets as a multi keyword"""

    cams_tickets = Keyword(multi=True)

    _TIMELINESS_START_FIELD = "first_frame_start"
    _TIMELINESS_END_FIELD = "stop_delivery"

    _BITRATE_VOLUME = "overall_data_volume"
    _BITRATE_DURATION = "from_acq_delivery_timeliness"


class CdsCadipAcquisitionPassStatus(
    generated.CdsCadipAcquisitionPassStatus, AnomalyMixin, TimelinessCalculationMixin, BitrateCalculationMixin
):
    """overide to add cams_tickets as a multi keyword"""

    cams_tickets = Keyword(multi=True)

    _TIMELINESS_START_FIELD = "downlink_start"
    _TIMELINESS_END_FIELD = "delivery_stop"

    _BITRATE_VOLUME = "TotalVolume"
    _BITRATE_DURATION = "from_acq_delivery_timeliness"

class CdsEdrsAcquisitionPassStatus(
    generated.CdsEdrsAcquisitionPassStatus, AnomalyMixin
):
    """overide to add cams_tickets as a multi keyword"""

    cams_tickets = Keyword(multi=True)
