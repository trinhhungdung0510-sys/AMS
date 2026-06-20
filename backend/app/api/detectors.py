from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.detectors import get_detector_registry

router = APIRouter(prefix="/detectors", tags=["detectors"], dependencies=[Depends(get_current_user)])


@router.get("")
def list_detectors() -> list[dict]:
    return get_detector_registry().list_dicts()


@router.get("/{detector_name}")
def get_detector(detector_name: str) -> dict:
    detector = get_detector_registry().get(detector_name)
    if not detector:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detector not found")
    return detector.to_dict()
