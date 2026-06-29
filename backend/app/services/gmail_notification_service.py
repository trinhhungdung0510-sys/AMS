from __future__ import annotations

import logging
import mimetypes
import smtplib
import time
import uuid
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path
from typing import Any, Optional
from urllib import request as urlrequest

from sqlalchemy.orm import Session

from app.core.config import get_settings, log_smtp_config_presence, resolve_smtp_credentials
from app.services.violation_notification_service import (
    CHANNEL_GMAIL,
    NOTIFICATION_TITLE,
    ChannelResult,
    build_violation_notification_content,
    get_notification_settings,
    save_notification_settings,
)

logger = logging.getLogger(__name__)

DEFAULT_SMTP_HOST = "smtp.gmail.com"
SMTP_TIMEOUT_SECONDS = 10
BRAND_NAME = "Tín Nghĩa AMS"
BRAND_GREEN = "#15803d"
BRAND_ORANGE = "#ea580c"

# Gmail chỉ phục vụ cảnh báo tức thời — không báo cáo định kỳ / digest.
GMAIL_PURPOSE_VIOLATION = "violation"
GMAIL_PURPOSE_TEST = "test"
GMAIL_PURPOSE_SYSTEM = "system"

SYSTEM_ALERT_TITLE = "⚠️ CẢNH BÁO HỆ THỐNG AMS"


class GmailNotificationError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


@dataclass
class GmailSendResult:
    success: bool
    recipient: str
    error: Optional[str] = None
    smtp_latency_ms: Optional[int] = None


def utc_now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()


def get_smtp_config_from_env() -> dict[str, Any]:
    creds = resolve_smtp_credentials()
    host = (creds.get("host") or "").strip() or DEFAULT_SMTP_HOST
    port = int(creds.get("port") or 587)
    user = (creds.get("user") or "").strip()
    password = creds.get("password") or ""
    log_smtp_config_presence(source="get_smtp_config_from_env")
    if not user or not password:
        raise GmailNotificationError(
            "Thiếu SMTP_USER hoặc SMTP_PASSWORD trong backend/.env. Liên hệ quản trị viên."
        )
    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "sender": user,
    }


def severity_badge(severity: str | None) -> dict[str, str]:
    value = str(severity or "MEDIUM").upper()
    if value in {"HIGH", "CRITICAL"} or "NGHIÊM" in value or "CAO" in value:
        return {"label": "🔴 Cao", "color": "#dc2626", "background": "#fef2f2"}
    if value in {"MEDIUM", "WARNING"} or "TRUNG" in value or "CẢNH" in value:
        return {"label": "🟡 Trung bình", "color": "#ca8a04", "background": "#fefce8"}
    return {"label": "🟢 Thấp", "color": "#16a34a", "background": "#f0fdf4"}


def verify_smtp_connection() -> None:
    smtp = get_smtp_config_from_env()
    try:
        with smtplib.SMTP(smtp["host"], smtp["port"], timeout=SMTP_TIMEOUT_SECONDS) as client:
            client.starttls()
            client.login(smtp["user"], smtp["password"])
    except smtplib.SMTPAuthenticationError as exc:
        raise GmailNotificationError(
            f"Authentication failed — kiểm tra App Password Gmail: {exc}"
        ) from exc
    except Exception as exc:
        raise GmailNotificationError(
            f"Không kết nối SMTP ({smtp['host']}:{smtp['port']}): {exc}"
        ) from exc


