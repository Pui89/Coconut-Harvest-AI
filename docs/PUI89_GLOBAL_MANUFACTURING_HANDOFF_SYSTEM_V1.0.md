# PUI89 Global Manufacturing Handoff System v1.0

**Status:** Mandatory engineering-control framework; not a product release or approved BOM.
**Revision:** 22 November 2026
**Applies to:** All PUI89 products, manufacturing partners, engineering contractors, inspectors, technicians and operators.
**Authority:** The latest approved, revision-controlled product documents and signed release records. This document never authorises a TBD item for procurement or production.

## 1. Purpose and non-negotiable rule

A qualified person who has not met the founder must be able to identify the exact product configuration, find the governing instructions, perform an assigned task, record the result and know when to stop. No person may fill a missing engineering value by assumption.

**STOP — DO NOT BUILD / BUY / SUBSTITUTE / OPERATE** when a required value, drawing, revision, acceptance limit, safety control or approval is missing, contradictory, obsolete or unreadable. Raise a documented Technical Query (TQ) or Non-Conformance Report (NCR). Work resumes only after the authorised engineering disposition is released.

## 2. Document hierarchy and precedence

1. Product Safety Requirements and approved risk controls.
2. Released Product Requirements Specification (PRS).
3. Released interface-control documents (ICD), drawings and CAD.
4. Released BOM and approved-source register.
5. Released manufacturing process, assembly and inspection instructions.
6. Released software/firmware configuration and test procedures.
7. Approved deviation/waiver and engineering-change records.
8. This common framework and product design briefs.

If two controlled documents conflict, stop the affected work and raise a TQ. Never choose the newest-looking file or infer precedence. The document-control owner resolves the conflict and issues a revision-controlled correction.

## 3. Universal identification and status

Every controlled item must show:
- Document or part ID; full title; product; revision; lifecycle status; issue date; owner; approver; language; units; page count; source file and change history.
- Status exactly one of: **DRAFT**, **IN REVIEW**, **RELEASED**, **SUPERSEDED**, **WITHDRAWN**.
- Evidence state exactly one of: **PROPOSED**, **SPECIFIED**, **TESTED**, **VERIFIED**.
- A released item must identify the approval record and the configuration it applies to.

A draft, comment, chat message, concept image, simulation or supplier suggestion is not production authority.

## 4. Requirement-to-evidence traceability

Each requirement receives a unique stable ID (example format: P89-[PRODUCT]-REQ-0001) and contains:
| Mandatory field | Meaning |
|---|---|
| Requirement | One unambiguous “shall” statement |
| Rationale / source | User need, hazard, law, interface or engineering basis |
| Applicability | Product, variant, serial/lot range and operating mode |
| Units / conditions | SI unit, environment, load, duty cycle and measurement conditions |
| Acceptance criteria | Numeric limit or objectively observable pass/fail condition |
| Verification method | Inspection, analysis, demonstration or test |
| Evidence | Report, data, drawing, certificate or record ID |
| Owner / approver | Named role, not an informal verbal approval |
| Status | Open, proposed, specified, tested, verified, waived (approved only) |

“High quality”, “rugged”, “waterproof”, “fast”, “safe” and “works in all countries” are not testable requirements until converted into measurable criteria and conditions.

## 5. Common hardware and component dictionary

Use these functional classes consistently across all products. A class is a category, not permission to procure a specific part.

