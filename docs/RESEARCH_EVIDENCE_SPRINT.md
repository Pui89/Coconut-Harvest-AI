# Coconut Harvest AI — Evidence Sprint

**Purpose:** turn the existing software prototype into a more credible, reproducible research case study. This is a work plan; it does not claim the experiments below have been completed.

## Priority 1 — Make the first real-image result reproducible

Use the existing [first real-image benchmark checklist](FIRST_REAL_IMAGE_BENCHMARK_CHECKLIST.md), [research evidence checklist](RESEARCH_EVIDENCE_CHECKLIST.md), and [experiment record template](EXPERIMENT_RECORD_TEMPLATE.md). Start one copy of the record for every detector run, including failed runs; fill results only from actual outputs.

1. Review image-source rights and suitability before any reuse or redistribution.
2. Download the optional reference images only if needed for private review:
   `python scripts/prepare_real_image_review.py --download`
3. Manually annotate distinct, visible coconut instances; inspect annotation overlays and correct errors.
4. Compute and verify file hashes:
   `python tools/verify_image_manifest_hashes.py --help`
5. Audit source-group splits:
   `python tools/audit_dataset_split_leakage.py --help`
6. Obtain predictions from an actual detector on the frozen held-out images. Record model/checkpoint provenance, licence, preprocessing, settings, environment and commit.
7. Evaluate the reviewed labels against those predictions:
   `python tools/evaluate_coconut_detections.py --ground-truth path/to/ground_truth.csv --predictions path/to/predictions.csv --iou 0.50 --score 0.25 --output evaluation.json`

The paths above are examples; replace them with real local files. Do not create illustrative prediction rows and report them as model output. If no compatible detector and weights are available, stop and record **inference not yet run**.

## Priority 2 — Publish the evidence, including failures

For each completed run, preserve:
- dataset source, rights status, version, image/object counts and split manifest;
- annotation instructions and human QA notes;
- detector and checkpoint identity/hash, code commit, software/hardware environment and exact command;
- raw predictions and evaluation JSON outside Git when they contain restricted images or data;
- precision, recall, F1 at declared thresholds, false-positive/false-negative examples and known limitations.

Keep the original two-image baseline visible until a later result is actually reproduced. Do not claim AP/mAP from the single-threshold evaluator, and do not infer maturity accuracy, 3D localization, cutting safety, or field reliability from detection metrics.

## Priority 3 — Keep the work free-first and safe

- Use local, standard-library tools where possible; no paid API or cloud GPU is required for the audit/evaluation scripts.
- Before downloading model weights or installing packages, check disk/RAM needs, licence and whether the local computer can run them.
- Keep datasets and model weights out of Git unless redistribution rights are explicitly confirmed.
- Keep all physical actuation disabled. Any later hardware work needs separate risk review, guarding, emergency stop, independent interlocks, qualified supervision and staged validation.

## Completion rule

A task is complete only when the command was run, its output was inspected, the evidence was saved, and another person could reproduce it from documented inputs. A script existing or CI passing is not a detector-performance result.