def _resolve_snapshot_file(snapshot_url: str | None) -> Path | None:
    if not snapshot_url or snapshot_url.startswith(("http://", "https://")):
        return None
    env = get_settings()
    relative = snapshot_url.lstrip("/")
    candidates = [
        Path(relative),
        Path(env.uploads_root) / relative,
        Path(env.storage_root) / relative,
        Path(env.uploads_root) / Path(relative).name,
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def _download_http_snapshot(snapshot_url: str) -> tuple[bytes, str] | None:
    try:
        with urlrequest.urlopen(snapshot_url, timeout=SMTP_TIMEOUT_SECONDS) as response:
            data = response.read()
            if not data:
                return None
            content_type = response.headers.get_content_type() or "image/jpeg"
            return data, content_type
    except Exception:
        logger.warning("Could not download snapshot URL for email: %s", snapshot_url)
        return None


def _field_row(label: str, value: str | None) -> str:
    return (
        f'<tr>'
        f'<td style="padding:10px 12px;border-bottom:1px solid #e5e7eb;color:#64748b;width:38%;">{label}</td>'
        f'<td style="padding:10px 12px;border-bottom:1px solid #e5e7eb;color:#111827;font-weight:600;">{value or "—"}</td>'
        f'</tr>'
    )


def build_violation_email_html(content: dict[str, Any], *, snapshot_cid: str | None = None) -> str:
    badge = severity_badge(content.get("severity"))
    violation_type = content.get("violation_type") or content.get("rule_name") or "Vi phạm an toàn sinh học"
    if snapshot_cid:
        snapshot_block = (
            '<div style="margin:20px 0;text-align:center;">'
            f'<img src="cid:{snapshot_cid}" alt="Ảnh vi phạm" '
            'style="max-width:100%;border-radius:12px;border:1px solid #e5e7eb;" />'
            "</div>"
        )
    else:
        snapshot_block = (
            '<div style="margin:20px 0;text-align:center;padding:32px;background:#f9fafb;'
            'border-radius:12px;border:1px dashed #d1d5db;color:#64748b;font-size:15px;">'
            "📷 Chưa có hình ảnh."
            "</div>"
        )

    ams_url = content.get("ams_url") or content.get("detail_url")
    return f"""\
<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#f3f4f6;font-family:Arial,sans-serif;color:#111827;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#f3f4f6;padding:24px 0;">
    <tr>
      <td align="center">
        <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="max-width:600px;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 8px 24px rgba(15,23,42,0.08);">
          <tr>
            <td style="background:linear-gradient(135deg,{BRAND_GREEN},{BRAND_ORANGE});padding:24px 28px;color:#fff;">
              <div style="font-size:13px;letter-spacing:0.08em;text-transform:uppercase;opacity:0.92;">AMS</div>
              <div style="font-size:24px;font-weight:700;margin-top:6px;">{BRAND_NAME}</div>
              <div style="font-size:15px;margin-top:10px;">{NOTIFICATION_TITLE}</div>
            </td>
          </tr>
          <tr>
            <td style="padding:24px 28px;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border:1px solid #e5e7eb;border-radius:12px;overflow:hidden;">
                {_field_row("Trang trại", content.get("farm_name"))}
                {_field_row("Camera", content.get("camera_name"))}
                {_field_row("Khu vực", content.get("zone_name"))}
                {_field_row("Thời gian", content.get("occurred_at"))}
                {_field_row("Loại vi phạm", violation_type)}
                <tr>
                  <td style="padding:10px 12px;border-bottom:1px solid #e5e7eb;color:#64748b;">Mức độ</td>
                  <td style="padding:10px 12px;border-bottom:1px solid #e5e7eb;">
                    <span style="display:inline-block;padding:6px 12px;border-radius:999px;background:{badge['background']};color:{badge['color']};font-weight:700;">
                      {badge['label']}
                    </span>
                  </td>
                </tr>
              </table>
              {snapshot_block}
              <div style="margin-top:24px;text-align:center;">
                <a href="{ams_url}" style="display:inline-block;background:{BRAND_ORANGE};color:#fff;padding:14px 28px;border-radius:10px;text-decoration:none;font-weight:700;font-size:15px;">
                  Mở AMS
                </a>
              </div>
            </td>
          </tr>
          <tr>
            <td style="padding:16px 28px 24px;color:#64748b;font-size:12px;text-align:center;background:#fafafa;">
              Tự động gửi bởi {BRAND_NAME}
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def build_violation_email_text(content: dict[str, Any]) -> str:
    badge = severity_badge(content.get("severity"))
    violation_type = content.get("violation_type") or content.get("rule_name") or "Vi phạm an toàn sinh học"
    ams_url = content.get("ams_url") or content.get("detail_url")
    lines = [
        NOTIFICATION_TITLE,
        "",
        f"Trang trại: {content.get('farm_name') or '—'}",
        f"Camera: {content.get('camera_name') or '—'}",
        f"Khu vực: {content.get('zone_name') or '—'}",
        f"Thời gian: {content.get('occurred_at') or '—'}",
        f"Loại vi phạm: {violation_type}",
        f"Mức độ: {badge['label']}",
        "",
        f"Mở AMS: {ams_url}",
    ]
    return "\n".join(lines)


def build_system_alert_email_html(alert: dict[str, Any]) -> str:
    details = alert.get("details") or {}
    detail_rows = ""
    for label, key in (
        ("Camera", "camera_name"),
        ("Mã camera", "camera_id"),
        ("Lỗi", "error"),
        ("Lần lỗi", "failure_count"),
    ):
        value = details.get(key)
        if value not in (None, ""):
            detail_rows += _field_row(label, str(value))

    return f"""\
<!DOCTYPE html>
<html>
<body style="margin:0;padding:0;background:#f3f4f6;font-family:Arial,sans-serif;color:#111827;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#f3f4f6;padding:24px 0;">
    <tr>
      <td align="center">
        <table role="presentation" width="600" cellspacing="0" cellpadding="0" style="max-width:600px;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 8px 24px rgba(15,23,42,0.08);">
          <tr>
            <td style="background:linear-gradient(135deg,{BRAND_ORANGE},#dc2626);padding:24px 28px;color:#fff;">
              <div style="font-size:13px;letter-spacing:0.08em;text-transform:uppercase;opacity:0.92;">AMS</div>
              <div style="font-size:24px;font-weight:700;margin-top:6px;">{BRAND_NAME}</div>
              <div style="font-size:15px;margin-top:10px;">{alert.get('title') or SYSTEM_ALERT_TITLE}</div>
            </td>
          </tr>
          <tr>
            <td style="padding:24px 28px;">
              <p style="margin:0 0 16px;line-height:1.6;color:#334155;">{alert.get('message') or 'Cảnh báo hệ thống nghiêm trọng.'}</p>
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border:1px solid #e5e7eb;border-radius:12px;overflow:hidden;">
                {_field_row("Thời gian", alert.get("occurred_at"))}
                {_field_row("Loại cảnh báo", alert.get("alert_type"))}
                {detail_rows}
              </table>
              <div style="margin-top:24px;text-align:center;">
                <a href="{alert.get('ams_url')}" style="display:inline-block;background:{BRAND_GREEN};color:#fff;padding:14px 28px;border-radius:10px;text-decoration:none;font-weight:700;font-size:15px;">
                  Mở AMS
                </a>
              </div>
            </td>
          </tr>
          <tr>
            <td style="padding:16px 28px 24px;color:#64748b;font-size:12px;text-align:center;background:#fafafa;">
              Tự động gửi bởi {BRAND_NAME}
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def build_system_alert_email_text(alert: dict[str, Any]) -> str:
    lines = [
        alert.get("title") or SYSTEM_ALERT_TITLE,
        "",
        alert.get("message") or "Cảnh báo hệ thống nghiêm trọng.",
        f"Thời gian: {alert.get('occurred_at') or '—'}",
        f"Loại: {alert.get('alert_type') or '—'}",
        "",
        f"Mở AMS: {alert.get('ams_url')}",
    ]
    return "\n".join(lines)


def send_system_alert_gmail(*, recipient: str, alert: dict[str, Any]) -> GmailSendResult:
    subject = alert.get("title") or SYSTEM_ALERT_TITLE
    return _send_html_email(
        recipient=recipient,
        subject=subject,
        plain=build_system_alert_email_text(alert),
        html=build_system_alert_email_html(alert),
    )


def _normalize_smtp_error(exc: Exception) -> str:
    text = str(exc)
    lower = text.lower()
    if "authentication failed" in lower or isinstance(exc, smtplib.SMTPAuthenticationError):
        return f"Authentication failed — kiểm tra App Password Gmail: {text}"
    if "timeout" in lower or "timed out" in lower:
        return f"SMTP timeout ({SMTP_TIMEOUT_SECONDS}s)"
    if "recipient" in lower and "rejected" in lower:
        return f"Recipient rejected: {text}"
    return text


def _send_html_email(
    *,
    recipient: str,
    subject: str,
    plain: str,
    html: str,
    snapshot_bytes: bytes | None = None,
    snapshot_subtype: str = "jpeg",
    snapshot_cid: str | None = None,
) -> GmailSendResult:
    recipient = (recipient or "").strip()
    if not recipient:
        return GmailSendResult(success=False, recipient="", error="Thiếu email người nhận")

    try:
        smtp = get_smtp_config_from_env()
    except GmailNotificationError as exc:
        return GmailSendResult(success=False, recipient=recipient, error=exc.message)

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = smtp["sender"]
    message["To"] = recipient
    message.set_content(plain)
    message.add_alternative(html, subtype="html")

    if snapshot_bytes and snapshot_cid:
        html_part = message.get_payload()[1]
        html_part.make_related()
        html_part.add_related(
            snapshot_bytes,
            maintype="image",
            subtype=snapshot_subtype,
            cid=f"<{snapshot_cid}>",
        )

    started = time.perf_counter()
    try:
        with smtplib.SMTP(smtp["host"], smtp["port"], timeout=SMTP_TIMEOUT_SECONDS) as client:
            client.starttls()
            client.login(smtp["user"], smtp["password"])
            client.send_message(message)
        latency_ms = int((time.perf_counter() - started) * 1000)
        logger.info("[Gmail] Sent to %s via %s in %sms", recipient, smtp["host"], latency_ms)
        return GmailSendResult(success=True, recipient=recipient, smtp_latency_ms=latency_ms)
    except Exception as exc:
        latency_ms = int((time.perf_counter() - started) * 1000)
        logger.exception("Gmail send failed")
        return GmailSendResult(
            success=False,
            recipient=recipient,
            error=_normalize_smtp_error(exc),
            smtp_latency_ms=latency_ms,
        )


def send_gmail_message(*, recipient: str, content: dict[str, Any], subject: str | None = None) -> GmailSendResult:
    recipient = (recipient or "").strip()
    if not recipient:
        return GmailSendResult(success=False, recipient="", error="Thiếu email người nhận")

    content = {**content, "purpose": content.get("purpose") or GMAIL_PURPOSE_VIOLATION}
    snapshot_bytes: bytes | None = None
    snapshot_subtype = "jpeg"
    snapshot_path = _resolve_snapshot_file(content.get("snapshot_url"))
    if snapshot_path is not None:
        snapshot_bytes = snapshot_path.read_bytes()
        guessed = mimetypes.guess_type(str(snapshot_path))[0]
        if guessed and guessed.startswith("image/"):
            snapshot_subtype = guessed.split("/", 1)[1]
    elif str(content.get("snapshot_url") or "").startswith("http"):
        downloaded = _download_http_snapshot(content["snapshot_url"])
        if downloaded:
            snapshot_bytes, content_type = downloaded
            if content_type.startswith("image/"):
                snapshot_subtype = content_type.split("/", 1)[1]

    snapshot_cid = "violation-snapshot" if snapshot_bytes else None
    if not content.get("ams_url"):
        content["ams_url"] = content.get("detail_url")

    return _send_html_email(
        recipient=recipient,
        subject=subject or content.get("title") or NOTIFICATION_TITLE,
        plain=build_violation_email_text(content),
        html=build_violation_email_html(content, snapshot_cid=snapshot_cid),
        snapshot_bytes=snapshot_bytes,
        snapshot_subtype=snapshot_subtype,
        snapshot_cid=snapshot_cid,
    )


def connect_gmail_with_test_email(
    db: Session,
    *,
    gmail_recipient: str,
    updated_by: str | None = None,
) -> dict[str, Any]:
    recipient = (gmail_recipient or "").strip()
    if not recipient or "@" not in recipient:
        raise GmailNotificationError("Vui lòng nhập email nhận cảnh báo hợp lệ")

    verify_smtp_connection()
    settings = get_notification_settings(db)
    test_content = {
        "title": NOTIFICATION_TITLE,
        "farm_name": "AMS — Kiểm tra kết nối",
        "camera_name": "—",
        "zone_name": "—",
        "occurred_at": utc_now_iso(),
        "rule_name": "Email kiểm tra Gmail Notification Service",
        "severity": "MEDIUM",
        "description": "Đây là email xác nhận kết nối Gmail từ AMS Settings.",
        "detail_url": settings.get("ams_app_url") or "http://localhost:5173/vi-pham-atsh",
        "ams_url": settings.get("ams_app_url") or "http://localhost:5173/vi-pham-atsh",
        "snapshot_url": None,
        "video_url": None,
    }
    result = send_gmail_message(
        recipient=recipient,
        content=test_content,
        subject="✓ AMS — Xác nhận kết nối Gmail",
    )
    if not result.success:
        raise GmailNotificationError(result.error or "Không gửi được email kiểm tra")

    return save_notification_settings(
        db,
        {
            "gmail_enabled": True,
            "gmail_recipient": recipient,
            "gmail_connected": True,
        },
        updated_by=updated_by,
    )


def send_violation_gmail_for_event(db: Session, event: dict[str, Any]) -> ChannelResult:
    settings = get_notification_settings(db)
    if not settings.get("gmail_enabled", True):
        return ChannelResult(channel=CHANNEL_GMAIL, status="skipped", error="Gmail disabled")

    recipient = (settings.get("gmail_recipient") or "").strip()
    if not recipient:
        return ChannelResult(
            channel=CHANNEL_GMAIL,
            status="failed",
            error="Chưa cấu hình email nhận cảnh báo. Bấm «Kết nối Gmail» trong Cài đặt.",
        )
    if not settings.get("gmail_connected"):
        return ChannelResult(
            channel=CHANNEL_GMAIL,
            status="failed",
            error="Chưa kết nối Gmail. Bấm «Kết nối Gmail» trong Cài đặt.",
        )

    content = build_violation_notification_content(db, event, settings)
    result = send_gmail_message(recipient=recipient, content=content)
    if result.success:
        return ChannelResult(
            channel=CHANNEL_GMAIL,
            status="success",
            smtp_latency_ms=result.smtp_latency_ms,
        )
    return ChannelResult(
        channel=CHANNEL_GMAIL,
        status="failed",
        error=result.error,
        smtp_latency_ms=result.smtp_latency_ms,
    )


def send_gmail_test(db: Session) -> GmailSendResult:
    settings = get_notification_settings(db)
    recipient = (settings.get("gmail_recipient") or "").strip()
    if not recipient:
        raise GmailNotificationError("Chưa có email nhận cảnh báo. Nhập email và bấm «Kết nối Gmail».")

    event = {
        "id": f"TST-GML-{uuid.uuid4().hex[:8].upper()}",
        "farm_id": "FARM-001",
        "status": "OPEN",
        "category": "compliance_violation",
        "event_type": "NO_HAND_SANITIZE",
        "severity": "HIGH",
        "severityLabel": "Nghiêm trọng",
        "camera_id": "CAM-001",
        "camera_name": "Camera cổng vào",
        "zone_name": "Khu sát trùng tay",
        "rule_name": "Không sát trùng tay",
        "description": "Email thử nghiệm từ AMS Gmail Notification Service.",
        "started_at": utc_now_iso(),
        "metadata": {"source": "compliance_engine", "object_class": "person"},
    }
    content = build_violation_notification_content(db, event, settings)
    return send_gmail_message(recipient=recipient, content=content, subject=NOTIFICATION_TITLE)
