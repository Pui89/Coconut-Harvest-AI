# Coconut Palm Height Metadata and Label-Review Protocol

## Purpose

Record evidence-backed coconut-palm height labels for research and evaluation. This protocol is a data-collection plan, not a claim that the repository already contains a verified 0–30 m dataset.

## Height bands

Use these bins only after recording a measured or otherwise defensible numeric height:

- H1: 0–5 m (include 5.0 m)
- H2: >5–10 m (include 10.0 m)
- H3: >10–15 m (include 15.0 m)
- H4: >15–20 m (include 20.0 m)
- H5: >20–25 m (include 25.0 m)
- H6: >25–30 m (include 30.0 m)

If height is unknown, set `height_m` blank and `height_status=unverified`. Do not infer metres from visual appearance, perspective, or image dimensions. If a height is outside 0–30 m, preserve the measured value and mark it out-of-range for this planned evaluation rather than forcing it into a band.

## Minimum record requirements

1. **Image provenance:** Record source URL, title, creator, exact licence and licence URL. Confirm that the licence permits the intended reuse before copying an image into the dataset. A paper being open access does not automatically mean every associated image or dataset can be redistributed.
2. **Integrity:** Record the downloaded file's SHA-256 hash after download. Keep the original file unchanged; store resized/annotated derivatives separately.
3. **Tree-height evidence:** Prefer a field measurement with method, date and evidence record. Accept a published height only when the source clearly links that measurement to the pictured tree or sample. Record method and evidence URL. A species-level typical height is not an individual-tree label.
4. **Identity and grouping:** Use stable `tree_id`, `orchard_id`, and `session_id` values where known. Do not invent IDs when identity is unknown.
5. **Review:** Keep `height_status` as `unverified`, `provisional`, or `verified`. A second reviewer should check the source and units before a label is verified. Record fruit-annotation review separately in `annotation_status`.
6. **Splits:** Assign train/validation/test by tree, orchard, capture session, or source group—not by randomly splitting near-duplicate images. Images from the same tree or burst must not leak across splits.
7. **Missingness:** Use blank numeric fields for unknown measurements, not 0. Use notes to explain uncertainty or exclusions.

## Suggested controlled values

- `height_status`: `unverified`, `provisional`, `verified`, `out_of_range`
- `height_method`: `field_tape`, `laser_rangefinder`, `survey_or_point_cloud`, `published_measurement`, `other`
- `image_quality_review`: `pending`, `pass`, `fail`
- `annotation_status`: `not_started`, `draft`, `reviewed`, `rejected`
- `split`: `unassigned`, `train`, `validation`, `test`, `excluded`

## Evaluation safeguards

- Report the number of unique trees and images in each height band, plus missing/unverified labels.
- Report detection metrics per height band only where the test set has enough independently sourced examples; publish counts alongside every metric.
- Keep fruit maturity labels separate from palm-height labels.
- Detection performance does not prove that a robot can reach, cut, catch, or safely harvest fruit at that height. Those require separate mechanical and field validation.
- Do not claim full 0–30 m coverage until eligible, reviewed examples actually exist across the bands.

## Files

- CSV schema/template: [`data/height_metadata_template.csv`](../data/height_metadata_template.csv)
- Project overview and height-stratified plan: [README section](../README.md#real-palm-height-dataset-labels-training-and-test-plan)
