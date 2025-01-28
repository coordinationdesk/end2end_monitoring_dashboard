# pylint: skip-file
"""
DA0 classes generated from index templates.

**DO NOT EDIT, ONLY INHERIT !**

Generated date: 2025-01-17T08:13:23.698885

Generated from:
    - /maas-cds/resources/templates/cds-acquisition-pass-status_template.json
    - /maas-cds/resources/templates/cds-cadip-acquisition-pass-status_template.json
    - /maas-cds/resources/templates/cds-cams-tickets_template.json
    - /maas-cds/resources/templates/cds-completeness_template.json
    - /maas-cds/resources/templates/cds-databudget_template.json
    - /maas-cds/resources/templates/cds-dataflow_template.json
    - /maas-cds/resources/templates/cds-datatake_template.json
    - /maas-cds/resources/templates/cds-ddp-data-available_template.json
    - /maas-cds/resources/templates/cds-downlink-datatake_template.json
    - /maas-cds/resources/templates/cds-edrs-acquisition-pass-status_template.json
    - /maas-cds/resources/templates/cds-grafana-usage_template.json
    - /maas-cds/resources/templates/cds-hktm-acquisition-completeness_template.json
    - /maas-cds/resources/templates/cds-hktm-production-completeness_template.json
    - /maas-cds/resources/templates/cds-interface-product-deletion_template.json
    - /maas-cds/resources/templates/cds-interface-status_template.json
    - /maas-cds/resources/templates/cds-lta-download-quota_template.json
    - /maas-cds/resources/templates/cds-metrics-product_template.json
    - /maas-cds/resources/templates/cds-product_template.json
    - /maas-cds/resources/templates/cds-publication_template.json
    - /maas-cds/resources/templates/cds-s2-tilpar_template.json
    - /maas-cds/resources/templates/cds-s3-completeness_template.json
    - /maas-cds/resources/templates/cds-s5-completeness_template.json
    - /maas-cds/resources/templates/cds-sat-unavailability_template.json
    - /maas-cds/resources/templates/maas-config-completeness_template.json
    - /maas-cds/resources/templates/raw-data-app-product_template.json
    - /maas-cds/resources/templates/raw-data-aps-edrs_template.json
    - /maas-cds/resources/templates/raw-data-aps-file_template.json
    - /maas-cds/resources/templates/raw-data-aps-per-pass_template.json
    - /maas-cds/resources/templates/raw-data-aps-product_template.json
    - /maas-cds/resources/templates/raw-data-aps-quality-info_template.json
    - /maas-cds/resources/templates/raw-data-aps-session_template.json
    - /maas-cds/resources/templates/raw-data-auxip-product_template.json
    - /maas-cds/resources/templates/raw-data-cams-anomaly-correlation_template.json
    - /maas-cds/resources/templates/raw-data-cams-cloud-anomaly-correlation_template.json
    - /maas-cds/resources/templates/raw-data-cams-cloud-tickets_template.json
    - /maas-cds/resources/templates/raw-data-cams-tickets_template.json
    - /maas-cds/resources/templates/raw-data-creodias-product_template.json
    - /maas-cds/resources/templates/raw-data-das-product_template.json
    - /maas-cds/resources/templates/raw-data-databudget_template.json
    - /maas-cds/resources/templates/raw-data-dd-archive_template.json
    - /maas-cds/resources/templates/raw-data-dd-product_template.json
    - /maas-cds/resources/templates/raw-data-ddp-data-available_template.json
    - /maas-cds/resources/templates/raw-data-deletion-issue_template.json
    - /maas-cds/resources/templates/raw-data-download-volume-count_template.json
    - /maas-cds/resources/templates/raw-data-grafana-usage_template.json
    - /maas-cds/resources/templates/raw-data-interface-probe_template.json
    - /maas-cds/resources/templates/raw-data-lta-product_template.json
    - /maas-cds/resources/templates/raw-data-metrics-product_template.json
    - /maas-cds/resources/templates/raw-data-mp-all-product_template.json
    - /maas-cds/resources/templates/raw-data-mp-hktm-acquisition-product_template.json
    - /maas-cds/resources/templates/raw-data-mp-hktm-downlink_template.json
    - /maas-cds/resources/templates/raw-data-mp-product_template.json
    - /maas-cds/resources/templates/raw-data-mpcip-product_template.json
    - /maas-cds/resources/templates/raw-data-mpip-product_template.json
    - /maas-cds/resources/templates/raw-data-prip-product_template.json
    - /maas-cds/resources/templates/raw-data-product-deletion_template.json
    - /maas-cds/resources/templates/raw-data-sat-unavailability-product_template.json
"""

from opensearchpy import (
    Boolean,
    Float,
    GeoShape,
    Integer,
    Keyword,
    Long,
    Object,
    Text,
    InnerDoc,
)

from maas_model import MAASDocument, MAASRawDocument, ZuluDate

__all__ = [
    "AppProduct",
    "ApsEdrs",
    "ApsFile",
    "ApsPerPass",
    "ApsProduct",
    "ApsQualityInfo",
    "ApsSession",
    "ApsSessionQualityInfos",
    "AuxipProduct",
    "CamsAnomalyCorrelation",
    "CamsCloudAnomalyCorrelation",
    "CamsCloudTickets",
    "CamsTickets",
    "CdsAcquisitionPassStatus",
    "CdsCadipAcquisitionPassStatus",
    "CdsCadipAcquisitionPassStatusQualityInfos",
    "CdsCamsTickets",
    "CdsCompleteness",
    "CdsCompletenessMissingPeriods",
    "CdsDatabudget",
    "CdsDataflow",
    "CdsDatatake",
    "CdsDatatakeMissingPeriods",
    "CdsDdpDataAvailable",
    "CdsDownlinkDatatake",
    "CdsEdrsAcquisitionPassStatus",
    "CdsGrafanaUsage",
    "CdsHktmAcquisitionCompleteness",
    "CdsHktmProductionCompleteness",
    "CdsInterfaceProductDeletion",
    "CdsInterfaceStatus",
    "CdsLtaDownloadQuota",
    "CdsMetricsProduct",
    "CdsProduct",
    "CdsPublication",
    "CdsS2Tilpar",
    "CdsS3Completeness",
    "CdsS5Completeness",
    "CdsSatUnavailability",
    "CreodiasProduct",
    "DasProduct",
    "Databudget",
    "DdArchive",
    "DdProduct",
    "DdpDataAvailable",
    "DeletionIssue",
    "DownloadVolumeCount",
    "GrafanaUsage",
    "InterfaceProbe",
    "LtaProduct",
    "MaasConfigCompleteness",
    "MetricsProduct",
    "MpAllProduct",
    "MpHktmAcquisitionProduct",
    "MpHktmDownlink",
    "MpProduct",
    "MpcipProduct",
    "MpipProduct",
    "PripProduct",
    "ProductDeletion",
    "SatUnavailabilityProduct",
]


class AppProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-app-product

    Generated from: /maas-cds/resources/templates/raw-data-app-product_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-app-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-app-product-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    acquisition_id = Keyword()

    downlink_duration = Long()

    downlink_orbit = Keyword()

    downlink_start_date = ZuluDate()

    downlink_stop_date = ZuluDate()

    interface_name = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    reportFolder = Keyword()

    satellite_id = Keyword()

    station_id = Keyword()


class ApsEdrs(MAASRawDocument):
    """
    Mapping class for index: raw-data-aps-edrs

    Generated from: /maas-cds/resources/templates/raw-data-aps-edrs_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-aps-edrs"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-aps-edrs-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "product"

    archived_data_size = Float()

    cadus = Long()

    dcsu_archive_status = Keyword()

    disseminated_data = Float()

    dissemination_start = ZuluDate()

    dissemination_stop = ZuluDate()

    doy = Integer()

    edte_acquisition_status = Keyword()

    fer = Long()

    geo_satellite_id = Keyword()

    ground_station = Keyword()

    interface_name = Keyword()

    link_session_id = Keyword()

    mission = Keyword()

    moc_accept_status = Keyword()

    notes = Keyword()

    planned_link_session_start = ZuluDate()

    planned_link_session_stop = ZuluDate()

    production_service_name = Keyword()

    production_service_type = Keyword()

    reportFolder = Keyword()

    report_type = Keyword()

    satellite_id = Keyword()

    sfdap_dissem_status = Keyword()

    spacecraft_execution = Keyword()

    total_status = Keyword()

    uplink_status = Keyword()


class ApsFile(MAASRawDocument):
    """
    Mapping class for index: raw-data-aps-file

    Generated from: /maas-cds/resources/templates/raw-data-aps-file_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-aps-file"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-aps-file-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    block_number = Long()

    channel = Long()

    eviction_date = ZuluDate()

    final_block = Boolean()

    interface_name = Keyword()

    name = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    publication_date = ZuluDate()

    reportFolder = Keyword()

    retransfer = Boolean()

    session_id = Keyword()

    size = Long()


class ApsPerPass(MAASRawDocument):
    """
    Mapping class for index: raw-data-aps-per-pass

    Generated from: /maas-cds/resources/templates/raw-data-aps-per-pass_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-aps-per-pass"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-aps-per-pass-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    acquisition_id = Keyword()

    antenna_id = Keyword()

    comments = Keyword()

    downlink_end_time = ZuluDate()

    downlink_orbit = Keyword()

    downlink_start_time = ZuluDate()

    downlink_status = Keyword()

    fer_data = Float()

    fer_downlink = Float()

    interface_name = Keyword()

    mission = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    reportFolder = Keyword()

    satellite_id = Keyword()

    station_id = Keyword()


class ApsProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-aps-product

    Generated from: /maas-cds/resources/templates/raw-data-aps-product_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-aps-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-aps-product-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    antenna_id = Keyword()

    antenna_status = Keyword()

    delivery_push_status = Keyword()

    downlink_orbit = Keyword()

    doy = Integer()

    fer_data = Float()

    fer_downlink = Float()

    first_frame_start = ZuluDate()

    front_end_id = Keyword()

    front_end_status = Keyword()

    ground_station = Keyword()

    interface_name = Keyword()

    last_frame_stop = ZuluDate()

    mission = Keyword()

    notes = Keyword()

    number_of_chunks = Integer()

    overall_data_volume = Long()

    overall_number_of_bad_data_acquired_frames = Long()

    overall_number_of_bad_downlinked_frames = Long()

    overall_number_of_data_acquired_frames = Long()

    overall_number_of_downlinked_frames = Long()

    planned_data_start = ZuluDate()

    planned_data_stop = ZuluDate()

    production_service_name = Keyword()

    production_service_type = Keyword()

    reportFolder = Keyword()

    report_type = Keyword()

    satellite_id = Keyword()

    start_delivery = ZuluDate()

    stop_delivery = ZuluDate()


class ApsQualityInfo(MAASRawDocument):
    """
    Mapping class for index: raw-data-aps-quality-info

    Generated from: /maas-cds/resources/templates/raw-data-aps-quality-info_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-aps-quality-info"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-aps-quality-info-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    acquired_tfs = Long()

    channel = Long()

    corrected_data_tfs = Long()

    corrected_tfs = Long()

    data_tfs = Long()

    delivery_start = ZuluDate()

    delivery_stop = ZuluDate()

    error_data_tfs = Long()

    error_tfs = Long()

    interface_name = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    reportFolder = Keyword()

    session_id = Keyword()

    total_chunks = Long()

    total_volume = Long()

    uncorrectable_data_tfs = Long()

    uncorrectable_tfs = Long()


class ApsSessionQualityInfos(InnerDoc):
    """
    Inner document class for parent class: ApsSession

    Generated from property: quality_infos
    """

    Channel = Long()

    AcquiredTFs = Long()

    SessionId = Keyword()

    ErrorTFs = Long()

    CorrectedTFs = Long()

    UncorrectableTFs = Long()

    DataTFs = Long()

    ErrorDataTFs = Long()

    CorrectedDataTFs = Long()

    UncorrectableDataTFs = Long()

    DeliveryStart = ZuluDate()

    DeliveryStop = ZuluDate()

    TotalChunks = Long()

    TotalVolume = Long()


class ApsSession(MAASRawDocument):
    """
    Mapping class for index: raw-data-aps-session

    Generated from: /maas-cds/resources/templates/raw-data-aps-session_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-aps-session"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-aps-session-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    acquisition_id = Keyword()

    antenna_id = Keyword()

    antenna_status = Boolean()

    delivery_push_status = Boolean()

    downlink_orbit = Keyword()

    downlink_start = ZuluDate()

    downlink_status = Boolean()

    downlink_stop = ZuluDate()

    front_end_id = Keyword()

    front_end_status = Boolean()

    ground_station = Keyword()

    interface_name = Keyword()

    num_channels = Long()

    planned_data_start = ZuluDate()

    planned_data_stop = ZuluDate()

    production_service_name = Keyword()

    production_service_type = Keyword()

    publication_date = ZuluDate()

    quality_infos = Object(ApsSessionQualityInfos)

    reportFolder = Keyword()

    retransfer = Boolean()

    satellite_id = Keyword()

    session_id = Keyword()

    station_id = Keyword()

    station_unit_id = Keyword()


class AuxipProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-auxip-product

    Generated from: /maas-cds/resources/templates/raw-data-auxip-product_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-auxip-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-auxip-product-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    content_length = Long()

    end_date = ZuluDate()

    eviction_date = ZuluDate()

    interface_name = Keyword()

    origin_date = ZuluDate()

    product_id = Keyword()

    product_name = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    publication_date = ZuluDate()

    reportFolder = Keyword()

    start_date = ZuluDate()


class CamsAnomalyCorrelation(MAASRawDocument):
    """
    Mapping class for index: raw-data-cams-anomaly-correlation

    Generated from: /maas-cds/resources/templates/raw-data-cams-anomaly-correlation_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-cams-anomaly-correlation"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-cams-anomaly-correlation-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    acquisition_pass = Keyword()

    cams_issue = Keyword()

    datatake_ids = Keyword()

    description = Keyword()

    interface_name = Keyword()

    key = Keyword()

    origin = Keyword()

    products = Keyword()

    reportFolder = Keyword()


