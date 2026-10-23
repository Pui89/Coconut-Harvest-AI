"""Fail-closed promotion gate joining coconut rights and candidate-review ledgers.

Standard-library only. A candidate is eligible only when both ledgers agree and
rights, attribution, annotation QA, and explicit training approval are recorded.
This checks recorded fields; it does not independently verify licences or boxes.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from urllib.parse import urlparse
from datetime import date

RIGHTS_REQUIRED = {
    "candidate_id", "filename", "source_page_url", "creator_credit",
    "licence_as_displayed", "licence_url", "source_page_checked_on",
    "independent_page_check", "attribution_recorded", "annotation_qa_status",
    "training_promotion",
}
REVIEW_REQUIRED = {
    "candidate_id", "filename", "visual_triage", "label_status",
    "source_page_independently_checked", "review_decision", "review_notes",
}


def read_ledger(path: Path, required: set[str]) -> tuple[dict[str, dict[str, str]], list[str]]:
    errors: list[str] = []
    rows_by_id: dict[str, dict[str, str]] = {}
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            missing = sorted(required - set(reader.fieldnames or []))
            if missing:
                return {}, [f"{path}: missing required columns: {', '.join(missing)}"]
            for line, row in enumerate(reader, start=2):
                row = {key: (value or "").strip() for key, value in row.items() if key}
                candidate_id = row.get("candidate_id", "")
                if not candidate_id:
                    errors.append(f"{path}: line {line}: candidate_id is blank")
                    continue
                if candidate_id in rows_by_id:
                    errors.append(f"{path}: line {line}: duplicate candidate_id {candidate_id!r}")
                    continue
                rows_by_id[candidate_id] = row
    except (OSError, UnicodeError, csv.Error) as exc:
        errors.append(f"{path}: cannot read ledger: {exc}")
    return rows_by_id, errors


def _is_http_url(value: str) -> bool:
    """Accept only absolute HTTP(S) URLs with a hostname."""
    try:
        parsed = urlparse(value.strip())
        return parsed.scheme.lower() in {"http", "https"} and bool(parsed.netloc)
    except ValueError:
        return False


def _is_iso_date(value: str) -> bool:
    """Require a real ISO calendar date (YYYY-MM-DD)."""
    try:
        return date.fromisoformat(value.strip()).isoformat() == value.strip()
    except (ValueError, TypeError):
        return False


def evaluate(rights_csv: Path, review_csv: Path) -> dict:
    rights, errors = read_ledger(rights_csv, RIGHTS_REQUIRED)
    reviews, review_errors = read_ledger(review_csv, REVIEW_REQUIRED)
    errors.extend(review_errors)
    candidates = []
    for candidate_id, row in sorted(rights.items()):
        review = reviews.get(candidate_id)
        gates = {
            "filename_present": bool(row.get("filename", "").strip()),
            "source_page_present": bool(row.get("source_page_url")),
            "source_page_is_http_url": _is_http_url(row.get("source_page_url", "")),
            "creator_credit_present": bool(row.get("creator_credit")),
            "licence_and_url_present": bool(row.get("licence_as_displayed") and row.get("licence_url")),
            "licence_url_is_http_url": _is_http_url(row.get("licence_url", "")),
            "source_page_check_date_valid": _is_iso_date(row.get("source_page_checked_on", "")),
            "source_page_independently_checked": row.get("independent_page_check", "").lower() == "checked",
            "attribution_recorded": row.get("attribution_recorded", "").lower() == "yes",
            "annotation_qa_passed": row.get("annotation_qa_status", "").lower() == "passed",
            "rights_ledger_training_approved": row.get("training_promotion", "").lower() == "approved",
            "matching_review_record": review is not None,
            "review_filename_present": bool(review and review.get("filename", "").strip()),
            "review_filename_matches": bool(
                review and row.get("filename", "").strip()
                and review.get("filename", "").strip() == row.get("filename", "").strip()
            ),
            "review_source_checked": bool(review and review.get("source_page_independently_checked", "").lower() == "yes"),
            "candidate_review_approved": bool(review and review.get("review_decision", "").lower() == "approved"),
            "label_qa_passed": bool(review and review.get("label_status", "").lower() == "qa_passed"),
            "positive_target_candidate": bool(review and review.get("visual_triage", "").lower() == "positive_candidate"),
        }
        candidates.append({
            "candidate_id": candidate_id,
            "filename": row.get("filename", ""),
            "eligible_for_training": all(gates.values()),
            "failed_gates": [name for name, passed in gates.items() if not passed],
        })
    unmatched_reviews = sorted(set(reviews) - set(rights))
    if unmatched_reviews:
        errors.append("Review ledger has candidate IDs absent from rights ledger: " + ", ".join(unmatched_reviews))
    eligible = sum(c["eligible_for_training"] for c in candidates)
    return {
        "format": "pui89-coconut-promotion-gate-v1",
        "rights_ledger": str(rights_csv),
        "candidate_review_ledger": str(review_csv),
        "candidate_count": len(candidates),
        "eligible_count": eligible,
        "blocked_count": len(candidates) - eligible,
        "ready_for_training": bool(candidates) and not errors and eligible == len(candidates),
        "errors": errors,
        "candidates": candidates,
        "limitations": [
            "A pass verifies recorded fields only; it does not independently establish legal reuse rights.",
            "A label_qa_passed value must reflect a documented independent visual review, not just valid box geometry.",
            "This gate does not verify image bytes, near-duplicates, group leakage, split integrity, or detector performance.",
            "Do not promote archived labels or excluded candidates even if their metadata is otherwise complete.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rights-csv", type=Path, required=True, help="Source-rights audit CSV")
    parser.add_argument("--review-csv", type=Path, required=True, help="Candidate visual-review ledger CSV")
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    args = parser.parse_args()
    report = evaluate(args.rights_csv, args.review_csv)
    rendered = json.dumps(report, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if report["ready_for_training"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
