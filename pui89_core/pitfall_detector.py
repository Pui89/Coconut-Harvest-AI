"""PUI89 Pitfall Detector: dependency-free pre-action checks and JSON reports.

This is a conservative rule-based preflight, not a certified safety system.
It does not control hardware and must not be treated as proof of real-world safety.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


@dataclass
class Finding:
    code: str
    severity: str
    message: str
    field: str | None = None


def inspect_state(state: dict[str, Any]) -> dict[str, Any]:
    """Inspect a proposed AI/robot state and return a reproducible report.

    Recognized optional fields:
      project, confidence (0..1), required_fields (list[str]),
      missing_fields (list[str]), blockers (list[str]),
      sensor_conflict (bool), human_review_required (bool),
      action (str), simulation_only (bool).
    """
    findings: list[Finding] = []

    if not isinstance(state, dict):
        state = {}
        findings.append(Finding("INVALID_STATE", "BLOCK", "Input state must be a JSON object."))

    required = state.get("required_fields", [])
    missing = state.get("missing_fields", [])
    if not isinstance(required, list) or not isinstance(missing, list):
        findings.append(Finding("INVALID_FIELD_LIST", "BLOCK", "required_fields and missing_fields must be lists."))
    else:
        actual_missing = sorted({str(x) for x in missing} | {str(x) for x in required if x not in state or state.get(x) is None or state.get(x) == ""})
        for field in actual_missing:
            findings.append(Finding("MISSING_DATA", "BLOCK", f"Required data is missing: {field}", field))

    confidence = state.get("confidence")
    if confidence is not None:
        if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= confidence <= 1:
            findings.append(Finding("INVALID_CONFIDENCE", "BLOCK", "confidence must be a number from 0 to 1.", "confidence"))
        elif confidence < 0.60:
            findings.append(Finding("LOW_CONFIDENCE", "BLOCK", "Confidence is below the conservative 0.60 preflight threshold.", "confidence"))
        elif confidence < 0.80:
            findings.append(Finding("UNCERTAIN_RESULT", "WARN", "Confidence is below 0.80; consider human review.", "confidence"))

    blockers = state.get("blockers", [])
    if not isinstance(blockers, list):
        findings.append(Finding("INVALID_BLOCKERS", "BLOCK", "blockers must be a list."))
    else:
        for blocker in blockers:
            findings.append(Finding("SAFETY_BLOCKER", "BLOCK", f"Action blocked by condition: {blocker}"))

    if state.get("sensor_conflict") is True:
        findings.append(Finding("SENSOR_CONFLICT", "BLOCK", "Sensor outputs conflict; do not proceed automatically.", "sensor_conflict"))
    if state.get("human_review_required") is True:
        findings.append(Finding("HUMAN_REVIEW", "BLOCK", "Human review is required before proceeding.", "human_review_required"))

    action = state.get("action")
    if action is not None and (not isinstance(action, str) or not action.strip()):
        findings.append(Finding("INVALID_ACTION", "BLOCK", "action must be a non-empty string when provided.", "action"))

    # Stable order makes reports easier to compare between runs.
    findings.sort(key=lambda f: ({"BLOCK": 0, "WARN": 1, "INFO": 2}.get(f.severity, 3), f.code, f.message))
    blocked = any(f.severity == "BLOCK" for f in findings)
    return {
        "schema_version": "1.0",
        "detector": "PUI89 Pitfall Detector",
        "project": state.get("project", "unspecified"),
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "decision": "BLOCK" if blocked else ("WARN" if findings else "PASS"),
        "action_authorized": False if blocked else None,
        "finding_count": len(findings),
        "findings": [asdict(f) for f in findings],
        "limitations": [
            "Rule-based preflight only; not a certified safety system.",
            "PASS means only that these configured checks found no issue.",
            "No hardware commands are issued and real-world safety is not established."
        ],
    }


def inspect_file(input_path: str | Path, report_path: str | Path) -> dict[str, Any]:
    with open(input_path, "r", encoding="utf-8") as f:
        state = json.load(f)
    report = inspect_state(state)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return report


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Run PUI89 Pitfall Detector on a JSON state file.")
    parser.add_argument("input", help="Path to input JSON file")
    parser.add_argument("--report", default="pitfall-report.json", help="Output report path")
    args = parser.parse_args()
    result = inspect_file(args.input, args.report)
    print(f'{result["decision"]}: {result["finding_count"]} finding(s); report={args.report}')
    raise SystemExit(1 if result["decision"] == "BLOCK" else 0)
