from __future__ import annotations

import json
import logging
import threading
import time
import uuid
import asyncio
from dataclasses import dataclass
from typing import Any, Optional
from urllib import error as urlerror
from urllib import request as urlrequest

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import Farm, NotificationDelivery, NotificationDispatch, SystemSetting

logger = logging.getLogger(__name__)

SETTINGS_KEY = "violation_notification_settings"
NOTIFICATION_TITLE = "🚨 CẢNH BÁO VI PHẠM AN TOÀN SINH HỌC"
DEFAULT_SMTP_HOST = "smtp.gmail.com"

CHANNEL_DASHBOARD = "dashboard"
CHANNEL_ZALO = "zalo"
CHANNEL_GMAIL = "gmail"

GMAIL_MAX_ATTEMPTS = 3
GMAIL_RETRY_INTERVAL_SECONDS = 30
ALERT_TYPE_VIOLATION = "violation_alert"

OPEN_STATUSES = {"OPEN", "open", "new", "Mới"}
CLOSED_STATUSES = {"RESOLVED", "DISMISSED", "ACKNOWLEDGED", "IN_PROGRESS"}

_pending_gmail_lock = threading.Lock()
_pending_gmail_count = 0
ATSH_CATEGORIES = {
    "compliance_violation",
    "rule_engine",
    "biosecurity_violation",
    "atsh_violation",
}


@dataclass
class ChannelResult:
    channel: str
    status: str
    error: Optional[str] = None
    smtp_latency_ms: Optional[int] = None


def utc_now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()


def default_notification_settings() -> dict[str, Any]:
    return {
        "gmail_enabled": True,
        "zalo_enabled": True,
        "gmail_recipient": "ops@ams-farm.vn",
        "gmail_from": "ams-alerts@tin-nghia.local",
        "smtp_host": "",
        "smtp_port": 587,
        "smtp_user": "",
        "smtp_password": "",
        "zalo_oa_id": "",
        "zalo_recipient_id": "",
        "zalo_access_token": "",
        "gmail_connected": False,
        "zalo_connected": False,
        "ams_app_url": "http://localhost:5173/vi-pham-atsh",
    }


def resolve_smtp_config(settings: dict[str, Any] | None = None) -> dict[str, Any]:
    """SMTP credentials come from backend/.env only — never from frontend."""
    from app.core.config import resolve_smtp_credentials

    creds = resolve_smtp_credentials()
    host = (creds.get("host") or "").strip() or DEFAULT_SMTP_HOST
    port = int(creds.get("port") or 587)
    user = (creds.get("user") or "").strip()
    password = creds.get("password") or ""
    sender = user or "ams-alerts@local"
    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "sender": sender,
    }


def resolve_zalo_access_token(settings: dict[str, Any]) -> str:
    token = (settings.get("zalo_access_token") or "").strip()
    if token:
        return token
    return (getattr(get_settings(), "zalo_oa_access_token", None) or "").strip()


def resolve_gmail_delivery_status(db: Session) -> dict[str, Any]:
    delivery = db.scalar(
        select(NotificationDelivery)
        .where(NotificationDelivery.channel == CHANNEL_GMAIL)
        .order_by(NotificationDelivery.sent_at.desc())
        .limit(1)
    )
    if delivery is None:
        return {
            "gmail_last_sent_at": None,
            "gmail_last_status": None,
            "gmail_last_error": None,
        }
    return {
        "gmail_last_sent_at": delivery.sent_at,
        "gmail_last_status": delivery.status,
        "gmail_last_error": delivery.error_message if delivery.status == "failed" else None,
    }


