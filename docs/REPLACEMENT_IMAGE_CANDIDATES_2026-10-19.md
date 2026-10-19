# Replacement coconut image candidates — reviewed 19 October 2026

## Decision after full-resolution inspection

Do not use candidate 0031 as one of the two clean starter replacements. It has severe backlighting; most fruit are small, dark and partly hidden by the canopy. Keep it only as a later difficult-light evaluation candidate.

Prioritize these two images for the next annotation pass:
- **Candidate 0032 — Coconut in Coconut Tree.jpg:** best of the new replacement pair for annotation practice. A clear cluster is visible, although several fruit overlap and fronds obscure boundaries. Label only individually distinguishable fruit.
- **Candidate 0014 — Liberia, Africa - panoramio (272).jpg:** additional candidate from the recovered 30-image batch. Full-resolution inspection shows multiple attached coconut clusters. Some fruit are distant, overlapping or partly occluded, so it is a challenging candidate rather than a clean image. The Commons source page has been checked; credit **blk24ga**, licence **CC BY 3.0**.

Keep original candidates 0002 and 0004 plus their v0.1 labels unchanged for traceability. Do not silently transfer their labels to different images. Candidate 0031 should remain held out from the starter annotation pair; it can be reconsidered after a written minimum-visibility policy exists.

## Candidate 0031

- **Source:** https://commons.wikimedia.org/wiki/File:Coconuts_in_coconut_tree.jpg
- **Author:** Tanzeemfsugtvm
- **Licence shown:** CC BY-SA 3.0
- **Original dimensions:** 4160 × 3120
- **Visual decision:** defer from the initial annotation pair due to strong backlighting and small, ambiguous fruit.
- **Attribution:** retain author credit, source link and https://creativecommons.org/licenses/by-sa/3.0/; indicate changes if reused.

## Candidate 0032

- **Source:** https://commons.wikimedia.org/wiki/File:Coconut_in_Coconut_Tree.jpg
- **Author:** Sarmi~Kili
- **Licence shown:** CC BY-SA 4.0
- **Original dimensions:** 5184 × 3456
- **Visual decision:** prioritize for annotation practice; overlap and occlusion still require conservative boxes and independent review.
- **Attribution:** retain author credit, source link and https://creativecommons.org/licenses/by-sa/4.0/; indicate changes if reused.

## Candidate 0014

- **Source:** https://commons.wikimedia.org/wiki/File:Liberia,_Africa_-_panoramio_(272).jpg
- **Author:** blk24ga
- **Licence shown:** CC BY 3.0
- **Visual decision:** provisional positive candidate after full-resolution inspection; several attached fruit clusters are visible, but the image is not training-ready.
- **Attribution:** credit blk24ga, link to the source page and https://creativecommons.org/licenses/by/3.0/, and indicate changes if reused.

## Reproducible download helper

The repository includes `scripts/download_replacement_coconut_images.py` for candidates 0031–0032. Run it from the repository root with Python 3. It verifies the expected SHA-1 hashes and JPEG signatures. Successful download/checksum verification is not annotation approval. Candidate 0014 is available in the recovered candidate artifact; preserve its source record and image hash if it is selected for annotation.

## Next steps

1. Create new annotation records for 0032 and 0014; do not overwrite `annotations_v0.1.json`.
2. Write a single-fruit box policy covering overlap, occlusion and border truncation.
3. Record every visible, confidently identifiable fruit; mark ambiguous instances for review instead of guessing.
4. Have a second reviewer inspect all proposed boxes and record accept/change/reject decisions.
5. Complete per-image source/credit/licence and file-integrity checks before promoting any image.
6. Collect more independent orchard scenes and negative examples before defining leakage-safe train/validation/test splits.

## Status boundary

The full-resolution images for 0031–0032 were retrieved from GitHub Actions artifact run 39233532723 and visually inspected. Candidate 0014 was retrieved from artifact run 39092214196 and visually inspected. No labels have been created for these three candidates, no trained detector has been evaluated on them, and none is approved for training. Candidate 0032 and candidate 0014 are annotation priorities only; candidate 0031 is deferred.