| Class ID | Functional class | Required definition before release |
|---|---|---|
| MECH | Frame, chassis, brackets, housings, joints | Loads, geometry, material grade, process, finish, tolerances, inspection |
| MOT | Motor, actuator, gearbox, transmission | Torque/speed/duty, stall/fault behaviour, thermal limits, mounting, control interface |
| MOB | Wheel, tyre, track, caster, suspension, brake | Load, speed, traction, wear, environment, retention and failure behaviour |
| PWR | Battery, cells, BMS, power supply, DC/DC, charger | Chemistry, voltage/current/power, energy, protection, thermal limits, charging protocol, transport compliance |
| ELEC | PCB, MCU, CPU/GPU/NPU, memory, wiring, connector | Exact model/revision, electrical limits, pinout, EMC, thermal design, software compatibility |
| SNS | Camera, LiDAR, radar, IMU, encoder, environmental sensor | Range, accuracy, field of view, update rate, calibration, contamination and diagnostic behaviour |
| COM | Wi-Fi, Bluetooth, cellular, GNSS, wired network | Frequency/region, antenna, protocol, security configuration, approvals and fallback |
| THM | Heat sink, fan, duct, heater, insulation | Heat load, airflow, derating, temperature limits, ingress and service |
| SEA | Gasket, seal, membrane, cable gland | Material, compression, joint design, ageing, chemical compatibility and verified ingress test |
| HMI | Display, button, indicator, speaker, emergency stop | Human factors, visibility, accessibility, force, location, local language and safe state |
| SAF | Guard, interlock, bumper, brake, restraint, protective device | Hazard addressed, safety function, diagnostic coverage, validation and maintenance |
| CAB | Cable, harness, loom, grounding, shielding | Wire gauge, insulation, temperature, current, routing, bend radius, connector keying and test |
| SW | Firmware, drivers, models, runtime, configuration | Version/hash, dependencies, licence/provenance, hardware compatibility, rollback and test evidence |
| PKG | Packaging, transport restraints, labels | Handling loads, storage conditions, environmental protection, markings and transport rules |

For every actual BOM line, record at minimum: PUI89 part number; plain-language name; function; quantity; make/buy; exact manufacturer and model; manufacturer part number; datasheet revision; critical ratings; approved material/grade; finish/process; drawing and revision; interface/pinout; operating/storage/charging limits as applicable; country of origin/manufacture evidence; supplier and approved site; lot/serial traceability; lifecycle/obsolescence status; approved alternates; inspection method; acceptance criteria; and linked verification evidence.

No generic descriptions such as “industrial motor”, “high-grade aluminium”, “waterproof connector”, “AI camera” or “strong battery” may appear as a released procurement line.

## 6. Material and process definition

A released material callout must state the recognised material specification and exact grade/alloy, temper/condition where applicable, product form, thickness/section, mechanical/thermal/chemical properties required, coating/finish, joining method, process specification, inspection/certification evidence and traceability requirements.

A process callout must define the process, controlled parameters or allowable window, equipment/tooling, operator qualification where required, in-process checks, final acceptance criteria and records. “Equivalent material” or “same process” is not an acceptable substitution instruction.

Candidate materials in design briefs are for trade studies only. They are not approved purchasing instructions.

## 7. Interfaces and compatibility

Every mechanical, electrical, data, thermal and software interface must have a controlled ICD with:
- Interface ID and connected item IDs/revisions.
- Physical dimensions, datum, tolerance and mating/retention details.
- Voltage, current, power, grounding, protection and connector pinout.
- Signal level, protocol, timing, data format, units and error behaviour.
- Thermal, vibration, ingress and service constraints.
- Startup/shutdown sequence, fault response and safe state.
- Compatibility matrix and verified configuration.

Connector family alone does not prove pinout or electrical compatibility. Similar voltage does not prove battery/charger compatibility. Software compatibility requires a tested version matrix.

## 8. Manufacturing and operator work instructions

Each operation must have a unique operation ID and a controlled work instruction containing:
1. Operation purpose and prerequisites.
2. Required part numbers/revisions and incoming condition.
3. Tools, fixtures, gauges, PPE and calibration status.
4. Step-by-step sequence with annotated views or photographs.
5. Critical-to-quality characteristics and process parameters.
6. Torque/adhesive/cure/fastener values only from released engineering data.
7. Inspection point, method, sample size and pass/fail limits.
8. Expected record, traceability label and sign-off.
9. Abnormal condition, stop-work trigger and escalation path.
10. Rework/repair instruction or explicit “no rework permitted”.

