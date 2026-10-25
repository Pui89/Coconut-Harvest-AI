"""Offline tests for the opt-in source SHA-256 recorder."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from tools.record_coconut_source_hash import SOURCE_REFERENCE, record_source_hash


def write_fixture(tmp_path: Path, *, creator: str = "Sarmi~Kili"):
    image_name = SOURCE_REFERENCE["filename"]
    image = tmp_path / image_name
    image_bytes = b"synthetic source fingerprint test bytes"
    image.write_bytes(image_bytes)

    reference = dict(SOURCE_REFERENCE)
    reference["published_size_bytes"] = len(image_bytes)
    reference["published_sha1"] = hashlib.sha1(image_bytes).hexdigest()
    reference["creator_credit"] = "Sarmi~Kili"
    reference["licence_as_displayed"] = "CC BY-SA 4.0"

    payload = {
        "format": "pui89-coconut-annotations-v1",
        "status": "AI-assisted draft only; not human-QA-approved",
        "source": {
            "candidate_id": reference["candidate_id"],
            "filename": image_name,
            "file_page": reference["source_page_url"],
            "creator": creator,
            "license": reference["licence_as_displayed"],
            "source_image_sha256": "unverified placeholder",
        },
        "images": [{
            "filename": image_name,
            "width": reference["published_width"],
            "height": reference["published_height"],
            "boxes": [{"x": 0.1, "y": 0.2, "w": 0.3, "h": 0.4}],
        }],
        "human_qa_acknowledged": False,
        "training_approved": False,
    }
    annotation_path = tmp_path / "draft.json"
    annotation_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    rights_path = tmp_path / "rights.csv"
    fields = [
        "candidate_id", "filename", "source_page_url", "creator_credit",
        "licence_as_displayed",
    ]
    with rights_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow({
            "candidate_id": reference["candidate_id"],
            "filename": image_name,
            "source_page_url": reference["source_page_url"],
            "creator_credit": "Sarmi~Kili",
            "licence_as_displayed": "CC BY-SA 4.0",
        })
    return annotation_path, image, rights_path, reference, payload


def test_dry_run_reports_sha256_without_editing_annotation(tmp_path):
    annotation_path, image, rights_path, reference, original = write_fixture(tmp_path)
    before = annotation_path.read_bytes()

    report = record_source_hash(
        annotation_path, image, rights_path, source_reference=reference
    )

    assert report["source_identity_passed"] is True
    assert len(report["actual_sha256"]) == 64
    assert report["source_sha256_written"] is False
    assert annotation_path.read_bytes() == before
    assert json.loads(annotation_path.read_text()) == original


def test_explicit_write_changes_only_hash_and_never_approvals(tmp_path):
    annotation_path, image, rights_path, reference, original = write_fixture(tmp_path)
    original_boxes = original["images"][0]["boxes"]

    report = record_source_hash(
        annotation_path,
        image,
        rights_path,
        write_source_sha256=True,
        source_reference=reference,
    )

    updated = json.loads(annotation_path.read_text(encoding="utf-8"))
    assert report["source_identity_passed"] is True
    assert report["source_sha256_written"] is True
    assert updated["source"]["source_image_sha256"] == report["actual_sha256"]
    assert updated["images"][0]["boxes"] == original_boxes
    assert updated["human_qa_acknowledged"] is False
    assert updated["training_approved"] is False
    assert report["approval_flags_changed"] is False
    assert report["annotation_boxes_changed"] is False


def test_wrong_source_fingerprint_fails_closed_and_does_not_write(tmp_path):
    annotation_path, image, rights_path, reference, original = write_fixture(tmp_path)
    bad_reference = dict(reference)
    bad_reference["published_sha1"] = "0" * 40

    report = record_source_hash(
        annotation_path,
        image,
        rights_path,
        write_source_sha256=True,
        source_reference=bad_reference,
    )

    assert report["source_identity_passed"] is False
    assert report["source_checks"]["local_sha1_matches_published_source"] is False
    assert report["source_sha256_written"] is False
    assert json.loads(annotation_path.read_text(encoding="utf-8")) == original


def test_rights_metadata_mismatch_fails_closed(tmp_path):
    annotation_path, image, rights_path, reference, original = write_fixture(
        tmp_path, creator="Different Creator"
    )

    report = record_source_hash(
        annotation_path,
        image,
        rights_path,
        write_source_sha256=True,
        source_reference=reference,
    )

    assert report["source_identity_passed"] is False
    assert report["source_checks"]["creator_matches_rights_ledger"] is False
    assert report["source_sha256_written"] is False
    assert json.loads(annotation_path.read_text(encoding="utf-8")) == original


def test_filename_mismatch_fails_closed(tmp_path):
    annotation_path, image, rights_path, reference, original = write_fixture(tmp_path)
    wrong_name = tmp_path / "different-name.jpg"
    wrong_name.write_bytes(image.read_bytes())

    report = record_source_hash(
        annotation_path,
        wrong_name,
        rights_path,
        write_source_sha256=True,
        source_reference=reference,
    )

    assert report["source_identity_passed"] is False
    assert report["source_checks"]["local_basename_matches_reference"] is False
    assert report["source_sha256_written"] is False
    assert json.loads(annotation_path.read_text(encoding="utf-8")) == original
