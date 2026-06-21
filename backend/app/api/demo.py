from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.database.session import get_db
from app.services.demo_data_generator import generate_demo_violations
from app.services.demo_event_generator import demo_event_generator
from app.services.demo_mode_service import is_demo_mode

router = APIRouter(prefix="/demo", tags=["demo"], dependencies=[Depends(get_current_user)])


def _ensure_demo_mode(db: Session) -> None:
    if not is_demo_mode(db):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Demo mode is disabled. Set DEMO_MODE=true or enable in system settings.",
        )


@router.post("/generate-violations")
def seed_demo_violations(
    count: int = Query(default=12, ge=1, le=50),
    publish: bool = Query(default=True),
    db: Session = Depends(get_db),
) -> dict:
    _ensure_demo_mode(db)
    events = generate_demo_violations(db, count=count, publish=publish, use_today=True)
    return {
        "generated": len(events),
        "eventIds": [event.id for event in events],
    }


@router.post("/start")
async def start_demo(db: Session = Depends(get_db)) -> dict:
    _ensure_demo_mode(db)
    seeded = demo_event_generator.seed_baseline(db, count=get_settings().demo_seed_count, publish=True)
    await demo_event_generator.start()
    return {
        "running": demo_event_generator.is_running,
        "seeded": seeded,
        "complianceScore": demo_event_generator.current_compliance_score(),
    }


@router.post("/stop")
async def stop_demo(db: Session = Depends(get_db)) -> dict:
    _ensure_demo_mode(db)
    await demo_event_generator.stop()
    return {"running": demo_event_generator.is_running}


@router.get("/status")
def demo_status(db: Session = Depends(get_db)) -> dict:
    settings = get_settings()
    return {
        "demoMode": is_demo_mode(db),
        "envDemoMode": settings.demo_mode,
        "running": demo_event_generator.is_running,
        "eventsGenerated": demo_event_generator.events_generated,
        "complianceScore": demo_event_generator.current_compliance_score(),
        "intervalSeconds": settings.demo_interval_seconds,
        "autoStart": settings.demo_auto_start,
    }
