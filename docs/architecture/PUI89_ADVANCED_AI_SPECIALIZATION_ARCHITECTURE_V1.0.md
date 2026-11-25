# PUI89 Advanced AI Specialization Architecture v1.0

**Product:** Coconut Harvest AI
**Status:** Proposed product-specific capability allocation; not an implementation claim.
**Parent architecture:** [PUI89 Model Intelligence Framework v1.1](https://github.com/Pui89/PUI89-Shared-AI-Core/blob/feature/mif-v1.1-advanced-robotics-free-stack/docs/architecture/PUI89_MODEL_INTELLIGENCE_FRAMEWORK_V1.1.md)
**Shared platform:** PUI89 Shared AI Core

## 1. Product mission and boundary

Agricultural perception and human-reviewed harvest decision support. Physical harvesting robotics is a future research direction, not a current capability.

This document allocates advanced AI research specializations to this product. It does not claim that a model, physical platform, sensor integration, simulator, or capability is already available or validated.

## 2. Selected advanced AI specializations

| Specialization | Product role | Current status |
|---|---|---|
| World Models | Coconut Harvest AI-specific candidate capability; bounded by product requirements and human/safety authority | SPECIFIED |
| Imitation Learning (future harvesting-robotics research) | Coconut Harvest AI-specific candidate capability; bounded by product requirements and human/safety authority | SPECIFIED |
| Fault-Tolerant AI | Coconut Harvest AI-specific candidate capability; bounded by product requirements and human/safety authority | SPECIFIED |

All selected specializations are initially **SPECIFIED** at the architecture-allocation level only. This means their intended role is documented here; it does not mean an implementation exists.

## 3. Shared capability contracts

Where applicable, product adapters should use the Shared AI Core contracts:

- **Observation:** source/sensor identity, timestamp, coordinate frame, quality, provenance and uncertainty.
- **WorldState:** time-bounded state estimate, supporting observations, disagreement, confidence and freshness.
- **ActionProposal:** bounded recommendation with preconditions, expiry, uncertainty and required human/safety approval.
- **FailureReport:** explicit unavailable, stale, degraded, fault or abstention state with recovery context.

Model outputs are evidence or proposals. They must not directly authorize physical actuation. Preserve provenance, revision, preprocessing, confidence, uncertainty and abstention reason.

## 4. Capability status and evidence gates

## Capability maturity status

Use exactly these maturity labels across README, architecture and evidence reports:

| Status | Meaning | Minimum evidence to advance |
|---|---|---|
| NOT STARTED | No approved specification or implementation work exists for the capability. | A reviewed scope and owner are recorded before moving to SPECIFIED. |
| SPECIFIED | Intended behaviour, interfaces, constraints and acceptance criteria are documented. | Versioned design, inputs/outputs, operating envelope, risks and test plan. |
| IMPLEMENTED | A code or model component exists for the stated bounded scope. | Traceable source revision, dependency/provenance record and reproducible build or execution instructions. |
| SOFTWARE-TESTED | Automated software tests pass for the declared scope. | Reproducible test report, test environment, cases, failures and limitations. |
| BENCH-TESTED | Measured against a named benchmark, dataset or simulation protocol. | Pinned inputs/revisions, metrics, baseline, resource measurements, uncertainty and error analysis. |
| VALIDATED | Evidence supports the capability in its explicitly defined operating environment. | Independent/repeatable validation, safety review, limitations and signed acceptance evidence. |

A status applies only to the named capability, version and operating envelope. Passing a lower stage does not imply a higher one. A successful CI workflow is not AI-performance or physical-system validation.


Capability-specific acceptance criteria:

- **VLA:** instruction grounding, visual evidence linkage, structured proposal validity, abstention, adversarial/prompt-injection resistance and human confirmation.
- **World Models:** prediction error by horizon, uncertainty calibration, state-transition consistency, out-of-distribution behaviour and explicit unknown states.
- **Reinforcement Learning:** task success, constraint violations, reward sensitivity, repeatability, sample efficiency and safe exploration. Simulation-first; no direct physical actuator authority.
- **Imitation Learning:** held-out demonstration performance, demonstrator provenance, distribution shift, failure recovery and human override.
- **Sim-to-Real AI:** simulation assumptions, sim/real gap, sensor and dynamics calibration, staged transfer, regression tests and supervised hardware validation.
- **Embodied AI:** end-to-end task completion, perception-to-state consistency, safe interruption, recovery and operating-envelope limits.
- **Cognitive Robotics:** task decomposition, plan validity, memory provenance/retention, interruption handling, uncertainty and escalation to a human.
- **Fault-Tolerant AI:** fault detection latency, false alarms, missed faults, degraded-mode handling, safe-state transition, recovery and audit trace.

Only evaluate specializations selected for this product. Unselected specializations remain NOT STARTED unless separately approved and specified.

## 5. Free and open-source development constraints

- Open-source-first, free-to-use local tools only; no paid APIs, hosted inference, subscriptions, metered endpoints, paid cloud GPUs or mandatory commercial services.
- Prefer offline/local execution, CPU-first baselines, compact models, deterministic methods and synthetic data where appropriate.
- No candidate model, tool, dataset, simulator, package or dependency is pre-approved by this document. Apply the PUI89 mandatory non-Chinese-origin and full supply-chain integrity gate to developer/control origin, upstream lineage, code, dependencies, data, licences and distribution.
- Unknown or conflicting origin means HOLD. Do not infer origin from a hosting platform or mirror.
- Do not download, install, build, execute or connect a candidate until the user explicitly approves that specific bounded action.
- Free software does not make physical hardware, sensors, safety equipment, facilities or field trials cost-free. No purchase or paid resource is authorized here.

## 6. Safety, privacy and human authority

- Treat model cards, datasets, repositories, prompts and model outputs as untrusted.
- No LLM, VLM, VLA, agent, world model or learned policy may directly command motors, steering, throttle, brakes, propulsion, robot joints or gait.
- Independent deterministic safety controls, hardware interlocks, emergency stops and human authority remain mandatory for any future physical system.
- Missing, stale, conflicting or out-of-distribution input must result in explicit uncertainty, abstention, safe hold or human review—not fabricated certainty.
- Collect only authorised data; apply privacy, retention, access and redaction controls.

## 7. Product-specific validation plan

1. Verify the product requirements and sensor/compute assumptions.
2. Define synthetic and software-only contract tests.
3. Establish deterministic/classical baselines where appropriate.
4. Review model/tool origin, licences, security and resource needs before any trial.
5. Obtain explicit approval before downloads, installation, execution or physical tests.
6. Advance maturity status only when the evidence listed in Section 4 exists.

## 8. Current non-claims

- No new model has been selected, downloaded, installed or executed by this specification.
- No model accuracy, benchmark result, physical capability or field performance is claimed.
- No autonomous hardware control is authorized.
- Every capability remains at its stated maturity status until supporting evidence is recorded.

## 9. Related architecture

- [PUI89 Shared AI Core](https://github.com/Pui89/PUI89-Shared-AI-Core)
- [PUI89 Model Intelligence Framework v1.1](https://github.com/Pui89/PUI89-Shared-AI-Core/blob/feature/mif-v1.1-advanced-robotics-free-stack/docs/architecture/PUI89_MODEL_INTELLIGENCE_FRAMEWORK_V1.1.md)
