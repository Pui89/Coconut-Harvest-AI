import csv
import tempfile
import unittest
from pathlib import Path
from tools.validate_coconut_dataset import validate_dataset

class CoconutDatasetPreflightTests(unittest.TestCase):
    def write_csv(self, path, fields, rows):
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def test_valid_preflight_never_claims_accuracy(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp); manifest=root/"manifest.csv"; annotations=root/"annotations.csv"
            self.write_csv(manifest, ["image_id","path","source","license","split","tree_id"], [
                {"image_id":"img-1","path":"one.jpg","source":"session-1","license":"CC-BY-4.0","split":"train","tree_id":"tree-a"},
                {"image_id":"img-2","path":"two.jpg","source":"session-2","license":"CC-BY-4.0","split":"test","tree_id":"tree-b"}])
            self.write_csv(annotations, ["image_id","xmin","ymin","xmax","ymax","class"], [
                {"image_id":"img-1","xmin":"0","ymin":"0","xmax":"10","ymax":"10","class":"mature-green"}])
            result=validate_dataset(manifest,annotations)
            self.assertEqual(result["status"],"PASS_PREFLIGHT")
            self.assertIsNone(result["accuracy_metrics"])
            self.assertIn("no detector was run",result["note"])

    def test_duplicate_image_id_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            manifest=Path(temp)/"manifest.csv"
            self.write_csv(manifest,["image_id","path","source","license","split"],[
                {"image_id":"x","path":"x.jpg","source":"s","license":"L","split":"train"},
                {"image_id":"x","path":"y.jpg","source":"s2","license":"L","split":"test"}])
            self.assertEqual(validate_dataset(manifest)["status"],"FAIL")

    def test_tree_cross_split_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            manifest=Path(temp)/"manifest.csv"
            self.write_csv(manifest,["image_id","path","source","license","split","tree_id"],[
                {"image_id":"x","path":"x.jpg","source":"s1","license":"L","split":"train","tree_id":"same"},
                {"image_id":"y","path":"y.jpg","source":"s2","license":"L","split":"test","tree_id":"same"}])
            result=validate_dataset(manifest)
            self.assertEqual(result["status"],"FAIL")
            self.assertTrue(any("split leakage" in e for e in result["errors"]))

    def test_invalid_box_fails(self):
        with tempfile.TemporaryDirectory() as temp:
            manifest=Path(temp)/"manifest.csv"; annotations=Path(temp)/"annotations.csv"
            self.write_csv(manifest,["image_id","path","source","license","split"],[
                {"image_id":"x","path":"x.jpg","source":"s","license":"L","split":"test"}])
            self.write_csv(annotations,["image_id","xmin","ymin","xmax","ymax","class"],[
                {"image_id":"x","xmin":"10","ymin":"0","xmax":"5","ymax":"10","class":"c"}])
            self.assertEqual(validate_dataset(manifest,annotations)["status"],"FAIL")

if __name__ == "__main__":
    unittest.main()
