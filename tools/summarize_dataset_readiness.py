"""Summarize dataset readiness from the rights/annotation audit CSV.

Standard-library only. This reports recorded statuses; it does not independently
verify licences, annotations, image identity, or split leakage.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

REQUIRED = {
    "candidate_id", "filename", "source_page_url", "creator_credit",
    "licence_as_displayed", "licence_url", "source_page_checked_on",
    "independent_page_check", "attribution_recorded", "annotation_qa_status",
    "training_promotion",
}


def summarize(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = sorted(REQUIRED - set(reader.fieldnames or []))
        if missing:
            raise ValueError("missing required columns: " + ", ".join(missing))
        rows = list(reader)

    seen: set[str] = set()
    errors: list[str] = []
    candidates = []
    for line, row in enumerate(rows, start=2):
        candidate_id = (row.get("candidate_id") or "").strip()
        if not candidate_id:
            errors.append(f"line {line}: candidate_id is required")
        elif candidate_id in seen:
            errors.append(f"line {line}: duplicate candidate_id {candidate_id!r}")
        seen.add(candidate_id)
        gates = {
            "source_page_present": bool((row.get("source_page_url") or "").strip()),
            "creator_credit_present": bool((row.get("creator_credit") or "").strip()),
            "licence_and_url_present": bool(
                (row.get("licence_as_displayed") or "").strip()
                and (row.get("licence_url") or "").strip()
            ),
            "independent_page_check": (row.get("independent_page_check") or "").strip().lower() == "checked",
            "attribution_recorded": (row.get("attribution_recorded") or "").strip().lower() == "yes",
            "annotation_qa_passed": (row.get("annotation_qa_status") or "").strip().lower() == "passed",
            "promotion_approved": (row.get("training_promotion") or "").strip().lower() == "approved",
        }
        eligible = all(gates.values())
        candidates.append({
            "candidate_id": candidate_id,
            "filename": (row.get("filename") or "").strip(),
            "eligible_for_training": eligible,
            "failed_gates": [name for name, passed in gates.items() if not passed],
        })

    return {
        "source_file": path.name,
        "candidate_count": len(rows),
        "eligible_count": sum(item["eligible_for_training"] for item in candidates),
        "blocked_count": sum(not item["eligible_for_training"] for item in candidates),
        "ready_for_training": bool(rows) and not errors and all(item["eligible_for_training"] for item in candidates),
        "errors": errors,
        "candidates": candidates,
        "limitations": [
            "This is a fail-closed summary of recorded CSV fields, not independent rights verification.",
            "A recorded licence check does not prove legal permission or image provenance.",
            "Annotation QA must be independently completed and recorded as passed.",
            "Group-aware split integrity, duplicate/leakage checks, and image/label integrity need separate validation.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_path", type=Path, help="Path to source-rights audit CSV")
    args = parser.parse_args()
    try:
        report = summarize(args.csv_path)
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
