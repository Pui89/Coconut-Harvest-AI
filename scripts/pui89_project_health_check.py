"""Free, standard-library PUI89 project health checker.

Checks repository structure and Python syntax without installing packages, using
network services, downloading models, or changing project files. Optional pytest
execution is opt-in and only runs if pytest is already installed.
"""
from __future__ import annotations

import argparse
import json
import py_compile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", "site-packages", "build", "dist"}


def python_files(root: Path):
    for path in root.rglob("*.py"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Optional JSON report path (relative to current directory unless absolute).")
    parser.add_argument("--run-tests", action="store_true", help="Run tests using pytest if installed, otherwise built-in unittest; installs nothing.")
    args = parser.parse_args()

    checks = []
    for relative in ("README.md", "docs", "scripts"):
        path = ROOT / relative
        checks.append({
            "check": f"required repository item: {relative}",
            "status": "PASS" if path.exists() else "WARN",
            "detail": "present" if path.exists() else "not found",
        })

    files = list(python_files(ROOT))
    syntax_errors = []
    for path in files:
        try:
            source = path.read_text(encoding="utf-8")
            compile(source, str(path), "exec")
        except (SyntaxError, UnicodeDecodeError, OSError) as exc:
            syntax_errors.append({"file": str(path.relative_to(ROOT)), "error": str(exc)})
    checks.append({
        "check": "Python source syntax",
        "status": "PASS" if not syntax_errors else "FAIL",
        "python_files_scanned": len(files),
        "errors": syntax_errors,
        "detail": "syntax scan only; code was not executed",
    })

    test_files = sorted(
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("test_*.py")
        if not any(part in SKIP_DIRS for part in path.parts)
    )
    test_files += sorted(
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*_test.py")
        if not any(part in SKIP_DIRS for part in path.parts)
    )
    checks.append({
        "check": "test-file discovery",
        "status": "PASS" if test_files else "WARN",
        "count": len(set(test_files)),
        "files": sorted(set(test_files)),
        "detail": "discovery only; tests are not proof of real-world safety",
    })

    test_run = {"requested": args.run_tests, "status": "NOT_RUN"}
    if args.run_tests:
        import importlib.util
        import subprocess

        if importlib.util.find_spec("pytest") is not None:
            command = [sys.executable, "-m", "pytest", "-q"]
            runner = "pytest"
        else:
            # unittest ships with Python; use it as the no-install fallback.
            command = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]
            runner = "unittest"
        try:
            result = subprocess.run(
                command,
                cwd=ROOT,
                text=True,
                capture_output=True,
                timeout=300,
                check=False,
            )
            test_run.update({
                "runner": runner,
                "status": "PASS" if result.returncode == 0 else "FAIL",
                "return_code": result.returncode,
                "stdout": result.stdout[-12000:],
                "stderr": result.stderr[-6000:],
            })
        except subprocess.TimeoutExpired as exc:
            test_run.update({
                "runner": runner,
                "status": "FAIL",
                "reason": "test command exceeded the 300-second limit",
                "stdout": str(exc.stdout or "")[-12000:],
                "stderr": str(exc.stderr or "")[-6000:],
            })

    report = {
        "framework": "PUI89 Free Project Health Check",
        "project_root": str(ROOT),
        "cost_boundary": {
            "packages_installed": False,
            "models_downloaded": False,
            "network_used": False,
            "cloud_services_used": False,
        },
        "checks": checks,
        "optional_test_run": test_run,
        "limitations": [
            "A syntax scan does not prove code correctness.",
            "Passing unit tests do not prove real-world model accuracy or robot safety.",
            "Dataset licences, labels, model licences, and performance still require project-specific review.",
            "No physical robot or operational screening/rescue system is tested by this checker.",
        ],
    }
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    print(rendered)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")
        print(f"\nReport saved to: {args.output}")
    failed = any(item["status"] == "FAIL" for item in checks) or test_run.get("status") == "FAIL"
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
