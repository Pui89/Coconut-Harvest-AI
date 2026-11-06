# PUI89 Shared Technology Standard
Version 1.0 | Reviewed 2026-11-06
Applies to every current and future PUI89 project and the shared PUI89 AI Core.

## 1. Purpose
Adopt high-quality, current, evidence-backed AI and engineering resources while preserving strict zero-cost development, non-Chinese provenance, security, privacy, safety, maintainability and reproducibility. This is an adoption gate and research catalogue: listing a resource does not mean it has been installed, downloaded, enabled, benchmarked or approved for production.

## 2. Mandatory resource-adoption gate
Before adopting any tool, model, dataset, API, package, GitHub Action, service, simulator or hardware design, record:
- Exact name, version/revision, official source, publisher and evidence of origin/country.
- Separate licences for source code, model weights, tokenizer, training data, datasets and redistribution.
- Total cost, usage/rate limits, storage, bandwidth, compute, egress, trial expiry, auto-renewal, billing triggers and payment-card requirements.
- Data sent to provider, retention, telemetry, privacy, security posture and requested account permissions.
- Hardware/RAM/VRAM/disk/OS/runtime/energy requirements.
- Vulnerabilities, maintenance, provenance, checksums/signatures where available and dependency chain.
- Reproducible task-specific evaluation, limitations, failure modes and human-oversight requirements.

Decision states:
- APPROVED: all gates verified, compatible, free for intended use, non-Chinese origin and evidence recorded.
- TRIAL-ONLY: isolated evaluation with synthetic/non-sensitive data and explicit limits.
- UNVERIFIED — DO NOT USE: any unresolved origin, licence, cost, data, security or hardware question.
- REJECTED: violates PUI89 policy or unacceptable risk.

"Free", "open", "open source" and "open weights" marketing labels are not sufficient evidence.

## 3. Strict zero-cost and non-Chinese policy
Prohibited: paid APIs, subscriptions, cloud GPUs/compute, metered services, paid datasets/licences/storage/support; free trials that convert to paid plans; automatic upgrades; unexpected or retrospective billing; and unreviewed third-party actions, model downloads or package installations. Exclude Chinese-origin models, providers, tools, platforms, datasets, infrastructure and services. If origin, ownership, licence, price or data handling is unclear, stop at UNVERIFIED — DO NOT USE. Prefer local/offline, small-footprint, standard-library-first work. Do not add a dependency merely because it is fashionable.

## 4. Non-Chinese AI research candidates (not approved for deployment)
| Candidate | Verified public facts | PUI89 disposition |
|---|---|---|
| Google DeepMind Gemma 4 | Open weights; Apache-2.0; multimodal family with E2B/E4B edge variants and larger models. | PRIORITY RESEARCH CANDIDATE. Evaluate E2B/E4B only after checking exact quantized file size, runtime, RAM/VRAM and model-card terms. Do not download without a measured hardware fit. |
| Meta Muse Glimmer | Meta describes a 30B open-weight agentic model under Apache-2.0 for local agent workflows. | RESEARCH ONLY. Not a practical assumption for low-memory hardware; no cloud hosting. |
| Reflection Beam | Reflection describes open weights under Apache-2.0 for coding, reasoning and long-horizon agentic work. | RESEARCH ONLY until exact model size, weights terms, runtime, origin and reproducible benchmarks are checked. |
| OpenVLA 7B | MIT-licensed vision-language-action research model from a team including Stanford, UC Berkeley, Google DeepMind and Toyota Research Institute. Its model card states limitations on unseen robot embodiments. | SIMULATION-ONLY. No physical actuation. Check component/data licences and hardware before use. |
| Physical Intelligence OpenPI / pi-family | Open robotics VLA research code and checkpoints; requirements and checkpoint terms vary. | UNVERIFIED PER CHECKPOINT until exact code/weight/data licences, origin and hardware are verified. Simulation only. |

Official references:
- Gemma 4 release: https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/
- Gemma 4 model card: https://gemma.ai/models/gemma-4/model-card/
- Gemma 4 technical overview: https://ai.google.dev/gemma/docs/core
- Muse Glimmer: https://research.meta.ai/blog/introducing-muse-glimmer-open-agentic-model
- Reflection Beam: https://reflection.ai/blog/beam-is-available
- OpenVLA model card: https://huggingface.co/openvla/openvla-7b
- OpenVLA source: https://github.com/openvla/openvla
- OpenPI source: https://github.com/Physical-Intelligence/openpi

Open weights are not a free hosted API. Code, weights, tokenizer and datasets may have different terms. No model may make operational or safety-critical decisions until PUI89 has task-specific benchmarks and safety evidence.

