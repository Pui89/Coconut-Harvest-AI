# Coconut Harvest AI — Product Hazard Analysis & Alert Rules v1.0

**Status:** Proposed product-specific engineering specification — qualified review required  
**Product:** Coconut Harvest AI  
**Parent:** PUI89 Unified Multimodal Alert & Notification Standard v1.0  
**Scope:** Local operator alerts, harvest-task decision support and proposed future robotic harvesting hazards

> Preliminary design analysis only. This is not a completed formal machinery risk assessment, safety case, certification or proof of installed protection. The physical robot configuration, actuators, cutter, battery, sensors, guards, site conditions and applicable standards have not been established here. No physical harvesting, autonomous cutting, 0–30 m reach, safety performance or alert hardware is claimed.

## 1. Product boundary

The current product direction is a local-first computer-vision decision-support workflow for four visible coconut groups: young green, mature green, yellow and brown. The workflow may report image quality, fruit candidates, maturity assessment, uncertainty and a human-review recommendation. Visible colour alone is not proof of physiological maturity.

An uncertain/review-required state is mandatory when evidence is insufficient, occluded, conflicting, stale or outside the validated operating envelope. Uncertainty is a decision state, not a fifth maturity class.

The proposed future robot concept includes mobile and harvesting machinery. Every mechanical hazard below is a hazard to assess, not an assertion that the corresponding component exists.

**Authority boundary**
- AI perception may report observations and propose a candidate task.
- The alert system communicates evidence, uncertainty, faults and recommended operator actions.
- The alert system does not authorize cutting, gripping, climbing, motion or other actuation.
- A separate, appropriately designed and independently validated safety/control system must govern hazardous energy and motion.
- Human approval does not replace guards, interlocks, exclusion zones, emergency stop or other required protective measures.
- Hazardous action must not automatically restart after a fault, power loss, communication recovery or emergency-stop reset.

## 2. Method and unresolved inputs

This first pass identifies foreseeable hazard families, possible harms, alert needs and required independent controls. It intentionally does not assign numeric risk scores, SIL/PL categories, probability values or universal severity from incomplete design data.

Before formal risk estimation, a qualified reviewer must establish:
1. Intended use, users, tasks, operating modes and prohibited use.
2. Robot mass, geometry, reach, speed, stability, brakes, arm/tool/load characteristics.
3. Cutter type, energy source, guarding, stopping time and maintenance isolation.
4. Battery chemistry, voltage/current, protection, charging and thermal limits.
5. Sensor identities, mounting, calibration, coverage, failure modes and diagnostics.
6. Orchard terrain, slope, weather, wind, visibility, tree condition, overhead lines and worker/public access.
7. Foreseeable misuse, single faults and reasonably foreseeable fault combinations.
8. Applicable Thai and target-market machinery, electrical, battery, EMC, radio, occupational safety and privacy requirements.

**Risk rating:** TBD pending the above. L1–L4 below are alert-presentation levels, not formal hazard-risk classes.

## 3. Preliminary hazard register

