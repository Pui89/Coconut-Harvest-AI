# Project status and verification log — updated 19 October 2026

## Current state

**Stage:** local-first software research prototype with an initial 30-image candidate batch, first-pass labels on two images, and simulation-oriented workflow. This is not a trained, field-validated autonomous harvesting robot.

## Successful and evidenced

- Python CI run [39096443251](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39096443251) passed across Python 3.10, 3.11 and 3.12. This is software regression evidence only.
- Candidate-image workflow [39092214196](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39092214196) collected 30 candidate images and generated provenance/review files. The temporary artifact is due to expire on **25 October 2026** unless downloaded earlier.
- GitHub Pages deployment [39093607358](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39093607358) passed.
- The 30-image batch was visually triaged; the batch report records readable files (29 JPEG and 1 PNG) and no byte-identical duplicates. This does not rule out visually similar images.
- First-pass bounding boxes exist for candidates 0002 (9 boxes) and 0004 (6 boxes) in [annotations v0.1](../data/review_batch_2026-10-18/annotations_v0.1.json). They are single-pass labels and still require independent visual QA.
- A fixed OpenCV HSV-contour heuristic was measured on those same two images: 20 predictions, 15 reference boxes, zero matches at IoU ≥ 0.50, precision 0.000, recall 0.000, F1 0.000, mean CPU runtime 15.12 ms/image. This is a failed exploratory heuristic baseline, **not** a trained AI detector result.
- Repository tools include provenance capture, offline annotation, annotation conversion, dataset building/split auditing, local training/evaluation scaffolding, and simulation-oriented decision workflow.

## Still in progress

1. Download the temporary image artifact before 25 October 2026 and preserve the files and provenance locally.
2. Individually verify original source-page licence, creator credit and reuse conditions for every image intended for training. Candidates 0001, 0002, 0004 and 0014 have had their source pages checked so far; the other 26 are not cleared.
3. Independently inspect and correct the 15 first-pass boxes on candidates 0002 and 0004; use a consistent annotation policy and keep an audit trail.
4. Reject irrelevant/ambiguous images, and collect or obtain permission for more varied orchard images.
5. Create source/tree/session-separated train, validation and test splits; inspect label previews and pass dataset and leakage audits before training.
6. Review the chosen local checkpoint and framework licences, then run a small local detector experiment only after the dataset is ready.

## Not yet demonstrated

- A complete, independently QA'd and licence-verified training dataset.
- A trained coconut detector with valid held-out precision/recall/mAP, latency, or independent-orchard generalization.
- Measured RGB-D localization benefit, calibrated camera-to-robot coordinates, validated collision-free motion, or physical harvesting.
- Any evidence that this robot is safer, faster, cheaper or better than alternatives.

## Next actions, in order

1. **Preserve the temporary artifact** before its stated expiry.
2. Finish licence checks and independent QA of the existing labels; do not treat the candidate batch as training-ready.
3. Expand the dataset with permitted, diverse orchard scenes; split by source/tree/session and run audits.
4. Run focused tests and a reproducible local detector experiment with a frozen held-out test set only when prerequisites pass.
5. Publish actual dataset/split counts, model/checkpoint provenance, hardware, thresholds, latency, metrics and failure examples. Keep missing values as **not measured**.
6. Separately test RGB-D localization against ground-truth positions, then test robot geometry, reachability, collisions and stop/fault cases in simulation.

## Future

Study performance across occlusion, lighting, distance/viewpoint and background clutter. Compare RGB-only with RGB-D localization only when paired depth data and credible ground-truth positions are available. Consider a supervised, non-cutting hardware test only after risk review and independent safety gates.

## Corrections and boundaries

- Candidate images are not automatically a labelled or legally cleared dataset.
- A model adapter, synthetic demo, fixture, or passing CI run is not proof of detector accuracy or safe harvesting.
- The current HSV baseline failed at the stated IoU threshold; do not present it as successful detection.
- Concept drawings and trajectories are illustrations, not a built robot or measured physical performance.
- No actuator commands or real harvesting are authorized by the current prototype.

## Cost and data boundary

Free/open-source-first. Do not use paid inference APIs, cloud GPUs, hosted endpoints or subscriptions for this plan. Review licences before downloading or redistributing model weights. Do not commit private/copyrighted images or model weights to Git.

## Evidence references

- [Candidate-image batch report](CANDIDATE_IMAGE_BATCH_2026-10-18.md)
- [Review-batch README and reproduction steps](../data/review_batch_2026-10-18/README.md)
- [First-pass annotations v0.1](../data/review_batch_2026-10-18/annotations_v0.1.json)
- [Baseline report v0.1](../data/review_batch_2026-10-18/benchmark_report_v0.1.json)


## Dataset follow-up — 19 October 2026

- Retrieved the 15.6 MB candidate artifact and verified its SHA-256 against GitHub's artifact digest: `da87fe2b3380fec4f5675f7c6d8b02a28f5597eaed1b03771c8ae2df4529480f`. The source artifact is still scheduled to expire on 25 October 2026; preserve a separate copy.
- Overlaid the 15 existing boxes on the original image files. Candidate 0002 has two box pairs with IoU above the 0.15 review threshold (pairs 2/3 and 3/5); candidate 0004 has three boxes touching image boundaries (box 4 right edge, boxes 5/6 bottom edge). No normalized-coordinate bounds errors were detected. These checks do not prove the boxes are correct.
- Added a dependency-free geometry-audit tool, a saved first-pass report, a source-rights ledger with the three already-checked source pages, and tests for geometry errors and review warnings.
- The source-rights ledger leaves all unverified source-page fields blank and keeps every candidate blocked from training promotion. Candidate 0004's displayed CC BY-SA and GFDL options are recorded; select and preserve a compliant attribution/licence path before reuse.
- **Current gate:** independent visual QA of all 15 boxes, explicit policy for occluded/truncated fruit, and per-image rights clearance are incomplete. Do not train a learned detector or publish detector metrics yet.


## Follow-up checkpoint — 20 October 2026

- Downloaded a local preservation copy of the GitHub Actions artifact `coconut-image-candidates` from run 39092214196 before its scheduled expiry. The copy should also be saved by the project owner to their own computer or storage.
- Created [candidate image visual triage](CANDIDATE_IMAGE_TRIAGE_2026-10-20.md) from a 30-image contact sheet and linked it from the README.
- The contact sheet suggests that many candidates are broad plantation, harvesting-person, tool, seedling, historical, or unrelated scenes rather than clear individual fruit targets. Candidates 0002 and 0004 are the strongest immediate candidates for full-resolution annotation review; they still have only first-pass boxes.
- This triage is not pixel-level annotation approval and does not independently verify source-page licences. The training gate remains **BLOCKED** until retained images have verified provenance/licences, reviewed labels, suitable class coverage, and leakage-safe splits.
