"""Dependency-free tests for the shared PUI89 safety contract."""
import unittest

from tools.pui89_world_state import Observation, WorldState, assess_observation


def good(value="target", *, source="sensor-A", timestamp=98.0, confidence=0.95):
    return Observation(value, source, timestamp, confidence, calibrated=True)


class ObservationGateTests(unittest.TestCase):
    def test_fresh_high_confidence_observation_is_planning_eligible(self):
        result = assess_observation(good(), now=100.0)
        self.assertEqual(result.status, "ACCEPT")
        self.assertFalse(result.may_actuate_hardware)

    def test_missing_value_is_rejected(self):
        result = assess_observation(Observation(None, "sensor-A", 99.0, 0.9), now=100.0)
        self.assertEqual(result.status, "REJECT")

    def test_stale_observation_requires_review(self):
        result = assess_observation(good(timestamp=80.0), now=100.0)
        self.assertIn("stale_observation", result.reasons)
        self.assertEqual(result.status, "REVIEW")

    def test_future_timestamp_is_rejected(self):
        result = assess_observation(good(timestamp=101.0), now=100.0)
        self.assertEqual(result.status, "REJECT")

    def test_low_confidence_requires_review(self):
        result = assess_observation(good(confidence=0.2), now=100.0)
        self.assertEqual(result.status, "REVIEW")

    def test_invalid_confidence_is_rejected(self):
        result = assess_observation(good(confidence=1.5), now=100.0)
        self.assertEqual(result.status, "REJECT")

    def test_required_calibration_is_checked(self):
        obs = Observation("target", "sensor-A", 99.0, 0.9, calibrated=None)
        result = assess_observation(obs, now=100.0, require_calibration=True)
        self.assertIn("calibration_unverified", result.reasons)

    def test_explicit_human_review_never_passes_as_accept(self):
        result = assess_observation(good(), now=100.0, require_human_review=True)
        self.assertEqual(result.status, "REVIEW")

    def test_unknown_world_state_is_rejected(self):
        self.assertEqual(WorldState().assess("target", now=100.0).status, "REJECT")

    def test_conflicting_fresh_observations_require_review(self):
        state = WorldState()
        state.update("target", good("left", source="camera-A"))
        state.update("target", good("right", source="camera-B"))
        result = state.assess("target", now=100.0)
        self.assertEqual(result.status, "REVIEW")
        self.assertIn("conflicting_fresh_observations", result.reasons)

    def test_matching_fresh_observations_are_consistent(self):
        state = WorldState()
        state.update("target", good("visible", source="camera-A"))
        state.update("target", good("visible", source="camera-B"))
        result = state.assess("target", now=100.0)
        self.assertEqual(result.status, "ACCEPT")

    def test_blank_world_state_key_is_rejected(self):
        with self.assertRaises(ValueError):
            WorldState().update("  ", good())


if __name__ == "__main__":
    unittest.main()
