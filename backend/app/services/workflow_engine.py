import json
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.data.workflow_defaults import (
    VIOLATION_CODE_BY_ZONE,
    WORKFLOW_VIOLATION_CODES,
)
from app.models import (
    AuditLog,
    Camera,
    Event,
    PersonTrack,
    TrackWorkflowProgress,
    Workflow,
    WorkflowStep,
    ZoneTransition,
)
from app.services.audit import write_audit_log
from app.services.snapshot_generator import SnapshotAnnotation, create_event_snapshot
from app.services.vi_localization import resolve_severity_label, resolve_zone_name

DEFAULT_CAMERA_ID = "CAM-001"


def record_person_track(db: Session, transition: ZoneTransition) -> PersonTrack:
    open_visit = db.scalar(
        select(PersonTrack)
        .where(PersonTrack.track_id == transition.track_id)
        .where(PersonTrack.camera_id == transition.camera_id)
        .where(PersonTrack.exit_time.is_(None))
        .order_by(PersonTrack.enter_time.desc(), PersonTrack.id.desc())
        .limit(1)
    )
    if open_visit and open_visit.zone_id == transition.to_zone:
        return open_visit

    if open_visit:
        open_visit.exit_time = transition.cross_time
        db.add(open_visit)

    visit = PersonTrack(
        id=f"PT-{uuid.uuid4().hex[:10].upper()}",
        track_id=transition.track_id,
        camera_id=transition.camera_id,
        zone_id=transition.to_zone,
        enter_time=transition.cross_time,
        exit_time=None,
    )
    db.add(visit)
    return visit


def evaluate_workflow(db: Session, transition: ZoneTransition) -> Optional[dict]:
    if transition.object_type.lower() != "person":
        return None

    record_person_track(db, transition)

    workflows = list(
        db.scalars(
            select(Workflow)
            .where(Workflow.enabled.is_(True))
            .where(Workflow.object_type == "person")
            .order_by(Workflow.id)
        )
    )
    if not workflows:
        return None

    last_violation = None
    for workflow in workflows:
        violation = _evaluate_single_workflow(db, transition, workflow)
        if violation:
            last_violation = violation
    return last_violation


def get_workflow_history(
    db: Session,
    *,
    workflow_id: Optional[str] = None,
    track_id: Optional[int] = None,
    limit: int = 50,
) -> list[dict]:
    events = list(
        db.scalars(
            select(Event)
            .where(Event.category == "workflow_violation")
            .order_by(Event.occurred_at.desc(), Event.id.desc())
            .limit(limit * 3)
        )
    )
    history = []
    for event in events:
        audit = db.scalar(
            select(AuditLog)
            .where(AuditLog.action == "workflow_violation")
            .where(AuditLog.metadata_json.like(f'%"event_id": "{event.id}"%'))
            .limit(1)
        )
        metadata = json.loads(audit.metadata_json) if audit else {}
        if workflow_id and metadata.get("workflow_id") != workflow_id:
            continue
        if track_id is not None and metadata.get("track_id") != track_id:
            continue

        resolved_track_id = metadata.get("track_id")
        zones_visited = (
            _load_zone_history(db, track_id=resolved_track_id) if resolved_track_id is not None else []
        )
        history.append(
            {
                "event_id": event.id,
                "workflow_id": metadata.get("workflow_id"),
                "ten_quy_trinh": metadata.get("workflow_name"),
                "track_id": resolved_track_id,
                "loai_vi_pham": event.violation_code,
                "ten_vi_pham": WORKFLOW_VIOLATION_CODES.get(
                    event.violation_code or "",
                    event.alert_type,
                ),
                "ten_vung": resolve_zone_name(db, event.zone),
                "muc_do": resolve_severity_label(event.severity),
                "thoi_gian": event.occurred_at,
                "cac_vung_da_di": zones_visited,
                "camera_id": event.camera_id,
            }
        )
        if len(history) >= limit:
            break
    return history


def get_workflow_dashboard(db: Session) -> dict:
    today_prefix = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    today_violations = list(
        db.scalars(
            select(Event)
            .where(Event.category == "workflow_violation")
            .where(Event.occurred_at.like(f"{today_prefix}%"))
            .order_by(Event.occurred_at.desc())
        )
    )

    workflow_counts: dict[str, int] = {}
    for event in today_violations:
        workflow_name = _extract_workflow_name(event.alert_type)
        workflow_counts[workflow_name] = workflow_counts.get(workflow_name, 0) + 1

    top_workflows = sorted(
        (
            {"ten_quy_trinh": name, "so_vi_pham": count}
            for name, count in workflow_counts.items()
        ),
        key=lambda item: item["so_vi_pham"],
        reverse=True,
    )

    return {
        "vi_pham_hom_nay": len(today_violations),
        "top_quy_trinh_bi_vi_pham": top_workflows[:5],
        "chi_tiet_hom_nay": [
            {
                "event_id": event.id,
                "loai_vi_pham": event.violation_code,
                "ten_vi_pham": WORKFLOW_VIOLATION_CODES.get(
                    event.violation_code or "",
                    event.alert_type,
                ),
                "ten_vung": resolve_zone_name(db, event.zone),
                "thoi_gian": event.occurred_at,
            }
            for event in today_violations[:10]
        ],
    }