| ID | Hazard / initiating condition | Possible harm | Alert requirement | Independent control / design requirement |
|---|---|---|---|---|
| COC-H01 | Person or animal enters a harvesting/exclusion zone | Impact, crushing, entanglement, cutter injury or falling-object injury | Prominent warning; state zone status and required action; unknown coverage is explicit | Physical exclusion/guarding and independently validated protective sensing/stop function as required; AI detection alone is not protective |
| COC-H02 | Coconut, branch, tool or load may fall or release unexpectedly | Head injury, impact, property damage | Warn of falling-object risk, retention fault or unverified drop zone | Designed retention/collection path, exclusion zone, guarding and engineered load control |
| COC-H03 | Cutter or hazardous tool enabled unexpectedly or remains energised | Severe laceration, amputation or fatal injury | Distinct critical alert on unexpected enable, guard/interlock fault or stop-chain fault | Guarded tool, independent energy isolation, interlocks, lockout/isolation and deliberate reset |
| COC-H04 | Arm/base instability, tip risk, excessive load, jam or unexpected movement | Crush, impact, overturning, dropped load | Warning/critical alert according to approved hazard analysis | Mechanically verified stability envelope, brakes/holding, load limits and independent protective controls |
| COC-H05 | Collision, pinch or entrapment-zone obstruction | Injury or equipment damage | Obstruction warning; identify affected zone only when evidence supports it | Physical guarding, safe clearances and independently validated protective functions |
| COC-H06 | Invalid, stale, missing, occluded or conflicting camera/depth/position data | Incorrect target, reach or clearance decision | Sensor/perception fault or UNKNOWN; state harvest eligibility cannot be established | Fail closed: no cut or hazardous motion when required safety evidence is unavailable |
| COC-H07 | Wrong fruit/maturity class, uncertain identity or incorrect target association | Unwanted harvest or unsafe task | Candidate uncertainty/manual-review alert; never label uncertain fruit harvest-ready | Human review and independent task validation; maturity classification never authorizes actuation |
| COC-H08 | Localization, coordinate transform, reachability or workspace model invalid | Motion outside intended workspace or contact with nearby/overhead objects | Navigation/workspace fault; task inhibited pending review | Verified geometry, calibration, workspace limits, collision checking and independent motion limits |
| COC-H09 | Battery, wiring, motor, controller or electrical fault; overheating, smoke, water ingress | Fire, shock, burns, unexpected movement or loss of control | Equipment/thermal/electrical fault alert; action follows approved procedure | Qualified electrical/battery design, protection, isolation, enclosure review and controlled emergency procedure |
| COC-H10 | Operator link loss, computer crash, watchdog reset or power interruption | Unsupervised task, stale command, unexpected restart | Local system-fault alert where available; preserve recovery history | Pre-tested independent watchdog/safety chain; inhibit hazardous task; no automatic restart |
| COC-H11 | Unsafe weather, wind, wet/slippery ground, unstable tree/branch or overhead electrical line | Tip-over, falling objects, electrical contact or loss of traction | Site-condition caution/stop-work alert when supported by approved input or operator report | Site assessment and engineering-defined operating envelope; no numerical limits until validated |
| COC-H12 | Maintenance, jam clearing, charging or recovery while hazardous energy remains | Unexpected start, tool/arm movement or shock | Maintenance/isolation state and reset-required alert | Documented lockout/isolation, stored-energy control and trained maintenance procedure |
| COC-H13 | Alert channel failure or alert fatigue | Operator misses a serious condition | Channel-health warning; critical event uses independent approved path and suitable redundancy | Channel self-test, fallback, human-factors evaluation and independent safety function |
| COC-H14 | Unauthorized command, configuration change or compromised interface/update | Unexpected task or disabled safeguards | Security/configuration-integrity alert; inhibit task if integrity is uncertain | Authentication, least privilege, audit and safe recovery; AI alerting is not a cybersecurity control |

This register is preliminary and non-exhaustive. Qualified review must add hazards from the actual design, task observation, foreseeable misuse, applicable standards and site review.

## 4. Proposed Coconut alert rules

All rules below are proposed. Numerical thresholds, trigger latency, repeat intervals and hardware channels remain TBD until the physical design and hazard analysis establish them.

