# PUI89 Verification Runner

Run the shared world-state contract tests from the repository root:

```bash
python tools/pui89_test_report.py
```

The runner prints a JSON report with Python/platform details, exact test names, pass/fail/error/skip counts, and failure details. It exits non-zero if a test fails or no matching tests are discovered.

To save a report locally (optional):

```bash
python tools/pui89_test_report.py --report reports/pui89-test-report.json
```

No report file is created unless `--report` is supplied. Reports may contain local environment details and should be reviewed before public sharing.

This runner uses Python's standard library and the shared contract test file only. It does not install dependencies, download models, call hosted services, or control hardware. A passing run is software-contract evidence only, not model-accuracy, simulation, physical-safety, or customer validation.
