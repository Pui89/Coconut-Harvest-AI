# Coconut dataset preparation and annotation

**Detector training and inference are disabled in this repository.** The previous model-specific training, evaluation and runtime integrations have been retired. No replacement model or detector is selected.

This directory's dataset-preparation and audit utilities remain available for provenance, human annotation QA, group-aware splitting and data integrity work. Their outputs are datasets and audit records only; they do not train or evaluate a detector.

## Current evidence status

- No active detector implementation.
- No active detector training or evaluation command.
- No selected production model or bundled model weights.
- No coconut detection accuracy metrics are claimed.
- Human inspection and annotation remain available.
- The application demo continues to use manually supplied example evidence; it does not infer objects from photographs.

## Dataset handling

Collect images only where reuse rights are documented. Preserve source, licence, attribution, capture session and checksum metadata. Keep private orchard images and model weights outside this public repository. Split by tree, orchard or capture session to reduce near-duplicate leakage.

Useful data-only tools include:

- `tools/collect_commons_coconuts.py` — optional metadata-aware candidate collection; review each source and licence before use.
- `tools/coconut_annotator.html` — offline human annotation.
- `tools/convert_annotations_to_yolo.py` — annotation-format conversion.
- `training/build_dataset_from_annotations.py` — reviewed dataset packaging.
- `training/check_dataset.py` and `training/audit_dataset_splits.py` — structural and split audits.
- `tools/preview_yolo_labels.py` — offline visual label review.

These utilities do not establish annotation correctness, legal permission, orchard representativeness or model performance. Do not interpret a dataset build or audit as a trained model result.

## Reconsideration gate

Any future detector proposal requires a separate user decision, architecture and dependency review, exact code/weight/data licence review, security assessment, compatibility tests, held-out coconut dataset, human-reviewed labels and reproducible CPU-first benchmark. No package installation, model download or hosted inference is authorized by this document.
