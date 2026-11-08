"""Dependency-free conformance smoke tests for the Coconut v0.1 mapping."""
import json
import os
import unittest
from pathlib import Path

from pui89_coconut_adapter import build_coconut_message
from pui89_shared_core_v01 import build_coconut_v01_records

NOW = "2026-10-31T00:00:00+00:00"


class CoconutSharedCoreV01Tests(unittest.TestCase):
    def make_record(self, **overrides):
        values = {
            "observation_id": "coco-v01-001",
            "source_ref": "synthetic-fixture:coco-v01-001",
            "timestamp": NOW,
            "maturity_label": "mature_green",
            "modality": "rgb",
            "evidence_kind": "synthetic",
        }
        values.update(overrides)
        return build_coconut_message(**values)

    def test_maps_to_shared_observation_and_advisory_proposal(self):
        bundle = build_coconut_v01_records(self.make_record())
        observation = bundle["observation"]
        proposal = bundle["action_proposal"]

        self.assertEqual(observation["schema_version"], "0.1.0")
        self.assertEqual(observation["source"]["source_type"], "simulation")
        self.assertEqual(observation["quality"]["status"], "unknown")
        self.assertEqual(observation["payload"]["claims"][0]["value"], "mature_green")
        self.assertEqual(proposal["schema_version"], "0.1.0")
        self.assertEqual(proposal["authority"]["mode"], "advisory_only")
        self.assertIs(proposal["authority"]["human_approval_required"], True)
        self.assertIs(proposal["authority"]["execution_authorized"], False)
        self.assertEqual(proposal["actions"][0]["evidence_refs"], ["coco-v01-001"])

    def test_caller_label_is_not_promoted_to_sensor_truth(self):
        bundle = build_coconut_v01_records(self.make_record(evidence_kind="inferred"))
        observation = bundle["observation"]
        self.assertEqual(observation["source"]["source_type"], "human")
        self.assertEqual(observation["quality"]["status"], "unknown")

    def test_rejects_unsupported_modality(self):
        record = self.make_record(modality="ultrasound")
        with self.assertRaises(ValueError):
            build_coconut_v01_records(record)

    def test_rejects_timezone_missing(self):
        record = self.make_record(timestamp="2026-10-31T00:00:00")
        with self.assertRaises(ValueError):
            build_coconut_v01_records(record)

    def test_matches_pinned_shared_core_schema_invariants(self):
        core_dir = os.environ.get("PUI89_SHARED_CORE_DIR")
        if not core_dir:
            self.skipTest("Shared AI Core checkout is supplied by the GitHub Actions workflow")
        schema_dir = Path(core_dir) / "schemas" / "v0.1"
        for filename, required in (
            ("observation.schema.json", {"schema_version", "observation_id", "observed_at", "source", "modality", "payload", "quality", "provenance"}),
            ("action-proposal.schema.json", {"schema_version", "proposal_id", "created_at", "objective", "actions", "authority"}),
        ):
            with self.subTest(schema=filename):
                schema = json.loads((schema_dir / filename).read_text(encoding="utf-8"))
                self.assertEqual(schema["properties"]["schema_version"]["const"], "0.1.0")
                self.assertTrue(required.issubset(set(schema["required"])))
        bundle = build_coconut_v01_records(self.make_record())
        for key, filename in (
            ("observation", "observation.schema.json"),
            ("action_proposal", "action-proposal.schema.json"),
        ):
            schema = json.loads((schema_dir / filename).read_text(encoding="utf-8"))
            self.assertTrue(set(schema["required"]).issubset(bundle[key].keys()))


if __name__ == "__main__":
    unittest.main()
