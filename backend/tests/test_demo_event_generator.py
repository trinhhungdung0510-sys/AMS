from __future__ import annotations

from unittest.mock import MagicMock, patch

from app.services.demo_event_generator import DemoEventGenerator, demo_event_generator


def test_demo_event_generator_compliance_targets():
    generator = DemoEventGenerator()
    assert generator.current_compliance_score() == 85
    generator._rotate_compliance_target()
    assert generator.current_compliance_score() == 90
    generator._rotate_compliance_target()
    assert generator.current_compliance_score() == 95


def test_build_dashboard_kpis_demo_override():
    from app.services.compliance_report_service import build_dashboard_kpis

    db = MagicMock()
    with patch("app.services.compliance_report_service.query_events_all", return_value=[]):
        with patch("app.services.demo_mode_service.is_demo_mode", return_value=True):
            with patch("app.services.demo_event_generator.demo_event_generator") as mock_generator:
                mock_generator.is_running = True
                mock_generator.current_compliance_score.return_value = 90
                kpis = build_dashboard_kpis(db)
    assert kpis["complianceScore"] == 90


def test_demo_event_generator_singleton():
    assert demo_event_generator is not None
    assert hasattr(demo_event_generator, "start")
    assert hasattr(demo_event_generator, "stop")
