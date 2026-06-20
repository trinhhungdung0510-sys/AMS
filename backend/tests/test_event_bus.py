import unittest

from app.core.event_bus.event_bus import InMemoryEventBus
from app.core.event_bus.event_types import OBSERVATION_CREATED, TRACK_UPDATED


class EventBusTest(unittest.TestCase):
    def test_publish_subscribe(self) -> None:
        bus = InMemoryEventBus()
        received: list[dict] = []

        def handler(message: dict) -> None:
            received.append(message)

        bus.subscribe(OBSERVATION_CREATED, handler)
        bus.publish(OBSERVATION_CREATED, {"data": {"observation": {"id": "OBS-1"}}})

        self.assertEqual(len(received), 1)
        self.assertEqual(received[0]["data"]["observation"]["id"], "OBS-1")

    def test_unsubscribe(self) -> None:
        bus = InMemoryEventBus()
        received: list[dict] = []

        def handler(message: dict) -> None:
            received.append(message)

        bus.subscribe(TRACK_UPDATED, handler)
        bus.unsubscribe(TRACK_UPDATED, handler)
        bus.publish(TRACK_UPDATED, {"data": {"trackId": "T-1"}})

        self.assertEqual(received, [])

    def test_handler_failure_does_not_break_bus(self) -> None:
        bus = InMemoryEventBus()
        received: list[dict] = []

        def bad_handler(_message: dict) -> None:
            raise RuntimeError("boom")

        def good_handler(message: dict) -> None:
            received.append(message)

        bus.subscribe(OBSERVATION_CREATED, bad_handler)
        bus.subscribe(OBSERVATION_CREATED, good_handler)
        bus.publish(OBSERVATION_CREATED, {"data": {"ok": True}})

        self.assertEqual(len(received), 1)


if __name__ == "__main__":
    unittest.main()
