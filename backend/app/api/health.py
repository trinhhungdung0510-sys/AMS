from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.database.session import get_db
from app.schemas.health import HealthResponse
from app.services.health import check_database, check_redis

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)) -> HealthResponse:
    settings = get_settings()

    try:
        database_status = check_database(db)
    except Exception:
        database_status = "unavailable"

    try:
        redis_status = check_redis()
    except Exception:
        redis_status = "unavailable"

    return HealthResponse(
        status="ok",
        service=settings.app_name,
        database=database_status,
        redis=redis_status,
    )
