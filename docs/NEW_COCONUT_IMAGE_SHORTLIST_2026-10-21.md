# New coconut image shortlist — 21 October 2026

## Purpose

These are newly identified public image candidates for README illustration and possible future manual review. **None is approved for training.** Source-page licence labels were checked on 21 October 2026; this does not establish that image pixels are suitable, annotations are correct, or data leakage has been ruled out.

## Priority candidates

| Priority | Image and source | Licence shown on source page | Reported original dimensions | Intended use / review note |
|---|---|---|---|---|
| 1 | [Fruiting Coconut Palm Canopy](https://commons.wikimedia.org/wiki/File:Fruiting_Coconut_Palm_Canopy.jpg) — Paul The Writer | CC0 1.0 | 4,080 × 3,072 | Strong candidate for a real-canopy overview. Inspect whether individual fruit boundaries are large and clear enough for labels. |
| 2 | [My coconut farm](https://commons.wikimedia.org/wiki/File:My_coconut_farm.jpg) — Zammy2004 | CC0 1.0 | 4,000 × 3,000 | Farm-context image; assess fruit visibility before considering annotation. |
| 3 | [Coconut Palm Bearing Fruits](https://commons.wikimedia.org/wiki/File:Coconut_Palm_Bearing_Fruits.jpg) | Confirm full source-page attribution before reuse | 3,072 × 4,096 | Promising fruit-cluster view; verify exact licence and author details from the page before copying or modifying. |
| 4 | [Immature coconut fruit](https://commons.wikimedia.org/wiki/File:Immature_coconut_fruit.jpg) | CC0 1.0 | Check source page | Close-up useful for explanatory visuals, but likely not representative of full-canopy detection. |
| 5 | [Coconut harvest](https://commons.wikimedia.org/wiki/File:Coconut_harvest.jpg) | GFDL shown in original upload history; verify current page terms | 1,340 × 2,866 | Harvesting-context illustration only; avoid unless its licence obligations are suitable for the intended redistribution. |
| 6 | [Koh Mak coconut palm plantation, Thailand](https://commons.wikimedia.org/wiki/File:Koh_Mak_%28island%29%2C_Thailand%2C_Coconut_palm_plantation.jpg) | CC BY 4.0 | 4,032 × 2,688 | Thailand-specific orchard context. Credit Vyacheslav Argenberg, link the licence, and indicate changes if modified. |

## Fast review workflow

1. **README illustration:** select at most one or two clear images with a verified compatible licence; keep the existing original project images if they are stronger.
2. **Dataset candidate:** download the original locally, record source URL, creator, exact licence URL, retrieval date, dimensions, file type and SHA-256.
3. **Visual QA:** inspect at full resolution; reject blurry, tiny, occluded, redundant or irrelevant images.
4. **Annotation QA:** label only clearly separable fruit instances, create an overlay, validate box geometry and obtain an independent review.
5. **Leakage checks:** compare file hashes and group related views by source/capture before splitting. Never place near-duplicate views across train and test.
6. **Promotion gate:** keep candidates pending until rights, annotation QA, duplicate checks and split assignment are independently recorded. A source-page licence is not proof that the candidate is training-ready.

## Status

- New source candidates listed: 6.
- Downloaded into the repository: none.
- Added to the training dataset: none.
- Annotation or model-performance claims: none.
