import tempfile, unittest
from pathlib import Path
from apps.pui89_app.inspection_workspace import (
    InspectionError, add_annotation, create_inspection, export_report,
    export_annotation_manifest, load_inspection, record_quality_review, sha256_bytes
)
IMAGE = b"synthetic-image-bytes"

def create(workspace, **kwargs):
    return create_inspection(workspace, image_bytes=IMAGE, image_extension=".jpg",
        image_format="JPEG", image_width=640, image_height=480,
        original_filename="../../private.jpg", source_description="Synthetic fixture only",
        rights_confirmed=True, site_code="TEST", operator_alias="tester", **kwargs)

class InspectionWorkspaceTests(unittest.TestCase):
    def test_create_hash_and_filename_sanitization(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=create(tmp)
            self.assertEqual(r["image"]["sha256"], sha256_bytes(IMAGE))
            self.assertEqual(r["image"]["original_filename"], "private.jpg")
            self.assertEqual(r["revision"], 1)

    def test_rights_and_source_are_required(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(InspectionError, "authorised"):
                create_inspection(tmp, image_bytes=IMAGE, image_extension=".jpg", image_format="JPEG",
                    image_width=1, image_height=1, original_filename="a.jpg",
                    source_description="test", rights_confirmed=False)
            with self.assertRaisesRegex(InspectionError, "required"):
                create_inspection(tmp, image_bytes=IMAGE, image_extension=".jpg", image_format="JPEG",
                    image_width=1, image_height=1, original_filename="a.jpg",
                    source_description="", rights_confirmed=True)

    def test_annotation_appends_a_revision(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=create(tmp)
            u=add_annotation(tmp, r["inspection_id"], candidate_id="fruit-01",
                label="mature_green", reviewer_alias="reviewer", x1=.1, y1=.2, x2=.8, y2=.9)
            self.assertEqual(u["revision"], 2)
            self.assertEqual(len(u["annotations"]), 1)
            self.assertEqual(load_inspection(tmp, r["inspection_id"]), u)
            self.assertEqual(len((Path(tmp)/"inspections"/r["inspection_id"]/"events.jsonl").read_text().splitlines()), 2)

    def test_invalid_box_and_duplicate_id_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=create(tmp)
            args=dict(candidate_id="fruit-01", label="young", reviewer_alias="r", x1=.7, y1=.2, x2=.1, y2=.9)
            with self.assertRaisesRegex(InspectionError, "bounding box"):
                add_annotation(tmp, r["inspection_id"], **args)
            args.update(x1=.1, x2=.8)
            add_annotation(tmp, r["inspection_id"], **args)
            with self.assertRaisesRegex(InspectionError, "already exists"):
                add_annotation(tmp, r["inspection_id"], **args)

    def test_unknown_is_needs_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=create(tmp)
            u=add_annotation(tmp, r["inspection_id"], candidate_id="unknown-01",
                label="unknown_needs_review", reviewer_alias="reviewer", x1=.1, y1=.1, x2=.9, y2=.9)
            self.assertEqual(u["annotations"][0]["status"], "NEEDS_REVIEW")

    def test_export_checks_image_integrity_and_no_harvest_authority(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=create(tmp); report=export_report(tmp, r["inspection_id"])
            self.assertTrue(report["integrity"]["image_sha256_verified"])
            self.assertFalse(report["decision_boundary"]["harvest_authorized"])
            self.assertFalse(report["decision_boundary"]["automatic_classification_performed"])
            p=Path(tmp)/"inspections"/r["inspection_id"]/"images"/r["image"]["stored_filename"]
            p.write_bytes(b"tampered")
            with self.assertRaisesRegex(InspectionError, "integrity"):
                export_report(tmp, r["inspection_id"])

    def test_path_traversal_id_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(InspectionError, "invalid inspection ID"):
                load_inspection(tmp, "../etc/passwd")

    def test_quality_review_is_append_only_and_validated(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=create(tmp, image_quality={"assessment_method":"fixture","flags":["LOW_RESOLUTION"]})
            u=record_quality_review(tmp, r["inspection_id"], reviewer_alias="reviewer",
                visibility="partial", occlusion="minor", notes="Leaves cover part of fruit")
            self.assertEqual(u["revision"], 2)
            self.assertEqual(u["image_quality"]["human_review"]["visibility"], "partial")
            self.assertEqual(len((Path(tmp)/"inspections"/r["inspection_id"]/"events.jsonl").read_text().splitlines()), 2)
            with self.assertRaisesRegex(InspectionError, "visibility"):
                record_quality_review(tmp, r["inspection_id"], reviewer_alias="r",
                    visibility="perfect", occlusion="none")

    def test_batch_id_and_annotation_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=create(tmp, batch_id="orchard-session-01")
            add_annotation(tmp, r["inspection_id"], candidate_id="fruit-01",
                label="developing_green", reviewer_alias="reviewer", x1=.1, y1=.2, x2=.8, y2=.9)
            manifest=export_annotation_manifest(tmp)
            self.assertEqual(manifest["annotation_count"], 1)
            self.assertEqual(manifest["records"][0]["batch_id"], "orchard-session-01")
            self.assertEqual(manifest["training_use"], "NOT_APPROVED_BY_DEFAULT")
            self.assertIn("Do not randomly split", manifest["split_policy"])

if __name__ == "__main__":
    unittest.main()
