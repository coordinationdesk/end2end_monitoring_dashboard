from maas_cds.engines.reports.anomaly_correlation_file import (
    ConsolidateAnomalyCorrelationFileEngine,
)
from maas_cds.model import CamsCloudAnomalyCorrelation, CdsCamsTickets


def test_cams_cloud_ticket_created_before():
    report = CamsCloudAnomalyCorrelation(
        **{
            "reportName": "Jira_CAMS_Cloud_Anomaly_Correlation_20240207_142434086673_1.json",
            "created": "2024-02-01T03:18:38.354Z",
            "description": "Missing S2A datatstrip data due to antenna acquisition issue at Svalbard Station",
            "impacted_passes": ["44974"],
            "impacted_observations": ["S2A-44973-3"],
            "issue": "GSANOM-14445",
            "key": "AN-192",
            "origin": "Acquisition",
            "summary": "GSANOM-14445 - anomaly correlation",
            "sattelite_unit": "S2A",
            "station_type": "X-Band",
            "station": "SGS",
            "status": "Done",
            "title": "GSANOM-14445 - anomaly correlation",
            "updated": "2024-02-01T15:20:34.397Z",
            "interface_name": "Jira_CAMS_Cloud_Anomaly_Correlation",
            "ingestionTime": "2024-02-01T22:38:39.185Z",
        }
    )
    report.meta.id = "AN-192"
    report.meta.index = "raw-data-cams-cloud-anomaly-correlation-static"
    report.full_clean()

    ticket = CdsCamsTickets(
        **{
            "created": "2024-02-01T03:18:31.763Z",
            "occurence_date": "2024-02-01T03:00:00.000Z",
            "title": "CGS-SGS: S2A: 44974: Data missing, FER above threshold",
            "url": "https://esa-cams.atlassian.net/browse/GSANOM-14445",
            "datatake_ids": ["S2A-44973-3"],
            "linked_issues": "AN-192",
            "updated": "2024-02-14T14:47:50.207Z",
            "key": "GSANOM-14445",
            "status": "Closed",
            "affected_systems": "S-2",
            "assigned_element": ["ATOS", "ESA S-2", "OMCS", "Svalbard Station"],
            "criticality": "Blocking",
            "entity": "Svalbard Station",
            "involved_entities": ["ATOS", "ESA S-2", "OMCS", "Svalbard Station"],
            "originating_entity": "Svalbard Station",
            "reporter": "sentinel-cams@ksat.no",
            "review_board_dispositions": "Coorddesk(jnschmidt)@2024-02-01: delegated to Svalbard station for investigation",
            "urgency": "Low",
        }
    )
    ticket.meta.id = ""
    ticket.meta.index = ""
    ticket.full_clean()
    engine = ConsolidateAnomalyCorrelationFileEngine()
    engine.consolidate_cams_cloud_ticket(report, ticket)

    assert "origin" in ticket
    assert "description" in ticket
    assert ticket.correlation_file_id == "AN-192"

    assert ticket.acquisition_pass == ["S2A_X-Band_44974_SGS"]


