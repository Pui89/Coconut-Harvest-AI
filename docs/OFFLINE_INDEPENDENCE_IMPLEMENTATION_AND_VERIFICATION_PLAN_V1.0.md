# Offline Independence Implementation & Verification Plan — Coconut Harvest AI

**Status:** Engineering specification and verification plan only. Hardware implementation, testing and validation are not claimed.

This plan is normative for product design reviews and must be reconciled with the product hazard analysis, applicable vehicle/robot standards and the exact hardware/software revision.

## Objective
Software-first orchard image assessment. When deployed on a supported local computer, image review, quality checks, four-class visual assessment and record creation may work offline. This repository does not establish a physical harvesting machine. Do not imply cutting, gripping or field robot operation.

## Minimum offline capability
Offline image import/review; local model only when installed and compatible; manual human review; local export; no cloud requirement. If model/runtime is unavailable, clearly mark AI assessment unavailable and retain manual review.

## Required deliverables
1. Product control inventory and local indication map.
2. Offline capability matrix identifying each function, its sensor/compute/power dependencies and whether it is local, optional-connected or unavailable.
3. Connectivity fault-response table covering phone absence, app failure, local radio loss, Wi-Fi loss, internet/cloud outage, stale data, authentication expiry and reconnection.
4. Product-specific hazard analysis for loss of communication, power, sensing, compute and local storage.
5. Printed manual and Quick Start & Safety Guide proof for each launch language and revision.
6. Local log format, retention policy, storage-full response and offline export/recovery procedure.
7. Verification report for the applicable OFF-01 through OFF-15 tests in the product manual appendix.
8. Defect register and release approval record.

## Mandatory engineering rules
- Core local operation and safety do not depend on phone, app, Wi-Fi, internet or cloud.
- Local physical stop and required safety interlocks override all remote commands.
- No stale, duplicated, expired or replayed command may cause action.
- Reconnection never resumes hazardous activity automatically.
- Restart begins in a defined safe state.
- Missing sensors, models or compute capacity produce explicit unavailable/uncertain status.
- Printed manuals contain all essential instructions; QR is supplementary.
- Customer recovery steps never bypass guards, interlocks or emergency stop.
- Vehicle steering, throttle, braking and propulsion remain under the validated vehicle control architecture; PUI89 remote app cannot actuate them.

## Verification record template
| Field | Required record |
|---|---|
| Test ID | OFF-01 … OFF-15 |
| Product/build | Hardware revision, firmware/software commit and configuration |
| Preconditions | Setup, fixture, battery/power state, safety observer |
| Procedure | Reproducible numbered steps |
| Expected result | Product-specific acceptance criteria |
| Actual result | Observed behaviour and measurements |
| Evidence | Log, photo/video, trace or report reference |
| Result | Pass / Fail / Blocked / Not applicable with rationale |
| Ownership | Tester, reviewer, date, defect ID and corrective action |

## Product-specific safe-state design
Do not choose a generic “power off” response. Derive the safe state from the product hazard analysis. For mobile robots, consider controlled stop/hold, obstacle/terrain state, braking/actuator behaviour and local operator takeover. For road vehicles, loss of PUI89 connectivity must not interfere with rider/driver control or OEM safety functions. For the current Coconut software-first milestone, preserve local image review and manual assessment; do not imply a harvesting machine exists.

## Release gate
This plan is complete as documentation only when reviewed and approved by the responsible engineering and safety reviewers. Product offline-readiness remains **Not yet demonstrated** until applicable tests pass on the actual product build with retained evidence.


## Detailed implementation and release checklist

- Build a product-specific offline capability matrix; identify every hardware, sensor, model, compute, storage and power dependency.
- Define physical controls, local indicators, STOP/E-stop and reset behaviour; keep these independent from phone/app/network/cloud.
- Define fault responses for phone absent, app crash, local radio/Wi-Fi/internet/cloud loss, stale data, expired authentication, sensor/model fault, low battery and power loss.
- Partition safety logic from remote services. Reject expired, duplicated, replayed and out-of-order commands; reconnect only after fresh state synchronisation and deliberate local authorisation.
- Define bounded local event logging, integrity, retention, storage-full/corrupt response and approved offline export.
- Supply complete printed User Manual and Quick Start & Safety Guide in-box; QR is supplementary. Test the manual-only workflow.
- Test OFF-01 through OFF-15 from the product manual on the exact build. Record build, preconditions, steps, expected/actual, evidence, tester/date, defects and disposition. N/A requires approved safety rationale.
- No offline-ready claim until applicable tests pass and safety/engineering reviewers approve. Documentation and simulation alone do not prove physical performance.

### Product-specific scope
- **Coconut Harvest AI:** Software-first orchard image assessment; local image review and compatible local inference may work offline. No physical harvesting machine or actuator operation is established.
- **PUI89 Sentinel:** Quadruped inspection concept; local operator control and physical stop must be independent of remote links. Motion link-loss response must be derived from hazard analysis and prototype-tested.
