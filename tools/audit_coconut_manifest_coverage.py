"""Audit coverage of the legacy coconut image inventory against review ledgers.

Standard-library only. This checks inventory metadata coverage, not local image bytes,
licence legality, annotation correctness, or training eligibility.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

MANIFEST_REQUIRED = {"filename", "bytes", "sha256"}
LEDGER_REQUIRED = {"candidate_id", "filename"}


def read_csv(path: Path, required: set[str]) -> tuple[list[dict[str, str]], list[str]]:
    errors: list[str] = []
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            missing = sorted(required - set(reader.fieldnames or []))
            if missing:
                return [], [f"{path}: missing required columns: {', '.join(missing)}"]
            return [
                {key: (value or "").strip() for key, value in row.items() if key}
                for row in reader
            ], []
    except (OSError, UnicodeError, csv.Error) as exc:
        return [], [f"{path}: cannot read CSV: {exc}"]


def candidate_id(filename: str) -> str | None:
    match = re.match(r"^(\d{4})_", filename)
    return match.group(1) if match else None


def audit(manifest_path: Path, rights_path: Path, review_path: Path) -> dict:
    manifest, errors = read_csv(manifest_path, MANIFEST_REQUIRED)
    rights, e = read_csv(rights_path, LEDGER_REQUIRED)
    errors.extend(e)
    reviews, e = read_csv(review_path, LEDGER_REQUIRED)
    errors.extend(e)

    inventory_by_id: dict[str, dict[str, str]] = {}
    duplicate_inventory_ids: list[str] = []
    invalid_inventory_rows: list[dict[str, str]] = []
    for line, row in enumerate(manifest, start=2):
        cid = candidate_id(row.get("filename", ""))
        issues = []
        if cid is None:
            issues.append("filename_has_no_four_digit_candidate_prefix")
        else:
            if cid in inventory_by_id:
                duplicate_inventory_ids.append(cid)
                issues.append("duplicate_candidate_id_in_inventory")
            else:
                inventory_by_id[cid] = row
        try:
            size = int(row.get("bytes", ""))
            if size <= 0:
                issues.append("bytes_must_be_positive")
        except ValueError:
            issues.append("bytes_must_be_positive_integer")
        digest = row.get("sha256", "").lower()
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            issues.append("sha256_must_be_64_hex_characters")
        if issues:
            invalid_inventory_rows.append({
                "line": str(line), "filename": row.get("filename", ""),
                "candidate_id": cid or "", "issues": issues,
            })

    def ledger_index(rows: list[dict[str, str]], label: str):
        indexed = {}
        duplicates = []
        for row in rows:
            cid = row.get("candidate_id", "")
            if not cid:
                errors.append(f"{label}: blank candidate_id")
            elif cid in indexed:
                duplicates.append(cid)
            else:
                indexed[cid] = row
        return indexed, sorted(set(duplicates))

    rights_by_id, duplicate_rights = ledger_index(rights, "rights ledger")
    review_by_id, duplicate_reviews = ledger_index(reviews, "review ledger")
    all_ids = sorted(set(rights_by_id) | set(review_by_id) | set(inventory_by_id))
    coverage = []
    for cid in all_ids:
        rr, rv, inv = rights_by_id.get(cid), review_by_id.get(cid), inventory_by_id.get(cid)
        coverage.append({
            "candidate_id": cid,
            "rights_ledger_present": rr is not None,
            "review_ledger_present": rv is not None,
            "inventory_present": inv is not None,
            "rights_filename_matches_inventory": bool(rr and inv and rr.get("filename") == inv.get("filename")),
            "review_filename_matches_inventory": bool(rv and inv and rv.get("filename") == inv.get("filename")),
        })
    missing_inventory = sorted((set(rights_by_id) | set(review_by_id)) - set(inventory_by_id))
    inventory_without_ledgers = sorted(set(inventory_by_id) - (set(rights_by_id) | set(review_by_id)))
    return {
        "format": "pui89-coconut-inventory-coverage-audit-v1",
        "manifest": str(manifest_path),
        "candidate_count_in_rights_ledger": len(rights_by_id),
        "candidate_count_in_review_ledger": len(review_by_id),
        "inventory_row_count": len(manifest),
        "missing_inventory_candidate_ids": missing_inventory,
        "inventory_ids_without_ledger_records": inventory_without_ledgers,
        "duplicate_inventory_candidate_ids": sorted(set(duplicate_inventory_ids)),
        "duplicate_rights_candidate_ids": duplicate_rights,
        "duplicate_review_candidate_ids": duplicate_reviews,
        "invalid_inventory_rows": invalid_inventory_rows,
        "coverage": coverage,
        "errors": errors,
        "coverage_complete": bool(all_ids) and not errors and not missing_inventory
            and not inventory_without_ledgers and not duplicate_inventory_ids
            and not duplicate_rights and not duplicate_reviews and not invalid_inventory_rows
            and all(item["rights_filename_matches_inventory"] and item["review_filename_matches_inventory"]
                    for item in coverage),
        "limitations": [
            "This audit checks CSV coverage and digest formatting only; it does not hash image files.",
            "A syntactically valid SHA-256 value is not proof that it matches an image.",
            "Coverage does not establish legal reuse rights, annotation QA, training approval, or detector accuracy.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--rights-csv", required=True, type=Path)
    parser.add_argument("--review-csv", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = audit(args.manifest, args.rights_csv, args.review_csv)
    rendered = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["coverage_complete"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
