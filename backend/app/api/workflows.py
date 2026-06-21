from app.api.deps import get_current_user
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.farm_access import assert_farm_access, resolve_farm_scope
from app.core.permissions import require_permission
from app.core.roles import DEFAULT_FARM_ID
from app.data.workflow_defaults import DEFAULT_PERSON_ENTRY_WORKFLOW, WORKFLOW_VIOLATION_CODES
from app.database.session import get_db
from app.models import User, Workflow, WorkflowStep
from app.schemas.workflow import (
    WorkflowComplianceSummary,
    WorkflowCreate,
    WorkflowDashboardResponse,
    WorkflowHistoryItem,
    WorkflowResponse,
    WorkflowStepResponse,
    WorkflowUpdate,
    WorkflowViolationType,
)
from app.services.atsh_pipeline import atsh_pipeline
from app.services.workflow_engine import (
    get_compliance_summary,
    get_workflow_dashboard,
    get_workflow_history,
)
from app.services.audit import write_audit_log

router = APIRouter(prefix="/workflows", tags=["workflows"],
    dependencies=[Depends(get_current_user)]
)


def _step_response(step: WorkflowStep) -> WorkflowStepResponse:
    return WorkflowStepResponse(
        id=step.id,
        workflow_id=step.workflow_id,
        step_order=step.step_order,
        step_name=step.step_name,
        zone_code=step.zone_code,
        required=step.required,
        thu_tu=step.step_order,
        zone_type=step.zone_code,
        ten_buoc=step.step_name,
        bat_buoc=step.required,
    )


def _load_workflow_response(db: Session, workflow: Workflow) -> WorkflowResponse:
    steps = list(
        db.scalars(
            select(WorkflowStep)
            .where(WorkflowStep.workflow_id == workflow.id)
            .order_by(WorkflowStep.step_order, WorkflowStep.id)
        )
    )
    return WorkflowResponse(
        id=workflow.id,
        name=workflow.name,
        description=workflow.description,
        object_type=workflow.object_type,
        enabled=workflow.enabled,
        created_at=workflow.created_at,
        ten_quy_trinh=workflow.name,
        mo_ta=workflow.description,
        kich_hoat=workflow.enabled,
        steps=[_step_response(step) for step in steps],
    )


def _get_workflow_or_404(workflow_id: str, db: Session) -> Workflow:
    workflow = db.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workflow not found")
    return workflow


@router.get("/compliance/summary", response_model=WorkflowComplianceSummary)
def workflow_compliance_summary(
    workflow_id: str = DEFAULT_PERSON_ENTRY_WORKFLOW["id"],
    db: Session = Depends(get_db),
) -> WorkflowComplianceSummary:
    try:
        return WorkflowComplianceSummary(**get_compliance_summary(db, workflow_id))
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/violation-types", response_model=list[WorkflowViolationType])
def list_workflow_violation_types() -> list[WorkflowViolationType]:
    return [
        WorkflowViolationType(ma=code, ten=label)
        for code, label in WORKFLOW_VIOLATION_CODES.items()
    ]


@router.get("/pipeline")
def workflow_pipeline_status() -> dict:
    return {
        "version": "v3.1",
        "engines": atsh_pipeline.registered_engines,
        "next": ["route_engine_v32", "contact_risk_engine_v33", "atsh_score_engine_v34"],
    }


@router.get("/dashboard", response_model=WorkflowDashboardResponse)
def workflow_dashboard(db: Session = Depends(get_db)) -> WorkflowDashboardResponse:
    return WorkflowDashboardResponse(**get_workflow_dashboard(db))


@router.get("/history", response_model=list[WorkflowHistoryItem])
def workflow_history(
    workflow_id: Optional[str] = Query(default=None),
    track_id: Optional[int] = Query(default=None),
    limit: int = Query(default=50, ge=1, le=200),
    db: Session = Depends(get_db),
) -> list[WorkflowHistoryItem]:
    return [WorkflowHistoryItem(**item) for item in get_workflow_history(db, workflow_id=workflow_id, track_id=track_id, limit=limit)]


@router.get("", response_model=list[WorkflowResponse])
def list_workflows(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("workflow.read")),
) -> list[WorkflowResponse]:
    scope = resolve_farm_scope(current_user)
    query = select(Workflow).order_by(Workflow.id)
    if scope:
        query = query.where(Workflow.farm_id == scope)
    workflows = list(db.scalars(query))
    return [_load_workflow_response(db, workflow) for workflow in workflows]