def mask_settings_for_api(settings: dict[str, Any], db: Session | None = None) -> dict[str, Any]:
    try:
        from app.services.gmail_notification_service import get_smtp_config_from_env

        smtp_ready = True
        get_smtp_config_from_env()
    except Exception:
        smtp_ready = False
    zalo_ready = bool(
        (settings.get("zalo_recipient_id") or "").strip()
        and (
            (settings.get("zalo_access_token") or "").strip()
            or resolve_zalo_access_token(settings)
        )
        and (
            (settings.get("zalo_oa_id") or "").strip()
            or (getattr(get_settings(), "zalo_oa_id", None) or "").strip()
        )
    )
    gmail_connected = bool(settings.get("gmail_connected"))
    zalo_connected = bool(settings.get("zalo_connected")) or zalo_ready
    gmail_sender = ""
    try:
        from app.core.config import resolve_smtp_credentials

        gmail_sender = (resolve_smtp_credentials().get("user") or "").strip()
    except Exception:
        gmail_sender = ""

    payload = {
        "gmail_enabled": bool(settings.get("gmail_enabled", True)),
        "gmail_recipient": settings.get("gmail_recipient") or "",
        "gmail_sender": gmail_sender,
        "gmail_connected": gmail_connected,
        "zalo_enabled": bool(settings.get("zalo_enabled", True)),
        "zalo_connected": zalo_connected,
        "ams_app_url": settings.get("ams_app_url") or "http://localhost:5173/vi-pham-atsh",
    }
    if db is not None:
        payload.update(resolve_gmail_delivery_status(db))
    else:
        payload.update(
            {
                "gmail_last_sent_at": None,
                "gmail_last_status": None,
                "gmail_last_error": None,
            }
        )
    return payload


def _new_test_event_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:8].upper()}"


def publish_event_created(event: dict[str, Any]) -> None:
    from app.core.event_bus import get_event_bus
    from app.core.event_bus.event_types import EVENT_CREATED

    get_event_bus().publish(
        EVENT_CREATED,
        {
            "topic": EVENT_CREATED,
            "timestamp": utc_now_iso(),
            "data": {"event": event},
        },
    )


def publish_event_removed(event_id: str) -> None:
    from app.core.event_bus import get_event_bus
    from app.core.event_bus.event_types import EVENT_REMOVED

    get_event_bus().publish(
        EVENT_REMOVED,
        {
            "topic": EVENT_REMOVED,
            "timestamp": utc_now_iso(),
            "data": {"event": {"id": event_id}},
        },
    )


def schedule_ephemeral_event_removal(event_id: str, *, delay_seconds: float = 5.0) -> None:
    from app.services.event_stream_service import event_stream_service

    async def _remove_later() -> None:
        await asyncio.sleep(delay_seconds)
        publish_event_removed(event_id)

    loop = event_stream_service._loop
    if loop and loop.is_running():
        asyncio.run_coroutine_threadsafe(_remove_later(), loop)
        return

    try:
        running = asyncio.get_running_loop()
        running.create_task(_remove_later())
    except RuntimeError:
        logger.warning("Could not schedule ephemeral removal for %s — no event loop", event_id)


def build_ephemeral_test_event(db: Session, farm_id: str) -> dict[str, Any]:
    now = utc_now_iso()
    event_id = _new_test_event_id("EPH")
    farm = db.get(Farm, farm_id)
    farm_name = farm.name if farm else farm_id
    return {
        "id": event_id,
        "farm_id": farm_id,
        "category": "compliance_violation",
        "camera_id": "CAM-001",
        "camera_name": "Camera cổng vào (thử nghiệm)",
        "zone_id": "ZONE-TEST",
        "zone_name": "Khu sát trùng tay",
        "rule_id": "RULE-TEST",
        "rule_name": "Không sát trùng tay",
        "event_type": "NO_HAND_SANITIZE",
        "status": "OPEN",
        "severity": "HIGH",
        "severityLabel": "Nghiêm trọng",
        "title": "Không sát trùng tay",
        "description": "Vi phạm thử nghiệm từ Cài đặt AMS — tự động xóa sau vài giây.",
        "started_at": now,
        "occurred_at": now,
        "created_at": now,
        "metadata": {
            "source": "compliance_engine",
            "ephemeral": True,
            "farm_name": farm_name,
        },
    }


def run_dashboard_notification_test(db: Session, farm_id: str) -> tuple[ChannelResult, dict[str, Any], dict[str, Any]]:
    settings = get_notification_settings(db)
    event = build_ephemeral_test_event(db, farm_id)
    publish_event_created(event)
    content = build_violation_notification_content(db, event, settings)
    result = send_dashboard_notification(content)
    if result.status == "success":
        schedule_ephemeral_event_removal(event["id"])
    return result, event, content


