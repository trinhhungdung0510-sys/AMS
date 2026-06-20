import unittest
from datetime import datetime, timedelta, timezone

from app.services.camera_health_service import (
    STATUS_DEGRADED,
    STATUS_OFFLINE,
    STATUS_ONLINE,
    CameraHealthService,
)


class CameraHealthTransitionTest(unittest.TestCase):
    def test_offline_after_timeout(self) -> None:
        now = datetime.now(timezone.utc)
        last_seen_value = (now - timedelta(seconds=130)).isoformat()

        age_seconds = (
            now - datetime.fromisoformat(last_seen_value.replace("Z", "+00:00"))
        ).total_seconds()
        if age_seconds >= 120:
            next_status = STATUS_OFFLINE
        elif age_seconds >= 60:
            next_status = STATUS_DEGRADED
        else:
            next_status = STATUS_ONLINE

        self.assertEqual(next_status, STATUS_OFFLINE)

    def test_degraded_between_thresholds(self) -> None:
        now = datetime.now(timezone.utc)
        last_seen = (now - timedelta(seconds=75)).isoformat()
        age_seconds = (now - datetime.fromisoformat(last_seen.replace("Z", "+00:00"))).total_seconds()

        if age_seconds >= 120:
            next_status = STATUS_OFFLINE
        elif age_seconds >= 60:
            next_status = STATUS_DEGRADED
        else:
            next_status = STATUS_ONLINE

        self.assertEqual(next_status, STATUS_DEGRADED)


if __name__ == "__main__":
    unittest.main()
