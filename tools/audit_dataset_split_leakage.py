#!/usr/bin/env python3
"""Fail-closed audit of dataset split leakage from a CSV manifest.

This checks recorded identifiers, hashes, and group assignments only. It does not
compute image hashes, verify annotations, or independently establish dataset rights.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

REQUIRED = {"image_id", "filename", "split", "group_id", "sha256"}
SPLITS = {"train", "validation", "test", "challenge", "unassigned"}
SHA256 = re.compile(r"^[0-9a-fA-F]{64}$")


def audit_manifest(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(REQUIRED - set(reader.fieldnames or []))
        if missing:
            raise ValueError("missing required columns: " + ", ".join(missing))
        rows = list(reader)

    errors: list[str] = []
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
        "group_cross_split_findings": group_leaks,
        "errors": errors,
        "passed": bool(records) and not errors and assigned,
        "limitations": [
            "This audits declared CSV values; it does not calculate SHA-256 from image files.",
            "Matching hashes detect exact byte duplicates only, not visually similar or resized images.",
            "Group IDs must be assigned consistently by the dataset curator (for example, orchard/session/source image).",
            "A passing audit does not verify image licences, label correctness, model performance, or scientific validity.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="CSV with image_id, filename, split, group_id, sha256")
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    args = parser.parse_args()
    try:
        report = audit_manifest(args.manifest)
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
