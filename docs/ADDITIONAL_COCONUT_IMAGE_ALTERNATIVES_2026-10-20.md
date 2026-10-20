# Additional coconut-image alternatives — 20 October 2026

## Why this list exists

The earlier replacement candidates remain **unapproved** until original files are downloaded and checked, bounding boxes are independently reviewed, and provenance is recorded. These are additional alternatives so the team can replace any candidate that fails visual QA. None of these images is automatically training-ready.

## Candidate C — full-grown coconut tree with fruits

- Source: https://commons.wikimedia.org/wiki/File:Full_grown_coconut_tree_with_fruits.png
- Author: Beendy234
- Licence shown: CC BY-SA 4.0
- Dimensions listed: 1,242 × 2,208 pixels
- Why consider it: source page describes a full-grown coconut tree with bundles of coconuts; a potential alternate view for visible fruit clusters.
- Possible rejection reason: if individual fruit boundaries are too small, blurred, or obscured for consistent boxes, exclude it.

## Candidate D — coconut and palm fronds

- Source: https://commons.wikimedia.org/wiki/File:Coconut_and_Palm_fronds.jpg
- Author: Ruby sunday
- Licence shown: CC BY-SA 4.0
- Dimensions listed: 1,728 × 3,840 pixels
- Why consider it: source page describes unharvested fresh coconut fruits hanging on a coconut tree; recent original photograph may provide a different capture and foliage context.
- Possible rejection reason: the narrow portrait composition and foliage occlusion may make some fruits hard to label. Inspect original resolution before annotation.

## Optional alternative E — fruiting coconut palm from Hawaii

- Source: https://commons.wikimedia.org/wiki/File:Coconut_Palm_plant_and_fruits_from_Hawaii.jpg
- Author: IGANZE
- Licence shown: CC BY 4.0
- Dimensions listed on page: 4,624 × 3,468 pixels
- Why consider it: high-resolution image described as a coconut palm with fruits; CC BY 4.0 does not impose the same ShareAlike condition as CC BY-SA.
- Possible rejection reason: reject if the fruit targets are too small, not clearly visible, duplicated elsewhere, or unsuitable for the target detection task.

## Mandatory pass/fail review for each alternative

1. Download the original file from its source page; record retrieval date, dimensions, file type and SHA-256.
2. Preserve attribution and licence information in the provenance ledger; check that the licence fits the project's intended use and redistribution plan.
3. Inspect the original at full resolution for relevance, sharpness, lighting, occlusion and visible individual fruit boundaries.
4. Check for duplicates or near-duplicates against all existing candidates before assigning a permanent ID.
5. Annotate only fruits that can be labelled consistently; create an overlay and compare it with the untouched original.
6. Run coordinate/geometry validation, inspect missed and false boxes, and obtain independent visual review.
7. If any check fails, mark the candidate **REJECTED** and move to the next alternative. Do not train on rejected or pending candidates.

## Evidence boundary

The source-page metadata and licence statements have been checked from Wikimedia Commons search results. This is not a claim that full-resolution pixels have been inspected, that any candidate has passed annotation QA, or that any image is now included in the dataset. Only an audited local copy with accepted labels may enter the training workflow.
