import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from pui89_coconut_model_adapter import adapt_coconut_mock

def request():
    return {"request_id":"coc-1","timestamp":"2026-11-01T00:00:01Z",
      "evidence":{"source_id":"fixture-1","source_ref":"synthetic://coconut/1",
        "timestamp":"2026-11-01T00:00:00Z","evidence_kind":"synthetic","lineage":["unit-test"]},
      "mock_observation":{"candidate_maturity_label":"mature_green","visual_cues":["green husk","example fixture"]}}

class CoconutModelAdapterTests(unittest.TestCase):
    def test_valid_fixture_is_review_only(self):
        r=adapt_coconut_mock(request())
        self.assertEqual(r["project_id"],"coconut_harvest")
        self.assertEqual(r["status"],"MOCK_OBSERVATION_REVIEW_REQUIRED")
        self.assertFalse(r["adapter"]["inference_performed"])
        self.assertEqual(r["proposed_actions"],[])
        self.assertFalse(r["physical_actuation_permitted"])
    def test_unknown_maturity_rejected(self):
        q=request(); q["mock_observation"]["candidate_maturity_label"]="harvest_ready"
        with self.assertRaises(ValueError): adapt_coconut_mock(q)
    def test_missing_visual_cues_rejected(self):
        q=request(); q["mock_observation"]["visual_cues"]=[]
        with self.assertRaises(ValueError): adapt_coconut_mock(q)
    def test_non_synthetic_evidence_rejected(self):
        q=request(); q["evidence"]["evidence_kind"]="observed"
        with self.assertRaises(ValueError): adapt_coconut_mock(q)
    def test_hardware_command_rejected(self):
        q=request(); q["robot_command"]={"cut":True}
        with self.assertRaises(ValueError): adapt_coconut_mock(q)
    def test_future_evidence_rejected(self):
        q=request(); q["evidence"]["timestamp"]="2026-11-01T00:00:02Z"
        with self.assertRaises(ValueError): adapt_coconut_mock(q)
if __name__=="__main__": unittest.main()
