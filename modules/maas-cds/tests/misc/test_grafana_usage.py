import datetime
import hashlib
from maas_cds.engines.reports.grafana_usage import GrafanaUsageConsolidatorEngine
from maas_cds.model import CdsGrafanaUsage, GrafanaUsage
import maas_cds.model


def test_grafana_usage():
    """Check grafana usage consolidation engine"""
    dashboard_id_dict = {"FICTIVE_ID": "TITLE"}
    GrafanaUsageConsolidatorEngine.MODEL_MODULE = maas_cds.model

    engine = GrafanaUsageConsolidatorEngine(
        dashboard_id_dict, target_model="CdsGrafanaUsage"
    )

    raw = GrafanaUsage()
    raw.access_date = datetime.datetime(
        2022, 12, 7, 15, 0, 0, 12345, tzinfo=datetime.timezone.utc
    )
    raw.dashboard = "/api/dashboards/uid/FICTIVE_ID"
    raw.user = "TOTO"
    calculated_id = engine.get_consolidated_id(raw)
    out = CdsGrafanaUsage()
    engine.consolidate(raw, out)

    assert out.access_date == raw.access_date
    assert out.user == raw.user
    assert out.dashboard_title == "TITLE"
    assert out.dashboard_uid == "FICTIVE_ID"

    md5 = hashlib.md5()
    date_without_sub_sec = raw.access_date.replace(microsecond=0)
    md5.update(str(date_without_sub_sec).encode())
    md5.update(str(raw.user).encode())
    md5.update(str(raw.dashboard).encode())
    expected_id = md5.hexdigest()
    assert calculated_id == expected_id


def test_grafana_usage_home_page():
    """Check grafana usage with special home page format"""
    dashboard_id_dict = {
        "GENERIC_UID_1": "TOTO",
        "UID_HOME_PAGE": "Home",
        "GENERIC_UID_2": "TITI",
    }
    GrafanaUsageConsolidatorEngine.MODEL_MODULE = maas_cds.model

    engine = GrafanaUsageConsolidatorEngine(
        dashboard_id_dict, target_model="CdsGrafanaUsage"
    )

    raw = GrafanaUsage()
    raw.access_date = datetime.datetime(
        2022, 12, 7, 15, 0, 0, 12345, tzinfo=datetime.timezone.utc
    )
    raw.dashboard = "/api/dashboards/home"
    raw.user = "RAWUSER"
    out = CdsGrafanaUsage()
    engine.consolidate(raw, out)

    assert out.access_date == raw.access_date
    assert out.user == raw.user
    assert out.dashboard_title == "Home"
    assert out.dashboard_uid == "UID_HOME_PAGE"