def get_track_detail(db: Session, track_id: int, camera_id: Optional[str] = None) -> dict:
    query = (
        select(PersonTrack)
        .where(PersonTrack.track_id == track_id)
        .order_by(PersonTrack.enter_time.asc(), PersonTrack.id.asc())
    )
    if camera_id:
        query = query.where(PersonTrack.camera_id == camera_id)

    visits = list(db.scalars(query))
    return {
        "track_id": track_id,
        "camera_id": camera_id or (visits[0].camera_id if visits else None),
        "lich_su_vung": [
            {
                "id": visit.id,
                "zone_id": visit.zone_id,
                "ten_vung": resolve_zone_name(db, visit.zone_id),
                "enter_time": visit.enter_time,
                "exit_time": visit.exit_time,
            }
            for visit in visits
        ],
    }


def get_compliance_summary(db: Session, workflow_id: str) -> dict:
    workflow = db.get(Workflow, workflow_id)
    if not workflow:
        raise ValueError("Workflow not found")

    steps = _load_steps(db, workflow_id)
    progress_rows = list(
        db.scalars(select(TrackWorkflowProgress).where(TrackWorkflowProgress.workflow_id == workflow_id))
    )
    final_step_order = steps[-1].step_order if steps else 0
    compliant_tracks = sum(1 for row in progress_rows if row.completed_step_order >= final_step_order)

    violations = list(
        db.scalars(
            select(Event)
            .where(Event.category == "workflow_violation")
            .where(Event.alert_type.like(f"%{workflow.name}%"))
            .order_by(Event.occurred_at.desc())
            .limit(20)
        )
    )
    workflow_violations = []
    for event in violations:
        workflow_violations.append(
            {
                "event_id": event.id,
                "loai_vi_pham": event.violation_code,
                "ten_vi_pham": WORKFLOW_VIOLATION_CODES.get(
                    event.violation_code or "",
                    event.alert_type,
                ),
                "ten_vung": resolve_zone_name(db, event.zone),
                "muc_do": resolve_severity_label(event.severity),
                "thoi_gian": event.occurred_at,
            }
        )

    total_tracks = len(progress_rows)
    violation_count = len(workflow_violations)
    compliance_score = 100
    if total_tracks:
        compliance_score = max(0, min(100, int((compliant_tracks / total_tracks) * 100)))

    dashboard = get_workflow_dashboard(db)

    return {
        "workflow_id": workflow.id,
        "workflow_name": workflow.name,
        "ten_quy_trinh": workflow.name,
        "compliance_score": compliance_score,
        "total_tracks": total_tracks,
        "compliant_tracks": compliant_tracks,
        "violation_count": violation_count,
        "vi_pham_hom_nay": dashboard["vi_pham_hom_nay"],
        "top_quy_trinh_bi_vi_pham": dashboard["top_quy_trinh_bi_vi_pham"],
        "expected_steps": [step.step_name for step in steps],
        "recent_violations": workflow_violations[:5],
    }


def _evaluate_single_workflow(
    db: Session,
    transition: ZoneTransition,
    workflow: Workflow,
) -> Optional[dict]:
    steps = _load_steps(db, workflow.id)
    if not steps:
        return None

    matched_step = _match_step(steps, transition.to_zone)
    if matched_step is None:
        return None

    progress = _get_or_create_progress(db, transition, workflow.id)
    next_expected_order = progress.completed_step_order + 1
    final_step_order = steps[-1].step_order

    if matched_step.step_order <= progress.completed_step_order:
        progress.last_zone = transition.to_zone
        progress.updated_at = transition.cross_time
        db.add(progress)
        return None

    if matched_step.step_order == next_expected_order:
        progress.completed_step_order = matched_step.step_order
        progress.last_zone = transition.to_zone
        progress.updated_at = transition.cross_time
        db.add(progress)
        return None

    if matched_step.step_order != final_step_order:
        return None

    skipped_steps = [
        step
        for step in steps
        if step.required
        and progress.completed_step_order < step.step_order < matched_step.step_order
    ]
    if not skipped_steps:
        return None

    return _create_violations(
        db,
        transition=transition,
        workflow=workflow,
        skipped_steps=skipped_steps,
        attempted_step=matched_step.step_name,
    )


def _create_violations(
    db: Session,
    *,
    transition: ZoneTransition,
    workflow: Workflow,
    skipped_steps: list[WorkflowStep],
    attempted_step: str,
) -> dict:
    violation_codes = _resolve_violation_codes(skipped_steps)
    last_payload = None
    for violation_code in violation_codes:
        last_payload = _create_violation(
            db,
            transition=transition,
            workflow=workflow,
            skipped_steps=[step.step_name for step in skipped_steps],
            attempted_step=attempted_step,
            violation_code=violation_code,
        )
    return last_payload or {}


