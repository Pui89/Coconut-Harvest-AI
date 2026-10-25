# Development Roadmap

This roadmap is an engineering plan, not a claim that the milestones have already been completed.

## Priority order

1. **Audit existing repository:** run the current tests and demo; record environment and failures.
2. **Model validation:** verify `robots/coconut_harvester.urdf`, joint axes, limits, inertias, and collision geometry.
3. **Repeatable simulation:** add a simple palm trunk and target bunch; make test conditions configurable.
4. **Safety state machine:** implement explicit states such as IDLE, PERCEPTION, PLAN, OPERATOR_APPROVAL, EXECUTE, ABORT, and FAULT.
5. **Vision baseline:** establish a documented dataset and a held-out evaluation before claiming detection performance.
6. **Benchmark evidence:** save raw logs and produce a summary from the raw records.
7. **Physical feasibility:** review risk and validate a tethered, low-height non-cutting rig before considering field operation.

## Release gates

| Gate | Required evidence |
|---|---|
| Simulation alpha | Robot model loads, repeatable world, automated tests |
| Research prototype | Documented dataset, baseline metrics, raw logs, known failure cases |
| Hardware feasibility | Measured grip/slip/braking, risk assessment, emergency-stop test |
| Field-trial candidate | Independent safety review, guarded tooling, operating procedure, supervised low-risk trials |

## Minimum benchmark record

Each run should record timestamp, git commit, simulator and dependency versions, scenario ID/seed, trunk dimensions, friction assumptions, sensor-noise settings, target pose, planner outcome, safety stops, elapsed time, and failure reason.

Do not publish a metric without its test conditions, sample count, raw data, and repeatable command. Keep simulated and physical results separate.

## Additional free-first five-task roadmap

This task list supplements the roadmap above. It is a plan, not evidence that each capability is already implemented.

| Priority | Development task | Cost target | Acceptance evidence |
|---|---|---|---|
| 1 | Improve autonomy-supervisor tests and common interfaces | Free | Unit tests cover healthy, unsafe, missing, invalid and non-finite inputs; interfaces are documented; commands and results are recorded |
| 2 | Improve coconut dataset quality and establish a vision baseline | Free, local | Source/license/credit manifest; hashes and duplicate review; corrected annotations; leakage-safe source/tree/session split; precision, recall and per-class results |
| 3 | Add perception uncertainty and task-planning tests to all three projects | Free, local | Tests cover low confidence, conflicting observations, missing inputs, invalid plans, unapproved actions and safe-hold outcomes |
| 4 | Add simulated navigation and multi-robot coordination for Flood Rescue | Free tools where feasible | Reproducible ground/boat/drone scenarios; route and task metrics; communication-loss and localization-failure tests; simulation limits stated |
| 5 | Add multimodal provenance, calibration and human-review workflow | Free, local | Each observation records source/reference, modality, timestamp and model/version; calibration is evaluated on held-out data; uncertain/conflicting cases route to human review |

### Project-specific priorities

- **Coconut Harvest AI:** complete source/license/hash review and annotation geometry checks before training; then establish a leakage-safe local vision baseline. Dataset quality and baseline metrics remain incomplete until evidence is recorded.
- **Extreme Flood Rescue AI:** define reproducible simulation scenarios and metrics for navigation, multi-robot task allocation, communication loss and localization failure. Simulation does not establish real-world rescue capability.
- **Multimodal Narcotics Screening AI:** document lawful data provenance and modality limitations, evaluate calibration on held-out data, and route conflicting or uncertain results to human review. AI output is not proof of substance identity or guilt.

### Free local interface tests

Run from each repository root:

```bash
python -m unittest discover -s tests -p "test_autonomy_supervisor.py" -v
python -m unittest discover -s tests -p "test_llm_interfaces.py" -v
```

These are commands to run, not a claim that the tests have passed. No model download is required for these interface tests. Do not add paid APIs, cloud GPUs, subscriptions or large model downloads without explicit approval after reviewing cost, license, download size and hardware fit.

