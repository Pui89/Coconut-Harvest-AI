# Bristol PrO-AI Case-Study Evidence Plan

**Project:** Coconut Harvest AI  
**Purpose:** organise a credible, reproducible case study for a practice-oriented AI PhD application.  
**Status:** planning document; it is not a report of completed experiments.

## Research question

How can a local-first coconut-perception and robotic-task-planning workflow communicate uncertainty and fail safely when orchard observations are incomplete, ambiguous, or spatially unreliable?

A practical first study should evaluate perception and decision support separately. It should not assume that a detector is accurate, that RGB-D fusion improves localization, or that a physical robot can harvest coconuts.

## Evidence already present in the repository

- Software components for a detector adapter, RGB-D proposal/localization interface, simple IoU tracking baseline, decision gates, simulation workflow, and JSON audit reporting.
- Dataset collection/review and annotation tooling, split-leakage audit tooling, and experiment provenance scripts.
- Synthetic fixtures and automated software tests.
- CI checks that can demonstrate selected software paths execute successfully.

These are implementation and software-testing evidence. They are not evidence of held-out detector accuracy, calibrated 3D localization, collision-free motion, or physical harvesting.

## Experiment sequence

### Study 1 — Dataset quality and provenance

**Question:** Can a small, legally usable image set be assembled with traceable sources and consistent labels?

1. Review every candidate image for relevance to coconut harvesting and record the source page, exact licence, attribution requirements, and reviewer decision.
2. Exclude irrelevant, duplicate, ambiguous, or licence-unresolved images.
3. Annotate only clearly visible coconuts; define how to handle partial occlusion and truncated fruit before labelling.
4. Have a second reviewer check a subset if available; record disagreements and how they were resolved.
5. Split by source, tree, location, or capture session where possible—not randomly by near-duplicate image alone.
6. Run the repository's split-leakage audit and save the output.

**Report:** candidate count, retained count, excluded count and reasons, verified licence coverage, label review procedure, split counts, and known sampling bias.

**Pass gate:** no unresolved licensing claims for images used in the experiment; splits are reproducible; test data remain frozen before model selection.

### Study 2 — Held-out coconut detection baseline

**Question:** How well does a specified detector identify coconuts on unseen, labelled images?

1. Record repository commit, dataset manifest/checksum, split counts, model name and version, checkpoint SHA-256, dependency versions, hardware, and exact command.
2. Train or configure one baseline only after checking the model/checkpoint licence and available hardware.
3. Freeze the test set before tuning thresholds or model settings.
4. Evaluate the frozen test set once for the reported result; preserve raw predictions and logs.
5. Report precision, recall, F1 at a stated confidence threshold, and mAP only where the evaluation implementation and labels support it. Include false positives, false negatives, per-condition breakdowns where sample sizes permit, and latency with the hardware and timing method stated.
6. Inspect representative successes and failures, including occlusion, backlighting, small/distant targets, and non-coconut lookalikes.

**Pass gate:** results can be reproduced from the recorded configuration; the test set was not used for tuning; all metrics include their evaluation conditions.

**If training cannot be completed:** report the blocker and leave metrics as “not measured.” Do not substitute synthetic fixtures, demo screenshots, or candidate counts for model performance.

### Study 3 — Localization and tracking (separate from detection)

**Question:** Under what conditions does the spatial proposal have useful, measurable error?

- Start with recorded, labelled sensor observations and documented camera/depth calibration.
- Compare predicted positions with a reference measurement collected using a stated procedure.
- Report sample count, coordinate frame, units, mean and median absolute error, error distribution, missing/invalid depth rate, and failure cases.
- Compare RGB-only, depth-only, and fused methods only if each method is implemented and evaluated under the same split and conditions.
- For tracking, state the association rule and report suitable metrics only if ground-truth tracks are available.

**Pass gate:** calibration and coordinate transforms are documented; reference measurements and units are clear; invalid depth and out-of-range cases are reported rather than silently discarded.

### Study 4 — Simulation-only task and safety-gate evaluation

**Question:** Does the workflow reject known unsafe or insufficiently evidenced proposals in the defined test scenarios?

Build a fixed scenario suite covering at least: missing sensor data, low confidence, occlusion, invalid depth, unreachable target, obstacle/collision flag, stale timestamps, human stop, and normal proposal flow. Use synthetic inputs clearly marked as synthetic.

**Report:** scenario count, expected versus actual decision, false-accept and false-reject counts, safe-hold behaviour, exceptions, and audit-log completeness.

**Pass gate:** all predeclared rejection cases behave as expected in the test suite. This verifies the specified software logic only; it does not establish physical safety or prove the simulated geometry is realistic.

## Evidence table for reports and application materials

| Claim | Evidence required | Current status |
|---|---|---|
| Application/workflow prototype exists | Source code, documented inputs/outputs, automated tests | Implemented; selected software paths tested |
| Dataset is suitable and permitted | Per-image review, licence records, labels, split audit | Candidate collection exists; review and labelling remain required |
| Detector works on unseen orchard images | Frozen held-out set and reproducible metrics | Not yet established |
| RGB-D improves localization | Calibrated comparison against reference positions | Not yet established |
| Tracking is reliable in orchard scenes | Ground-truth tracks and a stated tracking metric | Not yet established |
| Planner is collision-safe | Validated robot geometry, independent collision checks, scenario coverage | Not yet established |
| Robot physically harvests coconuts | Controlled physical trials, risk assessment, logged outcomes | Not demonstrated |

## Reproducibility bundle

For every experiment, preserve a small report folder containing:

- README.md — question, method, environment, and exact run command.
- manifest.json — commit, dataset checksum, split counts, model/checkpoint identity, dependency versions, and hardware.
- metrics.json or a clearly structured CSV — raw and aggregated measurements.
- failures/ — selected failure cases with identifiers and annotations, respecting image licences and privacy.
- limitations.md — what the experiment does not show, data gaps, and deviations from the plan.

Do not commit private or licence-restricted image data, model weights, local paths containing personal information, access tokens, or large generated datasets. Keep data and weights local or in an explicitly chosen free artifact location, and check retention/size limits before relying on temporary CI artifacts. No paid service is required by this plan.

## Suggested concise case-study statement

> I have developed a software prototype for AI-assisted coconut-harvesting research, including data-review tools, a perception/localization interface, conservative decision gates, a simulation-only task workflow, and automated checks. My next research step is to evaluate the components separately using a traceable, licence-checked dataset, a frozen held-out detection benchmark, calibrated localization measurements, and predefined simulation safety scenarios. The current project does not yet establish real-world detection accuracy or validated physical harvesting.

This statement is intentionally limited to evidence that can be inspected in the repository. Update it only when new results have actually been generated and reviewed.
