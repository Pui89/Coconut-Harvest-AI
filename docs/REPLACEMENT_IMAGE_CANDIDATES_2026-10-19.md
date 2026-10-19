# Replacement coconut image candidates — 19 October 2026

## Decision

Use two new source images as replacements for the two difficult first-pass annotations in candidate 0002 and candidate 0004. Keep the old images and v0.1 labels for audit traceability, but do not spend the next annotation pass repairing those two labels. The new records are candidates 0031 and 0032 in `data/review_batch_2026-10-18/source_rights_audit_2026-10-19.csv`.

## New candidate 0031

- **File:** Coconuts in coconut tree.jpg
- **Source page:** https://commons.wikimedia.org/wiki/File:Coconuts_in_coconut_tree.jpg
- **Author:** Tanzeemfsugtvm
- **Licence shown:** CC BY-SA 3.0
- **Original dimensions reported by Commons:** 4160 × 3120
- **Why selected:** high-resolution image showing coconuts on a tree; provides a new view from a different photographer.
- **Attribution/licence:** retain the author credit, link to the source page and https://creativecommons.org/licenses/by-sa/3.0/; indicate any changes.

## New candidate 0032

- **File:** Coconut in Coconut Tree.jpg
- **Source page:** https://commons.wikimedia.org/wiki/File:Coconut_in_Coconut_Tree.jpg
- **Author:** Sarmi~Kili
- **Licence shown:** CC BY-SA 4.0
- **Original dimensions reported by Commons:** 5184 × 3456
- **Why selected:** high-resolution coconut-tree image from a different photographer and source, adding visual diversity.
- **Attribution/licence:** retain the author credit, link to the source page and https://creativecommons.org/licenses/by-sa/4.0/; indicate any changes.

## Required next steps

1. Download the original-resolution files from their Commons pages into the local candidate-image folder; do not commit image binaries or datasets to Git.
2. Open each image at full resolution and confirm that individual coconuts are visible enough to label consistently. These are source-checked candidates, not yet approved annotations.
3. Annotate each clearly distinguishable fruit with a tight box and apply one consistent rule for occlusion and image-edge truncation.
4. Save new annotation records under new candidate IDs; do not overwrite the old v0.1 labels.
5. Record the image hashes and source/credit/licence details, then include only reviewed images in the dataset builder and run the leakage audit.

## Status boundary

The Commons source pages and stated licences were checked on 19 October 2026. This document does **not** claim that the image binaries have already been downloaded into the repository, that labels have been created, or that either image has passed annotation QA. Both new candidates remain `not_yet_annotated` and `blocked` for training until the steps above are complete.
