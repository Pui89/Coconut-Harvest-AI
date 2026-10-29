"""Standard-library tests for shared PUI89 state, planning, and reporting."""
import json
import tempfile
import unittest
from pathlib import Path

from pui89_core import (
    ActionProposal, TrackedObject, WorldState, propose_action, write_failure_report,
)


class WorldStateTests(unittest.TestCase):
    def test_upsert_and_serialization(self):
        state = WorldState()
        state.upsert(TrackedObject("obj-1", "coconut", 0.9, {"stage": "mature-green"}))
        data = state.to_dict()
        self.assertEqual(data["objects"]["obj-1"]["label"], "coconut")
        self.assertEqual(data["objects"]["obj-1"]["confidence"], 0.9)

    def test_invalid_confidence_rejected(self):
        for confidence in (-0.01, 1.01):
            with self.subTest(confidence=confidence), self.assertRaises(ValueError):
                TrackedObject("obj-1", "person", confidence)

    def test_confidence_boundaries_are_valid(self):
        self.assertEqual(TrackedObject("low", "object", 0.0).confidence, 0.0)
        self.assertEqual(TrackedObject("high", "object", 1.0).confidence, 1.0)

    def test_empty_id_and_label_rejected(self):
        with self.assertRaises(ValueError):
            TrackedObject("", "person", 0.5)
        with self.assertRaises(ValueError):
            TrackedObject("obj-1", " ", 0.5)

    def test_upsert_replaces_existing_object(self):
        state = WorldState()
        state.upsert(TrackedObject("obj-1", "unknown", 0.2))
        state.upsert(TrackedObject("obj-1", "coconut", 0.9))
        self.assertEqual(len(state.objects), 1)
        self.assertEqual(state.objects["obj-1"].label, "coconut")

    def test_serialization_order_is_stable(self):
        state = WorldState()
        state.upsert(TrackedObject("z", "zebra", 0.5))
        state.upsert(TrackedObject("a", "apple", 0.5))
        self.assertEqual(list(state.to_dict()["objects"]), ["a", "z"])


class PlanningTests(unittest.TestCase):
    def test_proposal_is_simulation_only_and_not_executed(self):
        proposal = propose_action("inspect_target", "uncertainty remains", 0.6)
        self.assertTrue(proposal.simulation_only)
        self.assertTrue(proposal.requires_human_review)
        self.assertFalse(proposal.executed)

    def test_direct_execution_configuration_rejected(self):
        with self.assertRaises(ValueError):
            ActionProposal("move", "test", 0.8, simulation_only=False)

    def test_executed_proposal_rejected(self):
        with self.assertRaises(ValueError):
            ActionProposal("move", "test", 0.8, executed=True)

    def test_invalid_proposal_confidence_rejected(self):
        with self.assertRaises(ValueError):
            propose_action("inspect", "test", 1.2)

    def test_empty_action_rejected(self):
        with self.assertRaises(ValueError):
            propose_action(" ", "test", 0.5)


class ReportingTests(unittest.TestCase):
    def test_failure_report_is_reproducibly_structured(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_failure_report(
                Path(tmp) / "report.json", [{"test": "x", "error": "expected"}]
            )
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["schema_version"], "1.0")
            self.assertEqual(data["failure_count"], 1)
            self.assertEqual(data["failures"][0]["test"], "x")

    def test_empty_failure_report_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_failure_report(Path(tmp) / "report.json", [])
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["failure_count"], 0)
            self.assertEqual(data["failures"], [])


if __name__ == "__main__":
    unittest.main()
