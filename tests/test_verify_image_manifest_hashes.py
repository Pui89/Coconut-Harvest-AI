import csv
import hashlib
import tempfile
import unittest
from pathlib import Path
from tools.verify_image_manifest_hashes import verify

class VerifyImageManifestHashesTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.images = self.root / "images"
        self.images.mkdir()
        self.manifest = self.root / "manifest.csv"
        self.a, self.b = b"fake-image-bytes-a", b"fake-image-bytes-b"
        (self.images / "a.jpg").write_bytes(self.a)
        (self.images / "b.jpg").write_bytes(self.b)
    def tearDown(self):
        self.temp.cleanup()
    def row(self, image_id, filename, split, data):
        return {"image_id": image_id, "filename": filename, "split": split,
                "group_id": image_id, "sha256": hashlib.sha256(data).hexdigest()}
    def write_manifest(self, rows):
        with self.manifest.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["image_id","filename","split","group_id","sha256"])
            writer.writeheader()
            writer.writerows(rows)
    def test_valid_hashes_pass(self):
        self.write_manifest([self.row("a","a.jpg","train",self.a),self.row("b","b.jpg","test",self.b)])
        report = verify(self.manifest,self.images)
        self.assertTrue(report["passed"])
        self.assertEqual(report["verified_file_count"],2)
    def test_hash_mismatch_fails(self):
        row = self.row("a","a.jpg","train",self.a); row["sha256"] = "0"*64
        self.write_manifest([row])
        report = verify(self.manifest,self.images)
        self.assertFalse(report["passed"])
        self.assertEqual(report["manifest_hash_mismatches"],1)
    def test_missing_file_fails(self):
        self.write_manifest([self.row("a","missing.jpg","train",self.a)])
        report = verify(self.manifest,self.images)
        self.assertFalse(report["passed"])
        self.assertIn("image_file_missing",report["files"][0]["issues"])
    def test_exact_duplicate_across_splits_fails(self):
        same = b"same bytes"
        (self.images/"a.jpg").write_bytes(same); (self.images/"b.jpg").write_bytes(same)
        self.write_manifest([self.row("a","a.jpg","train",same),self.row("b","b.jpg","test",same)])
        report = verify(self.manifest,self.images)
        self.assertFalse(report["passed"])
        self.assertEqual(len(report["exact_duplicate_cross_split_findings"]),1)
    def test_path_escape_is_rejected(self):
        (self.root/"outside.jpg").write_bytes(self.a)
        self.write_manifest([self.row("a","../outside.jpg","train",self.a)])
        report = verify(self.manifest,self.images)
        self.assertFalse(report["passed"])
        self.assertIn("filename_escapes_images_directory",report["files"][0]["issues"])

if __name__ == "__main__":
    unittest.main()
