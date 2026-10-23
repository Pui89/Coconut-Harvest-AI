#!/usr/bin/env python3
"""Fail-closed audit of dataset split leakage from a CSV manifest.

This checks recorded identifiers, hashes, and group assignments only. It does not
compute image hashes, verify annotations, or independently establish dataset rights.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

REQUIRED = {"image_id", "filename", "split", "group_id", "sha256"}
SPLITS = {"train", "validation", "test", "challenge", "unassigned"}
SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")


def audit_manifest(path: Path, *, verify_files: bool = False, image_root: Path | None = None) -> dict:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(REQUIRED - set(reader.fieldnames or []))
        if missing:
            raise ValueError("missing required columns: " + ", ".join(missing))
        rows = list(reader)

    errors: list[str] = []
    file_hash_checks: list[dict] = []
    if verify_files and image_root is None:
        raise ValueError("image_root is required when verify_files=True")
    root = image_root.resolve() if image_root is not None else None
    by_image: dict[str, int] = {}
    by_filename: dict[str, int] = {}
    by_hash: dict[str, list[dict]] = defaultdict(list)
    by_group: dict[str, list[dict]] = defaultdict(list)
    records = []

    for line, row in enumerate(rows, start=2):
        record = {key: (row.get(key) or "").strip() for key in REQUIRED}
        prefix = f"line {line}"
        for field in ("image_id", "filename", "split", "group_id", "sha256"):
            if not record[field]:
                errors.append(f"{prefix}: {field} is required")
        if record["split"] and record["split"] not in SPLITS:
            errors.append(f"{prefix}: invalid split {record['split']!r}")
        if record["sha256"] and not SHA256.fullmatch(record["sha256"]):
            errors.append(f"{prefix}: sha256 must be 64 hexadecimal characters")
        for field, index in (("image_id", by_image), ("filename", by_filename)):
            value = record[field].casefold()
            if value and value in index:
                errors.append(f"{prefix}: duplicate {field} {record[field]!r} (first seen on line {index[value]})")
            elif value:
                index[value] = line
        if verify_files and root is not None and record["filename"] and SHA256.fullmatch(record["sha256"]):
            candidate = (root / record["filename"]).resolve()
            try:
                candidate.relative_to(root)
            except ValueError:
                errors.append(f"{prefix}: filename resolves outside image root")
            else:
                if not candidate.is_file():
                    errors.append(f"{prefix}: image file not found under image root: {record['filename']!r}")
                else:
                    digest = hashlib.sha256()
                    with candidate.open("rb") as image_file:
                        for chunk in iter(lambda: image_file.read(1024 * 1024), b""):
                            digest.update(chunk)
                    actual_hash = digest.hexdigest()
                    matches = actual_hash.casefold() == record["sha256"].casefold()
                    file_hash_checks.append({"line": line, "filename": record["filename"], "expected_sha256": record["sha256"].lower(), "actual_sha256": actual_hash, "matches": matches})
                    if not matches:
                        errors.append(f"{prefix}: sha256 does not match file content for {record['filename']!r}")
        normalized_hash = record["sha256"].lower()
        if SHA256.fullmatch(normalized_hash):
            by_hash[normalized_hash].append({**record, "line": line})
        if record["group_id"]:
            by_group[record["group_id"].casefold()].append({**record, "line": line})
        records.append(record)

    def cross_split(items: dict[str, list[dict]], label: str) -> list[dict]:
        findings = []
        for key, group in sorted(items.items()):
            splits = sorted({item["split"] for item in group if item["split"]})
            if len(splits) > 1:
                findings.append({
                    "key": key,
                    "splits": splits,
                    "rows": [{"line": item["line"], "image_id": item["image_id"], "filename": item["filename"]} for item in group],
                    "issue": label,
                })
        return findings

    hash_leaks = cross_split(by_hash, "identical_sha256_across_splits")
    group_leaks = cross_split(by_group, "group_id_spans_multiple_splits")
    for item in hash_leaks:
        errors.append(f"SHA-256 {item['key']} appears across splits: {', '.join(item['splits'])}")
    for item in group_leaks:
        errors.append(f"group_id {item['key']!r} appears across splits: {', '.join(item['splits'])}")

    split_counts = {split: sum(row["split"] == split for row in records) for split in sorted(SPLITS)}
    assigned = all(row["split"] in {"train", "validation", "test"} for row in records)
    return {
        "schema": "pui89-coconut-split-leakage-audit-v1",
        "manifest": path.name,
        "row_count": len(records),
        "split_counts": split_counts,
        "assigned_to_train_validation_test_only": assigned,
        "identical_hash_cross_split_findings": hash_leaks,
        "file_hash_verification_enabled": verify_files,
        "file_hash_checks": file_hash_checks,
        "group_cross_split_findings": group_leaks,
        "errors": errors,
        "passed": bool(records) and not errors and assigned,
        "limitations": [
            "File hashes are checked against image bytes only when --verify-files is enabled.",
            "Matching hashes detect exact byte duplicates only, not visually similar or resized images.",
            "Group IDs must be assigned consistently by the dataset curator (for example, orchard/session/source image).",
            "A passing audit does not verify image licences, label correctness, model performance, or scientific validity.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="CSV with image_id, filename, split, group_id, sha256")
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    parser.add_argument("--verify-files", action="store_true", help="Calculate each image file SHA-256 and compare it with the manifest")
    parser.add_argument("--image-root", type=Path, help="Directory containing manifest image paths; required with --verify-files")
    args = parser.parse_args()
    if args.verify_files and args.image_root is None:
        parser.error("--image-root is required with --verify-files")
    try:
        report = audit_manifest(args.manifest, verify_files=args.verify_files, image_root=args.image_root)
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
