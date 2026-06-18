import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models import FarmLayout, FarmMapLayer, FarmObject, FarmRoute
from app.schemas.smart_farm import (
    FarmLayoutResponse,
    FarmMapLayerResponse,
    FarmObjectResponse,
    FarmRouteResponse,
    SmartFarmFullResponse,
    SmartFarmSaveRequest,
    parse_route_labels,
    parse_route_points,
)

router = APIRouter(prefix="/smart-farm", tags=["smart-farm-designer"])

DEFAULT_FARM_ID = "FARM-001"
DEFAULT_LAYOUT_ID = "SF-LAYOUT-001"

DEFAULT_LAYERS = [
    ("objects", True, 1.0),
    ("cameras", True, 1.0),
    ("atsh", True, 0.85),
    ("routes", True, 1.0),
    ("heatmap", False, 0.6),
]


def _route_to_response(route: FarmRoute) -> FarmRouteResponse:
    return FarmRouteResponse(
        id=route.id,
        layout_id=route.layout_id,
        route_type=route.route_type,
        name=route.name,
        points=parse_route_points(route.points),
        labels=parse_route_labels(route.labels),
        valid=route.valid,
    )


def _layer_to_response(layer: FarmMapLayer) -> FarmMapLayerResponse:
    return FarmMapLayerResponse(
        id=layer.id,
        layout_id=layer.layout_id,
        layer_key=layer.layer_key,
        visible=layer.visible,
        opacity=layer.opacity,
    )


@router.get("/designer", response_model=SmartFarmFullResponse)
def get_active_designer(db: Session = Depends(get_db)) -> SmartFarmFullResponse:
    layout = db.scalar(
        select(FarmLayout)
        .where(FarmLayout.farm_id == DEFAULT_FARM_ID, FarmLayout.is_active.is_(True))
        .order_by(FarmLayout.id)
    )
    if layout is None:
        raise HTTPException(status_code=404, detail="Chưa có sơ đồ trang trại")

    objects = list(db.scalars(select(FarmObject).where(FarmObject.layout_id == layout.id)))
    routes = list(db.scalars(select(FarmRoute).where(FarmRoute.layout_id == layout.id)))
    layers = list(db.scalars(select(FarmMapLayer).where(FarmMapLayer.layout_id == layout.id)))

    return SmartFarmFullResponse(
        layout=layout,
        objects=objects,
        routes=[_route_to_response(item) for item in routes],
        layers=[_layer_to_response(item) for item in layers],
    )


@router.post("/designer/save", response_model=SmartFarmFullResponse)
def save_designer(payload: SmartFarmSaveRequest, db: Session = Depends(get_db)) -> SmartFarmFullResponse:
    layout_id = DEFAULT_LAYOUT_ID if not payload.layout.is_template else f"SF-TPL-{payload.layout.farm_id}"
    layout = db.get(FarmLayout, layout_id)

    if layout is None:
        layout = FarmLayout(
            id=layout_id,
            farm_id=payload.layout.farm_id,
            name=payload.layout.name,
            address=payload.layout.address,
            center_lat=payload.layout.center_lat,
            center_lng=payload.layout.center_lng,
            zoom=payload.layout.zoom,
            base_layer=payload.layout.base_layer,
            is_template=payload.layout.is_template,
            is_active=not payload.layout.is_template,
        )
        db.add(layout)
    else:
        layout.name = payload.layout.name
        layout.address = payload.layout.address
        layout.center_lat = payload.layout.center_lat
        layout.center_lng = payload.layout.center_lng
        layout.zoom = payload.layout.zoom
        layout.base_layer = payload.layout.base_layer
        layout.is_template = payload.layout.is_template
        if not payload.layout.is_template:
            layout.is_active = True

    db.execute(delete(FarmObject).where(FarmObject.layout_id == layout.id))
    db.execute(delete(FarmRoute).where(FarmRoute.layout_id == layout.id))
    db.execute(delete(FarmMapLayer).where(FarmMapLayer.layout_id == layout.id))

    for item in payload.objects:
        db.add(
            FarmObject(
                id=item.id,
                layout_id=layout.id,
                object_type=item.object_type,
                name=item.name,
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
        )

    for item in payload.routes:
        db.add(
            FarmRoute(
                id=item.id,
                layout_id=layout.id,
                route_type=item.route_type,
                name=item.name,
                points=json.dumps(item.points),
                labels=json.dumps(item.labels),
                valid=item.valid,
            )
        )

    layer_items = payload.layers or [
        {"layer_key": key, "visible": visible, "opacity": opacity}
        for key, visible, opacity in DEFAULT_LAYERS
    ]
    for index, item in enumerate(layer_items):
        db.add(
            FarmMapLayer(
                id=f"{layout.id}-L{index + 1}",
                layout_id=layout.id,
                layer_key=item["layer_key"] if isinstance(item, dict) else item.layer_key,
                visible=item["visible"] if isinstance(item, dict) else item.visible,
                opacity=item["opacity"] if isinstance(item, dict) else item.opacity,
            )
        )

    db.commit()
    db.refresh(layout)

    objects = list(db.scalars(select(FarmObject).where(FarmObject.layout_id == layout.id)))
    routes = list(db.scalars(select(FarmRoute).where(FarmRoute.layout_id == layout.id)))
    layers = list(db.scalars(select(FarmMapLayer).where(FarmMapLayer.layout_id == layout.id)))

    return SmartFarmFullResponse(
        layout=layout,
        objects=objects,
        routes=[_route_to_response(item) for item in routes],
        layers=[_layer_to_response(item) for item in layers],
    )
