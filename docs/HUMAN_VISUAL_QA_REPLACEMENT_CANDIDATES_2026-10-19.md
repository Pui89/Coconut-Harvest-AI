# Visual QA — Replacement Coconut Candidates 0031–0032

**Review date:** 19 October 2026. Both original JPEGs were downloaded by GitHub Actions run 39233532723. The script's SHA-1 and JPEG-signature checks passed. Images are in a short-lived Actions artifact and were not committed to the repository.

## Decisions

| Candidate | Decision | Findings | Next action |
|---|---|---|---|
| 0031 — Coconuts_in_coconut_tree.jpg | Hold for difficult-light review; not for the initial clean training subset | Strong backlighting leaves many fruits dark, small, and partly hidden by fronds and stems. Consistent labels will be difficult. | Reconsider only after defining a minimum-visible-fruit policy; do not guess at ambiguous dark shapes. |
| 0032 — Coconut_in_Coconut_Tree.jpg | Keep as a challenging annotation candidate; not training-ready | More fruit is visible than in 0031, but green coconuts overlap and are partly obscured by fronds and branches. | Annotate clearly identifiable fruit individually, apply a consistent occlusion/truncation policy, and obtain a second label review before promotion. |

## Source and attribution records

- 0031 source: https://commons.wikimedia.org/wiki/File:Coconuts_in_coconut_tree.jpg — author Tanzeemfsugtvm; stated licence CC BY-SA 3.0.
- 0032 source: https://commons.wikimedia.org/wiki/File:Coconut_in_Coconut_Tree.jpg — author Sarmi~Kili; stated licence CC BY-SA 4.0.

The download script's expected SHA-1 checks passed for both files. Preserve source-page attribution and licence details in any distributed dataset and follow applicable licence terms. This visual review does not replace checking the source-page terms before redistribution.

## Annotation policy needed

1. Box the visible extent of each identifiable coconut without including nearby stems or fronds unnecessarily.
2. Label occluded fruit only when an individual fruit can be distinguished confidently.
3. Define a consistent rule for fruit cut by image boundaries and record truncation if supported.
4. Flag uncertain instances for review rather than guessing.
5. Keep both images in the review pool until labels are independently checked.

## Limits

This is a visual suitability review only. No labels were created for 0031 or 0032, no model was trained, and no detector metric can be inferred. Candidate 0032 is the better annotation candidate; 0031 is more suitable as a later difficult-light case than as a first training example.
