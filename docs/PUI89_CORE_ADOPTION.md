# PUI89 Shared AI Core — Coconut Harvest AI Adapter

**Status:** Integration plan; documentation only.  
**Platform contract:** [PUI89 Evidence-to-Action Intelligence Platform](https://github.com/Pui89/Pui89.github.io/blob/main/docs/PUI89_EVIDENCE_TO_ACTION_PLATFORM.md)

## Purpose

Connect coconut maturity assessment and proposed harvesting decisions to PUI89's shared evidence, world-state, uncertainty, safety and evaluation contracts. This guide does not claim a validated detector or physical harvesting robot.

## Domain observations

Represent each observation with source, timestamp, image/data identifier, tree or fruit identifier where available, image quality, viewpoint, maturity label (young, mature green, yellow, brown-aging), annotator/source provenance and uncertainty. Missing labels remain unknown; do not infer a maturity class from an unavailable or unusable image.

## World-state fields

Track tree context, fruit candidates, maturity evidence, estimated reach/workspace only when measured, worker/animal presence, environmental conditions, robot state if physically instrumented, and the age/source of each field. Keep design assumptions separate from measured observations.

## Proposal and safety rules

- Harvest recommendation is advisory and requires human review.
- HOLD when maturity evidence is ambiguous, image quality is inadequate, tree/fruit association is uncertain, worker/animal exclusion is unknown, workspace/reach is unverified, or the system reports conflicting observations.
- BLOCK proposals that violate defined exclusion zones or operating limits.
- No cutter, arm, gripper, basket or motion command may be issued by the shared core.
- Physical reach, cutting, load handling, stability and worker-safety performance remain unvalidated until independently tested.

## Evaluation gates

1. Validate observations and world-state payloads against shared schemas.
2. Test all maturity labels plus unknown, ambiguous and low-quality cases.
3. Test missing, stale, duplicated and conflicting observations.
4. Measure per-class precision/recall on a permission-verified held-out dataset; report class counts and dataset version.
5. Evaluate abstention and calibration only when the dataset supports meaningful measurement.
6. Test human-review routing and fail-closed workspace/exclusion-zone checks.
7. Keep synthetic scenarios separate from real-image evaluation.

## Required report

Publish test command, environment, dataset/split identifier, counts, metrics, failure cases, artifact links and reviewer. If no valid held-out dataset exists, report model accuracy as NOT MEASURED.

## Implementation boundary

This document is an adoption plan. Runtime integration, field validation and physical robot safety are not established by adding this file.
