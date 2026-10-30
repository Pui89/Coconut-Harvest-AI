"""Regression tests for the shared PUI89 fail-closed health gate."""
import math
import unittest

from pui89_core.health_gate import assess_health

READY = {
    "emergency_stop": False,
    "sensors_ok": True,
    "sensor_data_fresh": True,
    "perception_ok": True,
    "localization_ok": True,
    "comms_ok": True,
    "safety_monitor_ok": True,
    "operator_approved": True,
    "confidence": 0.95,
}


class HealthGateTests(unittest.TestCase):
    def test_healthy_telemetry_allows_simulation_only(self):
        result = assess_health(READY)
        self.assertEqual(result["mode"], "SIMULATION_READY")
        self.assertTrue(result["simulation_only"])
        self.assertFalse(result["physical_actuation_permitted"])

    def test_missing_or_malformed_telemetry_fails_closed(self):
        for key in READY:
            with self.subTest(key=key):
                state = dict(READY)
                del state[key]
                self.assertEqual(assess_health(state)["mode"], "SAFE_HOLD")
        for value in (None, 0, 1, "true", [], {}):
            state = {**READY, "sensors_ok": value}
            self.assertEqual(assess_health(state)["mode"], "SAFE_HOLD")

    def test_emergency_stop_has_stopped_priority(self):
        self.assertEqual(assess_health({**READY, "emergency_stop": True})["mode"], "STOPPED")

    def test_unhealthy_safety_monitor_stops(self):
        self.assertEqual(assess_health({**READY, "safety_monitor_ok": False})["mode"], "STOPPED")

    def test_stale_or_failed_sensor_health_holds(self):
        for key in ("sensors_ok", "sensor_data_fresh", "perception_ok", "localization_ok", "comms_ok"):
            with self.subTest(key=key):
                self.assertEqual(assess_health({**READY, key: False})["mode"], "SAFE_HOLD")

    def test_operator_approval_is_required(self):
        self.assertEqual(assess_health({**READY, "operator_approved": False})["mode"], "REQUEST_HUMAN_REVIEW")

    def test_low_confidence_requests_review(self):
        self.assertEqual(assess_health({**READY, "confidence": 0.2})["mode"], "REQUEST_HUMAN_REVIEW")

    def test_invalid_confidence_holds(self):
        for value in (None, True, "0.9", -0.1, 1.1, math.nan, math.inf):
            with self.subTest(value=value):
                self.assertEqual(assess_health({**READY, "confidence": value})["mode"], "SAFE_HOLD")

    def test_invalid_threshold_is_rejected(self):
        for value in (True, -0.1, 1.1, math.nan, math.inf):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    assess_health(READY, value)

    def test_non_mapping_input_holds(self):
        self.assertEqual(assess_health(None)["mode"], "SAFE_HOLD")

    def test_conflicting_modalities_request_human_review(self):
        self.assertEqual(assess_health({**READY, "modalities_conflict": True})["mode"], "REQUEST_HUMAN_REVIEW")

    def test_missing_required_modality_requests_human_review(self):
        self.assertEqual(assess_health({**READY, "required_modality_missing": True})["mode"], "REQUEST_HUMAN_REVIEW")

    def test_sensor_observation_older_than_limit_holds(self):
        state = {**READY, "sensor_age_seconds": 5.1, "max_sensor_age_seconds": 5}
        self.assertEqual(assess_health(state)["mode"], "SAFE_HOLD")

    def test_sensor_observation_at_age_limit_is_accepted(self):
        state = {**READY, "sensor_age_seconds": 5, "max_sensor_age_seconds": 5}
        self.assertEqual(assess_health(state)["mode"], "SIMULATION_READY")

    def test_invalid_or_incomplete_sensor_age_holds(self):
        cases = (
            {"sensor_age_seconds": 1},
            {"sensor_age_seconds": True, "max_sensor_age_seconds": 5},
            {"sensor_age_seconds": -1, "max_sensor_age_seconds": 5},
            {"sensor_age_seconds": math.inf, "max_sensor_age_seconds": 5},
        )
        for extra in cases:
            with self.subTest(extra=extra):
                self.assertEqual(assess_health({**READY, **extra})["mode"], "SAFE_HOLD")

    def test_malformed_optional_multimodal_flags_hold(self):
        for key in ("modalities_conflict", "required_modality_missing"):
            self.assertEqual(assess_health({**READY, key: "false"})["mode"], "SAFE_HOLD")


if __name__ == "__main__":
    unittest.main()
