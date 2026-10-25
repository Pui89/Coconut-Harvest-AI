from __future__ import annotations

import csv
import hashlib
from pathlib import Path

from tools.inventory_coconut_local_images import build_report, sha256_file


def test_sha256_file_uses_actual_bytes(tmp_path: Path) -> None:
    image = tmp_path / "0001_sample.jpg"
    image.write_bytes(b"sample-image-bytes")
    assert sha256_file(image) == hashlib.sha256(b"sample-image-bytes").hexdigest()


def test_inventory_reports_found_and_missing_without_changing_ledger(tmp_path: Path) -> None:
    root = tmp_path / "project"
    root.mkdir()
    image = root / "0001_sample.jpg"
    image.write_bytes(b"actual-local-image")
    ledger = tmp_path / "rights.csv"
    ledger.write_text(
        "candidate_id,filename\n0001,0001_sample.jpg\n0002,0002_missing.jpg\n",
        encoding="utf-8",
    )
    original_ledger = ledger.read_bytes()

    rows = build_report(root, ledger)
    by_id = {row["candidate_id"]: row for row in rows}

    assert by_id["0001"]["status"] == "found_hashed"
    assert by_id["0001"]["bytes"] == str(len(b"actual-local-image"))
    assert by_id["0001"]["sha256"] == hashlib.sha256(b"actual-local-image").hexdigest()
    assert by_id["0002"]["status"] == "missing"
    assert ledger.read_bytes() == original_ledger


def test_duplicate_filename_is_not_assigned_a_hash(tmp_path: Path) -> None:
    root = tmp_path / "project"
    (root / "one").mkdir(parents=True)
    (root / "two").mkdir()
    (root / "one" / "0001_sample.jpg").write_bytes(b"first")
    (root / "two" / "0001_sample.jpg").write_bytes(b"second")
    ledger = tmp_path / "rights.csv"
    ledger.write_text(
        "candidate_id,filename\n0001,0001_sample.jpg\n",
        encoding="utf-8",
    )

    row = build_report(root, ledger)[0]
    assert row["status"] == "ambiguous_duplicate_filename"
    assert row["sha256"] == ""
    assert ";" in row["local_paths"]
