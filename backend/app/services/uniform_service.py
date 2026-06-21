from __future__ import annotations

import logging
import shutil
from pathlib import Path

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models import CameraZone, UniformTemplate

logger = logging.getLogger(__name__)


def list_zones_using_uniform(db: Session, uniform_id: str) -> list[CameraZone]:
    return list(
        db.scalars(
            select(CameraZone)
            .where(CameraZone.required_uniform_id == uniform_id)
            .order_by(CameraZone.name, CameraZone.id)
        )
    )


def format_usage_zones(zones: list[CameraZone]) -> list[dict[str, str]]:
    return [{"id": zone.id, "name": zone.name} for zone in zones]


def get_uniform_usage(db: Session, uniform_id: str) -> dict:
    zones = list_zones_using_uniform(db, uniform_id)
    formatted = format_usage_zones(zones)
    return {
        "in_use": bool(formatted),
        "zones": formatted,
    }


def raise_uniform_in_use_error(zones: list[CameraZone]) -> None:
    count = len(zones)
    noun = "zone" if count == 1 else "zone"
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail={
            "error": "UNIFORM_IN_USE",
            "message": f"Uniform đang được sử dụng bởi {count} {noun}.",
            "zones": format_usage_zones(zones),
        },
    )


def resolve_uniform_image_path(public_path: str) -> Path | None:
    if not public_path:
        return None

    settings = get_settings()
    normalized = public_path.strip()

    if normalized.startswith("/storage/"):
        relative = normalized.removeprefix("/storage/").lstrip("/")
        return Path(settings.storage_root) / relative
    if normalized.startswith("/uploads/"):
        relative = normalized.removeprefix("/uploads/").lstrip("/")
        return Path(settings.uploads_root) / relative
    if normalized.startswith("storage/"):
        return Path(settings.storage_root) / normalized.removeprefix("storage/").lstrip("/")
    if normalized.startswith("uploads/"):
        return Path(settings.uploads_root) / normalized.removeprefix("uploads/").lstrip("/")

    candidate = Path(normalized)
    if candidate.is_absolute() and candidate.exists():
        return candidate
    return None


def _image_paths_used_elsewhere(db: Session, uniform_id: str, public_path: str) -> bool:
    others = db.scalars(
        select(UniformTemplate).where(UniformTemplate.id != uniform_id)
    )
    for item in others:
        if public_path in (item.image_paths or []):
            return True
    return False


def delete_uniform_image_files(db: Session, uniform: UniformTemplate) -> list[str]:
    deleted: list[str] = []
    seen: set[str] = set()

    for public_path in uniform.image_paths or []:
        if public_path in seen:
            continue
        seen.add(public_path)
        if _image_paths_used_elsewhere(db, uniform.id, public_path):
            continue
        file_path = resolve_uniform_image_path(public_path)
        if file_path and file_path.is_file():
            try:
                file_path.unlink()
                deleted.append(str(file_path))
            except OSError:
                logger.exception("Failed deleting uniform image %s", file_path)

    settings = get_settings()
    uniform_dir = Path(settings.storage_root) / "uniforms" / uniform.id
    if uniform_dir.is_dir():
        try:
            shutil.rmtree(uniform_dir)
            deleted.append(str(uniform_dir))
        except OSError:
            logger.exception("Failed deleting uniform directory %s", uniform_dir)

    return deleted


def delete_uniform_template(db: Session, uniform: UniformTemplate) -> dict:
    zones = list_zones_using_uniform(db, uniform.id)
    if zones:
        raise_uniform_in_use_error(zones)

    deleted_files = delete_uniform_image_files(db, uniform)
    db.delete(uniform)
    db.flush()
    return {
        "uniformId": uniform.id,
        "deletedImagePaths": deleted_files,
        "clearedZoneMappings": 0,
    }
