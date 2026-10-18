# Project status and verification log — 18 October 2026

## Current state

**Stage:** software prototype + candidate-data collection. This is not a validated autonomous harvesting robot.

### Completed and evidenced
- [Candidate-image workflow passed](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39092214196); the run generated a downloadable artifact containing 30 candidate images, provenance metadata and a review gallery.
- [GitHub Pages deployment passed](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39093607358).
- Repository contains a local-first collection tool, licence/provenance capture, offline box annotator, annotation conversion, reviewed-dataset builder, split audit, training/evaluation scripts and simulation-oriented application components.
- Preliminary contact-sheet triage was recorded in [candidate batch report](CANDIDATE_IMAGE_BATCH_2026-10-18.md).

### In progress
- Review the 30 images at full resolution and verify original source/licence terms.
- Remove irrelevant or unsuitable images; manually label every visible target coconut.
- Build a group-separated train/validation/test dataset and inspect the generated previews/manifests.
- Check script/CLI compatibility and extend automated tests before any baseline experiment.

### Not yet demonstrated
- A complete, reviewed and licensed detection dataset.
- Measured held-out detection metrics, independent-orchard generalization, RGB-D benefit, safe arm motion, or physical harvesting.
- A reproducible trained model checkpoint. The training scripts deliberately require a user-provided local checkpoint.

## Next actions
1. Review and annotate candidate images.
2. Run dataset builder, dataset checks, split/leakage audit and visual label QA.
3. Run tests for dataset edge cases and baseline CLI argument compatibility.
4. Train only when data and a legally usable local checkpoint are available.
5. Freeze a held-out test split and publish real metrics with dataset size, provenance, limitations and experiment settings.

## Future
- Collect orchard-specific data with permission; evaluate occlusion, lighting, distance, viewpoint and negative examples.
- Compare detector baselines and RGB-only vs RGB-D localization using predefined metrics.
- Validate perception and motion in simulation before any supervised physical trials.

## Cost and safety
Free-first; no paid APIs or cloud GPUs required. Do not commit private/copyrighted images or model weights. No actuator commands or real harvesting are authorized by this prototype. A green CI result is software verification only, not evidence of agricultural performance.