#!/usr/bin/env python3
"""PUI89 repository-level guardrail preflight (stdlib only).

This is a CI configuration risk screen. It does not prove runtime safety,
model correctness, legal clearance, or physical robot safety.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

WORKFLOWS = Path(".github/workflows")
BLOCK_PATTERNS = {
    "privileged pull_request_target trigger": re.compile(r"(?m)^\s*pull_request_target\s*:"),
    "unrestricted write-all token permissions": re.compile(r"(?im)^\s*permissions\s*:\s*write-all\s*$"),
    "remote script piped directly to shell": re.compile(
        r"(?i)\b(?:curl|wget)\b[^\n|]*\|\s*(?:sudo\s+)?(?:ba)?sh\b"
    ),
    "mutable main/master action reference": re.compile(
        r"(?im)^\s*uses\s*:\s*[^\s]+@(main|master)\s*(?:#.*)?$"
    ),
}
REVIEW_PATTERNS = {
    "workflow trigger may require privilege review": re.compile(r"(?m)^\s*workflow_run\s*:"),
    "workflow has no explicit permissions block": None,
}


def main() -> int:
    files = sorted(WORKFLOWS.glob("*.yml")) + sorted(WORKFLOWS.glob("*.yaml"))
    findings: list[dict[str, str]] = []
    if not files:
        findings.append({"level": "BLOCK", "file": str(WORKFLOWS), "finding": "No GitHub Actions workflow files found"})
    for path in files:
        try:
            content = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            findings.append({"level": "BLOCK", "file": str(path), "finding": f"Cannot read workflow: {exc}"})
            continue
        for label, pattern in BLOCK_PATTERNS.items():
            if pattern.search(content):
                findings.append({"level": "BLOCK", "file": str(path), "finding": label})
        if REVIEW_PATTERNS["workflow trigger may require privilege review"].search(content):
            findings.append({
                "level": "REVIEW", "file": str(path),
                "finding": "workflow_run trigger needs an explicit privilege and artifact-trust review"
            })
        if not re.search(r"(?m)^\s*permissions\s*:", content):
            findings.append({
                "level": "REVIEW", "file": str(path),
                "finding": "No explicit permissions block; verify least-privilege token scope"
            })

    blocked = [item for item in findings if item["level"] == "BLOCK"]
    review = [item for item in findings if item["level"] == "REVIEW"]
    report = {
        "check": "pui89_repository_guardrails",
        "workflow_files_scanned": len(files),
        "status": "BLOCKED" if blocked else ("PASS_WITH_REVIEW" if review else "PASS"),
        "blocked_count": len(blocked),
        "review_count": len(review),
        "findings": findings,
        "scope_limit": (
            "Static workflow configuration screening only. Does not test application runtime, "
            "model behavior, tool permissions, hardware interlocks, deployment security, "
            "dataset/model licensing, or legal compliance."
        ),
    }
    print(json.dumps(report, indent=2))
    Path("pui89-guardrail-report.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    return 1 if blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
