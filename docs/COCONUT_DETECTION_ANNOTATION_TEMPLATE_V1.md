# Coconut Detection Annotation Template v1

**Date:** 17 November 2026  
**Scope:** WMC-01 and WMC-02 candidate images only.  
**Status:** Schema and blank template only; no image annotations have been created.

## 1. Purpose

Provide a consistent, reviewable format for annotating visible coconut instances for object detection. Detection labels and biological maturity labels are separate tasks. A fruit can be detected even when its maturity is unknown.

## 2. Annotation unit

One row in `data/coconut_detection_annotations_v1.csv` represents one visible coconut instance in one source image.

- Use a tight axis-aligned bounding box around the visible fruit pixels only.
- Do not draw boxes around hidden or guessed portions of an occluded fruit.
- If two fruits overlap, annotate separate instances only when each visible instance can be distinguished.
- Do not annotate leaves, trunks, flowers, or background as coconut objects.
- If an instance cannot be distinguished confidently, record it in the review notes rather than inventing a box.

## 3. Coordinate convention

Use pixel coordinates in the verified original image coordinate system:

- `x_min`, `y_min`: top-left corner.
- `x_max`, `y_max`: bottom-right corner.
- Require `0 <= x_min < x_max <= image_width` and `0 <= y_min < y_max <= image_height`.
- Record image width and height for every annotation row.
- Do not resize or recompress the source image before annotation. If a tool uses a resized display, map coordinates back to original pixels and document the transform.

## 4. Required fields

| Field | Rule |
|---|---|
| image_id | Stable source ID, e.g. WMC-01 |
| source_filename | Exact acquired filename |
| source_url | Original source URL |
| license | Source-page license |
| sha256 | SHA-256 of acquired original bytes; blank until verified |
| image_width / image_height | Verified original dimensions |
| object_id | Unique within image, e.g. WMC-01-001 |
| class_name | `coconut` |
| x_min / y_min / x_max / y_max | Visible-instance pixel box |
| occlusion | `none`, `partial`, or `heavy` |
| truncation | `yes` or `no` (fruit cut by image boundary) |
| visibility | `clear`, `limited`, or `unusable` |
| maturity_label | `young_green`, `mature_green`, `yellow`, `brown`, or `unknown` |
| maturity_evidence | Human/field evidence supporting maturity; never colour alone |
| annotator_id | Reviewer-safe identifier, not personal contact details |
| annotation_status | `draft`, `qa_pass`, `qa_reject`, or `needs_review` |
| reviewer_id | Independent reviewer identifier, if reviewed |
| review_notes | Ambiguity, disagreement, or reason for rejection |

## 5. Maturity-label policy

- Default `maturity_label=unknown`.
- Husk colour alone is insufficient to establish biological maturity; cultivar, harvest age, intended use, and other agronomic evidence matter.
- Do not infer maturity from a Commons caption such as “mature” or “ready for harvest” without independent ground truth.
- If no reliable maturity evidence exists, keep `unknown` and continue detection annotation if the fruit instance is visually identifiable.

## 6. Independent QA and dataset controls

1. A second annotator/reviewer checks every box and all metadata.
2. Record disagreements; do not silently overwrite the first annotation.
3. Check box bounds, duplicate object IDs, missed visible fruit, and impossible overlaps.
4. Split train/validation/test by source photograph or acquisition session, never by crops from the same original image across splits.
5. Keep source images outside the public repository unless publication is separately approved.
6. Training approval remains false until original-byte integrity, annotation QA, rights review, and split integrity are complete.

## 7. Current gate

- WMC-01 and WMC-02 are detection candidates only.
- Original-byte local acquisition and SHA-256: pending.
- Annotation rows: none.
- Biological maturity labels: unknown.
- Independent QA: not started.
- Model training/evaluation: not approved.
