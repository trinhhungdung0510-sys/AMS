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

    def test_outside_to_inside_emits_enter(self) -> None:
        self.tracker.update("CAM-1", "T-1", "CZ-1", False)
        self.assertEqual(self.tracker.get_state("CAM-1", "T-1", "CZ-1"), PRESENCE_OUTSIDE)
        self.assertEqual(self.tracker.update("CAM-1", "T-1", "CZ-1", True), PRESENCE_ENTER)
        self.assertEqual(self.tracker.get_state("CAM-1", "T-1", "CZ-1"), PRESENCE_INSIDE)

    def test_unknown_to_inside_emits_enter(self) -> None:
        self.assertEqual(self.tracker.update("CAM-1", "T-1", "CZ-1", True), PRESENCE_ENTER)

    def test_inside_to_inside_is_silent(self) -> None:
        self.tracker.update("CAM-1", "T-1", "CZ-1", True)
        self.assertIsNone(self.tracker.update("CAM-1", "T-1", "CZ-1", True))

    def test_inside_to_outside_emits_exit(self) -> None:
        self.tracker.update("CAM-1", "T-1", "CZ-1", True)
        self.assertEqual(self.tracker.update("CAM-1", "T-1", "CZ-1", False), PRESENCE_EXIT)
        self.assertEqual(self.tracker.get_state("CAM-1", "T-1", "CZ-1"), PRESENCE_OUTSIDE)


if __name__ == "__main__":
    unittest.main()