Never infer torque, adhesive, clearance, cable routing, polarity, firmware version or calibration from appearance or experience.

## 9. Quality control and production acceptance

A product-specific Control Plan must link each critical characteristic to its requirement ID, process step, measurement method, gauge ID/calibration, sampling frequency, acceptance limit, reaction plan, record and responsible role.

Minimum controls, where applicable:
- Supplier qualification and incoming inspection.
- Material and certificate verification.
- First-article inspection (FAI) against released drawings.
- In-process inspection and process capability for critical features.
- Electrical safety, grounding, insulation and harness checks.
- Firmware/model identity and configuration checks.
- Functional, fault-injection and safe-state tests.
- Environmental and durability tests tied to stated use conditions.
- Final inspection, serial/lot traceability and release sign-off.
- Packaging audit and shipment records.

A test is PASS only when the approved procedure, calibrated equipment, actual conditions, measured results and acceptance criteria are all recorded. Missing data is NOT PASS. Failed results remain in the record; do not erase or silently retest.

## 10. Substitution, deviation and change control

No factory, supplier or operator may substitute a material, component, supplier, process, software version, tool, dimension or test method without an approved Engineering Change Request (ECR) and documented impact review.

The review must assess form-fit-function, safety, reliability, thermal, EMC, software, calibration, environmental, regulatory, service, spare parts and supply-chain effects. Require verification/validation and customer/regulatory notification where applicable. Approved alternates must be listed by exact part number, scope, conditions and evidence.

Temporary deviation must state quantity/serial range, reason, risk controls, expiry, disposition and authorised approvals. A verbal instruction is never a deviation approval.

## 11. Non-conformance, technical query and stop-work

- **TQ:** unclear, missing or conflicting requirement/document/interface.
- **NCR:** actual or suspected non-conforming material, process, product or result.
- **ECR/ECO:** proposed and approved engineering change.
- **Deviation/Waiver:** time- and scope-limited permission, only with documented risk assessment and approval.

Quarantine affected material/product, preserve evidence and prevent unintended use. Record who found it, when, item/serial/lot, document revision, actual condition, photos/data, containment, root cause, corrective action, verification and closure approval. Do not conceal or delete failed records.

## 12. Environmental qualification

Never apply a single programme temperature or IP value to every subsystem. For each product and component separately define operating, storage, transport, charging and survival conditions, including duration, ramp rate, powered/unpowered state, load, recovery and acceptance criteria.

Assess applicable combinations of cold/heat, thermal cycling, humidity/condensation, dust/sand, water, salt/corrosion, UV, vibration, shock, drop, altitude and chemical exposure. Battery charging limits and transport requirements are separate safety controls. A component datasheet or IP code does not establish whole-product qualification.

PUI89's -50°C to +60°C programme envelope is a study objective only until each product/subsystem has passed its defined qualification. Never advertise it as a product rating without evidence.

## 13. Software, AI and data configuration

For every software-controlled product release, identify hardware compatibility, OS/runtime, firmware, driver, model name/version/hash, dataset provenance/licence, calibration, configuration, safety limits, network dependencies and rollback package. Record test dataset/version and known limitations. Define loss-of-sensor, stale-data, low-confidence, communication-loss, compute-overload and power-fault behaviour. AI output must not silently override safety controls or human-authorised decisions.

## 14. Roles and authority

| Role | Responsibility | Cannot do without approval |
|---|---|---|
| Product/System Engineering | Requirements, architecture, interfaces, technical decisions | Release safety-critical design without required independent review |
| Mechanical/Electrical/Software Engineering | Discipline design, calculations, drawings, code and evidence | Change another discipline's released interface unilaterally |
| Manufacturing Engineering | Process, tooling, work instructions, process validation | Change product design to suit a process without ECR |
| Quality | Inspection plans, NCR, audit, release evidence review | Waive a requirement outside delegated authority |
| Supplier/Factory | Build exactly to released package; maintain traceability | Substitute, reinterpret or self-approve deviations |
| Operator/Technician | Follow current work instruction; record results; stop on abnormality | Guess missing values, bypass interlocks or conceal failures |
| Configuration Control | Revision, release, distribution, archive and obsolete-document control | Alter technical content without approved change |
| Product Release Authority | Approve defined release scope after gates pass | Declare unverified claims or bypass mandatory gates |

