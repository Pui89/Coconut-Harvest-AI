# Coconut Harvest AI — external replacement candidates (20 October 2026)

## Status

**Candidate discovery only — not approved training data.** The two Wikimedia Commons source pages below were opened and checked for visible author/source and a CC BY-SA 4.0 licence. Their full-resolution pixels still require local download verification, annotation, missed-fruit review, geometry checks, and independent visual review before they can enter any dataset split. Do not infer model performance from these images.

These are new source-page candidates, not replacements for existing local IDs 0031/0032 or the current 0032/0034 annotation-review work. Assign permanent dataset IDs only after the image bytes and provenance are recorded locally.

## Candidate A — young green coconuts in a dense cluster

- Source page: https://commons.wikimedia.org/wiki/File:Coconut_Palm_with_Young_Fruits_(Cocos_nucifera).jpg
- Author: Johnnybam
- Source: Own work
- Licence shown on source page: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
- Source-page dimensions: 3,072 × 4,096 pixels
- Initial visual screen: real coconut palm with several visible green fruits and substantial foliage/occlusion; potentially useful for a challenging detection example. Some small fruits overlap or are partly hidden, so label only objects whose boundaries can be judged reliably.
- Attribution requirement: credit Johnnybam, link to the source page and licence, and note any edits/crops.

## Candidate B — multiple green coconut clusters on a palm

- Source page: https://commons.wikimedia.org/wiki/File:Fruiting_Coconut_Palm_(Cocos_nucifera).jpg
- Author: Johnnybam
- Source: Own work
- Licence shown on source page: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
- Source-page dimensions: 3,072 × 4,096 pixels
- Initial visual screen: real palm with multiple visible green coconut clusters at different positions and partial occlusion by trunk/fronds; potentially useful for varied object sizes and lighting. Inspect the full-resolution image before deciding whether every visible fruit is labelable.
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
