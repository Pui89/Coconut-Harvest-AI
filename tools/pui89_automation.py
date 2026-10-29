#!/usr/bin/env python3
"""PUI89 lightweight CI runner. Uses only Python's standard library."""
from __future__ import annotations

import json
import os
import sys
import time
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "verification-report.json"


class JsonTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.failures_json = []

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.failures_json.append({"test": str(test), "kind": "failure", "error": self._exc_info_to_string(err, test)})

    def addError(self, test, err):
        super().addError(test, err)
        self.failures_json.append({"test": str(test), "kind": "error", "error": self._exc_info_to_string(err, test)})

    def addSkip(self, test, reason):
        super().addSkip(test, reason)


def main() -> int:
    started = time.time()
    checked_dirs = [ROOT / name for name in ("pui89_core", "src", "apps", "tests", "tools")]
    compile_errors = []
    for folder in checked_dirs:
        if folder.is_dir():
            import compileall
            if not compileall.compile_dir(str(folder), quiet=1, force=True):
                compile_errors.append({"path": str(folder.relative_to(ROOT)), "error": "Python compilation failed"})

    tests_dir = ROOT / "tests"
    suite = unittest.defaultTestLoader.discover(str(tests_dir), top_level_dir=str(ROOT)) if tests_dir.is_dir() else unittest.TestSuite()
    stream = sys.stdout
    result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=JsonTestResult).run(suite)
    failures = compile_errors + result.failures_json
    report = {
        "schema_version": "1.0",
        "project": ROOT.name,
        "python": sys.version.split()[0],
        "checks": {"compile_directories": [p.name for p in checked_dirs if p.is_dir()],
                   "tests_discovered": result.testsRun,
                   "tests_successful": result.testsRun - len(result.failures) - len(result.errors),
                   "tests_failed": len(result.failures),
                   "tests_errored": len(result.errors),
                   "tests_skipped": len(result.skipped),
                   "compile_errors": len(compile_errors)},
        "failure_count": len(failures),
        "failures": failures,
        "duration_seconds": round(time.time() - started, 3),
        "note": "Passing software checks do not validate physical robot safety or real-world performance."
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("\nPUI89 report written to verification-report.json")
    print(json.dumps(report["checks"], indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
