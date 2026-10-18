# Reproducible Benchmark Protocol

This document defines how to evaluate Coconut Harvest AI without confusing synthetic demonstrations with real-world evidence. It is a protocol, not a report of completed experiments.

## Evaluation principles

- Separate synthetic, simulator, offline real-image, and physical-robot results.
- Use a held-out test split that was not used for model selection or threshold tuning.
- Record model weights, source commit, dependency versions, hardware, configuration, random seed, and dataset version.
- Save per-example predictions and failure cases, not only aggregate scores.
- Report sample counts and uncertainty where appropriate. Do not invent or estimate results when a run has not occurred.
- Do not treat manually entered demo values as AI predictions.
- Do not connect benchmark code to physical actuators.

## Stage A — software and safety logic

Purpose: test deterministic decision rules, input validation, report generation, and fail-closed behavior.

Minimum cases:
1. Valid candidate and complete evidence.
2. Missing RGB image.
3. Missing, non-finite, or out-of-range depth.
4. Invalid or stale sensor-health state.
5. Low-confidence candidate.
6. Candidate marked occluded or not reachable.
7. Malformed bounding box or invalid coordinate.
8. Planner failure.
9. Collision or workspace constraint violation.
10. Operator rejection, abort, and fault state.
11. Repeated run with identical input and seed.
12. JSON report round-trip and required-field validation.

Report: test count, pass/fail count, failures, environment, command, and commit SHA.

## Stage B — coconut detection on real images

Before evaluation, document image provenance, licence/permission, label policy, target definition, and train/validation/test split. Keep images from the same burst, tree, or recording session in one split to reduce leakage. Run `training/audit_dataset_splits.py` to detect exact-image hashes crossing splits; provide a `split,image,group_id` CSV to audit declared tree/session/source groups as well. Preserve the JSON audit report with the experiment.

Report at minimum:
- Number of images and labelled coconut instances per split.
- Precision, recall, and F1 at a stated confidence threshold.
- Average precision / mAP with the IoU thresholds explicitly stated, if supported by the evaluation tooling.
- Performance by lighting, occlusion, distance, and viewing angle when sample sizes permit.
- False positives, missed coconuts, and representative failure examples.

No detector score should be published until the dataset and evaluation script are fixed and the held-out evaluation has been run.

## Stage C — RGB-D localization

Evaluate only examples with valid, synchronized depth and reliable reference measurements. Document camera intrinsics, RGB-depth alignment, depth units, invalid-depth handling, and coordinate-frame conventions.

Report:
- Number of valid test targets and excluded samples, with reasons.
- Mean and median 3D position error, plus a high percentile such as the 95th percentile.
- Error by distance and occlusion where possible.
- Calibration method and independent validation procedure.
- Baseline comparison: RGB-only estimate versus RGB-D estimate, on the same held-out examples.

Do not assume an identity transform is a valid camera-to-robot calibration. Results in camera coordinates do not prove robot-base localization accuracy.

## Stage D — tracking

Use annotated sequences, not isolated still images. Define track identity, missed-detection policy, and sequence split before running experiments.

Possible metrics: ID switches, track fragmentation, precision/recall over frames, and tracking metrics supported by the selected evaluation package. Report frame rate and hardware separately.

## Stage E — simulation and motion planning

First validate the robot description, joint limits, collision geometry, tool envelope, and coordinate frames. Define a repeatable simulator version and scenario seeds.

Scenarios should include clear targets, partial occlusion, unreachable targets, joint-limit boundaries, collisions on the nominal path, invalid sensor inputs, planner timeouts, emergency stop, and recovery from a fault.

Report success and failure counts, collision events, safety-stop behavior, planning time, path length, and scenario parameters. A simulation result is not a physical safety certification.

## Stage F — controlled physical feasibility (future gate)

Physical testing is out of scope until there is a documented risk assessment, independent safety review, guarded non-cutting setup, emergency-stop verification, and qualified supervision. Do not test overhead cutting or autonomous palm climbing as an early experiment.

## Benchmark result template

| Field | Value |
|---|---|
| Experiment ID | |
| Date/time | |
| Git commit | |
| Dataset / simulator version | |
| Model and weight checksum | |
| Hardware and software versions | |
| Command and configuration | |
| Random seed(s) | |
| Split and sample count | |
| Metrics and units | |
| Failure cases / exclusions | |
| Raw log location | |
| Reproduction status | Not run / Passed / Failed |

## Publication rule

Publish only values directly produced by retained logs from the stated protocol. If an experiment has not been run, mark its status **Not yet measured**. Never present target metrics, toy examples, or simulator outputs as real-orchard or physical-robot performance.
