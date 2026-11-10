"""Fail-closed, dependency-free governance audit for coconut image manifests.

This tool checks metadata and split hygiene only. It does not inspect pixels,
verify licences with a rights holder, judge labels, or measure model accuracy.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

LABELS = {"young", "developing_green", "mature_green", "brown_aging"}
SPLITS = {"train", "validation", "test"}
RIGHTS_OK = {"permission_verified", "public_domain_verified", "open_license_verified"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def audit_manifest(document: object) -> dict:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(document, dict) or document.get("schema_version") != "1.0":
        return {"status": "BLOCKED", "approved_records": 0,
                "record_count": 0, "errors": ["Expected object with schema_version '1.0'."],
                "warnings": []}
    records = document.get("records")
    if not isinstance(records, list) or not records:
        return {"status": "BLOCKED", "approved_records": 0,
                "record_count": 0, "errors": ["records must be a non-empty array."],
                "warnings": []}

    seen_ids: set[str] = set()
    seen_hashes: set[str] = set()
    group_splits: dict[str, set[str]] = defaultdict(set)
    class_counts: Counter = Counter()
    approved = 0

    for index, record in enumerate(records):
        prefix = f"records[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix}: expected an object.")
            continue
        sample_id = record.get("sample_id")
        if not isinstance(sample_id, str) or not sample_id.strip():
            errors.append(f"{prefix}: sample_id is required.")
        elif sample_id in seen_ids:
            errors.append(f"{prefix}: duplicate sample_id {sample_id!r}.")
        else:
            seen_ids.add(sample_id)

        digest = record.get("sha256")
        if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
            errors.append(f"{prefix}: sha256 must be 64 lowercase hexadecimal characters.")
        elif digest in seen_hashes:
            errors.append(f"{prefix}: duplicate image hash; deduplicate exact copies.")
        else:
            seen_hashes.add(digest)

        for field in ("source_reference", "license_name", "orchard_id",
                      "tree_id", "capture_session_id", "near_duplicate_group"):
            if not isinstance(record.get(field), str) or not record[field].strip():
                errors.append(f"{prefix}: {field} is required.")

        if record.get("rights_status") not in RIGHTS_OK:
            errors.append(f"{prefix}: rights_status is not independently verified.")
        if record.get("commercial_use_allowed") is not True:
            errors.append(f"{prefix}: commercial-use permission is not confirmed.")

        split = record.get("split")
        if split not in SPLITS:
            errors.append(f"{prefix}: split must be train, validation, or test.")
        group = record.get("near_duplicate_group")
        if isinstance(group, str) and group.strip() and split in SPLITS:
            group_splits[group].add(split)

        label = record.get("label")
        if label not in LABELS:
            errors.append(f"{prefix}: label is not an approved four-class label.")
        else:
            class_counts[label] += 1

        reviewers = record.get("independent_reviewers")
        if (not isinstance(reviewers, list) or len(set(x for x in reviewers if isinstance(x, str))) < 2):
            errors.append(f"{prefix}: at least two distinct independent reviewers are required.")
        if record.get("annotation_status") != "adjudicated":
            errors.append(f"{prefix}: annotation_status must be adjudicated.")

    for group, splits in sorted(group_splits.items()):
        if len(splits) > 1:
            errors.append(f"near_duplicate_group {group!r} crosses splits: {sorted(splits)}.")

    if set(class_counts) != LABELS:
        missing = sorted(LABELS - set(class_counts))
        warnings.append("Class coverage incomplete: " + (", ".join(missing) if missing else "none") + ".")
    if not any(record.get("split") == "test" for record in records if isinstance(record, dict)):
        errors.append("No independent test split is present.")

    # Approval is all-or-nothing: any blocker prevents the manifest being
    # treated as a training-ready dataset.
    if not errors:
        approved = len(records)
    return {
        "status": "READY_FOR_HUMAN_GATE" if not errors and not warnings else
                  ("BLOCKED" if errors else "REVIEW_REQUIRED"),
        "record_count": len(records),
        "approved_records": approved,
        "class_counts": dict(sorted(class_counts.items())),
        "errors": errors,
        "warnings": warnings,
        "scope": "Metadata and split-hygiene audit only; not legal verification, pixel QA, label truth, or model evaluation.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        document = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "BLOCKED", "errors": [str(exc)]}, indent=2))
        return 2
    report = audit_manifest(document)
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["status"] == "READY_FOR_HUMAN_GATE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
