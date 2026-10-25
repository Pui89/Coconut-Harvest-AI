import unittest
from scripts.free_first_project_tools import audit_records, validate_annotation, finite_unit_interval, binary_classification_metrics

class FreeFirstTests(unittest.TestCase):
    def test_annotation_accepts_normalized_box_and_provenance(self):
        row={"image_path":"img.jpg","source_id":"source-1","licence":"CC0",
             "maturity_class":"mature_green","bbox_xyxy":[0.1,0.2,0.7,0.9],"sha256":"a"*64}
        self.assertEqual(validate_annotation(row), [])
        self.assertTrue(audit_records([row])["training_approved"])

    def test_bad_box_and_missing_provenance_block_approval(self):
        row={"image_path":"img.jpg","bbox_xyxy":[0.8,0.2,0.1,0.9]}
        result=audit_records([row])
        self.assertFalse(result["training_approved"])
        self.assertGreater(result["error_count"],0)

    def test_duplicate_hash_blocks_approval(self):
        base={"image_path":"img.jpg","source_id":"src","licence":"CC0","maturity_class":"young_green","bbox_xyxy":[0,0,1,1],"sha256":"b"*64}
        result=audit_records([base,dict(base,image_path="copy.jpg")])
        self.assertFalse(result["training_approved"])
        self.assertTrue(any("duplicate" in e["issue"] for e in result["errors"]))

    def test_finite_confidence_helper(self):
        self.assertTrue(finite_unit_interval(0.0))
        self.assertFalse(finite_unit_interval(float("nan")))
        self.assertFalse(finite_unit_interval(True))


    def test_binary_metrics_match_hand_calculation(self):
        result = binary_classification_metrics([1, 1, 0, 0], [1, 0, 1, 0])
        self.assertEqual((result["tp"], result["tn"], result["fp"], result["fn"]), (1, 1, 1, 1))
        self.assertEqual(result["accuracy"], 0.5)
        self.assertEqual(result["precision"], 0.5)
        self.assertEqual(result["recall"], 0.5)
        self.assertEqual(result["f1"], 0.5)

    def test_binary_metrics_reject_empty_or_mismatched_inputs(self):
        with self.assertRaises(ValueError):
            binary_classification_metrics([], [])
        with self.assertRaises(ValueError):
            binary_classification_metrics([1], [1, 0])

    def test_binary_metrics_handle_zero_division(self):
        result = binary_classification_metrics([0, 0], [0, 0])
        self.assertEqual(result["precision"], 0.0)
        self.assertEqual(result["recall"], 0.0)
        self.assertEqual(result["f1"], 0.0)

if __name__ == "__main__": unittest.main()
