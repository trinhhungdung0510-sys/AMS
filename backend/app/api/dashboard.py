from collections import Counter, defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Camera, Event, Farm
from app.schemas.dashboard import (
    DashboardSummaryResponse,
    DashboardTopCameraItem,
    DashboardTopZoneItem,
    DashboardTrendItem,
)
from app.services.vi_localization import resolve_camera_name, resolve_zone_name

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummaryResponse)
def dashboard_summary(db: Session = Depends(get_db)) -> DashboardSummaryResponse:
    cameras = list(db.scalars(select(Camera)))
    events = list(db.scalars(select(Event)))
    farms = list(db.scalars(select(Farm)))
    high_events = [event for event in events if event.severity in {"danger", "critical", "high"}]

    return DashboardSummaryResponse(
        tong_camera=len(cameras),
        tong_trang_trai=len(farms),
        tong_canh_bao_ai=len(events),
        camera_truc_tuyen=sum(1 for camera in cameras if camera.status == "online"),
        tong_su_kien=len(events),
        su_kien_rui_ro_cao=len(high_events),
        su_kien_dang_mo=sum(1 for event in events if event.status in {"new", "processing"}),
    )


@router.get("/trends", response_model=list[DashboardTrendItem])
def dashboard_trends(db: Session = Depends(get_db)) -> list[DashboardTrendItem]:
    events = list(db.scalars(select(Event)))
    counts = Counter(event.occurred_at[:10] for event in events)
    return [
        DashboardTrendItem(ngay=date, su_kien=counts[date])
        for date in sorted(counts.keys())[-7:]
    ]


@router.get("/top-cameras", response_model=list[DashboardTopCameraItem])
def dashboard_top_cameras(db: Session = Depends(get_db)) -> list[DashboardTopCameraItem]:
    cameras = {camera.id: camera for camera in db.scalars(select(Camera))}
    counts = Counter(event.camera_id for event in db.scalars(select(Event)))
    items = []
    for camera_id, total in counts.most_common(5):
        if camera_id not in cameras:
            continue
        camera = cameras[camera_id]
        items.append(
            DashboardTopCameraItem(
                camera_id=camera_id,
                ten_camera=resolve_camera_name(db, camera_id),
                ten_vung=resolve_zone_name(db, camera.zone),
                so_su_kien=total,
            )
        )
    return items


@router.get("/top-zones", response_model=list[DashboardTopZoneItem])
def dashboard_top_zones(db: Session = Depends(get_db)) -> list[DashboardTopZoneItem]:
    events = list(db.scalars(select(Event)))
    by_zone = defaultdict(lambda: {"events": 0, "critical": 0})
    for event in events:
        zone_name = resolve_zone_name(db, event.zone)
        by_zone[zone_name]["events"] += 1
        if event.severity in {"danger", "critical", "high"}:
            by_zone[zone_name]["critical"] += 1

    return [
        DashboardTopZoneItem(
            ten_vung=zone,
            so_su_kien=stats["events"],
            nghiem_trong=stats["critical"],
        )
        for zone, stats in sorted(
            by_zone.items(),
            key=lambda item: item[1]["events"],
            reverse=True,
        )[:5]
    ]
