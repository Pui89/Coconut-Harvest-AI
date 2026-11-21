# Product Manual & Remote Companion Standard v1.0

**Product:** Coconut Harvest AI  
**Status:** approved development specification; not a claim that translated manuals, a mobile app, remote connectivity, or product hardware are already implemented or validated.  
**Applies to:** physical product packaging, offline documentation, digital manuals, and a future PUI89 Remote Companion application.

## 1. Customer commitment

Every shipped unit must include a clear, product-specific printed quick-start and safety guide in the destination-market language, plus a QR code and short readable URL for the complete digital manual. The printed guide must remain useful without a phone, account, app installation, or internet connection. The complete manual must also be available as a downloadable, versioned offline file.

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
- Printed multilingual Quick Start Guide, or a destination-language printed guide with a clear language-selection card.
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
