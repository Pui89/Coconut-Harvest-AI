# Four-Class Coconut Harvesting and 0–30 m Validation Roadmap

**Purpose:** Turn the Coconut Harvest AI concept into a staged, evidence-led development programme. This roadmap is a plan, not proof that any milestone has been achieved.

## Correct interpretation of the four classes

These are four **proposed operational maturity classes**, not universal biological stages. Real maturity depends on cultivar, age, intended use, and orchard conditions; colour alone is not a reliable maturity measurement.

1. **Young green** — visually young fruit intended for young-coconut products, subject to an operator-defined harvest specification.
2. **Developing green** — fruit still developing; normally recommend WAIT / REVIEW unless a defined use-case explicitly calls for harvest.
3. **Mature green** — green fruit assessed against a validated maturity specification for the intended market.
4. **Brown / dry mature** — brown or aging fruit assessed against a validated specification; exterior appearance cannot confirm internal quality.

A **mixed-stage bunch is a scene condition**, not a fifth maturity class. The system should classify visible fruits individually where possible, preserve uncertainty, and avoid assigning one maturity label to an entire mixed bunch without evidence.

## Current evidence boundary

The repository status snapshot reports 34 candidate image records and 0 approved for training. Until rights, labels, geometry, and independent human QA are complete, do not train on the blocked set or publish model-accuracy claims. Software tests and synthetic scenarios verify software paths only; they do not establish fruit-classification accuracy or physical harvesting capability.

## Phased roadmap and acceptance gates

### Gate 0 — Define the task and label policy
- Freeze the four class definitions, intended-use assumptions, and an UNKNOWN / NEEDS_REVIEW outcome.
- Document cases that colour cannot resolve, including occlusion, mixed bunches, damage, unusual cultivars, and poor lighting.
- **Pass evidence:** versioned label guide; reviewed examples; agreement from at least two independent reviewers on a pilot set, with disagreements documented.

### Gate 1 — Make a lawful, reviewed dataset
- Verify source page, creator, licence, attribution, file identity/hash, and reuse conditions for every image.
- Review every bounding box and class label at native resolution; reject incomplete, ambiguous, or malformed annotations.
- Split by source/tree/session where known so near-duplicates cannot leak across train and test.
- **Pass evidence:** promotion-gate report with nonzero explicitly approved examples in each class; clean geometry audit; leakage audit passes; a frozen held-out test manifest. Do not fabricate or infer missing class labels.

### Gate 2 — Establish a reproducible visual baseline
- Run a compatible, licence-reviewed detector/classifier locally where feasible; do not download model weights automatically.
- Record exact code revision, model/weight source and licence, hardware, dataset hashes, thresholds, and command used.
- Report per-class precision, recall, F1 and confusion matrix; include false positives, false negatives, and UNKNOWN handling. Add mAP only if the evaluation implementation and ground truth support it.
- Measure latency on the actual target computer and report the sample count and summary statistic.
- **Pass evidence:** repeatable results on the frozen held-out set, plus an error review. No universal pass score is claimed in advance; define task-specific acceptance thresholds before evaluating.

### Gate 3 — Test selection and safe-stop logic
- Use synthetic cases first to test wrong-class predictions, low confidence, stale/broken sensors, occlusion, out-of-reach targets, obstacles, unstable positioning, tool faults, lost communications, and missing human approval.
- For any uncertain or unsafe condition, the required result is STOP / HOLD / HUMAN REVIEW, not a harvest command.
- **Pass evidence:** automated regression tests, traceable event logs, and independent review of failure cases. This is still not proof of hardware safety.

### Gate 4 — Validate geometry and reach in simulation
- Define a specific robot architecture before claiming a reach envelope: ground-supported boom, climbing platform, aerial platform, or another design. Each has different load, wind, stability, power, and recovery constraints.
- Simulate camera calibration, target depth, arm/boom reach, collision envelopes, payload, fruit fall/capture, and recovery. Model uncertainty rather than treating simulated values as measured reality.
- **Pass evidence:** reproducible simulation scenarios, assumptions and limits, failure cases, and a reviewable report. Simulation does not validate a real 30 m system.

### Gate 5 — Controlled physical prototype trials
- Begin with a secured bench rig and non-sharp tools, then low-height tests using a protected test area and an independent emergency-stop system.
- Progress only after each previous test stage passes. Use a secured test arrangement and trained supervision appropriate to the equipment; keep people outside drop and crush zones.
- Measure target-selection correctness, completed harvests, fruit damage, capture/lowering success, cycle time, faults, and near misses. Report denominators and failures, not just successful examples.
- **Pass evidence:** documented risk assessment, test protocol, calibrated measurements, independent safety review, and repeatable results for the exact hardware configuration.

### Gate 6 — Expand the verified height envelope
The **0–30 m range is a long-term design target**, not a current reach rating. Establish a measured operating envelope only for each specific tested configuration and conditions. Do not skip from a concept or low-height trial to a 30 m claim. At high elevation, structural loading, wind, overturning, falling-fruit risk, emergency recovery, and rescue access become critical engineering constraints.

**Pass evidence for each new height band:** approved risk assessment, secured test plan, independent safety review, successful repeat trials, recorded failures, and an explicitly bounded operating envelope. Never imply that the system can reach the full 0–30 m range until tests substantiate it.

## Minimum evidence dashboard

Keep these statuses separate and dated:

- Dataset: candidate count; source-rights approved count; annotation-QA approved count; per-class counts; leakage audit.
- AI: per-class precision/recall/F1 and confusion matrix on a frozen held-out set; model and dataset hashes; latency.
- Decision workflow: regression tests and failure-mode coverage; number of cases ending in safe hold / review.
- Robot: simulated reach versus physically measured reach; configuration and payload; successful trials / attempted trials; damage, faults, near misses, capture/lowering success.
- Safety: risk assessment revision, emergency-stop test record, operator approval process, and recovery plan.

## Free-first operating rules

- Prefer standard-library checks and existing local tools first.
- No paid API, cloud GPU, new subscription, or automatic model/package download without explicit cost, licence, disk-space, and hardware review.
- Do not install heavy robotics stacks on the development laptop until requirements, storage, GPU/RAM fit, and setup cost are understood.
- No automatic actuator control from the current software agent. Human review and independent hardware safety controls are required for physical tests.

## Immediate next actions

1. Resolve dataset blockers and review the candidate-0032 image hash and annotations.
2. Approve a small but legitimate pilot set with examples for all four classes; if any class has no approved samples, mark the class blocked rather than inventing data.
3. Freeze a leakage-safe held-out split.
4. Run a local baseline and publish per-class metrics with the exact command and limitations.
5. Only then advance to geometry/simulation and controlled hardware trials.
