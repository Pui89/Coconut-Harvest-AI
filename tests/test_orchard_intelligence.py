import unittest

from coconut_harvest_robot.orchard_intelligence import (
    build_orchard_report, height_band, validate_fruit_observation,
)


class HeightBandTests(unittest.TestCase):
    def test_band_boundaries_are_explicit(self):
        expected = {
            0: "H1_0_5m", 5: "H1_0_5m", 5.01: "H2_over5_10m",
            10: "H2_over5_10m", 10.01: "H3_over10_15m",
            15: "H3_over10_15m", 15.01: "H4_over15_20m",
            20: "H4_over15_20m", 20.01: "H5_over20_25m",
            25: "H5_over20_25m", 25.01: "H6_over25_30m",
            30: "H6_over25_30m", 30.01: "OUT_OF_RANGE",
        }
        for value, band in expected.items():
            result = height_band(
                value, status="verified", method="laser_rangefinder",
                evidence_ref="field-record-001",
            )
            self.assertEqual(result["height_band"], band)

    def test_unverified_height_never_gets_a_band(self):
        result = height_band(
            18, status="unverified", method="laser_rangefinder",
            evidence_ref="field-record-001",
        )
        self.assertIsNone(result["height_m"])
        self.assertEqual(result["height_band"], "UNKNOWN")

    def test_verified_height_requires_method_and_evidence(self):
        result = height_band(
            8, status="verified", method="", evidence_ref=None
        )
        self.assertEqual(result["height_status"], "review_required")
        self.assertEqual(result["height_band"], "UNKNOWN")

    def test_nan_and_negative_height_rejected(self):
        for value in (float("nan"), float("inf"), -1, True, "8"):
            result = height_band(
                value, status="verified", method="field_tape",
                evidence_ref="record",
            )
            self.assertEqual(result["height_status"], "invalid_measurement")


class FruitEvidenceTests(unittest.TestCase):
    def valid(self, **updates):
        row = {
            "fruit_id": "f-001", "image_id": "img-001",
            "maturity_class": "mature_green", "source_kind": "human_annotation",
            "class_confidence": 1.0, "bbox_xyxy_normalized": [0.1, 0.2, 0.8, 0.9],
            "review_status": "reviewed",
        }
        row.update(updates)
        return row

    def test_reviewed_annotation_is_not_ground_truth_or_authorization(self):
        result = validate_fruit_observation(self.valid())
        self.assertEqual(result["disposition"], "annotation_reviewed_not_ground_truth")
        self.assertFalse(result["harvest_authorized"])

    def test_model_prediction_requires_human_review(self):
        result = validate_fruit_observation(
            self.valid(source_kind="model_prediction", review_status="pending")
        )
        self.assertEqual(result["disposition"], "human_review_required")
        self.assertFalse(result["harvest_authorized"])

    def test_synthetic_record_stays_synthetic(self):
        result = validate_fruit_observation(
            self.valid(source_kind="synthetic_test", review_status="reviewed")
        )
        self.assertEqual(result["disposition"], "synthetic_only")

    def test_uncertain_stage_is_preserved(self):
        result = validate_fruit_observation(self.valid(maturity_class="uncertain"))
        self.assertEqual(result["maturity_class"], "uncertain")

    def test_invalid_box_and_class_are_rejected(self):
        result = validate_fruit_observation(
            self.valid(maturity_class="ripe", bbox_xyxy_normalized=[0, 0, 2, 1])
        )
        self.assertIn("unsupported_or_missing_maturity_class", result["errors"])
        self.assertIn("invalid_normalized_bbox", result["errors"])
        self.assertFalse(result["harvest_authorized"])

    def test_report_keeps_unknown_tree_height_unknown(self):
        report = build_orchard_report(
            tree_record={"height_m": None, "height_status": "unverified"},
            fruit_records=[self.valid(), self.valid(
                fruit_id="f-002", maturity_class="young_green"
            )],
        )
        self.assertEqual(report["tree"]["height_band"], "UNKNOWN")
        self.assertEqual(report["maturity_counts"]["mature_green"], 1)
        self.assertEqual(report["maturity_counts"]["young_green"], 1)
        self.assertFalse(report["decision_boundary"]["image_classification_performed"])
        self.assertFalse(report["decision_boundary"]["automatic_harvest_authorized"])


if __name__ == "__main__":
    unittest.main()