class CamsCloudAnomalyCorrelation(MAASRawDocument):
    """
    Mapping class for index: raw-data-cams-cloud-anomaly-correlation

    Generated from: /maas-cds/resources/templates/raw-data-cams-cloud-anomaly-correlation_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-cams-cloud-anomaly-correlation"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-cams-cloud-anomaly-correlation-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    created = ZuluDate()

    description = Keyword()

    impacted_observations = Keyword()

    impacted_passes = Keyword()

    interface_name = Keyword()

    issue = Keyword()

    key = Keyword()

    origin = Keyword()

    products = Keyword()

    reportFolder = Keyword()

    satellite_unit = Keyword()

    station = Keyword()

    station_type = Keyword()

    status = Keyword()

    summary = Keyword()

    title = Keyword()

    updated = ZuluDate()


class CamsCloudTickets(MAASRawDocument):
    """
    Mapping class for index: raw-data-cams-cloud-tickets

    Generated from: /maas-cds/resources/templates/raw-data-cams-cloud-tickets_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-cams-cloud-tickets"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-cams-cloud-tickets-")

    _PARTITION_FIELD = "created"

    _PARTITION_FIELD_FORMAT = "static"

    addressed_entities = Keyword()

    affected_systems = Keyword()

    assigned_element = Keyword()

    created = ZuluDate()

    criticality = Keyword()

    entity = Keyword()

    environment = Keyword()

    esa_group = Keyword()

    interface_name = Keyword()

    involved_entities = Keyword()

    key = Keyword()

    linked_issues = Keyword()

    occurence_date = ZuluDate()

    originating_entity = Keyword()

    reportFolder = Keyword()

    reporter = Keyword()

    review_board_dispositions = Keyword()

    status = Keyword()

    title = Keyword()

    updated = ZuluDate()

    urgency = Keyword()


class CamsTickets(MAASRawDocument):
    """
    Mapping class for index: raw-data-cams-tickets

    Generated from: /maas-cds/resources/templates/raw-data-cams-tickets_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-cams-tickets"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-cams-tickets-")

    _PARTITION_FIELD = "created"

    _PARTITION_FIELD_FORMAT = "static"

    affected_systems = Keyword()

    assigned_element = Keyword()

    created = ZuluDate()

    criticality = Keyword()

    entity = Keyword()

    environment = Keyword()

    interface_name = Keyword()

    involved_entities = Keyword()

    key = Keyword()

    linked_issues = Keyword()

    occurence_date = ZuluDate()

    originating_entity = Keyword()

    reportFolder = Keyword()

    reporter = Keyword()

    review_board_dispositions = Keyword()

    status = Keyword()

    title = Keyword()

    updated = ZuluDate()

    urgency = Keyword()


class CdsAcquisitionPassStatus(MAASDocument):
    """
    Mapping class for index: cds-acquisition-pass-status

    Generated from: /maas-cds/resources/templates/cds-acquisition-pass-status_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-acquisition-pass-status"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-acquisition-pass-status-")

    _PARTITION_FIELD = "planned_data_start"

    _PARTITION_FIELD_FORMAT = "static"

    antenna_id = Keyword()

    antenna_status = Keyword()

    cams_description = Keyword()

    cams_origin = Keyword()

    cams_tickets = Keyword()

    delivery_bitrate = Float()

    delivery_push_status = Keyword()

    downlink_orbit = Keyword()

    doy = Integer()

    fer_data = Float()

    fer_downlink = Float()

    first_frame_start = ZuluDate()

    from_acq_delivery_timeliness = Long()

    front_end_id = Keyword()

    front_end_status = Keyword()

    ground_station = Keyword()

    last_attached_ticket = Keyword()

    last_attached_ticket_url = Keyword()

    last_frame_stop = ZuluDate()

    mission = Keyword()

    notes = Text()

    number_of_chunks = Integer()

    overall_data_volume = Long()

    overall_number_of_bad_data_acquired_frames = Long()

    overall_number_of_bad_downlinked_frames = Long()

    overall_number_of_data_acquired_frames = Long()

    overall_number_of_downlinked_frames = Long()

    planned_data_start = ZuluDate()

    planned_data_stop = ZuluDate()

    report_name_daily = Keyword()

    report_name_monthly = Keyword()

    report_name_weekly = Keyword()

    report_type = Keyword()

    satellite_id = Keyword()

    start_delivery = ZuluDate()

    stop_delivery = ZuluDate()

    updateTime = ZuluDate()


class CdsCadipAcquisitionPassStatusQualityInfos(InnerDoc):
    """
    Inner document class for parent class: CdsCadipAcquisitionPassStatus

    Generated from property: quality_infos
    """

    Channel = Long()

    AcquiredTFs = Long()

    SessionId = Keyword()

    ErrorTFs = Long()

    CorrectedTFs = Long()

    UncorrectableTFs = Long()

    DataTFs = Long()

    ErrorDataTFs = Long()

    CorrectedDataTFs = Long()

    UncorrectableDataTFs = Long()

    DeliveryStart = ZuluDate()

    DeliveryStop = ZuluDate()

    TotalChunks = Long()

    TotalVolume = Long()


