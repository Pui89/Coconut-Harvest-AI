import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class SharedWorkflowContractTests(unittest.TestCase):
    def test_schema_covers_all_four_projects(self):
        schema = json.loads((ROOT / "schemas/pui89-intelligence-report.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(set(schema["properties"]["project"]["enum"]), {"coconut-harvest-ai", "flood-rescue-ai", "multimodal-narcotics-screening-ai", "homeguard-ai-nomad"})

    def test_report_requires_evidence_and_safety(self):
        schema = json.loads((ROOT / "schemas/pui89-intelligence-report.schema.json").read_text(encoding="utf-8"))
        self.assertTrue({"world_state", "evidence", "uncertainty", "risks", "recommendations", "safety_gate", "verification"} <= set(schema["required"]))

    def test_stage_labels_are_explicit(self):
        schema = json.loads((ROOT / "schemas/pui89-intelligence-report.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["stage"]["enum"], ["proposed", "implemented", "tested", "simulated", "validated"])

    def test_workflow_includes_fail_safe_and_human_review(self):
        doc = (ROOT / "docs/PUI89_SHARED_INTELLIGENCE_WORKFLOW.md").read_text(encoding="utf-8").lower()
        self.assertIn("human review", doc)
        self.assertIn("stop", doc)
        self.assertIn("simulation", doc)

if __name__ == "__main__":
    unittest.main()
