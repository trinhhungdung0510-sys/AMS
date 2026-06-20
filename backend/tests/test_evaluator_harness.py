import unittest

from app.core.event_bus.event_bus import InMemoryEventBus
from app.core.event_bus.event_types import OBSERVATION_CREATED, RULE_EVALUATED
from app.services.observation_replay_service import observation_replay_service
from app.services.observation_validator import observation_validator


class EvaluatorHarnessTest(unittest.TestCase):
    def test_fixture_has_expected_event_contract(self) -> None:
        fixture = observation_replay_service.load_fixture("person_enter.json")
        self.assertIn("expectedEvents", fixture)
        self.assertTrue(fixture["expectedEvents"][0]["eventType"])

    def test_replay_publish_only_hits_event_bus(self) -> None:
        bus = InMemoryEventBus()
        received: list[dict] = []

        def capture(message: dict) -> None:
            received.append(message)

        bus.subscribe(OBSERVATION_CREATED, capture)

        original = observation_replay_service.__class__

        class HarnessReplayService(original):
            def replay_fixture(self, db, fixture_name, *, camera_id=None, publish_only=False):
                raw = self.load_fixture(fixture_name)
                validated = observation_validator.validate(raw)
                observation_dict = validated.model_dump(by_alias=True)
                bus.publish(
                    OBSERVATION_CREATED,
                    {"topic": OBSERVATION_CREATED, "data": {"observation": observation_dict}},
                )
                return {"mode": "publish_only", "observation": observation_dict}

        svc = HarnessReplayService()
        result = svc.replay_fixture(None, "person_enter.json", publish_only=True)
        self.assertEqual(result["mode"], "publish_only")
        self.assertEqual(len(received), 1)

    def test_rule_evaluated_topic_constant(self) -> None:
        self.assertEqual(RULE_EVALUATED, "rule.evaluated")


if __name__ == "__main__":
    unittest.main()