class CdsCadipAcquisitionPassStatus(MAASDocument):
    """
    Mapping class for index: cds-cadip-acquisition-pass-status

    Generated from: /maas-cds/resources/templates/cds-cadip-acquisition-pass-status_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-cadip-acquisition-pass-status"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-cadip-acquisition-pass-status-")

    _PARTITION_FIELD = "publication_date"

    _PARTITION_FIELD_FORMAT = "static"

    AcquiredTFs = Long()

    CorrectedDataTFs = Long()

    CorrectedTFs = Long()

    DataTFs = Long()

    ErrorDataTFs = Long()

    ErrorTFs = Long()

    TotalChunks = Long()

    TotalVolume = Long()

    UncorrectableDataTFs = Long()

    UncorrectableTFs = Long()

    acquisition_id = Keyword()

    antenna_id = Keyword()

    antenna_status = Boolean()

    cams_description = Keyword()

    cams_origin = Keyword()

    cams_tickets = Keyword()

    delivery_bitrate = Float()

    delivery_push_status = Boolean()

    delivery_start = ZuluDate()

    delivery_stop = ZuluDate()

    downlink_orbit = Keyword()

    downlink_start = ZuluDate()

    downlink_status = Boolean()

    downlink_stop = ZuluDate()

    fer_data = Float()

    from_acq_delivery_timeliness = Long()

    front_end_id = Keyword()

    front_end_status = Boolean()

    global_status = Keyword()

    ground_station = Keyword()

    interface_name = Keyword()

    last_attached_ticket = Keyword()

    last_attached_ticket_url = Keyword()

    mission = Keyword()

    num_channels = Long()

    planned_data_start = ZuluDate()

    planned_data_stop = ZuluDate()

    production_service_name = Keyword()

    production_service_type = Keyword()

    publication_date = ZuluDate()

    quality_infos = Object(CdsCadipAcquisitionPassStatusQualityInfos)

    reportFolder = Keyword()

    retransfer = Boolean()

    satellite_id = Keyword()

    session_id = Keyword()

    station_unit_id = Keyword()

    updateTime = ZuluDate()


class CdsCamsTickets(MAASDocument):
    """
    Mapping class for index: cds-cams-tickets

    Generated from: /maas-cds/resources/templates/cds-cams-tickets_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-cams-tickets"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-cams-tickets-")

    _PARTITION_FIELD = "created"

    _PARTITION_FIELD_FORMAT = "static"

    acquisition_pass = Keyword()

    addressed_entities = Keyword()

    affected_systems = Keyword()

    assigned_element = Keyword()

    correlation_file_id = Keyword()

    created = ZuluDate()

    criticality = Keyword()

    datatake_ids = Keyword()

    description = Keyword()

    entity = Keyword()

    environment = Keyword()

    esa_group = Keyword()

    involved_entities = Keyword()

    key = Keyword()

    linked_issues = Keyword()

    occurence_date = ZuluDate()

    origin = Keyword()

    originating_entity = Keyword()

    products = Keyword()

    publications = Keyword()

    reporter = Keyword()

    review_board_dispositions = Keyword()

    status = Keyword()

    title = Keyword()

    updated = ZuluDate()

    urgency = Keyword()

    url = Keyword()


class CdsCompletenessMissingPeriods(InnerDoc):
    """
    Inner document class for parent class: CdsCompleteness

    Generated from property: missing_periods
    """

    name = Keyword()

    product_type = Keyword()

    sensing_start_date = ZuluDate()

    sensing_end_date = ZuluDate()

    duration = Long()


class CdsCompleteness(
    MAASDocument,
):
    """
    Mapping class for index: cds-completeness

    Generated from: /maas-cds/resources/templates/cds-completeness_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-completeness"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-completeness-")

    _PARTITION_FIELD = ["satellite_unit", "prip_name"]

    _PARTITION_FIELD_FORMAT = "{satellite_unit}-{prip_name}"

    absolute_orbit = Keyword()

    application_date = ZuluDate()

    cams_description = Keyword()

    cams_origin = Keyword()

    cams_tickets = Keyword()

    datastrip_ids = Keyword()

    datatake_id = Keyword()

    hex_datatake_id = Keyword()

    instrument_mode = Keyword()

    instrument_swath = Keyword()

    key = Keyword()

    l0_sensing_duration = Long()

    l0_sensing_time_start = ZuluDate()

    l0_sensing_time_stop = ZuluDate()

    last_attached_ticket = Keyword()

    last_attached_ticket_url = Keyword()

    missing_periods = Object(CdsCompletenessMissingPeriods)

    mission = Keyword()

    name = Keyword()

    number_of_expected_tiles = Integer()

    number_of_scenes = Integer()

    observation_duration = Long()

    observation_time_start = ZuluDate()

    observation_time_stop = ZuluDate()

    polarization = Keyword()

    prip_name = Keyword()

    product_group_ids = Keyword()

    relative_orbit = Keyword()

    satellite_unit = Keyword()

    timeliness = Keyword()

    updateTime = ZuluDate()


class CdsDatabudget(MAASDocument):
    """
    Mapping class for index: cds-databudget

    Generated from: /maas-cds/resources/templates/cds-databudget_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-databudget"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-databudget-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "conf"

    archived = Keyword()

    data_category = Keyword()

    database_timeliness = Keyword()

    database_type = Keyword()

    databudget_type = Keyword()

    disseminated = Keyword()

    level = Keyword()

    mission = Keyword()

    num_day = Keyword()

    produced = Keyword()

    threshold_count = Float()

    threshold_subtype = Keyword()

    threshold_volume = Float()

    timeliness = Keyword()

    version = Keyword()

    volume_day = Float()


class CdsDataflow(MAASDocument):
    """
    Mapping class for index: cds-dataflow

    Generated from: /maas-cds/resources/templates/cds-dataflow_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-dataflow"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-dataflow-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "conf"

    consumed_by = Keyword()

    groups = Keyword()

    instrument = Keyword()

    level = Keyword()

    mission = Keyword()

    mode = Keyword()

    origin_level = Keyword()

    product_type = Keyword()

    published_by = Keyword()

    type = Keyword()


class CdsDatatakeMissingPeriods(InnerDoc):
    """
    Inner document class for parent class: CdsDatatake

    Generated from property: missing_periods
    """

    name = Keyword()

    product_type = Keyword()

    sensing_start_date = ZuluDate()

    sensing_end_date = ZuluDate()

    duration = Long()


class CdsDatatake(MAASDocument):
    """
    Mapping class for index: cds-datatake

    Generated from: /maas-cds/resources/templates/cds-datatake_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-datatake"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-datatake-")

    _PARTITION_FIELD = "observation_time_start"

    _PARTITION_FIELD_FORMAT = "s1-s2"

    absolute_orbit = Keyword()

    application_date = ZuluDate()

    cams_description = Keyword()

    cams_origin = Keyword()

    cams_tickets = Keyword()

    datastrip_ids = Keyword()

    datatake_id = Keyword()

    hex_datatake_id = Keyword()

    instrument_mode = Keyword()

    instrument_swath = Keyword()

    key = Keyword()

    l0_sensing_duration = Long()

    l0_sensing_time_start = ZuluDate()

    l0_sensing_time_stop = ZuluDate()

    last_attached_ticket = Keyword()

    last_attached_ticket_url = Keyword()

    missing_periods = Object(CdsDatatakeMissingPeriods)

    mission = Keyword()

    name = Keyword()

    number_of_expected_tiles = Integer()

    number_of_scenes = Integer()

    observation_duration = Long()

    observation_time_start = ZuluDate()

    observation_time_stop = ZuluDate()

    polarization = Keyword()

    product_group_ids = Keyword()

    relative_orbit = Keyword()

    satellite_unit = Keyword()

    timeliness = Keyword()

    updateTime = ZuluDate()


