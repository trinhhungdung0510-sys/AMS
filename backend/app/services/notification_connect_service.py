from __future__ import annotations

import json
import logging
import smtplib
import time
import uuid
from typing import Any
from urllib import error as urlerror
from urllib import request as urlrequest
from urllib.parse import quote

from sqlalchemy.orm import Session

from app.core.config import get_settings, resolve_smtp_credentials
from app.services.violation_notification_service import (
    get_notification_settings,
    save_notification_settings,
)

logger = logging.getLogger(__name__)

GMAIL_SMTP_HOST = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587
ZALO_SESSION_TTL_SECONDS = 600

_zalo_connect_sessions: dict[str, dict[str, Any]] = {}


class NotificationConnectError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


def _system_gmail_credentials() -> dict[str, str]:
    creds = resolve_smtp_credentials()
    host = (creds.get("host") or "").strip() or GMAIL_SMTP_HOST
    return {
        "host": host,
        "port": GMAIL_SMTP_PORT,
        "user": (creds.get("user") or "").strip(),
        "password": (creds.get("password") or "").strip(),
    }


def _system_zalo_credentials() -> dict[str, str]:
    env = get_settings()
    return {
        "oa_id": (getattr(env, "zalo_oa_id", None) or "").strip(),
        "access_token": (getattr(env, "zalo_oa_access_token", None) or "").strip(),
    }


def verify_smtp_login(*, host: str, port: int, user: str, password: str) -> None:
    if not host or not user or not password:
        raise NotificationConnectError(
            "Hệ thống chưa sẵn sàng gửi Gmail. Liên hệ quản trị viên để cấu hình máy chủ."
        )
    try:
        with smtplib.SMTP(host, port, timeout=20) as client:
            client.starttls()
            client.login(user, password)
    except Exception as exc:
        logger.exception("Gmail SMTP verification failed")
        raise NotificationConnectError(f"Không kết nối được Gmail: {exc}") from exc


def connect_gmail(
    db: Session,
    *,
    gmail_recipient: str,
    updated_by: str | None = None,
) -> dict[str, Any]:
    from app.services.gmail_notification_service import (
        GmailNotificationError,
        connect_gmail_with_test_email,
    )

    try:
        return connect_gmail_with_test_email(
            db,
            gmail_recipient=gmail_recipient,
            updated_by=updated_by,
        )
    except GmailNotificationError as exc:
        raise NotificationConnectError(exc.message) from exc


def _fetch_zalo_follower_ids(access_token: str) -> list[str]:
    req = urlrequest.Request(
        "https://openapi.zalo.me/v2.0/oa/getfollowers?offset=0&count=50",
        headers={"access_token": access_token},
        method="GET",
    )
    try:
        with urlrequest.urlopen(req, timeout=20) as response:
            raw = response.read().decode("utf-8", errors="replace")
            body = json.loads(raw) if raw else {}
    except urlerror.URLError as exc:
        logger.exception("Zalo followers fetch failed")
        raise NotificationConnectError(f"Không truy cập được Zalo OA: {exc.reason or exc}") from exc

    if body.get("error") not in (None, 0, "0"):
        detail = body.get("message") or f"Zalo error {body.get('error')}"
        raise NotificationConnectError(str(detail))

    followers = body.get("data", {}).get("followers") or []
    return [str(item.get("user_id")) for item in followers if item.get("user_id")]


def _zalo_follow_url(oa_id: str) -> str:
    env = get_settings()
    custom = (getattr(env, "zalo_oa_follow_url", None) or "").strip()
    if custom:
        return custom
    return f"https://zalo.me/{oa_id}"


def start_zalo_connect(db: Session) -> dict[str, Any]:
    creds = _system_zalo_credentials()
    if not creds["oa_id"] or not creds["access_token"]:
        raise NotificationConnectError(
            "Hệ thống chưa sẵn sàng gửi Zalo. Liên hệ quản trị viên để cấu hình OA."
        )

    baseline = set(_fetch_zalo_follower_ids(creds["access_token"]))
    session_id = uuid.uuid4().hex
    follow_url = _zalo_follow_url(creds["oa_id"])
    _zalo_connect_sessions[session_id] = {
        "baseline": baseline,
        "oa_id": creds["oa_id"],
        "access_token": creds["access_token"],
        "expires_at": time.time() + ZALO_SESSION_TTL_SECONDS,
    }

    return {
        "session_id": session_id,
        "follow_url": follow_url,
        "qr_url": f"https://quickchart.io/qr?size=240&margin=2&text={quote(follow_url, safe='')}",
        "expires_in": ZALO_SESSION_TTL_SECONDS,
        "message": "Quét mã QR bằng Zalo và quan tâm Official Account AMS.",
    }


def poll_zalo_connect(
    db: Session,
    session_id: str,
    *,
    updated_by: str | None = None,
) -> dict[str, Any]:
    session = _zalo_connect_sessions.get(session_id)
    if session is None:
        raise NotificationConnectError("Phiên kết nối Zalo không tồn tại hoặc đã hết hạn")

    if time.time() > session["expires_at"]:
        _zalo_connect_sessions.pop(session_id, None)
        return {"status": "expired", "connected": False}

    current_ids = _fetch_zalo_follower_ids(session["access_token"])
    baseline: set[str] = session["baseline"]
    new_followers = [user_id for user_id in current_ids if user_id not in baseline]

    if not new_followers:
        return {"status": "pending", "connected": False}

    recipient_id = new_followers[0]
    updated = save_notification_settings(
        db,
        {
            "zalo_enabled": True,
            "zalo_oa_id": session["oa_id"],
            "zalo_access_token": session["access_token"],
            "zalo_recipient_id": recipient_id,
            "zalo_connected": True,
        },
        updated_by=updated_by,
    )
    _zalo_connect_sessions.pop(session_id, None)
    logger.info("[Notification] Zalo connected for user %s", recipient_id)
    return {"status": "connected", "connected": True, "settings": updated}


def disconnect_gmail(db: Session, *, updated_by: str | None = None) -> dict[str, Any]:
    return save_notification_settings(
        db,
        {
            "gmail_connected": False,
            "smtp_password": "",
            "smtp_user": "",
            "smtp_host": "",
        },
        updated_by=updated_by,
    )


def disconnect_zalo(db: Session, *, updated_by: str | None = None) -> dict[str, Any]:
    return save_notification_settings(
        db,
        {
            "zalo_connected": False,
            "zalo_recipient_id": "",
            "zalo_access_token": "",
        },
        updated_by=updated_by,
    )
