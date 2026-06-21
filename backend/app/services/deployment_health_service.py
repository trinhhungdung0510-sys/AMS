from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import Camera, CameraHealth
from app.services.camera_health_service import STATUS_OFFLINE, STATUS_ONLINE
from app.services.health import check_database, check_redis
from app.ws.connection_manager import events_manager


def _check_storage() -> dict[str, Any]:
    settings = get_settings()
    uploads = Path(settings.uploads_root)
    storage = Path(settings.storage_root)
    uploads.mkdir(parents=True, exist_ok=True)
    storage.mkdir(parents=True, exist_ok=True)

    usage = shutil.disk_usage(str(uploads.resolve()))
    uploads_writable = os.access(uploads, os.W_OK)
    storage_writable = os.access(storage, os.W_OK)
    status = "ok" if uploads_writable and storage_writable else "degraded"

    return {
        "status": status,
        "uploadsPath": str(uploads),
        "storagePath": str(storage),
        "writable": uploads_writable and storage_writable,
        "freeGb": round(usage.free / (1024**3), 2),
    }


def _check_ffmpeg() -> dict[str, Any]:
    settings = get_settings()
    ffmpeg = shutil.which(settings.ffmpeg_path) or shutil.which("ffmpeg")
    ffprobe = shutil.which(settings.ffprobe_path) or shutil.which("ffprobe")
    if ffmpeg and ffprobe:
        return {"status": "ok", "ffmpeg": ffmpeg, "ffprobe": ffprobe}
    return {
        "status": "unavailable",
        "ffmpeg": ffmpeg,
        "ffprobe": ffprobe,
    }


def _check_cameras(db: Session) -> dict[str, Any]:
    cameras = list(db.scalars(select(Camera).where(Camera.is_active.is_(True))))
    health_rows = {
        row.camera_id: row.status
        for row in db.scalars(select(CameraHealth))
    }
    online = 0
    offline = 0
    for camera in cameras:
        status = (health_rows.get(camera.id) or camera.status or "").upper()
        if status in {STATUS_ONLINE, "ONLINE"} or camera.status == "online":
            online += 1
        elif status in {STATUS_OFFLINE, "OFFLINE"} or camera.status == "offline":
            offline += 1
        else:
            online += 1

    total = len(cameras)
    return {
        "status": "ok" if total else "empty",
        "total": total,
        "online": online,
        "offline": offline,
    }


def _check_websocket() -> dict[str, Any]:
    clients = len(events_manager.active_connections)
    return {
        "status": "ok",
        "connectedClients": clients,
        "endpoint": "/ws/events",
    }


def build_health_report(db: Session) -> dict[str, Any]:
    database = "unavailable"
    try:
        database = check_database(db)
    except Exception:
        pass

    redis = "unavailable"
    try:
        redis = check_redis()
    except Exception:
        pass

    storage = _check_storage()
    camera = _check_cameras(db)
    ffmpeg = _check_ffmpeg()
    websocket = _check_websocket()

    components = [database, redis, storage["status"], camera["status"], ffmpeg["status"], websocket["status"]]
    overall = "ok"
    if "unavailable" in components or camera["status"] == "empty":
        overall = "degraded" if database == "ok" else "unavailable"

    return {
        "status": overall,
        "service": get_settings().app_name,
        "version": "2.0",
        "database": database,
        "redis": redis,
        "websocket": websocket,
        "storage": storage,
        "camera": camera,
        "ffmpeg": ffmpeg,
    }