## 5. Free/open security and engineering candidates
Evaluate official projects first; do not install automatically:
- OSV-Scanner: local dependency vulnerability and licence checks; https://google.github.io/osv-scanner/
- Gitleaks: open-source secret scanner; https://github.com/gitleaks/gitleaks
- OpenSSF Scorecard: repository security-practice assessment; https://scorecard.dev/ and https://github.com/ossf/scorecard
- GitHub Dependabot/supply-chain features: verify current plan and repository-visibility limits before enabling; https://github.com/security/advanced-security/software-supply-chain
- OWASP Dependency-Check / Dependency-Track: https://owasp.org/www-project-dependency-check/ and https://owasp.org/www-project-dependency-track/

Pin and review action versions; use least-privilege workflow permissions; never expose secrets to untrusted pull requests; avoid automatic write permissions; and verify publisher, source, licence, release integrity and transitive dependencies. Do not enable paid tiers.

## 6. Robotics and simulation candidates
- ROS 2 and Gazebo: simulation-first interfaces; verify supported distribution and licences.
- NVIDIA Isaac Lab: framework published under BSD-3-Clause; check hardware and Isaac Sim/Omniverse terms separately. https://developer.nvidia.com/isaac/lab
- NVIDIA Isaac Sim: NVIDIA describes free/open-source Apache-2.0 availability while documenting additional software/materials terms and separate paid redistribution/cloud costs. No cloud services or paid redistribution. https://developer.nvidia.com/isaac/sim

Do not install heavy simulators on constrained machines. Keep robot/car/motorcycle interfaces in mock or simulation mode. No direct hardware actuation, road/rescue deployment or safety-critical control from an unvalidated AI model.

## 7. Shared PUI89 AI Core contracts
Reuse one versioned design rather than incompatible project-specific duplicates:
- WorldState: timestamp, source, coordinate/frame context, observed facts, uncertainty and freshness.
- Observation: sensor/source identity, payload reference, calibration, quality, provenance and missing-data flags.
- ActionProposal: proposed action, preconditions, risk, confidence, expiry and required approvals. A proposal is never an execution command.
- FailureReport: failure class, severity, evidence, affected component, containment and recovery state.

Cross-cutting capabilities: Evidence Integrity; provenance; uncertainty propagation and calibration; missing/noisy/conflicting evidence handling; human review; safety gates and fail-closed defaults; emergency stop/safe state; reproducible benchmarks and tests; change/deterioration/predictive maintenance; cybersecurity, secrets protection, dependency provenance, backup/recovery; clear status labels (implemented, tested, passed, failed, proposed, blocked, unverified).

## 8. Project-specific application map
| Project | Priority applications |
|---|---|
| Coconut Harvest AI | Multimodal perception; maturity classification; uncertainty-aware detection; arm/gripper simulation; worker/animal safety; orchard robustness; predictive maintenance. |
| Flood Rescue AI | Multisensor world-state; water/current/terrain simulation; resilient navigation; communications-loss handling; stability modelling; human-authorized proposals only. |
| Multimodal Screening AI | RGB/approved sensor fusion; provenance/calibration; uncertainty and human review; false-positive/negative benchmarks; privacy/audit trail; no autonomous enforcement. |
| Homeguard AI Nomad | Heat/water/humidity/smoke/electrical/structural sensor fusion; anomaly/change detection; explainable alerts; offline-first; privacy and false-alarm controls. |
| PUI89 AI Robot Car | Perception, world-state, agent planning, simulation, predictive maintenance, cybersecurity and human override; no unvalidated road deployment. |
| PUI89 AI Robot Motorcycle | Rider-centric perception, stability/hazard simulation, fault detection, battery/electrical protection and human override; no unvalidated road deployment. |

## 9. Evidence and release gates
Documentation is not proof of implementation. For each capability record code/config path, test/benchmark and version, command/environment, expected/actual result, evidence/log reference, limitations, unresolved risks, reviewer and date.

Release gates: resource provenance/licence/cost review; security review; unit/integration tests; negative and fault-injection tests; simulation evaluation; performance/resource-budget checks; human safety review; rollback/recovery documentation.

## 10. Adoption workflow
Discover from official non-Chinese sources; verify origin/licences/cost/privacy independently; check hardware fit before download; compare with a simple baseline on fixed benchmarks; record limitations; propose isolated changes; test and review security; approve per project only with evidence; recheck versions, pricing, licences and vulnerabilities before upgrades.

Last reviewed: 2026-11-06. Re-verify external facts before adoption because pricing, licences, availability and hardware requirements can change.
