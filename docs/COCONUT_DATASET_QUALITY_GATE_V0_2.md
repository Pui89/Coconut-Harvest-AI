# Coconut Dataset Quality Gate v0.3

**Status:** Implemented as a dependency-free metadata audit; not yet run in hosted CI or on a real dataset.

## Purpose

Prevent untraceable, unlicensed, weakly reviewed, duplicated or leakage-contaminated coconut images from being treated as training-ready. The gate is deliberately fail-closed.

## Required record fields

Each image record must include:
- Stable `sample_id` and lowercase SHA-256 of the original image bytes.
- `source_reference`, `rights_status`, `license_name`, and explicit `commercial_use_allowed`.
- `orchard_id`, `tree_id`, `capture_session_id`, and `near_duplicate_group`.
- One visual class: `young`, `developing_green`, `mature_green`, or `brown_aging`.
- `annotation_status: adjudicated` and at least two distinct independent reviewer identifiers.
- Group-safe `split`: `train`, `validation`, or `test`.

Do not put personal names, phone numbers, exact farm coordinates or other sensitive details in the public manifest. Use controlled pseudonymous identifiers and keep the identity/consent key separately with restricted access.

## Run

```bash
python -m unittest tests.test_coconut_dataset_gate -v
python tools/coconut_dataset_gate.py path/to/manifest.json --output dataset-gate-report.json
```

The command uses only Python's standard library. It installs nothing and makes no network calls.

## Gate semantics

- `READY_FOR_HUMAN_GATE`: metadata and split-hygiene checks passed. A human still must inspect original images, confirm permissions against source documents, adjudicate labels, and approve the dataset.
- `REVIEW_REQUIRED`: no hard error, but class coverage is incomplete.
- `BLOCKED`: one or more required checks failed; do not train.
- The tool never changes records or images and never grants legal permission.

## Leakage controls

The validator independently enforces split isolation for each declared grouping dimension:
- `orchard_id`: images from one orchard/site cannot be distributed across train, validation and test.
- `tree_id`: images from one tree remain in one split.
- `capture_session_id`: images from one capture session remain in one split.
- `near_duplicate_group`: exact/near-duplicate families remain in one split.

This is intentionally conservative. If an orchard/site is too broad to support useful splits, define and justify a different grouping protocol before dataset construction; do not silently weaken the gate. Stable pseudonymous group identifiers must be assigned truthfully. The validator checks declared identifiers and cannot discover incorrectly assigned groups or semantic duplicates by itself.

## Explicit non-claims

This audit does not inspect image pixels, detect blur/occlusion, verify copyright or consent, prove label correctness, create train/test splits, train a model, or measure accuracy. A passing report is not proof of dataset quality or legal clearance.

## Current dataset status

No real image is approved for training until its rights, provenance, annotation and independent review evidence are actually recorded and checked. Do not fabricate example records to make the gate pass.
