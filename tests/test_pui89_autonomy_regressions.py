"""Regression tests for the shared PUI89 autonomy policy and scenario validator.

Standard library only. These tests exercise software policy, not physical hardware.
Run from the repository root: python -m unittest discover -s tests -p "test_*.py"
"""
from __future__ import annotations
import copy
import importlib.util
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "pui89_autonomy_lab.py"
SPEC = importlib.util.spec_from_file_location("pui89_autonomy_lab_under_test", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load autonomy lab from {MODULE_PATH}")
LAB = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LAB)

def valid_config():
    return {
        "schema_version": 1,
        "project_id": "regression-test",
        "action_if_ready": "SIMULATED_MOVE",
        "confidence_threshold": 0.65,
        "scenarios": [{
            "id": "nominal", "seed": 7,
            "steps": [{"state": {}, "expected_action": "SIMULATED_MOVE", "dt_s": 1.0}],
        }],
    }

class StableEvidenceTests(unittest.TestCase):
    def test_stable_json_ignores_mapping_insertion_order(self):
        self.assertEqual(LAB.stable_json({"b": 2, "a": 1}), LAB.stable_json({"a": 1, "b": 2}))

    def test_digest_is_stable_for_same_input(self):
        self.assertEqual(LAB.digest("pui89"), LAB.digest("pui89"))
        self.assertNotEqual(LAB.digest("pui89"), LAB.digest("PUI89"))

    def test_valid_scenario_config_is_accepted(self):
        LAB.validate_config(valid_config())

    def test_duplicate_scenario_ids_are_rejected(self):
        config = valid_config()
        config["scenarios"].append(copy.deepcopy(config["scenarios"][0]))
        with self.assertRaisesRegex(ValueError, "duplicated"):
            LAB.validate_config(config)

    def test_boolean_is_not_accepted_as_numeric_confidence_threshold(self):
        config = valid_config()
        config["confidence_threshold"] = True
        with self.assertRaisesRegex(ValueError, "confidence_threshold"):
            LAB.validate_config(config)

    def test_nonpositive_step_duration_is_rejected(self):
        config = valid_config()
        config["scenarios"][0]["steps"][0]["dt_s"] = 0
        with self.assertRaisesRegex(ValueError, "dt_s"):
            LAB.validate_config(config)

class SafeActionPolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy = LAB.MockVLA(confidence_threshold=0.65)

    def test_nominal_state_only_proposes_configured_simulated_action(self):
        action, _ = self.policy.propose({}, "SIMULATED_MOVE")
        self.assertEqual(action, "SIMULATED_MOVE")

    def test_hazard_and_fault_flags_fail_safe_to_hold(self):
        cases = (
            {"emergency_stop": True}, {"sensors_ok": False},
            {"sensor_data_fresh": False}, {"comms_ok": False},
        )
        for state in cases:
            with self.subTest(state=state):
                action, _ = self.policy.propose(state, "SIMULATED_MOVE")
                self.assertEqual(action, "SAFE_HOLD")

    def test_malformed_safety_flag_does_not_count_as_safe(self):
        action, trace = self.policy.propose({"sensors_ok": "false"}, "SIMULATED_MOVE")
        self.assertEqual(action, "SAFE_HOLD")
        self.assertTrue(any("malformed_safety_flag" in item for item in trace))

    def test_conflicting_or_missing_required_modalities_return_unknown(self):
        for state in ({"modalities_conflict": True}, {"missing_required_modality": True}):
            with self.subTest(state=state):
                action, _ = self.policy.propose(state, "SIMULATED_MOVE")
                self.assertEqual(action, "UNKNOWN")

    def test_low_nonfinite_or_boolean_confidence_returns_unknown(self):
        for confidence in (0.1, math.nan, math.inf, True, "0.99"):
            with self.subTest(confidence=confidence):
                action, _ = self.policy.propose({"confidence": confidence}, "SIMULATED_MOVE")
                self.assertEqual(action, "UNKNOWN")

    def test_required_human_review_overrides_ready_action(self):
        action, _ = self.policy.propose({"human_review_required": True}, "SIMULATED_MOVE")
        self.assertEqual(action, "REQUEST_HUMAN_REVIEW")

    def test_high_impact_screening_action_is_blocked(self):
        action, _ = self.policy.propose({}, "REQUEST_ENFORCEMENT")
        self.assertEqual(action, "REQUEST_HUMAN_REVIEW")

    def test_missing_target_does_not_proceed_with_ready_action(self):
        action, _ = self.policy.propose({"target_visible": False}, "SIMULATED_MOVE")
        self.assertEqual(action, "SEARCH")

if __name__ == "__main__":
    unittest.main()
