# Research Evidence Matrix

This matrix separates implementation evidence from research claims. Update statuses only after checking the current source, running the stated tests, and retaining evidence.

| Research question / claim | Current evidence category | Evidence still required | Permitted wording before validation |
|---|---|---|---|
| End-to-end workflow exists | Software prototype; synthetic workflow documented | Clean-checkout run and test logs for the current commit | “A simulation-first software workflow is implemented.” |
| Vision component detects coconuts | Local detector adapter / candidate proposal path | Identified model and weights, labelled held-out orchard dataset, metrics | “The application has a detector integration path; coconut-specific accuracy is not yet established.” |
| RGB-D improves 3D localization | RGB-D processing path | Calibrated sensor data, reference positions, matched RGB-only baseline | “RGB-D localization is a research hypothesis to evaluate.” |
| Tracking improves temporal consistency | Simple IoU tracking baseline | Annotated sequences and tracking metrics | “A simple tracking baseline is present; orchard tracking performance is unmeasured.” |
| Safety gates reject unsafe proposals | Decision-rule prototype | Adversarial unit/integration tests and independent review | “Software gates are intended to fail closed; they are not a certified safety system.” |
| Robot motion is feasible | Planning concepts / robot-model assets | Validated kinematics, joint limits, collision geometry, simulator runs | “Motion planning is a planned validation stage.” |
| Robot harvests coconuts | No physical-harvest evidence established | Guarded prototype, outcome logs, safety approval, supervised trials | “Physical harvesting has not been demonstrated.” |
| System is better than competing robots or human harvesting | No comparative evidence | Fair baseline, shared test protocol, adequate samples, cost and risk analysis | “Competitive advantage remains unproven.” |
| Product can reduce labour or cost | Intended application value only | Farm workflow study, measured cycle time, intervention rate, cost model | “Potential value requires a farm pilot and measured comparison.” |

## Minimum evidence bundle for each claimed result

- Source commit SHA and environment.
- Exact command and configuration.
- Dataset / scenario version and sample count.
- Raw per-example predictions or simulation logs.
- Evaluation script and resulting metrics.
- Failure examples and exclusions.
- Clear label: synthetic, simulator, offline real-image, or physical test.

Do not convert a planned experiment into a result statement. If evidence is missing, report “not yet measured” or “not demonstrated.”
