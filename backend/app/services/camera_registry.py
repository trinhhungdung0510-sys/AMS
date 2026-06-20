from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from sqlalchemy import select

from app.models import Camera
from app.schemas.camera import CameraCreate, CameraUpdate


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def build_rtsp_url(
    *,
    ip: str,
    port: int,
    username: str,
    password: str,
    rtsp_url: str | None = None,
) -> str:
    if rtsp_url and rtsp_url.strip():
        return rtsp_url.strip()
    return f"rtsp://{username}:{password}@{ip}:{port}/Streaming/Channels/101"


def camera_to_response_dict(camera: Camera) -> dict:
    return {
        "id": camera.id,
        "name": camera.name,
        "manufacturer": camera.manufacturer,
        "ip": camera.ip,
        "ip_address": camera.ip,
        "port": camera.port,
        "username": camera.username,
        "rtsp_url": camera.rtsp_url,
        "status": camera.status,
        "fps": camera.fps,
        "resolution": camera.resolution,
        "last_seen": camera.last_seen,
        "created_at": camera.created_at,
        "farm_id": camera.farm_id,
        "zone": camera.zone,
        "uptime": camera.uptime,
        "is_active": camera.is_active,
    }


def create_camera(db: Session, payload: CameraCreate) -> Camera:
    camera_id = payload.id or f"CAM-{uuid.uuid4().hex[:8].upper()}"
    if db.get(Camera, camera_id):
        raise ValueError("ID camera đã tồn tại")

    existing_ip = db.scalar(select(Camera).where(Camera.ip == payload.ip))
    if existing_ip:
        raise ValueError("IP camera đã tồn tại")

    rtsp_url = build_rtsp_url(
        ip=payload.ip,
        port=payload.port,
        username=payload.username,
        password=payload.password,
        rtsp_url=payload.rtsp_url,
    )

    camera = Camera(
        id=camera_id,
        farm_id=payload.farm_id,
        name=payload.name,
        zone=payload.zone,
        manufacturer=payload.manufacturer,
        ip=payload.ip,
        port=payload.port,
        username=payload.username,
        password=payload.password,
        rtsp_url=rtsp_url,
        status=payload.status,
        resolution=payload.resolution,
        uptime=payload.uptime,
        fps=payload.fps,
        is_active=payload.is_active,
        last_seen=None,
        created_at=utc_now_iso(),
    )
    db.add(camera)
    db.commit()
    db.refresh(camera)
    return camera


def update_camera(db: Session, camera: Camera, payload: CameraUpdate) -> Camera:
    values = payload.model_dump(exclude_unset=True)
    password = values.pop("password", None)

    if "ip" in values:
        existing_ip = db.scalar(
            select(Camera).where(Camera.ip == values["ip"], Camera.id != camera.id)
        )
        if existing_ip:
            raise ValueError("IP camera đã tồn tại")

    for field, value in values.items():
        setattr(camera, field, value)

    if password is not None:
        camera.password = password

    next_ip = values.get("ip", camera.ip)
    next_port = values.get("port", camera.port)
    next_username = values.get("username", camera.username)
    next_password = password if password is not None else camera.password
    next_rtsp = values.get("rtsp_url", camera.rtsp_url)

    if any(key in values for key in ("ip", "port", "username", "password", "rtsp_url")):
        camera.rtsp_url = build_rtsp_url(
            ip=next_ip,
            port=next_port,
            username=next_username,
            password=next_password,
            rtsp_url=next_rtsp,
        )

    db.add(camera)
    db.commit()
    db.refresh(camera)
    return camera
