from app.api.deps import get_current_user
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.compliance.constants import COMPLIANCE_RULE_IDS
from app.database.session import get_db
from app.models import Camera, Event
from app.schemas.event import EventEngineResponse, PaginatedEventsResponse
from app.services.event_engine_service import event_to_engine_dict
from app.services.event_query_service import query_events_all, query_events_paginated
from app.services.vi_localization import resolve_camera_name, resolve_severity_label, resolve_zone_name

router = APIRouter(prefix="/compliance", tags=["compliance"],
    dependencies=[Depends(get_current_user)]
)

COMPLIANCE_EVENT_TYPES = set(COMPLIANCE_RULE_IDS.values())

SEVERITY_PENALTY = {
    "CRITICAL": 8,
    "critical": 8,
    "high": 5,
    "danger": 5,
    "HIGH": 5,
    "warning": 2,
    "medium": 2,
    "low": 1,
    "info": 1,
}


def _violation_events(db: Session) -> list[Event]:
    return list(
        db.scalars(
            select(Event).where(
                Event.category.notin_(
                    {"camera_offline", "pig_fever", "pig_abnormal", "improper_clothing"}
                )
            )
        )
    )


def _score(events: list[Event]) -> int:
    penalty = sum(SEVERITY_PENALTY.get(event.severity, 1) for event in events)
    return max(0, min(100, 100 - penalty))


def _today_key() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def _trend(events: list[Event], days: int) -> list[dict]:
    counts = Counter(event.occurred_at[:10] for event in events)
    keys = sorted(counts.keys())[-days:]
    return [{"ngay": key, "vi_pham": counts[key]} for key in keys]


@router.get("/summary")
def compliance_summary(db: Session = Depends(get_db)) -> dict:
    events = _violation_events(db)
    today = _today_key()
    today_events = [event for event in events if event.occurred_at.startswith(today)]
    top_cameras = Counter(event.camera_id for event in events).most_common(5)

    return {
        "diem_atsh": _score(events),
        "vi_pham_hom_nay": len(today_events),
        "tong_vi_pham": len(events),
        "nghiem_trong": sum(
            1 for event in events if event.severity in {"critical", "danger", "CRITICAL"}
        ),
        "muc_cao": sum(1 for event in events if event.severity in {"high", "danger"}),
        "canh_bao": sum(1 for event in events if event.severity in {"warning", "medium"}),
        "camera_rui_ro_cao": [
            {
                "camera_id": camera_id,
                "ten_camera": resolve_camera_name(db, camera_id),
                "ten_vung": resolve_zone_name(db, db.get(Camera, camera_id).zone if db.get(Camera, camera_id) else ""),
                "so_vi_pham": total,
            }
            for camera_id, total in top_cameras
        ],
    }


@router.get("/trends")
def compliance_trends(db: Session = Depends(get_db)) -> dict:
    events = _violation_events(db)
    return {
        "xu_huong_7_ngay": _trend(events, 7),
        "xu_huong_30_ngay": _trend(events, 30),
    }


@router.get("/top-zones")
def compliance_top_zones(db: Session = Depends(get_db)) -> list[dict]:
    by_zone = defaultdict(lambda: {"so_vi_pham": 0, "nghiem_trong": 0, "muc_cao": 0, "canh_bao": 0})
    for event in _violation_events(db):
        zone_name = resolve_zone_name(db, event.zone)
        by_zone[zone_name]["so_vi_pham"] += 1
        if event.severity in {"critical", "danger"}:
            by_zone[zone_name]["nghiem_trong"] += 1
        elif event.severity == "high":
            by_zone[zone_name]["muc_cao"] += 1
        elif event.severity in {"warning", "medium"}:
            by_zone[zone_name]["canh_bao"] += 1

    return [
        {"ten_vung": zone, **stats}
        for zone, stats in sorted(by_zone.items(), key=lambda item: item[1]["so_vi_pham"], reverse=True)[:5]
    ]


@router.get("/top-violations")
def compliance_top_violations(db: Session = Depends(get_db)) -> list[dict]:
    by_type = defaultdict(lambda: {"so_vi_pham": 0, "muc_do": "Cảnh báo"})
    for event in _violation_events(db):
        label = event.alert_type
        by_type[label]["so_vi_pham"] += 1
        by_type[label]["muc_do"] = resolve_severity_label(event.severity)

    return [
        {"ten_vi_pham": violation_type, **stats}
        for violation_type, stats in sorted(by_type.items(), key=lambda item: item[1]["so_vi_pham"], reverse=True)[:5]
    ]


@router.get("/events", response_model=PaginatedEventsResponse)
def list_compliance_events(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=50, ge=1, le=200),
    eventType: Optional[str] = Query(default=None),
    cameraId: Optional[str] = Query(default=None),
    zoneId: Optional[str] = Query(default=None),
    date: Optional[str] = Query(default=None, description="YYYY-MM-DD"),
    db: Session = Depends(get_db),
) -> PaginatedEventsResponse:
    if eventType and eventType not in COMPLIANCE_EVENT_TYPES:
        return PaginatedEventsResponse(items=[], total=0, page=page, limit=limit)

    rows, total = query_events_paginated(
        db,
        page=page,
        limit=limit,
        event_type=eventType,
        camera_id=cameraId,
        zone_id=zoneId,
        event_types=COMPLIANCE_EVENT_TYPES if not eventType else None,
        date_prefix=date,
    )
    items = [EventEngineResponse(**event_to_engine_dict(db, event)) for event in rows]
    return PaginatedEventsResponse(items=items, total=total, page=page, limit=limit)


@router.get("/events/summary")
def compliance_events_summary(
    date: Optional[str] = Query(default=None, description="YYYY-MM-DD, default today UTC"),
    db: Session = Depends(get_db),
) -> dict:
    date_prefix = date or _today_key()
    events = query_events_all(
        db,
        event_types=COMPLIANCE_EVENT_TYPES,
        date_prefix=date_prefix,
    )
    by_type = Counter(event.event_type or "UNKNOWN" for event in events)
    return {
        "date": date_prefix,
        "total": len(events),
        "uniform_violation": by_type.get(COMPLIANCE_RULE_IDS["UNIFORM_VIOLATION"], 0),
        "zone_intrusion": by_type.get(COMPLIANCE_RULE_IDS["ZONE_INTRUSION"], 0),
        "animal_intrusion": by_type.get(COMPLIANCE_RULE_IDS["ANIMAL_INTRUSION"], 0),
        "vehicle_intrusion": by_type.get(COMPLIANCE_RULE_IDS["VEHICLE_INTRUSION"], 0),
        "no_hand_sanitization": by_type.get(COMPLIANCE_RULE_IDS["NO_HAND_SANITIZATION"], 0),
        "no_boot_sanitization": by_type.get(COMPLIANCE_RULE_IDS["NO_BOOT_SANITIZATION"], 0),
        "biosecurity_process_violation": by_type.get(COMPLIANCE_RULE_IDS["BIOSECURITY_PROCESS_VIOLATION"], 0),
    }
