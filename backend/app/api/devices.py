from app.api.deps import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import EdgeDevice
from app.schemas.device import EdgeDeviceResponse

router = APIRouter(prefix="/devices", tags=["edge-devices"],
    dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=list[EdgeDeviceResponse])
def list_devices(db: Session = Depends(get_db)) -> list[EdgeDevice]:
    return list(db.scalars(select(EdgeDevice).order_by(EdgeDevice.id)))