def record_test_channel_delivery(
    db: Session,
    *,
    event_id: str,
    farm_id: str,
    result: ChannelResult,
    subject: str | None = None,
    recipient: str | None = None,
) -> NotificationDelivery:
    delivery = _record_delivery(
        db,
        event_id=event_id,
        farm_id=farm_id,
        channel=result.channel,
        status=result.status,
        subject=subject,
        error_message=result.error,
        recipient=recipient,
        smtp_latency_ms=result.smtp_latency_ms,
    )
    db.commit()
    return delivery


def run_gmail_notification_test(db: Session, farm_id: str) -> tuple[ChannelResult, dict[str, Any]]:
    settings = get_notification_settings(db)
    event_id = _new_test_event_id("TST-GML")
    sample_event = {
        "id": event_id,
        "farm_id": farm_id,
        "status": "OPEN",
        "category": "compliance_violation",
        "event_type": "NO_HAND_SANITIZE",
        "severity": "HIGH",
        "severityLabel": "Nghiêm trọng",
        "camera_id": "CAM-001",
        "camera_name": "Camera cổng vào",
        "zone_name": "Khu sát trùng tay",
        "rule_name": "Không sát trùng tay",
        "description": "Thông báo thử nghiệm Gmail từ AMS Settings.",
        "started_at": utc_now_iso(),
        "metadata": {"source": "compliance_engine", "test": True},
    }
    content = build_violation_notification_content(db, sample_event, settings)
    result = send_gmail_notification(content, settings)
    record_test_channel_delivery(
        db,
        event_id=event_id,
        farm_id=farm_id,
        result=result,
        subject=content["title"],
        recipient=settings.get("gmail_recipient"),
    )
    return result, content


def run_zalo_notification_test(db: Session, farm_id: str) -> tuple[ChannelResult, dict[str, Any]]:
    settings = get_notification_settings(db)
    event_id = _new_test_event_id("TST-ZLO")
    sample_event = {
        "id": event_id,
        "farm_id": farm_id,
        "status": "OPEN",
        "category": "compliance_violation",
        "event_type": "NO_HAND_SANITIZE",
        "severity": "HIGH",
        "severityLabel": "Nghiêm trọng",
        "camera_id": "CAM-001",
        "camera_name": "Camera cổng vào",
        "zone_name": "Khu sát trùng tay",
        "rule_name": "Không sát trùng tay",
        "description": "Thông báo thử nghiệm Zalo từ AMS Settings.",
        "started_at": utc_now_iso(),
        "metadata": {"source": "compliance_engine", "test": True},
    }
    content = build_violation_notification_content(db, sample_event, settings)
    result = send_zalo_notification(content, settings)
    record_test_channel_delivery(db, event_id=event_id, farm_id=farm_id, result=result, subject=content["title"])
    return result, content


def build_test_api_response(result: ChannelResult, content: dict[str, Any]) -> dict[str, Any]:
    status_messages = {
        "success": "Thành công",
        "failed": "Gửi thất bại",
        "skipped": "Đã bỏ qua",
    }
    return {
        "channel": result.channel,
        "status": result.status,
        "error": result.error,
        "title": NOTIFICATION_TITLE,
        "message": status_messages.get(result.status, result.status),
        "notification": {
            "type": "violation_alert",
            "eventId": content["event_id"],
            "title": content["title"],
            "message": content["body"],
            "severity": content["severity"],
            "cameraName": content["camera_name"],
            "zoneName": content["zone_name"],
            "ruleName": content["rule_name"],
            "detailUrl": content["detail_url"],
            "snapshotUrl": content.get("snapshot_url"),
            "videoUrl": content.get("video_url"),
            "occurredAt": content["occurred_at"],
        },
    }


def get_notification_settings(db: Session) -> dict[str, Any]:
    values = default_notification_settings()
    row = db.get(SystemSetting, SETTINGS_KEY)
    if row is None:
        return values
    try:
        stored = json.loads(row.value_json)
        if isinstance(stored, dict):
            values.update(stored)
    except json.JSONDecodeError:
        logger.warning("Invalid notification settings JSON")
    return values


def save_notification_settings(
    db: Session,
    payload: dict[str, Any],
    *,
    updated_by: str | None = None,
) -> dict[str, Any]:
    current = get_notification_settings(db)
    incoming = dict(payload)
    for secret_key in ("smtp_password", "zalo_access_token"):
        if secret_key in incoming and not str(incoming.get(secret_key) or "").strip():
            incoming.pop(secret_key, None)
    current.update(incoming)
    now = utc_now_iso()
    row = db.get(SystemSetting, SETTINGS_KEY)
    if row is None:
        row = SystemSetting(key=SETTINGS_KEY, value_json="{}", updated_at=now, updated_by=updated_by)
    row.value_json = json.dumps(current, ensure_ascii=False)
    row.updated_at = now
    row.updated_by = updated_by
    db.add(row)
    db.commit()
    return current


