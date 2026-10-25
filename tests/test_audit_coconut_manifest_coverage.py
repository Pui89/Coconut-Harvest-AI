import csv
import hashlib
from pathlib import Path

from tools.audit_coconut_manifest_coverage import audit


def write_csv(path: Path, fields, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    return path


def row(cid, filename):
    return {"candidate_id": cid, "filename": filename}


def test_reports_newer_candidates_missing_from_inventory(tmp_path):
    manifest = write_csv(tmp_path / "manifest.csv", ["filename", "bytes", "sha256"], [
        {"filename": "0001_tree.jpg", "bytes": "123", "sha256": hashlib.sha256(b"x").hexdigest()},
    ])
    rights = write_csv(tmp_path / "rights.csv", ["candidate_id", "filename"], [
        row("0001", "0001_tree.jpg"), row("0032", "0032_tree.jpg"),
    ])
    review = write_csv(tmp_path / "review.csv", ["candidate_id", "filename"], [
        row("0001", "0001_tree.jpg"), row("0032", "0032_tree.jpg"),
    ])
    report = audit(manifest, rights, review)
    assert report["missing_inventory_candidate_ids"] == ["0032"]
    assert not report["coverage_complete"]


def test_complete_inventory_and_ledgers_pass_coverage_only(tmp_path):
    digest = hashlib.sha256(b"x").hexdigest()
    manifest = write_csv(tmp_path / "manifest.csv", ["filename", "bytes", "sha256"], [
        {"filename": "0001_tree.jpg", "bytes": "1", "sha256": digest},
    ])
    rights = write_csv(tmp_path / "rights.csv", ["candidate_id", "filename"], [row("0001", "0001_tree.jpg")])
    review = write_csv(tmp_path / "review.csv", ["candidate_id", "filename"], [row("0001", "0001_tree.jpg")])
    report = audit(manifest, rights, review)
    assert report["coverage_complete"]
    assert "does not hash image files" in report["limitations"][0]


def test_bad_hash_format_and_filename_mismatch_fail(tmp_path):
    manifest = write_csv(tmp_path / "manifest.csv", ["filename", "bytes", "sha256"], [
        {"filename": "0001_tree.jpg", "bytes": "0", "sha256": "bad"},
    ])
    rights = write_csv(tmp_path / "rights.csv", ["candidate_id", "filename"], [row("0001", "different.jpg")])
    review = write_csv(tmp_path / "review.csv", ["candidate_id", "filename"], [row("0001", "0001_tree.jpg")])
    report = audit(manifest, rights, review)
    assert not report["coverage_complete"]
    assert "sha256_must_be_64_hex_characters" in report["invalid_inventory_rows"][0]["issues"]
    assert "bytes_must_be_positive" in report["invalid_inventory_rows"][0]["issues"]
    assert not report["coverage"][0]["rights_filename_matches_inventory"]
