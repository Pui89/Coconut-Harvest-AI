# Free Local Project Automation — Coconut Harvest AI

## Shared fast feedback loop

Run the standard-library-only preflight first:

```bat
python tools\pui89_fast_check.py
```

It scans Python syntax and checks a few repository-structure markers without installing packages, downloading model weights, calling an API, or using a GPU. To request the full pytest suite, use `python tools\pui89_fast_check.py --pytest`; it runs pytest only if it is already installed and never installs it.

GitHub Actions also runs this quick preflight on relevant pushes and pull requests. It is an early warning, not a substitute for the full project tests, data/licence review, model benchmarks, or physical safety validation. The helper reports issues; it does not automatically rewrite or repair code.


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

To explicitly run project tests (pytest is used if installed; otherwise the built-in unittest runner is used):

```bat
python scripts\pui89_project_health_check.py --run-tests
```

If pytest is absent, the script falls back to Python's built-in unittest discovery. No packages are installed. The report file is created only when you request `--output`.

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
