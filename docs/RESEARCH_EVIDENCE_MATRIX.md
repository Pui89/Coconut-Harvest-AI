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


## External acoustic maturity evidence candidate — 20 November 2026

| Candidate | Source and observed facts | PUI89 relevance | Limitations / unresolved checks | Decision |
|---|---|---|---|---|
| EXT-ACOUSTIC-01 | [Acoustic Signal Dataset: Tall Coconut Fruit Species — Mendeley Data, DOI 10.17632/hxh8kd3snj.1](https://data.mendeley.com/datasets/hxh8kd3snj/1). Dataset page states CC BY 4.0 and describes 129 Philippine tall-coconut samples tapped on three side ridges, producing 387 signals. The associated open-access data article reports 44.1 kHz sampling and 132,300 time-series points per signal; samples were collected post-harvest in Argao, Philippines and pre-classified by local farmers/experts as premature, mature or overmature. | Candidate for offline research into acoustic features as an auxiliary maturity signal and for designing a future multimodal evaluation. It is not orchard-attached visual evidence and does not directly represent PUI89's four operational visual labels. | Severe class imbalance: dataset page reports 8 / 36 / 85 fruits; article text reports 8 / 35 / 85 in one location, so counts require reconciliation against the actual dataset. Three ridge recordings from one fruit are correlated and must remain in the same data split group to prevent leakage. Post-harvest tall Philippine coconuts may not generalize to other cultivars, regions, or attached fruit. Dataset licence and article publication licence are distinct: the article is CC BY-NC-ND; verify the exact dataset record, attribution and reuse conditions before acquisition. No local file, hash, independent label audit or PUI89 validation exists. | **CANDIDATE — research review only. No download, import, training, or performance claim.** |

### Evaluation constraints

- Treat each physical coconut as the independent grouping unit; never split its three ridge recordings across train, validation and test.
- Preserve the original maturity labels as source labels. Do not silently map premature / mature / overmature to PUI89's four visual classes.
- Report per-class support and imbalance; do not rely on accuracy alone. Any future evaluation should include per-class precision, recall, F1, confusion matrix and uncertainty.
- Acoustic tapping requires a repeatable acquisition method and controlled contact position/force, microphone placement, background-noise handling and device calibration. The published apparatus used a controlled knocking arm and microphone; results cannot be assumed to transfer to a robot-mounted or field sensor.
- Any fusion with vision must use paired observations from the same identified fruit and independently verified biological labels. Missing or poor-quality acoustic evidence must not force a maturity decision.
- The associated paper's publication licence is not the same as the dataset licence. Recheck both records and attribution requirements before any reuse.

**Current status:** candidate identified from public metadata and paper; no dataset bytes downloaded or imported, no model trained, no PUI89 test performed, and no readiness or accuracy claim is supported.
