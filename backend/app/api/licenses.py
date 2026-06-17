from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import License
from app.schemas.license import LicenseResponse

router = APIRouter(prefix="/licenses", tags=["licenses"])


@router.get("", response_model=list[LicenseResponse])
def list_licenses(db: Session = Depends(get_db)) -> list[License]:
    return list(db.scalars(select(License).order_by(License.id)))
