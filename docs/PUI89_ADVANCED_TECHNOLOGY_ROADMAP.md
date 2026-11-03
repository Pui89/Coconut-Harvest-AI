# PUI89 Advanced Technology Roadmap

**Project:** Coconut Harvest AI  
**Engineering status:** capability roadmap and governance specification; not a claim that all listed technology is implemented.  
**Operating principle:** free-first, local-first, evidence-first.

## Mission

Integrate advanced AI and robotics capabilities through a shared PUI89 engineering approach while preserving each project's domain-specific design. This repository's capability registry is the machine-readable source of truth for this roadmap.

## Capabilities tracked

1. **Multimodal perception and sensor fusion** — Images, text, audio and sensor streams; missing and conflicting modalities must remain explicit.
2. **World-state model and temporal event tracking** — Track entities, locations, timestamps, state changes and stale observations; never invent missing state.
3. **Uncertainty, abstention and calibration** — Expose confidence limits, calibration status and UNKNOWN/REVIEW_REQUIRED outcomes.
4. **Digital twin and physics-based simulation** — Use reproducible synthetic scenarios; simulation results are not field validation.
5. **SLAM, mapping and autonomous navigation** — Optional robotics integration; only activate with a compatible simulator/hardware profile and safety review.
6. **Motion, manipulation and mission planning** — Generate plans and safety constraints; no direct hardware actuation from this audit system.
7. **Predictive fault and anomaly detection** — Monitor sensor freshness, communication, battery and system-health signals where available.
8. **Tool-using agents and supervised workflows** — Agents may propose and evaluate tasks; require allowlisted tools, bounded actions and human approval for consequential actions.
9. **Multi-agent and multi-robot coordination** — Research/simulation only until communication, arbitration and fail-safe behaviour are validated.
10. **Safety verification and fail-safe decision gates** — Fail closed on missing or invalid safety signals; retain emergency-stop priority and human override.
11. **Offline/local model inference adapters** — Optional only; no model download or runtime activation by CI; check memory, hardware and license first.
12. **Evidence provenance and reproducible reports** — Record source, timestamp, version, dataset split, metric, test conditions and limitations.

## Technology candidates (not installed by this change)

- ROS 2 Jazzy / Nav2 — robot middleware and navigation.
- Gazebo Harmonic — physics-based robot and environment simulation.
- OpenCV — computer vision.
- ONNX Runtime — portable local inference.
- PyTorch — deep-learning research.
- SLAM Toolbox — mapping and localisation.
- Qdrant — optional local evidence retrieval.
- NVIDIA Isaac Sim — optional advanced robotics simulation.

These are candidates for evaluation, not approved dependencies. Check the exact version, licence, hardware requirements, redistribution terms, security posture and commercial-use obligations before adoption. This change does not install packages, download models, enable cloud services or add paid services.

## Project-specific engineering focus

- four-stage coconut maturity assessment
- fruit and bunch localisation
- 3D scene understanding and safe reach planning
- worker and animal separation
- harvest capture/drop-zone risk assessment

## Automation

The GitHub Actions workflow `.github/workflows/pui89-advanced-technology-audit.yml` checks the registry and governance policy on relevant pushes, pull requests and manual dispatch. It uses Python's standard library only and uploads a small JSON audit report.

The audit verifies registry integrity and policy constraints. It does **not** prove model accuracy, simulation fidelity, physical safety or product readiness.

## Evidence and status rules

- `ROADMAP`: planned; not implemented.
- `FOUNDATION`: supporting interfaces or documentation exist; capability not yet validated.
- `PROTOTYPE`: a prototype exists; evaluation is incomplete.
- `VERIFIED`: reproducible evidence is linked and reviewed against defined acceptance criteria.
- `BLOCKED`: blocked by missing data, licensing, safety, hardware or other prerequisites.

A capability cannot be marked `VERIFIED` without evidence references. Keep uncertain outputs as `UNKNOWN` or `REVIEW_REQUIRED`; do not silently convert them into positive detections.

## Cost, licensing and safety boundaries

- No paid API, subscription, cloud GPU or unapproved spend.
- No automatic model downloads or dependency installation in this audit workflow.
- Review licences before adopting or distributing any model, dataset, library or simulator.
- No direct hardware actuation from CI or from this registry.
- Missing or invalid safety signals must fail closed to `SAFE_HOLD`.
- High-impact decisions require qualified human review.

## Project-specific limitations

No cutting, gripping, actuator or robot movement is authorised by this software roadmap. Maturity labels and harvesting recommendations require representative, licensed, labelled field data and human confirmation.

## Next engineering sequence

1. Keep the shared report contract and safety gates consistent.
2. Implement and test capability adapters one at a time.
3. Add deterministic simulation scenarios where the relevant simulator is configured.
4. Benchmark against licensed, documented datasets and fixed evaluation splits.
5. Record failures, uncertainty, resource use and limitations.
6. Promote a capability's status only when the evidence supports it.
