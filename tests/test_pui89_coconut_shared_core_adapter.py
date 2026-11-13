"""Tests for the Coconut-to-Shared-AI-Core advisory adapter."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from pui89_coconut_shared_core_adapter import build_shared_core_records


def sample_request():
    return {
        "request_id": "coconut-fixture-001",
        "timestamp": "2026-11-13T10:00:01Z",
        "evidence": {
            "source_id": "synthetic-fixture-001",
            "source_ref": "synthetic://coconut/fixture-001",
            "source_type": "simulation",
            "timestamp": "2026-11-13T10:00:00Z",
            "lineage": ["unit-test", "synthetic-only"],
        },
    }


def sample_orchard_report():
    return {
        "tree": {"height_m": None, "height_band": "UNKNOWN", "height_status": "unverified"},
        "fruit_count": 1,
        "maturity_counts": {"mature_green": 1},
        "fruit_observations": [{
            "fruit_id": "fruit-001", "image_id": "image-fixture-001",
            "maturity_class": "mature_green", "source_kind": "synthetic_test",
            "class_confidence": None, "bbox_xyxy_normalized": [0.1, 0.2, 0.5, 0.8],
            "review_status": "pending", "disposition": "synthetic_only",
            "errors": [], "harvest_authorized": False,
        }],
        "decision_boundary": {
            "image_classification_performed": False,
            "height_inferred_from_pixels": False,
            "automatic_harvest_authorized": False,
        },
    }


class CoconutSharedCoreAdapterTests(unittest.TestCase):
    def test_builds_four_base_contracts_without_actuation(self):
        result = build_shared_core_records(sample_request(), sample_orchard_report())
        self.assertEqual(result["observation"]["schema_version"], "0.1.0")
        self.assertEqual(result["world_state"]["schema_version"], "0.1.0")
        self.assertEqual(result["action_proposal"]["schema_version"], "0.1.0")
        self.assertEqual(result["evidence_passport"]["schema_version"], "0.1.0")
        self.assertIsNone(result["failure_report"])
        self.assertEqual(result["action_proposal"]["actions"], [])
        self.assertFalse(result["action_proposal"]["authority"]["execution_authorized"])
        self.assertFalse(result["evidence_passport"]["execution_authorized"])
        self.assertFalse(result["physical_actuation_permitted"])
        self.assertFalse(result["model_inference_performed"])

    def test_emits_failure_report_only_for_explicit_failure_event(self):
        event = {
            "failure_id": "failure-001", "occurred_at": "2026-11-13T10:00:00Z",
            "system_or_component": "synthetic fixture parser", "severity": "low",
            "summary": "Synthetic test failure event",
            "observed_result": "Fixture intentionally marked invalid",
        }
        result = build_shared_core_records(
            sample_request(), sample_orchard_report(), failure_event=event
        )
        self.assertEqual(result["failure_report"]["failure_id"], "failure-001")
        self.assertEqual(result["failure_report"]["evidence_refs"], [
            "coconut-coconut-fixture-001-observation"
        ])

    def test_rejects_future_dated_evidence(self):
        request = sample_request()
        request["evidence"]["timestamp"] = "2026-11-13T10:00:02Z"
        with self.assertRaises(ValueError):
            build_shared_core_records(request, sample_orchard_report())

    def test_rejects_missing_provenance_lineage(self):
        request = sample_request()
        request["evidence"]["lineage"] = []
        with self.assertRaises(ValueError):
            build_shared_core_records(request, sample_orchard_report())

    def test_rejects_any_harvest_authority(self):
        report = sample_orchard_report()
        report["fruit_observations"][0]["harvest_authorized"] = True
        with self.assertRaises(ValueError):
            build_shared_core_records(sample_request(), report)

    def test_rejects_physical_command_fields(self):
        request = sample_request()
        request["robot_command"] = {"cut": True}
        with self.assertRaises(ValueError):
            build_shared_core_records(request, sample_orchard_report())

    def test_rejects_naive_timestamps(self):
        request = sample_request()
        request["timestamp"] = "2026-11-13T10:00:01"
        with self.assertRaises(ValueError):
            build_shared_core_records(request, sample_orchard_report())


if __name__ == "__main__":
    unittest.main()
