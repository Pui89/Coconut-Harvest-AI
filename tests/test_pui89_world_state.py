"""Dependency-free tests for the shared PUI89 safety contract."""
import unittest

from tools.pui89_world_state import Observation, WorldState, assess_observation


def good(value="target", *, source="sensor-A", timestamp=98.0, confidence=0.95):
    return Observation(value, source, timestamp, confidence, calibrated=True)


class ObservationGateTests(unittest.TestCase):
    def test_fresh_high_confidence_observation_is_planning_eligible(self):
        result = assess_observation(good(), now=100.0)
        self.assertEqual(result.status, "ACCEPT")
        self.assertTrue(result.may_enter_simulation)
        self.assertFalse(result.may_actuate_hardware)

    def test_missing_value_is_rejected(self):
        result = assess_observation(Observation(None, "sensor-A", 99.0, 0.9), now=100.0)
        self.assertEqual(result.status, "REJECT")

    def test_blank_or_non_string_source_requires_review(self):
        for source in (None, "", " \t\n", 123):
            with self.subTest(source=source):
                observation = Observation("target", source, 99.0, 0.95, calibrated=True)
                result = assess_observation(observation, now=100.0)
                self.assertEqual(result.status, "REVIEW")
                self.assertIn("missing_source_provenance", result.reasons)
                self.assertTrue(result.requires_human_review)
                self.assertFalse(result.may_enter_simulation)
                self.assertFalse(result.may_actuate_hardware)

    def test_stale_observation_requires_review(self):
        result = assess_observation(good(timestamp=80.0), now=100.0)
        self.assertIn("stale_observation", result.reasons)
        self.assertEqual(result.status, "REVIEW")
        self.assertFalse(result.may_enter_simulation)

    def test_future_timestamp_is_rejected(self):
        result = assess_observation(good(timestamp=101.0), now=100.0)
        self.assertEqual(result.status, "REJECT")
        self.assertFalse(result.may_enter_simulation)

    def test_low_confidence_requires_review(self):
        result = assess_observation(good(confidence=0.2), now=100.0)
        self.assertEqual(result.status, "REVIEW")
        self.assertFalse(result.may_enter_simulation)

    def test_invalid_confidence_is_rejected(self):
        result = assess_observation(good(confidence=1.5), now=100.0)
        self.assertEqual(result.status, "REJECT")
        self.assertFalse(result.may_enter_simulation)

    def test_required_calibration_is_checked(self):
        obs = Observation("target", "sensor-A", 99.0, 0.9, calibrated=None)
        result = assess_observation(obs, now=100.0, require_calibration=True)
        self.assertIn("calibration_unverified", result.reasons)
        self.assertFalse(result.may_enter_simulation)

    def test_explicit_human_review_never_passes_as_accept(self):
        result = assess_observation(good(), now=100.0, require_human_review=True)
        self.assertEqual(result.status, "REVIEW")
        self.assertFalse(result.may_enter_simulation)

    def test_review_assessments_cannot_enter_task_simulation(self):
        review_results = (
            assess_observation(good(source=" "), now=100.0),
            assess_observation(good(timestamp=80.0), now=100.0),
            assess_observation(good(confidence=0.2), now=100.0),
            assess_observation(good(), now=100.0, require_human_review=True),
        )
        for result in review_results:
            with self.subTest(reasons=result.reasons):
                self.assertEqual(result.status, "REVIEW")
                self.assertTrue(result.requires_human_review)
                self.assertFalse(result.may_enter_simulation)
                self.assertFalse(result.may_actuate_hardware)

    def test_unknown_world_state_is_rejected(self):
        result = WorldState().assess("target", now=100.0)
        self.assertEqual(result.status, "REJECT")
        self.assertFalse(result.may_enter_simulation)

    def test_conflicting_fresh_observations_require_review(self):
        state = WorldState()
        state.update("target", good("left", source="camera-A"))
        state.update("target", good("right", source="camera-B"))
        result = state.assess("target", now=100.0)
        self.assertEqual(result.status, "REVIEW")
        self.assertIn("conflicting_fresh_observations", result.reasons)
        self.assertFalse(result.may_enter_simulation)

    def test_matching_fresh_observations_are_consistent(self):
        state = WorldState()
        state.update("target", good("visible", source="camera-A"))
        state.update("target", good("visible", source="camera-B"))
        result = state.assess("target", now=100.0)
        self.assertEqual(result.status, "ACCEPT")
        self.assertTrue(result.may_enter_simulation)

    def test_blank_world_state_key_is_rejected(self):
        with self.assertRaises(ValueError):
            WorldState().update("  ", good())

    def test_non_finite_timestamps_are_rejected(self):
        for timestamp in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(timestamp=timestamp):
                result = assess_observation(good(timestamp=timestamp), now=100.0)
                self.assertEqual(result.status, "REJECT")
                self.assertIn("invalid_timestamp", result.reasons)
                self.assertFalse(result.may_enter_simulation)

    def test_non_finite_clock_and_age_limits_raise_value_error(self):
        for kwargs in (
            {"now": float("nan")},
            {"now": float("inf")},
            {"now": 100.0, "max_age_seconds": float("nan")},
            {"now": 100.0, "max_age_seconds": float("inf")},
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(ValueError):
                    assess_observation(good(), **kwargs)

    def test_unorderable_timestamp_among_observations_fails_closed(self):
        for timestamp in ("not-a-time", True, None, float("nan")):
            with self.subTest(timestamp=timestamp):
                state = WorldState()
                state.update("target", good("valid", timestamp=99.0))
                state.update("target", good("malformed", timestamp=timestamp))
                result = state.assess("target", now=100.0)
                self.assertEqual(result.status, "REJECT")
                self.assertIn("unorderable_observation_timestamp", result.reasons)
                self.assertFalse(result.may_enter_simulation)
                self.assertFalse(result.may_actuate_hardware)

    def test_non_string_world_state_keys_are_rejected_without_mutation(self):
        for key in (None, 123, [], {}):
            with self.subTest(key=key):
                state = WorldState()
                with self.assertRaises(ValueError):
                    state.update(key, good())
                self.assertEqual(state.keys(), ())

    def test_non_observation_payloads_are_rejected_without_mutation(self):
        for payload in (None, "target", {"value": "target"}):
            with self.subTest(payload=payload):
                state = WorldState()
                with self.assertRaises(TypeError):
                    state.update("target", payload)
                self.assertEqual(state.keys(), ())


if __name__ == "__main__":
    unittest.main()