| Rule | Event / trigger evidence | Proposed presentation | Operator message/action | Task boundary |
|---|---|---|---|---|
| COC-ALR-001 | Fruit candidate detected with valid image evidence | L1 Information: text/icon; optional soft tone | “Fruit candidate detected. Review maturity and image.” | Inform only; never authorize harvest |
| COC-ALR-002 | Maturity assessment uncertain, occluded or conflicting | L2 Caution or explicit UNKNOWN | “Maturity uncertain. Capture a clearer view or request human review.” | No harvest eligibility |
| COC-ALR-003 | Candidate assigned one of four visible groups | L1 Information with class and evidence reference | “Candidate class recorded. Confirm before planning.” | Human-reviewed decision support only |
| COC-ALR-004 | Person/animal/obstacle reported in relevant work zone by approved source | L3 Warning or L4 Critical per validated hazard rule | “Work zone not clear. Keep clear and follow site procedure.” | No hazardous task; independent protective system governs stop |
| COC-ALR-005 | Required safety sensor missing, stale, unhealthy or contradictory | L3/L4 per hazard analysis; explicit UNKNOWN | “Safety evidence unavailable. Harvesting inhibited. Inspect system.” | No cut; no autonomous movement if safe navigation cannot be established |
| COC-ALR-006 | Workspace, reachability, position or calibration unverified | L2/L3 per hazard analysis | “Target position or workspace unverified. Do not approach or cut.” | No task authorization |
| COC-ALR-007 | Collection/retention readiness false or unknown | L3 Warning | “Collection path not confirmed. Harvest action inhibited.” | No cut |
| COC-ALR-008 | Cutter guard/interlock/energy-isolation fault or unexpected hazardous enable | L4 Critical via independent approved alarm path | “Critical tool-safety fault. Keep clear. Follow emergency/isolation procedure.” | Independent protective system acts; inspection and deliberate reset required |
| COC-ALR-009 | Motor/arm jam, unexpected movement, collision or instability | L3/L4 per hazard analysis | “Motion fault. Keep clear and follow recovery procedure.” | Hardware-specific stop/hold; inhibit cutter; no automatic restart |
| COC-ALR-010 | Battery/thermal/electrical warning from qualified source | L2/L3/L4 per component limits and hazard analysis | “Power/temperature fault. Stop task and follow equipment procedure.” | Independent battery/electrical protection remains primary |
| COC-ALR-011 | Operator link lost or control computer/watchdog fault | L3/L4 per mode and hazard analysis | “Control link/system fault. Task inhibited. Manual recovery may be required.” | Pre-tested loss-of-link response; no automatic resume |
| COC-ALR-012 | Unsafe site/weather/tree/overhead-line condition reported or detected by approved method | L2/L3/L4 per assessed hazard | “Site condition requires inspection. Do not proceed until cleared.” | Stop-work/human assessment |
| COC-ALR-013 | Alert output channel fails self-test or stops responding | L2/L3 channel-health alert; escalate if critical coverage inadequate | “Alert channel fault. Use verified alternative and inspect before operation.” | Do not start if required warning coverage is unavailable |
| COC-ALR-014 | Emergency stop activated or protective chain reports active | L4 Critical; latched state | “Emergency stop active. Inspect cause; authorised manual reset required.” | Hazardous outputs remain disabled; reset does not restart motion |
| COC-ALR-015 | Maintenance/lockout state active or maintenance access open | L1/L2 status, stronger alert if hazardous enable attempted | “Maintenance isolation active. Operation prohibited.” | Prevent task start through independent interlock where required |

The same event may map to different presentation levels depending on operating mode, exposure, evidence quality and approved hazard analysis. Do not map severity from model confidence alone. UNKNOWN must never be presented as clear, safe or L1 merely because the model is uncertain.

## 5. Five-channel policy

| Channel | Intended use | Fallback / limitation |
|---|---|---|
| Signal | Distinct local attention, warning and critical patterns where acoustically suitable | Must not imitate regulated emergency signals without authorisation; channel fault logged; critical path independently designed |
| Voice | Short Thai/English status and recommended action where language/output is evaluated | Advisory and optional; cannot delay critical alarm or authorize actuation; text/light/signal fallback |
| Light | Local status and warning indicators using colour plus patterns/labels | Colour alone insufficient; daylight/night visibility tested; no unapproved external warning light |
| Text | Integrated product display or normal local operator station; event, severity, uncertainty, action, timestamp and history | Works without phone/cloud; readable at operator position; essential information cannot be app-only |
| Image | Warning pictogram, maturity illustration, simplified work-zone diagram or relevant visual evidence | Supplementary; no indiscriminate capture; privacy/retention policy required; never delays critical alarm |

Essential alerts and local history must not depend on smartphone, internet, cloud or subscription. A phone may only be an optional mirror.

## 6. Product-specific state and action policy

