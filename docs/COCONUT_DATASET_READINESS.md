# Coconut Dataset Readiness — Evidence Snapshot

**Snapshot date:** 22 October 2026  
**Source:** repository ledgers `data/review_batch_2026-10-18/source_rights_audit_2026-10-19.csv` and `data/review_batch_2026-10-18/candidate_review_2026-10-18.csv`.

## Current status

- Candidate records in the rights ledger: **34**.
- Matching candidate-review records: **34**.
- Candidates currently approved for training by the repository's promotion rules: **0**.
- Therefore the real-coconut training dataset is **not ready for training or accuracy claims**.

This is a transparent readiness status, not a failure of the project. The gate is designed to block unreviewed images rather than quietly treat them as valid training data. Re-run the gate whenever the ledgers change; this document is a dated snapshot, not a live report.

The gate's JSON report also includes `gate_failure_counts`, a ranked `top_blockers` list, and `recommended_next_steps` grouped into source rights, record consistency, human annotation review and explicit training approval. These are prioritisation aids only: they do not change eligibility or mark any candidate as reviewed.

## Why candidates remain blocked

The promotion gate requires all of the following to be recorded consistently in both ledgers: source and creator, licence and URL, independent source-page review, attribution, completed annotation QA, explicit training approval, matching filenames, a positive target decision, and approved label QA. The gate checks recorded fields; it cannot independently determine legal rights or whether boxes are correct.

Several source candidates are still unlabelled. The review ledger describes candidates 0001 and 0014 as provisional; 0031 and 0033 as difficult challenge candidates; 0032 as an annotation priority; and 0034 as a possible annotation exercise. These are **review priorities, not training approvals**. Their recorded visual limitations include small targets, occlusion, backlighting, glare, and overlapping fruit.

## Next no-cost action

1. **Candidate 0032 source review recorded:** the original [Wikimedia Commons page](https://commons.wikimedia.org/wiki/File:Coconut_in_Coconut_Tree.jpg) was rechecked on 2026-10-22; the ledger records creator Sarmi~Kili and CC BY-SA 4.0. The older [empty annotation handoff](../data/review_batch_2026-10-18/candidate_0032_annotation_draft_NOT_FOR_TRAINING.json) contains no boxes. A newer [eight-box AI-assisted draft](../data/review_batch_2026-10-22/ai_annotation_draft_NOT_FOR_TRAINING.json) exists, but its coordinates and coverage are **unverified and not ground truth**. The source image SHA-256 also must be checked against the actual downloaded image; the draft currently records a placeholder note rather than a digest.
2. Download the original image from the source page, verify attribution/licence and calculate its real SHA-256 locally. Open it at native resolution in `tools/coconut_annotator.html`; import the eight-box draft only as a starting point. Correct each box, remove false boxes, and add only clearly visible missed fruit. Do not guess hidden fruit boundaries.

   Before editing labels, compare the annotation draft's recorded source hash with the actual local file bytes (the current draft contains a placeholder, so the check should fail until corrected):

       python tools/audit_coconut_annotation_provenance.py --annotations data/review_batch_2026-10-22/ai_annotation_draft_NOT_FOR_TRAINING.json --image "C:\\path\\to\\candidate_0032.jpg" --rights-csv data/review_batch_2026-10-18/source_rights_audit_2026-10-19.csv --candidate-id 0032 --output provenance-audit.json

   Replace the example image path with the exact original image file on the local machine. The tool computes the actual SHA-256 and reports mismatches; it does not edit the annotation JSON, confirm legal rights, approve labels, or authorize training.

3. Export the reviewed annotations to a separate file; run `tools/audit_coconut_annotations.py`, inspect overlays, and request an independent visual QA review. Geometry checks alone do not establish correct labels.
4. Update the review and rights ledgers only with real review outcomes. Never mark QA passed or training approved merely because the JSON/box geometry is valid.
5. Re-run `tools/coconut_dataset_promotion_gate.py`. Keep candidates blocked until every required gate is genuinely satisfied.
6. After enough distinct, rights-cleared images are approved, split by orchard/source session before training, audit leakage, then evaluate on a frozen held-out test set.

## What we may claim today

- The repository has tooling for annotation, dataset validation, split-leakage audits, and detector evaluation.
- Hosted smoke tests demonstrate that selected model packages can run generic inference on a bus image.
- The repository does **not** yet demonstrate a training-ready real-coconut dataset or a validated coconut detector from those smoke tests.

## Related tools

- [Image inventory coverage audit](COCONUT_MANIFEST_COVERAGE_AUDIT.md)

- [First real-image benchmark checklist](FIRST_REAL_IMAGE_BENCHMARK_CHECKLIST.md)
- [Dataset split-leakage audit](DATASET_SPLIT_LEAKAGE_AUDIT.md)
- [Reproducible detection evaluation](REPRODUCIBLE_DETECTION_EVALUATION.md)
- [Model smoke-test results](model-smoke-test-results.md)
- [License-first model strategy](LICENSE_FIRST_MODEL_STRATEGY.md)


The provenance command's exit status represents source-byte/metadata integrity only. Its JSON separates `failed_provenance_checks` from `approval_gaps`; a provenance pass is not an approval pass, and a draft must remain blocked until actual human QA and the training gate are recorded.
