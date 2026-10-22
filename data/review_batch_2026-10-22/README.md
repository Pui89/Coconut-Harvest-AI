# AI-assisted coconut annotation draft — 22 October 2026

**Status: NOT human-QA-approved. NOT approved for model training or benchmark scoring.**

This draft contains eight candidate bounding boxes for the image below. I created these as a preliminary visual pass to reduce manual work, but overlapping fruit, foliage, and occlusion make the labels uncertain. Do not present them as verified ground truth.

- Image: `candidate_0032.jpg`
- Source page: https://commons.wikimedia.org/wiki/File:Coconut_in_Coconut_Tree.jpg
- Creator shown in the source metadata: Sarmi~Kili
- Licence shown in the fetched metadata: CC BY-SA 4.0
- Dimensions: 5184 × 3456
- Annotation file: `ai_annotation_draft_NOT_FOR_TRAINING.json`

## Required before use

1. Obtain the image from its source page and verify current attribution/licence terms.
2. Load `candidate_0032.jpg` in the offline annotator, then import this JSON.
3. Inspect every box at full resolution. Correct boundaries and add any clearly visible missed coconuts; remove false boxes.
4. Have an independent human review the labels and document that review.
5. Only then create a separately reviewed ground-truth CSV. This draft must not be used to claim detector accuracy.

This draft does not contain detector predictions, and it does not establish precision, recall, F1, or mAP.
