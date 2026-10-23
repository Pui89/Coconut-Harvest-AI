#!/usr/bin/env python3
"""Validate a Coconut Harvest AI candidate-review ledger (standard library only)."""
from __future__ import annotations

import argparse
import csv
import sys
from datetime import date
from pathlib import Path

REQUIRED = {
    "candidate_id", "filename", "decision", "reason_code", "reviewer",
    "reviewed_on", "source_url", "rights_status", "annotation_status", "split",
}
DECISIONS = {"approved", "reject", "quarantine_rights", "quarantine_annotation", "challenge", "deferred"}
RIGHTS = {"cleared", "unresolved", "not_checked", "not_applicable"}
ANNOTATIONS = {"reviewed", "unreviewed", "disputed", "not_applicable"}
SPLITS = {"train", "validation", "test", "challenge", "unassigned"}


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            headers = set(reader.fieldnames or [])
            missing = sorted(REQUIRED - headers)
            if missing:
                return [f"missing required columns: {', '.join(missing)}"]
            seen_ids: set[str] = set()
            seen_names: set[str] = set()
            for line, row in enumerate(reader, start=2):
                prefix = f"line {line}"
                values = {key: (row.get(key) or "").strip() for key in REQUIRED}
                for field in ("candidate_id", "filename", "decision", "reviewer", "reviewed_on", "source_url"):
                    if not values[field]:
                        errors.append(f"{prefix}: {field} is required")
                cid = values["candidate_id"]
                name = values["filename"].casefold()
                if cid:
                    if cid in seen_ids:
                        errors.append(f"{prefix}: duplicate candidate_id {cid!r}")
                    seen_ids.add(cid)
                if name:
                    if name in seen_names:
                        errors.append(f"{prefix}: duplicate filename {values['filename']!r} (case-insensitive)")
                    seen_names.add(name)
                if values["reviewed_on"]:
                    try:
                        parsed_date = date.fromisoformat(values["reviewed_on"])
                        if parsed_date.isoformat() != values["reviewed_on"]:
                            raise ValueError
                    except ValueError:
                        errors.append(f"{prefix}: reviewed_on must be a valid ISO date (YYYY-MM-DD)")
                decision = values["decision"]
                if decision and decision not in DECISIONS:
                    errors.append(f"{prefix}: invalid decision {decision!r}")
                if values["rights_status"] and values["rights_status"] not in RIGHTS:
                    errors.append(f"{prefix}: invalid rights_status {values['rights_status']!r}")
                if values["annotation_status"] and values["annotation_status"] not in ANNOTATIONS:
                    errors.append(f"{prefix}: invalid annotation_status {values['annotation_status']!r}")
                if values["split"] and values["split"] not in SPLITS:
                    errors.append(f"{prefix}: invalid split {values['split']!r}")
                if decision == "approved":
                    if values["rights_status"] != "cleared":
                        errors.append(f"{prefix}: approved candidate requires rights_status=cleared")
                    if values["annotation_status"] != "reviewed":
                        errors.append(f"{prefix}: approved candidate requires annotation_status=reviewed")
                    if values["split"] not in {"train", "validation", "test", "challenge"}:
                        errors.append(f"{prefix}: approved candidate requires an assigned split")
                if decision in {"reject", "quarantine_rights", "quarantine_annotation", "deferred"} and not values["reason_code"]:
                    errors.append(f"{prefix}: decision {decision!r} requires reason_code")
    except OSError as exc:
        return [f"cannot read {path}: {exc}"]
    except csv.Error as exc:
        return [f"CSV parse error: {exc}"]
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path, help="path to candidate-review ledger CSV")
    args = parser.parse_args()
    errors = validate(args.csv_file)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Review ledger failed: {len(errors)} issue(s).", file=sys.stderr)
        return 1
    print(f"Review ledger passed: {args.csv_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
