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
| EXT-ACOUSTIC-01 | [Acoustic Signal Dataset: Tall Coconut Fruit Species — Mendeley Data, DOI 10.17632/hxh8kd3snj.1](https://data.mendeley.com/datasets/hxh8kd3snj/1). The dataset page states CC BY 4.0 and describes 129 Philippine tall-coconut samples tapped on three side ridges, producing 387 signals; its metadata lists class counts 8 / 36 / 85. The 2023 data article reports 44.1 kHz sampling and 132,300 time-series points per signal, and describes post-harvest samples from Argao, Philippines, pre-classified by local farmers/experts as premature, mature or overmature. The 2023 article text separately reports 8 / 35 / 85 (128 by arithmetic), so the original records require reconciliation. A later 2026 study using this public dataset explicitly reports that the distributed data file comprises 127 fruits: 8 immature, 36 mature and 83 overmature. | Candidate for offline research into acoustic features as an auxiliary maturity signal and for designing a future multimodal evaluation. It is not orchard-attached visual evidence and does not directly represent PUI89's four operational visual labels. | The public descriptions and later study do not agree on cohort totals/class counts. Treat 127 fruits and 8 / 36 / 83 as a later-study report about the distributed file, not as an independently verified PUI89 file audit. Severe class imbalance remains. Three ridge recordings from one fruit are correlated and must remain in the same data split group to prevent leakage. Post-harvest tall Philippine coconuts may not generalize to other cultivars, regions, or attached fruit. The dataset record states CC BY 4.0; the associated 2023 article is CC BY-NC-ND. These are distinct licences: verify the exact dataset record, attribution and reuse conditions before acquisition. No local file, hash, independent label audit or PUI89 validation exists. | **CANDIDATE — research review only. No download, import, training, or performance claim.** |

### Evaluation constraints

- Treat each physical coconut as the independent grouping unit; never split its three ridge recordings across train, validation and test.
- Before any experiment, inspect the actual distributed workbook and create a fruit-level manifest. Reconcile unique fruit IDs and class counts against the published descriptions; preserve the raw source labels and document exclusions rather than silently forcing the total to 129.
- Preserve the original maturity labels as source labels. Do not silently map premature / mature / overmature to PUI89's four visual classes.
- Report per-class support and imbalance; do not rely on accuracy alone. Any future evaluation should include per-class precision, recall, F1, confusion matrix and uncertainty.
- Acoustic tapping requires a repeatable acquisition method and controlled contact position/force, microphone placement, background-noise handling and device calibration. The published apparatus used a controlled knocking arm and microphone; results cannot be assumed to transfer to a robot-mounted or field sensor.
- Any fusion with vision must use paired observations from the same identified fruit and independently verified biological labels. Missing or poor-quality acoustic evidence must not force a maturity decision.
- The associated paper's publication licence is not the same as the dataset licence. Recheck both records and attribution requirements before any reuse.

**Current status:** candidate identified from public metadata and papers; no dataset bytes downloaded or imported, no local workbook audit or hash, no model trained, no PUI89 test performed, and no readiness or accuracy claim is supported.

### External source cross-check

- [Mendeley Data dataset record](https://data.mendeley.com/datasets/hxh8kd3snj/1) — dataset description, metadata counts and stated CC BY 4.0 licence.
- [Caladcad et al., 2023, Data in Brief](https://doi.org/10.1016/j.dib.2023.108936) — acquisition method, sample-rate details, source location and article publication licence.
- [2026 follow-up study using the public dataset](https://www.mdpi.com/2624-7402/8/9/395) — reports that the distributed data comprise 127 fruits (8 / 36 / 83); this is a published report, not a PUI89 independent file audit.
