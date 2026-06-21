from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import Camera, CameraZone, Event, UniformTemplate, Workflow, WorkflowStep
from app.services.system_settings_service import get_system_settings

DEFAULT_FARM_ID = "FARM-001"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def export_backup(db: Session) -> dict[str, Any]:
    from app.models import Farm

    farms = [
        {
            "id": farm.id,
            "name": farm.name,
            "code": farm.code or farm.id,
            "address": farm.address or farm.location,
            "contactName": farm.contact_name,
            "contactPhone": farm.contact_phone,
            "createdAt": farm.created_at,
            "location": farm.location,
            "plan": farm.plan,
            "status": farm.status,
        }
        for farm in db.scalars(select(Farm).order_by(Farm.id))
    ]

    cameras = [
        {
            "id": camera.id,
            "farmId": camera.farm_id,
            "name": camera.name,
            "zone": camera.zone,
            "status": camera.status,
            "resolution": camera.resolution,
            "isActive": camera.is_active,
        }
        for camera in db.scalars(select(Camera).order_by(Camera.id))
    ]

    zones = [
        {
            "id": zone.id,
            "farmId": zone.farm_id,
            "cameraId": zone.camera_id,
            "name": zone.name,
            "zoneType": zone.zone_type,
            "points": zone.points,
            "requiredUniformId": zone.required_uniform_id,
        }
        for zone in db.scalars(select(CameraZone).order_by(CameraZone.id))
    ]

    workflows = []
    for workflow in db.scalars(select(Workflow).order_by(Workflow.id)):
        steps = list(
            db.scalars(
                select(WorkflowStep)
                .where(WorkflowStep.workflow_id == workflow.id)
                .order_by(WorkflowStep.step_order)
            )
        )
        workflows.append(
            {
                "id": workflow.id,
                "farmId": workflow.farm_id,
                "name": workflow.name,
                "description": workflow.description,
                "objectType": workflow.object_type,
                "enabled": workflow.enabled,
                "steps": [
                    {
                        "stepOrder": step.step_order,
                        "stepName": step.step_name,
                        "zoneCode": step.zone_code,
                        "required": step.required,
                    }
                    for step in steps
                ],
            }
        )

    uniforms = [
        {
            "id": item.id,
            "farmId": item.farm_id,
            "name": item.name,
            "description": item.description,
            "imagePaths": item.image_paths,
        }
        for item in db.scalars(select(UniformTemplate).order_by(UniformTemplate.id))
    ]

    return {
        "version": "1.9-rc1",
        "exportedAt": utc_now_iso(),
        "settings": get_system_settings(db),
        "farms": farms,
        "cameras": cameras,
        "zones": zones,
        "workflows": workflows,
        "uniforms": uniforms,
    }


def restore_backup(db: Session, payload: dict[str, Any]) -> dict[str, int]:
    from app.models import Farm
    from app.services.system_settings_service import save_system_settings

    counts = {"farms": 0, "cameras": 0, "zones": 0, "workflows": 0, "uniforms": 0}

    if payload.get("settings"):
        save_system_settings(db, payload["settings"])

    for farm_data in payload.get("farms", []):
        farm_id = farm_data.get("id") or DEFAULT_FARM_ID
        farm = db.get(Farm, farm_id) or Farm(
            id=farm_id,
            name=farm_data.get("name", farm_id),
            location=farm_data.get("location", farm_data.get("address", "")),
            plan=farm_data.get("plan", "standard"),
            status=farm_data.get("status", "active"),
        )
        farm.name = farm_data.get("name", farm.name)
        farm.code = farm_data.get("code", farm.code or farm_id)
        farm.address = farm_data.get("address", farm.address or farm.location)
        farm.contact_name = farm_data.get("contactName")
        farm.contact_phone = farm_data.get("contactPhone")
        farm.created_at = farm_data.get("createdAt") or utc_now_iso()
        db.merge(farm)
        counts["farms"] += 1

    for camera_data in payload.get("cameras", []):
        camera = db.get(Camera, camera_data["id"])
        if camera is None:
            continue
        camera.farm_id = camera_data.get("farmId", camera.farm_id or DEFAULT_FARM_ID)
        camera.name = camera_data.get("name", camera.name)
        camera.zone = camera_data.get("zone", camera.zone)
        camera.status = camera_data.get("status", camera.status)
        camera.is_active = camera_data.get("isActive", camera.is_active)
        db.merge(camera)
        counts["cameras"] += 1

    for zone_data in payload.get("zones", []):
        zone = db.get(CameraZone, zone_data["id"])
        if zone is None:
            continue
        zone.farm_id = zone_data.get("farmId", zone.farm_id or DEFAULT_FARM_ID)
        zone.name = zone_data.get("name", zone.name)
        zone.zone_type = zone_data.get("zoneType", zone.zone_type)
        zone.points = zone_data.get("points", zone.points)
        zone.required_uniform_id = zone_data.get("requiredUniformId")
        db.merge(zone)
        counts["zones"] += 1

    for workflow_data in payload.get("workflows", []):
        workflow = db.get(Workflow, workflow_data["id"])
        if workflow is None:
            continue
        workflow.farm_id = workflow_data.get("farmId", workflow.farm_id or DEFAULT_FARM_ID)
        workflow.name = workflow_data.get("name", workflow.name)
        workflow.description = workflow_data.get("description", workflow.description)
        workflow.object_type = workflow_data.get("objectType", workflow.object_type)
        workflow.enabled = workflow_data.get("enabled", workflow.enabled)
        db.merge(workflow)
        counts["workflows"] += 1

    for uniform_data in payload.get("uniforms", []):
        uniform = db.get(UniformTemplate, uniform_data["id"])
        if uniform is None:
            continue
        uniform.farm_id = uniform_data.get("farmId", uniform.farm_id or DEFAULT_FARM_ID)
        uniform.name = uniform_data.get("name", uniform.name)
        uniform.description = uniform_data.get("description", uniform.description)
        uniform.image_paths = uniform_data.get("imagePaths", uniform.image_paths)
        db.merge(uniform)
        counts["uniforms"] += 1

    db.commit()
    return counts
