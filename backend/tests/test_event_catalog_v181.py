from __future__ import annotations

from unittest.mock import MagicMock, patch

from app.events.event_catalog import (
    build_event_explanation,
    enrich_event_fields,
    normalize_event_type,
    resolve_event_classification,
    resolve_event_severity,
)
from app.services.compliance_report_service import build_dashboard_kpis, build_top_violations


def test_normalize_process_violation_alias():
    assert normalize_event_type("PROCESS_VIOLATION") == "BIOSECURITY_PROCESS_VIOLATION"


def test_uniform_violation_classification_and_severity():
    assert resolve_event_classification("UNIFORM_VIOLATION") == "BIOSECURITY"
    assert resolve_event_severity("UNIFORM_VIOLATION") == "MEDIUM"


def test_animal_intrusion_classification():
    assert resolve_event_classification("ANIMAL_INTRUSION") == "ANIMAL"
    assert resolve_event_severity("ANIMAL_INTRUSION") == "HIGH"


def test_process_violation_is_critical():
    assert resolve_event_severity("BIOSECURITY_PROCESS_VIOLATION") == "CRITICAL"


def test_camera_offline_is_system():
    assert resolve_event_classification("CAMERA_OFFLINE") == "SYSTEM"


def test_explanation_has_required_fields():
    explanation = build_event_explanation("UNIFORM_VIOLATION")
    assert explanation["title"]
    assert explanation["description"]
    assert explanation["recommendedAction"]


def test_enrich_event_fields_payload():
    payload = enrich_event_fields(
        event_type="ZONE_INTRUSION",
        category="compliance_violation",
        severity="high",
        zone_name="Chuồng nái bầu",
    )
    assert payload["classification"] == "BIOSECURITY"
    assert payload["severity"] == "HIGH"
    assert payload["title"]
    assert payload["recommendedAction"]


def test_build_dashboard_kpis_with_mock_db():
    db = MagicMock()
    with patch("app.services.compliance_report_service.query_events_all", return_value=[]):
        kpis = build_dashboard_kpis(db)
    assert kpis["totalViolationsToday"] == 0
    assert kpis["complianceScore"] == 100


def test_build_top_violations_with_mock_db():
    db = MagicMock()
    with patch("app.services.compliance_report_service.query_events_all", return_value=[]):
        items = build_top_violations(db, days=7, limit=10)
    assert items == []
