from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from app.core.event_bus import get_event_bus
from app.core.event_bus.event_types import OBSERVATION_CREATED
from app.services.observation_service import create_observation, observation_to_response_dict, utc_now_iso
from app.services.observation_validator import observation_validator

logger = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[3]
FIXTURES_DIR = REPO_ROOT / "fixtures" / "observations"


class ObservationReplayService:
    def load_fixture(self, fixture_name: str) -> dict[str, Any]:
        path = FIXTURES_DIR / fixture_name
        if not path.exists():
            raise FileNotFoundError(f"Fixture not found: {fixture_name}")
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def list_fixtures(self) -> list[str]:
        if not FIXTURES_DIR.exists():
            return []
        return sorted(path.name for path in FIXTURES_DIR.glob("*.json"))

    def replay_fixture(
        self,
        db: Session,
        fixture_name: str,
        *,
        camera_id: Optional[str] = None,
        publish_only: bool = False,
    ) -> dict[str, Any]:
        raw = self.load_fixture(fixture_name)
        if camera_id:
            raw = {**raw, "cameraId": camera_id, "camera_id": camera_id}

        validated = observation_validator.validate(raw)

        if publish_only:
            observation_dict = validated.model_dump(by_alias=True)
            observation_dict["id"] = raw.get("id") or f"REPLAY-{fixture_name}"
            observation_dict["created_at"] = utc_now_iso()
            get_event_bus().publish(
                OBSERVATION_CREATED,
                {
                    "topic": OBSERVATION_CREATED,
                    "timestamp": utc_now_iso(),
                    "data": {"observation": observation_dict, "replay": True},
                },
            )
            return {"mode": "publish_only", "observation": observation_dict}

        observation = create_observation(db, validated)
        return {
            "mode": "persist",
            "observation": observation_to_response_dict(observation),
        }

    def replay_many(
        self,
        db: Session,
        fixture_name: str,
        *,
        camera_ids: list[str],
        publish_only: bool = False,
    ) -> list[dict[str, Any]]:
        return [
            self.replay_fixture(db, fixture_name, camera_id=camera_id, publish_only=publish_only)
            for camera_id in camera_ids
        ]


observation_replay_service = ObservationReplayService()
