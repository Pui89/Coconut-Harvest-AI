# PUI89 Advanced Technology Implementation Plan

**Project:** Coconut Harvest AI  
**Scope:** all four PUI89 applications, coordinated through one shared AI Core contract  
**Priority:** core first  
**Cost policy:** strict zero-paid-services, local-first, no automatic downloads  
**Status:** implementation plan and evidence index; not a claim that every advanced capability is implemented.

## 1. Architecture decision

PUI89 already contains reusable intelligence foundations. Do not create a second world-state engine, health gate, autonomy supervisor, reporting library, or simulation framework inside this project. Reuse the current implementations and make this project a domain adapter to the shared PUI89 report contract.

The cross-project contract is `schemas/pui89-intelligence-report.schema.json`. It must be byte-identical across all four repositories and cover the four project identifiers. This repository's existing domain-specific schemas remain in place and may extend the common contract; do not replace them.

## 2. Existing foundations to reuse

- `pui89_core/world_state.py`
- `pui89_core/health_gate.py`
- `pui89_core/planning.py`
- `pui89_core/reporting.py`
- `pui89_autonomy/supervisor.py`
- `pui89_autonomy/experiment_report.py`

Existing simulation and verification assets:
- `apps/pui89_app/test_local_to_simulation.py`
- `tests/test_gazebo_world_contract.py`

Existing domain adapters and evidence sources:
- `apps/pui89_app/local_first_pipeline.py`
- `docs/PUI89_COCONUT_MODEL_ADAPTER.md`

Other established PUI89 documents remain authoritative for detailed design, including `docs/PUI89_AI_CORE_CONTRACT.md`, `docs/PUI89_SHARED_CORE_CONTRACT.md`, `docs/PUI89_SHARED_INTELLIGENCE_WORKFLOW.md`, `docs/PUI89_SAFETY_AND_VALIDATION_GATES.md`, `docs/PUI89_FREE_FIRST_TECH_STACK.md`, and `docs/PUI89_ZERO_COST_UPGRADE_POLICY.md` where present. This plan links those sources instead of duplicating their implementation.

## 3. Domain adapter responsibilities

- maturity-stage assessment
- coconut bunch localisation
- worker/animal separation
- safe reach and capture-zone planning

The adapter translates domain observations into the shared world-state, evidence, uncertainty, risk, recommendation, safety-gate and verification fields. It must preserve missing data, timestamps, source identity, sensor quality and modality disagreement. It must not invent observations or convert uncertainty into a positive finding.

## 4. Core-first implementation sequence

1. **Contract convergence:** keep the same report schema in all four projects; validate JSON syntax and project identifiers.
2. **Core reuse:** call existing world-state, health-gate, planning, reporting and supervisor functions. Avoid parallel implementations.
3. **Adapter conformance:** map this project's existing outputs to the common report format without removing domain-specific schemas.
4. **Evidence and uncertainty:** record provenance, timestamps, calibration state, limitations, unknowns and conflicting inputs.
5. **Safety and human review:** fail closed on missing safety signals; keep high-impact decisions human-reviewed; prohibit CI and report tooling from issuing hardware commands.
6. **Deterministic regression:** test normal, missing, stale, malformed, conflicting, fault and recovery cases using fixed fixtures/seeds.
7. **Simulation integration:** use existing simulation workflows first. Add simulator-specific tests only where the simulator is already configured and licensed.
8. **Optional advanced adapters:** evaluate multimodal models, local inference, SLAM, motion planning, predictive monitoring and agent tools one at a time after license, resource and acceptance checks.

## 5. Technology adoption gates

Candidates include OpenCV, ONNX Runtime, PyTorch, ROS 2, Nav2, Gazebo, SLAM Toolbox and optional local vector retrieval. They are not mandatory dependencies and are not installed by this plan.

Before adoption, record:
- exact project, version and licence;
- commercial-use and redistribution implications;
- local CPU/RAM/disk requirements;
- offline behaviour and model/data provenance;
- measurable acceptance criteria and fallback behaviour.

For ROS 2 simulation, the official compatibility pairing for ROS 2 Jazzy is Gazebo Harmonic. Use the existing repository's configured distribution rather than upgrading the stack blindly. See https://gazebosim.org/docs/latest/ros_installation/ and https://gazebosim.org/docs/harmonic/install/.

## 6. Strict execution policy

- No paid APIs, subscriptions, cloud GPU or paid hosted databases.
- No automatic model or dataset downloads.
- No dependency installation in the lightweight registry audit.
- Do not introduce a new dependency when existing code or the Python standard library is sufficient.
- Review model, dataset and package licences before use.
- No physical actuator commands from CI, tests, agents or report generation.
- Unknown or conflicting evidence must produce an explicit review/hold state.

## 7. Automated verification and evidence

This project retains its existing test and security workflows. The advanced-technology audit checks only registry integrity and cost/safety policy. The shared-report contract tests check schema validity and project coverage. Existing domain regression and simulation tests remain the source of project-specific verification.

Each report should record project, commit, schema version, capability status, evidence references, test conditions, limitations and result. A capability is `FOUNDATION` when supporting code exists, `PROTOTYPE` when an executable prototype exists, and `VERIFIED` only when defined acceptance criteria pass with reproducible evidence. Documentation or a passing registry audit alone never qualifies as verification.

## 8. Release gates

A change is ready for merge only when:
- shared schema is valid and matches the other project copies;
- new audit and shared-contract tests pass;
- existing project tests pass or pre-existing failures are explicitly isolated and tracked;
- no paid service, auto-download or unreviewed dependency was introduced;
- all physical-safety and performance claims remain within the evidence.

## 9. Current project limitations

Coconut maturity and localisation remain dependent on approved representative data; harvesting mechanics and field safety are not validated.
