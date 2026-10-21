# Coconut Harvest AI: Research Evidence Checklist

This checklist defines the minimum evidence needed before making performance claims in a research statement, portfolio, or project report. It is a protocol, not a claim that the experiments have already been completed.

## 1. Freeze the evaluation setup

- [ ] Record the dataset source, usage rights, and version.
- [ ] Keep a manifest with image path, SHA-256, source-group ID, split, and annotation status.
- [ ] Split by orchard, capture session, or source group where possible; do not randomly split near-identical frames across train and test.
- [ ] Preserve a fixed held-out test set and document any exclusions before evaluating.
- [ ] Record the model name/version, weights provenance, code commit, environment, and inference settings.

## 2. Establish a human-reviewed baseline

- [ ] Have a human reviewer inspect labels and a sample of missed/ambiguous targets.
- [ ] Report the number of images, target instances, and split composition.
- [ ] Evaluate predictions against reviewed ground-truth boxes using a declared IoU threshold (include IoU >= 0.50; optionally report stricter thresholds).
- [ ] Report precision, recall, F1, and average precision only when the evaluator and ground truth support those metrics.
- [ ] Include per-image results and false-positive / false-negative examples.
- [ ] If no actual model inference has been run, label the result “not measured”; never substitute a synthetic demonstration for model performance.

## 3. Record reproducibility details

For every run, record:

| Field | Value to record |
|---|---|
| Run ID and date | Unique identifier and UTC timestamp |
| Dataset version | Manifest/version and split |
| Code | Git commit SHA |
| Model | Architecture, checkpoint source, checkpoint hash |
| Environment | OS, Python, framework and versions |
| Hardware | CPU/GPU and memory; note if CPU-only |
| Settings | Image size, confidence threshold, NMS and IoU settings |
| Results | Counts, metrics, runtime, errors, and exclusions |

## 4. Test beyond the headline metric

- [ ] Check performance by lighting, occlusion, distance, camera angle, and fruit-bunch density when labels allow.
- [ ] Check calibration/uncertainty before using confidence scores to support decisions.
- [ ] Test malformed inputs, empty detections, low-confidence outputs, and missing sensor data.
- [ ] Audit split leakage and exact duplicate images; acknowledge that hashes do not catch resized or near-duplicate images.
- [ ] Report limitations and failures alongside successful examples.

## 5. Keep robot claims separate from vision claims

A detector benchmark does not establish calibrated 3D localization, reachability, cutting safety, fruit retention, or field reliability. Before any physical trial, require an independently reviewed hazard analysis, guarded hardware, emergency stop, safe test area, human supervision, and validated interlocks. The software prototype must not directly authorize a physical cut.

## 6. Application-safe wording

Use wording supported by the evidence, for example:

> “I developed software prototypes and reproducible evaluation tools for a coconut-harvesting AI workflow. The current work focuses on data quality, held-out evaluation, and safety-aware decision support. Real-orchard generalization and physical harvesting remain unvalidated.”

Update this wording only after the corresponding experiments are completed and their results are recorded.

## Completion rule

Do not mark a checklist item complete merely because a script exists. Mark it complete only after the experiment has been run, the artifacts are saved, and the result can be reproduced from the documented inputs.
