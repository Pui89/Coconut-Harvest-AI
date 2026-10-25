import unittest
from unittest.mock import patch

from agents.agentic_workflow import run_agentic_workflow


class AgenticWorkflowFailureTests(unittest.TestCase):
    def test_unexpected_agent_exception_returns_inconclusive_report(self):
        with patch(
            "agents.agentic_workflow.run_agent",
            side_effect=RuntimeError("private diagnostic should not leak"),
        ):
            report = run_agentic_workflow({"sensor_ok": True})

        self.assertEqual(report["status"], "INCONCLUSIVE")
        self.assertTrue(report["human_review_required"])
        self.assertFalse(report["execution_performed"])
        self.assertFalse(report["network_access_used"])
        self.assertFalse(report["model_inference_used"])
        self.assertFalse(report["actuator_commands_issued"])
        self.assertEqual(report["trace"][-1], {"step": "project_agent", "status": "failed"})
        self.assertIn("project decision agent", report["issues"][0])
        self.assertNotIn("private diagnostic", report["issues"][0])


if __name__ == "__main__":
    unittest.main()
