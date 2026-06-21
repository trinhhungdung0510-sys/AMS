from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.farm_access import assert_farm_access, resolve_farm_scope
from app.core.permissions import require_permission
from app.database.session import get_db
from app.models import Camera, User
from app.schemas.camera import (
    CameraConnectionTestRequest,
    CameraConnectionTestResponse,
    CameraCreate,
    CameraResponse,
    CameraUpdate,
)
from app.services.camera_connection_test import probe_rtsp_stream
from app.services.camera_registry import camera_to_response_dict, create_camera, update_camera
from app.services.snapshot_generator import render_camera_frame_bytes
from app.services.audit import write_audit_log

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
def list_cameras(
    farm_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("camera.read")),
) -> list[CameraResponse]:
    scope = resolve_farm_scope(current_user, farm_id)
    query = select(Camera).order_by(Camera.id)
    if scope:
        query = query.where(Camera.farm_id == scope)
    cameras = list(db.scalars(query))
    return [_to_response(camera) for camera in cameras]


@router.post("/test", response_model=CameraConnectionTestResponse)
def test_camera_connection(payload: CameraConnectionTestRequest) -> CameraConnectionTestResponse:
    result = probe_rtsp_stream(payload.rtsp_url)
    return CameraConnectionTestResponse(
        success=result.success,
        fps=result.fps,
        resolution=result.resolution,
        error=result.error,
    )


@router.get("/{camera_id}", response_model=CameraResponse)
def get_camera(camera_id: str, db: Session = Depends(get_db)) -> CameraResponse:
    return _to_response(_get_camera_or_404(camera_id, db))


@router.post("", response_model=CameraResponse, status_code=status.HTTP_201_CREATED)
def create_camera_endpoint(
    payload: CameraCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("camera.manage")),
) -> CameraResponse:
    assert_farm_access(current_user, payload.farm_id)
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
    current_user: User = Depends(require_permission("camera.manage")),
) -> CameraResponse:
    camera = _get_camera_or_404(camera_id, db)
    assert_farm_access(current_user, camera.farm_id)
    try:
        updated = update_camera(db, camera, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    write_audit_log(
        db,
        user_id=current_user.id,
        action="update_camera",
        resource_type="camera",
        resource_id=camera.id,
        farm_id=camera.farm_id,
        metadata={"name": updated.name},
    )
    db.commit()
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
