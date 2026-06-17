from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import FarmMapObject
from app.schemas.map import FarmMapObjectResponse

router = APIRouter(prefix="/map", tags=["farm-map"])


@router.get("", response_model=list[FarmMapObjectResponse])
def list_map_objects(db: Session = Depends(get_db)) -> list[FarmMapObject]:
    return list(db.scalars(select(FarmMapObject).order_by(FarmMapObject.id)))
