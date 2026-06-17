from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import AIModel
from app.schemas.ai_model import AIModelResponse

router = APIRouter(prefix="/models", tags=["ai-models"])


@router.get("", response_model=list[AIModelResponse])
def list_ai_models(db: Session = Depends(get_db)) -> list[AIModel]:
    return list(db.scalars(select(AIModel).order_by(AIModel.id)))
