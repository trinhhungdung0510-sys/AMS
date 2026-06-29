from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services import system_alert_notification_service as service


def test_should_send_alert_respects_cooldown():
    service._alert_sent_at.clear()
    assert service._should_send_alert("camera_offline", "CAM-001") is True
    assert service._should_send_alert("camera_offline", "CAM-001") is False


@patch("app.services.system_alert_notification_service.schedule_system_alert")
def test_handle_camera_status_changed_only_offline(mock_schedule):
    service.handle_camera_status_changed(
        {"data": {"cameraId": "CAM-001", "status": "ONLINE", "lastSeenAt": "now"}}
    )
    mock_schedule.assert_not_called()

    service.handle_camera_status_changed(
        {"data": {"cameraId": "CAM-001", "status": "OFFLINE", "lastSeenAt": "now"}}
    )
    mock_schedule.assert_called_once()
    assert mock_schedule.call_args.kwargs["alert_type"] == "camera_offline"


@patch("app.services.system_alert_notification_service.notify_notification_service_failure")
def test_record_gmail_delivery_outcome_triggers_after_threshold(mock_notify):
    service._consecutive_gmail_failures = 0
    service.record_gmail_delivery_outcome(success=True)
    service.record_gmail_delivery_outcome(success=False, error="timeout")
    service.record_gmail_delivery_outcome(success=False, error="timeout")
    mock_notify.assert_not_called()
    service.record_gmail_delivery_outcome(success=False, error="timeout")
    mock_notify.assert_called_once()


def test_build_system_alert_email_contains_open_ams():
    from app.services.gmail_notification_service import build_system_alert_email_html

    html = build_system_alert_email_html(
        {
            "title": "⚠️ Database không khả dụng",
            "message": "Không kết nối được database.",
            "occurred_at": "2026-06-18T10:00:00+00:00",
            "alert_type": "database_unavailable",
            "ams_url": "http://localhost:5173/bang-dieu-khien",
        }
    )
    assert "Mở AMS" in html
    assert "database_unavailable" in html
