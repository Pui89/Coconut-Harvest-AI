# Coconut Dataset Readiness — Evidence Snapshot

**Snapshot date:** 22 October 2026  
**Source:** repository ledgers `data/review_batch_2026-10-18/source_rights_audit_2026-10-19.csv` and `data/review_batch_2026-10-18/candidate_review_2026-10-18.csv`.

## Current status

- Candidate records in the rights ledger: **34**.
- Matching candidate-review records: **34**.
- Candidates currently approved for training by the repository's promotion rules: **0**.
- Therefore the real-coconut training dataset is **not ready for training or accuracy claims**.

This is a transparent readiness status, not a failure of the project. The gate is designed to block unreviewed images rather than quietly treat them as valid training data. Re-run the gate whenever the ledgers change; this document is a dated snapshot, not a live report.

## Why candidates remain blocked

The promotion gate requires all of the following to be recorded consistently in both ledgers: source and creator, licence and URL, independent source-page review, attribution, completed annotation QA, explicit training approval, matching filenames, a positive target decision, and approved label QA. The gate checks recorded fields; it cannot independently determine legal rights or whether boxes are correct.

Several source candidates are still unlabelled. The review ledger describes candidates 0001 and 0014 as provisional; 0031 and 0033 as difficult challenge candidates; 0032 as an annotation priority; and 0034 as a possible annotation exercise. These are **review priorities, not training approvals**. Their recorded visual limitations include small targets, occlusion, backlighting, glare, and overlapping fruit.

## Next no-cost action

1. **Candidate 0032 source review completed:** the original [Wikimedia Commons page](https://commons.wikimedia.org/wiki/File:Coconut_in_Coconut_Tree.jpg) was rechecked on 2026-10-22; it names Sarmi~Kili and displays CC BY-SA 4.0. A [not-for-training annotation handoff record](../data/review_batch_2026-10-18/candidate_0032_annotation_draft_NOT_FOR_TRAINING.json) has been added. Native-resolution box annotation is still required; no bounding boxes or training approval have been fabricated.
2. Annotate only individually distinguishable attached coconuts using `tools/coconut_annotator.html` locally. Do not guess hidden fruit boundaries.
3. Export annotations outside the tracked source data; run `tools/audit_coconut_annotations.py`, inspect overlays, and request an independent visual QA review.
4. Update the review and rights ledgers only with real review outcomes. Never mark QA passed or training approved merely because the JSON/box geometry is valid.
5. Re-run `tools/coconut_dataset_promotion_gate.py`. Keep candidates blocked until every required gate is genuinely satisfied.
6. After enough distinct, rights-cleared images are approved, split by orchard/source session before training, audit leakage, then evaluate on a frozen held-out test set.

## What we may claim today

- The repository has tooling for annotation, dataset validation, split-leakage audits, and detector evaluation.
- Hosted smoke tests demonstrate that selected model packages can run generic inference on a bus image.
- The repository does **not** yet demonstrate a training-ready real-coconut dataset or a validated coconut detector from those smoke tests.

## Related tools

- [First real-image benchmark checklist](FIRST_REAL_IMAGE_BENCHMARK_CHECKLIST.md)
- [Dataset split-leakage audit](DATASET_SPLIT_LEAKAGE_AUDIT.md)
- [Reproducible detection evaluation](REPRODUCIBLE_DETECTION_EVALUATION.md)
- [Model smoke-test results](model-smoke-test-results.md)
- [License-first model strategy](LICENSE_FIRST_MODEL_STRATEGY.md)
