import unittest

from tools.evaluate_coconut_detections import Box, box_iou, evaluate


class CoconutDetectionEvaluationTests(unittest.TestCase):
    def test_iou_identical_boxes_is_one(self):
        box = Box("img1", 0, 0, 10, 10, "coconut")
        self.assertEqual(box_iou(box, box), 1.0)

    def test_counts_true_positive_false_positive_and_false_negative(self):
        truth = [Box("img1", 0, 0, 10, 10, "coconut")]
        predictions = [
            Box("img1", 0, 0, 10, 10, "coconut", 0.9),
            Box("img1", 20, 20, 30, 30, "coconut", 0.8),
        ]
        result = evaluate(truth, predictions)
        self.assertEqual(result["true_positives"], 1)
        self.assertEqual(result["false_positives"], 1)
        self.assertEqual(result["false_negatives"], 0)
        self.assertEqual(result["precision"], 0.5)
        self.assertEqual(result["recall"], 1.0)

    def test_duplicate_predictions_cannot_match_one_truth_twice(self):
        truth = [Box("img1", 0, 0, 10, 10, "coconut")]
        predictions = [
            Box("img1", 0, 0, 10, 10, "coconut", 0.9),
            Box("img1", 1, 1, 9, 9, "coconut", 0.8),
        ]
        result = evaluate(truth, predictions)
        self.assertEqual(result["true_positives"], 1)
        self.assertEqual(result["false_positives"], 1)

    def test_score_threshold_filters_predictions(self):
        truth = [Box("img1", 0, 0, 10, 10, "coconut")]
        predictions = [Box("img1", 0, 0, 10, 10, "coconut", 0.2)]
        result = evaluate(truth, predictions, score_threshold=0.5)
        self.assertEqual(result["prediction_count_after_score_threshold"], 0)
        self.assertEqual(result["false_negatives"], 1)

    def test_rejects_invalid_iou_threshold(self):
        with self.assertRaises(ValueError):
            evaluate([], [], iou_threshold=0)


if __name__ == "__main__":
    unittest.main()