@router.get("/definitions/biosecurity")
def list_biosecurity_workflow_definitions() -> list[dict]:
    from app.biosecurity_workflow.workflow_manager import get_workflow_manager

    return [
        {
            "id": definition.id,
            "name": definition.name,
            "steps": definition.steps,
        }
        for definition in get_workflow_manager().list_definitions()
    ]


@router.get("/{workflow_id}", response_model=WorkflowResponse)
def get_workflow(workflow_id: str, db: Session = Depends(get_db)) -> WorkflowResponse:
    return _load_workflow_response(db, _get_workflow_or_404(workflow_id, db))


@router.post("", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
def create_workflow(
    payload: WorkflowCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("workflow.manage")),
) -> WorkflowResponse:
    workflow_id = payload.id or f"WF-{uuid.uuid4().hex[:8].upper()}"
    if db.get(Workflow, workflow_id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Workflow id already exists")

    farm_id = getattr(payload, "farm_id", None) or current_user.farm_id or DEFAULT_FARM_ID
    assert_farm_access(current_user, farm_id)

    workflow = Workflow(
        id=workflow_id,
        farm_id=farm_id,
        name=payload.name,
        description=payload.description,
        object_type=payload.object_type.lower(),
        enabled=payload.enabled,
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    db.add(workflow)
    for step in payload.steps:
        db.add(
            WorkflowStep(
                id=f"WFS-{uuid.uuid4().hex[:8].upper()}",
                workflow_id=workflow_id,
                step_order=step.step_order,
                step_name=step.step_name,
                zone_code=step.zone_code,
                required=step.required,
            )
        )
    write_audit_log(
        db,
        user_id=current_user.id,
        action="create_workflow",
        resource_type="workflow",
        resource_id=workflow_id,
        farm_id=farm_id,
        metadata={"name": payload.name},
    )
    db.commit()
    return _load_workflow_response(db, workflow)


@router.put("/{workflow_id}", response_model=WorkflowResponse)
def update_workflow(
    workflow_id: str,
    payload: WorkflowUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("workflow.manage")),
) -> WorkflowResponse:
    workflow = _get_workflow_or_404(workflow_id, db)
    assert_farm_access(current_user, workflow.farm_id)
    values = payload.model_dump(exclude_unset=True)
    steps = values.pop("steps", None)
    for field, value in values.items():
        if field == "object_type" and value is not None:
            value = value.lower()
        setattr(workflow, field, value)

    if steps is not None:
        existing_steps = list(db.scalars(select(WorkflowStep).where(WorkflowStep.workflow_id == workflow_id)))
        for step in existing_steps:
            db.delete(step)
        for step in steps:
            step_data = step if isinstance(step, dict) else step.model_dump()
            db.add(
                WorkflowStep(
                    id=f"WFS-{uuid.uuid4().hex[:8].upper()}",
                    workflow_id=workflow_id,
                    step_order=step_data["step_order"],
                    step_name=step_data["step_name"],
                    zone_code=step_data["zone_code"],
                    required=step_data.get("required", True),
                )
            )

    db.add(workflow)
    write_audit_log(
        db,
        user_id=current_user.id,
        action="update_workflow",
        resource_type="workflow",
        resource_id=workflow.id,
        farm_id=workflow.farm_id,
        metadata={"fields": list(values.keys()) if steps is None else list(values.keys()) + ["steps"]},
    )
    db.commit()
    db.refresh(workflow)
    return _load_workflow_response(db, workflow)


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workflow(
    workflow_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("workflow.manage")),
) -> None:
    workflow = _get_workflow_or_404(workflow_id, db)
    assert_farm_access(current_user, workflow.farm_id)
    steps = list(db.scalars(select(WorkflowStep).where(WorkflowStep.workflow_id == workflow_id)))
    for step in steps:
        db.delete(step)
    write_audit_log(
        db,
        user_id=current_user.id,
        action="delete_workflow",
        resource_type="workflow",
        resource_id=workflow.id,
        farm_id=workflow.farm_id,
        metadata={"name": workflow.name},
    )
    db.delete(workflow)
    db.commit()
