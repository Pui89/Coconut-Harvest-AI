# PUI89 Free-First Technology Stack (Recommended)

This is a staged recommendation, not a claim that every component is installed or tested. Keep the current working code until a replacement passes local checks.

## Default foundation
- Python standard library: deterministic contract tests, validation, failure reports and synthetic scenarios without extra packages.
- Python 3.12 or 3.13 for compatibility where dependencies need time to catch up; do not upgrade project environments just to chase the newest release.
- Git and documented manual test commands for reproducibility. Keep GitHub Actions disabled or absent unless the owner explicitly approves the cost and workflow.
- JSON/CSV evidence records with explicit labels for synthetic, simulated and measured results.

## Optional technologies — review before adoption
- OpenCV: image processing when needed; review the exact package licence, dependencies and install size first.
- ONNX Runtime CPU: optional local inference for a compatible, licensed model; do not download a model automatically. The runtime alone does not provide a model or prove accuracy.
- ROS 2 Jazzy + its compatible Gazebo release: only for a later robotics simulation stage, preferably on a supported Ubuntu 24.04 environment. ROS 2 Jazzy is an LTS release supported through May 2029. Do not assume this stack installs cleanly on every Windows setup.
- Local VLM/VLA: research only after model licence, weight source, size, VRAM/RAM, disk use and offline operation are reviewed. Mock interfaces first; no cloud inference.

## Selection rule
Prefer the newest **stable and supported** version that works with the project's tested dependencies and hardware—not the newest version number. Test upgrades in an isolated environment, keep a rollback path, pin reviewed versions, and measure latency, memory, failures and task success before claiming performance.

## Project-specific use
- Coconut Harvest AI: image provenance and label checks, maturity/localization contracts, uncertainty-aware harvest proposals; cutting stays disabled until validated safety gates exist.
- Extreme Flood Rescue AI: deterministic world-state and sensor-failure tests, stale/conflicting input handling, communication-loss safe-hold; 15 m is a simulation target only.
- Multimodal Narcotics Screening AI: modality provenance/calibration, missing-sensor and abstention tests, false-positive/false-negative evaluation, human review; chemical detection remains conceptual until validated.

## Cost and safety boundary
No paid API, subscription, cloud GPU, scheduled workflow, automatic dataset/model download or artifact upload by default. Before adding any dependency, check its licence, security advisories, download size, hardware needs and any possible service charges. If cost or licence is unclear, do not add it.
