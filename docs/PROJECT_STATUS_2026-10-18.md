# Project status and verification log — 18 October 2026

## Current state

**Stage:** local-first software prototype, dataset-candidate collection and simulation-oriented workflow. This is not a trained, field-validated autonomous harvesting robot.

## Successful and evidenced

- Latest known Python CI run [39096443251](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39096443251) passed across Python 3.10, 3.11 and 3.12. This is software regression evidence only.
- The candidate-image workflow [39092214196](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39092214196) collected 30 candidate images and generated provenance/review files. The artifact is temporary and is due to expire on 25 October 2026 unless downloaded earlier.
- The GitHub Pages deployment [39093607358](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39093607358) passed.
- Repository tools include candidate collection, provenance capture, offline bounding-box annotation, annotation conversion, dataset building/split auditing, local training/evaluation scaffolding, and a simulation-oriented decision workflow.

## Continuing now

- Download and inspect the 30-image artifact; verify every image's relevance and original licence/attribution terms.
- Exclude irrelevant or ambiguous images; label only clear coconut targets and review labels visually.
- Build group-separated train/validation/test splits and run manifest, duplicate/leakage and label-quality checks.
- Check dataset/training script compatibility and run a baseline only after rights, labels, hardware and checkpoint licence are confirmed.

## Not yet demonstrated

- A complete, human-reviewed, licence-verified dataset.
- A trained detector with held-out precision/recall/mAP, latency or independent-orchard generalization.
- Measured RGB-D localization benefit, calibrated camera-to-robot coordinates, validated collision-free motion, or physical harvesting.
- Any claim that this robot is safer, faster, cheaper or better than alternatives.

## Next actions

1. Download the candidate artifact before its stated expiry; inspect images and licences.
2. Annotate approved images, build the dataset, inspect previews, and pass the leakage/manifest audits.
3. Run the focused tests and a reproducible local baseline with a frozen held-out test set.
4. Publish raw results, dataset/split counts, model/checkpoint provenance, hardware, thresholds, latency and failure examples; use **not measured** for missing results.
5. Validate RGB-D error against reference positions, then test robot geometry, reachability, collisions and stop/fault cases in simulation.

## Future

Collect permitted orchard-specific images across occlusion, lighting, distance and viewpoint; compare detector baselines and RGB-only versus RGB-D localization; then progress from simulation to any supervised, non-cutting hardware test only after risk review and independent safety gates.

## Corrections and boundaries

- Candidate images are not a labelled or validated dataset.
- A model adapter, demo, synthetic fixture, or passing CI run is not proof of detector accuracy or safe harvesting.
- Concept drawings and trajectories are illustrations, not a built robot or measured physical performance.
- No actuator commands or real harvesting are authorized by the current prototype.

## Cost boundary

Free/open-source-first. No paid inference API, cloud GPU or subscription is required by this plan. Do not commit private/copyrighted images or model weights.

### Candidate-image review progress — 18 October 2026

- Retrieved and inspected the temporary 30-image candidate artifact; 30 files are readable (29 JPEG, 1 PNG) and no byte-identical duplicates were found.
- Completed full-resolution visual inspection and checked the source-page licence/credit details for three priority candidates: IDs 0001, 0002 and 0004. The source pages list CC BY-SA licences (0004 also displays GFDL); the credits and URLs are recorded in [the batch report](CANDIDATE_IMAGE_BATCH_2026-10-18.md).
- **Progress is still preliminary:** the other 27 source pages have not been individually licence-verified; the priority images still need bounding-box annotations and QA; no dataset split or model benchmark has been completed.