The founder is not the default technical approval path. Authority must be assigned by role and competence, with named deputies and escalation contacts recorded in each controlled project plan.

## 15. Factory transfer and qualification

Before production at a new site: audit capability and quality controls; verify equipment/gauges and calibration; train and qualify personnel; confirm supplier/source traceability; build FAI units; complete process validation; run product verification on the site-built configuration; close NCRs; approve the site and exact product/variant/revision scope. Requalification triggers include major process/site/supplier changes, prolonged inactivity, serious quality escapes or design changes affecting production.

## 16. Mandatory release package checklist

A product cannot enter production release until the applicable package is complete and approved:
- [ ] Product requirements and hazard/risk controls.
- [ ] System architecture and interface-control documents.
- [ ] Released 3D CAD, neutral STEP, 2D PDF/DXF drawings and tolerances.
- [ ] Released BOM with exact parts, materials, suppliers and approved alternates.
- [ ] Material/process specifications and certificates.
- [ ] Electrical schematics, harness drawings, pinouts and grounding.
- [ ] Software/firmware/model configuration and rollback.
- [ ] Assembly, inspection, calibration and service work instructions.
- [ ] Control Plan, FAI, end-of-line and safety test procedures.
- [ ] Verification/validation and environmental qualification reports.
- [ ] Packaging, transport, storage, maintenance and spare parts.
- [ ] Country-specific compliance matrix and technical file.
- [ ] Training/competence records, factory/site qualification and release approval.
- [ ] Complete revision, deviation, NCR and change history.

## 17. Reusable controlled templates

Use these fields in controlled CSV/XLSX or repository templates; do not leave blank cells ambiguous:
- **Requirements register:** Requirement ID, shall statement, rationale, variant, condition, unit, acceptance limit, verification method, owner, evidence ID, status.
- **BOM:** Item, part number, description, quantity, manufacturer, exact MPN, revision, material/grade, rating, supplier/site, origin, approved alternate, inspection, evidence, lifecycle.
- **Drawing register:** Drawing ID, part, revision, units, scale, CAD source, STEP, PDF, DXF, datum scheme, tolerances, material, finish, approval.
- **Interface register:** Interface ID, endpoints/revisions, mechanical/electrical/data/thermal definition, pinout/protocol, limits, fault behaviour, verification.
- **Control Plan:** Characteristic, requirement ID, process step, method, gauge/calibration, sample frequency, limit, reaction plan, record, owner.
- **Test report:** Procedure/revision, requirement IDs, DUT serial/configuration, equipment/calibration, environment, raw data, result, deviations, reviewer.
- **NCR/TQ/ECR:** Unique ID, affected items/revisions/serials, issue, containment, impact, disposition, approvals, verification, closure.
- **Training matrix:** Role, task, prerequisite competence, training revision, assessment, authorisation, expiry/refresher.
- **Factory transfer record:** Site, scope, equipment, supplier chain, personnel, FAI, process validation, open issues, approval.

## 18. Language and worker usability

Controlled engineering English is authoritative unless a contract specifies otherwise. Translate operator-facing safety instructions, warnings, labels and work instructions into the workers' required language. Keep IDs, part numbers, units, symbols, revision and acceptance limits identical across translations. Use standardised symbols plus words; never rely on colour alone. Require translation review and practical comprehension checks by local competent personnel.

## 19. Release principle

A factory may manufacture only the exact product, variant, site, process and revision stated in the release record. **No released value = no assumption. No evidence = no pass. No approval = no change. No traceability = no production release.**
