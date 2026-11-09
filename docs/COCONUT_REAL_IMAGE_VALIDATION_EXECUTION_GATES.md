# Coconut Harvest AI — Real-Image Validation Execution Gates

**Status:** execution plan; no new images, labels, model scores, or robot validation are claimed by this document.  
**Policy:** zero-cost first, CPU-first, human-reviewed, fail-closed, evidence before capability claims.

This plan makes real-image validation the project's primary development objective. It uses the existing rights ledger, candidate-review ledger, annotation tools, promotion gate, split audit, evaluator, and simulation/mission interfaces. It does not replace those tools or silently approve existing records.

## Current evidence baseline

The repository's 29 October 2026 readiness snapshot records 34 candidate records, 34 matching review records, and **0 candidates approved for training**. The two-image annotation audit records 15 first-pass boxes across images 0002 and 0004; both images still require independent box-by-box review. Candidate 0032 has an eight-box AI-assisted draft, but its source-byte SHA-256 is a placeholder and its boxes, human-QA flag, and training approval remain unverified.

Therefore:
- Do not train or publish coconut-detection accuracy from the current candidate batch.
- Do not treat geometry validation, source-page inspection, or automated smoke tests as human annotation QA.
- Do not infer the user's local source-image file is available to GitHub or this workflow.
- Keep all current approval flags unchanged until the actual evidence exists.

## Gate 1 — Source image rights and provenance

For every candidate considered for training, record and independently review:
- source URL and original creator/rights holder;
- exact licence or written permission, including commercial-use and derivative-work conditions;
- required attribution and share-alike obligations, if any;
- original filename, dimensions, byte size, and cryptographic fingerprint;
- date and reviewer of the source-page check;
- whether the local file is byte-identical to the reviewed source.

A source page that displays a licence is not proof that a local copy is byte-identical. Use the repository's source-hash helper for candidate 0032 exactly as documented in `docs/COCONUT_DATASET_READINESS.md`. Run its dry-run first; write the SHA-256 only after all source checks pass. Never guess a hash, re-encode the source before fingerprinting, or mark a candidate approved based only on metadata.

**Gate 1 exit:** rights and provenance fields are complete and independently checked for each image; unresolved rights means the image stays excluded.

## Gate 2 — Human annotation QA

Use the offline annotator and preserve every prior annotation version. A label represents one individually distinguishable coconut fruit, not an entire bunch, leaf, stem, or cluster.

