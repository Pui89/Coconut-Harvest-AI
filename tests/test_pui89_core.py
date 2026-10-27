"""Standard-library tests: run with python -m unittest discover -s tests -v."""
import json
import tempfile
import unittest
from pathlib import Path

from pui89_core import ActionProposal, TrackedObject, WorldState, propose_action, write_failure_report


class WorldStateTests(unittest.TestCase):
    def test_upsert_and_serialization(self):
        state = WorldState()
        state.upsert(TrackedObject("obj-1", "coconut", 0.9, {"stage": "mature-green"}))
        data = state.to_dict()
        self.assertEqual(data["objects"]["obj-1"]["label"], "coconut")
        self.assertEqual(data["objects"]["obj-1"]["confidence"], 0.9)

    def test_invalid_confidence_rejected(self):
        with self.assertRaises(ValueError):
            TrackedObject("obj-1", "person", 1.2)

    def test_empty_id_rejected(self):
        with self.assertRaises(ValueError):
            TrackedObject("", "person", 0.5)


class PlanningTests(unittest.TestCase):
    def test_proposal_is_simulation_only_and_not_executed(self):
        proposal = propose_action("inspect_target", "uncertainty remains", 0.6)
        self.assertTrue(proposal.simulation_only)
        self.assertTrue(proposal.requires_human_review)
        self.assertFalse(proposal.executed)

    def test_direct_execution_configuration_rejected(self):
        with self.assertRaises(ValueError):
            ActionProposal("move", "test", 0.8, simulation_only=False)


class ReportingTests(unittest.TestCase):
    def test_failure_report_is_reproducibly_structured(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_failure_report(Path(tmp) / "report.json", [{"test": "x", "error": "expected"}])
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["schema_version"], "1.0")
            self.assertEqual(data["failure_count"], 1)
            self.assertEqual(data["failures"][0]["test"], "x")


if __name__ == "__main__":
    unittest.main()