def _increment_pending_gmail() -> None:
    global _pending_gmail_count
    with _pending_gmail_lock:
        _pending_gmail_count += 1


def _decrement_pending_gmail() -> None:
    global _pending_gmail_count
    with _pending_gmail_lock:
        _pending_gmail_count = max(0, _pending_gmail_count - 1)


def get_pending_gmail_count() -> int:
    with _pending_gmail_lock:
        return _pending_gmail_count


def is_open_violation_event(event: dict[str, Any]) -> bool:
    status = str(event.get("status") or "OPEN").upper()
    if status in CLOSED_STATUSES:
        return False
    return status in {item.upper() for item in OPEN_STATUSES} or status == "OPEN"


def is_compliance_open_violation(event: dict[str, Any]) -> bool:
    """Mọi vi phạm OPEN do Compliance Engine xác nhận — không lọc theo rule."""
    if not is_open_violation_event(event):
        return False
    category = str(event.get("category") or "").lower()
    if category == "compliance_violation":
        return True
    metadata = event.get("metadata") or {}
    return metadata.get("source") == "compliance_engine"


def is_atsh_violation_event(event: dict[str, Any]) -> bool:
    category = str(event.get("category") or event.get("metadata", {}).get("source") or "").lower()
    if category in ATSH_CATEGORIES or "compliance" in category:
        return True
    metadata = event.get("metadata") or {}
    if metadata.get("source") in {"compliance_engine", "evaluator_engine", "rule_engine"}:
        return True
    event_type = str(event.get("event_type") or event.get("eventType") or "").upper()
    return bool(event_type)


def build_violation_notification_content(db: Session, event: dict[str, Any], settings: dict[str, Any]) -> dict[str, Any]:
    farm_id = event.get("farm_id") or "FARM-001"
    farm = db.get(Farm, farm_id)
    farm_name = farm.name if farm else farm_id

    occurred_at = event.get("started_at") or event.get("occurred_at") or event.get("created_at") or utc_now_iso()
    camera_name = event.get("camera_name") or event.get("camera_id") or "Chưa có dữ liệu"
    zone_name = event.get("zone_name") or event.get("zone_id") or event.get("zone") or "Chưa có dữ liệu"
    rule_name = event.get("rule_name") or event.get("ruleName") or event.get("title") or event.get("event_type")
    violation_type = (
        event.get("violation_type")
        or event.get("violationType")
        or rule_name
        or event.get("event_type")
        or "Vi phạm an toàn sinh học"
    )
    severity = event.get("severityLabel") or event.get("severity") or "MEDIUM"
    description = event.get("description") or event.get("explanation") or event.get("recommendedAction") or ""
    metadata = event.get("metadata") or {}
    object_name = (
        event.get("object_name")
        or event.get("objectName")
        or metadata.get("object_name")
        or metadata.get("objectName")
        or metadata.get("object_class")
        or metadata.get("objectClass")
        or metadata.get("track_label")
        or metadata.get("trackLabel")
    )
    snapshot_url = event.get("snapshot_url") or event.get("snapshotPath")
    video_url = (event.get("metadata") or {}).get("video_url") or (event.get("metadata") or {}).get("videoUrl")
    app_url = settings.get("ams_app_url") or "http://localhost:5173/vi-pham-atsh"
    detail_url = f"{app_url.rstrip('/')}/{event.get('id')}" if event.get("id") else app_url

    body_lines = [
        NOTIFICATION_TITLE,
        "",
        f"Thời gian phát hiện: {occurred_at}",
        f"Trang trại: {farm_name}",
        f"Camera: {camera_name}",
        f"Khu vực: {zone_name}",
        f"Đối tượng: {object_name or 'Chưa có dữ liệu'}",
        f"Loại vi phạm: {violation_type}",
        f"Mức độ: {severity}",
        f"Liên kết mở AMS: {detail_url}",
    ]

    return {
        "title": NOTIFICATION_TITLE,
        "body": "\n".join(body_lines),
        "event_id": event.get("id"),
        "farm_id": farm_id,
        "farm_name": farm_name,
        "occurred_at": occurred_at,
        "camera_name": camera_name,
        "zone_name": zone_name,
        "object_name": object_name,
        "rule_name": rule_name,
        "violation_type": violation_type,
        "alert_type": ALERT_TYPE_VIOLATION,
        "severity": severity,
        "description": description,
        "detail_url": detail_url,
        "ams_url": app_url.rstrip("/"),
        "snapshot_url": snapshot_url,
        "video_url": video_url,
    }


