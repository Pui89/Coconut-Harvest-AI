"""Small, dependency-free evaluation helpers for embodied-agent projects.

This module records evaluator-provided outcomes. It does not run a robot, infer
real-world safety, or claim that a simulated test proves field readiness.
"""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

SCHEMA_VERSION = "1.0"
ALLOWED_STATUSES = {"pass", "fail", "blocked"}
REQUIRED_FIELDS = {"case_id", "scenario", "expected", "observed", "status"}


def validate_result(result: dict[str, Any]) -> list[str]:
    """Return validation errors for one result; an empty list means valid shape."""
    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS - result.keys())
    if missing:
        errors.append("missing required fields: " + ", ".join(missing))
    status = result.get("status")
    if status is not None and (not isinstance(status, str) or status not in ALLOWED_STATUSES):
        errors.append(f"status must be one of {sorted(ALLOWED_STATUSES)}")
    violations = result.get("safety_violations", [])
    if not isinstance(violations, list):
        errors.append("safety_violations must be a list")
    elif violations and status == "pass":
        errors.append("a result with safety violations cannot have status='pass'")
    for field in ("case_id", "scenario"):
        if field in result and (not isinstance(result[field], str) or not result[field].strip()):
            errors.append(f"{field} must be a non-empty string")
    return errors


def summarize_results(results: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Summarize validated case records without inventing or inferring outcomes."""
    records = list(results)
    errors: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    safety_violation_count = 0
    case_ids: set[str] = set()

    for index, record in enumerate(records):
        record_errors = validate_result(record)
        if record_errors:
            errors.append({"index": index, "case_id": record.get("case_id"), "errors": record_errors})
            continue
        case_id = record["case_id"]
        if case_id in case_ids:
            errors.append({"index": index, "case_id": case_id, "errors": ["duplicate case_id"]})
        case_ids.add(case_id)
        counts[record["status"]] += 1
        safety_violation_count += len(record.get("safety_violations", []))

    completed = counts["pass"] + counts["fail"]
    return {
        "schema_version": SCHEMA_VERSION,
        "total_records": len(records),
        "valid_status_counts": {status: counts[status] for status in ("pass", "fail", "blocked")},
        "completed_cases": completed,
        "pass_rate": (counts["pass"] / completed) if completed else None,
        "safety_violation_count": safety_violation_count,
        "validation_errors": errors,
        "interpretation_note": (
            "Results reflect the supplied evaluator records only. They do not establish "
            "real-world safety, physical-robot capability, or generalization beyond tested cases."
        ),
    }


def write_report(
    project: str,
    results: Iterable[dict[str, Any]],
    output_path: str | Path,
) -> dict[str, Any]:
    """Write a reproducible JSON report and return its contents."""
    if not isinstance(project, str) or not project.strip():
        raise ValueError("project must be a non-empty string")
    records = list(results)
    report = {
        "project": project,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        **summarize_results(records),
        "results": records,
    }
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report
