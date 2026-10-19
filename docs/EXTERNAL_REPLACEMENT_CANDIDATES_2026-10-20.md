# Coconut Harvest AI — external replacement candidates (20 October 2026)

## Status

**Candidate discovery only — not approved training data.** On 20 October 2026, both Wikimedia Commons source pages were re-opened and their original 3,072 × 4,096 pixel images were visually inspected in the browser. Both pages display author Johnnybam, own-work source information, and CC BY-SA 4.0. The original images have not yet been verified as local downloaded files with recorded SHA-256 hashes. They still require local download verification, annotation, missed-fruit review, geometry checks, and independent visual review before they can enter any dataset split. Do not infer model performance from these images.

These are new source-page candidates, not replacements for existing local IDs 0031/0032 or the current 0032/0034 annotation-review work. Assign permanent dataset IDs only after the image bytes and provenance are recorded locally.

## Candidate A — young green coconuts in a dense cluster

- Source page: https://commons.wikimedia.org/wiki/File:Coconut_Palm_with_Young_Fruits_(Cocos_nucifera).jpg
- Author: Johnnybam
- Source: Own work
- Licence shown on source page: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
- Source-page dimensions: 3,072 × 4,096 pixels
- Browser original-file visual review (20 Oct 2026): real palm with two prominent green fruits near the centre-left and a dense cluster of smaller green fruits on the right; heavy frond/trunk clutter and many partly occluded fruit-like structures. Potentially useful for a difficult detection example, but annotate only individually distinguishable coconuts. Local file/hash and annotation review are still pending.
- Attribution requirement: credit Johnnybam, link to the source page and licence, and note any edits/crops.

## Candidate B — multiple green coconut clusters on a palm

- Source page: https://commons.wikimedia.org/wiki/File:Fruiting_Coconut_Palm_(Cocos_nucifera).jpg
- Author: Johnnybam
- Source: Own work
- Licence shown on source page: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
- Source-page dimensions: 3,072 × 4,096 pixels
- Browser original-file visual review (20 Oct 2026): real palm with several clear green coconuts in multiple clusters, including larger foreground fruit and smaller partly hidden fruit near the trunk/fronds. Visually promising for varied target sizes, but overlapping/occluded objects need a conservative annotation policy. Local file/hash and annotation review are still pending.
- Attribution requirement: credit Johnnybam, link to the source page and licence, and note any edits/crops.

## Required gate before inclusion

1. Download each original from its source page and calculate a local SHA-256 hash.
2. Preserve the source URL, author, licence, retrieval date, dimensions, and hash in the provenance ledger.
3. Check image relevance, duplicates, visual quality, and whether fruit boundaries are sufficiently visible.
4. Annotate only clearly identifiable coconuts; mark ambiguous/occluded objects according to the project's annotation policy rather than guessing.
5. Review overlays against the original, run geometry checks, and obtain independent visual review.
6. Keep candidate images and draft labels in a temporary review artifact until all checks pass. Do not commit these images or draft labels to the public repository and do not train on them before approval.

## Evidence boundary

The source pages establish the displayed licence/attribution information, not dataset suitability. This note records two promising candidates for further review; it does **not** claim they have been downloaded, labelled, approved, or used for training.