This is a design policy for implementation and validation by the appropriate controller—not executable control logic.

| Condition | Alert outcome | Task decision boundary |
|---|---|---|
| Image-only maturity candidate, no physical robot task | Inform/review alert | Human-reviewed assessment only |
| Maturity uncertain or image quality poor | UNKNOWN/review required | No harvest eligibility |
| Required perception or safety input missing/stale | Sensor/evidence fault | No cutting; inhibit motion if safe navigation/safety cannot be established |
| Obstruction/person/animal in work zone | Warning/critical per assessed hazard | Independent safety system owns protective response |
| Cutter guard/interlock/E-stop fault | Critical latched alert | Independent hardware disables hazardous energy; no automatic restart |
| Arm/load/base instability or jam | Warning/critical per assessed hazard | Hardware-specific brake/hold/stop; do not assume abrupt power removal is safe |
| Communication loss or controller fault | System fault | Pre-tested loss-of-link response; manual recovery if safety state uncertain |
| Battery/electrical/thermal fault | Component-specific alert | Follow qualified component protection and emergency procedure |
| Maintenance isolation active | Maintenance status/operation prohibited | No task start until authorised inspection and reset |

No universal instruction such as “turn off all motors immediately” is specified. Actual safe response must account for arm/load holding, slope, brakes, stored energy, cutter state and physical design.

## 7. Verification plan

Use controlled software fixtures and simulation first. Physical hazard testing requires an approved test plan, guarded area, qualified personnel, independent emergency stop, risk review and staged test authorisation. Never create real person/animal exposure, overhead cutting tests or improvised battery-abuse tests to exercise alerts.

| Test ID | Stimulus | Expected result | Evidence class |
|---|---|---|---|
| COC-ALT-T001 | Valid fruit-candidate event | L1 informational event with image/provenance reference; no actuator authority | Unit/integration |
| COC-ALT-T002 | Candidate maturity ambiguous | UNKNOWN/review-required; no harvest eligibility | Unit |
| COC-ALT-T003 | Image blurred, occluded or invalid | Quality warning; no forced maturity class | Unit |
| COC-ALT-T004 | Human reviewer changes class | Correction and reviewer provenance recorded; prior model output retained | Integration |
| COC-ALT-T005 | Person/animal zone input active in test fixture | Correct warning policy; alert does not substitute for independent protective stop | Simulation/HIL |
| COC-ALT-T006 | Required safety sensor removed or stale | Evidence unavailable/UNKNOWN; no task authorization | Fault injection |
| COC-ALT-T007 | Position transform/calibration invalid | Workspace/reachability rejected; no approach/cut proposal accepted | Unit/simulation |
| COC-ALT-T008 | Collection readiness false/unknown | Harvest task remains inhibited | Unit |
| COC-ALT-T009 | Cutter guard/interlock fault fixture | Critical alert and latched state; no application-level bypass | HIL/bench after approved design |
| COC-ALT-T010 | E-stop asserted in safe test fixture | Latched critical indication; reset does not restart task | HIL/bench under approved procedure |
| COC-ALT-T011 | Arm jam/instability fixture | Correct fault alert; hardware-specific safe response not guessed by app logic | Simulation/HIL |
| COC-ALT-T012 | Battery/temperature fault input | Component-specific message; no invented threshold | Unit/HIL |
| COC-ALT-T013 | Operator link lost | Loss-of-link event logged; approved policy selected; no automatic resume | Integration/fault injection |
| COC-ALT-T014 | Main process restart during active task | Task remains inhibited pending approved recovery | Integration/HIL |
| COC-ALT-T015 | Audible channel unavailable | Fault recorded; suitable text/light fallback; critical independent path unaffected | Integration/bench |
| COC-ALT-T016 | Display/text channel unavailable | Fault recorded; fallback used; task cannot start if required coverage inadequate | Integration/bench |
| COC-ALT-T017 | Light channel unavailable | Fault recorded; alternate channel policy applied | Integration/bench |
| COC-ALT-T018 | Voice/image enrichment stalled | Critical alert path not delayed | Fault injection |
| COC-ALT-T019 | Internet and smartphone disconnected | Essential local alerting and history remain available | Offline integration |
| COC-ALT-T020 | Alert acknowledged while hazard remains active | Alert remains active; acknowledgement is not resolution | State transition |
| COC-ALT-T021 | Quiet mode/minimum permitted volume selected | Required critical alert remains available through approved independent/alternate channels | State/human factors |
| COC-ALT-T022 | Duplicate event repeats while condition persists | Deduplication does not hide escalation or continuing active hazard | Unit/integration |
| COC-ALT-T023 | Thai and English message fixtures | Meaning, urgency and action equivalent for evaluated translations | Content/usability |
| COC-ALT-T024 | User unable to distinguish colours reviews warning | Severity/action distinguishable by pattern, icon, text and/or sound | Accessibility/human factors |
| COC-ALT-T025 | Unauthorised role requests private camera evidence | Access denied and audit event recorded | Security/privacy |
| COC-ALT-T026 | Controlled power loss/recovery | Hazardous task does not automatically resume; history/recovery follows approved policy | HIL/bench after design review |

