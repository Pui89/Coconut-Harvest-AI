"""Cross-project conformance tests for the PUI89 simulation-only action policy.

Stdlib-only: no downloads, network access, optional models, or hardware commands.
"""
from __future__ import annotations

import importlib.util
import math
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "pui89_autonomy_lab.py"
SPEC = importlib.util.spec_from_file_location("pui89_autonomy_lab_conformance", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
MockVLA = MODULE.MockVLA

REQUIRED_FLAGS = {
    "emergency_stop": False,
    "sensors_ok": True,
    "sensor_data_fresh": True,
    "comms_ok": True,
}
READY_STATE = {
    **REQUIRED_FLAGS,
    "target_visible": True,
    "target_valid": True,
    "human_review_required": False,
    "operator_approved": True,
    "confidence": 0.95,
}


class PUI89AICoreConformanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.policy = MockVLA()

    def test_healthy_state_returns_simulation_only_proposal(self) -> None:
        action, trace = self.policy.propose(dict(READY_STATE), "SIMULATED_TASK")
        self.assertEqual(action, "SIMULATED_TASK")
        self.assertIn("simulation_only_action", trace)

    def test_each_missing_required_safety_flag_fails_closed(self) -> None:
        for flag in REQUIRED_FLAGS:
            with self.subTest(flag=flag):
                state = dict(READY_STATE)
                state.pop(flag)
                action, trace = self.policy.propose(state, "SIMULATED_TASK")
                self.assertEqual(action, "SAFE_HOLD")
                self.assertTrue(any(flag in item for item in trace))

    def test_malformed_required_safety_telemetry_fails_closed(self) -> None:
        for flag in REQUIRED_FLAGS:
            for bad_value in ("false", "true", 0, 1, None, [], {}):
                with self.subTest(flag=flag, bad_value=bad_value):
                    state = {**READY_STATE, flag: bad_value}
                    self.assertEqual(self.policy.propose(state, "SIMULATED_TASK")[0], "SAFE_HOLD")

    def test_active_safety_fault_fails_closed(self) -> None:
        faults = (
            ("emergency_stop", True),
            ("sensors_ok", False),
            ("sensor_data_fresh", False),
            ("comms_ok", False),
        )
        for flag, bad_value in faults:
            with self.subTest(flag=flag):
                self.assertEqual(
                    self.policy.propose({**READY_STATE, flag: bad_value}, "SIMULATED_TASK")[0],
                    "SAFE_HOLD",
                )

    def test_missing_confidence_abstains(self) -> None:
        state = dict(READY_STATE)
        state.pop("confidence")
        action, trace = self.policy.propose(state, "SIMULATED_TASK")
        self.assertEqual(action, "UNKNOWN")
        self.assertTrue(any("confidence_missing" in item for item in trace))

    def test_invalid_confidence_abstains(self) -> None:
        invalid_values = (True, False, "0.9", None, -0.01, 1.01, math.nan, math.inf, -math.inf)
        for confidence in invalid_values:
            with self.subTest(confidence=confidence):
                self.assertEqual(
                    self.policy.propose({**READY_STATE, "confidence": confidence}, "SIMULATED_TASK")[0],
                    "UNKNOWN",
                )

    def test_low_confidence_abstains(self) -> None:
        self.assertEqual(
            self.policy.propose({**READY_STATE, "confidence": 0.1}, "SIMULATED_TASK")[0],
            "UNKNOWN",
        )

    def test_conflicting_or_missing_modality_abstains(self) -> None:
        for flag in ("modalities_conflict", "missing_required_modality"):
            with self.subTest(flag=flag):
                self.assertEqual(
                    self.policy.propose({**READY_STATE, flag: True}, "SIMULATED_TASK")[0],
                    "UNKNOWN",
                )

    def test_required_human_review_is_not_bypassed(self) -> None:
        state = {**READY_STATE, "human_review_required": True}
        self.assertEqual(self.policy.propose(state, "SIMULATED_TASK")[0], "REQUEST_HUMAN_REVIEW")

    def test_high_impact_action_label_is_blocked(self) -> None:
        self.assertEqual(
            self.policy.propose(READY_STATE, "REQUEST_ENFORCEMENT")[0],
            "REQUEST_HUMAN_REVIEW",
        )

    def test_invalid_state_fails_closed(self) -> None:
        self.assertEqual(self.policy.propose(None, "SIMULATED_TASK")[0], "SAFE_HOLD")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
