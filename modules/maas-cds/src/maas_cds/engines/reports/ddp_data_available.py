"""Product consolidation"""

from maas_engine.engine.rawdata import RawDataEngine
from maas_cds.lib.dateutils import get_microseconds_delta
from maas_cds.model import CdsDdpDataAvailable, DdpDataAvailable


class DdpDataAvailableConsolidatorEngine(RawDataEngine):
    """Consolidate cds ddp data available"""

    ENGINE_ID = "CONSOLIDATE_DDP_DATA_AVAILABLE"

    CONSOLIDATED_MODEL = CdsDdpDataAvailable

    def __init__(self, args=None, send_reports=False, min_doi=None):
        super().__init__(args, send_reports=send_reports, min_doi=min_doi)

    def get_consolidated_id(self, raw_document: DdpDataAvailable):
        return raw_document.meta.id

    # consolidate_from_ModelClass
    # pylint: disable=C0103
    def consolidate_from_DdpDataAvailable(
        self, raw_document: DdpDataAvailable, document: CdsDdpDataAvailable
    ) -> CdsDdpDataAvailable:
        """consolidate ddp data available

        Args:
            raw_document (DdpDataAvailable): raw ddpDataAvailable extracted from DSIB files
            document (CdsDdpDataAvailable): consolidated data

        Returns:
            CdsDdpDataAvailable: consolided data
        """
        document.data_size = raw_document.data_size
        document.interface_name = raw_document.interface_name
        document.production_service_name = raw_document.production_service_name
        document.production_service_type = raw_document.production_service_type

        if (
            document.production_service_name == "EDRS_EDIP"
            or raw_document.session_id[4] == "L"
        ):
            # remove the satellite from the session id as it has been artificially added
            # from
            document.session_id = raw_document.session_id[4:]
        else:
            document.session_id = raw_document.session_id

        document.time_created = raw_document.time_created
        document.time_finished = raw_document.time_finished
        document.time_start = raw_document.time_start
        document.time_stop = raw_document.time_stop

        document.mission = raw_document.session_id[0:2]
        document.satellite_unit = raw_document.session_id[0:3]

        document.transfer_time = get_microseconds_delta(
            document.time_start, document.time_finished
        )

        return document
