# Candidate artifact backup and integrity audit — 20 October 2026

## Preservation result

- Artifact: `coconut-image-candidates`
- Source workflow run: https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39092214196
- GitHub artifact ID: `12122299751`
- GitHub-listed expiry: 25 October 2026
- Files extracted: 30 images, plus `collection_summary.json`, `provenance.csv`, and `review_gallery.html`
- ZIP size: 15,643,763 bytes
- ZIP SHA-256: `da87fe2b3380fec4f5675f7c6d8b02a28f5597eaed1b03771c8ae2df4529480f`
- Result: ZIP integrity verified against the GitHub artifact digest; archive opens and contains the expected 30 image files.
- Per-image hashes: [`image_sha256_manifest_2026-10-20.csv`](../data/review_batch_2026-10-18/image_sha256_manifest_2026-10-20.csv)

## Preliminary visual triage

A contact sheet was generated from the extracted files. This is a thumbnail-level relevance screen only, not licence approval or independent annotation review.

- Obvious task mismatches to exclude from the in-tree mature-coconut detector set: 0003 (collage), 0007 (tool close-up), 0011 (processing scene), 0018 (map/diagram), 0023–0024 (young plants), and 0029 (racetrack).
- 0002 and 0004 remain **NOT APPROVED FOR TRAINING**; first-pass boxes need full-resolution correction and independent review.
- Several harvesting/climber and plantation images may be useful, but only if fruit is individually visible, labelable and source rights are verified.
- 0026–0028 are archival/grayscale candidates and should be used only if that domain is deliberately in scope and fruit boundaries are resolvable.
- The complete 30-image batch is not a training-ready dataset. Its candidate count must not be reported as the number of approved samples.

## Next gates

1. Keep a separate local backup of the ZIP and this manifest outside the temporary ChatGPT download environment.
2. Verify exact Commons source page, author/credit, licence version and attribution for each image considered for use.
3. Remove task mismatches from the proposed detector dataset; retain provenance records for traceability.
4. Define one-fruit bounding-box rules, including partial/occluded and border-truncated fruit.
5. Correct labels in a new version, preserving the original v0.1 labels unchanged, and record a second reviewer’s decision.
6. Deduplicate by SHA-256 and perceptual similarity; split by source/tree/session before training.
7. Train and evaluate locally only after the dataset gate passes. Report held-out results and failure cases; otherwise report **NOT RUN**.

## Safety and cost boundary

Remain free/open-source and local-first. No paid API, cloud GPU, or physical actuator command is needed for these data-quality steps. Passing software tests or simulation does not establish real-world harvesting safety.
