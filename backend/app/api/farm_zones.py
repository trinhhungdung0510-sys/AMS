from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import FarmZone
from app.schemas.farm_template import FarmZoneResponse

router = APIRouter(prefix="/farm-zones", tags=["farm-zones"])


@router.get("", response_model=list[FarmZoneResponse])
def list_farm_zones(
    farm_id: Optional[str] = Query(default=None),
    db: Session = Depends(get_db),
) -> list[FarmZone]:
    query = select(FarmZone).order_by(FarmZone.sort_order, FarmZone.id)
    if farm_id:
        query = query.where(FarmZone.farm_id == farm_id)
    return list(db.scalars(query))
