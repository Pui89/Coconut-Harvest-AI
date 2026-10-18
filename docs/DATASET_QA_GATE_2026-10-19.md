# Coconut Harvest AI — dataset QA gate

**Updated:** 19 October 2026  
**Scope:** Candidate batch collected by GitHub Actions run [39092214196](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39092214196). This document records the gate for promoting candidate images into a research dataset; it is not a claim that the gate has passed.

## Current batch snapshot

- Candidate batch: 30 images; temporary Actions artifact is preserved as a ZIP backup outside the Git repository. Original artifact expiry is 25 October 2026.
- Candidate review ledger: `data/review_batch_2026-10-18/candidate_review_2026-10-18.csv`.
- First-pass annotation file: `data/review_batch_2026-10-18/annotations_v0.1.json`.
- Current labels: 15 boxes across two images (9 on candidate 0002, 6 on candidate 0004). These are single-pass annotations and have not passed independent QA.
- Independently checked Commons source pages: candidates 0001, 0002 and 0004 only. That does not mean all three are approved for training: candidate 0001 remains provisional and unlabelled; candidates 0002 and 0004 remain provisional pending label review and full attribution/licence recording.
- Candidate 0010 and 0014 are potential positives but have not had source-page checks or annotations.
- The other candidates were excluded from this fruit-detection batch for domain/visibility reasons. Do not infer that their licences were independently verified.

## Promotion gate: every included image must pass

1. **File integrity:** file opens successfully; record filename, dimensions, byte size and SHA-256.
2. **Source and reuse rights:** save the original source-page URL, creator/credit line, exact licence/version, licence URL, retrieval date, and any attribution requirements. Independently check the page itself. Collector metadata alone is insufficient.
3. **Domain decision:** attached coconut fruit is visible enough to label for the target use case. Keep distant, ambiguous, processing-only, unrelated, or non-orchard images out of the positive set.
4. **Annotation QA:** label every clearly visible target according to a written policy; use tight, consistent boxes; do not guess hidden fruit. A second review must resolve missing targets, loose boxes, duplicate boxes and boundary errors. Record reviewer, date and decision.
5. **Group provenance:** assign a meaningful group identifier based on tree, orchard, capture session, video or known source grouping. Related images must stay in the same split.
6. **Dataset leakage checks:** check exact duplicates and, where possible, visually near-duplicates. Run the repository dataset and split audits after building.
7. **Visual inspection:** render the boxes over every included image, inspect positive and negative examples, and retain a QA decision log.
8. **Frozen split:** only create train/validation/test after enough independently sourced groups exist. Never weaken the group split just to make a two-image dataset trainable.

## Current decision for this batch

| Candidate | Current status | Required next action |
|---|---|---|
| 0001 | Provisional positive; source page checked; not labelled | Re-check attribution/licence record, then label only if useful and unambiguous |
| 0002 | Provisional positive; 9 first-pass boxes; source page checked | Independently review every box and complete source/credit record |
| 0004 | Provisional positive; 6 first-pass boxes; source page checked | Independently review every box and record the Commons page's displayed licence options accurately |
| 0010 | Potential positive; source page not checked; unlabelled | Verify source/licence first, then decide whether to annotate |
| 0014 | Potential positive; source page not checked; unlabelled | Verify source/licence first, then decide whether to annotate |
| Other 25 | Excluded from this detection batch | Do not include as training examples unless a documented re-review changes the decision |

## Baseline interpretation

The 18 October HSV-contour smoke test scored 0 true positives at IoU >= 0.50 on the same two images used for first-pass labels. This is a failed, in-sample, non-ML heuristic baseline. It is not evidence that a trained detector fails or succeeds, and it is not a held-out benchmark. Do not train a learned detector on the current two-image sample.

## Next actions

1. Keep the ZIP backup and provenance records; do not commit candidate image files to the public repository.
2. Finish licence/attribution review and independent label QA for candidates 0002 and 0004; then decide whether 0001, 0010 and 0014 merit inclusion.
3. Collect more independently sourced, permitted orchard images, including genuine negative images and varied lighting, distance, cultivar, occlusion and backgrounds.
4. Record source/tree/session groups before annotation grows large.
5. Build a dataset only after every included image passes the gate; run both dataset audits and inspect generated label galleries before training.
6. Publish model metrics only after a real trained checkpoint is evaluated on a frozen, group-separated test set.

## Safety and licensing

A public web image is not automatically reusable. If the source page, creator, licence terms or attribution cannot be verified, exclude the image from a distributable training dataset. Keep the dataset local and do not upload images or model weights to this repository unless distribution rights are explicitly confirmed. Dataset approval does not prove robot safety or physical harvesting capability.
