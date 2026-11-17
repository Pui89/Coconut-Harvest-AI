# Coconut Harvest AI — Dataset Preparation and CPU-First Evaluation

This directory supports rights-aware image collection, human annotation, dataset auditing, experiment provenance and the separate four-class CPU appearance baseline. It does not currently provide an active object-detector training or inference stack.

## Data and rights gate

- Use only images you are authorised to access and reuse.
- Record the original source, author, licence/permission, attribution and SHA-256.
- Keep private farm images and all datasets outside the public Git repository.
- Human-review every image and annotation; ambiguous fruit must remain unlabelled or marked for review.
- Group splits by orchard, tree, capture session or video to prevent leakage.

## Annotation and dataset checks

The offline annotator and dataset utilities can prepare image/annotation records and audit the resulting dataset. The existing bounding-box text format is retained as a neutral interchange format; it does not imply that a particular detector framework is selected.

Before any model work, complete:
1. Rights and provenance review for every image.
2. Human annotation and independent annotation QA.
3. Duplicate and near-duplicate checks.
4. Group-separated train/validation/test splits.
5. Visual review of every split.
6. A written evaluation protocol with per-class precision, recall, F1, confusion matrix, sample counts and failure cases.

## Current detector status

Object-detector training and inference are paused. No detector framework, checkpoint, package or model weights are approved or selected in this repository at this stage. Do not install detector-specific packages, download weights or run retired detector scripts. A future candidate must pass independent licence, provenance, security, CPU/RAM, reproducibility and dataset-suitability review before adoption.

## CPU-first maturity appearance baseline

The separate four-class appearance model is intended for human-cropped individual coconut images. It is a lightweight appearance baseline, not a fruit detector, botanical maturity test or harvest-readiness model.

See [PUI89 Coconut Maturity Model v0.1](../docs/PUI89_COCONUT_MATURITY_MODEL_V0.1.md). Train only after image rights, human review and group-separated dataset gates pass. Keep validation and test sets separate and grouped by tree/orchard/source/session. Predictions remain uncalibrated and require human confirmation.

## Evidence boundary

No detector accuracy, orchard generalisation, physical harvesting capability or field safety is established by dataset-preparation scripts, synthetic fixtures or software tests. Publish only results generated from a reviewed, frozen, independently held-out real-image dataset, with complete conditions and limitations.
