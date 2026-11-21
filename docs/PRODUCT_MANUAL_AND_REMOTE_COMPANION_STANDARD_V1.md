# Product Manual & Remote Companion Standard v1.0

**Product:** Coconut Harvest AI  
**Status:** approved development specification; not a claim that translated manuals, a mobile app, remote connectivity, or product hardware are already implemented or validated.  
**Applies to:** physical product packaging, offline documentation, digital manuals, and a future PUI89 Remote Companion application.

## 1. Customer commitment

Every shipped unit must include both (1) the complete printed, product-specific User Manual and (2) a concise printed Quick Start & Safety Guide in the destination-market language. Both must be readable without a phone, QR scan, account, app, Wi-Fi or internet. The QR code and short readable URL are supplementary routes to the digital manual, updates and support; they must never replace printed instructions. A downloadable, versioned offline PDF/HTML edition is an additional copy.

Do not ship a product with machine-translated safety instructions that have not been reviewed by a competent technical translator and product safety reviewer.

## 2. Language coverage

### Required release baseline
- English — international master source.
- Thai — Thailand.
- Add destination-market languages before commercial shipment, according to the approved sales territory and local legal requirements.

### Market language plan
Target markets identified for this product: Thailand; India (Hindi, Tamil, Malayalam); Philippines (Filipino, English); Indonesia (Bahasa Indonesia); Vietnam; Sri Lanka; Brazil; global English.

Planned language coverage: English, Thai, Hindi, Tamil, Malayalam, Filipino, Bahasa Indonesia, Vietnamese, Sinhala, Spanish, Portuguese.

Language priority is a planning decision, not evidence of completed translation or confirmed customer demand. Add languages when market validation, distribution plans, and support capacity justify them. For India, select regional languages according to the actual state/customer audience; Hindi alone is not sufficient for every region.

### Translation quality controls
1. Maintain one version-controlled English master.
2. Use a product terminology glossary and translation memory.
3. Translate warnings, labels, procedures, and troubleshooting without changing technical meaning.
4. Have a native-language technical reviewer check each language.
5. Have a product/safety reviewer approve all safety-critical content.
6. Record language, document version, reviewer, approval date, and source revision.
7. Keep all language editions aligned to the same hardware/software revision; show a clear superseded-version notice.
8. Never use unreviewed automated translation as the final safety manual.

## 3. In-the-box documentation

Every retail/service package must contain:
- Complete printed User Manual in the destination-market language.
- Printed Quick Start & Safety Guide in the destination-market language, or a clear language-selection card when multiple editions are packed.
- Printed safety essentials: intended use, prohibited use, warnings, emergency stop/stop procedure, and local operator responsibilities.
- QR card and short URL to the official product manual, app instructions, support and current document revision.
- Product identification and hardware/software revision reference.
- Warranty/service information applicable to the destination country.

The full User Manual must include:
1. Product overview, intended use, limitations and specifications.
2. Unboxing, installation, charging/power and first-time setup.
3. Controls, indicators, status messages and normal operation.
4. Safety, emergency stop, safe states and recovery.
5. App pairing and account/device permissions, when available.
6. Remote connectivity requirements, offline behaviour and loss-of-connection response.
7. Cleaning, inspection, maintenance and approved spare parts.
8. Troubleshooting, fault codes, logs and support.
9. Data privacy, camera/microphone/sensor controls and data export/deletion.
10. Warranty, service, regulatory notices and revision history.

## 4. PUI89 Remote Companion App — shared requirements

**App name (working title):** PUI89 Remote Companion.  
**Status:** proposed shared application specification; not yet a released or implemented app.

The app should provide one customer interface for the six PUI89 products, while showing only features supported by the paired product and its verified hardware/software version.

### Core customer features
- Pair a product locally using a deliberate physical/on-device pairing action.
- View connection state, product identity, firmware/software version and device health.
- Open the correct language manual and product-specific quick-start steps.
- View alerts, fault codes, maintenance schedules and service history.
- View permitted telemetry, reports and diagnostic summaries.
- Manage authorized users, roles, notification preferences and privacy permissions.
- Download manuals and selected diagnostic reports for offline reference.
- Show last-updated time, stale-data warning and connection-loss state.
- Provide accessible language selection and clear units/date/time formats.

