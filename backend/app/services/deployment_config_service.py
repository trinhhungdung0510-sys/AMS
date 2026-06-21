from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.services.backup_service import export_backup, restore_backup


def export_config_files(db: Session) -> dict[str, Any]:
    backup = export_backup(db)
    backup["version"] = "2.0"
    return {
        "farm.json": backup["farms"],
        "camera.json": backup["cameras"],
        "zone.json": backup["zones"],
        "workflow.json": backup["workflows"],
        "settings.json": backup["settings"],
        "uniform.json": backup["uniforms"],
        "meta": {
            "version": "2.0",
            "exportedAt": backup["exportedAt"],
        },
    }


def import_config_files(db: Session, payload: dict[str, Any]) -> dict[str, int]:
    restore_payload = {
        "farms": payload.get("farm.json") or payload.get("farms") or [],
        "cameras": payload.get("camera.json") or payload.get("cameras") or [],
        "zones": payload.get("zone.json") or payload.get("zones") or [],
        "workflows": payload.get("workflow.json") or payload.get("workflows") or [],
        "uniforms": payload.get("uniform.json") or payload.get("uniforms") or [],
        "settings": payload.get("settings.json") or payload.get("settings") or {},
    }
    return restore_backup(db, restore_payload)