def _new_delivery_id() -> str:
    return f"ND-{uuid.uuid4().hex[:10].upper()}"


def _record_delivery(
    db: Session,
    *,
    event_id: str,
    farm_id: str,
    channel: str,
    status: str,
    subject: str | None = None,
    error_message: str | None = None,
    recipient: str | None = None,
    smtp_latency_ms: int | None = None,
) -> NotificationDelivery:
    delivery = NotificationDelivery(
        id=_new_delivery_id(),
        event_id=event_id,
        farm_id=farm_id,
        channel=channel,
        status=status,
        sent_at=utc_now_iso(),
        subject=subject,
        recipient=recipient,
        smtp_latency_ms=smtp_latency_ms,
        error_message=error_message,
    )
    db.add(delivery)
    return delivery


def _claim_dispatch(db: Session, event_id: str, farm_id: str) -> bool:
    dispatch = NotificationDispatch(
        event_id=event_id,
        farm_id=farm_id,
        dispatched_at=utc_now_iso(),
        status="processing",
        summary=None,
    )
    db.add(dispatch)
    try:
        db.flush()
        return True
    except IntegrityError:
        db.rollback()
        return False


def _finalize_dispatch(db: Session, event_id: str, results: list[ChannelResult], summary: str) -> None:
    dispatch = db.get(NotificationDispatch, event_id)
    if dispatch is None:
        return
    statuses = {item.status for item in results}
    if statuses == {"success"}:
        dispatch.status = "completed"
    elif "success" in statuses:
        dispatch.status = "partial"
    else:
        dispatch.status = "failed"
    dispatch.summary = summary


def send_dashboard_notification(content: dict[str, Any]) -> ChannelResult:
    from app.core.event_bus import get_event_bus
    from app.core.event_bus import event_types as topics

    try:
        get_event_bus().publish(
            topics.NOTIFICATION_CREATED,
            {
                "topic": topics.NOTIFICATION_CREATED,
                "timestamp": utc_now_iso(),
                "data": {
                    "notification": {
                        "type": "violation_alert",
                        "eventId": content["event_id"],
                        "title": content["title"],
                        "message": content["body"],
                        "severity": content["severity"],
                        "cameraName": content["camera_name"],
                        "zoneName": content["zone_name"],
                        "ruleName": content["rule_name"],
                        "detailUrl": content["detail_url"],
                        "snapshotUrl": content.get("snapshot_url"),
                        "videoUrl": content.get("video_url"),
                        "occurredAt": content["occurred_at"],
                    }
                },
            },
        )
        return ChannelResult(channel=CHANNEL_DASHBOARD, status="success")
    except Exception as exc:
        logger.exception("Dashboard notification failed")
        return ChannelResult(channel=CHANNEL_DASHBOARD, status="failed", error=str(exc))


def publish_gmail_delivery_failed(*, event_id: str, error: str, recipient: str | None = None) -> None:
    from app.core.event_bus import get_event_bus
    from app.core.event_bus.event_types import NOTIFICATION_GMAIL_FAILED

    get_event_bus().publish(
        NOTIFICATION_GMAIL_FAILED,
        {
            "topic": NOTIFICATION_GMAIL_FAILED,
            "timestamp": utc_now_iso(),
            "data": {
                "alert": {
                    "type": "gmail_delivery_failed",
                    "eventId": event_id,
                    "title": "Gửi Email thất bại",
                    "message": error,
                    "recipient": recipient,
                }
            },
        },
    )


