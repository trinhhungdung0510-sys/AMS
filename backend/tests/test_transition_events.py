import unittest
from types import SimpleNamespace
from typing import Optional
from unittest.mock import patch

from app.core.runtime.zone_presence_tracker import ZonePresenceTracker
from app.services import pipeline_subscribers


def _rule(rule_type: str, zone_id: str = "CZ-1") -> SimpleNamespace:
    return SimpleNamespace(
        id=f"RULE-{rule_type}",
        zone_id=zone_id,
        rule_type=rule_type,
        severity="MEDIUM",
        enabled=True,
        config={},
    )


class TransitionEventsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tracker = ZonePresenceTracker()
        self.tracker_patcher = patch(
            "app.services.pipeline_subscribers.get_zone_presence_tracker",
            return_value=self.tracker,
        )
        self.tracker_patcher.start()

        self.rules_patcher = patch(
            "app.services.pipeline_subscribers.list_rules_for_camera",
            return_value=[
                _rule("PERSON_ENTER"),
                _rule("PERSON_EXIT"),
                _rule("PERSON_COUNT"),
            ],
        )
        self.rules_patcher.start()

    def tearDown(self) -> None:
        self.rules_patcher.stop()
        self.tracker_patcher.stop()

    def _evaluate(self, zone_mapping, previous_inside: Optional[bool] = None) -> list:
        track = {
            "trackId": "T-1",
            "cameraId": "CAM-1",
            "class": "person",
        }
        observation = {
            "id": "OBS-1",
            "objects": [
                {
                    "trackId": "T-1",
                    "class": "person",
                    "confidence": 0.9,
                }
            ],
        }

        if previous_inside is False:
            self.tracker.update("CAM-1", "T-1", "CZ-1", False, "2026-06-20T10:00:00+00:00")

        return pipeline_subscribers._evaluate_track_rules(
            db=None,
            track=track,
            observation=observation,
            zone_mapping=zone_mapping,
        )

    def test_outside_to_inside_generates_person_enter(self) -> None:
        hits = self._evaluate({"zones": ["CZ-1"], "subzones": []}, previous_inside=False)
        event_types = [hit["eventType"] for hit in hits]
        self.assertIn("PERSON_ENTER", event_types)
        self.assertNotIn("PERSON_EXIT", event_types)

    def test_inside_to_inside_is_silent(self) -> None:
        self.tracker.update("CAM-1", "T-1", "CZ-1", False, "2026-06-20T10:00:00+00:00")
        self.tracker.update("CAM-1", "T-1", "CZ-1", True, "2026-06-20T10:01:00+00:00")
        hits = self._evaluate({"zones": ["CZ-1"], "subzones": []})
        self.assertEqual(hits, [])

    def test_inside_to_outside_generates_person_exit(self) -> None:
        self.tracker.update("CAM-1", "T-1", "CZ-1", False, "2026-06-20T10:00:00+00:00")
        self.tracker.update("CAM-1", "T-1", "CZ-1", True, "2026-06-20T10:01:00+00:00")
        hits = self._evaluate({"zones": [], "subzones": []})
        event_types = [hit["eventType"] for hit in hits]
        self.assertIn("PERSON_EXIT", event_types)
        self.assertNotIn("PERSON_ENTER", event_types)


if __name__ == "__main__":
    unittest.main()
