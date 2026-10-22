# Reproducible Coconut Detector Experiment Record

Use one copy of this template for **each** detector run, including failed or zero-detection runs. Keep the completed record with the local experiment outputs; commit only records and images that are safe and permitted to redistribute. Do not fill fields from memory when they can be recovered from logs.

## 1. Run identity

- Experiment ID:
- Date/time (include timezone):
- Operator:
- Repository commit SHA:
- Command used (exact):
- Exit status / error:

## 2. Data and rights

- Dataset manifest path and SHA-256:
- Source-page / creator / licence review completed: yes / no
- Attribution requirements recorded: yes / no / not applicable
- Number of images: train ___ / validation ___ / held-out test ___
- Number of ground-truth coconut instances in held-out test:
- Source-group split audit result and output path:
- Annotation QA reviewer and date:
- Known data limitations (occlusion, glare, small fruit, repeated views, etc.):

Do not mark an image as training-approved solely because it downloaded successfully or passed a box-geometry check.

## 3. Model and inference environment

- Model architecture/name:
- Model code repository and version/commit:
- Weight filename and SHA-256:
- Weight source URL:
- Weight licence and evidence URL:
- Python version:
- Framework/runtime version:
- Operating system:
- CPU/GPU and available memory:
- Preprocessing and image-size settings:
- Confidence/score threshold:
- IoU threshold for matching:
- Warm-up policy and timing method:

If any item is unknown, write “unknown” and resolve it before making a comparison claim. Do not download weights or install packages without checking their size, licence, dependencies, and local resource requirements.

## 4. Results — fill only from actual output

| Metric | Observed value | Output file / command evidence |
|---|---|---|
| True positives (TP) | | |
| False positives (FP) | | |
| False negatives (FN) | | |
| Precision | | |
| Recall | | |
| F1 | | |
| Mean / median latency (ms per image) | | |
| Number of images actually evaluated | | |
| Number of ground-truth objects | | |

The repository CSV evaluator reports precision, recall, and F1 at the chosen thresholds; it does **not** calculate COCO mAP. Report latency separately from accuracy. Never substitute sample rows or example values for measured results.

## 5. Error analysis

- False-positive patterns:
- Missed-object patterns:
- Difficult examples inspected (IDs only where appropriate):
- Were all predictions reviewed visually? yes / no
- Did any test-set information influence model or threshold selection? If yes, invalidate the test result and create a new held-out split.
- Known failure cases:

## 6. Reproduction and conclusion

- Ground-truth CSV path and SHA-256:
- Prediction CSV path and SHA-256:
- Evaluation JSON path and SHA-256:
- Annotation audit output path:
- Dataset split audit output path:
- Exact rerun instructions:
- Conclusion supported by these data:
- Claims explicitly **not** supported:
- Next experiment:

## Release gate

Before publishing a result, confirm:

- [ ] Image reuse and redistribution terms have been checked.
- [ ] Ground-truth boxes were manually inspected and independently QA-reviewed.
- [ ] Train/validation/test source groups are disjoint; duplicate/near-duplicate risks were reviewed.
- [ ] Model weights, code version, settings, and hardware are recorded.
- [ ] Metrics come from actual held-out predictions and are reproducible from saved files.
- [ ] Dataset size, thresholds, limitations, and failure cases are disclosed.
- [ ] No claims of orchard-wide generalisation, 3D accuracy, safe cutting, or autonomous field operation are inferred from this image benchmark.

**Status until populated:** template only — no new detector experiment or performance result is implied.
