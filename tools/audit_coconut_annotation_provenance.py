"""Check image-byte provenance for a coconut annotation JSON file.

Standard-library only. Computes a local file SHA-256 and compares it with the
recorded annotation source hash and optional rights-ledger metadata. It never
downloads images, changes annotations, or approves labels for training.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


RIGHTS_REQUIRED = {
    "candidate_id",
    "source_page_url",
    "creator_credit",
    "licence_as_displayed",
}
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def sha256_file(path: Path) -> str:
    """Calculate SHA-256 using bounded memory."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _is_http_url(value: Any) -> bool:
    """Accept well-formed absolute HTTP(S) URLs without credentials.

    This is syntax validation only; it does not verify source ownership,
    licence terms, reachability, or permission to reuse an image.
    """
    if not isinstance(value, str):
        return False
    candidate = value.strip()
    if not candidate or any(ch.isspace() or ord(ch) < 0x20 for ch in candidate):
        return False
    try:
        parsed = urlparse(candidate)
        if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
            return False
        # Credentials in source URLs can leak secrets and are not needed for
        # public provenance records.
        if parsed.username is not None or parsed.password is not None:
            return False
        # Accessing .port forces urllib.parse to reject non-numeric/out-of-range ports.
        _ = parsed.port
        return True
    except ValueError:
        return False


def _read_rights_row(path: Path, candidate_id: str) -> dict[str, str]:
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            missing = sorted(RIGHTS_REQUIRED - set(reader.fieldnames or []))
            if missing:
                raise ValueError("rights ledger is missing columns: " + ", ".join(missing))
            matches = [
                {key: (value or "").strip() for key, value in row.items() if key}
                for row in reader
                if (row.get("candidate_id") or "").strip() == candidate_id
            ]
    except (OSError, UnicodeError, csv.Error) as exc:
        raise ValueError("could not read rights ledger") from exc

    if len(matches) != 1:
        raise ValueError(
            f"expected exactly one rights-ledger row for candidate {candidate_id}; found {len(matches)}"
        )
    return matches[0]


