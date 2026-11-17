import json
import unittest
from pathlib import Path


class ProductFailureScenarioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / "quality" / "failure-scenarios.json"
        cls.data = json.loads(path.read_text(encoding="utf-8"))
        cls.scenarios = cls.data["scenarios"]

    def test_scenario_ids_are_unique(self):
        ids = [item["id"] for item in self.scenarios]
        self.assertTrue(ids)
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_scenario_requires_human_review(self):
        self.assertTrue(all(item.get("human_review") is True for item in self.scenarios))

    def test_every_scenario_has_a_fail_safe_expected_response(self):
        self.assertTrue(all(item.get("input") and item.get("expected") for item in self.scenarios))
        self.assertGreaterEqual(len(self.scenarios), 10)


if __name__ == "__main__":
    unittest.main()
