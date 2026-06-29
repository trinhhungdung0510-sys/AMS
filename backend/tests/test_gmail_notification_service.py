from __future__ import annotations

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.gmail_notification_service import (
    GmailNotificationError,
    build_violation_email_html,
    get_smtp_config_from_env,
    send_gmail_message,
    severity_badge,
)


def test_build_violation_email_html_contains_fields_and_button():
    html = build_violation_email_html(
        {
            "farm_name": "AMS Farm Long An",
            "camera_name": "Cam 1",
            "zone_name": "Zone A",
            "occurred_at": "2026-06-18T10:00:00+00:00",
            "violation_type": "Không sát trùng tay",
            "severity": "HIGH",
            "detail_url": "http://localhost:5173/vi-pham-atsh",
        }
    )
    assert "AMS Farm Long An" in html
    assert "Cam 1" in html
    assert "Loại vi phạm" in html
    assert "Không sát trùng tay" in html
    assert "Mở AMS" in html
    assert "Chưa có hình ảnh." in html
    assert "Mã vi phạm" not in html
    assert "EVT-" not in html
    assert "Mô tả" not in html


def test_build_violation_email_html_with_snapshot():
    html = build_violation_email_html(
        {
            "farm_name": "Farm",
            "camera_name": "Cam",
            "zone_name": "Zone",
            "occurred_at": "now",
            "violation_type": "Rule",
            "severity": "LOW",
            "detail_url": "http://localhost",
        },
        snapshot_cid="violation-snapshot",
    )
    assert 'cid:violation-snapshot' in html
    assert "Chưa có hình ảnh." not in html


def test_severity_badge_levels():
    assert severity_badge("HIGH")["label"] == "🔴 Cao"
    assert severity_badge("MEDIUM")["label"] == "🟡 Trung bình"
    assert severity_badge("LOW")["label"] == "🟢 Thấp"


@patch("app.services.gmail_notification_service.resolve_smtp_credentials")
def test_get_smtp_config_from_env_requires_credentials(mock_creds):
    mock_creds.return_value = {
        "host": "smtp.gmail.com",
        "port": 587,
        "user": "",
        "password": "",
    }
    with pytest.raises(GmailNotificationError):
        get_smtp_config_from_env()


@patch("app.services.gmail_notification_service.smtplib.SMTP")
@patch("app.services.gmail_notification_service.get_smtp_config_from_env")
def test_send_gmail_message_success(mock_smtp_config, mock_smtp):
    mock_smtp_config.return_value = {
        "host": "smtp.gmail.com",
        "port": 587,
        "user": "sender@gmail.com",
        "password": "secret",
        "sender": "sender@gmail.com",
    }
    client = MagicMock()
    mock_smtp.return_value.__enter__.return_value = client

    result = send_gmail_message(
        recipient="manager@gmail.com",
        content={
            "title": "Test",
            "event_id": "EVT-1",
            "farm_name": "Farm",
            "camera_name": "Cam",
            "zone_name": "Zone",
            "object_name": "person",
            "occurred_at": "now",
            "rule_name": "Rule",
            "severity": "HIGH",
            "description": "Desc",
            "detail_url": "http://localhost/v/1",
        },
    )
    assert result.success is True
    assert result.recipient == "manager@gmail.com"
    assert result.smtp_latency_ms is not None
    client.starttls.assert_called_once()
    client.login.assert_called_once()
    client.send_message.assert_called_once()
    mock_smtp.assert_called_once()
    assert mock_smtp.call_args.kwargs.get("timeout") == 10
