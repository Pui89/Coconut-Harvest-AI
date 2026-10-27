# PUI89 Free-Source Upgrade and Cost Guard

**Purpose:** improve engineering quality without introducing a purchase, subscription, metered API, cloud GPU, automatic model download, or automatic hardware action.

## Hard cost rules

- Use Python's standard library first. Do not add a dependency unless a concrete test requires it.
- Do not add paid API endpoints, hosted inference, cloud GPU, larger GitHub runners, paid datasets, or subscription tools.
- Do not add scheduled workflows, automatic dataset downloads, model-weight downloads, video rendering, or artifact uploads by default.
- Before suggesting an optional tool, record its official source, licence, download size, runtime requirements, network requirements, and any possible billing trigger. If any cost or licence is uncertain, mark **NOT APPROVED** and do not install it.
- Never claim that a project, model, dataset, simulation, or robot is validated when only a smoke test or synthetic scenario passed.
- Do not store credentials, personal data, or sensitive operational details in reports.

## Free-first upgrade sequence

1. **Baseline:** run the repository's existing local verification and unit tests. Record the exact command, commit, pass/fail count, and environment.
2. **Contracts:** test malformed inputs, missing/stale/conflicting observations, invalid confidence, unknown world state, human-review requirements, and fail-closed behavior.
3. **Deterministic simulation:** use small synthetic scenarios and fixed seeds; test both expected success and expected failure.
4. **Evidence:** report only metrics actually measured on a documented evaluation set. Label synthetic results as synthetic and simulation-only.
5. **Optional resources:** consider a model, simulator, or dependency only after manual licence, hardware, disk, network, and cost review. Nothing is downloaded automatically.
6. **Hardware:** no physical actuator control until separate safety engineering, hardware-in-the-loop testing, and human authorization are documented.

## Project-specific priorities

- **Coconut Harvest AI:** dataset provenance and licence review; image/hash and split integrity; maturity-label agreement; target-localization metrics; uncertainty/abstention and harvestability proposal tests. Do not claim real-time performance or validated tree-height reach without measurements.
- **Extreme Flood Rescue AI:** stale/conflicting sensor tests; communication-loss safe-hold; unknown water/current limits; person/animal candidate uncertainty; route and multi-agent toy scenarios. Toy grids are not flood physics, buoyancy, or validated rescue capability.
- **Multimodal Narcotics Screening AI:** modality-missing tests; sensor provenance and calibration status; uncertainty and abstention; human-review routing; false-positive/false-negative evaluation on a lawfully sourced, documented dataset. Chemical identification remains conceptual unless validated evidence exists.

## Cost transparency

This document is a project policy, not a guarantee about a GitHub account's billing settings or third-party terms. Public-repository standard GitHub-hosted runners are documented as free by GitHub, but larger runners and some storage/services can have separate costs. Check the account's billing dashboard before enabling any new service. If a cost cannot be ruled out, keep the feature disabled.

## Status labels

Use **IMPLEMENTED** only when code exists; **TESTED** only for a recorded test; **MEASURED** only for a reproducible metric; **SIMULATION-ONLY** for synthetic or simulator outcomes; **PROPOSED** for planned work; and **NOT VALIDATED** for unverified real-world capability.