### Remote operation boundary
The app is a companion and supervisory interface, not a replacement for local controls or safety systems. Core product functions must remain available offline where the product design supports offline operation. Internet access must not be a prerequisite for emergency stop or safe shutdown.

Remote commands must be limited to explicitly approved, low-risk functions. Any movement or hazardous operation requires the product-specific local physical enable, local operator presence where required, safety interlocks, and a visible stop path. The app must never bypass an emergency stop, interlock, safe state, human approval, or local control.

Product-specific restrictions:
Inspection records, image review, maturity-assessment review, device health, dataset/software version, alerts, reports, maintenance reminders, and supervised job planning. Remote cutting/harvesting or actuator commands are prohibited in this product stage.

### Connectivity and security requirements
- Prefer local, direct pairing for initial setup; remote access is opt-in.
- Use authenticated, encrypted communication and per-device authorization.
- Apply least-privilege roles; separate owner, operator, service and read-only access.
- Provide revocation, session expiry, device unpairing and audit records.
- Do not expose credentials, tokens or sensitive diagnostics in manuals, QR codes or logs.
- Do not silently enable remote access or upload images, audio, location or telemetry.
- Clearly disclose which data leaves the device, destination, purpose and retention.
- On stale telemetry, communication loss, authentication failure or conflicting state, disable remote commands and show a clear warning.
- Do not rely on a cloud connection for emergency stop or essential local safety functions.
- Avoid single-vendor lock-in and unapproved third-party/cloud dependencies; review supplier, hosting and software provenance before selection.

## 5. User journey

1. Customer opens the printed Quick Start Guide.
2. Customer chooses the preferred language.
3. Customer reads safety essentials before powering or operating the product.
4. Customer scans the QR code or enters the short URL to open the correct manual.
5. If the app is available, customer installs it from an official, verified distribution channel and checks the app publisher/version.
6. Customer pairs locally using the product's physical/on-device pairing process.
7. Customer explicitly chooses whether to enable optional remote connectivity and data sharing.
8. Customer uses only functions supported by that product; the app explains unavailable functions rather than implying they exist.

## 6. Release gates — do not claim completion until evidence exists

- [ ] English master manual approved for the exact product revision.
- [ ] Destination-market language list confirmed for the actual launch territory.
- [ ] Each translated manual reviewed by a native-language technical reviewer.
- [ ] Safety warnings independently approved.
- [ ] Printed in-box quick-start and QR/short URL proof checked.
- [ ] QR destination, offline manual download and document version verified.
- [ ] App implementation and supported OS/device matrix tested.
- [ ] Local pairing, permissions, revocation and offline behaviour tested.
- [ ] Remote-command restrictions and connection-loss fail-safe tested.
- [ ] Privacy, security, data retention and support procedures reviewed.
- [ ] Customer usability test completed in each launch language.
- [ ] Country-specific legal, warranty, radio/connectivity and product requirements reviewed.

Until the relevant gate passes, label the item **planned**, **draft**, **in translation**, **under review**, **implemented**, or **validated** accurately. Do not describe the app as available or manuals as included in shipped boxes until production and packaging evidence confirms it.

## 7. Versioning and ownership

Store each language edition with a stable product/document ID, product revision, language code, version, release date, reviewer and change log. Keep a printable PDF and accessible HTML version. The QR code should resolve to a stable official product documentation page, not a temporary file link.

## 8. Immediate implementation sequence

1. Approve the English master structure and product-specific safety content.
2. Publish English and Thai digital manuals first.
3. Confirm target-country language priorities from actual launch plans.
4. Translate and independently review the next highest-priority languages.
5. Design and test the in-box printed quick-start/QR card.
6. Build the shared app shell around manuals, pairing, device status and diagnostics.
7. Add product-specific remote functions only after the relevant hardware and safety interfaces are validated.


## 9. Offline Independence & Connectivity Resilience — Product-Specific Requirements

