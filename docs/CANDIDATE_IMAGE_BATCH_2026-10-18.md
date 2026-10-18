# Candidate-image batch 1 — 18 October 2026

## Provenance and reproducibility

- Collection run: [GitHub Actions run 39092214196](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39092214196)
- Artifact: `coconut-image-candidates` (30 downloaded images, review gallery, provenance CSV and collection summary; 7-day retention)
- Source: Wikimedia Commons; collector only accepts licence labels matching CC0, Public Domain, CC BY or CC BY-SA and records source/licence metadata.
- The workflow log records some individual HTTP 429 rate-limit failures. It nevertheless downloaded 30 candidate files.
- This batch is **not a labelled dataset**. The image files have not been annotated, the licence metadata has not been independently verified image-by-image, and no model was trained or evaluated.

## First-pass visual triage

The following is a rough relevance screen based on the generated contact sheet, not a formal image annotation or a substitute for opening each original image. The numbers correspond to the `images/0001_...` prefixes inside the artifact.

| Candidate IDs | First-pass category | Suggested handling |
|---|---|---|
| 0001, 0002, 0004 | Clear coconut/palm-fruit candidates in the thumbnail view | Prioritize for source/licence review; annotate only visible fruit instances |
| 0005, 0006, 0008, 0009, 0010, 0012, 0013, 0015 | Harvesting/climbing or palm-related scenes; target visibility varies | Inspect at full resolution; keep only if the intended target and scene are clear |
| 0003 | Harvested coconuts / coconut products rather than a clear attached-fruit target | Possible negative/domain-context sample; do not treat as attached-fruit detection evidence |
| 0011, 0014, 0016, 0017, 0019–0022, 0025–0028, 0030 | Plantation, palm-tree or processing context; fruit visibility may be weak or absent | Inspect for actual visible target fruit; use as negative examples only if carefully reviewed and appropriate |
| 0007 | Harvest tool, not a coconut-fruit target image | Exclude from positive fruit-box training; retain only if a separate tool class is intentionally defined |
| 0018 | Map/plantation record rather than an ordinary fruit image | Exclude from the coconut-fruit detector dataset |
| 0023, 0024 | Young plants/seedling context rather than visible mature fruit | Exclude from positive fruit-box training |
| 0029 | Unrelated racecourse scene in the thumbnail view | Exclude from this task |

## Required before training

1. Download the artifact and inspect all 30 original files, not only the contact sheet.
2. Open each original Commons file page and confirm the current licence, attribution requirements, and intended reuse.
3. Reject irrelevant images, broken/low-quality images, and images where the target is too ambiguous to label.
4. Annotate every clearly visible target coconut under one consistent bounding-box policy; use an empty label only for a verified negative image.
5. Group related images by source/tree/session before creating separate train, validation and test splits. Do not place related frames or near-duplicates across splits.
6. Run the dataset builder and leakage audit; inspect the generated manifest and sample visualizations before training.

**Research integrity:** this triage is only an initial human-readable screening aid. It does not establish annotation quality, licence clearance, detector accuracy, localization performance, robot safety, or physical harvesting capability.


## Follow-up integrity check — 18 October 2026

The workflow artifact was retrieved for a first-pass technical inspection in this session.

- 30 image files were present and readable: 29 JPEG files and 1 PNG file.
- Image dimensions range from 476×458 to 1280×2773 pixels.
- A byte-level SHA-256 check found no exact duplicate files in this batch. This does not rule out visually similar or near-duplicate images.
- A contact sheet was visually reviewed. It confirms the batch mixes likely attached-fruit candidates with harvesting scenes, plantation context, seedlings, a tool image, a graphic/collage and an unrelated racecourse image.
- The most promising first-pass attached-fruit candidates remain IDs 0001, 0002 and 0004; other scenes require full-resolution inspection before deciding whether any visible fruit can be labelled reliably.

**Important boundary:** this check is not a full-resolution annotation review, image-by-image licence verification, near-duplicate audit, or dataset acceptance. Every image remains unreviewed/unlabelled for training until those checks are completed. The Actions artifact expires on 25 October 2026; download it from the linked run if you need a durable local copy.


## Full-resolution and source-page check — priority candidates

I opened the original-resolution artifact files for IDs 0001, 0002 and 0004 and checked their Wikimedia Commons source pages on 18 October 2026.

| ID | Visual suitability for attached-coconut detection | Commons page's stated licence | Credit shown on source page | Decision |
|---|---|---|---|---|
| 0001 | Fruits are present but relatively small and partly obscured by fronds; useful as a harder/occluded example if boxes can be drawn consistently | CC BY-SA 3.0 | Muminur Rahman | **Provisional candidate**; annotation and attribution record still required |
| 0002 | Close-up cluster of attached coconuts; several fruit boundaries are visible | CC BY-SA 4.0 | Siva301in | **Strong provisional positive candidate**; annotate each clearly separable fruit under one policy |
| 0004 | Close-up cluster of attached coconuts; multiple fruit boundaries visible despite overlap and strong shadows | CC BY-SA 3.0 and GFDL 1.2-or-later (dual licence displayed) | H. Zell | **Strong provisional positive candidate**; annotate visible instances and retain the selected licence/credit details |

Source pages checked:
- [0001 — Coconuts on Tree.jpg](https://commons.wikimedia.org/wiki/File:Coconuts_on_Tree.jpg)
- [0002 — Fresh coconuts.jpg](https://commons.wikimedia.org/wiki/File:Fresh_coconuts.jpg)
- [0004 — Cocos nucifera 003.jpg](https://commons.wikimedia.org/wiki/File:Cocos_nucifera_003.jpg)

These three source pages displayed the stated licences and attribution details when checked. This is not a legal opinion and does not clear the other 27 images. Preserve source URLs, author credit, licence URL and any changes with the dataset; do not assume the whole batch is approved.

**Still pending for these three:** write and visually inspect bounding-box labels, confirm the precise class definition, retain the provenance metadata, and include them only after the project’s dataset audit passes. No model has been trained from them.


## Follow-up — full-batch visual triage and first measured baseline (18 October 2026)

This update supersedes the earlier wording that all candidates remained visually unreviewed. The downloaded original-resolution files were inspected as a full 30-image contact sheet, and every candidate now has a conservative triage decision in [the review ledger](../data/review_batch_2026-10-18/candidate_review_2026-10-18.csv). This is a visual triage decision, not a complete licence review.

- First-pass labels were created for IDs 0002 (9 boxes) and 0004 (6 boxes); see [annotations v0.1](../data/review_batch_2026-10-18/annotations_v0.1.json). Labels are single-pass and need independent QA.
- The fixed OpenCV HSV-contour heuristic was run on these same two images: 20 predictions, 15 reference boxes, 0 matches at IoU ≥ 0.50, precision 0.000, recall 0.000, F1 0.000, mean CPU runtime 15.12 ms/image. This is a failed exploratory heuristic baseline, not a learned AI detector result.
- Source pages were checked for IDs 0001, 0002 and 0004 only. The other 27 image pages have not been independently checked in this session and are not cleared for inclusion in a distributable training set.
- The two labelled images do not form a valid train/validation/test dataset. There is no trained detector benchmark or held-out generalization result yet.

See [batch README and reproduction steps](../data/review_batch_2026-10-18/README.md). The temporary source artifact still expires on 25 October 2026.