def test_cams_cloud_ticket_created_after_failed():
    report = CamsCloudAnomalyCorrelation(
        **{
            "reportName": "Jira_CAMS_Cloud_Anomaly_Correlation_20240207_142434086673_1.json",
            "created": "2025-02-01T03:18:38.354Z",
            "description": "Missing S2A datatstrip data due to antenna acquisition issue at Svalbard Station",
            "impacted_passes": ["44974"],
            "impacted_observations": ["S2A-44973-3"],
            "issue": "GSANOM-14445",
            "key": "AN-192",
            "origin": "Acquisition",
            "summary": "GSANOM-14445 - anomaly correlation",
            "sattelite_unit": "S2A",
            "station_type": "X-Band",
            "station": "SGS",
            "status": "Done",
            "title": "GSANOM-14445 - anomaly correlation",
            "updated": "2024-02-01T15:20:34.397Z",
            "interface_name": "Jira_CAMS_Cloud_Anomaly_Correlation",
            "ingestionTime": "2024-02-01T22:38:39.185Z",
        }
    )
    report.meta.id = "AN-192"
    report.meta.index = "raw-data-cams-cloud-anomaly-correlation-static"
    report.full_clean()

    ticket = CdsCamsTickets(
        **{
            "created": "2024-02-01T03:18:31.763Z",
            "occurence_date": "2024-02-01T03:00:00.000Z",
            "title": "CGS-SGS: S2A: 44974: Data missing, FER above threshold",
            "url": "https://esa-cams.atlassian.net/browse/GSANOM-14445",
            "datatake_ids": ["S2A-44973-3"],
            "linked_issues": "AN-192",
            "updated": "2024-02-14T14:47:50.207Z",
            "key": "GSANOM-14445",
            "status": "Closed",
            "affected_systems": "S-2",
            "assigned_element": ["ATOS", "ESA S-2", "OMCS", "Svalbard Station"],
            "criticality": "Blocking",
            "entity": "Svalbard Station",
            "involved_entities": ["ATOS", "ESA S-2", "OMCS", "Svalbard Station"],
            "originating_entity": "Svalbard Station",
            "reporter": "sentinel-cams@ksat.no",
            "review_board_dispositions": "Coorddesk(jnschmidt)@2024-02-01: delegated to Svalbard station for investigation",
            "urgency": "Low",
        }
    )
    ticket.meta.id = ""
    ticket.meta.index = ""
    ticket.full_clean()
    engine = ConsolidateAnomalyCorrelationFileEngine()
    engine.consolidate_cams_cloud_ticket(report, ticket)

    assert "origin" in ticket
    assert "description" in ticket
    assert ticket.correlation_file_id == "AN-192"

    assert ticket.acquisition_pass == []


def test_cams_cloud_ticket_created_after_failed():
    report = CamsCloudAnomalyCorrelation(
        **{
            "reportName": "Jira_CAMS_Cloud_Anomaly_Correlation_20240207_142434086673_1.json",
            "created": "2025-02-01T03:18:38.354Z",
            "description": "Missing S2A datatstrip data due to antenna acquisition issue at Svalbard Station",
            "impacted_passes": ["S2A-44974"],
            "impacted_observations": ["S2A-44973-3"],
            "issue": "GSANOM-14445",
            "key": "AN-192",
            "origin": "Acquisition",
            "summary": "GSANOM-14445 - anomaly correlation",
            "sattelite_unit": "S2A",
            "station_type": "X-Band",
            "station": "SGS",
            "status": "Done",
            "title": "GSANOM-14445 - anomaly correlation",
            "updated": "2024-02-01T15:20:34.397Z",
            "interface_name": "Jira_CAMS_Cloud_Anomaly_Correlation",
            "ingestionTime": "2024-02-01T22:38:39.185Z",
        }
    )
    report.meta.id = "AN-192"
    report.meta.index = "raw-data-cams-cloud-anomaly-correlation-static"
    report.full_clean()

    ticket = CdsCamsTickets(
        **{
            "created": "2024-02-01T03:18:31.763Z",
            "occurence_date": "2024-02-01T03:00:00.000Z",
            "title": "CGS-SGS: S2A: 44974: Data missing, FER above threshold",
            "url": "https://esa-cams.atlassian.net/browse/GSANOM-14445",
            "datatake_ids": ["S2A-44973-3"],
            "linked_issues": "AN-192",
            "updated": "2024-02-14T14:47:50.207Z",
            "key": "GSANOM-14445",
            "status": "Closed",
            "affected_systems": "S-2",
            "assigned_element": ["ATOS", "ESA S-2", "OMCS", "Svalbard Station"],
            "criticality": "Blocking",
            "entity": "Svalbard Station",
            "involved_entities": ["ATOS", "ESA S-2", "OMCS", "Svalbard Station"],
            "originating_entity": "Svalbard Station",
            "reporter": "sentinel-cams@ksat.no",
            "review_board_dispositions": "Coorddesk(jnschmidt)@2024-02-01: delegated to Svalbard station for investigation",
            "urgency": "Low",
        }
    )
    ticket.meta.id = ""
    ticket.meta.index = ""
    ticket.full_clean()
    engine = ConsolidateAnomalyCorrelationFileEngine()
    engine.consolidate_cams_cloud_ticket(report, ticket)

    assert "origin" in ticket
    assert "description" in ticket
    assert ticket.correlation_file_id == "AN-192"

    assert ticket.acquisition_pass == ["S2A_X-Band_44974_SGS"]