def audit(
    annotations_path: Path,
    image_path: Path,
    rights_csv: Path | None = None,
    candidate_id: str | None = None,
) -> dict[str, Any]:
    """Report provenance consistency for one local image and annotation JSON."""
    try:
        payload = json.loads(annotations_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("could not read valid annotation JSON") from exc
    if not isinstance(payload, dict):
        raise ValueError("annotation JSON root must be an object")
    source = payload.get("source")
    if not isinstance(source, dict):
        raise ValueError("annotation JSON must contain a source object")
    images = payload.get("images")
    if not isinstance(images, list) or not images:
        raise ValueError("annotation JSON must contain a non-empty images list")
    if not image_path.is_file():
        raise ValueError("local image file does not exist or is not a regular file")

    matching_images = [
        image for image in images
        if isinstance(image, dict) and image.get("filename") == image_path.name
    ]
    source_filename = source.get("filename")
    annotation_filename_matches = len(matching_images) == 1
    source_filename_matches = source_filename == image_path.name
    source_candidate_id = source.get("candidate_id")
    source_candidate_id_present = (
        isinstance(source_candidate_id, str) and bool(source_candidate_id.strip())
    )
    requested_candidate_id = candidate_id.strip() if isinstance(candidate_id, str) and candidate_id.strip() else None
    source_candidate_id_matches = (
        None if requested_candidate_id is None
        else source_candidate_id == requested_candidate_id
    )

    try:
        actual_sha256 = sha256_file(image_path)
    except OSError as exc:
        raise ValueError("could not read local image bytes") from exc

    recorded_sha256 = source.get("source_image_sha256")
    recorded_hash_valid = (
        isinstance(recorded_sha256, str)
        and SHA256_PATTERN.fullmatch(recorded_sha256.strip().lower()) is not None
    )
    hash_matches = bool(
        recorded_hash_valid
        and recorded_sha256.strip().lower() == actual_sha256
    )

    source_page = source.get("file_page")
    creator = source.get("creator")
    licence = source.get("license")
    source_metadata_present = all(
        isinstance(value, str) and value.strip()
        for value in (source_page, creator, licence)
    )
    source_page_is_http_url = _is_http_url(source_page)
    rights_checks: dict[str, bool] | None = None

    if rights_csv is not None:
        if not isinstance(candidate_id, str) or not candidate_id.strip():
            raise ValueError("--candidate-id is required when --rights-csv is supplied")
        rights = _read_rights_row(rights_csv, candidate_id.strip())
        rights_checks = {
            "source_page_matches": rights["source_page_url"].strip() == str(source_page).strip(),
            "creator_matches": rights["creator_credit"].strip() == str(creator).strip(),
            "licence_matches": rights["licence_as_displayed"].strip().casefold() == str(licence).strip().casefold(),
        }

    source_metadata_matches_rights = (
        all(rights_checks.values()) if rights_checks is not None else None
    )
    provenance_passed = all(
        (
            annotation_filename_matches,
            source_filename_matches,
            source_candidate_id_present,
            source_candidate_id_matches is not False,
            recorded_hash_valid,
            hash_matches,
            source_metadata_present,
            source_page_is_http_url,
            source_metadata_matches_rights is not False,
        )
    )

    # These flags must be explicit; valid hashes never imply human review.
    human_qa_acknowledged = payload.get("human_qa_acknowledged") is True
    training_approved = payload.get("training_approved") is True

    provenance_check_results = (
        ("annotation_filename_matches_local_image", annotation_filename_matches),
        ("source_filename_matches_local_image", source_filename_matches),
        ("source_candidate_id_present", source_candidate_id_present),
        ("source_candidate_id_matches_requested", source_candidate_id_matches is not False),
        ("recorded_source_sha256_is_valid", recorded_hash_valid),
        ("recorded_source_sha256_matches_actual_bytes", hash_matches),
        ("source_metadata_present", source_metadata_present),
        ("source_page_is_http_url", source_page_is_http_url),
        ("source_metadata_matches_rights_ledger", source_metadata_matches_rights is not False),
    )
    failed_provenance_checks = [
        name for name, passed in provenance_check_results if not passed
    ]
    approval_gaps = []
    if not human_qa_acknowledged:
        approval_gaps.append("human_qa_acknowledged")
    if not training_approved:
        approval_gaps.append("training_approved")

    return {
        "schema": "pui89-coconut-annotation-provenance-v1",
        "candidate_id": candidate_id or source.get("candidate_id"),
        "annotation_file": annotations_path.name,
        "image_file": image_path.name,
        "actual_sha256": actual_sha256,
        "recorded_source_sha256": recorded_sha256,
        "recorded_source_sha256_valid": recorded_hash_valid,
        "recorded_source_sha256_matches_actual": hash_matches,
        "annotation_filename_matches_local_image": annotation_filename_matches,
        "source_filename_matches_local_image": source_filename_matches,
        "source_candidate_id_present": source_candidate_id_present,
        "source_candidate_id_matches_requested": source_candidate_id_matches,
        "source_metadata_present": source_metadata_present,
        "source_page_is_http_url": source_page_is_http_url,
        "rights_ledger_row_found": rights_checks is not None,
        "source_metadata_rights_checks": rights_checks,
        "source_metadata_matches_rights_ledger": source_metadata_matches_rights,
        "provenance_passed": provenance_passed,
        "human_qa_acknowledged": human_qa_acknowledged,
        "training_approved": training_approved,
        "ready_for_training": provenance_passed and human_qa_acknowledged and training_approved,
        "failed_provenance_checks": failed_provenance_checks,
        "approval_gaps": approval_gaps,
        "limitations": [
            "This compares local image bytes to a recorded SHA-256 and checks recorded source metadata; it does not access the internet.",
            "It does not decode image dimensions, verify licence legality, or judge annotation correctness.",
            "A provenance pass is not human label QA and does not by itself authorize training.",
            "This tool never edits annotation JSON or source-rights ledgers.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--annotations", required=True, type=Path)
    parser.add_argument("--image", required=True, type=Path, help="Original local image file to hash")
    parser.add_argument("--rights-csv", type=Path, help="Optional source-rights ledger")
    parser.add_argument("--candidate-id", help="Required with --rights-csv")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        report = audit(args.annotations, args.image, args.rights_csv, args.candidate_id)
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
    return 0 if report["provenance_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
