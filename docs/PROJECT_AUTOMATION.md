# Free Local Project Automation — Coconut Harvest AI

## Purpose

This repository uses the shared PUI89 Free Project Health Check to perform repeatable, local engineering checks. The helper uses only the Python standard library by default and does not install packages, download models, call APIs, use cloud GPUs, or contact external services.

## Run on Windows

From the repository root:

```bat
python scripts\pui89_project_health_check.py
```

To save a JSON report:

```bat
python scripts\pui89_project_health_check.py --output project_health_report.json
```

If pytest is already installed and you explicitly want to run discovered project tests:

```bat
python scripts\pui89_project_health_check.py --run-tests
```

If pytest is absent, the script skips the test run and does not install it. The report file is created only when you request `--output`.

## Project-specific automation priorities

- real-image dataset provenance, annotation integrity, detector evaluation, harvest-agent rules and explicit no-actuator safety boundary.
- Record test inputs, environment, actual output, and failures.
- Report model metrics only when a model has been run on labelled test data.
- Keep concept-only, simulated, manually reviewed, and physically validated evidence clearly separated.

## What this checker does

- Confirms key repository folders and the README exist.
- Scans tracked/local Python source files outside common virtual-environment and build directories for syntax errors.
- Discovers test files.
- Optionally runs pytest only if already installed and requested.
- Emits a machine-readable JSON report.

## Limitations

This is a local starter framework, not a full CI system or an autonomous agent that silently changes code. It does not validate dataset licences, scientific labels, model accuracy, real-world rescue performance, narcotics classification reliability, robot reachability, or physical safety. Those require project-specific tests and evidence. No cloud automation or recurring background job is created by these files.
