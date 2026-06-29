from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.violation_notification_service import (
    CHANNEL_GMAIL,
    mask_settings_for_api,
    send_gmail_notification,
)


def test_mask_settings_for_api_returns_simple_fields_only():
    masked = mask_settings_for_api(
        {
            "gmail_enabled": True,
            "gmail_recipient": "user@example.com",
            "gmail_connected": True,
            "zalo_enabled": True,
            "zalo_connected": False,
            "smtp_host": "smtp.gmail.com",
            "smtp_user": "secret@example.com",
            "smtp_password": "secret",
            "ams_app_url": "http://localhost:5173/vi-pham-atsh",
        }
    )
    assert set(masked.keys()) == {
        "gmail_enabled",
        "gmail_recipient",
        "gmail_sender",
        "gmail_connected",
        "gmail_last_sent_at",
        "gmail_last_status",
        "gmail_last_error",
        "zalo_enabled",
        "zalo_connected",
        "ams_app_url",
    }
    assert masked["gmail_connected"] is True
    assert "smtp_password" not in masked


def test_mask_settings_gmail_connected_requires_explicit_flag():
    masked = mask_settings_for_api(
        {
            "gmail_enabled": True,
            "gmail_recipient": "user@example.com",
            "gmail_connected": False,
            "zalo_enabled": True,
            "zalo_connected": False,
            "smtp_user": "secret@example.com",
            "smtp_password": "secret",
        }
    )
    assert masked["gmail_connected"] is False


def test_gmail_requires_connection_before_send():
    content = {
        "title": "Test",
        "body": "Body",
        "detail_url": "http://localhost/vi-pham-atsh/EVT-1",
    }
    result = send_gmail_notification(
        content,
        {
            "gmail_enabled": True,
            "gmail_recipient": "user@example.com",
            "gmail_connected": False,
        },
    )
    assert result.channel == CHANNEL_GMAIL
    assert result.status == "failed"
    assert "kết nối" in (result.error or "").lower()


def test_ephemeral_event_skips_auto_dispatch():
    from app.services.violation_notification_service import handle_event_created_for_notifications

    with patch("app.services.violation_notification_service.dispatch_violation_notifications") as mocked:
        handle_event_created_for_notifications(
            {
                "data": {
                    "event": {
                        "id": "EPH-TEST001",
                        "status": "OPEN",
                        "category": "compliance_violation",
                        "metadata": {"ephemeral": True, "source": "compliance_engine"},
                    }
                }
            }
        )
        mocked.assert_not_called()


def test_dispatch_schedules_gmail_in_background():
    from app.services.violation_notification_service import dispatch_violation_notifications

    event = {
        "id": "EVT-BGMAIL1",
        "farm_id": "FARM-001",
        "status": "OPEN",
        "category": "compliance_violation",
        "event_type": "NO_HAND_SANITIZE",
        "metadata": {"source": "compliance_engine"},
    }

    with patch("app.database.session.SessionLocal") as mock_session_local, patch(
        "app.services.violation_notification_service.send_dashboard_notification",
        return_value=MagicMock(channel="dashboard", status="success", error=None, smtp_latency_ms=None),
    ), patch(
        "app.services.violation_notification_service.send_zalo_notification",
        return_value=MagicMock(channel="zalo", status="skipped", error="Zalo disabled", smtp_latency_ms=None),
    ), patch(
        "app.services.violation_notification_service.schedule_gmail_notification"
    ) as schedule_mock:
        db = MagicMock()
        db.get.return_value = None
        db.scalar.return_value = None
        mock_session_local.return_value = db

        results = dispatch_violation_notifications(event)
        assert len(results) >= 1
        schedule_mock.assert_called_once()
