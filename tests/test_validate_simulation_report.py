import csv
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from validate_simulation_report import stable_json, validate  # noqa: E402

class SimulationReportValidatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.config = {"schema_version": 1, "project_id": "validator-test", "scenarios": []}
        self.config_path = self.root / "scenarios.json"
        self.config_path.write_text(json.dumps(self.config), encoding="utf-8")
        self.csv_path = self.root / "steps.csv"
        with self.csv_path.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=["project_id", "hardware_actuation"])
            writer.writeheader()
            writer.writerow({"project_id": "validator-test", "hardware_actuation": "false"})
        self.report_path = self.root / "report.json"
        self.report = {
            "schema_version": 1,
            "project_id": "validator-test",
            "run_id": "test-run",
            "scenario_config_sha256": hashlib.sha256(stable_json(self.config).encode()).hexdigest(),
            "status": "PASS",
            "metrics": {
                "scenario_count": 1, "scenario_pass_count": 1,
                "step_count": 1, "step_pass_count": 1, "failure_count": 0,
                "step_pass_rate": 1.0, "scenario_pass_rate": 1.0,
                "action_counts": {"SAFE_HOLD": 1}, "safe_hold_count": 1
            },
            "scenarios": [{"passed": True}],
            "steps": [{"passed": True, "hardware_actuation": False}],
            "failures": [],
            "output_files": {"csv": str(self.csv_path)}
        }
        self.save_report()

    def save_report(self):
        self.report_path.write_text(json.dumps(self.report), encoding="utf-8")

    def test_valid_report_passes(self):
        self.assertEqual(validate(self.report_path, self.config_path), [])

    def test_config_hash_mismatch_is_detected(self):
        self.report["scenario_config_sha256"] = "0" * 64
        self.save_report()
        self.assertTrue(any("SHA-256 mismatch" in error for error in validate(self.report_path, self.config_path)))

    def test_inconsistent_step_count_is_detected(self):
        self.report["metrics"]["step_count"] = 2
        self.save_report()
        self.assertTrue(any("step_count" in error for error in validate(self.report_path, self.config_path)))

    def test_hardware_actuation_claim_is_rejected(self):
        self.report["steps"][0]["hardware_actuation"] = True
        self.save_report()
        self.assertTrue(any("hardware_actuation" in error for error in validate(self.report_path, self.config_path)))

if __name__ == "__main__":
    unittest.main()
