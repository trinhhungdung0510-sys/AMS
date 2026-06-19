from app.api.deps import get_current_user
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import EventSnapshot
from app.schemas.snapshot import EventSnapshotResponse

router = APIRouter(prefix="/snapshots", tags=["snapshots"],
    dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=list[EventSnapshotResponse])
def list_snapshots(db: Session = Depends(get_db)) -> list[EventSnapshot]:
    return list(db.scalars(select(EventSnapshot).order_by(EventSnapshot.id)))
