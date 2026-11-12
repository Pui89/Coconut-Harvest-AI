# PUI89 Shared AI Core — Coconut adapter adoption

**Status: Draft project fixtures prepared; conformance run pending.**

This document records Coconut Harvest AI's first proposed adoption of the shared
contract-fixture framework. It does not claim runtime adapter integration,
model validation, detector accuracy, field performance, or robot readiness.

## Pinned interface

- Shared Core repository: https://github.com/Pui89/PUI89-Shared-AI-Core
- Contract version: `0.1.0`
- Manifest version: `0.2.0`
- Project ID: `coconut-harvest-ai`
- Adapter fixture version: `0.1.0`
- Reference Core commit at preparation: `f7bfee3ce45a32b970573bd2d6cc1fb7fdde63bd`

The fixtures are synthetic and deliberately preserve unknown maturity,
unknown evidence quality, and non-executable action authority. They contain
no real images, personal data, proprietary records, model outputs, or sensor
measurements.

## Offline conformance check

Clone both repositories as sibling directories. From the Coconut repository
root, run the following command with Python 3.10 or newer:

```bash
PYTHONPATH=../PUI89-Shared-AI-Core python -c "from pui89_core.conformance import validate_project_adapter; import json; report = validate_project_adapter('.'); print(json.dumps(report, indent=2)); raise SystemExit(report['status'] != 'passed')"
```

This uses the Python standard library and local files only. It does not install
packages, download models, access paid APIs, use cloud compute, or control
hardware.

## What a pass means

A pass means only that the declared positive and negative JSON fixtures match
the pinned Shared AI Core v0.1 contract checks. It does **not** demonstrate
that Coconut's runtime adapter emits these records, that a vision model is
accurate or calibrated, or that a harvesting robot is safe.

Runtime adapter integration is a later task and must be tested separately
against real adapter outputs, permissioned data, and explicit safety gates.

## Next gates

1. Run the offline conformance command and retain its report against exact
   commits of both repositories.
2. Resolve any fixture or schema errors without weakening the safety rules.
3. Add runtime adapter tests only after the fixture gate passes.
4. Keep all hardware actions proposal-only; hardware execution remains out of
   scope for this adoption.


## Current repository pin audit — 13 November 2026

The following default-branch heads were checked against GitHub `main` and each comparison returned `identical`:

- Coconut Harvest AI: `3aa38ea884bf0081d50b1a183765e3a478736d17`
- PUI89 Shared AI Core: `d91f842bb20002627bfa6279ee15273c3e2b6906`

These are verified repository-head references for a future reproducible run. They do not mean the CLI has verified a local checkout: its current report format explicitly labels supplied pins as caller-declared. A runner must record `git rev-parse HEAD` for both checkouts before generating a result that claims checkout verification.

### Fixture inventory review

The manifest declares five positive and five negative fixture paths across Observation, WorldState, ActionProposal, FailureReport and EvidencePassport. All ten referenced files were directly retrieved from the current Coconut `main` branch during this audit.

A source-level review found that the positive examples preserve unknown maturity/evidence, and the ActionProposal and EvidencePassport examples explicitly deny execution authority. The negative examples include empty objects and explicit attempts to set `execution_authorized` to true. This is a static content review, **not an executed conformance result**.

### Current run status

**Current pinned conformance: NOT RUN.** The existing CLI is local-only, but this review did not execute repository code or dispatch/rerun GitHub Actions. No pass/fail result is inferred from the manifest or fixture presence.

Before claiming a pass:
1. Check out the exact two repository SHAs above.
2. Verify both checkouts with `git rev-parse HEAD`.
3. Run the documented offline validator against those checkouts.
4. Preserve the generated JSON report, runner version, exact SHAs and every fixture result.
5. Run runtime adapter tests separately; fixture conformance does not prove that Coconut's runtime adapter emits these records.

**Safety boundary remains unchanged:** schema-fixture checks only; no detector accuracy, real-image evidence quality, orchard performance, physical harvesting, or hardware safety claim is established.
