"""Tests for conservative coconut dataset structural audit."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "audit_coconut_dataset.py"
SPEC = importlib.util.spec_from_file_location("audit_coconut_dataset", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class DatasetAuditTests(unittest.TestCase):
    def test_manifest_without_candidates_fails_closed(self):
        report = MODULE.audit({}, Path("data/candidate_images"))
        self.assertFalse(report["passed_structural_checks"])
        self.assertEqual(report["training_approved_count"], 0)

    def test_unapproved_metadata_candidate_passes_with_warning(self):
        manifest = {"candidates": [{
            "candidate_id": "c1", "downloaded": False,
            "training_approved": False, "file_page": "https://example.test/file",
            "license_short_name": "CC BY-SA 4.0",
        }]}
        report = MODULE.audit(manifest, Path("data/candidate_images"))
        self.assertTrue(report["passed_structural_checks"])
        self.assertEqual(report["training_approved_count"], 0)
        self.assertTrue(report["warnings"])

    def test_detects_download_hash_mismatch(self):
        with TemporaryDirectory() as temp:
            root = Path(temp)
            image_dir = root / "candidate_images"
            image_dir.mkdir()
            image = image_dir / "c1.jpg"
            image.write_bytes(b"test image bytes")
            manifest = {"candidates": [{
                "candidate_id": "c1", "downloaded": True,
                "local_file": "data/candidate_images/c1.jpg",
                "sha256": "not-the-real-hash", "training_approved": False,
                "file_page": "https://example.test/file", "license_short_name": "CC BY-SA 4.0",
            }]}
            # Use a manifest path relative to the test working directory via a safe absolute path
            manifest["candidates"][0]["local_file"] = str(image)
            report = MODULE.audit(manifest, image_dir)
            self.assertFalse(report["passed_structural_checks"])
            self.assertTrue(any("SHA-256 mismatch" in err for err in report["errors"]))

    def test_rejects_self_approved_manifest(self):
        manifest = {"candidates": [{
            "candidate_id": "c1", "downloaded": False, "training_approved": True,
        }]}
        report = MODULE.audit(manifest, Path("data/candidate_images"))
        self.assertFalse(report["passed_structural_checks"])
        self.assertTrue(any("must not self-approve" in err for err in report["errors"]))


if __name__ == "__main__":
    unittest.main()
