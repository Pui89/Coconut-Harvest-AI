#!/usr/bin/env python3
"""Fail-closed licence check for the installed Python environment.

Input is the JSON report produced by: pip-licenses --format=json
This is a metadata screening gate, not legal advice or a substitute for
reviewing licence texts, notices, model weights, datasets, or bundled assets.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

BLOCKED_PACKAGES = {
    "nvidia-nvshmem-cu12",
    "nvidia-nvshmem-cu13",
}
UNKNOWN_LICENSES = {
    "",
    "unknown",
    "unknown license",
    "license not found",
    "not specified",
    "n/a",
    "none",
}
PROPRIETARY_MARKERS = ("proprietary", "commercial license", "commercial licence")


def normalize_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value.strip().lower())


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: check_dependency_licenses.py <pip-licenses.json>", file=sys.stderr)
        return 2

    report_path = Path(sys.argv[1])
    try:
        records = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Cannot read licence report: {exc}", file=sys.stderr)
        return 2

    if not isinstance(records, list):
        print("Licence report must be a JSON array.", file=sys.stderr)
        return 2

    failures: list[str] = []
    reviewed = 0
    for item in records:
        if not isinstance(item, dict):
            failures.append("Malformed package record")
            continue
        name = str(item.get("Name") or item.get("name") or "").strip()
        license_name = str(item.get("License") or item.get("license") or "").strip()
        normalized = normalize_name(name)
        license_folded = license_name.casefold()

        if normalized in BLOCKED_PACKAGES:
            failures.append(
                f"{name}: blocked optional NVIDIA NVSHMEM dependency; "
                "do not include in the default CPU-first application environment"
            )
            continue
        if license_folded in UNKNOWN_LICENSES or any(
            marker in license_folded for marker in PROPRIETARY_MARKERS
        ):
            failures.append(
                f"{name or '<unnamed package>'}: licence metadata is missing, "
                f"unknown, or proprietary ({license_name or 'not declared'})"
            )
            continue
        reviewed += 1

    print(f"Packages with metadata passing this screening: {reviewed}/{len(records)}")
    if failures:
        print("LICENCE REVIEW REQUIRED:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Dependency licence metadata screening passed.")
    print(
        "Scope: installed Python package metadata only. Review full licence texts, "
        "transitive notices, model/checkpoint licences, datasets, and non-Python assets separately."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
