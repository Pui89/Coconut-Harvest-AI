"""Integrity and safety regression tests for the Coconut Shared AI Core adapter.

These tests exercise caller-supplied synthetic records only. They do not run a
vision model, access a dataset, or issue commands to physical equipment.
"""
from __future__ import annotations

import unittest

from tools.pui89_coconut_adapter import (
    build_coconut_message,
    evaluate_coconut_snapshot,
)

NOW = "2026-11-08T00:00:00+00:00"


class CoconutAdapterIntegrityTests(unittest.TestCase):
    def make_record(self, **overrides):
        values = {
            "observation_id": "coco-integrity-001",
            "source_ref": "synthetic-fixture:coco-integrity-001",
            "timestamp": NOW,
            "maturity_label": "mature_green",
            "modality": "rgb",
            "evidence_kind": "synthetic",
            "confidence": None,
        }
        values.update(overrides)
        return build_coconut_message(**values)

    def test_unknown_confidence_is_explicitly_allowed_not_invented(self):
        record = self.make_record()
        self.assertIsNone(record["message"]["confidence"])
        self.assertIn("caller-supplied label", " ".join(record["message"]["uncertainty"]))
        self.assertEqual(record["message"]["confidence_interpretation"], "uncalibrated")

    def test_boolean_confidence_is_rejected(self):
        for value in (True, False):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.make_record(confidence=value)

    def test_non_finite_and_out_of_range_confidence_is_rejected(self):
        for value in (float("nan"), float("inf"), float("-inf"), -0.01, 1.01):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.make_record(confidence=value)

    def test_empty_source_reference_is_rejected(self):
        for value in ("", "  ", None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.make_record(source_ref=value)

    def test_empty_modality_is_rejected(self):
        with self.assertRaises(ValueError):
            self.make_record(modality=" ")

    def test_unknown_evidence_kind_is_rejected(self):
        with self.assertRaises(ValueError):
            self.make_record(evidence_kind="verified-by-model")

    def test_timezone_is_required_for_observation_timestamp(self):
        with self.assertRaises(ValueError):
            self.make_record(timestamp="2026-11-08T00:00:00")

    def test_valid_record_keeps_claim_linked_to_same_evidence_id(self):
        record = self.make_record()
        evidence_id = record["evidence"]["source_id"]
        self.assertEqual(record["message"]["source_ids"], [evidence_id])
        self.assertEqual(record["message"]["claims"][0]["evidence_ids"], [evidence_id])
        self.assertEqual(record["evidence"]["lineage"], [evidence_id])

    def test_adapter_snapshot_never_authorizes_physical_actuation(self):
        result = evaluate_coconut_snapshot([self.make_record()], now=NOW)
        self.assertTrue(result["simulation_only"])
        self.assertFalse(result["physical_actuation_permitted"])

    def test_mutated_evidence_fails_closed(self):
        record = self.make_record()
        record["evidence"]["source_ref"] = " "
        result = evaluate_coconut_snapshot([record], now=NOW)
        self.assertEqual(result["action"], "SAFE_HOLD")
        self.assertFalse(result["physical_actuation_permitted"])

    def test_mutated_claim_reference_fails_closed(self):
        record = self.make_record()
        record["message"]["claims"][0]["evidence_ids"] = ["unknown-evidence"]
        result = evaluate_coconut_snapshot([record], now=NOW)
        self.assertEqual(result["action"], "SAFE_HOLD")
        self.assertFalse(result["physical_actuation_permitted"])

    def test_disagreement_is_not_automatically_resolved(self):
        first = self.make_record(observation_id="coco-green")
        second = self.make_record(
            observation_id="coco-brown",
            maturity_label="brown_aging",
            source_ref="synthetic-fixture:coco-brown",
        )
        result = evaluate_coconut_snapshot([first, second], now=NOW)
        self.assertEqual(result["action"], "REQUEST_SPECIALIST_VERIFICATION")
        self.assertIsNone(result["disagreements"][0]["resolution"])
        self.assertFalse(result["physical_actuation_permitted"])


if __name__ == "__main__":
    unittest.main()
