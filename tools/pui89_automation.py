#!/usr/bin/env python3
"""Dependency-free CI preflight. Full dependency-backed tests run in dedicated workflows."""
from __future__ import annotations
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "verification-report.json"
OBSERVABILITY = ROOT / "tools" / "pui89_observability.py"

def main() -> int:
    started = time.time()
    compile_errors = []
    compile_dirs = []
    for name in ("pui89_core", "src", "apps", "tests", "tools"):
        folder = ROOT / name
        if folder.is_dir():
            compile_dirs.append(name)
            proc = subprocess.run(
                [sys.executable, "-m", "compileall", "-q", str(folder)],
                cwd=ROOT, capture_output=True, text=True
            )
            if proc.returncode:
                compile_errors.append({"path": name, "error": (proc.stderr or proc.stdout).strip()})
    observability_path = ROOT / "observability-report.json"
    obs = subprocess.run(
        [sys.executable, str(OBSERVABILITY), "--report", str(observability_path)],
        cwd=ROOT, capture_output=True, text=True
    ) if OBSERVABILITY.is_file() else None
    failures = list(compile_errors)
    if obs is None:
        failures.append({"check": "observability", "error": "tools/pui89_observability.py is missing"})
    elif obs.returncode:
        failures.append({"check": "observability", "error": (obs.stderr or obs.stdout).strip()})
    report = {
        "schema_version": "1.0",
        "project": ROOT.name,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "checks": {
            "compile_directories": compile_dirs,
            "compile_errors": len(compile_errors),
            "observability_smoke": "PASS" if obs is not None and obs.returncode == 0 else "FAIL",
            "full_unit_tests": "NOT_RUN_IN_LIGHTWEIGHT_PREFLIGHT",
        },
        "failure_count": len(failures),
        "failures": failures,
        "duration_seconds": round(time.time() - started, 3),
        "limitations": [
            "This lightweight preflight intentionally does not discover dependency-backed tests.",
            "Dedicated Python test workflows remain responsible for the project's unit and integration tests.",
            "No hardware, live system telemetry, model inference, simulation, or physical safety was tested.",
        ],
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 1 if failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
