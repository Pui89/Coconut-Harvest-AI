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