Proposed four-class taxonomy (operational definitions must be confirmed against the project's intended harvest policy by a qualified human reviewer before labels are approved):
1. `young` — visibly immature, predominantly green fruit;
2. `mature_green` — developed fruit with predominantly green external appearance;
3. `yellow` — fruit with a clearly yellow/yellowing maturity appearance;
4. `brown_aging` — brown, drying, or aging fruit.

Use `uncertain` / `ignore` for ambiguous, heavily occluded, blurred, or insufficiently visible fruit. These are review states, not a fifth maturity class. Do not force uncertain fruit into one of the four classes. If mixed-stage bunches occur, annotate individual fruits where separable and record bunch-level context separately.

Annotation rules:
- draw a tight box around the visible extent of each individually identifiable fruit;
- do not include neighbouring fruit, leaves, stems, or large background regions;
- apply one documented rule to partially occluded and image-border-truncated fruit;
- record missed, ambiguous, accepted, changed, and rejected instances with reasons;
- inspect full-resolution overlays, not only normalized-coordinate geometry;
- require an independent second-person review for every box before promotion;
- save reviewed output as a new version; retain draft and prior versions unchanged.

**Gate 2 exit:** all included boxes have documented human decisions, class definitions are consistently applied, and independent review is recorded. A geometry audit alone never satisfies this gate.

## Gate 3 — Dataset construction and leakage control

Create a versioned manifest containing candidate ID, source fingerprint, rights decision, annotation version, reviewer status, class counts, capture context, and inclusion/exclusion reason.

Before any split:
- remove exact and near duplicates;
- group images by orchard/tree, photographer/source, and capture session;
- split groups—not individual near-identical frames—into train, validation, and frozen test sets;
- publish image counts, scene/group counts, and per-class instance counts for every split;
- report class imbalance and missing environmental coverage;
- keep the frozen test set unavailable for model or threshold tuning.

Do not invent a universal minimum image count. The release review must show enough independent scenes and examples per class to support the intended claim; if not, label the result exploratory and keep the gate blocked.

**Gate 3 exit:** all included images are rights-cleared and human-reviewed; split-leakage audit passes; every class and split has a transparent count; the test set is frozen.

## Gate 4 — CPU-first detector baseline

Start with the smallest reproducible baseline that is already supported by the repository and the available machine. Prefer the existing standard-library evaluator and preflight tools. Before selecting a training framework or checkpoint, verify its licence, CPU compatibility, package footprint, Python compatibility, and whether weights download automatically.

Rules:
- no paid API, subscription, hosted inference, cloud GPU, or automatic model/weight download;
- no new dependency installation without explicit cost, licence, and disk/RAM review;
- record exact model/checkpoint provenance and SHA-256;
- if no suitable model is available locally, report `NOT RUN — no approved local checkpoint`; do not substitute a generic model and call it a coconut detector;
- keep detection and maturity classification as separately measurable tasks;
- use the same declared input size, confidence threshold, NMS settings, and hardware profile for comparisons.

**Gate 4 exit:** a reproducible CPU run exists on the approved dataset, with full environment and model provenance. If resources are insufficient, retain the honest `NOT RUN` status and document the constraint.

## Gate 5 — Evaluation and failure analysis

Use the existing evaluation tooling and report, at minimum:
- precision, recall, and F1 at a declared box IoU threshold;
- AP/mAP at IoU 0.50 and, where supported, mAP across IoU 0.50:0.95;
- per-class results and TP/FP/FN counts for all four maturity classes;
- confusion matrix for maturity classification, separately from box detection;
- inference latency, image size, CPU model, batch size, and memory use;
- false positives, missed fruit, merged/split boxes, occlusion, backlighting, blur, and uncertain-class cases.

Include confidence intervals or a clear small-sample warning where appropriate. Never compare results from different test sets as if they were a controlled model comparison. A heuristic is a heuristic baseline, not a trained AI model. A model not executed receives no score.

**Gate 5 exit:** results are reproducible from a frozen test set, per-class failure cases are reviewed, and limitations are published alongside scores.

## Gate 6 — Simulation-only harvest integration

Only after Gates 1–5 pass for a defined model/dataset version, connect perception output to the existing harvest mission interface in simulation.

The detector may produce a reviewable target proposal containing image/target identity, maturity class, confidence, uncertainty, timestamp, and source evidence. The planner must reject stale, low-confidence, out-of-distribution, occluded, or conflicting observations and preserve human approval.

Simulation sequence:
1. replay frozen, rights-cleared test scenes;
2. transform image detections into simulated target hypotheses only when camera calibration and geometry are available;
3. test reachability, exclusion zones, worker/animal detection, collision checks, emergency-stop state, and sensor-health gates;
4. evaluate target selection and no-harvest/abstain decisions;
5. record simulated harvest success/failure, collision/unsafe-action counts, and failure reports.

No actuator authorization, physical cutting, or autonomous field operation is enabled by this plan. Perception scores do not prove safe reachability or successful harvesting.

**Gate 6 exit:** repeatable simulation evidence exists with zero unreviewed physical actions; hardware integration remains a separate safety and validation programme.

## Execution order and reporting

1. Complete source provenance for candidate 0032 using the user's original local file; keep the hash helper dry-run first.
2. Conduct independent human review of candidate 0032's eight-box draft and the 15 existing boxes in images 0002 and 0004.
3. Resolve rights and annotation review for the remaining candidates; update ledgers only with observed outcomes.
4. Run the fail-closed dataset promotion gate and split-leakage audit.
5. Freeze a versioned dataset; only then run the CPU baseline and evaluator.
6. Integrate approved perception outputs into simulation-only missions.

Every report must state **confirmed**, **not yet verified**, **not run**, and **next action** separately. A blocked gate is an expected safety control, not a reason to weaken the gate.
