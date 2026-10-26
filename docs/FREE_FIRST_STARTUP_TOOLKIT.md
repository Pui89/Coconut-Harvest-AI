# Free-First Product and Engineering Toolkit

This project is built free-first. Prefer tools that run locally or are already available through GitHub. Do not add a paid service merely because it appears in a startup directory.

## Recommended workflow

1. **Source and dataset evidence:** record image origin, licence/reuse permission, attribution, file SHA-256, annotation version, reviewer and review date. Unclear provenance means the sample stays quarantined.
2. **Repeatable checks:** run `python tools/pui89_master_verify.py` first. Run existing unit tests only when their dependencies are already installed; do not let a convenience script install packages silently.
3. **Agent evaluation:** use the repository's labelled synthetic scenarios and evaluation harness. Synthetic pass rates measure workflow logic, not coconut detection accuracy.
4. **Model evaluation:** use only reviewed, licensed data and leakage-safe splits grouped by tree/source/session. Report sample counts, per-class precision/recall, mAP where applicable, and runtime with hardware and software versions.
5. **Customer discovery:** use a simple free document or spreadsheet to record orchard operators' needs, tree-height ranges, safety constraints, willingness to trial, and success criteria. Do not promise harvesting capability before field validation.

## Free-first tool choices

| Need | First choice | Guardrail |
|---|---|---|
| Version control and code review | GitHub repository and pull requests | Review changes before merging |
| Repeatable CI | Existing GitHub Actions workflows | Keep jobs short; monitor included usage |
| Local checks | Python standard library and existing tests | No hidden downloads or installs |
| Dataset audit | Existing provenance, geometry and promotion gates | Draft or unlicensed samples cannot enter approved training |
| Metrics | Existing evaluation scripts and JSON reports | Publish failures and sample counts, not only averages |
| Product page | GitHub Pages or the existing project site | Use only images with documented reuse rights |

## Cost and evidence rules

- No paid API, cloud GPU, subscription, or model download is required by this guide.
- Before adding any dependency, check its licence, maintenance status, install size, and whether an existing tool already covers the need.
- Never upload private, sensitive, or restricted agricultural data to a hosted service without permission.
- Label the robot as a concept until the relevant hardware, safety and field tests have actually been completed.
- Treat the 0–30 m tree-height range as a challenge target, not demonstrated performance, unless measured and independently evaluated.

## Definition of done for each upgrade

A change is complete only when its purpose is documented, a reproducible check exists, the check result is recorded, and limitations are explicit. A tool being installed or a CI job being green does not by itself prove real-world performance.
