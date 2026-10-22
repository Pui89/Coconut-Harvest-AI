# AI Agent Review and Support Plan

## Purpose
Provide repeatable, low-cost support for the Coconut Harvest AI prototype. The agent reviews evidence and software checks; it does not claim field readiness or operate harvesting hardware.

## Automated review stages
1. **Repository health:** run existing tests, check required files and report failing jobs with links.
2. **Dataset integrity:** verify image readability, annotation schema, coordinate bounds, missing files, duplicate hashes, and train/validation/test leakage.
3. **Annotation review queue:** render boxes and list suspicious boxes (zero/negative size, out-of-bounds, extreme aspect ratios, overlap, or empty labels). These are flags for human review, not automatic truth.
4. **Experiment readiness:** require a documented dataset version, split manifest, model/checkpoint identity, configuration, and reproducible command before evaluating a detector.
5. **Benchmark report:** only calculate precision, recall, F1, IoU/mAP and latency when approved ground truth and model predictions exist. Record hardware, thresholds, sample counts, and limitations.
6. **Safety-case tests:** exercise low confidence, missing depth, unreachable targets, blocked paths, and human-approval requirements. The current agent must not issue arm or cutter commands.

## Evidence labels
- **PASS:** a defined automated check ran and passed.
- **FAIL:** a defined check ran and failed.
- **NOT RUN:** required code/data/model is unavailable.
- **HUMAN REVIEW REQUIRED:** automated checks cannot establish correctness or permission.
- Never describe AI-generated draft boxes as ground truth until a person has reviewed and approved them.

## Suggested report
Create a dated Markdown report containing commit SHA, test command, test summary, dataset manifest/version, failures, evidence links, limitations, and next actions. Do not include fabricated metrics.

## Cost and permissions
Use existing GitHub Actions and Python tooling where available. No paid API, hosted model, external upload, or new cloud service is required. Workflows should use least-privilege permissions and should not commit generated data automatically without review.

## First priorities
- Fix and test retry handling for Wikimedia HTTP 429; retain partial-download provenance and clearly report incomplete candidate sets.
- Add unit tests for annotation schema and normalized bounding-box bounds.
- Add a report generator that distinguishes automated checks from human approval.
- Keep the AI annotation draft marked NOT FOR TRAINING until reviewed.

## Limitations
Software tests do not prove detector accuracy, orchard performance, robot reachability, safe cutting, or field readiness.