from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Camera
from app.schemas.camera_snapshot import CameraSnapshotResponse
from app.services.camera_registry import utc_now_iso
from app.services.camera_snapshot_service import (
    capture_camera_snapshot,
    get_latest_camera_snapshot,
    snapshot_result_to_dict,
)

router = APIRouter(
    prefix="/cameras",
    tags=["camera-snapshots"],
    dependencies=[Depends(get_current_user)],
)


def _get_camera_or_404(camera_id: str, db: Session) -> Camera:
    camera = db.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy camera")
    return camera


def _to_response(result) -> CameraSnapshotResponse:
    return CameraSnapshotResponse(**snapshot_result_to_dict(result))


@router.get("/{camera_id}/snapshot", response_model=CameraSnapshotResponse)
def capture_camera_snapshot_endpoint(
    camera_id: str,
    db: Session = Depends(get_db),
) -> CameraSnapshotResponse:
    camera = _get_camera_or_404(camera_id, db)
    result = capture_camera_snapshot(camera)

    if result.success:
        camera.last_seen = result.captured_at or utc_now_iso()
        db.add(camera)
        db.commit()

    return _to_response(result)


@router.get("/{camera_id}/latest-snapshot", response_model=CameraSnapshotResponse)
def get_latest_camera_snapshot_endpoint(camera_id: str, db: Session = Depends(get_db)) -> CameraSnapshotResponse:
    _get_camera_or_404(camera_id, db)
    return _to_response(get_latest_camera_snapshot(camera_id))
