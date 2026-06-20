#!/usr/bin/env python3
"""Test zone mapping + evaluator pipeline with fixtures."""

from __future__ import annotations

import json
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

from sqlalchemy import delete, select

from app.core.event_bus.event_bus import InMemoryEventBus
import app.core.event_bus.event_bus as event_bus_module
from app.core.runtime.track_store import get_track_store
from app.core.runtime.zone_mapper import map_observation_to_zones
from app.database.session import SessionLocal
from app.models import CameraZone, Event, ZoneRule
from app.services.observation_replay_service import observation_replay_service
from app.services.observation_service import utc_now_iso
from app.services.pipeline_subscribers import register_pipeline_subscribers

CAMERA_ID = "CAM-001"
ZONE_ID = "ZONE-TEST-MAIN"
RULES = {
    "PERSON_ENTER": "RULE-TEST-PENTER",
    "PERSON_COUNT": "RULE-TEST-PCOUNT",
    "ANIMAL_ENTER": "RULE-TEST-AENTER",
}


def seed_zones(db) -> None:
    now = utc_now_iso()
    zone = db.get(CameraZone, ZONE_ID)
    if not zone:
        db.add(
            CameraZone(
                id=ZONE_ID,
                camera_id=CAMERA_ID,
                name="Vung test toan khung hinh",
                description="Zone test AMS v1.6",
                zone_type="monitoring",
                points=[
                    {"x": 0.0, "y": 0.0},
                    {"x": 1.0, "y": 0.0},
                    {"x": 1.0, "y": 1.0},
                    {"x": 0.0, "y": 1.0},
                ],
                points_format="normalized",
                reference_width=1280,
                reference_height=720,
                color="#00ff88",
                created_at=now,
                updated_at=now,
            )
        )

    for rule_type, rule_id in RULES.items():
        if db.get(ZoneRule, rule_id):
            continue
        config = {"maxPersons": 2} if rule_type == "PERSON_COUNT" else {}
        db.add(
            ZoneRule(
                id=rule_id,
                camera_id=CAMERA_ID,
                zone_id=ZONE_ID,
                name=f"Test {rule_type}",
                rule_type=rule_type,
                severity="MEDIUM" if rule_type != "ANIMAL_ENTER" else "HIGH",
                enabled=True,
                cooldown_seconds=0,
                config=config,
                created_at=now,
                updated_at=now,
            )
        )
    db.commit()


def zone_row(db, zone_id: str) -> dict:
    zone = db.get(CameraZone, zone_id)
    return {
        "id": zone.id,
        "name": zone.name,
        "parent_zone_id": zone.parent_zone_id,
        "points": zone.points,
        "points_format": zone.points_format,
        "reference_width": zone.reference_width,
        "reference_height": zone.reference_height,
    }


def run_fixture_test(db, fixture_name: str) -> dict:
    get_track_store().clear()
    before = db.scalars(select(Event).where(Event.camera_id == CAMERA_ID)).all()
    before_ids = {event.id for event in before}

    result = observation_replay_service.replay_fixture(
        db,
        fixture_name,
        camera_id=CAMERA_ID,
    )
    db.commit()

    new_events = [
        event
        for event in db.scalars(select(Event).where(Event.camera_id == CAMERA_ID)).all()
        if event.id not in before_ids
    ]
    return {
        "fixture": fixture_name,
        "observation_id": result["observation"]["id"],
        "events": [
            {
                "id": event.id,
                "event_type": event.event_type,
                "zone_id": event.zone_id,
                "severity": event.severity,
                "metadata": event.event_metadata,
            }
            for event in new_events
        ],
    }


def main() -> None:
    event_bus_module._event_bus = InMemoryEventBus()
    register_pipeline_subscribers()

    db = SessionLocal()
    try:
        seed_zones(db)
        zones = [zone_row(db, ZONE_ID)]

        print("=== ZONE MAPPING (fixture person_enter) ===")
        fixture = observation_replay_service.load_fixture("person_enter.json")
        fixture["cameraId"] = CAMERA_ID
        mappings = map_observation_to_zones(fixture, zones)
        print(json.dumps(mappings, indent=2, ensure_ascii=False))

        print("\n=== PIPELINE FIXTURE TESTS ===")
        results = []
        for name in ("person_enter.json", "person_count.json", "animal_enter.json"):
            results.append(run_fixture_test(db, name))
            print(f"\n{name}:")
            print(json.dumps(results[-1], indent=2, ensure_ascii=False))

        print("\n=== TONG KET ===")
        for item in results:
            types = [event["event_type"] for event in item["events"]]
            print(f"- {item['fixture']}: events={types or 'KHONG CO'}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
