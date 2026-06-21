from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from app.compliance.constants import COMPLIANCE_RULE_IDS
from app.core.config import get_settings

ASSET_SPECS: tuple[tuple[str, str, str], ...] = (
    ("person.jpg", "#2563eb", "Person"),
    ("animal.jpg", "#16a34a", "Animal"),
    ("vehicle.jpg", "#7c3aed", "Vehicle"),
    ("uniform.jpg", "#ea580c", "Uniform"),
)

EVENT_SNAPSHOT_MAP = {
    COMPLIANCE_RULE_IDS["UNIFORM_VIOLATION"]: "uniform.jpg",
    COMPLIANCE_RULE_IDS["ZONE_INTRUSION"]: "person.jpg",
    COMPLIANCE_RULE_IDS["ANIMAL_INTRUSION"]: "animal.jpg",
    COMPLIANCE_RULE_IDS["VEHICLE_INTRUSION"]: "vehicle.jpg",
    COMPLIANCE_RULE_IDS["BIOSECURITY_PROCESS_VIOLATION"]: "person.jpg",
}


def _backend_root() -> Path:
    return Path(__file__).resolve().parents[2]


def demo_assets_dir() -> Path:
    configured = Path(get_settings().demo_assets_dir)
    if configured.is_absolute():
        return configured
    return _backend_root() / configured


def _render_asset(path: Path, *, color: str, label: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (1280, 720), color="#111827")
    draw = ImageDraw.Draw(image)
    draw.rectangle((40, 40, 1240, 680), outline=color, width=6)
    draw.rectangle((320, 120, 960, 620), fill=color)
    draw.text((56, 56), f"AMS Demo — {label}", fill="#f8fafc")
    draw.text((360, 340), label.upper(), fill="#ffffff")
    image.save(path, format="JPEG", quality=90, optimize=True)


def ensure_demo_assets() -> Path:
    assets_dir = demo_assets_dir()
    assets_dir.mkdir(parents=True, exist_ok=True)
    for filename, color, label in ASSET_SPECS:
        destination = assets_dir / filename
        if not destination.exists():
            _render_asset(destination, color=color, label=label)
    return assets_dir


def snapshot_url_for_event_type(event_type: str) -> str:
    filename = EVENT_SNAPSHOT_MAP.get(event_type, "person.jpg")
    return f"/demo-assets/{filename}"
