import unittest
from unittest.mock import patch

from agents.agentic_workflow import run_agentic_workflow


class AgenticWorkflowTests(unittest.TestCase):
    def test_empty_observation_returns_auditable_review_proposal(self):
        report = run_agentic_workflow({})
        self.assertEqual(report["status"], "PROPOSAL_READY_FOR_HUMAN_REVIEW")
        self.assertTrue(report["human_review_required"])
        self.assertFalse(report["execution_performed"])
        self.assertFalse(report["network_access_used"])
        self.assertFalse(report["model_inference_used"])
        self.assertFalse(report["actuator_commands_issued"])
        self.assertIs(report["decision"]["requires_human_approval"], True)
        self.assertIsNone(report["decision"]["actuator_command"])
        self.assertEqual(len(report["evidence_sha256"]), 64)

    def test_non_object_input_is_inconclusive(self):
        report = run_agentic_workflow(["not", "an", "object"])
        self.assertEqual(report["status"], "INCONCLUSIVE")
        self.assertIsNone(report["evidence_sha256"])
        self.assertTrue(report["human_review_required"])
        self.assertFalse(report["execution_performed"])

    def test_non_finite_observation_is_rejected(self):
        report = run_agentic_workflow({"confidence": float("nan")})
        self.assertEqual(report["status"], "INCONCLUSIVE")
        self.assertIsNone(report["evidence_sha256"])

    def test_repeatable_input_produces_same_evidence_hash(self):
        observation = {"target_detected": True, "confidence": 0.75}
        first = run_agentic_workflow(observation)
        second = run_agentic_workflow(observation)
        self.assertEqual(first["evidence_sha256"], second["evidence_sha256"])

    def test_agent_proposal_never_performs_actuation(self):
        report = run_agentic_workflow(
            {
                "target_detected": True,
                "confidence": 0.95,
                "depth_m": 2.0,
                "reachable": True,
                "obstacle_clear": True,
                "human_approved": True,
                "requested_command": "CUT_NOW",
            }
        )
        self.assertFalse(report["actuator_commands_issued"])
        self.assertFalse(report["execution_performed"])
        self.assertIsNone(report["decision"]["actuator_command"])
        self.assertTrue(report["human_review_required"])

    def test_policy_gate_blocks_an_agent_that_tries_to_issue_commands(self):
        class UnsafeDecision:
            def to_dict(self):
                return {
                    "project": "test",
                    "status": "READY",
                    "recommendation": "RUN_COMMAND",
                    "reasons": [],
                    "requires_human_approval": False,
                    "actuator_command": "MOVE",
                }

        with patch("agents.agentic_workflow.run_agent", return_value=UnsafeDecision()):
            report = run_agentic_workflow({"sensor_ok": True})

        self.assertEqual(report["status"], "BLOCKED_BY_POLICY")
        self.assertIsNone(report["decision"])
        self.assertTrue(report["issues"])
        self.assertFalse(report["actuator_commands_issued"])
        self.assertTrue(report["human_review_required"])


if __name__ == "__main__":
    unittest.main()
