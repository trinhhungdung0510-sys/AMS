from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.farm_access import resolve_farm_scope
from app.core.roles import normalize_role
from app.data.workflow_defaults import DEFAULT_PERSON_ENTRY_WORKFLOW
from app.models import Camera, CameraHealth, NotificationDelivery, NotificationDispatch, NotificationRule, User, ZoneTransition
from app.schemas.auth import UserMeResponse
from app.schemas.dashboard import DashboardSummaryResponse
from app.schemas.dashboard_bootstrap import DashboardBootstrapResponse
from app.services.atsh_biosecurity_engine import get_atsh_violation_summary
from app.services.camera_health_service import STATUS_DEGRADED, STATUS_OFFLINE, STATUS_ONLINE
from app.services.camera_registry import camera_to_response_dict
from app.services.compliance_report_service import build_dashboard_kpis, build_top_violations
from app.services.deployment_health_service import build_health_report
from app.services.violation_notification_service import (
    CHANNEL_GMAIL,
    get_notification_settings,
    get_pending_gmail_count,
)
from app.services.event_engine_service import events_to_engine_dicts
from app.services.event_query_service import query_events_paginated
from app.services.workflow_engine import get_compliance_summary, get_workflow_dashboard

_HIGH_SEVERITIES = ("danger", "critical", "high", "CRITICAL")
_OPEN_STATUSES = ("new", "processing")
_BOOTSTRAP_EVENT_LIMIT = 100
_BOOTSTRAP_CROSSING_LIMIT = 8


def _build_dashboard_summary(db: Session) -> DashboardSummaryResponse:
    from app.models import Event, Farm

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


def _build_camera_health_summary(db: Session) -> dict:
    health_rows = list(db.scalars(select(CameraHealth)))
    cameras = list(db.scalars(select(Camera).where(Camera.is_active.is_(True))))
    health_by_camera = {row.camera_id: row for row in health_rows}

    online = 0
    offline = 0
    warning = 0

    for camera in cameras:
        row = health_by_camera.get(camera.id)
        status = (row.status if row else camera.status or "").upper()
        if status in {STATUS_ONLINE, "ONLINE"}:
            online += 1
        elif status in {STATUS_DEGRADED, "DEGRADED", "WARNING"}:
            warning += 1
        elif status in {STATUS_OFFLINE, "OFFLINE"} or camera.status == "offline":
            offline += 1
        else:
            online += 1

    return {
        "total": len(cameras),
        "online": online,
        "offline": offline,
        "warning": warning,
    }


def _list_cameras_for_user(db: Session, user: User) -> list[dict]:
    scope = resolve_farm_scope(user)
    query = select(Camera).order_by(Camera.id)
    if scope:
        query = query.where(Camera.farm_id == scope)
    cameras = list(db.scalars(query))
    return [camera_to_response_dict(camera) for camera in cameras]


def _build_recent_crossings(db: Session, *, limit: int = _BOOTSTRAP_CROSSING_LIMIT) -> dict:
    total = db.scalar(select(func.count()).select_from(ZoneTransition)) or 0
    items = list(
        db.scalars(
            select(ZoneTransition)
            .order_by(ZoneTransition.cross_time.desc(), ZoneTransition.id.desc())
            .limit(limit)
        )
    )
    return {
        "total": int(total),
        "items": [
            {
                "id": item.id,
                "camera_id": item.camera_id,
                "track_id": item.track_id,
                "object_type": item.object_type,
                "from_zone": item.from_zone,
                "to_zone": item.to_zone,
                "cross_time": item.cross_time,
            }
            for item in items
        ],
    }


def _today_start_iso() -> str:
    from datetime import datetime, timezone

    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    return today.isoformat()


def _build_gmail_channel_summary(db: Session) -> dict:
    settings = get_notification_settings(db)
    deliveries = list(
        db.scalars(
            select(NotificationDelivery).where(NotificationDelivery.channel == CHANNEL_GMAIL)
        )
    )
    today_start = _today_start_iso()
    sent_today = sum(
        1 for item in deliveries if item.status == "success" and (item.sent_at or "") >= today_start
    )
    errors_today = sum(
        1 for item in deliveries if item.status == "failed" and (item.sent_at or "") >= today_start
    )
    last_delivery = max(deliveries, key=lambda item: item.sent_at or "", default=None)

    dispatch_rows = list(db.scalars(select(NotificationDispatch)))
    delivery_by_event = {item.event_id for item in deliveries if item.channel == CHANNEL_GMAIL}
    pending_db = sum(
        1
        for item in dispatch_rows
        if item.status in {"processing", "partial"}
        and item.event_id not in delivery_by_event
    )

    return {
        "channel": "gmail",
        "connected": bool(settings.get("gmail_connected")),
        "enabled": bool(settings.get("gmail_enabled", True)),
        "sentToday": sent_today,
        "pending": get_pending_gmail_count() + pending_db,
        "errorsToday": errors_today,
        "lastSentAt": last_delivery.sent_at if last_delivery and last_delivery.status == "success" else None,
        "lastStatus": last_delivery.status if last_delivery else None,
    }


def _build_notification_summary(db: Session) -> dict:
    rules = list(db.scalars(select(NotificationRule)))
    enabled = sum(1 for rule in rules if getattr(rule, "enabled", True))
    return {
        "totalRules": len(rules),
        "enabledRules": enabled,
        "gmail": _build_gmail_channel_summary(db),
    }


def build_dashboard_bootstrap(db: Session, user: User) -> DashboardBootstrapResponse:
    workflow_id = DEFAULT_PERSON_ENTRY_WORKFLOW["id"]
    workflow_dashboard = get_workflow_dashboard(db)
    event_rows, event_total = query_events_paginated(
        db,
        page=1,
        limit=_BOOTSTRAP_EVENT_LIMIT,
    )
    event_items = events_to_engine_dicts(db, event_rows)

    try:
        workflow_compliance = get_compliance_summary(
            db,
            workflow_id,
            workflow_dashboard=workflow_dashboard,
        )
    except ValueError:
        workflow_compliance = {
            "workflow_id": workflow_id,
            "workflow_name": DEFAULT_PERSON_ENTRY_WORKFLOW.get("name", workflow_id),
            "compliance_score": 100,
            "expected_steps": [],
            "compliant_tracks": 0,
            "violation_count": 0,
            "recent_violations": [],
            "top_quy_trinh_bi_vi_pham": [],
            "vi_pham_hom_nay": 0,
        }

    return DashboardBootstrapResponse(
        user=UserMeResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            role=normalize_role(user.role),
            farm_id=user.farm_id,
            is_active=user.is_active,
        ),
        dashboardSummary=_build_dashboard_summary(db),
        complianceSummary={
            "kpis": build_dashboard_kpis(db),
            "topViolations": {
                "days": 7,
                "items": build_top_violations(db, days=7, limit=10),
            },
        },
        workflowSummary={
            "compliance": workflow_compliance,
            "dashboard": workflow_dashboard,
            "recentCrossings": _build_recent_crossings(db),
        },
        cameraSummary={
            "health": _build_camera_health_summary(db),
            "cameras": _list_cameras_for_user(db, user),
        },
        recentEvents={
            "items": event_items,
            "total": int(event_total),
            "page": 1,
            "limit": _BOOTSTRAP_EVENT_LIMIT,
        },
        notificationSummary=_build_notification_summary(db),
        systemHealth=build_health_report(db),
    )
