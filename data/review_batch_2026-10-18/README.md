# Candidate batch 1 — visual review and first labels

**Review date:** 18–19 October 2026  
**Scope:** 30 images from the temporary GitHub Actions artifact `coconut-image-candidates` (run 39092214196).

## Current result

- All 30 files were visually triaged in a contact sheet and assigned a conservative decision in `candidate_review_2026-10-18.csv`.
- The first-pass labels for candidates 0002 (9 boxes) and 0004 (6 boxes) are now **retired from the active training candidate set** because their annotation QA is unresolved. They remain in `annotations_ARCHIVE_v0.1_NOT_FOR_TRAINING.json` as audit history only; do not train on them.
- Replacement candidates 0033 and 0034 have been selected after visual screening: [Coconut bunch in the tree](https://commons.wikimedia.org/wiki/File:Coconut_bunch_in_the_tree.JPG) (Yasagan, CC BY-SA 3.0) and [Coconut fruits](https://commons.wikimedia.org/wiki/File:Coconut_fruits.jpg) (Vinshi / Vishwas Suryawanshi, CC BY-SA 3.0). Both have source-page and licence records in the updated source-rights ledger. They are **not labelled yet**; do not promote them to training until annotations are created and independently reviewed.
- Commons source pages for candidates 0001, 0002 and 0004 were checked on 18 October; candidate 0014 was checked on 19 October. Candidate 0001 remains provisional and is not yet boxed. The other 26 image source pages have not been independently checked here and are not cleared for inclusion in a distributable training set. See the [source-rights audit ledger](source_rights_audit_2026-10-19.csv).
- The fixed HSV-contour smoke test on the same two images produced 20 predicted boxes against 15 manually drawn boxes, with 0 true positives at IoU ≥ 0.50 (precision 0.000, recall 0.000, F1 0.000); mean CPU runtime was 15.12 ms/image in that run. This is a failed colour-contour heuristic baseline, not a learned detector.

## Dataset promotion gate

Use the [dataset QA gate](../../docs/DATASET_QA_GATE_2026-10-19.md) before any candidate is promoted into a distributable training dataset. Candidate triage, source-page checks, first-pass boxes, and geometric checks are separate states; none alone constitutes dataset approval.

## Important limits

This is **not** a complete training dataset or a valid held-out benchmark. The 15 boxes are single-pass annotations and need independent label QA. Two images cannot support a train/validation/test split or a generalization claim. No learned model was trained, no checkpoint was evaluated, and no orchard/robot performance was measured. The zero scores are for the simple HSV heuristic only—not for a trained AI model.

## Files

- `candidate_review_2026-10-18.csv`: visual triage and review/licence state for all 30 files.
- `source_rights_audit_2026-10-19.csv`: per-candidate source-page and attribution gate; blank fields mean not verified, not permission granted.
- `annotations_ARCHIVE_v0.1_NOT_FOR_TRAINING.json`: archived first-pass boxes for candidates 0002 and 0004; excluded from active training.
- [Annotation geometry audit tool](../../tools/audit_coconut_annotations.py): dependency-free checks for invalid normalized coordinates, overlapping boxes and image-border contact. Warnings require human review; the tool cannot identify missed coconuts or confirm box accuracy.
- [HSV baseline script](../../training/benchmark_hsv_baseline.py): reproducible OpenCV heuristic baseline; requires OpenCV and NumPy.
- `benchmark_report_v0.1.json`: measured run summary from 18 October 2026.

## Reproduce checks locally

Run the geometry audit:

```bash
python tools/audit_coconut_annotations.py --annotations data/review_batch_2026-10-18/annotations_ARCHIVE_v0.1_NOT_FOR_TRAINING.json --output data/review_batch_2026-10-18/annotation_geometry_audit_v0.1.json
```

Extract the candidate artifact so the `images/` directory contains the original image files, then run the HSV smoke test:

```bash
python training/benchmark_hsv_baseline.py --images-dir /path/to/extracted/images --annotations data/review_batch_2026-10-18/annotations_ARCHIVE_v0.1_NOT_FOR_TRAINING.json --output benchmark_report.json
```

Before training a learned detector: independently review every label, complete source-page licence/credit checks for every included image, annotate more independent orchard scenes, group by source/tree/session, and create a leakage-safe frozen test split. Keep downloaded images and weights out of Git unless distribution rights are explicitly confirmed.
