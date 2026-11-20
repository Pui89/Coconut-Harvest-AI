# Batch 01 — Full-Resolution and Source-Rights Review

**Review date:** 2026-11-21  
**Source batch:** GitHub Actions run [44794101486](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/44794101486)  
**Scope:** Priority candidates 1–6 and 8  
**Review basis:** Original batch files (1280 px derivatives) inspected at full available batch resolution; Commons file pages checked where accessible.

## Outcome

- **Visual candidates worth retaining for later annotation:** 1, 2, 3, 4, 6, 8 — provisional, subject to annotation suitability review.
- **Low-priority / scene-context only:** 5.
- **Rights approved:** 0.
- **Agronomic labels approved:** 0.
- **Training approved:** 0.

This review is a technical screening, not legal advice, legal clearance, or an agronomic maturity assessment. No appearance class, biological maturity, or target-product suitability is assigned.

## Candidate-level findings

| ID | Full-resolution visual finding | Technical disposition | Source / license evidence |
|---|---|---|---|
| 1 | Multiple coconuts visible in a cluster; fruit boundaries overlap and are partly occluded by fronds. | Retain for manual box/mask feasibility review; not ground truth. | Provenance CSV lists Dcubillas and CC BY-SA 3.0. Commons page could not be independently retrieved in this review; rights pending. |
| 2 | A compact cluster with several visible fruit surfaces; strong occlusion and overlap. | Retain for manual annotation feasibility; check near-duplicate/source grouping with IDs 1, 3, 4. | Provenance CSV lists Dcubillas and CC BY-SA 3.0. Commons page could not be independently retrieved in this review; rights pending. |
| 3 | Vertical photograph; cluster is visible but occupies a limited area, with leaves obscuring fruit boundaries. | Retain as a difficult/occlusion example, not a primary clean sample. | Commons page identifies Dcubillas, Sabah, Malaysia, 30 Dec 2008, own work, CC BY-SA 3.0 (also GFDL metadata). |
| 4 | Vertical photograph; several fruits visible around the crown, with substantial leaf and stem occlusion. | Retain as a difficult/occlusion example; group with IDs 1–3 for split hygiene. | Commons page identifies Dcubillas, Sabah, Malaysia, 30 Dec 2008, own work, CC BY-SA 3.0. |
| 5 | Wide scene; coconut cluster is small relative to the frame and fruit boundaries are not reliably resolvable at the batch image size. | Demote to orchard/scene context; not a priority for fruit-instance labels. | Commons page identifies Muminur Rahman, own work, CC BY-SA 3.0. |
| 6 | Close cluster of fruits with useful visible surfaces; some fruit overlap, and colour is affected by lighting/scene conditions. | Highest-priority manual fruit-instance annotation candidate in this set; no maturity inference. | Commons page identifies Siva301in, own work, CC BY-SA 4.0. |
| 8 | Several green fruits are visible with comparatively clear outlines; stems and background still create occlusion. | High-priority manual fruit-instance annotation candidate; green appearance only, not maturity ground truth. | Commons page identifies H. Zell, own work, CC BY-SA 3.0 and GFDL; page says license of choice. |

## Source-group and split hygiene

IDs 1–4 are attributed to the same creator, same stated capture date (30 December 2008), and same location (Sabah, Malaysia). Treat them as one correlated source/session group. Do not distribute these images across training, validation, and test splits as if they were independent samples. The original-file checksums and visual similarity should be reviewed before final dataset grouping.

## Rights and reuse controls

1. A license statement on Wikimedia Commons is a useful provenance record, not a substitute for PUI89's own documented rights review.
2. CC BY-SA requires attribution, a license link, indication of modifications, and ShareAlike treatment for adaptations as described by the source page. Confirm how the obligations apply to any intended dataset packaging, annotation derivatives, model distribution, and commercial use before reuse.
3. ID 8 also lists GFDL alongside CC BY-SA 3.0 and allows the licensee to select a license. Record the chosen license and required attribution before reuse.
4. IDs 1 and 2 remain source-page-unverified in this review because their Commons pages could not be retrieved reliably. The artifact's provenance metadata alone does not clear them.
5. No image in this review is marked rights-approved. Obtain human sign-off and preserve source URL, author, exact license, attribution text, access date, file hash, and modification record.

## Agronomic and dataset boundaries

- Exterior colour is not sufficient to label Young Green, Mature Green, Yellow, or Brown with biological confidence.
- Images cannot establish internal water quality, meat thickness, embryo/haustorium status, seed viability, or suitability for coconut milk, copra, oil, or propagation.
- Fruit-instance boxes/masks may be annotated only after human review of each visible fruit. Ambiguous/occluded fruits should be marked uncertain or omitted under the annotation protocol.
- Keep appearance class, biological maturity evidence, and target-product suitability as separate labels.
- All candidates remain `UNKNOWN` for biological maturity and product suitability until supported by independent evidence.

## Status

`FULL_RESOLUTION_TECHNICAL_SCREENING_COMPLETE_RIGHTS_AND_AGRONOMY_PENDING`

This report does not alter the original batch summary. Counts remain: 0 rights-approved, 0 human-reviewed/annotated, and 0 training-approved.
