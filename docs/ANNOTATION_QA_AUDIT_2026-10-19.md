# Annotation QA audit — 19 October 2026

## Scope and conclusion

I retrieved the original candidate-image artifact and overlaid the existing first-pass boxes on both labelled images (0002 and 0004). This is an initial visual and geometry audit, not independent expert annotation. **The labels are not approved for training yet.** The existing annotations remain unchanged until disputed fruit boundaries and partial-fruit rules are resolved.

- Image 0002: 9 first-pass boxes.
- Image 0004: 6 first-pass boxes.
- Total: 15 boxes across only 2 source images.
- The boxes are normalized `x, y, width, height` values in `annotations_v0.1.json`.
- No original image pixels or labels have been silently changed by this audit.

## Findings from the box overlays

### Candidate 0002 — `Fresh_coconuts.jpg`

- Several boxes overlap neighbouring fruit regions; the box pairs (2, 3) and (3, 5) have geometric IoU above 0.15. This is a review flag, not proof that the annotations are wrong: touching/overlapping coconuts can legitimately have overlapping rectangles.
- Some rectangles appear loose relative to the visible fruit silhouettes and cross into adjacent fruit, fronds, or background. Recheck each boundary at full resolution.
- The upper and lower parts of the cluster are visually crowded. Recount every distinct visible coconut, including partially occluded fruit, and document any intentionally unlabelled instances.
- Box 9 covers a fruit near the top of the frame. The annotation policy must state whether truncated fruit at image borders are included and how their boxes are drawn.
- Decision: **needs independent box-by-box review; do not promote yet**.

### Candidate 0004 — `Cocos_nucifera_003.jpg`

- The central cluster is heavily occluded by stems/fronds and shadow. Review each box against one individual fruit rather than the whole visible cluster.
- Box 4 touches the right image boundary; boxes 5 and 6 touch the bottom boundary. These may represent truncated fruits, but the dataset needs one consistent rule for border-truncated instances.
- Recheck whether every clearly separable visible fruit has a box and whether any box includes substantial neighbouring fruit or background.
- Decision: **needs independent box-by-box review; do not promote yet**.

## Geometry checks

Run the repository's dependency-free audit:

```bash
python tools/audit_coconut_annotations.py \
  --annotations data/review_batch_2026-10-18/annotations_v0.1.json \
  --output data/review_batch_2026-10-18/annotation_geometry_audit_v0.1.json
```

The audit checks normalized coordinates, positive width/height, boxes outside image bounds, pairs with IoU at or above 0.15, and boxes touching image borders. An overlap or border warning is for human review; it is not automatically a label error.

## Required annotation policy before v0.2

1. Define one class precisely: a single visible coconut fruit, not a whole bunch, husk cluster, leaf, or stem.
2. Draw a tight rectangle around the visible extent of each individually distinguishable fruit; do not expand a box to include adjacent fruits or foliage.
3. Decide and document how to handle occluded and image-truncated fruit. Apply the same policy to every image.
4. Recount instances at full resolution and record ambiguous or unlabelled objects explicitly.
5. Have a second reviewer inspect all 15 boxes; record accepted/changed/rejected decisions and reasons.
6. Save corrected labels as a new version (for example `annotations_v0.2.json`); retain v0.1 unchanged for traceability.
7. Finish source-page licence and credit verification for every image selected for training, then run dataset and leakage audits.

## Release gate

**Current status: BLOCKED — independent annotation QA and per-image rights clearance are incomplete.** These two images are useful for developing the annotation process, but two images are not a valid train/validation/test dataset. No learned detector should be trained or reported as benchmarked from this batch yet.
