# PUI89 Quality Engineering Adoption — Coconut Harvest AI

**Status:** Initial product-specific test contract added. This is not evidence of model accuracy, physical testing or validation.

This repository adopts the shared [PUI89 Quality Engineering Standard](https://github.com/Pui89/PUI89-Shared-AI-Core/blob/main/docs/PUI89_QUALITY_ENGINEERING_STANDARD_V1.0.md).

## Nine controls and local acceptance

1. **Defects/regressions:** add a regression test for every reproducible software defect; cover valid, boundary, missing, stale and invalid inputs.
2. **Dependencies/security:** inventory direct/transitive dependencies, versions, licences and provenance. Review advisories before upgrades. No package is installed by this baseline; a static review is not a vulnerability scan.
3. **Performance:** record reproducible machine-readable results using the shared benchmark schema. Include commit, hardware, runtime, dataset/model versions and repeated-run method. Do not invent metrics.
4. **One-command check:** run `python -m unittest discover -s tests -v`. It uses the Python standard library and does not download models or call paid services.
5. **Dataset/model quality:** use the shared dataset manifest; document provenance, licence, labels, splits, leakage checks and human QA. Model accuracy remains Unknown until evaluated on held-out evidence.
6. **Failure simulation:** maintain the product scenarios in `quality/failure-scenarios.json`; add deterministic software tests before claiming simulation coverage. Simulation is not physical validation.
7. **Branch/PR workflow:** use feature branches and reviewable PRs. Keep required checks visible; no auto-merge or protection bypass.
8. **Documentation/evidence sync:** update this record, README and implementation status with the same evidence-backed maturity labels.
9. **Fair comparison:** disclose task, dataset/split, hardware, preprocessing, thresholds and metrics. Do not compare unlike configurations or claim superiority without comparable evidence.

## Product acceptance focus

Four maturity classes; rights-cleared real images; human-reviewed labels; per-class precision/recall/F1 and occlusion cases; reproducible CPU-only evaluation. No detector accuracy or harvest performance is claimed without results.

## Evidence status

- Regression scenario contract: **Implemented in this branch; tests pending execution by CI**.
- Vulnerability scan: **Not run**.
- Performance benchmark: **Not run; no metrics claimed**.
- Dataset rights/label QA: **Not verified by this file**.
- End-to-end simulation: **Scenarios specified; execution evidence pending**.
- Physical/field validation: **Not established**.

## Review gate

Merge only after CI passes, dependency and licence review is recorded, benchmark/dataset evidence is attached where applicable, and a human reviewer approves the PR.
