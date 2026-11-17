# Coconut real-image source recheck — 17 November 2026

**Scope:** public source-page metadata and visible Commons previews for the five candidates in `docs/COCONUT_FOUR_STAGE_IMAGE_SOURCE_REGISTER.md`.
**Boundary:** this is a source-page recheck only. No original image bytes were downloaded or imported, no local SHA-256 was calculated, no annotation was approved, and no candidate was promoted for training. The canonical CSV ledgers and existing approval flags are unchanged.

## Findings

| Register ID | Source / creator | Current source-page metadata | Dataset assessment | Decision |
|---|---|---|---|---|
| WMC-01 / existing candidate 0032 | [Coconut in Coconut Tree.jpg](https://commons.wikimedia.org/wiki/File:Coconut_in_Coconut_Tree.jpg) — Sarmi~Kili | CC BY-SA 4.0; 5,184 × 3,456; 8.23 MB | Commons preview shows a dense attached-fruit cluster with substantial overlap, frond occlusion and uneven/backlit illumination. Eight AI-assisted draft boxes cannot be validated against the original pixel file from the preview. | Keep as annotation priority, **not approved**. Original bytes, source fingerprint, box-by-box full-resolution review and independent QA remain required. |
| WMC-02 | [Mature Coconut Palm with Coconuts (Cocos nucifera).jpg](https://commons.wikimedia.org/wiki/File:Mature_Coconut_Palm_with_Coconuts_(Cocos_nucifera).jpg) — Johnnybam | CC BY-SA 4.0; 3,072 × 4,096; 4.68 MB | Page caption describes a mature palm bearing fully grown coconuts. This is uploader metadata, not independent agronomic confirmation of each fruit's maturity. | Strong candidate for visual suitability review; not acquired, annotated or approved. |
| WMC-03 | [Coconut Yellow Gourigatram.jpg](https://commons.wikimedia.org/wiki/File:Coconut_Yellow_Gourigatram.jpg) — Giri1234 | Public-domain dedication displayed; 1,536 × 2,048; 731 KB | Page description explicitly says this yellow variety is mainly used as tender coconut. Yellow colour therefore cannot be treated as evidence of the PUI89 mature-yellow class. | Keep only as a cultivar/colour-variation reference unless an agronomy reviewer defines a valid task label; not a mature-yellow training example by default. |
| WMC-04 | [Coconut Yellow.JPG](https://commons.wikimedia.org/wiki/File:Coconut_Yellow.JPG) — Iaminfo | CC BY-SA 3.0 and GFDL 1.2-or-later offered; 2,304 × 3,072; 2.14 MB | Source page identifies yellow coconuts but does not establish biological maturity or attached-canopy context. | Colour reference only pending native-resolution/domain review and explicit licence selection; not approved. |
| WMC-05 | [The fruit of coconut.jpg](https://commons.wikimedia.org/wiki/File:The_fruit_of_coconut.jpg) — Lotadegbemijowa | CC BY-SA 4.0; 4,160 × 3,120; 6.45 MB | Source page describes a ripe/plucked coconut. This is outside the primary attached-fruit canopy-detection domain. | Exclude from the primary canopy dataset; may be separately considered for a harvested-fruit auxiliary task, with its own labels and split. |

## What this changes

- The five public source pages were reopened on 17 November 2026 and their displayed creator/licence/dimension information was checked.
- The register's WMC-03 wording should not be interpreted as a mature-yellow label: the source page identifies a yellow variety mainly used as tender coconut.
- WMC-05 is explicitly a plucked-fruit image and should not be mixed into attached-fruit canopy detection.
- WMC-02 is a promising candidate for the next full-resolution review, but its uploader caption does not replace expert maturity review.
- WMC-01/0032 remains the immediate annotation priority. The visible preview confirms a difficult, occluded cluster, but does not validate the eight draft boxes.

## Remaining blockers

1. Obtain the unchanged original file for candidate 0032 in the local review workspace. The source page currently displays 5,184 × 3,456 and 8.23 MB; the previously recorded SHA-1 and byte-size check must pass before calculating/recording SHA-256.
2. Review all eight 0032 boxes at native resolution; correct/add/remove boxes only with visible evidence, then obtain independent second-person QA.
3. Review WMC-02 at native resolution and establish whether individual attached fruit can be annotated.
4. Obtain qualified agronomy review of the four operational labels. Keep visible husk colour separate from biological maturity; use uncertain/ignore where evidence is insufficient.
5. Update canonical ledgers only after actual file, rights, annotation and reviewer evidence exists. Keep the fail-closed training promotion gate in force.
6. Do not train or report detector metrics until enough approved, group-separated images and a frozen held-out test set exist.

## Evidence boundary

This recheck confirms what the Commons pages currently display. It does not provide legal advice, verify the bytes of a local copy, establish the uploader's biological maturity claims, validate annotations, or approve any image for training. No image files were added to this repository.
