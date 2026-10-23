# PUI89 Product Engineering Standard — Coconut Harvest AI

**Product direction:** perception-assisted orchard inspection and robotic harvesting.  
**Status rule:** this document is an engineering plan, not a claim of validated field performance.

## Product promise

Build a system that can identify candidate coconuts, estimate maturity and location, explain uncertainty, and request a safe harvest decision. The robot must prefer **no cut** over an uncertain or unsafe cut.

## Architecture boundaries

1. **Perception:** detector and tracker identify candidate fruits; a separate maturity classifier may be evaluated where labels support it.
2. **Geometry:** estimate target position only when camera calibration and depth/geometry evidence are valid. Do not infer exact reach from a 2-D box.
3. **Planning:** rank candidate targets using maturity, reachability, visibility, branch/workspace risk, and task cost.
4. **Safety supervisor:** independently checks stale data, uncertainty, target identity, human exclusion, collision limits, and emergency-stop state.
5. **Actuation boundary:** model output is only a proposal. No generative or vision-language model may directly command the cutter or robot joints.
6. **Evidence:** every benchmark run records dataset version, split, code revision, model identifier/checksum, runtime environment, metrics, and limitations.

## Required evaluation gates

- Dataset provenance, license, annotation geometry, and human-review status are complete before training or final evaluation.
- Split by tree/source/session where possible to reduce leakage; never select the test set after seeing results.
- Compare at least two compatible detectors on the same held-out set before choosing a default.
- Report precision, recall, mAP at stated IoU thresholds, per-stage confusion where supported, latency, peak memory, and false-negative/false-positive examples.
- Evaluate blur, backlighting, shadows, leaf occlusion, distance, camera movement, and maturity ambiguity.
- Report uncertainty and abstention behavior; a model score is not a safety certificate.
- The 0–30 m range is a design envelope only until each distance band has valid, representative, measured evidence.

## Release blockers

Do not label a model or robot field-ready if data provenance is unresolved, held-out evaluation is absent, safety regressions fail, target geometry is unverified, or the required hardware has not been tested. Synthetic images must be marked synthetic and must not be mixed into real-world test metrics.

## Model and license policy

Keep large weights out of Git history. Record the exact model source, version/revision, checksum, license and commercial-use implications, download instructions, hardware requirements, and known limitations. Do not enable model downloads or training automatically in CI. CI should run lightweight tests without requiring a GPU or large model download.

## Product-grade release evidence

Each release should include:
- tested installation and inference path;
- versioned benchmark report;
- dataset/model cards and license inventory;
- safety and failure-injection test results;
- known limitations and a clear rollback procedure;
- reproducible commands that work without paid services.

## Current truthfulness rule

A design concept, simulation, unit test, and real orchard trial are different evidence levels. Describe each separately. Never invent accuracy, latency, successful harvesting, physical reach, or field validation.
