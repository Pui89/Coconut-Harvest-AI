"""Tests for the synthetic agent evaluation harness; standard library only."""
from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.evaluate_agentic_workflow import (
    evaluate_scenarios,
    load_scenarios,
)


ROOT = Path(__file__).resolve().parents[1]


class AgentEvaluationTests(unittest.TestCase):
    def test_repository_synthetic_suite_passes(self):
        manifest = load_scenarios(ROOT / "examples" / "agentic_workflow.evaluation.json")
        report = evaluate_scenarios(manifest)
        self.assertEqual(report["result"], "PASS", report["scenarios"])
        self.assertEqual(report["metrics"]["failed_count"], 0)
        self.assertGreaterEqual(report["metrics"]["scenario_count"], 5)
        self.assertTrue(report["synthetic_only"])
        self.assertFalse(report["resource_profile"]["network_access_used"])
        self.assertFalse(report["resource_profile"]["model_inference_used"])
        self.assertFalse(report["resource_profile"]["hardware_actuation_used"])

    def test_report_does_not_copy_observation_payloads(self):
        manifest = load_scenarios(ROOT / "examples" / "agentic_workflow.evaluation.json")
        report_text = json.dumps(evaluate_scenarios(manifest))
        for scenario in manifest["scenarios"]:
            self.assertNotIn(json.dumps(scenario["observation"], sort_keys=True), report_text)
        self.assertNotIn('"observation":', report_text)

    def test_status_mismatch_fails_evaluation(self):
        manifest = load_scenarios(ROOT / "examples" / "agentic_workflow.evaluation.json")
        manifest["scenarios"] = [dict(manifest["scenarios"][0])]
        manifest["scenarios"][0]["expected_decision_status"] = "IMPOSSIBLE_STATUS"
        report = evaluate_scenarios(manifest)
        self.assertEqual(report["result"], "FAIL")
        self.assertEqual(report["metrics"]["failed_count"], 1)
        self.assertFalse(report["scenarios"][0]["passed"])

    def test_loader_rejects_nonstandard_json_constants(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "invalid.json"
            path.write_text(
                '{"schema_version": 1, "synthetic_only": true, '
                '"evaluation_id": "bad", "scenarios": [], "x": NaN}',
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                load_scenarios(path)

    def test_loader_rejects_duplicate_scenario_ids(self):
        manifest = load_scenarios(ROOT / "examples" / "agentic_workflow.evaluation.json")
        manifest["scenarios"].append(dict(manifest["scenarios"][0]))
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "duplicate.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unique"):
                load_scenarios(path)


if __name__ == "__main__":
    unittest.main()
