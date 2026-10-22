# Coconut Image Source Shortlist — 2026-10-22

## Purpose and status

This is a **research shortlist**, not an approved training dataset. The links below point to Wikimedia file-description pages where image dimensions, author attribution, and a stated licence can be reviewed. Re-check each page and preserve a dated copy of its metadata before use. No image is promoted to training status by this document.

The repository's promotion gate still applies: confirm reuse terms, download and hash the exact image, annotate every clearly visible coconut using the original image coordinate system, run geometry/path checks, and complete independent visual QA before training.

## Candidate sources for manual review

| Candidate | Source page | Attribution shown on source page | Licence shown on source page | Source-reported dimensions | Status |
|---|---|---|---|---|---|
| Existing candidate 0032 | [Coconut in Coconut Tree.jpg](https://commons.wikimedia.org/wiki/File:Coconut_in_Coconut_Tree.jpg) | Sarmi~Kili | CC BY-SA 4.0 | 5184 × 3456 | Annotation draft is incomplete; not approved |
| Shortlist A | [Coconuts in coconut tree.jpg](https://commons.wikimedia.org/wiki/File:Coconuts_in_coconut_tree.jpg) | Tanzeemfsugtvm | CC BY-SA 3.0 | 4160 × 3120 | Not downloaded, annotated, or approved |
| Shortlist B | [Coconut tree top.JPG](https://commons.wikimedia.org/wiki/File:Coconut_tree_top.JPG) | Bhaskaranaidu | Page describes a public-domain dedication; verify the exact source page and terms | 4608 × 3456 | Not downloaded, annotated, or approved |
| Shortlist C | [Coconut Tree With Coconuts.jpg](https://commons.wikimedia.org/wiki/File:Coconut_Tree_With_Coconuts.jpg) | Arif98741 | CC BY-SA 4.0 | 480 × 640 | Not downloaded, annotated, or approved |
| Shortlist D | [Coconut bunch in the tree.JPG](https://commons.wikimedia.org/wiki/File:Coconut_bunch_in_the_tree.JPG) | Yasagan | CC BY-SA 3.0 | 1920 × 2560 | Not downloaded, annotated, or approved |

## Required review before training

1. Open the original file page and verify the exact author, licence version, and source URL. Do not rely on this shortlist alone.
2. Decide whether the image is suitable for the target task. A close-up bunch, a tree-top scene, and an orchard view are different conditions; record the condition rather than treating them as interchangeable.
3. Download the exact image from its source page and calculate a SHA-256 hash. Keep the original file unchanged.
4. Record the attribution and licence in the repository's source-rights ledger. Check whether distributing images, annotations, crops, or derived assets is permitted and what attribution/share-alike obligations apply. If terms are ambiguous, do not include the image in a released dataset.
5. Annotate each individually distinguishable coconut. Do not guess at heavily occluded objects; follow the project annotation policy and mark ambiguous examples for review.
6. Validate box geometry, overlay every box on the original image, and arrange an independent visual review. A geometry validator alone cannot establish that a box encloses a coconut.
7. Keep all images from the same original capture/source together when splitting data. Do not let near-duplicates or crops of the same image cross train/validation/test splits.
8. Only update the promotion ledger after the evidence above exists. Until then, these remain candidates and must not be counted as training examples.

## Attribution notes

When an image is ultimately accepted, include the creator, exact file page, licence version and link, and a note describing any changes. For share-alike licences, review the obligations for any distributed modified image or annotation package before redistribution. This document does not provide legal advice.

## Honest reporting

Do not claim dataset readiness, detector accuracy, or model generalisation based on a source shortlist. The number of approved training images remains whatever the current promotion ledger confirms; this document does not change that count.
