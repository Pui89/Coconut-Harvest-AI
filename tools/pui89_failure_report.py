#!/usr/bin/env python3
"""Create a consistent, local PUI89 check/failure record using only Python's standard library.

This records supplied results; it does not run tests, infer success, access the network,
download dependencies, execute robot actions, or upload artifacts.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

STATUSES = ("pass", "fail", "blocked", "not_run")
SEVERITIES = ("info", "low", "medium", "high", "critical")


def build_record(args):
    status = args.status
    return {
        "schema_version": "1.0",
        "project": args.project,
        "check_id": args.check_id,
        "status": status,
        "severity": args.severity,
        "expected": args.expected,
        "actual": args.actual,
        "evidence": args.evidence,
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "execution_claim": "user_supplied_status_not_independently_verified",
        "scope": "local record only; not proof of model accuracy, simulation validity, or physical safety",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="repository/project identifier")
    parser.add_argument("--check-id", required=True, help="stable, human-readable test/check ID")
    parser.add_argument("--status", choices=STATUSES, required=True)
    parser.add_argument("--severity", choices=SEVERITIES, default="medium")
    parser.add_argument("--expected", default="Not specified")
    parser.add_argument("--actual", default="Not specified")
    parser.add_argument("--evidence", default="Not supplied")
    parser.add_argument("--report", type=Path, help="optional output JSON path; no file is written without this")
    args = parser.parse_args()

    record = build_record(args)
    rendered = json.dumps(record, indent=2, ensure_ascii=False) + "\n"
    if args.report:
        target = args.report
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(rendered, encoding="utf-8")
        print(f"Report written locally: {target}")
    else:
        sys.stdout.write(rendered)
    return 1 if args.status == "fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())
