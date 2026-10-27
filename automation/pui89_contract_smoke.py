"""PUI89 shared interface smoke checks. Standard-library only; no robot control."""
import argparse
import json
import math
import time
import unittest
from datetime import datetime, timezone
from pathlib import Path


def valid_confidence(value):
    return isinstance(value, (int, float)) and math.isfinite(value) and 0 <= value <= 1


def update_world_state(state, key, observation):
    if not key or not isinstance(key, str):
        raise ValueError("key must be a non-empty string")
    confidence = observation.get("confidence")
    if not valid_confidence(confidence):
        raise ValueError("confidence must be finite and within 0..1")
    state["observations"][key] = observation
    if confidence < 0.5:
        flag = "low_confidence:" + key
        if flag not in state["uncertainty_flags"]:
            state["uncertainty_flags"].append(flag)


def check_proposal(proposal, state_known, human_approved=False):
    """Evaluate a proposal only; this function never executes it."""
    confidence = proposal.get("confidence")
    if not proposal.get("action"):
        return False, "empty_action"
    if not valid_confidence(confidence):
        return False, "invalid_confidence"
    if not state_known:
        return False, "unknown_world_state"
    if confidence < 0.75:
        return False, "confidence_below_threshold"
    if proposal.get("requires_human_approval") and not human_approved:
        return False, "human_approval_required"
    if proposal.get("simulation_only") is not True:
        return False, "simulation_only_required"
    return True, "proposal_passed_for_simulation"


class ContractTests(unittest.TestCase):
    def test_valid_observation_updates_state(self):
        state = {"observations": {}, "uncertainty_flags": []}
        update_world_state(state, "target", {"value": "candidate", "confidence": 0.9})
        self.assertEqual(state["observations"]["target"]["value"], "candidate")
        self.assertEqual(state["uncertainty_flags"], [])

    def test_uncertainty_is_recorded(self):
        state = {"observations": {}, "uncertainty_flags": []}
        update_world_state(state, "target", {"value": None, "confidence": 0.2})
        self.assertIn("low_confidence:target", state["uncertainty_flags"])

    def test_invalid_confidence_is_rejected(self):
        state = {"observations": {}, "uncertainty_flags": []}
        with self.assertRaises(ValueError):
            update_world_state(state, "target", {"value": None, "confidence": float("nan")})

    def test_unknown_state_is_rejected(self):
        ok, reason = check_proposal({"action": "observe", "confidence": 0.95, "simulation_only": True}, False)
        self.assertFalse(ok)
        self.assertEqual(reason, "unknown_world_state")

    def test_low_confidence_is_rejected(self):
        ok, reason = check_proposal({"action": "observe", "confidence": 0.4, "simulation_only": True}, True)
        self.assertFalse(ok)
        self.assertEqual(reason, "confidence_below_threshold")

    def test_human_review_gate(self):
        proposal = {"action": "review_case", "confidence": 0.9, "requires_human_approval": True, "simulation_only": True}
        ok, reason = check_proposal(proposal, True)
        self.assertFalse(ok)
        self.assertEqual(reason, "human_approval_required")

    def test_non_simulated_proposal_is_rejected(self):
        ok, reason = check_proposal({"action": "move", "confidence": 0.95, "simulation_only": False}, True)
        self.assertFalse(ok)
        self.assertEqual(reason, "simulation_only_required")

    def test_safe_simulated_proposal_passes(self):
        ok, reason = check_proposal({"action": "observe", "confidence": 0.9, "simulation_only": True}, True)
        self.assertTrue(ok)
        self.assertEqual(reason, "proposal_passed_for_simulation")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", default="reports/pui89-contract-smoke.json")
    args = parser.parse_args()
    started = time.perf_counter()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ContractTests)
    result = unittest.TestResult()
    suite.run(result)
    report = {
        "schema_version": "1.0",
        "suite": "pui89-shared-interface-smoke",
        "status": "pass" if result.wasSuccessful() else "fail",
        "tests_run": result.testsRun,
        "failures": [{"test": test.id(), "details": detail} for test, detail in result.failures + result.errors],
        "duration_seconds": round(time.perf_counter() - started, 6),
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope_note": "Interface and proposal-gate checks only; no model accuracy or physical performance is measured.",
    }
    path = Path(args.report)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