**Normative reference:** [PUI89 Offline Independence & Connectivity Resilience Standard v1.0](https://github.com/Pui89/Pui89.github.io/blob/main/docs/PUI89_OFFLINE_INDEPENDENCE_CONNECTIVITY_RESILIENCE_STANDARD_V1.0.md). Apply the shared L0 fully-offline, L1 local-connection, L2 internet-connected and L3 remote-service model. L0 is the baseline; higher connectivity levels are optional.

### 9.1 Offline baseline
Local image import/capture where supported; image-quality checks; on-device maturity assessment only when the approved model, sensors and compute are installed; human review; local result display and storage. If AI resources are unavailable, preserve manual review/recording and mark automated assessment unavailable. Remote loss must not erase local work. No remote cutting, harvesting or actuator commands.

### 9.2 Required local design
- Printed Quick Start and Safety Guide accompanies every shipped unit; full manual is supplied in an offline-readable form. QR code and human-readable short URL are supplemental only.
- Physical local controls, local status/fault indication and the applicable stop/emergency-stop path must not depend on the app, Wi-Fi, internet or cloud.
- Identify the exact local AI/model/sensor/compute functions that remain available offline. Missing inputs, unavailable models, thermal/compute limits and stale observations must produce an explicit unavailable/unknown state, never a fabricated result.
- Store relevant records and fault events locally with defined capacity, integrity, retention and export/recovery behaviour.
- Document low-power, power-loss, restart and local service/recovery procedures. Restart must not replay stale remote commands or automatically resume hazardous work.

### 9.3 Connectivity-loss response
- Detect local-link, internet, cloud, remote-operator and telemetry-freshness failures separately.
- Reject delayed, duplicated, expired and out-of-order remote commands. Disable remote command acceptance when link state or data freshness is uncertain.
- Enter the product-specific safe state defined by hazard analysis. Reconnection must not automatically resume mobility or hazardous activity.
- The local stop and safety interlocks always override the app. No remote bypass is permitted.

### 9.4 Remote Companion boundary
Remote Companion is optional. It may expose only product functions implemented and verified for the connected hardware/software revision. No remote actuation that could create a hazardous condition is permitted under this specification. Remote diagnostics/status must be authenticated, encrypted, least-privilege, revocable and auditable.

### 9.5 Verification gates
Before claiming offline capability, test with no smartphone/app, radios disabled, no internet/cloud, link loss during active tasks, stale/duplicate/delayed commands, reconnection, local emergency stop, low power/power loss, restart, full/corrupt local storage, unavailable sensors/model and manual-only troubleshooting. Record exact build/configuration, procedure, expected/actual result, logs, tester, date and defects. A documented test checklist is not evidence of a passed test.

### 9.6 Status boundary
This appendix defines proposed engineering requirements only. Mark each item planned, specified, implemented, tested or validated based on evidence. Do not claim the product is fully offline, fail-safe, certified or commercially ready until its applicable release gates pass.


## 10. Engineering implementation contract (normative)

This section converts the offline principles into testable product requirements. It is a design specification, not evidence that hardware or software already implements them.

### 10.1 Independence boundaries
- **Safety independence:** emergency stop, protective interlocks, braking/steering/propulsion safety and safe shutdown must not depend on a smartphone, app process, Wi-Fi, internet, DNS, cloud service, remote operator or subscription.
- **Basic-use independence:** define a documented minimum-use case that a customer can complete using supplied physical controls and the printed manual alone.
- **AI independence:** identify each AI function as (a) local and available offline, (b) optional connected enhancement, or (c) unavailable without a service. Never describe category (b) or (c) as offline capability.
- **Service independence:** provide an authorised local diagnostic/recovery path and downloadable/printable service instructions. Remote support is optional.

### 10.2 Required control and indication design
For the exact product revision, create a control inventory with: control ID, physical location, action, operating state, feedback, hold/release behaviour, misuse protection, accessibility, and failure response. Define physical STOP and, where hazard analysis requires it, a latching emergency-stop device with deliberate manual reset. Reset must not itself restart motion or hazardous work. Provide local indication for power, ready, active, warning, fault, connectivity loss and safe/stop state using text/icons plus distinguishable light/sound patterns where appropriate. Do not rely on colour alone.

### 10.3 Local software and data architecture
- Partition safety-related control from app/remote/network services. Remote software must not have authority to override local safety logic.
- Keep essential control loops and required perception local. Document processor, memory, storage, model, sensor and power dependencies for each offline function.
- Store events in a bounded local log with timestamp source, sequence number, event severity, software/configuration version and integrity check. Define retention, full-storage behaviour, export and user privacy.
- On storage full/corrupt, preserve safety behaviour, surface a local fault and avoid silently overwriting protected evidence.
- Use monotonic sequence/expiry checks for remote requests. Reject expired, duplicated, replayed, out-of-order or unauthenticated commands. Reconnection must require fresh state synchronisation and explicit operator confirmation before any permitted activity.
- A restart must initialise to a defined safe state. Never restore a previous motion command as an active command.

### 10.4 Connectivity fault handling
Detect and distinguish: app crash, phone absent, Bluetooth/local radio loss, Wi-Fi loss, internet loss, cloud/service outage, authentication expiry, stale telemetry, sensor loss, model/runtime unavailable and low-power shutdown. For each fault define detection threshold, local indication, allowed functions, prohibited functions, safe response, recovery steps and event log. Remote loss must not be confused with loss of local sensing or loss of the vehicle's own control network.

### 10.5 Printed documentation and packaging
Each unit must include a complete printed User Manual and a printed Quick Start & Safety Guide in the destination-market language. The complete manual must cover: unpacking, installation, controls, normal operation, offline operation, no-phone operation, no-Wi-Fi/no-internet operation, safe stop/E-stop, power loss, fault indicators, troubleshooting, manual recovery, cleaning, maintenance, data/privacy, service and revision identification. QR and short URL are optional supplements only. The customer must be able to find the correct procedure from printed page numbers, contents and index without scanning anything.

### 10.6 Recovery and service
Document a tiered recovery path: user-safe checks; operator stop/isolation; authorised technician diagnostics; manufacturer service. Identify what must never be opened, bypassed, reset or repaired by the customer. Provide offline fault-code lookup, local log export using an approved physical/local method, configuration backup/restore rules and a service record. No recovery procedure may defeat guards, interlocks or emergency stop.

### 10.7 Verification matrix — mandatory evidence
Run and record each test against a specific hardware/software build. Use safe test fixtures and simulated faults before physical trials. Record setup, preconditions, steps, expected result, actual result, evidence/log reference, tester, date, severity and disposition.

| ID | Test condition | Acceptance criteria |
|---|---|---|
| OFF-01 | No smartphone and app not installed | Defined basic-use workflow and local stop remain available; no account prompt blocks operation |
| OFF-02 | Wi-Fi disabled and no internet route | Offline functions listed in the product capability matrix remain usable |
| OFF-03 | Cloud/DNS/service unavailable | No safety function or basic local workflow fails because of service dependency |
| OFF-04 | Remote/app process terminated during idle | Local controls and status remain correct; clear connection indication |
| OFF-05 | Remote/app link lost during active task | Product enters its hazard-analysis-defined safe response; no unsafe continuation |
| OFF-06 | Delayed, duplicated, replayed and out-of-order request | All stale/invalid requests are rejected and logged |
| OFF-07 | Connectivity restored after OFF-05 | No automatic motion/task resume; fresh state sync and deliberate local re-authorisation required |
| OFF-08 | Emergency stop activated with all radios off | E-stop/required stop path functions independently; reset does not auto-restart |
| OFF-09 | Power interruption and low-energy threshold | Product transitions safely; protected records remain consistent; no unexpected restart motion |
| OFF-10 | Local storage full or corrupted | Safety remains effective; local fault is indicated; protected evidence is not silently destroyed |
| OFF-11 | Required sensor or local AI runtime unavailable | Affected AI feature reports unavailable/uncertain; no fabricated result; safe fallback defined |
| OFF-12 | Printed manual only; no QR or phone | Representative user can find and complete the approved safe basic-use/recovery procedure |
| OFF-13 | Local service with no cloud | Authorised technician can retrieve allowed diagnostics and complete approved recovery |
| OFF-14 | Reboot after network loss/fault | Device starts in defined safe state and does not replay stale commands |
| OFF-15 | Wrong language/revision/manual supplied | Packaging release check detects mismatch before shipment |

**Pass rule:** all applicable tests must pass with evidence; not applicable tests require a documented product-safety rationale and approval. A checklist, simulation or design review alone does not prove hardware performance. Failed or blocked tests must remain visible with owner and corrective action.

### 10.8 Product-specific offline operating profile
**Coconut Harvest AI**
- Software-first orchard image assessment. When deployed on a supported local computer, image review, quality checks, four-class visual assessment and record creation may work offline. This repository does not establish a physical harvesting machine. Do not imply cutting, gripping or field robot operation.
- Offline capability boundary: Offline image import/review; local model only when installed and compatible; manual human review; local export; no cloud requirement. If model/runtime is unavailable, clearly mark AI assessment unavailable and retain manual review.

**PUI89 Sentinel**
- All-terrain inspection and exploration quadruped concept. Local operator controls, onboard status and physical emergency stop must remain independent of phone, radio and internet. Remote loss during motion must trigger a validated controlled stop/hold or other hazard-analysis-defined safe response; never assume immediate power removal is safe.
- Offline capability boundary: Local operator control; onboard mission/status/logging where implemented; local sensor/diagnostic review; physical E-stop; no autonomous resume after link recovery. Mobility, fall recovery and terrain responses require physical prototype testing.

**PUI89 AI HOME**
- Indoor four-wheel assistant concept. Local user controls and safety sensing must remain available without the app. On loss of remote connectivity, stop or safely hold mobility as determined by occupancy, obstacle and stability state; maintain essential local alerts where hardware supports them.
- Offline capability boundary: Local interaction, local sensing/alerts and local stop when implemented; no remote movement into occupied or unknown spaces; no autonomous resumption after reconnection; physical stop overrides all software.

**PUI89 AI NOMAD**
- Outdoor/mobile assistant concept. Local operator control and stop must be independent of remote connectivity. Loss of link during movement requires hazard-analysis-defined controlled stop/hold, obstacle-aware safe state and explicit local restart.
- Offline capability boundary: Local status, sensing and logs where implemented; location sharing is optional; no unattended remote driving; no movement based on stale route/mission commands; local recovery path required.

**PUI89 AI Global SUV**
- Vehicle concept with rider/driver-first control. Vehicle steering, throttle, braking, propulsion, lighting and OEM safety functions must remain independent of PUI89 app/cloud. Loss of PUI89 connectivity must not change driver control or trigger unsafe braking/steering/engine actions.
- Offline capability boundary: Driver-operated vehicle functions remain governed by the validated vehicle platform. PUI89 AI advisory functions may become unavailable with clear local indication. Never remote-start, steer, accelerate, brake, shift or move the vehicle under this standard.

**PUI89 AI Step-Through Scooter**
- Two-wheel rider-first scooter concept. Rider-operated steering, throttle, braking, propulsion, lighting and OEM safety functions must remain independent of PUI89 app/cloud. Loss of connectivity must not cause unexpected motion or control changes.
- Offline capability boundary: Rider retains direct control. AI advisory may become unavailable with clear local indication. Never remote throttle, steer, brake, activate ignition/motion or move the scooter under this standard.

### 10.9 Release gates
Do not mark offline-ready until: architecture review is approved; control and fault matrices are complete; local-only usability test passes; no-phone/no-network verification passes; E-stop/stop path is independently verified where applicable; stale-command and reconnection tests pass; printed manual and packaging proof are checked; service/recovery procedure is demonstrated; open safety defects are closed or formally accepted by authorised safety review.

### 10.10 Evidence and status labels
Use separate labels for **Specified**, **Implemented**, **Tested**, **Validated** and **Released**. Attach test records to each claim. Current repository documentation establishes requirements only unless a specific implementation and test artefact is linked. Never infer implementation from a README or specification.

## 10. Offline-first engineering implementation contract

This is a normative design and test specification, not evidence of implementation or validation.

### 10.1 Independence boundaries
- Safety controls, emergency stop, protective interlocks and safe shutdown must not depend on a phone, app, Bluetooth, Wi-Fi, internet, DNS, cloud or remote operator.
- Define a minimum customer workflow that works with the supplied physical controls and printed manual only.
- Classify every function as **local/offline**, **optional-connected**, or **unavailable**. State sensor, compute, model, storage and power dependencies. Never describe an optional-connected function as offline.
- Essential local control/perception must not be delegated to cloud services. Remote services cannot override local safety logic.

### 10.2 Physical controls and local indication
For each product revision, maintain a control inventory: ID, location, function, feedback, misuse protection and failure response. Provide physical STOP and, where hazard analysis requires it, a latching E-stop with deliberate manual reset. Reset must never restart motion or hazardous work. Provide local status/fault indication for power, ready, active, warning, fault, connectivity loss and safe/stop state. Use text/icons and distinguishable signals; do not rely on colour alone.

### 10.3 Local compute, storage and command integrity
- Partition safety-related control from app/network services.
- Essential local functions must list their compute, memory, model, sensor and power dependencies.
- Store bounded local event logs with timestamp source, sequence, severity, build/configuration ID and integrity check. Define retention, export, storage-full and corruption behaviour. Never silently overwrite protected evidence.
- Reject unauthenticated, expired, duplicated, replayed and out-of-order remote requests.
- After reconnection, synchronise fresh state and require deliberate operator confirmation before any permitted activity. Never replay a previous motion command.
- Restart into a defined safe state.

### 10.4 Connectivity fault matrix
Specify detection, local indication, allowed/prohibited functions, safe response, log event and recovery for: phone absent; app crash; local radio loss; Wi-Fi loss; internet/cloud/DNS outage; expired authentication; stale telemetry; sensor failure; model/runtime unavailable; low battery and power loss. Distinguish loss of PUI89 remote connectivity from faults in the product's own control/safety network.

### 10.5 Printed manual and in-box content
Every shipped unit includes a complete printed User Manual and a printed Quick Start & Safety Guide in the destination-market language. Essential instructions must be findable using contents, page numbers and index without scanning a QR code. Cover installation, physical controls, normal use, no-phone use, no-Wi-Fi/no-internet use, status indicators, stop/E-stop, connectivity loss, power loss, troubleshooting, manual recovery, maintenance, privacy, service and document revision. QR and short URL are optional supplements only.

### 10.6 Recovery and service
Provide tiered procedures: user-safe checks; operator stop/isolation; authorised technician diagnostics; manufacturer service. Define what customers must not open, bypass, reset or repair. Provide offline fault-code lookup and approved local log export. Recovery must never defeat guards, interlocks or E-stop.

### 10.7 Mandatory verification matrix
Run on the exact hardware/software build using safe fixtures and a safety observer where needed. Record preconditions, procedure, expected/actual result, evidence/log, tester, date, defects and disposition.

| ID | Test | Acceptance |
|---|---|---|
| OFF-01 | No phone; app absent | Basic-use workflow and local stop remain available; no account blocks use |
| OFF-02 | Wi-Fi disabled; no internet | All declared offline functions remain usable |
| OFF-03 | Cloud/DNS unavailable | No safety/basic local workflow depends on service |
| OFF-04 | App terminated while idle | Local controls/status remain correct; connection loss is indicated |
| OFF-05 | Remote link lost during task | Hazard-analysis-defined safe response; no unsafe continuation |
| OFF-06 | Delayed, duplicate, replayed, out-of-order command | Request rejected and logged |
| OFF-07 | Link restored after loss | No automatic motion/task resume; fresh state and deliberate local re-authorisation |
| OFF-08 | E-stop with all radios disabled | Stop works independently; reset does not auto-restart |
| OFF-09 | Low power/power interruption | Safe transition; records consistent; no unexpected restart motion |
| OFF-10 | Local storage full/corrupt | Safety remains effective; local fault shown; protected evidence not silently destroyed |
| OFF-11 | Sensor/model/runtime unavailable | Feature reports unavailable/uncertain; no fabricated output |
| OFF-12 | Printed manual only; no QR/phone | User can locate approved safe-use/recovery instructions |
| OFF-13 | Local service with no cloud | Authorised technician can retrieve allowed diagnostics and recover |
| OFF-14 | Reboot after fault/link loss | Defined safe startup; no stale command replay |
| OFF-15 | Wrong language/revision manual | Packaging check catches mismatch before shipment |

All applicable tests must pass with evidence. N/A requires a documented safety rationale and approval. A checklist or simulation alone does not prove physical performance.

### 10.8 Product-specific offline profile
Coconut Harvest AI: Software-first orchard image assessment. Offline image review, local inference only when installed and compatible, manual human review and local export may be supported. No physical harvesting robot is established; no cutting or actuator operation is implied.
PUI89 Sentinel: Quadruped inspection robot concept. Local operator control and physical stop must work without remote links. Link loss during motion requires a hazard-analysis-defined controlled stop/hold; mobility and terrain responses require prototype verification.

### 10.9 Release gate and status
Offline-ready may be claimed only after architecture/hazard review, control/fault matrices, no-phone/no-network usability, applicable OFF tests, stop-path verification, stale-command/reconnection tests, printed-manual proof and service recovery demonstration pass. Use distinct labels **Specified**, **Implemented**, **Tested**, **Validated**, **Released**. This repository change establishes specifications only; it does not claim hardware implementation or passed tests.

## 10. Engineering implementation and acceptance criteria

Specification only; this does not prove implementation or test completion.

### Independence and controls
- Essential local operation, protective interlocks, STOP/E-stop and safe shutdown must not depend on phone, app, Bluetooth, Wi-Fi, internet, DNS, cloud or remote operator.
- Define a basic-use workflow completed with supplied physical controls and printed manual only.
- Classify every feature as local/offline, optional-connected or unavailable, listing sensor, compute, model, storage and power dependencies.
- Maintain a control inventory (ID, position, action, feedback, misuse protection, failure response). Use physical STOP and, where hazard analysis requires, a latching E-stop with deliberate reset. Reset never restarts motion.
- Show local ready/active/warning/fault/connectivity-lost/safe states with text/icons and distinct signals; never rely on colour alone.
- Partition safety control from app/network services. Remote software cannot override local safety logic.

### Data, command and recovery behaviour
- Keep bounded local event logs with time source, sequence, severity, build/configuration and integrity check. Define retention, export, full-storage and corruption handling; never silently overwrite protected evidence.
- Reject unauthenticated, expired, duplicated, replayed and out-of-order commands. After reconnection require fresh state sync and explicit local authorisation; never replay an old motion command.
- Restart into a defined safe state. Document user-safe checks, operator stop/isolation, authorised technician diagnostics and manufacturer service. Recovery must not bypass guards/interlocks/E-stop.
- Define behaviour for absent phone, app crash, radio/Wi-Fi/internet/cloud loss, expired authentication, stale telemetry, sensor/model failure, low battery and power loss.

### In-box printed documentation
Every shipped unit includes a complete printed User Manual and Quick Start & Safety Guide in the destination-market language. Include no-phone/no-app/no-Wi-Fi/no-internet use, controls, indicators, stop/E-stop, connectivity and power loss, troubleshooting, manual recovery, maintenance, privacy and revision. Contents/page numbers/index must make procedures findable without QR. QR and short URL are supplementary.

### Mandatory OFF verification matrix
| ID | Test | Acceptance |
|---|---|---|
| OFF-01 | No phone/app | Basic-use and local stop work; no account blocks use |
| OFF-02 | Wi-Fi off/no internet | Declared offline functions remain usable |
| OFF-03 | Cloud/DNS unavailable | Safety/basic local workflow unaffected |
| OFF-04 | App terminated | Local controls/status remain correct; link loss shown |
| OFF-05 | Remote lost during task | Hazard-analysis safe response; no unsafe continuation |
| OFF-06 | Delayed/duplicate/replay/out-of-order command | Rejected and logged |
| OFF-07 | Reconnection | No automatic resume; fresh state and local re-authorisation |
| OFF-08 | E-stop with radios off | Stop independent; reset does not auto-start |
| OFF-09 | Low power/power interruption | Safe transition; no unexpected motion on restart |
| OFF-10 | Storage full/corrupt | Safety remains effective; fault shown; protected evidence retained |
| OFF-11 | Sensor/model/runtime unavailable | Explicit unavailable/uncertain; no fabricated output |
| OFF-12 | Printed manual only | User finds safe-use/recovery instructions without QR/phone |
| OFF-13 | Local service/no cloud | Authorised technician can inspect and recover |
| OFF-14 | Reboot after fault | Safe startup; no stale command replay |
| OFF-15 | Wrong manual language/revision | Packaging check catches mismatch before shipment |

Run on exact build with safe fixtures and safety observer where needed. Record setup, procedure, expected/actual result, logs, tester/date and defects. All applicable tests must pass with evidence; N/A requires approved safety rationale. A checklist or simulation alone is not proof of physical performance.

### Product profile
Coconut Harvest AI: Software-first orchard image assessment; local image review and compatible local inference may work offline. No physical harvesting machine or actuator operation is established.
PUI89 Sentinel: Quadruped inspection concept; local operator control and physical stop must be independent of remote links. Motion link-loss response must be derived from hazard analysis and prototype-tested.

### Release and status
Offline-ready requires approved architecture/hazard review, control/fault matrices, no-phone/no-network usability, applicable OFF tests, stop-path verification, stale-command/reconnection tests, printed manual proof and service demonstration. Use separate labels Specified, Implemented, Tested, Validated and Released. Current docs establish requirements only.
