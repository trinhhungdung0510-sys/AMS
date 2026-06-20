from __future__ import annotations

from typing import Any, Optional

OBSERVATION_SCHEMA_V1 = "v1"
OBSERVATION_SCHEMA_V2 = "v2"
SUPPORTED_SCHEMA_VERSIONS = {OBSERVATION_SCHEMA_V1, OBSERVATION_SCHEMA_V2}
DEFAULT_SCHEMA_VERSION = OBSERVATION_SCHEMA_V1


def normalize_schema_version(value: Optional[str]) -> str:
    if not value:
        return DEFAULT_SCHEMA_VERSION
    cleaned = value.strip().lower()
    if cleaned not in SUPPORTED_SCHEMA_VERSIONS:
        raise ValueError(f"schemaVersion phải là một trong: {', '.join(sorted(SUPPORTED_SCHEMA_VERSIONS))}")
    return cleaned


def migrate_observation_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Upgrade legacy payloads without schemaVersion to v1 shape."""
    version = normalize_schema_version(payload.get("schemaVersion") or payload.get("schema_version"))
    migrated = dict(payload)
    migrated["schemaVersion"] = version

    if version == OBSERVATION_SCHEMA_V1:
        return migrated

    # v2 reserved — currently same fields, allows future extensions
    return migrated
