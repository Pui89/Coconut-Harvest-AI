import unittest

from pui89_coconut_adapter import build_coconut_message, evaluate_coconut_snapshot

NOW = "2026-10-31T00:00:00+00:00"

class CoconutAdapterTests(unittest.TestCase):
    def make_record(self, **kwargs):
        values = {
            "observation_id": "coco-001",
            "source_ref": "synthetic-fixture:coco-001",
            "timestamp": NOW,
            "maturity_label": "mature_green",
            "modality": "rgb",
            "evidence_kind": "synthetic",
        }
        values.update(kwargs)
        return build_coconut_message(**values)

    def test_maps_four_class_label_to_shared_contract(self):
        record = self.make_record()
        self.assertEqual(record["message"]["claims"][0]["claim_key"], "coconut_maturity")
        self.assertEqual(record["message"]["claims"][0]["value"], "mature_green")
        self.assertEqual(record["evidence"]["evidence_kind"], "synthetic")

    def test_rejects_unknown_maturity_class(self):
        with self.assertRaises(ValueError):
            self.make_record(maturity_label="ripe")

    def test_rejects_timezone_missing(self):
        with self.assertRaises(ValueError):
            self.make_record(timestamp="2026-10-31T00:00:00")

    def test_routes_through_shared_orchestrator(self):
        result = evaluate_coconut_snapshot([self.make_record()], now=NOW)
        self.assertEqual(result["action"], "CONTINUE")
        self.assertTrue(result["simulation_only"])
        self.assertFalse(result["physical_actuation_permitted"])

    def test_stale_observation_requests_evidence(self):
        record = self.make_record(timestamp="2026-10-30T00:00:00+00:00")
        result = evaluate_coconut_snapshot([record], now=NOW)
        self.assertEqual(result["action"], "REQUEST_EVIDENCE")

    def test_disagreeing_coconut_labels_request_verification(self):
        first = self.make_record(observation_id="coco-a")
        second = self.make_record(observation_id="coco-b", maturity_label="brown_aging")
        result = evaluate_coconut_snapshot([first, second], now=NOW)
        self.assertEqual(result["action"], "REQUEST_SPECIALIST_VERIFICATION")
        self.assertIsNone(result["disagreements"][0]["resolution"])

if __name__ == "__main__":
    unittest.main()