class CdsDdpDataAvailable(MAASDocument):
    """
    Mapping class for index: cds-ddp-data-available

    Generated from: /maas-cds/resources/templates/cds-ddp-data-available_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-ddp-data-available"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-ddp-data-available-")

    _PARTITION_FIELD = "time_created"

    _PARTITION_FIELD_FORMAT = "static"

    data_size = Long()

    interface_name = Keyword()

    mission = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    satellite_unit = Keyword()

    session_id = Keyword()

    time_created = ZuluDate()

    time_finished = ZuluDate()

    time_start = ZuluDate()

    time_stop = ZuluDate()

    transfer_time = Long()

    updateTime = ZuluDate()


class CdsDownlinkDatatake(MAASDocument):
    """
    Mapping class for index: cds-downlink-datatake

    Generated from: /maas-cds/resources/templates/cds-downlink-datatake_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-downlink-datatake"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-downlink-datatake-")

    _PARTITION_FIELD = "effective_downlink_start"

    _PARTITION_FIELD_FORMAT = "static"

    acquisition_absolute_orbit = Keyword()

    acquisition_relative_orbit = Keyword()

    acquisition_start = ZuluDate()

    acquisition_stop = ZuluDate()

    channel = Keyword()

    datatake_id = Keyword()

    delivery_stop = ZuluDate()

    downlink_absolute_orbit = Keyword()

    downlink_duration = Long()

    downlink_polarization = Keyword()

    effective_downlink_start = ZuluDate()

    effective_downlink_stop = ZuluDate()

    from_sensing_to_delivery_stop_timeliness = Long()

    latency = Long()

    mission = Keyword()

    observation_time_start = ZuluDate()

    partial = Keyword()

    satellite_unit = Keyword()

    session_id = Keyword()

    station = Keyword()

    updateTime = ZuluDate()


class CdsEdrsAcquisitionPassStatus(MAASDocument):
    """
    Mapping class for index: cds-edrs-acquisition-pass-status

    Generated from: /maas-cds/resources/templates/cds-edrs-acquisition-pass-status_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-edrs-acquisition-pass-status"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-edrs-acquisition-pass-status-")

    _PARTITION_FIELD = "planned_link_session_start"

    _PARTITION_FIELD_FORMAT = "product"

    archived_data_size = Float()

    cadus = Long()

    cams_description = Keyword()

    cams_origin = Keyword()

    cams_tickets = Keyword()

    dcsu_archive_status = Keyword()

    disseminated_data = Float()

    dissemination_start = ZuluDate()

    dissemination_stop = ZuluDate()

    doy = Integer()

    edte_acquisition_status = Keyword()

    fer = Long()

    geo_satellite_id = Keyword()

    ground_station = Keyword()

    last_attached_ticket = Keyword()

    last_attached_ticket_url = Keyword()

    link_session_id = Keyword()

    mission = Keyword()

    moc_accept_status = Keyword()

    notes = Keyword()

    planned_link_session_start = ZuluDate()

    planned_link_session_stop = ZuluDate()

    report_name_daily = Keyword()

    report_name_monthly = Keyword()

    report_name_weekly = Keyword()

    report_type = Keyword()

    satellite_id = Keyword()

    sfdap_dissem_status = Keyword()

    spacecraft_execution = Keyword()

    total_status = Keyword()

    updateTime = ZuluDate()

    uplink_status = Keyword()


class CdsGrafanaUsage(MAASDocument):
    """
    Mapping class for index: cds-grafana-usage

    Generated from: /maas-cds/resources/templates/cds-grafana-usage_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-grafana-usage"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-grafana-usage-")

    _PARTITION_FIELD = "access_date"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    access_date = ZuluDate()

    dashboard_title = Keyword()

    dashboard_uid = Keyword()

    interface_name = Keyword()

    user = Keyword()


class CdsHktmAcquisitionCompleteness(MAASDocument):
    """
    Mapping class for index: cds-hktm-acquisition-completeness

    Generated from: /maas-cds/resources/templates/cds-hktm-acquisition-completeness_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-hktm-acquisition-completeness"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-hktm-acquisition-completeness-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    absolute_orbit = Keyword()

    cadip_completeness = Long()

    cams_description = Keyword()

    cams_origin = Keyword()

    cams_tickets = Keyword()

    channel = Long()

    edrs_completeness = Long()

    execution_time = ZuluDate()

    ground_station = Keyword()

    interface_name = Keyword()

    last_attached_ticket = Keyword()

    last_attached_ticket_url = Keyword()

    mission = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    reportFolder = Keyword()

    satellite_unit = Keyword()

    session_id = Keyword()

    session_id_full = Keyword()


class CdsHktmProductionCompleteness(MAASDocument):
    """
    Mapping class for index: cds-hktm-production-completeness

    Generated from: /maas-cds/resources/templates/cds-hktm-production-completeness_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-hktm-production-completeness"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-hktm-production-completeness-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    absolute_orbit = Keyword()

    acquisition_duration = Long()

    acquisition_start = ZuluDate()

    acquisition_stop = ZuluDate()

    completeness = Long()

    datatake_id = Keyword()

    downlink_absolute_orbit = Keyword()

    downlink_duration = Long()

    downlink_execution_time = ZuluDate()

    downlink_start = ZuluDate()

    downlink_stop = ZuluDate()

    effective_downlink_start = ZuluDate()

    effective_downlink_stop = ZuluDate()

    interface_name = Keyword()

    latency = Long()

    mission = Keyword()

    number_of_scenes = Long()

    partial = Keyword()

    reportFolder = Keyword()

    satellite_unit = Keyword()

    station = Keyword()

    x_off = ZuluDate()

    x_on = ZuluDate()


class CdsInterfaceProductDeletion(MAASDocument):
    """
    Mapping class for index: cds-interface-product-deletion

    Generated from: /maas-cds/resources/templates/cds-interface-product-deletion_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-interface-product-deletion"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-interface-product-deletion-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    interface_type = Keyword()

    jira_issue = Keyword()

    product_name = Keyword()


class CdsInterfaceStatus(MAASDocument):
    """
    Mapping class for index: cds-interface-status

    Generated from: /maas-cds/resources/templates/cds-interface-status_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-interface-status"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-interface-status-")

    _PARTITION_FIELD = "status_time_start"

    _PARTITION_FIELD_FORMAT = "monitoring"

    interface_name = Keyword()

    status = Keyword()

    status_duration = Long()

    status_time_start = ZuluDate()

    status_time_stop = ZuluDate()

    updateTime = ZuluDate()


