import unittest

from app.core.runtime.zone_presence_tracker import (
    PRESENCE_ENTER,
    PRESENCE_EXIT,
    PRESENCE_INSIDE,
    PRESENCE_OUTSIDE,
    PRESENCE_UNKNOWN,
    ZonePresenceTracker,
)


class ZonePresenceTrackerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tracker = ZonePresenceTracker()

    def test_initial_state_is_unknown(self) -> None:
        self.assertEqual(self.tracker.get_state("CAM-1", "T-1", "CZ-1"), PRESENCE_UNKNOWN)

    def test_unknown_to_outside_is_silent(self) -> None:
        result = self.tracker.update("CAM-1", "T-1", "CZ-1", False, "2026-06-20T10:00:00+00:00")
        self.assertIsNone(result.transition)
        self.assertEqual(result.next_state, PRESENCE_OUTSIDE)

    def test_outside_to_inside_emits_enter(self) -> None:
        self.tracker.update("CAM-1", "T-1", "CZ-1", False, "2026-06-20T10:00:00+00:00")
        result = self.tracker.update("CAM-1", "T-1", "CZ-1", True, "2026-06-20T10:01:00+00:00")
        self.assertEqual(result.transition, PRESENCE_ENTER)
        self.assertEqual(result.next_state, PRESENCE_INSIDE)
        self.assertEqual(result.zone_state["enteredAt"], "2026-06-20T10:01:00+00:00")

    def test_unknown_to_inside_is_silent(self) -> None:
        result = self.tracker.update("CAM-1", "T-1", "CZ-1", True, "2026-06-20T10:00:00+00:00")
        self.assertIsNone(result.transition)
        self.assertEqual(result.next_state, PRESENCE_INSIDE)

    def test_inside_to_inside_is_silent(self) -> None:
        self.tracker.update("CAM-1", "T-1", "CZ-1", True, "2026-06-20T10:00:00+00:00")
        result = self.tracker.update("CAM-1", "T-1", "CZ-1", True, "2026-06-20T10:01:00+00:00")
        self.assertIsNone(result.transition)

    def test_inside_to_outside_emits_exit(self) -> None:
        self.tracker.update("CAM-1", "T-1", "CZ-1", True, "2026-06-20T10:00:00+00:00")
        result = self.tracker.update("CAM-1", "T-1", "CZ-1", False, "2026-06-20T10:02:00+00:00")
        self.assertEqual(result.transition, PRESENCE_EXIT)
        self.assertEqual(result.zone_state["exitedAt"], "2026-06-20T10:02:00+00:00")


class TransitionScenarioTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tracker = ZonePresenceTracker()
        self.timestamp = "2026-06-20T10:00:00+00:00"

    def _collect(self, results) -> list[str]:
        return [result.transition for result in results.values() if result.transition]

    def test_scenario_1_outside_to_inside(self) -> None:
        self.tracker.update("CAM-1", "T-1", "CZ-1", False, self.timestamp)
        result = self.tracker.update("CAM-1", "T-1", "CZ-1", True, self.timestamp)
        self.assertEqual(result.transition, PRESENCE_ENTER)

    def test_scenario_2_inside_stays_inside(self) -> None:
        self.tracker.update("CAM-1", "T-1", "CZ-1", True, self.timestamp)
        transitions = [
            self.tracker.update("CAM-1", "T-1", "CZ-1", True, self.timestamp).transition,
            self.tracker.update("CAM-1", "T-1", "CZ-1", True, self.timestamp).transition,
            self.tracker.update("CAM-1", "T-1", "CZ-1", True, self.timestamp).transition,
        ]
        self.assertEqual([item for item in transitions if item], [])

    def test_scenario_3_inside_to_outside(self) -> None:
        self.tracker.update("CAM-1", "T-1", "CZ-1", True, self.timestamp)
        result = self.tracker.update("CAM-1", "T-1", "CZ-1", False, self.timestamp)
        self.assertEqual(result.transition, PRESENCE_EXIT)

    def test_scenario_4_enter_exit_enter(self) -> None:
        self.tracker.update("CAM-1", "T-1", "CZ-1", False, self.timestamp)
        transitions = []
        transitions.append(self.tracker.update("CAM-1", "T-1", "CZ-1", True, self.timestamp).transition)
        transitions.append(self.tracker.update("CAM-1", "T-1", "CZ-1", False, self.timestamp).transition)
        transitions.append(self.tracker.update("CAM-1", "T-1", "CZ-1", True, self.timestamp).transition)
        self.assertEqual(transitions.count(PRESENCE_ENTER), 2)
        self.assertEqual(transitions.count(PRESENCE_EXIT), 1)

    def test_scenario_5_multi_zone_move(self) -> None:
        self.tracker.apply_zones("CAM-1", "T-1", set(), self.timestamp, {"ZONE-A", "ZONE-B"})
        self.tracker.apply_zones("CAM-1", "T-1", {"ZONE-A"}, self.timestamp, {"ZONE-A", "ZONE-B"})
        results = self.tracker.apply_zones(
            "CAM-1",
            "T-1",
            {"ZONE-B"},
            self.timestamp,
            {"ZONE-A", "ZONE-B"},
        )
        self.assertEqual(results["ZONE-A"].transition, PRESENCE_EXIT)
        self.assertEqual(results["ZONE-B"].transition, PRESENCE_ENTER)


if __name__ == "__main__":
    unittest.main()
