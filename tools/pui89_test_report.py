"""Run shared PUI89 contract tests and emit a reproducible JSON report."""
from __future__ import annotations
import argparse
import io
import json
import platform
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PATTERN = "test_pui89_world_state.py"

class RecordingResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []
    def addSuccess(self, test):
        super().addSuccess(test)
        self.records.append({"test": str(test), "status": "PASS"})
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.records.append({"test": str(test), "status": "FAIL", "detail": self._exc_info_to_string(err, test)})
    def addError(self, test, err):
        super().addError(test, err)
        self.records.append({"test": str(test), "status": "ERROR", "detail": self._exc_info_to_string(err, test)})
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.records.append({"test": str(test), "status": "SKIP", "detail": reason})

class RecordingRunner(unittest.TextTestRunner):
    resultclass = RecordingResult

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, help="optional JSON report path; no file is written unless specified")
    parser.add_argument("--pattern", default=DEFAULT_PATTERN, help=f"unittest filename pattern (default: {DEFAULT_PATTERN})")
    args = parser.parse_args()
    tests_dir = ROOT / "tests"
    if not tests_dir.is_dir():
        print(f"ERROR: test directory not found: {tests_dir}", file=sys.stderr)
        return 2
    suite = unittest.defaultTestLoader.discover(start_dir=str(tests_dir), pattern=args.pattern, top_level_dir=str(ROOT))
    stream = io.StringIO()
    result = RecordingRunner(stream=stream, verbosity=2).run(suite)
    report = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "repository": ROOT.name,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "test_pattern": args.pattern,
        "status": "PASS" if result.wasSuccessful() else "FAIL",
        "tests_run": result.testsRun,
        "passed": sum(x["status"] == "PASS" for x in result.records),
        "failed": sum(x["status"] == "FAIL" for x in result.records),
        "errors": sum(x["status"] == "ERROR" for x in result.records),
        "skipped": sum(x["status"] == "SKIP" for x in result.records),
        "tests": result.records,
        "runner_output": stream.getvalue(),
        "limitations": [
            "Passing contract tests do not establish AI accuracy or field reliability.",
            "Unit tests do not validate a physical robot or operational safety.",
            "No external dataset, model, simulator, or service is evaluated.",
        ],
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if args.report:
        report_path = args.report if args.report.is_absolute() else ROOT / args.report
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"Saved JSON report: {report_path}")
    return 0 if result.wasSuccessful() and result.testsRun > 0 else 1

if __name__ == "__main__":
    raise SystemExit(main())
