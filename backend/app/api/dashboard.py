from app.api.deps import get_current_user
from collections import Counter, defaultdict

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Camera, Event, Farm, User
from app.schemas.dashboard import (
    DashboardSummaryResponse,
    DashboardTopCameraItem,
    DashboardTopZoneItem,
    DashboardTrendItem,
)
from app.schemas.dashboard_bootstrap import DashboardBootstrapResponse
from app.services.atsh_biosecurity_engine import get_atsh_violation_summary
from app.services.dashboard_bootstrap_service import build_dashboard_bootstrap
from app.services.vi_localization import resolve_camera_name, resolve_zone_name

router = APIRouter(prefix="/dashboard", tags=["dashboard"],
    dependencies=[Depends(get_current_user)]
)

_HIGH_SEVERITIES = ("danger", "critical", "high", "CRITICAL")
_OPEN_STATUSES = ("new", "processing")


@router.get("/bootstrap", response_model=DashboardBootstrapResponse)
def dashboard_bootstrap(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> DashboardBootstrapResponse:
    return build_dashboard_bootstrap(db, current_user)


@router.get("/summary", response_model=DashboardSummaryResponse)
def dashboard_summary(db: Session = Depends(get_db)) -> DashboardSummaryResponse:
    tong_camera = db.scalar(select(func.count()).select_from(Camera)) or 0
    camera_truc_tuyen = db.scalar(
        select(func.count()).select_from(Camera).where(Camera.status == "online")
    ) or 0
    tong_trang_trai = db.scalar(select(func.count()).select_from(Farm)) or 0
    tong_su_kien = db.scalar(select(func.count()).select_from(Event)) or 0
    su_kien_rui_ro_cao = db.scalar(
        select(func.count()).select_from(Event).where(Event.severity.in_(_HIGH_SEVERITIES))
    ) or 0
    su_kien_dang_mo = db.scalar(
        select(func.count()).select_from(Event).where(Event.status.in_(_OPEN_STATUSES))
    ) or 0
    atsh_summary = get_atsh_violation_summary(db)

    return DashboardSummaryResponse(
        tong_camera=tong_camera,
        tong_trang_trai=tong_trang_trai,
        tong_canh_bao_ai=tong_su_kien,
        camera_truc_tuyen=camera_truc_tuyen,
        tong_su_kien=tong_su_kien,
        su_kien_rui_ro_cao=su_kien_rui_ro_cao,
        su_kien_dang_mo=su_kien_dang_mo,
        tong_vi_pham_atsh=atsh_summary["tong_vi_pham_atsh"],
        vi_pham_atsh_hom_nay=atsh_summary["vi_pham_hom_nay"],
        vi_pham_atsh_info=atsh_summary["theo_muc_do"]["INFO"],
        vi_pham_atsh_warning=atsh_summary["theo_muc_do"]["WARNING"],
        vi_pham_atsh_critical=atsh_summary["theo_muc_do"]["CRITICAL"],
        top_quy_tac_atsh=atsh_summary["top_quy_tac"],
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
