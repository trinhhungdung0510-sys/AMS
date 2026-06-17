import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Employee, Event, ObjectTrack
from app.schemas.object_track import ObjectTrackSyncItem
from app.services.audit import write_audit_log

PRODUCTION_ZONES = {
    "gestation_barn",
    "farrowing_barn",
    "boar_barn",
    "weaning_barn",
    "fattening_barn",
    "quarantine_barn",
}


def sync_tracks(db: Session, items: list[ObjectTrackSyncItem]) -> list[ObjectTrack]:
    synced: list[ObjectTrack] = []
    for item in items:
        track_key = f"TRK-{item.camera_id}-{item.track_id}"
        track = db.get(ObjectTrack, track_key)
        previous_zone = track.current_zone if track else None

        employee_id = item.employee_id
        if not employee_id and item.object_type == "person":
            employee_id = _auto_identify_employee(db, item.current_zone)

        if track is None:
            track = ObjectTrack(
                id=track_key,
                track_id=item.track_id,
                camera_id=item.camera_id,
                object_type=item.object_type,
                current_zone=item.current_zone,
                previous_zone=item.previous_zone,
                employee_id=employee_id,
                enter_time=item.enter_time,
                leave_time=item.leave_time,
                last_seen=item.last_seen,
                confidence=item.confidence,
            )
        else:
            track.object_type = item.object_type
            track.previous_zone = item.previous_zone or track.previous_zone
            track.current_zone = item.current_zone
            track.enter_time = item.enter_time
            track.leave_time = item.leave_time
            track.last_seen = item.last_seen
            track.confidence = item.confidence
            if employee_id:
                track.employee_id = employee_id
            elif track.employee_id is None and item.object_type == "person":
                track.employee_id = _auto_identify_employee(db, item.current_zone)

        db.add(track)
        synced.append(track)

        if (
            track.employee_id
            and previous_zone
            and previous_zone != track.current_zone
        ):
            _evaluate_employee_zone_compliance(db, track)

    return synced


def link_track_to_employee(
    db: Session,
    *,
    track_id: int,
    camera_id: str,
    employee_id: str,
) -> ObjectTrack:
    track_key = f"TRK-{camera_id}-{track_id}"
    track = db.get(ObjectTrack, track_key)
    if not track:
        raise ValueError("Track not found")

    employee = db.get(Employee, employee_id)
    if not employee:
        raise ValueError("Employee not found")

    track.employee_id = employee_id
    db.add(track)
    _evaluate_employee_zone_compliance(db, track)
    return track


def enrich_track_response(db: Session, track: ObjectTrack) -> dict:
    payload = {
        "id": track.id,
        "track_id": track.track_id,
        "camera_id": track.camera_id,
        "object_type": track.object_type,
        "current_zone": track.current_zone,
        "previous_zone": track.previous_zone,
        "employee_id": track.employee_id,
        "employee_code": None,
        "employee_name": None,
        "assigned_zone": None,
        "zone_match": None,
        "enter_time": track.enter_time,
        "leave_time": track.leave_time,
        "last_seen": track.last_seen,
        "confidence": track.confidence,
    }
    if track.employee_id:
        employee = db.get(Employee, track.employee_id)
        if employee:
            payload["employee_code"] = employee.employee_code
            payload["employee_name"] = employee.full_name
            payload["assigned_zone"] = employee.assigned_zone
            payload["zone_match"] = track.current_zone == employee.assigned_zone
    return payload


def _auto_identify_employee(db: Session, current_zone: str) -> Optional[str]:
    if current_zone in {"unknown", "any_zone"}:
        return None

    employees = list(
        db.scalars(
            select(Employee)
            .where(Employee.active.is_(True))
            .where(Employee.assigned_zone == current_zone)
            .order_by(Employee.employee_code)
        )
    )
    if len(employees) == 1:
        return employees[0].id
    return None


def _evaluate_employee_zone_compliance(db: Session, track: ObjectTrack) -> None:
    if not track.employee_id or track.object_type != "person":
        return

    employee = db.get(Employee, track.employee_id)
    if not employee or not employee.active:
        return

    if track.current_zone == employee.assigned_zone:
        return

    if track.current_zone not in PRODUCTION_ZONES and track.current_zone not in {
        employee.assigned_zone,
        "person_disinfection_zone",
        "shower_room",
        "handwash_zone",
        "boot_disinfection_tray",
    }:
        return

    event_id = f"EVT-EMP-{uuid.uuid4().hex[:8].upper()}"
    event = Event(
        id=event_id,
        farm_id="FARM-001",
        camera_id=track.camera_id,
        category="employee_wrong_zone",
        alert_type=f"Nhân viên {employee.full_name} sai khu vực"[:80],
        zone=track.current_zone,
        severity="warning",
        status="new",
        handler=employee.full_name,
        confidence=int(track.confidence or 90),
        occurred_at=track.last_seen,
    )
    db.add(event)
    write_audit_log(
        db,
        user_id="SYSTEM",
        action="employee_zone_violation",
        resource_type="object_track",
        resource_id=track.id,
        metadata={
            "event_id": event_id,
            "employee_id": employee.id,
            "employee_code": employee.employee_code,
            "assigned_zone": employee.assigned_zone,
            "current_zone": track.current_zone,
            "track_id": track.track_id,
            "camera_id": track.camera_id,
        },
    )
