"""Unit tests for the conservative autonomy supervisor."""
import math
import unittest

from pui89_autonomy.supervisor import Mode, SystemStatus, evaluate_status


def healthy_status(**overrides):
    values = dict(
        perception_ok=True,
        localization_ok=True,
        communication_ok=True,
        safety_monitor_ok=True,
        operator_authorized=True,
        emergency_stop=False,
        hazard_clear=True,
        task_request_valid=True,
        confidence=0.95,
    )
    values.update(overrides)
    return SystemStatus(**values)


class SupervisorTests(unittest.TestCase):
    def test_healthy_inputs_only_propose_candidate_mode(self):
        decision = evaluate_status(healthy_status())
        self.assertEqual(decision.mode, Mode.AUTONOMOUS_CANDIDATE)
        self.assertTrue(any("not hardware safety certification" in reason for reason in decision.reasons))

    def test_emergency_stop_takes_priority(self):
        decision = evaluate_status(healthy_status(emergency_stop=True, operator_authorized=False))
        self.assertEqual(decision.mode, Mode.STOPPED)

    def test_failed_safety_monitor_stops(self):
        self.assertEqual(evaluate_status(healthy_status(safety_monitor_ok=False)).mode, Mode.STOPPED)

    def test_missing_authorization_requires_manual_recovery(self):
        self.assertEqual(evaluate_status(healthy_status(operator_authorized=False)).mode, Mode.MANUAL_RECOVERY)

    def test_invalid_task_requires_manual_recovery(self):
        self.assertEqual(evaluate_status(healthy_status(task_request_valid=False)).mode, Mode.MANUAL_RECOVERY)

    def test_sensor_or_link_failure_causes_safe_hold(self):
        for field in ("perception_ok", "localization_ok", "communication_ok", "hazard_clear"):
            with self.subTest(field=field):
                self.assertEqual(evaluate_status(healthy_status(**{field: False})).mode, Mode.SAFE_HOLD)

    def test_low_confidence_causes_safe_hold(self):
        self.assertEqual(evaluate_status(healthy_status(confidence=0.2)).mode, Mode.SAFE_HOLD)

    def test_non_finite_confidence_causes_safe_hold(self):
        for value in (math.nan, math.inf, -math.inf, -0.1, 1.1):
            with self.subTest(value=value):
                self.assertEqual(evaluate_status(healthy_status(confidence=value)).mode, Mode.SAFE_HOLD)

    def test_invalid_threshold_rejected(self):
        for threshold in (math.nan, math.inf, -0.1, 1.1):
            with self.subTest(threshold=threshold):
                with self.assertRaises(ValueError):
                    evaluate_status(healthy_status(), minimum_confidence=threshold)

    def test_decision_does_not_include_actuator_command(self):
        decision = evaluate_status(healthy_status())
        self.assertFalse(any("actuate" in step.lower() or "cut " in step.lower() for step in decision.permitted_next_steps))


if __name__ == "__main__":
    unittest.main()
