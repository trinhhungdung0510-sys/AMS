from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import Camera
from app.schemas.camera import CameraCreate, CameraResponse, CameraUpdate
from app.services.camera_registry import camera_to_response_dict, create_camera, update_camera
from app.services.snapshot_generator import render_camera_frame_bytes

router = APIRouter(prefix="/cameras", tags=["cameras"],
    dependencies=[Depends(get_current_user)]
)


def _get_camera_or_404(camera_id: str, db: Session) -> Camera:
    camera = db.get(Camera, camera_id)
    if not camera:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy camera")
    return camera


def _to_response(camera: Camera) -> CameraResponse:
    return CameraResponse(**camera_to_response_dict(camera))


@router.get("", response_model=list[CameraResponse])
def list_cameras(db: Session = Depends(get_db)) -> list[CameraResponse]:
    cameras = list(db.scalars(select(Camera).order_by(Camera.id)))
    return [_to_response(camera) for camera in cameras]


@router.get("/{camera_id}", response_model=CameraResponse)
def get_camera(camera_id: str, db: Session = Depends(get_db)) -> CameraResponse:
    return _to_response(_get_camera_or_404(camera_id, db))


@router.post("", response_model=CameraResponse, status_code=status.HTTP_201_CREATED)
def create_camera_endpoint(payload: CameraCreate, db: Session = Depends(get_db)) -> CameraResponse:
    try:
        camera = create_camera(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return _to_response(camera)


@router.put("/{camera_id}", response_model=CameraResponse)
def update_camera_endpoint(
    camera_id: str,
    payload: CameraUpdate,
    db: Session = Depends(get_db),
) -> CameraResponse:
    camera = _get_camera_or_404(camera_id, db)
    try:
        updated = update_camera(db, camera, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    return _to_response(updated)


@router.delete("/{camera_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_camera(camera_id: str, db: Session = Depends(get_db)) -> None:
    camera = _get_camera_or_404(camera_id, db)
    db.delete(camera)
    db.commit()


@router.get("/{camera_id}/frame")
def get_camera_frame(camera_id: str, db: Session = Depends(get_db)) -> Response:
    camera = _get_camera_or_404(camera_id, db)

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