class CdsLtaDownloadQuota(MAASDocument):
    """
    Mapping class for index: cds-lta-download-quota

    Generated from: /maas-cds/resources/templates/cds-lta-download-quota_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-lta-download-quota"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-lta-download-quota-")

    _PARTITION_FIELD = "timestamp"

    _PARTITION_FIELD_FORMAT = "conf"

    daily_download_quota = Long()

    service_name = Keyword()

    timestamp = ZuluDate()


class CdsMetricsProduct(MAASDocument):
    """
    Mapping class for index: cds-metrics-product

    Generated from: /maas-cds/resources/templates/cds-metrics-product_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-metrics-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-metrics-product-")

    _PARTITION_FIELD = "timestamp"

    _PARTITION_FIELD_FORMAT = "%Y"

    counter = Long()

    interface_name = Keyword()

    metric_name = Keyword()

    metric_type = Keyword()

    mission = Keyword()

    name = Keyword()

    product_type = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    satellite_unit = Keyword()

    timestamp = ZuluDate()

    updateTime = ZuluDate()


class CdsProduct(MAASDocument):
    """
    Mapping class for index: cds-product

    Generated from: /maas-cds/resources/templates/cds-product_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-product-")

    _PARTITION_FIELD = "sensing_start_date"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    EU_coverage_percentage = Float()

    absolute_orbit = Keyword()

    auxip_id = Keyword()

    auxip_publication_date = ZuluDate()

    cams_description = Keyword()

    cams_origin = Keyword()

    cams_tickets = Keyword()

    cloud_cover = Float()

    collection_number = Keyword()

    content_length = Long()

    dataflow_status = Keyword()

    datastrip_id = Keyword()

    datatake_id = Keyword()

    ddcreodias_id = Keyword()

    ddcreodias_name = Keyword()

    ddcreodias_publication_date = ZuluDate()

    dddas_id = Keyword()

    dddas_name = Keyword()

    dddas_publication_date = ZuluDate()

    ddip_id = Keyword()

    ddip_name = Keyword()

    ddip_publication_date = ZuluDate()

    detector_id = Keyword()

    expected_lta_number = Integer()

    expected_tiles = Keyword()

    from_prip_ddcreodias_timeliness = Long()

    from_prip_dddas_timeliness = Long()

    from_prip_ddip_timeliness = Long()

    hex_datatake_id = Keyword()

    instrument_mode = Keyword()

    instrument_swath = Keyword()

    key = Keyword()

    last_attached_ticket = Keyword()

    last_attached_ticket_url = Keyword()

    mission = Keyword()

    name = Keyword()

    nb_lta_served = Integer()

    polarization = Keyword()

    prip_id = Keyword()

    prip_publication_date = ZuluDate()

    prip_service = Keyword()

    processor_version = Keyword()

    product_class = Keyword()

    product_discriminator_date = ZuluDate()

    product_granularity = Keyword()

    product_group_id = Keyword()

    product_level = Keyword()

    product_type = Keyword()

    quality_control = Keyword()

    quality_status = Keyword()

    relative_orbit = Keyword()

    satellite_unit = Keyword()

    sensing_duration = Long()

    sensing_end_date = ZuluDate()

    sensing_start_date = ZuluDate()

    site_center = Keyword()

    tile_number = Keyword()

    timeliness = Keyword()

    updateTime = ZuluDate()


class CdsPublication(MAASDocument):
    """
    Mapping class for index: cds-publication

    Generated from: /maas-cds/resources/templates/cds-publication_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-publication"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-publication-")

    _PARTITION_FIELD = "sensing_start_date"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    absolute_orbit = Keyword()

    cams_description = Keyword()

    cams_origin = Keyword()

    cams_tickets = Keyword()

    cloud_cover = Float()

    collection_number = Keyword()

    content_length = Long()

    datastrip_id = Keyword()

    datatake_id = Keyword()

    deletion_cause = Keyword()

    deletion_date = ZuluDate()

    deletion_issue = Keyword()

    eviction_date = ZuluDate()

    expected = Boolean()

    from_sensing_time = Long()

    from_sensing_timeliness = Long()

    hex_datatake_id = Keyword()

    instrument_mode = Keyword()

    instrument_swath = Keyword()

    key = Keyword()

    last_attached_ticket = Keyword()

    last_attached_ticket_url = Keyword()

    mission = Keyword()

    modification_date = ZuluDate()

    name = Keyword()

    origin_date = ZuluDate()

    polarization = Keyword()

    processor_version = Keyword()

    product_class = Keyword()

    product_discriminator_date = ZuluDate()

    product_granularity = Keyword()

    product_group_id = Keyword()

    product_level = Keyword()

    product_type = Keyword()

    product_uuid = Keyword()

    publication_count = Long()

    publication_date = ZuluDate()

    quality_control = Keyword()

    quality_status = Keyword()

    relative_orbit = Keyword()

    satellite_unit = Keyword()

    sensing_duration = Long()

    sensing_end_date = ZuluDate()

    sensing_start_date = ZuluDate()

    service_id = Keyword()

    service_type = Keyword()

    site_center = Keyword()

    tile_number = Keyword()

    timeliness = Keyword()

    transfer_time = Long()

    transfer_timeliness = Long()

    updateTime = ZuluDate()

    within_from_sensing_timeliness = Long()

    within_transfer_timeliness = Long()


class CdsS2Tilpar(MAASDocument):
    """
    Mapping class for index: cds-s2-tilpar

    Generated from: /maas-cds/resources/templates/cds-s2-tilpar_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-s2-tilpar"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-s2-tilpar-")

    _PARTITION_FIELD = "timestamp"

    _PARTITION_FIELD_FORMAT = "tiles"

    geometry = GeoShape()

    name = Keyword()

    timestamp = ZuluDate()


class CdsS3Completeness(MAASDocument):
    """
    Mapping class for index: cds-s3-completeness

    Generated from: /maas-cds/resources/templates/cds-s3-completeness_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-s3-completeness"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-s3-completeness-")

    _PARTITION_FIELD = "observation_time_start"

    _PARTITION_FIELD_FORMAT = "static"

    cams_description = Keyword()

    cams_origin = Keyword()

    cams_tickets = Keyword()

    datatake_id = Keyword()

    expected = Long()

    key = Keyword()

    last_attached_ticket = Keyword()

    last_attached_ticket_url = Keyword()

    mission = Keyword()

    observation_duration = Long()

    observation_time_start = ZuluDate()

    observation_time_stop = ZuluDate()

    percentage = Long()

    product_level = Keyword()

    product_type = Keyword()

    satellite_unit = Keyword()

    status = Keyword()

    timeliness = Keyword()

    updateTime = ZuluDate()

    value = Long()

    value_adjusted = Long()


