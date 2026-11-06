# PUI89 Universal SHIELD
**Standard:** PUI89-USS-1.0  
**Scope:** All six PUI89 projects  
**Status:** Cross-project engineering and software governance standard; not a physical safety certification.

## Mission
Protect people, animals, assets, data, and project integrity through evidence-led risk detection, prevention, warning, containment, response, and recovery. Apply one governance model and shared intelligence interfaces across all six projects without duplicating the PUI89 AI Core.

## Six-project scope
1. Coconut Harvest AI — agricultural perception and harvesting-robot concept.
2. Flood Rescue AI — flood/disaster rescue-robot concept.
3. Multimodal Narcotics Screening AI — multimodal screening decision-support and robotic concept.
4. Homeguard AI Nomad — home/environment monitoring platform and future robot concept.
5. AI Car — vehicle intelligence and driver-assistance research.
6. AI Motorcycle — rider-focused vehicle intelligence research.

## 1. Physical safety and environmental protection
Maintain a hazard register for people/animal exposure, pinch/crush/cut/impact, entanglement, falls, collision, instability, environmental exposure, maintenance, transport, and foreseeable misuse. Define the operating domain, exclusions, safe states, emergency-stop/isolation concept, and human authority before implementation. Use simulation and non-actuating prototypes first. Document ingress, dust, vibration, shock, impact, corrosion, UV, temperature, humidity, and structural-load requirements as applicable. Controlled engineering tests are required before claiming physical protection or operational capability.

## 2. Fire, water, electrical and battery protection
Analyze water ingress, flooding, fire/heat, smoke, electrical shock/short circuit, overcurrent, insulation failure, battery damage, charging faults, and thermal runaway. Specify measurable requirements, detection limits, containment, isolation, evacuation/withdrawal, and recovery. Treat water and fire resistance as design/test requirements, not properties created by AI. Never claim an IP rating, waterproofing, fire resistance, battery safety, or certification without applicable independent physical test evidence. Software alerts do not replace certified alarms, protective equipment, emergency services, or trained responders.

## 3. Cybersecurity and anti-tampering
Apply least privilege; protected default branches and reviewed changes where configured; secret hygiene; input validation; detection of malformed, replayed, spoofed, stale, conflicting, and tampered evidence; provenance for datasets/models/configuration; dependency/license/workflow review; and incident response (identify, contain, preserve evidence, revoke/rotate credentials, recover from trusted state, test, document). Use available no-cost repository controls only. Do not enable paid plans, scanners, metered services, or billing features.

## 4. Hazard prediction and early warnings
Each risk record includes hazard, affected party/asset, observed evidence, source/time, likelihood estimate, severity, exposure, uncertainty, confidence, warning threshold, recommended action, and expiry. Separate observations from inferences/predictions. Display unknown when evidence is inadequate. Escalate stale, contradictory, low-quality, out-of-distribution, or integrity-compromised inputs. Measure false positives/negatives; do not claim predictive accuracy without representative validation.

## 5. Emergency response and recovery
Document detection/trigger, safe-state recommendation and prohibited actions, human notification/escalation, emergency-service boundary, isolation/containment, evidence preservation, recovery/inspection/restart authorization, and post-incident review with regression tests. Never delay emergency services in immediate danger. AI must not autonomously perform enforcement, rescue, medical, or safety-critical physical actions under this standard.

## 6. Shared AI Core across all six projects
Use one canonical, versioned PUI89 AI Core. Each project records the compatible core version/commit. Do not fork or silently redefine contracts.
- **Observation:** source, timestamp, value, units, quality, confidence, calibration, provenance, integrity status.
- **WorldState:** estimated state/entities, freshness, uncertainty, evidence references, operating domain, limitations.
- **ActionProposal:** advisory proposal, rationale, supporting evidence, confidence, expiry, required human authority, prohibited actuation.
- **FailureReport:** failure mode, severity, detection evidence, containment, recovery recommendation, unresolved risk.
Shared interfaces include input validation, evidence integrity, provenance/audit, uncertainty propagation, calibration, risk scoring, safety gates, degraded-mode handling, benchmark records, and consistent incident reporting. Project adapters may map local sensors into canonical contracts but must not create a competing core.

## 7. Automated testing, benchmarks and evidence
Provide a dependency-light, reproducible test path. Include unit, contract, integration, regression, negative, and failure-mode tests as appropriate. Test missing, noisy, stale, contradictory, malformed, corrupted, spoofed, and out-of-domain inputs; safety gates, authority boundaries, warnings, emergency states, and recovery. Record benchmark definition, dataset provenance/license, split method, baseline, sample size, metrics, uncertainty, limitations, environment, commit, and date. Use synthetic or lawfully sourced fixtures. CI must use minimal permissions and no paid runner/service. Passing software tests do not prove physical safety or real-world performance.

## 8. Strict zero-cost development
No paid APIs, subscriptions, cloud GPUs, metered services, paid datasets, or billable hosting by default. Check licensing, resource needs, security, and cost before package installation, model download, workflow expansion, or external service activation. Prefer existing code, standard-library solutions, synthetic tests, and free native GitHub features. No unexpected GitHub billing, paid CI minutes, or paid security features. If a requirement cannot be met at zero cost, mark it blocked/proposed; do not silently choose a paid alternative.

## 9. Evidence and capability status
Use exact labels: **Proposed**, **Implemented**, **Simulation-tested**, **Bench-tested**, **Field-tested**, **Independently validated/certified**. Upgrade status only with evidence. Public claims must state test conditions and limitations. Never infer waterproof, fireproof, secure, autonomous, real-time, roadworthy, rescue-capable, or certified status from a concept or software test.

## 10. Required SHIELD review report
Report known/verified, unknown/unobservable, changes, failures/near misses/unsupported cases, remaining risks and required human action, recommendations, evidence of improvement, and cost/dependency/security observations.

## 11. Project-specific hazard extensions
- **Coconut Harvest AI:** falling coconuts/tools, cutting/pinch zones, worker/animal exclusion, height/reach limits, tree/branch uncertainty, dropped-load containment.
- **Flood Rescue AI:** current, depth, debris, entrapment, capsizing, tether/anchor failure, battery isolation in water, rescuer exposure, communications loss, safe withdrawal. Depth/current capability requires measured evidence.
- **Multimodal Screening AI:** false positives/negatives, modality disagreement, calibration, dataset bias/provenance, chain of custody, privacy, human review, no autonomous enforcement.
- **Homeguard AI Nomad:** electrical/fire/water/mold and structural-warning uncertainty, false alarms, privacy, offline operation, safe charging, emergency escalation.
- **AI Car:** collision exposure, vulnerable road users, vehicle electrical/thermal hazards, occupant privacy, degraded sensing, no direct steering/throttle/brake control.
- **AI Motorcycle:** rider vulnerability, two-wheel stability/traction context, road-surface contamination, weather/visibility, distraction minimization, no direct steering/throttle/brake control.

## 12. Implementation gates
1. **Specify:** requirement, operating domain, hazards, authority boundary, cost review.
2. **Design:** contracts, evidence path, failure modes, safety gate, recovery.
3. **Implement:** minimal dependencies, secure defaults, documentation.
4. **Test:** automated negative/regression tests and benchmark protocol.
5. **Review:** evidence, limitations, privacy/security, human oversight.
6. **Release:** status label, change log, rollback/recovery path, no unapproved cost.

**PUI89 SHIELD principle:** prevent harm, detect uncertainty early, warn clearly, preserve human authority, recover safely, and prove every claim with evidence.