def send_gmail_notification_with_retry(content: dict[str, Any], settings: dict[str, Any]) -> ChannelResult:
    last_result: ChannelResult | None = None
    for attempt in range(1, GMAIL_MAX_ATTEMPTS + 1):
        result = send_gmail_notification(content, settings)
        if result.status == "success":
            if attempt > 1:
                logger.info("[Gmail] Sent after attempt %s/%s", attempt, GMAIL_MAX_ATTEMPTS)
            return result
        last_result = result
        if attempt < GMAIL_MAX_ATTEMPTS:
            logger.warning(
                "[Gmail] Attempt %s/%s failed, retry in %ss: %s",
                attempt,
                GMAIL_MAX_ATTEMPTS,
                GMAIL_RETRY_INTERVAL_SECONDS,
                result.error,
            )
            time.sleep(GMAIL_RETRY_INTERVAL_SECONDS)
    return last_result or ChannelResult(channel=CHANNEL_GMAIL, status="failed", error="Gửi Email thất bại")


def send_gmail_notification(content: dict[str, Any], settings: dict[str, Any]) -> ChannelResult:
    from app.services.gmail_notification_service import send_gmail_message

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


def _send_gmail_and_record(
    *,
    event_id: str,
    farm_id: str,
    content: dict[str, Any],
    settings: dict[str, Any],
) -> None:
    from app.database.session import SessionLocal

    _increment_pending_gmail()
    db = SessionLocal()
    try:
        existing = db.scalar(
            select(NotificationDelivery).where(
                NotificationDelivery.event_id == event_id,
                NotificationDelivery.channel == CHANNEL_GMAIL,
            )
        )
        if existing is not None:
            return

        result = send_gmail_notification_with_retry(content, settings)
        _record_delivery(
            db,
            event_id=event_id,
            farm_id=farm_id,
            channel=result.channel,
            status=result.status,
            subject=content.get("title") or NOTIFICATION_TITLE,
            error_message=result.error,
            recipient=settings.get("gmail_recipient") if result.channel == CHANNEL_GMAIL else None,
            smtp_latency_ms=result.smtp_latency_ms,
        )
        db.commit()
        if result.status == "failed":
            publish_gmail_delivery_failed(
                event_id=event_id,
                error=result.error or "Gửi Email thất bại",
                recipient=settings.get("gmail_recipient"),
            )
        from app.services.system_alert_notification_service import record_gmail_delivery_outcome

        record_gmail_delivery_outcome(success=result.status == "success", error=result.error)
    except Exception:
        logger.exception("Background Gmail dispatch failed for %s", event_id)
        db.rollback()
    finally:
        db.close()
        _decrement_pending_gmail()


def schedule_gmail_notification(
    *,
    event_id: str,
    farm_id: str,
    content: dict[str, Any],
    settings: dict[str, Any],
) -> None:
    worker = threading.Thread(
        target=_send_gmail_and_record,
        kwargs={
            "event_id": event_id,
            "farm_id": farm_id,
            "content": content,
            "settings": settings,
        },
        daemon=True,
        name=f"gmail-notify-{event_id}",
    )
    worker.start()


def send_zalo_notification(content: dict[str, Any], settings: dict[str, Any]) -> ChannelResult:
    if not settings.get("zalo_enabled", True):
        return ChannelResult(channel=CHANNEL_ZALO, status="skipped", error="Zalo OA đang tắt")

    oa_id = (settings.get("zalo_oa_id") or "").strip() or (getattr(get_settings(), "zalo_oa_id", None) or "").strip()
    access_token = resolve_zalo_access_token(settings)
    recipient_id = (settings.get("zalo_recipient_id") or "").strip()

    if not oa_id:
        return ChannelResult(
            channel=CHANNEL_ZALO,
            status="failed",
            error="Chưa kết nối Zalo. Vui lòng bấm «Quét mã QR» trong Cài đặt.",
        )
    if not recipient_id:
        return ChannelResult(
            channel=CHANNEL_ZALO,
            status="failed",
            error="Chưa kết nối Zalo. Vui lòng bấm «Quét mã QR» trong Cài đặt.",
        )
    if not access_token:
        return ChannelResult(
            channel=CHANNEL_ZALO,
            status="failed",
            error="Hệ thống chưa sẵn sàng gửi Zalo. Liên hệ quản trị viên.",
        )

    payload = json.dumps(
        {
            "recipient": {"user_id": recipient_id},
            "message": {"text": content["body"][:2000]},
        }
    ).encode("utf-8")
    req = urlrequest.Request(
        "https://openapi.zalo.me/v3.0/oa/message/cs",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "access_token": access_token,
        },
        method="POST",
    )
    try:
        with urlrequest.urlopen(req, timeout=20) as response:
            raw = response.read().decode("utf-8", errors="replace")
            try:
                body = json.loads(raw) if raw else {}
            except json.JSONDecodeError:
                body = {"message": raw}

            if response.status >= 400:
                detail = body.get("message") or body.get("error_description") or raw or f"HTTP {response.status}"
                return ChannelResult(channel=CHANNEL_ZALO, status="failed", error=str(detail))

            error_code = body.get("error")
            if error_code not in (None, 0, "0"):
                detail = body.get("message") or body.get("error_name") or f"Zalo error {error_code}"
                return ChannelResult(channel=CHANNEL_ZALO, status="failed", error=str(detail))

        logger.info("[Notification] Zalo sent to user %s via OA %s", recipient_id, oa_id)
        return ChannelResult(channel=CHANNEL_ZALO, status="success")
    except urlerror.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace") if exc.fp else str(exc.reason or exc)
        logger.exception("Zalo notification HTTP error")
        return ChannelResult(channel=CHANNEL_ZALO, status="failed", error=detail or str(exc))
    except urlerror.URLError as exc:
        logger.exception("Zalo notification failed")
        return ChannelResult(channel=CHANNEL_ZALO, status="failed", error=str(exc.reason or exc))


