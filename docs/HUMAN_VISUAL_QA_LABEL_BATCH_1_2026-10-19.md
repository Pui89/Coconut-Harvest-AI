# Human Visual QA — Coconut Label Batch 1

**Review date:** 19 October 2026  
**Reviewer:** visual review performed from the archived `coconut-image-candidates` GitHub Actions artifact (run `39092214196`)  
**Scope:** the two existing first-pass labelled images only. This is a visual QA record, not an independent second annotator certification.

## Decision summary

| Image | Decision | Why | Required action |
|---|---|---|---|
| `0002_1280px-Fresh_coconuts.jpg` | **Keep image; revise labels before training** | Useful close-up cluster with clear fruit shapes, but dense overlap and partial occlusion make boundaries ambiguous. | Redraw each fruit box tightly and independently; check every visible fruit against the annotation policy. |
| `0004_1280px-Cocos_nucifera_003.jpg` | **Keep image; revise labels before training** | Useful overlapping green coconuts and includes truncated fruit at the right image edge. Existing boxes have obvious excess/background and overlap neighbouring fruit. | Tighten boxes around individual fruit; explicitly apply the truncated-object policy to the right-edge fruit and lower fruit cut by the bottom edge. |

Neither image is rejected. Neither image is approved as training-ready. The original annotations remain unchanged in `annotations_v0.1.json` because this review did not produce a verified replacement annotation file with every object independently checked.

## Image 0002 — visual findings

- The nine boxes cover the main cluster but do not yet provide consistently tight fruit boundaries.
- Several boxes overlap across adjacent coconuts. Some overlap is expected when fruit overlap in the scene, but box overlap alone cannot establish whether the labels are correct.
- The lower-left fruit is partly occluded by foreground plant material. The visible coconut should be boxed according to the project's chosen visible-extent policy, not around the occluding debris.
- The upper central fruit and the right-side fruit require a second boundary pass so stems, branches, and neighbouring fruit are not unnecessarily included.
- Check for small/background coconuts near the upper-left cluster. Add boxes only when an annotator can distinguish an individual fruit confidently; do not guess at tiny ambiguous shapes.

**Disposition:** retain image for label correction. Current 9-box labels are provisional.

## Image 0004 — visual findings

- The left and central foreground coconuts are individually visible, but the existing boxes are broad and include unnecessary surrounding pixels.
- The right-side large coconut is partly obscured by stems and nearby structures; its box needs a tighter visible-fruit boundary.
- The far-right coconut is cut by the image boundary. It needs a documented consistent policy: either label visible truncated fruit and mark truncation in metadata, or exclude such instances consistently.
- Two lower coconuts are cut by the bottom edge. Their boxes should follow the same truncation policy and should not extend beyond image coordinates.
- Review the partially hidden fruit behind the foreground cluster. Include it only if the dataset policy defines a minimum visible extent and the fruit can be identified confidently.

**Disposition:** retain image for label correction. Current 6-box labels are provisional.

## Dataset and evaluation gate

1. Adopt one written policy for visible extent, occlusion, truncation at image edges, and ambiguous fruit.
2. Revise both images and have a second person independently check the revised labels if possible.
3. Record reviewer, review date, label version, and a reason for each changed/added/removed box.
4. Keep source/attribution clearance as a separate gate; visual suitability does not grant reuse rights.
5. Do not use these two images as a train/validation/test split or report generalization from them. The existing HSV heuristic result is a failed baseline only, not evidence about a learned detector.
6. Collect and label more independent orchard scenes, then split by tree/source/capture session before training a detector.

## Evidence and limits

The visual review used the two JPEGs stored in the temporary Actions artifact, not a newly downloaded full-resolution copy. It confirms that the labels need revision but does not certify exhaustive object recall, independent annotator agreement, or real-world detector performance. No learned model was trained in this review.

Related files:
- [First-pass annotations](../data/review_batch_2026-10-18/annotations_v0.1.json)
- [Geometry audit](../data/review_batch_2026-10-18/annotation_geometry_audit_v0.1.json)
- [Source-rights audit](../data/review_batch_2026-10-18/source_rights_audit_2026-10-19.csv)
- [Dataset QA gate](DATASET_QA_GATE_2026-10-19.md)
