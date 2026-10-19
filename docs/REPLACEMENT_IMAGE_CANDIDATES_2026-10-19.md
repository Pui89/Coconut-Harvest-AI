# Replacement coconut images — reviewed 19 October 2026

## Decision

Retire candidates 0002 and 0004 from active training because the existing single-pass labels have unresolved geometry/coverage problems. Keep their old labels only as audit history; do not train on `annotations_v0.1.json`.

The new replacement candidates are **0033** and **0034**. Both images were downloaded through GitHub Actions run [39235348989](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39235348989); the download and published SHA-1 checks passed. The files are in the short-lived artifact `coconut-clean-replacement-candidates`, not committed to the public repository.

## Candidate 0033 — Coconut bunch in the tree

- **Image:** `0033_Coconut_bunch_in_the_tree.JPG`
- **Source:** https://commons.wikimedia.org/wiki/File:Coconut_bunch_in_the_tree.JPG
- **Creator:** Yasagan
- **Licence:** CC BY-SA 3.0 — https://creativecommons.org/licenses/by-sa/3.0/
- **Original dimensions:** 1920 × 2560
- **Visual decision:** use as a close-up annotation candidate. Several individual coconuts are visible, but stems/fronds cross the fruit and some coconuts overlap. Draw tight boxes around distinguishable fruit only; flag ambiguous instances.
- **SHA-1:** `36986fc8a09899c84468b60491cae1acdef567c9`

## Candidate 0034 — Coconut fruits

- **Image:** `0034_Coconut_fruits.jpg`
- **Source:** https://commons.wikimedia.org/wiki/File:Coconut_fruits.jpg
- **Creator:** Vinshi (Vishwas Suryawanshi)
- **Licence:** CC BY-SA 3.0 — https://creativecommons.org/licenses/by-sa/3.0/
- **Original dimensions:** 2048 × 1536
- **Visual decision:** use as a green-fruit cluster annotation candidate. The main cluster is clear, but individual fruits overlap and a few fruit are partly obscured by fronds. Do not draw one box around the whole bunch; label individual identifiable coconuts.
- **SHA-1:** `afb1ab478f0b2b25af495082665fa3ede7fdfc55`

## Required next actions

1. Annotate 0033 and 0034 as new records; never copy or reuse labels from 0002 or 0004.
2. Follow one policy for overlapping fruit, partially occluded fruit, and fruit touching image borders.
3. Render overlays and check missed, duplicate, loose, and wrongly merged boxes.
4. Obtain an independent second review and record the review decision.
5. Keep the old v0.1 labels excluded. Do not build a training dataset until the replacements pass annotation QA and enough independently sourced images exist for a meaningful group-separated evaluation.

## Status boundary

Image selection, source-page checks, downloads and SHA-1 verification are complete for 0033 and 0034. **Annotation and independent label QA are not complete.** The dataset remains blocked from training until those checks pass; this document does not claim a trained model or benchmark.