class CdsS5Completeness(MAASDocument):
    """
    Mapping class for index: cds-s5-completeness

    Generated from: /maas-cds/resources/templates/cds-s5-completeness_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-s5-completeness"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-s5-completeness-")

    _PARTITION_FIELD = "observation_time_start"

    _PARTITION_FIELD_FORMAT = "static"

    absolute_orbit = Keyword()

    cams_description = Keyword()

    cams_origin = Keyword()

    cams_tickets = Keyword()

    datatake_id = Keyword()

    expected = Long()

    key = Keyword()

    last_attached_ticket = Keyword()

    last_attached_ticket_url = Keyword()

    mission = Keyword()

    observation_duration = Long()

    observation_time_start = ZuluDate()

    observation_time_stop = ZuluDate()

    percentage = Long()

    product_level = Keyword()

    product_type = Keyword()

    satellite_unit = Keyword()

    slice_expected = Long()

    slice_value = Long()

    status = Keyword()

    timeliness = Keyword()

    updateTime = ZuluDate()

    value = Long()

    value_adjusted = Long()


class CdsSatUnavailability(MAASDocument):
    """
    Mapping class for index: cds-sat-unavailability

    Generated from: /maas-cds/resources/templates/cds-sat-unavailability_template.json
    """

    class Index:
        "inner class for DSL"
        name = "cds-sat-unavailability"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("cds-sat-unavailability-")

    _PARTITION_FIELD = "start_time"

    _PARTITION_FIELD_FORMAT = "static"

    comment = Keyword()

    end_anx_offset = Integer()

    end_orbit = Keyword()

    end_time = ZuluDate()

    file_name = Keyword()

    key = Keyword()

    mission = Keyword()

    raw_data_ingestion_time = ZuluDate()

    satellite_unit = Keyword()

    start_anx_offset = Integer()

    start_orbit = Keyword()

    start_time = ZuluDate()

    subsystem = Keyword()

    type = Keyword()

    unavailability_duration = Long()

    unavailability_reference = Keyword()

    unavailability_type = Keyword()

    updateTime = ZuluDate()


class CreodiasProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-creodias-product

    Generated from: /maas-cds/resources/templates/raw-data-creodias-product_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-creodias-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-creodias-product-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "%Y"

    content_length = Long()

    end_date = ZuluDate()

    footprint = Keyword()

    ingestion_date = ZuluDate()

    interface_name = Keyword()

    modification_date = ZuluDate()

    online = Boolean()

    origin_date = ZuluDate()

    product_id = Keyword()

    product_name = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    publication_date = ZuluDate()

    reportFolder = Keyword()

    s3_path = Keyword()

    start_date = ZuluDate()


class DasProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-das-product

    Generated from: /maas-cds/resources/templates/raw-data-das-product_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-das-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-das-product-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "%Y"

    content_length = Long()

    end_date = ZuluDate()

    eviction_date = ZuluDate()

    interface_name = Keyword()

    modification_date = ZuluDate()

    origin_date = ZuluDate()

    product_id = Keyword()

    product_name = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    publication_date = ZuluDate()

    start_date = ZuluDate()


class Databudget(MAASRawDocument):
    """
    Mapping class for index: raw-data-databudget

    Generated from: /maas-cds/resources/templates/raw-data-databudget_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-databudget"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-databudget-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "conf"

    archived = Keyword()

    disseminated = Keyword()

    level = Keyword()

    mission = Keyword()

    num_day = Keyword()

    produced = Keyword()

    reportFolder = Keyword()

    timeliness = Keyword()

    type = Keyword()

    version = Keyword()

    volume_day = Keyword()


class DdArchive(MAASRawDocument):
    """
    Mapping class for index: raw-data-dd-archive

    Generated from: /maas-cds/resources/templates/raw-data-dd-archive_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-dd-archive"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-dd-archive-")

    _PARTITION_FIELD = "ingestion_date"

    _PARTITION_FIELD_FORMAT = "%Y"

    content_length = Long()

    end_date = ZuluDate()

    ingestion_date = ZuluDate()

    product_id = Keyword()

    product_name = Keyword()

    reportFolder = Keyword()

    start_date = ZuluDate()


class DdProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-dd-product

    Generated from: /maas-cds/resources/templates/raw-data-dd-product_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-dd-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-dd-product-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "%Y"

    content_length = Long()

    creation_date = ZuluDate()

    end_date = ZuluDate()

    ingestion_date = ZuluDate()

    interface_name = Keyword()

    modification_date = ZuluDate()

    product_id = Keyword()

    product_name = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    reportFolder = Keyword()

    start_date = ZuluDate()


class DdpDataAvailable(MAASRawDocument):
    """
    Mapping class for index: raw-data-ddp-data-available

    Generated from: /maas-cds/resources/templates/raw-data-ddp-data-available_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-ddp-data-available"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-ddp-data-available-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    data_size = Long()

    interface_name = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    reportFolder = Keyword()

    session_id = Keyword()

    time_created = ZuluDate()

    time_finished = ZuluDate()

    time_start = ZuluDate()

    time_stop = ZuluDate()


class DeletionIssue(MAASRawDocument):
    """
    Mapping class for index: raw-data-deletion-issue

    Generated from: /maas-cds/resources/templates/raw-data-deletion-issue_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-deletion-issue"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-deletion-issue-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    deletion_cause = Keyword()

    deletion_date = ZuluDate()

    deletion_interfaces = Keyword()

    interface_name = Keyword()

    interface_type = Keyword()

    key = Keyword()

    reportFolder = Keyword()


class DownloadVolumeCount(MAASRawDocument):
    """
    Mapping class for index: raw-data-download-volume-count

    Generated from: /maas-cds/resources/templates/raw-data-download-volume-count_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-download-volume-count"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-download-volume-count-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "statistics"

    instrument = Keyword()

    interface_name = Keyword()

    mission = Keyword()

    number = Long()

    number_increase = Long()

    reportFolder = Keyword()

    type = Keyword()

    volume = Long()

    volume_increase = Long()


class GrafanaUsage(MAASRawDocument):
    """
    Mapping class for index: raw-data-grafana-usage

    Generated from: /maas-cds/resources/templates/raw-data-grafana-usage_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-grafana-usage"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-grafana-usage-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    access_date = ZuluDate()

    dashboard = Keyword()

    interface_name = Keyword()

    user = Keyword()


class InterfaceProbe(MAASRawDocument):
    """
    Mapping class for index: raw-data-interface-probe

    Generated from: /maas-cds/resources/templates/raw-data-interface-probe_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-interface-probe"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-interface-probe-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "monitoring"

    details = Keyword()

    interface_name = Keyword()

    most_recent_modification_date = ZuluDate()

    probe_duration = Float()

    probe_time_start = ZuluDate()

    probe_time_stop = ZuluDate()

    reportFolder = Keyword()

    status = Keyword()

    status_code = Integer()


class LtaProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-lta-product

    Generated from: /maas-cds/resources/templates/raw-data-lta-product_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-lta-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-lta-product-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    content_length = Long()

    end_date = ZuluDate()

    eviction_date = ZuluDate()

    interface_name = Keyword()

    modification_date = ZuluDate()

    origin_date = ZuluDate()

    product_id = Keyword()

    product_name = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    publication_date = ZuluDate()

    reportFolder = Keyword()

    start_date = ZuluDate()


