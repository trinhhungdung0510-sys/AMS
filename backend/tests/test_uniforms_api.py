from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.models import CameraZone, UniformTemplate
from app.services.uniform_service import (
    delete_uniform_template,
    get_uniform_usage,
    list_zones_using_uniform,
    resolve_uniform_image_path,
)


def test_list_zones_using_uniform():
    db = MagicMock()
    zone = CameraZone(
        id="ZONE-001",
        farm_id="FARM-001",
        camera_id="CAM-001",
        name="Nhà tắm",
        zone_type="monitoring",
        points=[],
        created_at="2026-01-01T00:00:00+00:00",
        updated_at="2026-01-01T00:00:00+00:00",
        required_uniform_id="UNI-001",
    )
    db.scalars.return_value = [zone]
    result = list_zones_using_uniform(db, "UNI-001")
    assert len(result) == 1
    assert result[0].id == "ZONE-001"


def test_get_uniform_usage_when_not_in_use():
    db = MagicMock()
    db.scalars.return_value = []
    result = get_uniform_usage(db, "UNI-001")
    assert result == {"in_use": False, "zones": []}


def test_get_uniform_usage_when_zones_assigned():
    db = MagicMock()
    zones = [
        CameraZone(
            id="ZONE-001",
            farm_id="FARM-001",
            camera_id="CAM-001",
            name="Vùng sạch",
            zone_type="monitoring",
            points=[],
            created_at="2026-01-01T00:00:00+00:00",
            updated_at="2026-01-01T00:00:00+00:00",
            required_uniform_id="UNI-001",
        ),
        CameraZone(
            id="ZONE-002",
            farm_id="FARM-001",
            camera_id="CAM-002",
            name="Nhà tắm",
            zone_type="monitoring",
            points=[],
            created_at="2026-01-01T00:00:00+00:00",
            updated_at="2026-01-01T00:00:00+00:00",
            required_uniform_id="UNI-001",
        ),
    ]
    db.scalars.return_value = zones
    result = get_uniform_usage(db, "UNI-001")
    assert result["in_use"] is True
    assert len(result["zones"]) == 2
    assert result["zones"][0]["name"] == "Vùng sạch"


def test_delete_uniform_template_blocks_when_zone_uses_it():
    db = MagicMock()
    uniform = UniformTemplate(
        id="UNI-001",
        farm_id="FARM-001",
        name="Clean suit",
        description="",
        image_paths=["/storage/uniforms/UNI-001/a.jpg"],
        created_at="2026-01-01T00:00:00+00:00",
        updated_at="2026-01-01T00:00:00+00:00",
    )
    zone = CameraZone(
        id="ZONE-001",
        farm_id="FARM-001",
        camera_id="CAM-001",
        name="Nhà tắm",
        zone_type="monitoring",
        points=[],
        created_at="2026-01-01T00:00:00+00:00",
        updated_at="2026-01-01T00:00:00+00:00",
        required_uniform_id="UNI-001",
    )
    db.scalars.return_value = [zone]

    with pytest.raises(HTTPException) as exc:
        delete_uniform_template(db, uniform)

    assert exc.value.status_code == 409
    assert exc.value.detail["error"] == "UNIFORM_IN_USE"
    assert "1 zone" in exc.value.detail["message"]
    assert exc.value.detail["zones"][0]["id"] == "ZONE-001"
    assert exc.value.detail["zones"][0]["name"] == "Nhà tắm"
    db.delete.assert_not_called()


def test_delete_uniform_template_removes_metadata_and_images(tmp_path, monkeypatch):
    storage_root = tmp_path / "storage"
    image_dir = storage_root / "uniforms" / "UNI-002"
    image_dir.mkdir(parents=True)
    image_file = image_dir / "front.jpg"
    image_file.write_bytes(b"jpeg")

    monkeypatch.setenv("STORAGE_ROOT", str(storage_root))

    from app.core.config import get_settings

    get_settings.cache_clear()

    db = MagicMock()
    db.scalars.return_value = []
    uniform = UniformTemplate(
        id="UNI-002",
        farm_id="FARM-001",
        name="Boot cover",
        description="",
        image_paths=[f"/storage/uniforms/UNI-002/front.jpg"],
        created_at="2026-01-01T00:00:00+00:00",
        updated_at="2026-01-01T00:00:00+00:00",
    )

    result = delete_uniform_template(db, uniform)

    assert result["uniformId"] == "UNI-002"
    assert not image_file.exists()
    assert not image_dir.exists()
    db.delete.assert_called_once_with(uniform)
    db.flush.assert_called_once()


def test_resolve_uniform_image_path_storage_prefix(tmp_path, monkeypatch):
    storage_root = tmp_path / "storage"
    file_path = storage_root / "uniforms" / "UNI-003" / "a.jpg"
    file_path.parent.mkdir(parents=True)
    file_path.write_bytes(b"x")

    monkeypatch.setenv("STORAGE_ROOT", str(storage_root))
    from app.core.config import get_settings

    get_settings.cache_clear()

    resolved = resolve_uniform_image_path("/storage/uniforms/UNI-003/a.jpg")
    assert resolved == Path(file_path)
