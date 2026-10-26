#!/usr/bin/env python3
"""Free-first local quality check: syntax scan plus optional pytest run.

This script uses only the Python standard library for syntax checks. It does not
install packages, download models, call external APIs, edit source files, or
control physical hardware.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {
    ".git", ".venv", "venv", "env", "__pycache__", "node_modules",
    "build", "dist", ".tox", ".mypy_cache", ".pytest_cache",
}


def scan_python() -> tuple[int, list[dict[str, str]]]:
    checked = 0
    errors: list[dict[str, str]] = []
    for path in sorted(ROOT.rglob("*.py")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec", dont_inherit=True)
            checked += 1
        except (OSError, UnicodeError, SyntaxError) as exc:
            errors.append({
                "file": str(path.relative_to(ROOT)),
                "error": f"{type(exc).__name__}: {exc}",
            })
    return checked, errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run free, local Python syntax checks and optionally pytest."
    )
    parser.add_argument(
        "--syntax-only", action="store_true",
        help="Only scan Python syntax; requires no third-party packages.",
    )
    parser.add_argument(
        "--report", type=Path,
        help="Optional path for a JSON report (relative paths are from the repository root).",
    )
    args = parser.parse_args()

    checked, syntax_errors = scan_python()
    report: dict[str, object] = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": ROOT.name,
        "mode": "syntax-only" if args.syntax_only else "syntax-and-tests",
        "python_version": sys.version.split()[0],
        "python_files_checked": checked,
        "syntax_errors": syntax_errors,
        "pytest": {"status": "not_requested"},
        "safety_note": (
            "Software checks only; this does not validate dataset rights, model accuracy, "
            "physical robot safety, or field performance."
        ),
    }

    exit_code = 0
    if syntax_errors:
        print(f"SYNTAX CHECK FAILED: {len(syntax_errors)} issue(s) in {checked} readable file(s).")
        for item in syntax_errors:
            print(f"- {item['file']}: {item['error']}")
        report["pytest"] = {"status": "blocked_by_syntax_errors"}
        exit_code = 1
    else:
        print(f"SYNTAX CHECK PASSED: {checked} Python file(s).")
        if not args.syntax_only:
            try:
                completed = subprocess.run(
                    [sys.executable, "-m", "pytest", "-q"],
                    cwd=ROOT,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    check=False,
                )
                report["pytest"] = {
                    "status": "passed" if completed.returncode == 0 else "failed",
                    "exit_code": completed.returncode,
                    "output_tail": completed.stdout[-8000:],
                }
                print(completed.stdout[-8000:], end="" if completed.stdout.endswith("\n") else "\n")
                if completed.returncode == 0:
                    print("PYTEST PASSED.")
                else:
                    print(f"PYTEST FAILED (exit {completed.returncode}).")
                    exit_code = completed.returncode or 1
            except OSError as exc:
                report["pytest"] = {
                    "status": "unavailable",
                    "message": "Pytest could not be started. Install the project's documented dev/test dependencies, then retry.",
                    "error": str(exc),
                }
                print("PYTEST UNAVAILABLE: install the project's documented test dependencies and retry.")
                exit_code = 2

    if args.report:
        report_path = args.report if args.report.is_absolute() else ROOT / args.report
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"JSON REPORT: {report_path.relative_to(ROOT) if report_path.is_relative_to(ROOT) else report_path}")

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
