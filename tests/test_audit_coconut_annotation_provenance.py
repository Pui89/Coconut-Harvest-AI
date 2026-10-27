"""Offline tests for image-byte provenance and fail-closed approvals."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import pytest

from tools.audit_coconut_annotation_provenance import audit, sha256_file


def write_annotation(path: Path, image_name: str, digest: str, **overrides):
    payload = {
        "format": "pui89-coconut-annotations-v1",
        "status": "draft only; not human-QA-approved",
        "source": {
            "candidate_id": "0032",
            "filename": image_name,
            "file_page": "https://commons.wikimedia.org/wiki/File:Example.jpg",
            "creator": "Example Creator",
            "license": "CC BY-SA 4.0",
            "source_image_sha256": digest,
        },
        "images": [{"filename": image_name, "width": 100, "height": 80, "boxes": []}],
    }
    payload.update(overrides)
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def write_rights(path: Path, source="https://commons.wikimedia.org/wiki/File:Example.jpg",
                 creator="Example Creator", licence="CC BY-SA 4.0"):
    fields = [
        "candidate_id", "source_page_url", "creator_credit",
        "licence_as_displayed", "licence_url"
    ]
    row = {
        "candidate_id": "0032", "source_page_url": source,
        "creator_credit": creator, "licence_as_displayed": licence,
        "licence_url": "https://creativecommons.org/licenses/by-sa/4.0/"
    }
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow(row)
    return path


def test_hash_is_computed_from_actual_local_bytes(tmp_path):
    image = tmp_path / "candidate_0032.jpg"
    image.write_bytes(b"synthetic image bytes")
    actual = hashlib.sha256(image.read_bytes()).hexdigest()
    annotations = write_annotation(tmp_path / "annotation.json", image.name, actual)

    report = audit(annotations, image)

    assert report["actual_sha256"] == actual
    assert report["recorded_source_sha256_matches_actual"] is True
    assert report["provenance_passed"] is True
    assert report["ready_for_training"] is False
    assert report["human_qa_acknowledged"] is False
    assert report["training_approved"] is False


def test_placeholder_hash_fails_closed_but_reports_actual_hash(tmp_path):
    image = tmp_path / "candidate_0032.jpg"
    image.write_bytes(b"synthetic image bytes")
    annotations = write_annotation(
        tmp_path / "annotation.json",
        image.name,
        "from the workflow artifact manifest; recheck before reuse",
    )

    report = audit(annotations, image)

    assert len(report["actual_sha256"]) == 64
    assert report["recorded_source_sha256_valid"] is False
    assert report["recorded_source_sha256_matches_actual"] is False
    assert report["provenance_passed"] is False
    assert "recorded_source_sha256_is_valid" in report["failed_provenance_checks"]
    assert "training_approved" in report["approval_gaps"]


def test_filename_mismatch_blocks_provenance(tmp_path):
    image = tmp_path / "real.jpg"
    image.write_bytes(b"synthetic image bytes")
    digest = sha256_file(image)
    annotations = write_annotation(tmp_path / "annotation.json", "other.jpg", digest)

    report = audit(annotations, image)

    assert report["provenance_passed"] is False
    assert "annotation_filename_matches_local_image" in report["failed_provenance_checks"]
    assert "source_filename_matches_local_image" in report["failed_provenance_checks"]


def test_rights_ledger_metadata_must_match_recorded_source(tmp_path):
    image = tmp_path / "candidate_0032.jpg"
    image.write_bytes(b"synthetic image bytes")
    digest = sha256_file(image)
    annotations = write_annotation(tmp_path / "annotation.json", image.name, digest)
    rights = write_rights(tmp_path / "rights.csv", creator="Different Creator")

    report = audit(annotations, image, rights, "0032")

    assert report["rights_ledger_row_found"] is True
    assert report["source_metadata_matches_rights_ledger"] is False
    assert report["provenance_passed"] is False
    assert "source_metadata_matches_rights_ledger" in report["failed_provenance_checks"]


def test_candidate_id_mismatch_blocks_provenance_even_when_hash_matches(tmp_path):
    image = tmp_path / "candidate_0032.jpg"
    image.write_bytes(b"synthetic image bytes")
    digest = sha256_file(image)
    annotations = write_annotation(tmp_path / "annotation.json", image.name, digest)
    payload = json.loads(annotations.read_text(encoding="utf-8"))
    payload["source"]["candidate_id"] = "0033"
    annotations.write_text(json.dumps(payload), encoding="utf-8")
    rights = write_rights(tmp_path / "rights.csv")

    report = audit(annotations, image, rights, "0032")

    assert report["recorded_source_sha256_matches_actual"] is True
    assert report["source_candidate_id_present"] is True
    assert report["source_candidate_id_matches_requested"] is False
    assert report["provenance_passed"] is False
    assert "source_candidate_id_matches_requested" in report["failed_provenance_checks"]


def test_missing_image_fails_with_clear_error(tmp_path):
    annotations = write_annotation(tmp_path / "annotation.json", "missing.jpg", "0" * 64)
    with pytest.raises(ValueError, match="local image file"):
        audit(annotations, tmp_path / "missing.jpg")


def test_hash_updates_do_not_automatically_approve_training(tmp_path):
    image = tmp_path / "candidate_0032.jpg"
    image.write_bytes(b"synthetic image bytes")
    digest = sha256_file(image)
    annotations = write_annotation(
        tmp_path / "annotation.json",
        image.name,
        digest,
        human_qa_acknowledged=True,
        training_approved=False,
    )

    report = audit(annotations, image)

    assert report["provenance_passed"] is True
    assert report["human_qa_acknowledged"] is True
    assert report["ready_for_training"] is False
    assert "training_approved" in report["approval_gaps"]


def test_repository_candidate_0032_draft_metadata_matches_rights_ledger():
    """Guard the checked-in draft/ledger join without approving its labels."""
    root = Path(__file__).resolve().parents[1]
    draft_path = (
        root / "data" / "review_batch_2026-10-22"
        / "ai_annotation_draft_NOT_FOR_TRAINING.json"
    )
    rights_path = (
        root / "data" / "review_batch_2026-10-18"
        / "source_rights_audit_2026-10-19.csv"
    )
    draft = json.loads(draft_path.read_text(encoding="utf-8"))
    with rights_path.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    matches = [row for row in rows if row.get("candidate_id") == "0032"]

    assert len(matches) == 1
    rights_row = matches[0]
    assert draft["source"]["candidate_id"] == rights_row["candidate_id"] == "0032"
    assert draft["source"]["filename"] == rights_row["filename"]
    assert draft["images"][0]["filename"] == rights_row["filename"]
    assert draft["human_qa_acknowledged"] is False
    assert draft["training_approved"] is False
    assert "not human-QA-approved" in draft["status"]
    # Matching metadata is not a hash, label-quality, rights, or training approval.


@pytest.mark.parametrize(
    "bad_url",
    [
        "https://",
        "https:///wiki/File:Example.jpg",
        "https://example.com:99999/wiki/File:Example.jpg",
        "https://example.com/wiki/File:Example image.jpg",
        "https://user:password@example.com/wiki/File:Example.jpg",
    ],
)
def test_malformed_or_credential_bearing_source_url_blocks_provenance(tmp_path, bad_url):
    image = tmp_path / "candidate_0032.jpg"
    image.write_bytes(b"synthetic image bytes")
    annotations = write_annotation(
        tmp_path / "annotation.json", image.name, sha256_file(image)
    )
    payload = json.loads(annotations.read_text(encoding="utf-8"))
    payload["source"]["file_page"] = bad_url
    annotations.write_text(json.dumps(payload), encoding="utf-8")

    report = audit(annotations, image)

    assert report["source_page_is_http_url"] is False
    assert report["provenance_passed"] is False
    assert "source_page_is_http_url" in report["failed_provenance_checks"]

