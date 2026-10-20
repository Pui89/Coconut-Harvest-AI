# Validation Matrix — Coconut Harvest AI

Last reviewed: 20 October 2026. Status is evidence-based; a code file existing does not mean the capability has been validated.

## Latest automated evidence

The latest main-branch CI run [39276683425](https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39276683425) passed its Python test jobs on Python 3.10, 3.11 and 3.12. This verifies the configured software test suite only. It does not approve dataset labels, establish detector accuracy, validate RGB-D localisation, or demonstrate physical harvesting.

| Capability | Repository evidence | Current status | What is still required |
|---|---|---|---|
| Local application and workflow orchestration | `apps/pui89_app/`, `demo_end_to_end.py` | Prototype code and tests exist; latest CI passed | Inspect generated audit reports and test the intended local deployment |
| Detection adapter and IoU tracking baseline | `local_detector.py`, `iou_tracker.py` | Integration interfaces/baseline exist | Independent labelled orchard test set; precision, recall, mAP, latency and failure examples |
| RGB-D localisation | `rgbd_localization.py` | Localisation interface exists | Camera/depth calibration and error measured against reference positions |
| Harvest-target eligibility and safety gate | `robot_workflow.py`, `src/coconut_harvest_robot/safety_gate.py` | Software preflight checks exist; malformed numeric inputs fail closed; latest CI passed | Hardware-specific risk analysis and independent safety review |
| Dataset intake and annotation | `training/`, `tools/`, `scripts/prepare_real_image_review.py` | Local workflow tools exist; replacement candidates are not yet approved data | Actual images collected, rights reviewed, boxes human-verified, group leakage audit passed |
| Training and test evaluation | `training/train_detector.py`, `training/evaluate_detector.py` | Reproducible local scripts exist; no trained result asserted here | Licensed local checkpoint + complete dataset; train and evaluate on frozen held-out test set |
| Simulation | Simulated workflow and demo tests | Software simulation path exists | Full robot model, sensor simulation, collision and recovery scenarios with recorded evidence |
| Physical harvesting | No evidence of completed hardware harvest in this repository status | **Not validated** | Robot arm, cutter, interlocks, calibration, supervised dry runs, safety review and measured trials |

## Latest safety hardening

The software gate blocks emergency-stop state, human exclusion-zone occupancy, failed collision checks, low/invalid confidence, invalid or negative motion/force/height values, non-finite values, and invalid configured safety limits. It is defence-in-depth software only, not a certified safety controller.

## Rules for publishing results

- Never call a candidate image a labelled training sample until the label has been reviewed.
- Never use training or validation images to claim held-out test performance.
- Record dataset/checkpoint hashes, exact configuration, environment, failure cases and the CI run URL.
- Mark unexecuted tests **NOT RUN**. Do not infer physical safety or harvest success from simulation alone.

## Execution checkpoint — 20 October 2026

This checkpoint is intentionally conservative. It distinguishes work that can be automated from work that requires inspection of the actual image pixels and licence records.

### Dataset decision log

- **Training status: BLOCKED.** Do not start detector training or publish a training-ready dataset while any selected image has pending rights checks, unresolved labels, or incomplete provenance.
- **Existing labels:** images 0002 and 0004 have first-pass labels only. Geometry checks are not annotation approval; overlaps, border-touching boxes, missed coconuts and false boxes require visual adjudication.
- **Replacement candidates A–E:** the source-page and licence notes are discovery records only. No candidate is promoted by this checkpoint. A candidate may replace a rejected image only after the original bytes are downloaded, SHA-256 and dimensions are recorded, the source/author/licence are captured, duplicate checks pass, and a human-reviewed overlay passes geometry and missed/false-object review.
- **If a candidate fails:** record `REJECTED` plus the reason and try the next permitted candidate. Do not make the label easier by guessing hidden or ambiguous fruit boundaries.
- **Artifact preservation deadline:** the 30-image candidate artifact referenced in the README is scheduled to expire on 25 October 2026. Preserve it before expiry if it is still needed; this is separate from dataset approval.

### Release gates (all required, in order)

1. **Provenance:** every retained image has a source URL, creator, licence/permission basis, retrieval date, dimensions, file hash, and any required attribution.
2. **Visual relevance:** image shows the intended coconut-harvest target; irrelevant, unreadable, duplicate, or unsuitable images are excluded.
3. **Annotation review:** every box is checked against the original image; missed targets, false boxes, overlaps, occlusion policy and border handling are resolved; a second independent review is recorded.
4. **Automated audit:** annotation geometry, image/label correspondence, duplicate/near-duplicate review, and source/tree/session-separated split leakage checks pass.
5. **Dataset freeze:** record a dataset version and manifest/checksum before training; keep unapproved drafts out of public training paths.
6. **Model benchmark:** only then run a local, licensed baseline and report real frozen-test precision, recall, mAP where applicable, latency, hardware, threshold, seed, checkpoint hash and failure examples. If not run, write **NOT MEASURED**.
7. **Robot validation:** keep perception metrics separate from RGB-D localisation, simulation, collision/safe-stop tests, and any future supervised non-cutting hardware trial.

### Current completion statement

Automated Python CI passing is useful software evidence, but it does not clear any of the gates above. At this checkpoint, dataset approval, a trained detector benchmark, measured RGB-D localisation, validated robot safety, and physical harvesting remain **NOT ESTABLISHED**. The project remains local-first/free-first; do not introduce paid APIs, cloud GPUs, subscriptions, or public commits of unapproved images/labels to try to accelerate this work.

