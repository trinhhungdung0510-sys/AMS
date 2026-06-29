from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.violation_notification_service import (
    CHANNEL_DASHBOARD,
    CHANNEL_ZALO,
    build_violation_notification_content,
    dispatch_violation_notifications,
    is_atsh_violation_event,
    is_compliance_open_violation,
    is_open_violation_event,
)


def test_is_open_violation_event_only_open():
    assert is_open_violation_event({"status": "OPEN"}) is True
    assert is_open_violation_event({"status": "RESOLVED"}) is False
    assert is_open_violation_event({"status": "IN_PROGRESS"}) is False
    assert is_open_violation_event({"status": "new"}) is True


def test_is_compliance_open_violation_accepts_all_compliance_engine_open():
    assert is_compliance_open_violation(
        {
            "status": "OPEN",
            "category": "compliance_violation",
            "event_type": "NO_HAND_SANITIZE",
            "metadata": {"source": "compliance_engine"},
        }
    )
    assert is_compliance_open_violation(
        {
            "status": "OPEN",
            "category": "compliance_violation",
            "event_type": "WRONG_UNIFORM",
            "metadata": {"source": "compliance_engine", "rule_name": "Sai đồng phục"},
        }
    )
    assert is_compliance_open_violation(
        {
            "status": "OPEN",
            "category": "compliance_violation",
            "event_type": "ANIMAL_INTRUSION",
            "metadata": {"source": "compliance_engine"},
        }
    )


def test_is_compliance_open_violation_rejects_non_compliance():
    assert not is_compliance_open_violation(
        {"status": "OPEN", "category": "workflow_violation", "metadata": {"source": "workflow_engine"}}
    )
    assert not is_compliance_open_violation(
        {"status": "RESOLVED", "category": "compliance_violation", "metadata": {"source": "compliance_engine"}}
    )


def test_is_atsh_violation_event_detects_compliance():
    assert is_atsh_violation_event({"category": "compliance_violation"}) is True
    assert is_atsh_violation_event({"metadata": {"source": "compliance_engine"}}) is True
    assert is_atsh_violation_event({"event_type": "NO_HAND_SANITIZE"}) is True


def test_build_notification_content_contains_required_fields():
    db = MagicMock()
    db.get.return_value = MagicMock(name="AMS Farm Long An")
    event = {
        "id": "EVT-TEST-001",
        "farm_id": "FARM-001",
        "status": "OPEN",
        "camera_name": "Camera 1",
        "zone_name": "Khu sạch",
        "rule_name": "Không sát trùng tay",
        "severity": "HIGH",
        "description": "Test violation",
        "started_at": "2026-06-18T10:00:00+00:00",
    }
    content = build_violation_notification_content(
        db,
        event,
        {"ams_app_url": "http://localhost:5173/vi-pham-atsh"},
    )
    assert "🚨" in content["title"]
    assert "Camera 1" in content["body"]
    assert "Khu sạch" in content["body"]
    assert "EVT-TEST-001" in content["detail_url"]


@patch("app.database.session.SessionLocal")
@patch("app.services.violation_notification_service.schedule_gmail_notification")
@patch("app.services.violation_notification_service.send_zalo_notification")
@patch("app.services.violation_notification_service.send_dashboard_notification")
def test_dispatch_order_and_continue_on_failure(mock_dashboard, mock_zalo, mock_schedule_gmail, mock_session_local):
    db = MagicMock()
    db.get.return_value = None
    db.scalar.return_value = None
    mock_session_local.return_value = db

    mock_dashboard.return_value = MagicMock(channel=CHANNEL_DASHBOARD, status="success", error=None, smtp_latency_ms=None)
    mock_zalo.return_value = MagicMock(channel=CHANNEL_ZALO, status="failed", error="Zalo down", smtp_latency_ms=None)

    with patch("app.services.violation_notification_service._claim_dispatch", return_value=True), patch(
        "app.services.violation_notification_service.get_notification_settings",
        return_value={"gmail_enabled": True, "zalo_enabled": True, "ams_app_url": "http://localhost/vi-pham-atsh"},
    ), patch(
        "app.services.violation_notification_service.build_violation_notification_content",
        return_value={"title": "T", "body": "B", "event_id": "EVT-1", "farm_id": "FARM-001", "severity": "HIGH"},
    ):
        results = dispatch_violation_notifications(
            {
                "id": "EVT-1",
                "farm_id": "FARM-001",
                "status": "OPEN",
                "category": "compliance_violation",
                "event_type": "NO_HAND_SANITIZE",
                "metadata": {"source": "compliance_engine"},
            }
        )

    assert [item.channel for item in results] == [CHANNEL_DASHBOARD, CHANNEL_ZALO]
    assert mock_dashboard.called
    assert mock_zalo.called
    mock_schedule_gmail.assert_called_once()