class MaasConfigCompleteness(MAASDocument):
    """
    Mapping class for index: maas-config-completeness

    Generated from: /maas-cds/resources/templates/maas-config-completeness_template.json
    """

    class Index:
        "inner class for DSL"
        name = "maas-config-completeness"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("maas-config-completeness-")

    _PARTITION_FIELD_FORMAT = "production"

    activated = Boolean()

    end_date = ZuluDate()

    key = Keyword()

    prip_name = Keyword()

    satellite_unit = Keyword()

    start_date = ZuluDate()


class MetricsProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-metrics-product

    Generated from: /maas-cds/resources/templates/raw-data-metrics-product_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-metrics-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-metrics-product-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "%Y"

    counter = Long()

    interface_name = Keyword()

    metric_type = Keyword()

    modification_date = ZuluDate()

    name = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    reportFolder = Keyword()

    timestamp = ZuluDate()


class MpAllProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-mp-all-product

    Generated from: /maas-cds/resources/templates/raw-data-mp-all-product_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-mp-all-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-mp-all-product-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    absolute_orbit = Keyword()

    acquisition_duration = Long()

    acquisition_start = ZuluDate()

    acquisition_stop = ZuluDate()

    channel = Keyword()

    datatake_id = Keyword()

    downlink_absolute_orbit = Keyword()

    downlink_duration = Long()

    downlink_execution_time = ZuluDate()

    downlink_polarization = Keyword()

    effective_downlink_start = ZuluDate()

    effective_downlink_stop = ZuluDate()

    instrument_mode = Keyword()

    interface_name = Keyword()

    latency = Long()

    mission = Keyword()

    number_of_scenes = Integer()

    partial = Keyword()

    polarization = Keyword()

    relative_orbit = Keyword()

    reportFolder = Keyword()

    satellite_id = Keyword()

    session_id = Keyword()

    station = Keyword()

    status = Keyword()

    timeliness = Keyword()


class MpHktmAcquisitionProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-mp-hktm-acquisition-product

    Generated from: /maas-cds/resources/templates/raw-data-mp-hktm-acquisition-product_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-mp-hktm-acquisition-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-mp-hktm-acquisition-product-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    absolute_orbit = Keyword()

    channel = Long()

    execution_time = ZuluDate()

    ground_station = Keyword()

    interface_name = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    reportFolder = Keyword()

    satellite_id = Keyword()

    session_id = Keyword()


class MpHktmDownlink(MAASRawDocument):
    """
    Mapping class for index: raw-data-mp-hktm-downlink

    Generated from: /maas-cds/resources/templates/raw-data-mp-hktm-downlink_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-mp-hktm-downlink"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-mp-hktm-downlink-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    absolute_orbit = Keyword()

    acquisition_duration = Long()

    acquisition_start = ZuluDate()

    acquisition_stop = ZuluDate()

    datatake_id = Keyword()

    downlink_absolute_orbit = Keyword()

    downlink_duration = Long()

    downlink_execution_time = ZuluDate()

    downlink_mode = Keyword()

    downlink_start = ZuluDate()

    downlink_stop = ZuluDate()

    effective_downlink_start = ZuluDate()

    effective_downlink_stop = ZuluDate()

    interface_name = Keyword()

    latency = Long()

    mission = Keyword()

    number_of_scenes = Long()

    partial = Keyword()

    relative_orbit = Keyword()

    reportFolder = Keyword()

    satellite_id = Keyword()

    station = Keyword()

    x_off = ZuluDate()

    x_on = ZuluDate()


class MpProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-mp-product

    Generated from: /maas-cds/resources/templates/raw-data-mp-product_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-mp-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-mp-product-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    absolute_orbit = Keyword()

    datatake_id = Keyword()

    instrument_mode = Keyword()

    instrument_swath = Keyword()

    interface_name = Keyword()

    l0_sensing_duration = Long()

    l0_sensing_time_start = ZuluDate()

    number_of_scenes = Integer()

    observation_duration = Long()

    observation_time_start = ZuluDate()

    observation_time_stop = ZuluDate()

    polarization = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    relative_orbit = Keyword()

    reportFolder = Keyword()

    satellite_id = Keyword()

    timeliness = Keyword()


class MpcipProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-mpcip-product

    Generated from: /maas-cds/resources/templates/raw-data-mpcip-product_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-mpcip-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-mpcip-product-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    content_length = Long()

    end_date = ZuluDate()

    eviction_date = ZuluDate()

    footprint = Keyword()

    interface_name = Keyword()

    origin_date = ZuluDate()

    product_id = Keyword()

    product_name = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    publication_date = ZuluDate()

    reportFolder = Keyword()

    start_date = ZuluDate()


class MpipProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-mpip-product

    Generated from: /maas-cds/resources/templates/raw-data-mpip-product_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-mpip-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-mpip-product-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    ingestion_date = ZuluDate()

    interface_name = Keyword()

    product_name = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    reportFolder = Keyword()

    validity_start_time = ZuluDate()

    validity_stop_time = ZuluDate()


class PripProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-prip-product

    Generated from: /maas-cds/resources/templates/raw-data-prip-product_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-prip-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-prip-product-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "%Y-%m"

    cloud_cover = Float()

    content_length = Long()

    datastrip_id = Keyword()

    end_date = ZuluDate()

    eviction_date = ZuluDate()

    footprint = GeoShape()

    interface_name = Keyword()

    origin_date = ZuluDate()

    product_group_id = Keyword()

    product_id = Keyword()

    product_name = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    publication_date = ZuluDate()

    quality_status = Keyword()

    reportFolder = Keyword()

    start_date = ZuluDate()


class ProductDeletion(MAASRawDocument):
    """
    Mapping class for index: raw-data-product-deletion

    Generated from: /maas-cds/resources/templates/raw-data-product-deletion_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-product-deletion"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-product-deletion-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    interface_type = Keyword()

    product_name = Keyword()

    reportFolder = Keyword()


class SatUnavailabilityProduct(MAASRawDocument):
    """
    Mapping class for index: raw-data-sat-unavailability-product

    Generated from: /maas-cds/resources/templates/raw-data-sat-unavailability-product_template.json
    """

    class Index:
        "inner class for DSL"
        name = "raw-data-sat-unavailability-product"

    @classmethod
    def _matches(cls, hit):
        return hit["_index"].startswith("raw-data-sat-unavailability-product-")

    _PARTITION_FIELD = "ingestionTime"

    _PARTITION_FIELD_FORMAT = "static"

    comment = Keyword()

    end_anx_offset = Integer()

    end_orbit = Keyword()

    end_time = Keyword()

    file_name = Keyword()

    interface_name = Keyword()

    mission = Keyword()

    production_service_name = Keyword()

    production_service_type = Keyword()

    reportFolder = Keyword()

    start_anx_offset = Integer()

    start_orbit = Keyword()

    start_time = Keyword()

    subsystem = Keyword()

    type = Keyword()

    unavailability_reference = Keyword()

    unavailability_type = Keyword()
