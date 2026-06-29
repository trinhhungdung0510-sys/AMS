from __future__ import annotations

from unittest.mock import MagicMock

from app.services.dashboard_bootstrap_service import build_dashboard_bootstrap


def test_build_dashboard_bootstrap_shape(monkeypatch):
    db = MagicMock()
    user = MagicMock(
        id="USR-001",
        email="admin@ams.local",
        full_name="Admin",
        role="SUPER_ADMIN",
        farm_id="FARM-001",
        is_active=True,
    )

    db.scalar.side_effect = [3, 2, 1, 10, 4, 2, 0]
    db.scalars.side_effect = [[], [], [], [], [], []]

    monkeypatch.setattr(
        "app.services.dashboard_bootstrap_service.get_atsh_violation_summary",
        lambda _db: {
            "tong_vi_pham_atsh": 0,
            "vi_pham_hom_nay": 0,
            "theo_muc_do": {"INFO": 0, "WARNING": 0, "CRITICAL": 0},
            "top_quy_tac": [],
        },
    )
    monkeypatch.setattr(
        "app.services.dashboard_bootstrap_service.build_dashboard_kpis",
        lambda _db: {"complianceScore": 95},
    )
    monkeypatch.setattr(
        "app.services.dashboard_bootstrap_service.build_top_violations",
        lambda _db, days=7, limit=10: [],
    )
    monkeypatch.setattr(
        "app.services.dashboard_bootstrap_service.get_workflow_dashboard",
        lambda _db: {"vi_pham_hom_nay": 0, "top_quy_trinh_bi_vi_pham": [], "chi_tiet_hom_nay": []},
    )
    monkeypatch.setattr(
        "app.services.dashboard_bootstrap_service.query_events_paginated",
        lambda _db, page=1, limit=100: ([], 0),
    )
    monkeypatch.setattr(
        "app.services.dashboard_bootstrap_service.events_to_engine_dicts",
        lambda _db, _rows: [],
    )
    monkeypatch.setattr(
        "app.services.dashboard_bootstrap_service.build_health_report",
        lambda _db: {"status": "ok"},
    )
    monkeypatch.setattr(
        "app.services.dashboard_bootstrap_service.get_compliance_summary",
        lambda _db, _wid, **kwargs: {
            "workflow_name": "Test",
            "compliance_score": 100,
            "expected_steps": [],
            "compliant_tracks": 0,
            "violation_count": 0,
            "recent_violations": [],
        },
    )
    monkeypatch.setattr(
        "app.services.dashboard_bootstrap_service._list_cameras_for_user",
        lambda _db, _user: [],
    )
    monkeypatch.setattr(
        "app.services.dashboard_bootstrap_service.get_notification_settings",
        lambda _db: {"gmail_connected": True, "gmail_enabled": True},
    )
    monkeypatch.setattr(
        "app.services.dashboard_bootstrap_service.get_pending_gmail_count",
        lambda: 0,
    )

    payload = build_dashboard_bootstrap(db, user)

    assert payload.user.email == "admin@ams.local"
    assert payload.dashboardSummary.tong_camera == 3
    assert payload.complianceSummary.kpis["complianceScore"] == 95
    assert payload.recentEvents.total == 0
    assert payload.systemHealth["status"] == "ok"
    assert payload.notificationSummary.gmail["channel"] == "gmail"
    assert "sentToday" in payload.notificationSummary.gmail
