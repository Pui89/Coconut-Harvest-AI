# Coconut Harvest AI — Annotation Protocol v1

**Status:** Proposed protocol; not yet applied to image files.
**Scope:** Candidate images WMC-01 and WMC-02 in Real-Image Test Set v1.
**Purpose:** Define a reproducible human-annotation and independent-QA process before any model training.

## 1. Evidence and permission gates
- Preserve each source page URL, creator, source title, license, access date, and required attribution.
- After authorized acquisition, record exact downloaded-file SHA-256, byte size, pixel dimensions, and file format.
- Do not treat a preview, filename, uploader caption, or visual colour alone as biological maturity ground truth.
- Keep training_approved=false until image rights, image integrity, annotation, and independent QA gates pass.
- Do not download, redistribute, modify, or train on an asset unless acquisition approval and license requirements are satisfied.

## 2. Image-level annotation fields
| Field | Allowed values / rule |
|---|---|
| image_id | Stable ID from test-set manifest |
| source_id | Wikimedia file-page ID / URL |
| source_license | Exact license and version shown on source page |
| file_sha256 | Hash of acquired original; blank until acquired |
| image_width, image_height | Native pixel dimensions |
| scene_type | on_tree / harvested / unknown |
| visibility | clear / partial_occlusion / heavy_occlusion |
| annotator_id | Non-sensitive reviewer identifier |
| annotation_version | Semantic version |
| review_status | draft / submitted / qa_pass / qa_revise / rejected |

## 3. Object-level detection labels
- Draw one tight bounding box per visually identifiable whole coconut fruit.
- Include fruit husk; exclude leaves, stems, trunk, and background.
- Use pixel coordinates with origin at top-left: x_min, y_min, x_max, y_max.
- Require 0 <= x_min < x_max <= image_width and 0 <= y_min < y_max <= image_height.
- Do not create a box when the object cannot be distinguished from overlapping foliage or another fruit.
- For partial fruit, annotate only when at least 50% of its visible outline can be identified; otherwise mark ignore_region and explain.
- Do not split one fruit into multiple boxes or merge multiple fruits into one box.
- Record occlusion as none / partial / heavy and truncation as true / false.

## 4. Biological maturity labels
Allowed labels: young_green, mature_green, yellow, brown, unknown.
- unknown is mandatory when evidence is insufficient.
- Colour is an appearance attribute, not sufficient proof of biological maturity.
- A yellow cultivar or yellow-green husk must not automatically be labelled yellow maturity.
- A source caption such as “mature” or “ready for harvest” is supporting metadata, not independent ground truth.
- Assign maturity only with documented expert/horticultural review and supporting evidence such as cultivar, harvest age/flowering date, fruit size, husk condition, endosperm/meat development, or other validated local criteria.
- If evidence is absent, retain unknown even if a detector box is accepted.

## 5. Independent QA
A second reviewer, not the original annotator, checks:
1. Correct fruit count and no duplicate/missed objects.
2. Box boundaries and object separation under overlap/occlusion.
3. Ignore-region decisions and visibility tags.
4. Maturity evidence and consistency; colour-only labels fail QA.
5. Source/license/attribution metadata and file-hash linkage.

Record per-image results: objects_reviewed, boxes_accepted, boxes_corrected, objects_added, objects_removed, maturity_labels_accepted, maturity_labels_changed, qa_reviewer, qa_date, and qa_notes.
Resolve disagreements by a third qualified reviewer. Preserve original annotation and correction history; never silently overwrite.

## 6. Dataset split and leakage controls
- Split by source image and, where possible, by tree/orchard/session/cultivar—not by crops from the same source image.
- Keep near-duplicate frames and crops in the same split.
- Do not create train/validation/test splits until there are sufficient independent source groups.
- Report class counts, unknown-label counts, occlusion distribution, and split provenance before training.

## 7. Model evaluation gate
For detection, report precision, recall, F1, and mAP with IoU threshold(s), confidence threshold, class mapping, split definition, and sample counts. For maturity classification, evaluate only independently verified maturity labels; report a confusion matrix and per-class precision/recall/F1. Include CPU hardware, runtime environment, model version, and reproducible command/configuration. Do not claim field performance from this small candidate set.

## 8. Current candidate disposition
| Candidate | Detection annotation | Maturity label | Training approval |
|---|---|---|---|
| WMC-01 | Pending original-file QA | unknown | false |
| WMC-02 | Pending original-file QA | unknown | false |

**Current boundary:** This protocol does not assert that either candidate has been downloaded, fully inspected, annotated, independently approved, or used for training.