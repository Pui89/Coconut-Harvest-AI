import json
import tempfile
import unittest
from pathlib import Path

from pui89_models.coconut_maturity import (
    CLASSES, FEATURE_COUNT, load_model, predict_features, save_model, train,
)


def prototype(label_index):
    values = [0.0] * FEATURE_COUNT
    values[label_index * 8] = 1.0
    values[24 + label_index % 3] = 0.8
    values[27 + label_index % 3] = 0.1
    return values


class CoconutMaturityModelTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            (prototype(i), label)
            for i, label in enumerate(CLASSES)
            for _ in range(4)
        ]

    def test_training_requires_all_four_classes(self):
        with self.assertRaisesRegex(ValueError, "missing classes"):
            train([(prototype(0), "young")])

    def test_training_rejects_unknown_label(self):
        with self.assertRaisesRegex(ValueError, "unsupported labels"):
            train([(prototype(0), "ripe")])

    def test_training_is_deterministic_and_returns_expected_contract(self):
        first = train(self.rows, epochs=120)
        second = train(self.rows, epochs=120)
        self.assertEqual(first, second)
        self.assertEqual(first["classes"], list(CLASSES))
        self.assertEqual(first["training"]["sample_count"], 16)
        self.assertFalse(first["training"]["confidence_calibrated"])

    def test_prediction_never_authorizes_harvest(self):
        model = train(self.rows, epochs=160)
        result = predict_features(model, prototype(0), min_confidence=0.0, min_margin=0.0)
        self.assertFalse(result["harvest_authorized"])
        self.assertTrue(result["human_review_required"])

    def test_low_confidence_abstains(self):
        model = train(self.rows, epochs=80)
        result = predict_features(model, [0.0] * FEATURE_COUNT, min_confidence=1.0)
        self.assertEqual(result["status"], "UNCERTAIN_NEEDS_REVIEW")
        self.assertEqual(result["visual_class"], "uncertain")

    def test_save_and_load_round_trip(self):
        model = train(self.rows, epochs=80)
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "model.json"
            save_model(model, path)
            self.assertEqual(load_model(path), model)
            self.assertEqual(json.loads(path.read_text())["version"], "0.1.0")

    def test_invalid_feature_vector_is_rejected(self):
        model = train(self.rows, epochs=80)
        with self.assertRaisesRegex(ValueError, "finite features"):
            predict_features(model, [float("nan")] * FEATURE_COUNT)


if __name__ == "__main__":
    unittest.main()
