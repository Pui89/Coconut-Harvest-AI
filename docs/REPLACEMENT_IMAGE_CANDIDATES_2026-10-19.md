# Replacement coconut image candidates — 19 October 2026

## Decision

Use two new source images as replacements for the two difficult first-pass annotations in candidate 0002 and candidate 0004. Keep the old images and v0.1 labels for audit traceability, but do not spend the next annotation pass repairing those two labels. The new records are candidates 0031 and 0032 in `data/review_batch_2026-10-18/source_rights_audit_2026-10-19.csv`.

## New candidate 0031

- **File:** Coconuts in coconut tree.jpg
- **Source page:** https://commons.wikimedia.org/wiki/File:Coconuts_in_coconut_tree.jpg
- **Author:** Tanzeemfsugtvm
- **Licence shown:** CC BY-SA 3.0
- **Original dimensions reported by Commons:** 4160 × 3120
- **Initial visual screening:** the preview shows a large palm canopy with strong backlighting; many fruit targets are small and dark against the sky. Treat as a possible hard-case image, not automatically as a clean starter image. Full-resolution review is required before annotation.
- **Attribution/licence:** retain the author credit, link to the source page and https://creativecommons.org/licenses/by-sa/3.0/; indicate any changes.

## New candidate 0032

- **File:** Coconut in Coconut Tree.jpg
- **Source page:** https://commons.wikimedia.org/wiki/File:Coconut_in_Coconut_Tree.jpg
- **Author:** Sarmi~Kili
- **Licence shown:** CC BY-SA 4.0
- **Original dimensions reported by Commons:** 5184 × 3456
- **Initial visual screening:** the preview shows a closer fruit cluster, but coconuts overlap one another and are partly occluded by fronds. It may be more useful than 0031 for a first annotation pass, but boundaries must be judged at full resolution; do not invent boxes for ambiguous fruit.
- **Attribution/licence:** retain the author credit, link to the source page and https://creativecommons.org/licenses/by-sa/4.0/; indicate any changes.

## Reproducible download helper

The repository now includes `scripts/download_replacement_coconut_images.py`. Run it from the repository root with Python 3. It downloads the two original Commons files to `data/review_batch_2026-10-19/images/` and verifies their published SHA-1 checksums before saving. The script does not create annotations or mark images as training-approved.

## Required next steps

1. Run the download helper in an environment with internet access; verify it reports `OK` for both files and preserves the expected SHA-1 hashes.
2. Open each downloaded image at full resolution. Reject or defer a candidate if individual fruit boundaries cannot be labelled consistently.
3. Annotate only clearly distinguishable fruits with tight boxes and apply one consistent rule for occlusion and image-edge truncation.
4. Save new annotation records under new candidate IDs; do not overwrite the old v0.1 labels.
5. Record annotation reviewer, review date, image hashes and source/credit/licence details. Include only reviewed images in the dataset builder and run the leakage audit.

## Status boundary

The Commons source pages and stated licences were checked on 19 October 2026. The image previews have received an initial visual screen, which identified substantial backlighting in 0031 and overlap/occlusion in 0032. **Neither image has passed full-resolution annotation QA.** This document does not claim that the image binaries have been downloaded into the repository, that labels have been created, or that either image is training-approved. Both candidates remain `not_yet_annotated` and `blocked` for training until the steps above are complete.
