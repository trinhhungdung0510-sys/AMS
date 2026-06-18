from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Camera
from app.schemas.camera import CameraResponse
from app.services.snapshot_generator import render_camera_frame_bytes

router = APIRouter(prefix="/cameras", tags=["cameras"])


@router.get("", response_model=list[CameraResponse])
def list_cameras(db: Session = Depends(get_db)) -> list[Camera]:
    return list(db.scalars(select(Camera).order_by(Camera.id)))


@router.get("/{camera_id}/frame")
def get_camera_frame(camera_id: str, db: Session = Depends(get_db)) -> Response:
    camera = db.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy camera")

    image_bytes = render_camera_frame_bytes(
        camera_id=camera.id,
        camera_name=camera.name,
        zone=camera.zone,
        status=camera.status,
        resolution=camera.resolution,
    )
    return Response(
        content=image_bytes,
        media_type="image/jpeg",
        headers={"Cache-Control": "no-store, max-age=0"},
    )
