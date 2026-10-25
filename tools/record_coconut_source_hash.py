"""Safely record SHA-256 for the exact published Coconut Commons source image.

The tool is intentionally scoped to candidate 0032. It uses Wikimedia Commons'
published SHA-1 and byte size only to establish that the local file matches the
currently recorded source file, then calculates SHA-256 for project provenance.
Writing the JSON requires an explicit --write-source-sha256 flag. It never
changes boxes, human-QA status, training approval, or rights ledgers.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any

SOURCE_REFERENCE: dict[str, Any] = {
    "candidate_id": "0032",
    "filename": "0032_Coconut_in_Coconut_Tree.jpg",
    "source_page_url": "https://commons.wikimedia.org/wiki/File:Coconut_in_Coconut_Tree.jpg",
    "creator_credit": "Sarmi~Kili",
    "licence_as_displayed": "CC BY-SA 4.0",
    "published_sha1": "34a77896b7ad78532cd41aadc2c3967220fd91ab",
    "published_size_bytes": 8_631_989,
    "published_width": 5_184,
    "published_height": 3_456,
}
RIGHTS_REQUIRED = {
    "candidate_id", "filename", "source_page_url", "creator_credit",
    "licence_as_displayed",
}
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def _hash_file(path: Path) -> tuple[int, str, str]:
    """Return byte size, SHA-1, and SHA-256 using bounded memory."""
    size = 0
    sha1 = hashlib.sha1()
    sha256 = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            size += len(chunk)
            sha1.update(chunk)
            sha256.update(chunk)
    return size, sha1.hexdigest(), sha256.hexdigest()


def _rights_row(path: Path, candidate_id: str) -> dict[str, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            missing = sorted(RIGHTS_REQUIRED - set(reader.fieldnames or []))
            if missing:
                raise ValueError("rights ledger missing columns: " + ", ".join(missing))
            matches = [
                {key: (value or "").strip() for key, value in row.items() if key}
                for row in reader
                if (row.get("candidate_id") or "").strip() == candidate_id
            ]
    except (OSError, UnicodeError, csv.Error) as exc:
        raise ValueError("could not read rights ledger") from exc
    if len(matches) != 1:
        raise ValueError(
            f"expected exactly one rights-ledger row for candidate {candidate_id}; "
            f"found {len(matches)}"
        )
    return matches[0]


def record_source_hash(
    annotations_path: Path,
    image_path: Path,
    rights_csv: Path,
    *,
    write_source_sha256: bool = False,
    source_reference: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Check the source fingerprint, report SHA-256, and optionally write it.

    source_reference is exposed for offline unit tests. CLI callers use the
    fixed repository constant; the reference cannot be overridden via CLI.
    """
    reference = source_reference or SOURCE_REFERENCE
    try:
        payload = json.loads(annotations_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("could not read valid annotation JSON") from exc
    if not isinstance(payload, dict):
        raise ValueError("annotation JSON root must be an object")
    source = payload.get("source")
    images = payload.get("images")
    if not isinstance(source, dict):
        raise ValueError("annotation JSON must contain a source object")
    if not isinstance(images, list) or len(images) != 1 or not isinstance(images[0], dict):
        raise ValueError("expected exactly one image entry for candidate 0032")
    if not image_path.is_file():
        raise ValueError("local source image does not exist or is not a regular file")

    rights = _rights_row(rights_csv, str(reference["candidate_id"]))
    try:
        size, actual_sha1, actual_sha256 = _hash_file(image_path)
    except OSError as exc:
        raise ValueError("could not read local source image bytes") from exc

    img = images[0]
    checks = {
        "candidate_id_matches_reference": source.get("candidate_id") == reference["candidate_id"],
        "source_filename_matches_reference": source.get("filename") == reference["filename"],
        "annotation_filename_matches_reference": img.get("filename") == reference["filename"],
        "local_basename_matches_reference": image_path.name == reference["filename"],
        "annotation_dimensions_match_source_page": (
            img.get("width") == reference["published_width"]
            and img.get("height") == reference["published_height"]
        ),
        "source_page_matches_rights_ledger": (
            source.get("file_page") == reference["source_page_url"]
            and rights["source_page_url"] == reference["source_page_url"]
        ),
        "creator_matches_rights_ledger": (
            source.get("creator") == reference["creator_credit"]
            and rights["creator_credit"] == reference["creator_credit"]
        ),
        "licence_matches_rights_ledger": (
            str(source.get("license", "")).strip().casefold()
            == str(reference["licence_as_displayed"]).strip().casefold()
            and rights["licence_as_displayed"].strip().casefold()
            == str(reference["licence_as_displayed"]).strip().casefold()
        ),
        "rights_ledger_filename_matches_reference": (
            rights["candidate_id"] == reference["candidate_id"]
            and rights["filename"] == reference["filename"]
        ),
        "local_byte_size_matches_published_source": size == reference["published_size_bytes"],
        "local_sha1_matches_published_source": actual_sha1 == reference["published_sha1"],
    }
    source_identity_passed = all(checks.values())

    recorded_before = source.get("source_image_sha256")
    recorded_valid = (
        isinstance(recorded_before, str)
        and SHA256_PATTERN.fullmatch(recorded_before.strip().lower()) is not None
    )
    recorded_matches_before = bool(
        recorded_valid and recorded_before.strip().lower() == actual_sha256
    )

    wrote = False
    if write_source_sha256 and source_identity_passed:
        # Change only this field. The draft's boxes and review/approval flags stay intact.
        source["source_image_sha256"] = actual_sha256
        rendered = json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
        temporary_name: str | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                newline="\n",
                dir=annotations_path.parent,
                prefix=annotations_path.name + ".",
                suffix=".tmp",
                delete=False,
            ) as handle:
                temporary_name = handle.name
                handle.write(rendered)
            os.replace(temporary_name, annotations_path)
            wrote = True
        except OSError as exc:
            if temporary_name:
                try:
                    Path(temporary_name).unlink(missing_ok=True)
                except OSError:
                    pass
            raise ValueError("could not safely write annotation JSON") from exc

    recorded_after = actual_sha256 if wrote else recorded_before
    return {
        "schema": "pui89-coconut-source-hash-record-v1",
        "candidate_id": reference["candidate_id"],
        "image_file": image_path.name,
        "file_size_bytes": size,
        "published_size_bytes": reference["published_size_bytes"],
        "actual_sha1": actual_sha1,
        "published_sha1": reference["published_sha1"],
        "actual_sha256": actual_sha256,
        "recorded_sha256_before": recorded_before,
        "recorded_sha256_valid_before": recorded_valid,
        "recorded_sha256_matches_actual_before": recorded_matches_before,
        "recorded_sha256_after": recorded_after,
        "source_checks": checks,
        "source_identity_passed": source_identity_passed,
        "source_sha256_written": wrote,
        "human_qa_acknowledged": payload.get("human_qa_acknowledged") is True,
        "training_approved": payload.get("training_approved") is True,
        "approval_flags_changed": False,
        "annotation_boxes_changed": False,
        "limitations": [
            "The fixed SHA-1 and file-size fingerprint binds the local bytes to the Commons file version recorded by this tool; SHA-256 is the repository provenance digest.",
            "If Commons updates or replaces the source file, this tool fails closed until a human verifies the new source fingerprint and intentionally updates the reference.",
            "This tool does not judge annotation boxes, confirm legal advice, approve training, or measure detector performance.",
            "Writing the SHA-256 never sets human_qa_acknowledged or training_approved to true.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--annotations", required=True, type=Path)
    parser.add_argument("--image", required=True, type=Path)
    parser.add_argument("--rights-csv", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument(
        "--write-source-sha256",
        action="store_true",
        help="Explicitly write the computed SHA-256 only after the source fingerprint matches.",
    )
    args = parser.parse_args()
    try:
        report = record_source_hash(
            args.annotations,
            args.image,
            args.rights_csv,
            write_source_sha256=args.write_source_sha256,
        )
    except ValueError as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        try:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(rendered, encoding="utf-8")
        except OSError:
            parser.error("could not write report output")
    print(rendered, end="")
    return 0 if report["source_identity_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
