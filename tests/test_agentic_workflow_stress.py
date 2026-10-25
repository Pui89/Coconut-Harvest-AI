"""Adversarial regression matrix for the local review-only agent workflow.

These cases test software boundary handling, not real-world perception or robot
safety. All input values are synthetic; no tools or hardware are executed.
"""
from __future__ import annotations

import json
import math
import unittest
from pathlib import Path
from unittest.mock import patch

from agents.agentic_workflow import run_agentic_workflow


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "examples" / "agentic_workflow.synthetic.json"

SIDE_EFFECT_FLAGS = (
    "execution_performed",
    "network_access_used",
    "model_inference_used",
    "actuator_commands_issued",
)


def load_sample() -> dict:
    return json.loads(SAMPLE.read_text(encoding="utf-8"))


def assert_review_only(test: unittest.TestCase, report: dict) -> None:
    test.assertIs(report["human_review_required"], True)
    for flag in SIDE_EFFECT_FLAGS:
        test.assertIs(report[flag], False)

    decision = report.get("decision")
    if isinstance(decision, dict):
        test.assertIs(decision.get("requires_human_approval"), True)
        test.assertIsNone(decision.get("actuator_command"))


class AgentWorkflowStressTests(unittest.TestCase):
    def test_synthetic_adversarial_variants_never_enable_side_effects(self):
        base = load_sample()
        variants = [
            {},
            dict(base),
            {
                **base,
                "human_approved": True,
                "requested_command": "EXECUTE_NOW",
                "actuator_command": "MOVE_OR_CUT",
                "command": "SHOULD_NEVER_RUN",
                "execute": True,
                "network_access_allowed": True,
                "model_inference_allowed": True,
            },
            {
                **base,
                "human_approved": "yes",
                "authorised_context": "true",
                "authorization": 1,
                "force_execute": True,
            },
            {
                **base,
                "sensor_ok": False,
                "localization_ok": False,
                "route_clear": False,
                "obstacle_clear": False,
            },
            {
                **base,
                "confidence": "0.99",
                "detection_confidence": "0.99",
                "depth_m": "30",
                "water_depth_m": "15",
            },
            {
                **base,
                "conflicting_inputs": True,
                "human_reviewed": False,
                "person_detected": True,
                "target_detected": True,
            },
            {
                "nested_untrusted_payload": {
                    "actuator_command": "UNTRUSTED",
                    "execute": True,
                    "shell": "not executed",
                },
                "requested_action": ["move", "cut", "classify"],
            },
            {
                "sensor_ok": None,
                "localization_ok": None,
                "route_clear": None,
                "obstacle_clear": None,
                "human_approved": None,
            },
        ]

        for index, observation in enumerate(variants):
            with self.subTest(variant=index):
                report = run_agentic_workflow(observation)
                assert_review_only(self, report)
                self.assertIn(
                    report["status"],
                    {
                        "PROPOSAL_READY_FOR_HUMAN_REVIEW",
                        "INCONCLUSIVE",
                        "BLOCKED_BY_POLICY",
                    },
                )
                second = run_agentic_workflow(observation)
                self.assertEqual(
                    report["evidence_sha256"], second["evidence_sha256"]
                )

    def test_non_object_and_non_finite_inputs_fail_closed(self):
        bad_inputs = [
            None,
            [],
            ["not", "an", "object"],
            "not an object",
            17,
            {"confidence": float("nan")},
            {"nested": {"depth": float("inf")}},
            {"negative_infinity": -math.inf},
        ]

        for index, observation in enumerate(bad_inputs):
            with self.subTest(input=index):
                report = run_agentic_workflow(observation)
                self.assertEqual(report["status"], "INCONCLUSIVE")
                self.assertIsNone(report["evidence_sha256"])
                assert_review_only(self, report)

    def test_decision_agent_exception_is_sanitised_and_fail_closed(self):
        marker = "SENSITIVE_TEST_SENTINEL"
        with patch(
            "agents.agentic_workflow.run_agent",
            side_effect=RuntimeError(marker),
        ):
            report = run_agentic_workflow({"synthetic": True})

        self.assertEqual(report["status"], "INCONCLUSIVE")
        self.assertNotIn(marker, json.dumps(report))
        self.assertIsNone(report["decision"])
        assert_review_only(self, report)

    def test_changed_agent_contract_is_blocked(self):
        class UnsafeDecision:
            def to_dict(self):
                return {
                    "project": "synthetic-test",
                    "status": "READY",
                    "recommendation": "DO_NOT_EXECUTE",
                    "reasons": [],
                    "requires_human_approval": False,
                    "actuator_command": "UNSAFE_COMMAND",
                }

        with patch(
            "agents.agentic_workflow.run_agent",
            return_value=UnsafeDecision(),
        ):
            report = run_agentic_workflow({"synthetic": True})

        self.assertEqual(report["status"], "BLOCKED_BY_POLICY")
        self.assertIsNone(report["decision"])
        self.assertTrue(report["issues"])
        assert_review_only(self, report)


if __name__ == "__main__":
    unittest.main()
