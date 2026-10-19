# Three AI Projects — Evidence-Based Status and Next Actions

**Reviewed:** 19 October 2026  
**Purpose:** coordinate the next work across Coconut Harvest AI, Flood Rescue AI, and Multimodal Narcotics Screening AI. This is a working plan, not a claim that unrun experiments have succeeded.

## Executive status

| Project | Current evidence-backed stage | Main blocker | Next measurable milestone |
|---|---|---|---|
| Coconut Harvest AI | Software prototype, local dataset/annotation tooling, safety-gate tests; no detector benchmark claimed | Too few reviewed labels and unresolved candidate-image intake/annotation QA | Build a rights-audited, human-reviewed image set and publish a reproducible baseline evaluation |
| Flood Rescue AI | Software workflow and safety/regression tests; reported Python CI passed | No independent real-flood perception benchmark or validated robot navigation | Audit a lawful dataset, define a grouped split, and run a clearly scoped perception baseline |
| Multimodal Narcotics Screening AI | Application/evaluation pipeline and synthetic regression checks; reported Python CI passed | No expert-reviewed independent real-world dataset; chemical identity cannot be inferred from ordinary images | Define a lawful narrow use case and test uncertainty/abstention before any real-world accuracy claim |

## 1. Coconut Harvest AI — first priority

### Completed or present in the repository
- Application/workflow prototype, detection/tracking interfaces, RGB-D localisation interface, and software preflight/safety-gate logic.
- Local scripts for dataset preparation, training, and evaluation.
- Source-rights tracking for the replacement-image review batch.
- Downloader script for candidates 0031 and 0032. It checks expected SHA-1 values and downloads files locally; downloading does **not** approve an image for training.

### Not yet demonstrated
- Full-resolution visual QA of candidates 0031 and 0032 in this session.
- Correct, independently reviewed bounding boxes for a sufficiently large dataset.
- A trained detector's held-out precision, recall, mAP, latency, or failure profile.
- Calibrated RGB-D position error, physical harvesting, or hardware safety.

### Immediate sequence
1. Run [the local replacement-image downloader](../scripts/download_replacement_coconut_images.py) from the repository root.
2. Upload the resulting two JPEGs from `data/review_batch_2026-10-19/images/` into the ChatGPT conversation so full-resolution image and annotation review can be done.
3. Inspect each image for visibility, small/overlapping fruit, backlighting, and whether individual coconut instances can be boxed consistently.
4. Verify source attribution/licence fields and record keep/reject/review decisions. Keep uncertain images out of the training set.
5. Human-review all boxes; audit duplicates and split by tree/source/capture session to reduce leakage.
6. Only when the reviewed dataset is adequate, train a local baseline and evaluate once on a frozen held-out test split. Record dataset/checkpoint hashes, exact command/configuration, software versions, metrics, and failure examples.

**No paid cloud compute or subscription is required by this plan.** Keep images, datasets, and model weights out of Git unless there is a clear legal and repository-size reason to publish them.

## 2. Flood Rescue AI

### Current evidence
The repository documents a software prototype, automated workflow/safety checks, dataset-manifest tooling, and a benchmark plan. Its reported CI run is software evidence only; it does not establish flood-scene accuracy or rescue capability.

### Next sequence
1. Select a lawful dataset with labels that match the intended task. Do not treat scene-level flood labels as person-detection labels.
2. Record provenance/licence, label meaning, duplicates, capture location/session, and exclusions.
3. Freeze group-aware train/validation/test splits before training.
4. Establish separate baselines for the intended tasks (for example, person detection versus flood-region segmentation); report per-task metrics and false negatives.
5. Add reproducible fixed-seed scenario tests for missing/conflicting sensors, stale data, communication loss, and fail-closed behaviour.
6. Treat ROS 2/Nav2/Gazebo integration and any physical trial as future milestones until the implementation and evidence actually exist.

## 3. Multimodal Narcotics Screening AI

### Current evidence
The repository contains an application/evaluation workflow and synthetic regression tests. Those tests are not real-world screening results, and ordinary RGB imagery cannot prove a substance's chemical identity.

### Next sequence
1. Narrow the intended use and document who is authorized to use the system and what evidence it may report.
2. Identify lawful data and expert-defined labels for that exact task; record permissions, provenance, and limitations.
3. Build an independent group-aware evaluation split and a simple baseline before attempting multimodal fusion.
4. Report per-class precision/recall, confusion matrix, false-positive and false-negative rates, calibration, and abstention/UNKNOWN behaviour.
5. Require human review for uncertain outputs; do not allow an AI score alone to trigger enforcement or assert chemical identity.
6. Do not claim multimodal benefit unless aligned, appropriately labelled data and a controlled comparison demonstrate it.

## Shared release gates

Before claiming a model is validated:
- [ ] Data source, licence/permission, provenance, and label definitions are recorded.
- [ ] Annotation QA and duplicate checks are documented.
- [ ] Train/validation/test split prevents related samples leaking across groups.
- [ ] Model, dependencies, configuration, random seed, and hardware are recorded.
- [ ] Held-out metrics and representative failure cases are published.
- [ ] Limitations and unrun tests are explicitly marked.
- [ ] The README distinguishes code, concept illustrations, simulation, benchmark evidence, and physical deployment.

## Bristol PrO-AI application framing

Describe these repositories as practice-oriented prototypes and ongoing engineering work. Use Coconut Harvest AI as the primary case study, and distinguish:
- **Existing work:** code, interfaces, test workflows, current dataset audit, and any test results actually recorded.
- **Current blockers:** image/annotation QA, data rights and size, independent evaluation, calibration, and hardware validation.
- **Proposed doctoral research:** methods and experiments to be developed and tested during the PhD.

Do not present planned experiments, concept artwork, synthetic checks, or successful CI as proof of real-world AI performance.