def _create_violation(
    db: Session,
    *,
    transition: ZoneTransition,
    workflow: Workflow,
    skipped_steps: list[str],
    attempted_step: str,
    violation_code: str,
) -> dict:
    camera = db.get(Camera, transition.camera_id) or db.get(Camera, DEFAULT_CAMERA_ID)
    event_id = f"EVT-WF-{uuid.uuid4().hex[:8].upper()}"
    snapshot_id = f"SNP-WF-{uuid.uuid4().hex[:8].upper()}"
    violation_label = WORKFLOW_VIOLATION_CODES.get(violation_code, violation_code)
    alert_type = f"{workflow.name}: {violation_label}"[:120]

    event = Event(
        id=event_id,
        farm_id=camera.farm_id if camera else "FARM-001",
        camera_id=camera.id if camera else transition.camera_id,
        category="workflow_violation",
        alert_type=alert_type,
        zone=transition.to_zone,
        severity="critical",
        status="new",
        handler="Chưa phân công",
        confidence=99,
        occurred_at=transition.cross_time,
        violation_code=violation_code,
    )
    snapshot = create_event_snapshot(
        event_id=event_id,
        snapshot_id=snapshot_id,
        storage_category="workflow",
        annotation=SnapshotAnnotation(
            object_label=transition.object_type,
            zone_name=resolve_zone_name(db, transition.to_zone),
            rule_name=workflow.name,
            timestamp=transition.cross_time,
            severity="critical",
            track_id=transition.track_id,
            confidence=99,
        ),
    )
    db.add(event)
    db.add(snapshot)
    write_audit_log(
        db,
        user_id="SYSTEM",
        action="workflow_violation",
        resource_type="zone_transition",
        resource_id=transition.id,
        metadata={
            "workflow_id": workflow.id,
            "workflow_name": workflow.name,
            "violation_code": violation_code,
            "skipped_steps": skipped_steps,
            "attempted_step": attempted_step,
            "event_id": event_id,
            "snapshot_id": snapshot_id,
            "track_id": transition.track_id,
            "camera_id": transition.camera_id,
            "from_zone": transition.from_zone,
            "to_zone": transition.to_zone,
        },
    )

    return {
        "type": "workflow_violation",
        "workflow_id": workflow.id,
        "workflow_name": workflow.name,
        "violation_code": violation_code,
        "loai_vi_pham": violation_code,
        "ten_vi_pham": violation_label,
        "severity": "critical",
        "skipped_steps": skipped_steps,
        "attempted_step": attempted_step,
        "event_id": event_id,
        "snapshot_id": snapshot_id,
        "transition_id": transition.id,
        "track_id": transition.track_id,
        "camera_id": transition.camera_id,
        "from_zone": transition.from_zone,
        "to_zone": transition.to_zone,
        "occurred_at": transition.cross_time,
        "notification": {
            "email": True,
            "telegram": True,
            "zalo": True,
        },
    }


def _resolve_violation_codes(skipped_steps: list[WorkflowStep]) -> list[str]:
    codes: list[str] = []
    for step in skipped_steps:
        code = VIOLATION_CODE_BY_ZONE.get(step.zone_code, "DI_SAI_QUY_TRINH")
        if code not in codes:
            codes.append(code)
    return codes or ["DI_SAI_QUY_TRINH"]


def _load_zone_history(db: Session, *, track_id: int) -> list[dict]:
    visits = list(
        db.scalars(
            select(PersonTrack)
            .where(PersonTrack.track_id == track_id)
            .order_by(PersonTrack.enter_time.asc(), PersonTrack.id.asc())
        )
    )
    return [
        {
            "zone_id": visit.zone_id,
            "ten_vung": resolve_zone_name(db, visit.zone_id),
            "enter_time": visit.enter_time,
            "exit_time": visit.exit_time,
        }
        for visit in visits
    ]


def _extract_workflow_name(alert_type: str) -> str:
    if ":" in alert_type:
        return alert_type.split(":", 1)[0].strip()
    return alert_type


def _load_steps(db: Session, workflow_id: str) -> list[WorkflowStep]:
    return list(
        db.scalars(
            select(WorkflowStep)
            .where(WorkflowStep.workflow_id == workflow_id)
            .order_by(WorkflowStep.step_order, WorkflowStep.id)
        )
    )


def _match_step(steps: list[WorkflowStep], zone_code: str) -> Optional[WorkflowStep]:
    for step in steps:
        if step.zone_code == zone_code:
            return step
    return None


def _get_or_create_progress(
    db: Session,
    transition: ZoneTransition,
    workflow_id: str,
) -> TrackWorkflowProgress:
    progress_id = f"TWP-{transition.camera_id}-{transition.track_id}-{workflow_id}"
    progress = db.get(TrackWorkflowProgress, progress_id)
    if progress is None:
        progress = TrackWorkflowProgress(
            id=progress_id,
            track_id=transition.track_id,
            camera_id=transition.camera_id,
            workflow_id=workflow_id,
            completed_step_order=0,
            last_zone=transition.from_zone,
            updated_at=transition.cross_time,
        )
        db.add(progress)
    return progress
