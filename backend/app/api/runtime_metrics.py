from app.api.deps import get_current_user
from fastapi import APIRouter, Depends

from app.core.detectors import get_detector_registry
from app.database.session import get_db
from app.services.runtime_metrics_service import runtime_metrics
from sqlalchemy.orm import Session

router = APIRouter(prefix="/runtime", tags=["runtime"], dependencies=[Depends(get_current_user)])


@router.get("/metrics")
def get_runtime_metrics(db: Session = Depends(get_db)) -> dict:
    return runtime_metrics.refresh_runtime(db, detector_count=len(get_detector_registry().list()))
