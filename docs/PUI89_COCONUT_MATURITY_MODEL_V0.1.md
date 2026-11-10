# PUI89 Coconut Intelligence — Appearance Model v0.1

## Purpose

This is PUI89's first in-repository, trainable, CPU-first model baseline. It learns a four-way **visual appearance** classification from human-reviewed, cropped coconut images:

- \`young\`
- \`mature_green\`
- \`yellow\`
- \`brown_aging\`

These are project annotation categories, not universal botanical maturity standards. External appearance alone cannot prove internal quality or harvest readiness.

## What is implemented

- A deterministic multinomial logistic-regression model trained from scratch in Python.
- Global RGB histograms, channel means and standard deviations as features.
- Standard-library training math and JSON model serialization.
- Optional Pillow image decoding; the software does not install it.
- Local prediction with explicit uncertainty/abstention output.
- Human review required on every prediction.
- Harvest authorization is always false.

This is a deliberately simple baseline, not a state-of-the-art vision model. It classifies a **single cropped fruit image**; it does not locate coconuts in a full palm image, estimate distance/height, or control a robot.

## Dataset requirements

Use only original images with documented reuse rights, source URL, creator, licence, retrieval date and SHA-256. Each crop must have a human-reviewed class label and a reviewer record. Split by tree, orchard, source or capture session before model development. Do not put private images or model weights in Git.

Expected layout:

\`\`\`text
dataset/
  train/
    young/
    mature_green/
    yellow/
    brown_aging/
  validation/
    young/
    mature_green/
    yellow/
    brown_aging/
  test/
    young/
    mature_green/
    yellow/
    brown_aging/
\`\`\`

The trainer reads only \`train/\`. Validation and test are held aside for later independent evaluation. Do not train until rights, labels, and group-separated splits are independently reviewed. The repository's current evidence snapshot records zero approved candidates; therefore an actual real-image training run remains blocked.

## Run without installing packages

From the repository root, using an existing Python environment with Pillow already available:

\`\`\`powershell
python -m unittest tests.test_coconut_maturity_model -v
python training/train_maturity_classifier.py --dataset-root C:\\datasets\\coconut-maturity --output C:\\models\\pui89-coconut-maturity-v0.1.json
python training/predict_maturity.py --model C:\\models\\pui89-coconut-maturity-v0.1.json --image C:\\datasets\\reviewed-crops\\example.jpg
\`\`\`

No model is downloaded. If Pillow is unavailable, image training/inference stops with an explanatory error; do not install anything without checking the user's permission, licence, storage and hardware constraints.

## Evaluation and release gates

Before claiming performance, create a frozen, leakage-safe held-out test set and publish sample counts by class and source group. Report per-class precision, recall, F1, macro-F1, confusion matrix, abstention rate, latency, memory and failure examples. Compare against a majority-class baseline. Raw probabilities are **not calibrated**; confidence thresholds are triage controls only.

The model is not a detector, not a harvest-readiness certification, and not a safety controller. No output can authorize cutting or any physical action. Future robot integration must pass the separate safety, geometry, reachability, collision, exclusion-zone, emergency-stop and independent hardware-interlock gates.

## Current implementation status

- Model code: implemented in this branch.
- Unit tests: added; execution status must be read from CI.
- Real-image training: **NOT RUN — no approved training dataset established**.
- Real-image accuracy: **NOT MEASURED**.
- Physical harvesting: **NOT VALIDATED**.
