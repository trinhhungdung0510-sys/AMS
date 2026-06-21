from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Camera, CameraHealth, CameraZone, Farm
from app.services.camera_health_service import STATUS_ONLINE, new_health_id
from app.services.demo_assets_service import ensure_demo_assets

DEMO_FARM_ID = "FARM-DEMO"
DEMO_FARM_NAME = "Mind Farm Demo"

DEMO_CAMERAS: tuple[tuple[str, str, str, str], ...] = (
    ("CAM-DEMO-01", "Nhà tắm", "shower_room", "10.0.0.11"),
    ("CAM-DEMO-02", "Cổng trại", "farm_gate", "10.0.0.12"),
    ("CAM-DEMO-03", "Hàng rào", "fence_line", "10.0.0.13"),
)

DEFAULT_ZONE_POINTS = [
    {"x": 0.12, "y": 0.12},
    {"x": 0.88, "y": 0.12},
    {"x": 0.88, "y": 0.88},
    {"x": 0.12, "y": 0.88},
]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def bootstrap_demo_environment(db: Session) -> dict:
    ensure_demo_assets()
    now = utc_now_iso()
    counts = {"farms": 0, "cameras": 0, "zones": 0, "healthRows": 0}

    farm = db.get(Farm, DEMO_FARM_ID)
    if farm is None:
        farm = Farm(
            id=DEMO_FARM_ID,
            name=DEMO_FARM_NAME,
            code="DEMO",
            address="Demo deployment — no real RTSP required",
            contact_name="AMS Demo",
            contact_phone="0000000000",
            created_at=now,
            location="Demo Site",
            plan="demo",
            status="active",
        )
        db.add(farm)
        counts["farms"] += 1
    else:
        farm.name = DEMO_FARM_NAME
        farm.status = "active"

    for index, (camera_id, name, zone_code, ip) in enumerate(DEMO_CAMERAS, start=1):
        camera = db.get(Camera, camera_id)
        if camera is None:
            camera = Camera(
                id=camera_id,
                farm_id=DEMO_FARM_ID,
                name=name,
                zone=zone_code,
                manufacturer="AMS Demo",
                ip=ip,
                port=554,
                username="demo",
                password="demo",
                rtsp_url=f"rtsp://demo:demo@{ip}:554/demo/{index}",
                status="online",
                resolution="1080p",
                uptime=100.0,
                fps=25,
                is_active=True,
                last_seen=now,
                created_at=now,
            )
            db.add(camera)
            counts["cameras"] += 1
        else:
            camera.farm_id = DEMO_FARM_ID
            camera.name = name
            camera.zone = zone_code
            camera.status = "online"
            camera.is_active = True
            camera.last_seen = now

        zone_id = f"ZONE-DEMO-0{index}"
        zone = db.get(CameraZone, zone_id)
        if zone is None:
            zone = CameraZone(
                id=zone_id,
                farm_id=DEMO_FARM_ID,
                camera_id=camera_id,
                parent_zone_id=None,
                name=name,
                description=f"Demo zone — {name}",
                zone_type="monitoring",
                points=DEFAULT_ZONE_POINTS,
                color="#0B6B1B",
                reference_width=1280,
                reference_height=720,
                points_format="normalized",
                required_uniform_id=None,
                created_at=now,
                updated_at=now,
            )
            db.add(zone)
            counts["zones"] += 1

        health = db.scalar(select(CameraHealth).where(CameraHealth.camera_id == camera_id))
        if health is None:
            health = CameraHealth(
                id=new_health_id(),
                farm_id=DEMO_FARM_ID,
                camera_id=camera_id,
                fps=25,
                bitrate=2048.0,
                last_seen=now,
                status=STATUS_ONLINE,
            )
            db.add(health)
            counts["healthRows"] += 1
        else:
            health.status = STATUS_ONLINE
            health.last_seen = now
            health.fps = 25

    db.commit()
    return counts
