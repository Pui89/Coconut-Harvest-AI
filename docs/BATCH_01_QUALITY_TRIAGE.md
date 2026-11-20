# Batch 01 — Preliminary Visual Quality Triage

**Run:** [GitHub Actions run 44794101486](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/44794101486)  
**Artifact:** `coconut-real-image-review-batch-1`  
**Scope:** 30 downloaded Wikimedia Commons candidate images  
**Review type:** Preliminary visual screening from the generated contact sheet; not a rights, agronomy, annotation, or training approval.

## Screening result

| Preliminary bucket | Count | Candidate IDs | Meaning |
|---|---:|---|---|
| Priority for human per-fruit review | 7 | 1–6, 8 | Inspect original files at full resolution |
| Product-reference only | 1 | 7 | Cut-open/product imagery, not an on-tree detection sample |
| Harvest context / tool reference | 12 | 9–20 | Operational context, not core fruit-level detection |
| Orchard context only | 4 | 25–28 | Scene context, not individual fruit targets |
| Exclude from fruit detection | 5 | 21–23, 29–30 | Irrelevant, map/location-like, or seedling imagery |
| Historical processing context | 1 | 24 | Historical plantation/processing context |

## Important boundaries

- This is a visual triage of the contact sheet only. It does not replace inspection of every original image.
- A candidate marked `PRIORITY_REVIEW` does not mean its license has been legally verified or that it is approved for reuse.
- The provenance manifest records license metadata and attribution information, but every file page and applicable license terms still require human rights review.
- Exterior colour in a photograph cannot establish internal water quality, meat thickness, embryo/haustorium status, seed viability, or suitability for coconut milk, copra, or oil.
- No maturity class (Young Green, Mature Green, Yellow, Brown) is assigned by this triage.
- No fruit bounding boxes, instance masks, or agronomic labels have been created.
- All rows remain `NOT_REVIEWED` for rights and agronomic review, and `training_approved=false`.

## Recommended next gate

1. Human reviewer opens the original file and its Commons page for candidates 1–6 and 8.
2. Record image quality, visible fruit count, occlusion, fruit separability, camera viewpoint, and whether the fruit is attached to the palm.
3. Verify license, author, attribution requirements, and share-alike obligations before any reuse.
4. Agronomy reviewer separately determines whether any maturity or product-suitability label is supportable. If not, use `UNKNOWN` or `REVIEW_REQUIRED`.
5. Only after both rights and annotation gates pass may a candidate be considered for a training split.

## Status

`PRELIMINARY_VISUAL_TRIAGE_ONLY` — the original batch summary remains unchanged: 0 rights-approved, 0 human-reviewed, and 0 training-approved images.
