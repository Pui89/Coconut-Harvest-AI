import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from pui89_evidence_benchmark import build, summarize


class EvidenceBenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.report_path = self.root / "report.json"
        self.report = {
            "schema_version": 1, "project_id": "sample-project", "run_id": "abc123",
            "scenario_config_sha256": "a" * 64, "status": "PASS",
            "metrics": {"scenario_count": 1, "scenario_pass_count": 1, "step_count": 1,
                        "step_pass_count": 1, "failure_count": 0, "step_pass_rate": 1.0,
                        "scenario_pass_rate": 1.0, "safe_hold_count": 0},
            "scenarios": [{"passed": True}],
            "steps": [{"passed": True, "hardware_actuation": False,
                       "state": {"sensor_data_fresh": True, "confidence": 0.9}}],
            "failures": []
        }
        self.save()

    def save(self):
        self.report_path.write_text(json.dumps(self.report), encoding="utf-8")

    def test_valid_report_gets_hashes_and_no_actuation(self):
        result = summarize(self.report_path)
        self.assertEqual(result["world_state_snapshot_count"], 1)
        self.assertEqual(len(result["world_state_sequence_sha256"]), 64)
        self.assertFalse(result["hardware_actuation"])

    def test_state_change_changes_world_state_sequence_hash(self):
        before = summarize(self.report_path)["world_state_sequence_sha256"]
        self.report["steps"][0]["state"]["sensor_data_fresh"] = False
        self.save()
        after = summarize(self.report_path)["world_state_sequence_sha256"]
        self.assertNotEqual(before, after)

    def test_hardware_actuation_claim_is_rejected(self):
        self.report["steps"][0]["hardware_actuation"] = True
        self.save()
        with self.assertRaises(ValueError):
            summarize(self.report_path)

    def test_inconsistent_metrics_are_rejected(self):
        self.report["metrics"]["step_pass_count"] = 0
        self.save()
        with self.assertRaises(ValueError):
            summarize(self.report_path)

    def test_failed_report_is_preserved_as_valid_evidence(self):
        self.report["status"] = "FAIL"
        self.report["metrics"]["failure_count"] = 1
        self.report["metrics"]["step_pass_count"] = 0
        self.report["steps"][0]["passed"] = False
        self.report["failures"] = [{"scenario_id": "one", "step_index": 1}]
        self.save()
        result = summarize(self.report_path)
        self.assertEqual(result["status"], "FAIL")
        self.assertEqual(result["failure_count"], 1)

    def test_duplicate_projects_are_rejected(self):
        with self.assertRaises(ValueError):
            build([self.report_path, self.report_path])


if __name__ == "__main__":
    unittest.main()
