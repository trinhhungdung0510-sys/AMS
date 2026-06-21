from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.deployment import DeploymentHealthResponse
from app.services.deployment_health_service import build_health_report

router = APIRouter(tags=["health"])


@router.get("/health", response_model=DeploymentHealthResponse)
def api_health_check(db: Session = Depends(get_db)) -> DeploymentHealthResponse:
    report = build_health_report(db)
    return DeploymentHealthResponse(**report)