def dispatch_violation_notifications(event: dict[str, Any]) -> list[ChannelResult]:
    from app.database.session import SessionLocal

    if not event or not event.get("id"):
        return []

    if not is_open_violation_event(event):
        return []

    if not is_compliance_open_violation(event):
        return []

    db = SessionLocal()
    results: list[ChannelResult] = []
    try:
        event_id = event["id"]
        farm_id = event.get("farm_id") or "FARM-001"

        if db.get(NotificationDispatch, event_id) is not None:
            logger.debug("Skip duplicate notification dispatch for %s", event_id)
            return []

        if not _claim_dispatch(db, event_id, farm_id):
            return []

        settings = get_notification_settings(db)
        content = build_violation_notification_content(db, event, settings)

        channel_handlers = [
            (CHANNEL_DASHBOARD, lambda: send_dashboard_notification(content)),
            (CHANNEL_ZALO, lambda: send_zalo_notification(content, settings)),
        ]

        for channel, handler in channel_handlers:
            existing = db.scalar(
                select(NotificationDelivery).where(
                    NotificationDelivery.event_id == event_id,
                    NotificationDelivery.channel == channel,
                )
            )
            if existing is not None:
                continue

            result = handler()
            results.append(result)
            _record_delivery(
                db,
                event_id=event_id,
                farm_id=farm_id,
                channel=result.channel,
                status=result.status,
                subject=content["title"],
                error_message=result.error,
                recipient=settings.get("gmail_recipient") if result.channel == CHANNEL_GMAIL else None,
                smtp_latency_ms=result.smtp_latency_ms,
            )
            db.commit()

        gmail_existing = db.scalar(
            select(NotificationDelivery).where(
                NotificationDelivery.event_id == event_id,
                NotificationDelivery.channel == CHANNEL_GMAIL,
            )
        )
        if gmail_existing is None and settings.get("gmail_enabled", True):
            schedule_gmail_notification(
                event_id=event_id,
                farm_id=farm_id,
                content=content,
                settings=settings,
            )

        _finalize_dispatch(db, event_id, results, content["body"][:500])
        db.commit()
        return results
    except Exception:
        logger.exception("Violation notification dispatch failed for event %s", event.get("id"))
        db.rollback()
        return results
    finally:
        db.close()


def handle_event_created_for_notifications(message: dict[str, Any]) -> None:
    payload = message.get("data") or message
    event = payload.get("event")
    if not event:
        return
    metadata = event.get("metadata") or {}
    if metadata.get("ephemeral") or metadata.get("test"):
        return
    dispatch_violation_notifications(event)


def register_violation_notification_subscriber() -> None:
    from app.core.event_bus import get_event_bus
    from app.core.event_bus.event_types import EVENT_CREATED

    get_event_bus().subscribe(EVENT_CREATED, handle_event_created_for_notifications)
    logger.info("Violation notification subscriber registered on EventBus")
