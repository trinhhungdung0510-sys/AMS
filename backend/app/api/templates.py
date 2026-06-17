from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.data.farm_template import TEMPLATE_ZONE_CODES
from app.models import FarmLayoutTemplate, TemplateZoneDefinition
from app.schemas.farm_template import (
    FarmLayoutTemplateResponse,
    FarmLayoutTemplateSummaryResponse,
    TemplateZoneDefinitionResponse,
)

router = APIRouter(prefix="/templates", tags=["farm-templates"])


@router.get("", response_model=list[FarmLayoutTemplateSummaryResponse])
def list_templates(db: Session = Depends(get_db)) -> list[FarmLayoutTemplateSummaryResponse]:
    templates = list(db.scalars(select(FarmLayoutTemplate).order_by(FarmLayoutTemplate.id)))
    zone_counts = dict(
        db.execute(
            select(TemplateZoneDefinition.template_id, func.count())
            .group_by(TemplateZoneDefinition.template_id)
        ).all()
    )
    return [
        FarmLayoutTemplateSummaryResponse(
            id=template.id,
            name=template.name,
            description=template.description,
            version=template.version,
            zone_count=zone_counts.get(template.id, 0),
        )
        for template in templates
    ]


@router.get("/zone-codes", response_model=list[str])
def list_zone_codes() -> list[str]:
    return sorted(TEMPLATE_ZONE_CODES)


@router.get("/{template_id}", response_model=FarmLayoutTemplateResponse)
def get_template(template_id: str, db: Session = Depends(get_db)) -> FarmLayoutTemplateResponse:
    template = db.get(FarmLayoutTemplate, template_id)
    if not template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farm template not found")

    zones = list(
        db.scalars(
            select(TemplateZoneDefinition)
            .where(TemplateZoneDefinition.template_id == template_id)
            .order_by(TemplateZoneDefinition.sort_order, TemplateZoneDefinition.id)
        )
    )
    return FarmLayoutTemplateResponse(
        id=template.id,
        name=template.name,
        description=template.description,
        version=template.version,
        zones=[TemplateZoneDefinitionResponse.model_validate(zone) for zone in zones],
    )


@router.get("/{template_id}/zones", response_model=list[TemplateZoneDefinitionResponse])
def list_template_zones(template_id: str, db: Session = Depends(get_db)) -> list[TemplateZoneDefinition]:
    if not db.get(FarmLayoutTemplate, template_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Farm template not found")

    return list(
        db.scalars(
            select(TemplateZoneDefinition)
            .where(TemplateZoneDefinition.template_id == template_id)
            .order_by(TemplateZoneDefinition.sort_order, TemplateZoneDefinition.id)
        )
    )
