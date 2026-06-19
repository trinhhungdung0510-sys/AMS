from app.api.deps import get_current_user
import json
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.realtime import dashboard_manager, manager
from app.database.session import get_db
from app.models import AITask
from app.schemas.task import AITaskResponse
from app.services.alert_engine import process_ai_task

router = APIRouter(prefix="/tasks", tags=["ai-tasks"],
    dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=list[AITaskResponse])
def list_tasks(db: Session = Depends(get_db)) -> list[AITask]:
    return list(db.scalars(select(AITask).order_by(AITask.created_at.desc(), AITask.id)))


@router.post("/simulate-alert", response_model=AITaskResponse)
async def simulate_alert(
    camera_id: str = "CAM-001",
    category: str = "restricted_zone_intrusion",
    priority: int = 8,
    db: Session = Depends(get_db),
) -> AITask:
    task = AITask(
        id=f"TASK-{uuid.uuid4().hex[:10].upper()}",
        camera_id=camera_id,
        category=category,
        status="queued",
        priority=priority,
        result=json.dumps({"source": "manual_api"}, ensure_ascii=False),
        created_at=datetime.now(timezone.utc).isoformat(),
    )
    db.add(task)
    db.flush()

    payload = process_ai_task(db, task)
    db.commit()
    db.refresh(task)

    await manager.broadcast(payload)
    await dashboard_manager.broadcast({"type": "dashboard_update", "source": "manual_api"})
    return task
