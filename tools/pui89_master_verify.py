#!/usr/bin/env python3
"""PUI89 master verification helper: safe, local, dependency-free preflight.

Default mode checks Python syntax and inventories project-specific verification
tools. --pytest explicitly runs pytest if already installed. No package/model
downloads, network calls, cloud compute, data changes, or hardware control.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tokenize
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {
    ".git", ".venv", "venv", "env", "__pycache__", "node_modules",
    "site-packages", "build", "dist", ".mypy_cache", ".pytest_cache",
}
PROJECT_GATES = [
    "tools/validate_review_ledger.py",
    "tools/coconut_dataset_promotion_gate.py",
    "tools/audit_coconut_annotation_provenance.py",
    "tools/evaluate_coconut_detections.py",
    "tools/pui89_autonomy_lab.py"
]

def python_files():
    for path in sorted(ROOT.rglob("*.py")):
        relative = path.relative_to(ROOT)
        if not any(part in SKIP_DIRS for part in relative.parts):
            yield path

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pytest", action="store_true",
                        help="also run the existing pytest suite; installs nothing")
    parser.add_argument("--report", type=Path,
                        help="optional JSON report path (relative to repository root)")
    args = parser.parse_args()

    syntax_errors = []
    checked = 0
    for path in python_files():
        try:
            with tokenize.open(path) as stream:
                compile(stream.read(), str(path), "exec", dont_inherit=True)
            checked += 1
        except (SyntaxError, UnicodeDecodeError, OSError) as exc:
            syntax_errors.append({
                "file": str(path.relative_to(ROOT)),
                "error": f"{type(exc).__name__}: {exc}",
            })

    gates = []
    for relative in PROJECT_GATES:
        exists = (ROOT / relative).is_file()
        gates.append({"path": relative, "status": "PRESENT" if exists else "MISSING"})

    report = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": ROOT.name,
        "python_version": sys.version.split()[0],
        "mode": "syntax-plus-gate-inventory" + ("-and-pytest" if args.pytest else ""),
        "python_files_checked": checked,
        "syntax_errors": syntax_errors,
        "project_gate_inventory": gates,
        "pytest": {"status": "not_requested"},
        "limitations": [
            "Presence of a tool does not prove it was executed or passed.",
            "No dataset licence, annotation correctness, model accuracy, or physical safety is certified.",
            "Simulation and synthetic results are not real-world validation.",
        ],
    }

    if args.pytest and not syntax_errors:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "-q"],
                cwd=ROOT, text=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, check=False,
            )
            report["pytest"] = {
                "status": "passed" if result.returncode == 0 else "failed",
                "exit_code": result.returncode,
                "output_tail": result.stdout[-10000:],
            }
        except OSError as exc:
            report["pytest"] = {"status": "unavailable", "error": str(exc)}

    print(json.dumps(report, indent=2))
    if args.report:
        report_path = args.report if args.report.is_absolute() else ROOT / args.report
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"Saved report: {report_path}")

    if syntax_errors:
        return 1
    if args.pytest and report["pytest"]["status"] != "passed":
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
