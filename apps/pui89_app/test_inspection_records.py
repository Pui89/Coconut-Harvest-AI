"""Regression tests for local-first Coconut inspection records."""
from __future__ import annotations

import hashlib
import json
import struct
import tempfile
import unittest
import zlib
from pathlib import Path

from apps.pui89_app.inspection_records import (
    InspectionError,
    InspectionRecordStore,
    MATURITY_LABELS,
)


def _png_bytes(width: int = 2, height: int = 2) -> bytes:
    def chunk(kind: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    raw = b"".join(b"\x00" + b"\x20\x80\x40\xff" * width for _ in range(height))
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">2I5B", width, height, 8, 6, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw))
        + chunk(b"IEND", b"")
    )


class InspectionRecordStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = InspectionRecordStore(Path(self.temp.name) / "workspace")
        self.record = self.store.create_inspection(
            operator_alias="operator-01", site_code="farm-A", notes="Morning inspection"
        )

    def tearDown(self):
        self.temp.cleanup()

    def _add_image(self):
        payload = _png_bytes()
        image = self.store.import_image(
            self.record["inspection_id"],
            payload,
            filename="orchard.png",
            source_type="user_provided",
            source_reference="field notebook entry 01",
        )
        return payload, image

    def test_create_and_reopen_inspection(self):
        reopened = self.store.get_inspection(self.record["inspection_id"])
        self.assertEqual(reopened["inspection_id"], self.record["inspection_id"])
        self.assertEqual(reopened["metadata"]["site_code"], "farm-A")
        self.assertEqual(self.store.list_inspections()[0]["inspection_id"], self.record["inspection_id"])

    def test_import_preserves_bytes_and_records_sha256(self):
        payload, image = self._add_image()
        stored = self.store._record_path(self.record["inspection_id"]).parent / image["stored_path"]
        self.assertEqual(stored.read_bytes(), payload)
        self.assertEqual(image["sha256"], hashlib.sha256(payload).hexdigest())
        self.assertEqual(image["integrity"], "sha256_recorded_and_image_decoded")

    def test_read_image_rechecks_stored_hash(self):
        payload, image = self._add_image()
        self.assertEqual(self.store.read_image(self.record["inspection_id"], image["sha256"]), payload)
        stored = self.store._record_path(self.record["inspection_id"]).parent / image["stored_path"]
        stored.write_bytes(b"tampered")
        with self.assertRaisesRegex(InspectionError, "STORED_IMAGE_HASH_MISMATCH"):
            self.store.read_image(self.record["inspection_id"], image["sha256"])

    def test_duplicate_image_is_not_duplicated(self):
        _, first = self._add_image()
        second = self.store.import_image(self.record["inspection_id"], _png_bytes(), filename="copy.png")
        self.assertEqual(first["sha256"], second["sha256"])
        self.assertEqual(len(self.store.get_inspection(self.record["inspection_id"])["images"]), 1)

    def test_rejects_empty_unsupported_and_corrupt_images(self):
        with self.assertRaisesRegex(InspectionError, "IMAGE_EMPTY_OR_MISSING"):
            self.store.import_image(self.record["inspection_id"], b"", filename="empty.png")
        with self.assertRaisesRegex(InspectionError, "IMAGE_UNREADABLE_OR_CORRUPT"):
            self.store.import_image(self.record["inspection_id"], b"not-an-image", filename="bad.bin")
        with self.assertRaisesRegex(InspectionError, "IMAGE_UNREADABLE_OR_CORRUPT"):
            self.store.import_image(self.record["inspection_id"], b"\x89PNG\r\n\x1a\ntruncated", filename="bad.png")

    def test_all_four_maturity_labels_and_unknown_review_are_supported(self):
        self.assertEqual(MATURITY_LABELS, {
            "young_green", "mature_green", "yellow",
            "brown_aging", "unknown", "review",
        })

    def test_annotation_revision_history_and_report(self):
        _, image = self._add_image()
        inspection_id = self.record["inspection_id"]
        first = self.store.add_annotation(
            inspection_id, candidate_id="fruit-01", image_sha256=image["sha256"],
            maturity_label="yellow", reviewer_alias="reviewer-A",
            reason="Partly obscured", bbox_xywh_normalized=[0.1, 0.2, 0.3, 0.4],
        )
        second = self.store.add_annotation(
            inspection_id, candidate_id="fruit-01", image_sha256=image["sha256"],
            maturity_label="review", reviewer_alias="reviewer-B",
            reason="Needs second look",
        )
        record = self.store.get_inspection(inspection_id)
        revisions = record["candidates"][0]["revisions"]
        self.assertEqual(len(revisions), 2)
        self.assertEqual(revisions[0]["maturity_label"], "yellow")
        self.assertEqual(revisions[0]["revision_id"], first["revision_id"])
        self.assertEqual(second["supersedes"], first["revision_id"])
        report = self.store.export_report(inspection_id)
        self.assertEqual(report["current_assessments"][0]["current"]["maturity_label"], "review")
        self.assertEqual(report["evidence_summary"]["assessment_revision_count"], 2)
        report_path = self.store.write_report(inspection_id)
        self.assertTrue(report_path.is_file())
        self.assertEqual(json.loads(report_path.read_text())["inspection"]["inspection_id"], inspection_id)

    def test_invalid_label_confidence_and_bbox_are_rejected(self):
        _, image = self._add_image()
        base = {
            "inspection_id": self.record["inspection_id"],
            "candidate_id": "fruit-02",
            "image_sha256": image["sha256"],
            "reviewer_alias": "reviewer-A",
        }
        with self.assertRaisesRegex(InspectionError, "MATURITY_LABEL_INVALID"):
            self.store.add_annotation(**base, maturity_label="ripe", )
        with self.assertRaisesRegex(InspectionError, "MATURITY_LABEL_INVALID"):
            self.store.add_annotation(**base, maturity_label="developing_green", )
        with self.assertRaisesRegex(InspectionError, "CONFIDENCE_OUT_OF_RANGE"):
            self.store.add_annotation(**base, maturity_label="unknown", confidence=1.2, confidence_origin="human")
        with self.assertRaisesRegex(InspectionError, "BBOX_OUT_OF_BOUNDS"):
            self.store.add_annotation(**base, maturity_label="mature_green", bbox_xywh_normalized=[0.8, 0.8, 0.4, 0.4])

    def test_annotation_requires_image_in_same_inspection(self):
        with self.assertRaisesRegex(InspectionError, "ANNOTATION_IMAGE_NOT_IN_INSPECTION"):
            self.store.add_annotation(
                self.record["inspection_id"], candidate_id="fruit-03",
                image_sha256="a" * 64, maturity_label="unknown", reviewer_alias="reviewer-A",
            )

    def test_invalid_inspection_identifier_is_rejected(self):
        with self.assertRaisesRegex(InspectionError, "INSPECTION_ID_INVALID"):
            self.store.get_inspection("../outside")


if __name__ == "__main__":
    unittest.main()