@patch("app.database.session.SessionLocal")
def test_dispatch_sends_for_compliance_open_violation(mock_session_local):
    event = {
        "id": "EVT-COMP-001",
        "farm_id": "FARM-001",
        "status": "OPEN",
        "category": "compliance_violation",
        "event_type": "WRONG_UNIFORM",
        "metadata": {"source": "compliance_engine", "rule_name": "Sai đồng phục"},
    }

    with patch(
        "app.services.violation_notification_service.schedule_gmail_notification"
    ) as schedule_mock, patch(
        "app.services.violation_notification_service.send_dashboard_notification",
        return_value=MagicMock(channel="dashboard", status="success", error=None, smtp_latency_ms=None),
    ), patch(
        "app.services.violation_notification_service.send_zalo_notification",
        return_value=MagicMock(channel="zalo", status="skipped", error=None, smtp_latency_ms=None),
    ), patch(
        "app.services.violation_notification_service._claim_dispatch",
        return_value=True,
    ), patch(
        "app.services.violation_notification_service.get_notification_settings",
        return_value={"gmail_enabled": True, "zalo_enabled": True, "ams_app_url": "http://localhost/vi-pham-atsh"},
    ), patch(
        "app.services.violation_notification_service.build_violation_notification_content",
        return_value={
            "title": "T",
            "body": "B",
            "event_id": "EVT-COMP-001",
            "farm_id": "FARM-001",
            "severity": "HIGH",
            "description": "Sai đồng phục",
        },
    ):
        db = MagicMock()
        db.get.return_value = None
        db.scalar.return_value = None
        mock_session_local.return_value = db
        results = dispatch_violation_notifications(event)

    assert len(results) >= 1
    schedule_mock.assert_called_once()


def test_dispatch_skips_non_compliance_violation():
    results = dispatch_violation_notifications(
        {
            "id": "EVT-WF-001",
            "status": "OPEN",
            "category": "workflow_violation",
            "metadata": {"source": "workflow_engine"},
        }
    )
    assert results == []


@patch("app.database.session.SessionLocal")
def test_dispatch_skips_duplicate_event(mock_session_local):
    db = MagicMock()
    db.get.return_value = MagicMock(event_id="EVT-DUP")
    mock_session_local.return_value = db

    results = dispatch_violation_notifications(
        {
            "id": "EVT-DUP",
            "status": "OPEN",
            "category": "compliance_violation",
            "metadata": {"source": "compliance_engine"},
        }
    )
    assert results == []


@patch("app.services.violation_notification_service.time.sleep")
@patch("app.services.violation_notification_service.send_gmail_notification")
def test_send_gmail_notification_with_retry(mock_send, mock_sleep):
    from app.services.violation_notification_service import (
        CHANNEL_GMAIL,
        send_gmail_notification_with_retry,
    )

    mock_send.side_effect = [
        MagicMock(channel=CHANNEL_GMAIL, status="failed", error="timeout", smtp_latency_ms=10),
        MagicMock(channel=CHANNEL_GMAIL, status="failed", error="timeout", smtp_latency_ms=10),
        MagicMock(channel=CHANNEL_GMAIL, status="success", error=None, smtp_latency_ms=12),
    ]

    result = send_gmail_notification_with_retry({"title": "T"}, {"gmail_connected": True})

    assert result.status == "success"
    assert mock_send.call_count == 3
    assert mock_sleep.call_count == 2
    mock_sleep.assert_called_with(30)
