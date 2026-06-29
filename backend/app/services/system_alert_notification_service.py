"""Real-time Gmail system alerts — no scheduled reports or digests."""

from __future__ import annotations

import logging
import threading
import time
import uuid
from typing import Any, Optional

from sqlalchemy.orm import Session

from app.core.event_bus import get_event_bus
from app.core.event_bus.event_types import (
    CAMERA_STATUS_CHANGED,
    DETECTOR_FAILED,
    DETECTOR_STOPPED,
)
from app.database.session import SessionLocal
from app.models import Camera
from app.services.gmail_notification_service import (
    send_system_alert_gmail,
    utc_now_iso,
)
from app.services.violation_notification_service import (
    _record_delivery,
    get_notification_settings,
)

logger = logging.getLogger(__name__)

CHANNEL_GMAIL_SYSTEM = "gmail_system"
ALERT_COOLDOWN_SECONDS = 1800
GMAIL_FAILURE_ALERT_THRESHOLD = 3

_lock = threading.Lock()
_alert_sent_at: dict[str, float] = {}
_consecutive_gmail_failures = 0


def _cooldown_key(alert_type: str, resource_id: str | None = None) -> str:
    return f"{alert_type}:{resource_id or 'global'}"


def _should_send_alert(alert_type: str, resource_id: str | None = None) -> bool:
    key = _cooldown_key(alert_type, resource_id)
    now = time.monotonic()
    with _lock:
        last = _alert_sent_at.get(key)
        if last is not None and (now - last) < ALERT_COOLDOWN_SECONDS:
            return False
        _alert_sent_at[key] = now
    return True


def _new_system_event_id(alert_type: str, resource_id: str | None = None) -> str:
    suffix = (resource_id or uuid.uuid4().hex[:6]).replace(" ", "-")[:12].upper()
    prefix = alert_type.replace("_", "-").upper()[:16]
    return f"SYS-{prefix}-{suffix}"


def _resolve_camera_name(db: Session, camera_id: str | None) -> str:
    if not camera_id:
        return "Không xác định"
    camera = db.get(Camera, camera_id)
    return camera.name if camera else camera_id


def _send_system_alert(
    *,
    alert_type: str,
    title: str,
    message: str,
    resource_id: str | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    if not _should_send_alert(alert_type, resource_id):
        logger.debug("Skip system alert %s (cooldown)", alert_type)
        return

    db = SessionLocal()
    try:
        settings = get_notification_settings(db)
        if not settings.get("gmail_enabled", True) or not settings.get("gmail_connected"):
            return
        recipient = (settings.get("gmail_recipient") or "").strip()
        if not recipient:
            return

        app_url = settings.get("ams_app_url") or "http://localhost:5173/bang-dieu-khien"
        event_id = _new_system_event_id(alert_type, resource_id)
        payload = {
            "alert_type": alert_type,
            "title": title,
            "message": message,
            "occurred_at": utc_now_iso(),
            "resource_id": resource_id,
            "details": details or {},
            "ams_url": app_url.rstrip("/"),
        }
        result = send_system_alert_gmail(recipient=recipient, alert=payload)
        _record_delivery(
            db,
            event_id=event_id,
            farm_id="FARM-001",
            channel=CHANNEL_GMAIL_SYSTEM,
            status="success" if result.success else "failed",
            subject=title,
            error_message=result.error,
            recipient=recipient,
            smtp_latency_ms=result.smtp_latency_ms,
        )
        db.commit()
        if result.success:
            logger.info("[SystemAlert] Gmail sent: %s", alert_type)
        else:
            logger.warning("[SystemAlert] Gmail failed for %s: %s", alert_type, result.error)
    except Exception:
        logger.exception("System alert Gmail dispatch failed: %s", alert_type)
        db.rollback()
    finally:
        db.close()


def schedule_system_alert(**kwargs: Any) -> None:
    worker = threading.Thread(
        target=_send_system_alert,
        kwargs=kwargs,
        daemon=True,
        name=f"sys-alert-{kwargs.get('alert_type', 'unknown')}",
    )
    worker.start()


def notify_camera_offline(*, camera_id: str, last_seen_at: str | None = None) -> None:
    db = SessionLocal()
    try:
        camera_name = _resolve_camera_name(db, camera_id)
    finally:
        db.close()
    schedule_system_alert(
        alert_type="camera_offline",
        title="⚠️ Camera mất kết nối",
        message=f"Camera {camera_name} ({camera_id}) đã chuyển sang OFFLINE.",
        resource_id=camera_id,
        details={"camera_id": camera_id, "camera_name": camera_name, "last_seen_at": last_seen_at},
    )


def notify_ai_runtime_stopped(*, camera_id: str | None, error: str | None, reason: str) -> None:
    schedule_system_alert(
        alert_type="ai_runtime_stopped",
        title="⚠️ AI Runtime dừng",
        message=error or reason or "AI Runtime không phản hồi.",
        resource_id=camera_id,
        details={"camera_id": camera_id, "error": error, "reason": reason},
    )


def notify_database_unavailable(*, error: str | None = None) -> None:
    schedule_system_alert(
        alert_type="database_unavailable",
        title="⚠️ Database không khả dụng",
        message=error or "AMS không thể kết nối database.",
        resource_id=None,
        details={"error": error},
    )


def notify_notification_service_failure(*, failure_count: int, last_error: str | None) -> None:
    schedule_system_alert(
        alert_type="notification_service_failure",
        title="⚠️ Notification Service lỗi liên tục",
        message=f"Gmail gửi thất bại {failure_count} lần liên tiếp.",
        resource_id=None,
        details={"failure_count": failure_count, "last_error": last_error},
    )


def record_gmail_delivery_outcome(*, success: bool, error: str | None = None) -> None:
    global _consecutive_gmail_failures
    with _lock:
        if success:
            _consecutive_gmail_failures = 0
            return
        _consecutive_gmail_failures += 1
        count = _consecutive_gmail_failures

    if count >= GMAIL_FAILURE_ALERT_THRESHOLD:
        notify_notification_service_failure(failure_count=count, last_error=error)
        with _lock:
            _consecutive_gmail_failures = 0


def handle_camera_status_changed(message: dict[str, Any]) -> None:
    payload = message.get("data") or message
    status = str(payload.get("status") or "").upper()
    if status != "OFFLINE":
        return
    camera_id = payload.get("cameraId") or payload.get("camera_id")
    if not camera_id:
        return
    notify_camera_offline(camera_id=camera_id, last_seen_at=payload.get("lastSeenAt"))


def handle_detector_failed(message: dict[str, Any]) -> None:
    payload = message.get("data") or message
    camera_id = payload.get("camera_id") or payload.get("cameraId")
    error = payload.get("error")
    notify_ai_runtime_stopped(camera_id=camera_id, error=error, reason="detector.failed")


def handle_detector_stopped(message: dict[str, Any]) -> None:
    payload = message.get("data") or message
    camera_id = payload.get("camera_id") or payload.get("cameraId")
    error = payload.get("error")
    notify_ai_runtime_stopped(camera_id=camera_id, error=error, reason="detector.stopped")


def register_system_alert_gmail_subscriber() -> None:
    bus = get_event_bus()
    bus.subscribe(CAMERA_STATUS_CHANGED, handle_camera_status_changed)
    bus.subscribe(DETECTOR_FAILED, handle_detector_failed)
    bus.subscribe(DETECTOR_STOPPED, handle_detector_stopped)
    logger.info("System alert Gmail subscriber registered (real-time only)")
