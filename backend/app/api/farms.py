from app.api.deps import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Farm
from app.schemas.farm import FarmResponse

router = APIRouter(prefix="/farms", tags=["farms"],
    dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=list[FarmResponse])
def list_farms(db: Session = Depends(get_db)) -> list[Farm]:
    return list(db.scalars(select(Farm).order_by(Farm.id)))
