# Research Readiness and Evaluation Plan

## Purpose

This document defines a reproducible, zero-cost path for improving Coconut Harvest AI from a software prototype toward an experimentally evaluated agricultural-AI research case study. It is a plan, not a claim that the experiments have already been completed.

## Current evidence and limits

The current end-to-end demo uses synthetic RGB/depth inputs and explicitly supplied harvestability evidence. The current `TreeVisionEncoder` produces feature tensors; it is not a trained or validated coconut detector. The current demo does not infer coconut locations, ripeness, 3D coordinates, or reachability from image pixels. The safety gate and tests can verify specified software conditions, but do not establish physical robot safety.

Consequently, report the current state as a software research prototype. Do not publish detector accuracy, localization accuracy, harvest success, or real-world safety claims until these are measured using a documented protocol.

## Research question

Under what image conditions does an AI vision method reliably identify visible coconuts, and how does performance change with occlusion, illumination and background clutter?

A later study may investigate whether calibrated depth improves 3D localization. That study requires suitable paired RGB/depth data and ground-truth locations; ordinary RGB photographs alone cannot answer it.

## Phase 0 — Verify the current software

From the repository root, in a compatible isolated Python environment:

```bat
python scripts/check_local_environment.py
python demo_end_to_end.py
python -m pytest
```

Record the date, operating system, Python version, dependency versions, CUDA availability, command exit codes, test summary, and demo report. Preserve error output if any command fails. Do not change the global Python installation or bulk-upgrade packages to make the first run pass.

A passing demo/test run establishes only that the tested software paths execute as expected. Synthetic input and test-fixture confidence values are not model-performance results.

## Phase 1 — Create a small, honest image benchmark

1. Collect a manageable set of legally reusable coconut-orchard images. Record each source URL, creator, licence, download date, and any usage restrictions.
2. Keep a source manifest. Do not upload private or restricted orchard photographs without permission.
3. Annotate visible coconut bounding boxes using one consistent rule. Record ambiguous and heavily occluded instances as uncertain rather than inventing labels.
4. Create image-level metadata for lighting, occlusion, distance/viewpoint where known, and background clutter.
5. Split data by source, tree, or capture session where possible to reduce near-duplicate leakage. Freeze the test split before tuning.
6. Double-check a sample of annotations and document annotation limitations.

A tiny sample is useful for checking the workflow, not for broad claims about generalization. Increase the dataset before making strong scientific conclusions.

## Phase 2 — Establish a detector baseline

Choose one detector only after checking its code, model-card claims, licence, runtime requirements, and compatibility with the available local hardware. Keep the first run local; do not use paid APIs, cloud GPUs, hosted endpoints, or automatic uploads.

Before running inference, verify that the model's output classes actually include coconuts. A generic vision-language model, image caption, or unrelated pretrained class is not automatically a coconut detector.

Evaluate predictions against the frozen ground-truth annotations using a documented script and a stated IoU threshold. Report, as applicable:

- number of images and annotated instances;
- precision, recall, F1 and mAP at stated IoU thresholds;
- inference latency, image size, hardware and software versions;
- false positives, missed coconuts and representative failure cases;
- limitations, uncertainty and any exclusions.

Keep training, validation and test data separate. Do not tune thresholds on the final test set. Do not present training-set results as held-out performance.

## Phase 3 — Controlled robustness study

After the baseline is reproducible, compare performance across documented subsets such as:

- clear versus partly occluded coconuts;
- bright versus shadowed conditions;
- simple versus cluttered backgrounds;
- near versus distant viewpoints, when metadata supports the distinction.

Report per-condition sample counts alongside metrics. If applying synthetic corruptions, label them as simulated perturbations and do not imply they represent the full range of real orchard conditions. Use repeated runs or suitable confidence intervals when feasible; explain the chosen method.

## Phase 4 — Optional RGB-D study

Proceed only if paired RGB/depth inputs and credible ground-truth locations are available. Compare RGB-only and RGB-D methods on the same held-out cases. Measure 3D localization error only where ground truth supports it. Inject controlled depth noise as a separate robustness experiment and report missing/invalid depth behavior.

Do not infer depth, metric position, or robot reachability from a normal RGB photograph without a valid measurement method.

## Phase 5 — Safety-gate fault tests

Expand software tests for missing sensors, stale timestamps, invalid numerical inputs, degraded sensor quality, emergency-stop state, blocked collision checks, and uncertain target evidence. State the expected result for every test and retain the test report.

A passing software safety test demonstrates behavior for that test case only. It is not proof of collision-free motion, certified safety, or permission to connect physical actuators. The current project does not send actuator commands.

## Results table template

Fill this table only with measured values; use “not measured” until an experiment has actually run.

| Experiment | Dataset / split | Metric | Result | Conditions / notes |
|---|---|---|---|---|
| Software smoke test | Synthetic demo | Exit status / tests passed | Not measured | Record environment |
| Coconut detector baseline | Frozen labelled test set | Precision, recall, mAP | Not measured | State IoU threshold |
| Occlusion robustness | Labelled condition subset | Recall / mAP | Not measured | Include sample count |
| RGB vs RGB-D | Paired data with ground truth | 3D localization error | Not measured | Optional future phase |
| Safety-gate fault tests | Defined test cases | Pass / fail by case | Not measured | Not physical safety validation |

## Zero-cost and reproducibility boundary

- Prefer local, open-source tools and small experiments.
- Do not enter billing details, create paid cloud resources, or use paid hosted inference.
- Model weights and datasets may require downloads and consume disk space; review licences before use or redistribution.
- Keep generated outputs, environment logs and result tables separate from source code where appropriate.
- Commit scripts, configuration, protocol and small text results; do not commit large datasets or model weights without checking repository size and licence.
- Record every result's command, configuration, software versions and data split so another person can reproduce it.

## Acceptance criteria for a credible case study

The project can claim an experimentally evaluated detector only after it has: (1) documented ground-truth annotations, (2) a frozen held-out test split, (3) a runnable inference/evaluation procedure, (4) actual metrics with thresholds and sample counts, and (5) disclosed failure cases and limitations.

Until those criteria are met, describe the detector benchmark as planned work and the current system as an early-stage software prototype.
