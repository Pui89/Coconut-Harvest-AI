import json, sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from pui89_autonomy_lab import MockVLA, model_preflight, run_scenarios  # noqa: E402

class MockVLAGuardTests(unittest.TestCase):
    def setUp(self): self.policy = MockVLA(0.65)
    def test_estop_sensor_stale_comms_hold(self):
        for state in ({"emergency_stop": True},{"sensors_ok": False},{"sensor_data_fresh": False},{"comms_ok": False}):
            with self.subTest(state=state): self.assertEqual(self.policy.propose(state,"SIM_ACTION")[0],"SAFE_HOLD")
    def test_low_confidence_or_conflicting_modalities_abstain(self):
        for state in ({"confidence":0.2},{"modalities_conflict":True},{"missing_required_modality":True},{"confidence":2.0}):
            with self.subTest(state=state): self.assertEqual(self.policy.propose(state,"SIM_ACTION")[0],"UNKNOWN")
    def test_missing_target_searches(self):
        self.assertEqual(self.policy.propose({"target_visible":False},"SIM_ACTION")[0],"SEARCH")
    def test_human_review_blocks_nominal_action(self):
        self.assertEqual(self.policy.propose({"human_review_required":True},"ENFORCEMENT_ACTION")[0],"REQUEST_HUMAN_REVIEW")
    def test_simulation_has_stable_id_and_never_actuates(self):
        with tempfile.TemporaryDirectory() as tmp:
            report=run_scenarios(ROOT/"simulation/scenarios.json",Path(tmp))
            self.assertEqual(report["metrics"]["failure_count"],0)
            again=run_scenarios(ROOT/"simulation/scenarios.json",Path(tmp))
            self.assertEqual(report["run_id"],again["run_id"])
            self.assertTrue(all(not row["hardware_actuation"] for row in report["steps"]))
            saved=json.loads(Path(report["output_files"]["json"]).read_text(encoding="utf-8"))
            self.assertEqual(saved["run_id"],report["run_id"])
    def test_model_preflight_never_downloads(self):
        with tempfile.TemporaryDirectory() as tmp: report=model_preflight(Path(tmp))
        self.assertFalse(report["download_performed"]); self.assertFalse(report["software_installed"])
        self.assertFalse(report["hardware_actuation"])
        self.assertEqual(report["model_id"],"HuggingFaceTB/SmolVLM-256M-Instruct")

if __name__ == "__main__": unittest.main()