For every test record requirement IDs, code/configuration, fixture, stimulus, expected/observed result, evidence, test type, status, defects, reviewer and retest. Unexecuted tests are NOT TESTED. Simulation pass is not physical safety validation.

## 8. Alert record fields

Each event should carry, where applicable:
- event ID, product ID, event type, rule ID and rule version;
- event and receive timestamps with documented clock source/time convention;
- source identity, provenance, sensor health/freshness and calibration status;
- image/scene reference and privacy classification (not raw image by default);
- affected zone/component and operating mode;
- evidence quality, uncertainty, conflict and UNKNOWN reason;
- underlying event severity plus user-facing L1–L4 presentation level;
- recommended operator action and task-inhibit reason;
- channels selected, presentation status and channel failures;
- acknowledgement actor/time, escalation, resolution evidence and recovery outcome.

History must be local, access-controlled and protected against silent alteration. Retention/deletion periods remain TBD pending privacy and operational requirements.

## 9. Open decisions and approval gates

- [ ] Actual robot configuration, mass, geometry, actuator/tool and cutter design identified.
- [ ] Intended use, operating modes, prohibited use and site envelope reviewed.
- [ ] Formal machinery hazard analysis completed by qualified reviewer.
- [ ] Exclusion zones, guarding, interlocks, emergency stop and energy isolation designed independently of AI.
- [ ] Safe braking/holding and stored-energy behaviour assessed for actual arm/base/load.
- [ ] Sensors, coverage, calibration, diagnostics and failure modes selected and evidenced.
- [ ] Battery/electrical/thermal protection and environmental limits reviewed.
- [ ] Alert thresholds, latency, repetition and escalation derived from risk analysis.
- [ ] Local display/signal/voice/light hardware and fallback evaluated.
- [ ] Thai/English content and accessibility evaluated.
- [ ] Privacy, image capture, access, retention and deletion rules approved.
- [ ] Test fixtures, instruments, acceptance criteria and qualified supervision approved.
- [ ] Required tests executed; failures closed or explicitly accepted by authorised reviewer.
- [ ] Release decision and public claims reviewed against evidence.

## 10. Current status and non-claims

| Item | Status |
|---|---|
| Shared alert architecture | Specified at portfolio level |
| Coconut preliminary hazard register | Proposed in this document |
| Coconut event/alert rules | Proposed in this document |
| Product-specific numerical thresholds | Not established |
| Selected alert hardware and integrated channels | Not established by this document |
| Independent physical safety system | Not validated by this document |
| Alert software implementation | Not established by this document |
| Verification tests in Section 7 | Not executed by creating this document |
| Physical harvesting safety / field validation / certification | Not demonstrated |

**Release boundary:** This is an engineering proposal for review. It is not permission to connect the current software prototype to motors, cutters, climbing mechanisms or manipulators. It does not authorise hardware purchases, installation, field operation or autonomous harvesting.
