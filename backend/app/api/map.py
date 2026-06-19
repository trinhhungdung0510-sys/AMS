from app.api.deps import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import FarmMapLayout, FarmMapObject
from app.schemas.map import (
    FarmMapFullResponse,
    FarmMapLayoutResponse,
    FarmMapObjectResponse,
    FarmMapSaveRequest,
)

router = APIRouter(prefix="/map", tags=["farm-map"],
    dependencies=[Depends(get_current_user)]
)

DEFAULT_FARM_ID = "FARM-001"
DEFAULT_LAYOUT_ID = "MAP-LAYOUT-001"


def _object_from_input(layout_id: str, item) -> FarmMapObject:
    return FarmMapObject(
        id=item.id,
        layout_id=layout_id,
        object_type=item.object_type,
        name=item.name,
        zone=item.zone,
        description=item.description,
        x=item.x,
        y=item.y,
        width=item.width,
        height=item.height,
        rotation=item.rotation,
        atsh_zone_type=item.atsh_zone_type,
        atsh_level=item.atsh_level,
        linked_camera_id=item.linked_camera_id,
        linked_zone_id=item.linked_zone_id,
        camera_direction=item.camera_direction,
        camera_fov=item.camera_fov,
        status=item.status,
    )


@router.get("", response_model=list[FarmMapObjectResponse])
def list_map_objects(db: Session = Depends(get_db)) -> list[FarmMapObject]:
    return list(db.scalars(select(FarmMapObject).order_by(FarmMapObject.id)))


@router.get("/active", response_model=FarmMapFullResponse)
def get_active_layout(db: Session = Depends(get_db)) -> FarmMapFullResponse:
    layout = db.scalar(
        select(FarmMapLayout)
        .where(FarmMapLayout.farm_id == DEFAULT_FARM_ID, FarmMapLayout.is_active.is_(True))
        .order_by(FarmMapLayout.id)
    )
    if layout is None:
        raise HTTPException(status_code=404, detail="Chưa có bản đồ trang trại")

    objects = list(
        db.scalars(
            select(FarmMapObject)
            .where(FarmMapObject.layout_id == layout.id)
            .order_by(FarmMapObject.id)
        )
    )
    return FarmMapFullResponse(layout=layout, objects=objects)


@router.post("/save", response_model=FarmMapFullResponse)
def save_farm_map(payload: FarmMapSaveRequest, db: Session = Depends(get_db)) -> FarmMapFullResponse:
    layout_id = DEFAULT_LAYOUT_ID
    existing = db.get(FarmMapLayout, layout_id)

    if payload.layout.is_template:
        layout_id = f"MAP-TPL-{payload.layout.farm_id}"
        existing = db.get(FarmMapLayout, layout_id)

    if existing is None:
        layout = FarmMapLayout(
            id=layout_id,
            farm_id=payload.layout.farm_id,
            name=payload.layout.name,
            is_template=payload.layout.is_template,
            is_active=not payload.layout.is_template,
            center_lat=payload.layout.center_lat,
            center_lng=payload.layout.center_lng,
            zoom=payload.layout.zoom,
            base_layer=payload.layout.base_layer,
        )
        db.add(layout)
    else:
        layout = existing
        layout.name = payload.layout.name
        layout.is_template = payload.layout.is_template
        layout.center_lat = payload.layout.center_lat
        layout.center_lng = payload.layout.center_lng
        layout.zoom = payload.layout.zoom
        layout.base_layer = payload.layout.base_layer
        if not payload.layout.is_template:
            layout.is_active = True

    db.execute(delete(FarmMapObject).where(FarmMapObject.layout_id == layout.id))
    for item in payload.objects:
        db.add(_object_from_input(layout.id, item))

    db.commit()
    db.refresh(layout)
    objects = list(
        db.scalars(
            select(FarmMapObject)
            .where(FarmMapObject.layout_id == layout.id)
            .order_by(FarmMapObject.id)
        )
    )
    return FarmMapFullResponse(layout=layout, objects=objects)


@router.delete("/objects/{object_id}")
def delete_map_object(object_id: str, db: Session = Depends(get_db)) -> dict:
    obj = db.get(FarmMapObject, object_id)
    if obj is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy đối tượng")
    db.delete(obj)
    db.commit()
    return {"ok": True, "id": object_id}


@router.get("/layouts", response_model=list[FarmMapLayoutResponse])
def list_layouts(db: Session = Depends(get_db)) -> list[FarmMapLayout]:
    return list(
        db.scalars(
            select(FarmMapLayout)
            .where(FarmMapLayout.farm_id == DEFAULT_FARM_ID)
            .order_by(FarmMapLayout.name)
        )
    )
