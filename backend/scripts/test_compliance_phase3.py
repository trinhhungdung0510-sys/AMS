#!/usr/bin/env python3
"""Manual smoke test for AMS v1.7 Phase 3 Compliance Engine."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.compliance.compliance_engine import get_compliance_engine, init_compliance_engine
from app.compliance.types import ComplianceContext
from app.compliance.uniform_matcher import match_uniform
from unittest.mock import MagicMock

from app.compliance.rules.uniform_rule import UniformRule


def main() -> None:
    init_compliance_engine()
    engine = get_compliance_engine()
    print("Rules:", [rule.id for rule in engine.rules])

    match = match_uniform(b"mock-person", ["/storage/uniforms/a.jpg"], track_id=12, template_id="uniform-clean")
    print("Matcher:", match)

    db = MagicMock()
    db.get.return_value = None
    context = ComplianceContext(
        db=db,
        camera_id="CAM-001",
        zone_id="ZONE-001",
        track_id=12,
        timestamp="2026-06-18T10:00:00+00:00",
        metadata={"trigger_event": "PERSON_ENTER", "zone_name": "clean-zone"},
    )
    result = UniformRule().evaluate(context)
    print("UniformRule (no mapping):", result)
    print("Done.")


if __name__ == "__main__":
    main()
