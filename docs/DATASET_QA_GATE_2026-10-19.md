# Coconut Harvest AI — dataset QA gate

**Updated:** 19 October 2026  
**Scope:** Candidate batch collected by GitHub Actions run [39092214196](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39092214196). This document records the gate for promoting candidate images into a research dataset; it is not a claim that the gate has passed.

## Current batch snapshot

- Candidate batch: 30 images; temporary Actions artifact is preserved as a ZIP backup outside the Git repository. Original artifact expiry is 25 October 2026.
- Candidate review ledger: `data/review_batch_2026-10-18/candidate_review_2026-10-18.csv`.
- First-pass annotation file: `data/review_batch_2026-10-18/annotations_ARCHIVE_v0.1_NOT_FOR_TRAINING.json`.
- Historical labels: 15 first-pass boxes across candidates 0002 and 0004. Both images are now excluded from active training candidates because their annotation QA is unresolved. The original JSON is retained only for audit traceability; do not train on it.
- Source pages checked for new replacements 0033 and 0034: both have recorded creator, CC BY-SA 3.0 licence, and source URLs. The files were downloaded and SHA-1 verified in GitHub Actions run [39235348989](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39235348989). They remain unlabelled and are not training-approved. Candidates 0002 and 0004 are excluded from active training; their old labels are historical only.
- Candidate 0010 was inspected at full resolution and excluded from attached-fruit detection because the visible coconuts are harvested fruit, not attached targets.
- Replacement candidates 0031 and 0032 were reviewed from separate Actions artifact run [39233532723](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39233532723). Candidate 0031 is deferred due to severe backlighting; candidate 0032 is an annotation priority but remains unlabelled. See [replacement candidate review](REPLACEMENT_IMAGE_CANDIDATES_2026-10-19.md).
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

## Follow-up review — 19 October 2026

- **Candidate 0033:** do not use as the preferred first replacement; the full-resolution image is strongly shadowed and individual boundaries are difficult to distinguish.
- **Candidate 0032:** selected as the clearer replacement candidate for further review. Source page: https://commons.wikimedia.org/wiki/File:Coconut_in_Coconut_Tree.jpg; author Sarmi~Kili; licence CC BY-SA 4.0; downloaded SHA-1 matches the source-page checksum. It is still unlabelled and not training-approved.
- **Candidate 0034:** a provisional local annotation overlay was generated. Geometry checks report valid normalized coordinates, one border-touching box, and no box-pair overlap at IoU >= 0.15. This is only a geometry check; missed fruit, loose boundaries and incorrect fruit assignments remain possible. Independent visual review is outstanding.
- **Data handling:** the draft annotation and overlay remain in a temporary local review bundle and have not been committed as training data.

## Current decision for this batch

| Candidate | Current status | Required next action |
|---|---|---|
| 0001 | Provisional positive; source page checked; not labelled | Re-check attribution/licence record, then label only if useful and unambiguous |
| 0002 | Excluded from active training; 9 old boxes retained for audit | Do not use the v0.1 labels for training |
| 0004 | Excluded from active training; 6 old boxes retained for audit | Do not use the v0.1 labels for training |
| 0033 | New close-up cluster; source/licence checked; unlabelled | Annotate conservatively, then independent box review |
| 0034 | New green cluster; source/licence checked; unlabelled | Annotate conservatively, then independent box review |
| 0010 | Excluded after full-resolution review; harvested fruit are not attached targets | Keep excluded from attached-coconut detection |
| 0014 | Provisional positive; source page checked; CC BY 3.0; unlabelled | Annotate only individually identifiable attached fruit; second review required |
| Other 25 | Excluded from this detection batch, subject to documented re-review | Do not include as training examples unless a documented re-review changes the decision |

## Baseline interpretation

The 18 October HSV-contour smoke test scored 0 true positives at IoU >= 0.50 on the same two images used for first-pass labels. This is a failed, in-sample, non-ML heuristic baseline. It is not evidence that a trained detector fails or succeeds, and it is not a held-out benchmark. Do not train a learned detector on the current two-image sample.

## Next actions

1. Keep the ZIP backup and provenance records; do not commit candidate image files to the public repository.
2. Do not reactivate candidates 0002 and 0004. Annotate replacement candidates 0033 and 0034 and obtain independent label QA before promotion.
3. Collect more independently sourced, permitted orchard images, including genuine negative images and varied lighting, distance, cultivar, occlusion and backgrounds.
4. Record source/tree/session groups before annotation grows large.
5. Build a dataset only after every included image passes the gate; run both dataset audits and inspect generated label galleries before training.
6. Publish model metrics only after a real trained checkpoint is evaluated on a frozen, group-separated test set.

## Safety and licensing

A public web image is not automatically reusable. If the source page, creator, licence terms or attribution cannot be verified, exclude the image from a distributable training dataset. Keep the dataset local and do not upload images or model weights to this repository unless distribution rights are explicitly confirmed. Dataset approval does not prove robot safety or physical harvesting capability.
