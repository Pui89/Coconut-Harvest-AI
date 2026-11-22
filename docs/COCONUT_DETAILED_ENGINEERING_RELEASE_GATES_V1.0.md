# Coconut Harvest AI — Detailed Engineering Release Gates v1.0

**Document class:** Product-specific engineering execution and release-control specification  
**Status:** Proposed / planning baseline — NOT a released production specification  
**Revision date:** 22 November 2026  
**Applies to:** Coconut Harvest AI  
**Parent document:** [Global Manufacturing Design Brief v1.0](PUI89_GLOBAL_MANUFACTURING_DESIGN_BRIEF_V1.0.md)  
**Manufacturing principle:** Design Once. Document Clearly. Manufacture Globally. Verify Everywhere.

> **Release warning:** This document defines the evidence and control process required to produce a manufacturing-ready package. It does not supply approved dimensions, tolerances, material grades, component selections, CAD geometry, test results, or regulatory approvals. No factory may manufacture from this document alone.

## 1. Product baseline and physical-design boundary

The currently defined product milestone is software-first coconut image assessment and human-reviewed harvest decision support. The physical harvesting robot is a later research direction. The repository does not currently establish an approved physical machine mission, platform architecture, field prototype, validated reach, autonomous cutting, or physical safety performance.

Therefore:

- The software product configuration may proceed through software requirements, data/evaluation design, deployment-environment definition, and software verification.
- A physical harvesting platform must remain **CONCEPT / NOT FROZEN** until its supervised mission, operator workflow, orchard environment, access constraints, and hazard controls are approved.
- Do not create dimensioned production CAD, select production motors/batteries, release a physical BOM, or issue factory work instructions by guessing from concept illustrations.
- The 0–30 m range remains a research challenge and is not an approved reach, detection, or operating specification.

## 2. Engineering status vocabulary

Use these labels on every requirement, drawing, CAD model, BOM line, test and compliance record:

| Status | Meaning | Permitted use |
|---|---|---|
| PROPOSED | Candidate or design hypothesis; not approved | Trade study only |
| TBD / OPEN | Required input or value is missing | Must not be used for procurement or manufacture |
| SPECIFIED | Value and acceptance rule approved under change control | Design baseline; not proof of test |
| TESTED | Test executed with a traceable record | Report the measured result and limitations |
| VERIFIED | Requirement-to-evidence review completed and accepted by authorised reviewer | May support the stated release gate |
| NOT APPLICABLE | Reasoned, approved scope decision | Must include rationale and approver |

Never convert a candidate, datasheet claim, simulation, concept image, or unexecuted test plan into TESTED or VERIFIED status.

## 3. Gate sequence and mandatory exit evidence

| Gate | Work package | Mandatory exit evidence | Current disposition |
|---|---|---|---|
| DE-0 | Product mission and configuration freeze | Approved intended use, user/operator roles, supervised workflow, physical/software boundary, target markets, operating scenarios and exclusions | OPEN — physical platform mission not frozen |
| DE-1 | System requirements | Unique requirement IDs, measurable acceptance criteria, source/rationale, verification method, owner and safety classification | PARTIAL — software scope documented; physical requirements OPEN |
| DE-2 | Architecture and trade studies | System block diagram, interfaces, load cases, packaging studies, anthropometric inputs, risk analysis, material/component comparison | NOT RELEASED |
| DE-3 | Detailed mechanical/electrical design | Controlled 3D CAD assembly, neutral STEP, 2D drawings, electrical schematics, interface-control documents, calculations and design review | NOT RELEASED |
| DE-4 | Production definition | Exact material/process specifications, released component BOM, approved supplier/alternative register, assembly instructions and special-process controls | NOT RELEASED |
| DE-5 | Inspection and prototype verification | Inspection plan, calibrated measurement equipment, first-article records, test procedures/results, NCR closure and configuration record | NOT RELEASED |
| DE-6 | Environmental qualification | Product-specific environmental test plan, severity rationale, measured results, failures/retests and approval | NOT RELEASED |
| DE-7 | Market conformity and factory transfer | EU/US/Japan applicability matrix, conformity evidence, site qualification, process validation, manuals/labels and release approval | NOT RELEASED |

A gate may be marked complete only when all required evidence is linked, revision-matched, reviewed and approved. Missing evidence keeps the gate OPEN.

## 4. Required detailed engineering deliverables

### 4.1 Dimensions, datums and tolerances

For every physical part and assembly, provide:

- Unique part/assembly number, title, revision, units and drawing status.
- Overall and functional dimensions, datum reference frame, GD&T where justified, fits/clearances, thread callouts and critical-to-quality characteristics.
- Tolerance rationale linked to function, manufacturing process capability, stack-up analysis and inspection method.
- Mass properties and centre-of-gravity data where stability, lifting or handling depends on them.
- Explicit distinction between nominal dimensions, allowable limits and measured as-built values.

**Current status:** all physical production dimensions and tolerances are TBD because the physical mission and architecture are not frozen.

### 4.2 2D manufacturing drawings

Each released drawing must include:

- Orthographic views and sections sufficient to manufacture and inspect the part without interpretation.
- Dimensions, datums, tolerances, surface texture/finish, edge/burr requirements and geometric controls as applicable.
- Material specification, condition/temper, coating or treatment, joining/process notes and prohibited substitutions.
- Part number, revision, units, projection method, scale, author/checker/approver and change history.
- Inspection characteristics and the applicable measurement method.

Native editable drawing source and neutral PDF/DXF exports must share the same revision and be checked for export fidelity.

### 4.3 3D CAD assemblies and STEP

The controlled CAD release must contain:

- Native source files and complete assembly hierarchy with stable part numbers.
- Fully constrained assembly relationships, interface geometry and required clearances.
- Configurations/variants, suppressed or optional components clearly identified.
- Mass properties with material density source and calculation assumptions.
- Interference/clearance review, motion-envelope review where applicable, and design-review record.
- Neutral STEP export, export settings, units, revision and independent re-import/geometry comparison record.

A STEP file is not accepted merely because it opens; geometry, units, assembly structure and revision must be checked against the native source.

### 4.4 Materials and surface finishes

No material may be selected solely because a supplier labels it “industrial”, “aerospace”, “marine” or similar.

For each released material/process, record:

- Exact recognised material standard and grade; alloy/polymer designation; temper/condition; thickness or section.
- Mechanical properties relevant to the load case, including source and test/certificate basis.
- Corrosion, UV, moisture, chemical/cleaning, abrasion, temperature and fatigue suitability for the defined mission.
- Surface treatment/coating specification, thickness, preparation, adhesion/durability criteria and repair method.
- Joining compatibility, galvanic-corrosion controls, weldability/fastener compatibility and process limitations.
- Manufacturer, manufacturing country, lot/batch traceability, certificate type and incoming inspection requirements.
- Approved alternatives only after equivalence analysis and validation.

**Current status:** candidate material families in the parent brief are trade-study inputs only. No grade or finish is approved.

### 4.5 Motors, gearboxes, batteries and sensors

Every selected item must have an exact manufacturer and model/part number, revision, datasheet revision/date, approved operating envelope and verified supply-chain identity.

The selection record must cover, as applicable:

- Motor: continuous/peak torque and speed, duty cycle, thermal limits, efficiency map, mounting, shaft/interface, feedback and protection.
- Gearbox: ratio, rated/peak output torque, backlash, efficiency, service life assumptions, lubrication, mounting and environmental limits.
- Battery/cells: chemistry, exact cell model, series/parallel configuration, usable energy, current limits, temperature limits, protection architecture, BMS, charging profile, transport and service controls.
- Sensors: modality, field of view/range where relevant, accuracy and uncertainty, frame rate, interface, calibration, synchronisation, ingress/environmental limits and privacy controls.
- Compute/control electronics: processor/accelerator, memory, power/thermal envelope, interfaces, lifecycle and software/firmware compatibility.

Datasheets are design inputs, not proof that the selected component meets the system requirement. Verify critical ratings and interfaces at system level.

**Current status:** no physical harvesting motor, gearbox, battery, sensor or controller model is selected for production.

### 4.6 Component-level BOM

Every BOM line must contain:

PUI89 part number | item/description | parent assembly | quantity | make/buy | manufacturer | exact model/grade | revision | critical ratings | material/process | interface | manufacturing country | origin evidence | approved supplier | qualified alternatives | lifecycle/obsolescence status | inspection class | verification record | drawing/CAD reference

Also maintain a controlled supplier register with dated availability, lead time, traceability, quality-system evidence, change-notification obligations and country-of-origin evidence.

No substitute is permitted based only on similar appearance, marketing category, nominal voltage, connector shape or claimed grade. Form-fit-function equivalence and risk impact must be reviewed and approved.

### 4.7 Electrical schematics and interface control

The electrical package must include system power architecture, protection coordination, wiring/harness drawings, connector part numbers and pinouts, wire gauge/material/temperature rating, grounding/bonding, fuse/breaker ratings, isolation, emergency-stop circuit, battery/BMS interfaces, charging interface, sensor/compute interfaces, EMC considerations and revision-matched cable schedules.

Each interface must define electrical/mechanical limits, signal direction, protocol, timing, fault behaviour, connector keying, environmental sealing and verification method.

No electrical schematic is released until the physical architecture, power budget, hazard analysis and component models are approved.

### 4.8 Assembly, inspection and QC

Assembly instructions must specify prerequisites, part/revision checks, tools and fixtures, operator qualifications, sequence, orientation, fastener/torque values with source, adhesives/sealants and cure controls, cable routing, connector locking, calibration, firmware/software identity, in-process inspection, safety checks and rework limits.

The inspection and QC plan must identify:

- Characteristic ID and criticality.
- Nominal/limit values and approved acceptance criteria.
- Sampling method and rationale.
- Gauge/instrument, calibration status, resolution and measurement uncertainty where relevant.
- Inspection frequency and responsible role.
- Record format, traceability fields and reaction plan for nonconformance.
- First-article inspection and lot-release requirements.

If a tolerance, torque, threshold, or acceptance criterion is unknown, mark it TBD and stop the affected operation.

### 4.9 Environmental qualification

Environmental severities must be derived from the approved operating, storage, transport, charging and service environments. Do not apply a portfolio-wide temperature or ingress rating as a product rating.

The product-specific plan must consider relevant combinations of temperature, thermal cycling, humidity/condensation, rain/spray, dust, UV, corrosion, vibration, shock, transport, cleaning chemicals and battery exposure. Each test must state sample configuration, preconditioning, instrumentation, method/standard and edition, severity, duration/cycles, pass/fail criteria, deviations, raw data location, failures and retest rationale.

Simulation, component datasheets and analysis do not replace required system tests. No environmental qualification result is currently claimed.

### 4.10 EU / US / Japan compliance matrix

Maintain a controlled matrix with these columns:

Market | product classification/intended use | applicable legislation/regulation | applicable standard and edition | obligation/essential requirement | conformity route | required test/evidence | accredited/recognised body if required | technical-file record | label/manual/language requirement | importer/manufacturer responsibility | status | owner | review date

Evaluate EU, United States and Japan separately. Determine applicability from the final product configuration, intended use, radio/electrical/mechanical characteristics, battery and transport configuration, and market placement. Do not assume CE, FCC, UL, PSE or any other mark is universally required or interchangeable.

A compliance matrix is a planning tool; it is not a conformity assessment, certification, legal opinion or permission to place the product on the market.

## 5. Design for global manufacture and transfer

The released manufacturing package must be self-contained and revision-controlled. A qualified factory must receive the same approved baseline:

1. Native CAD plus validated STEP exports.
2. Dimensioned 2D drawings and controlled PDF/DXF exports.
3. Released BOM and approved-source/alternative register.
4. Material, finish, joining and special-process specifications.
5. Electrical schematics, harness drawings and interface-control documents.
6. Assembly work instructions, fixtures, tools and operator qualifications.
7. Inspection plan, gauges, calibration and acceptance criteria.
8. End-of-line functional and safety tests.
9. Software/firmware identifiers and configuration-loading instructions.
10. Packaging, storage, transport, maintenance and spare-parts instructions.
11. NCR, deviation, engineering-change and supplier-change procedures.
12. First-article inspection and manufacturing-site qualification records.

A second-country factory must complete site/process review, first-article inspection and equivalence validation before production approval. A drawing transfer alone does not establish equivalent manufacturing quality.

## 6. Human factors and market adaptation

Do not silently alter the core design by country. Maintain a controlled global core configuration and separately approved market variants where evidence or law requires them.

For each target market, document intended user population, anthropometric data source, user trials, PPE/clothing allowances, access/reach/visibility, physical-control forces, operator posture, local climate/exposure, language, labels, service capability and applicable law. Record the tested population and limitations; do not claim universal fit.

## 7. Change control, traceability and stop-work rules

- Every requirement, drawing, CAD assembly, BOM, supplier, test and compliance record has a unique ID, revision and change history.
- Changes require impact analysis across interfaces, safety, materials, suppliers, manufacturing, inspection, software and regulatory status.
- Supplier substitutions, deviations and concessions require documented approval before use.
- Factories must raise a Technical Query (TQ) when a requirement is ambiguous and a Non-Conformance Report (NCR) when output fails an approved requirement.
- Stop the affected operation when a critical value, drawing revision, material identity, inspection method or acceptance criterion is missing or conflicting.
- No verbal instruction overrides the controlled released package.

## 8. Current closure register

| Deliverable | Status | Evidence required to close |
|---|---|---|
| Final dimensions and tolerances | TBD / NOT RELEASED | Frozen mission, approved architecture, CAD, analysis, tolerance stack and inspection plan |
| 2D manufacturing drawings | NOT RELEASED | Reviewed, revision-controlled drawings with full manufacturing/inspection definition |
| 3D CAD assemblies and STEP | NOT RELEASED | Native assemblies, validated STEP exports and design-review record |
| Exact material grades and finishes | NOT RELEASED | Approved material/process specifications and traceable source evidence |
| Motor, gearbox, battery and sensor models | NOT SELECTED | Requirements-based trade studies, exact models and interface/qualification evidence |
| Component-level BOM | NOT RELEASED | Complete controlled BOM and approved supplier/alternative register |
| Electrical schematics | NOT RELEASED | Approved power architecture, schematics, harnesses and protection review |
| Assembly procedures | NOT RELEASED | Validated sequence, tooling, torque/process controls and build records |
| Inspection and QC specifications | NOT RELEASED | Characteristic-level acceptance criteria, gauges, calibration and inspection records |
| Environmental qualification results | NOT TESTED | Approved product-specific plan and traceable measured results |
| EU / US / Japan compliance matrix | OPEN | Product classification and jurisdiction-specific applicability review with evidence owners |

## 9. Immediate next engineering actions

1. Keep the current software-first milestone explicit; do not treat the future harvesting robot as an approved product configuration.
2. Define and approve one supervised physical mission and operator workflow before mechanical architecture selection.
3. Create a requirements traceability matrix with unique IDs, measurable acceptance criteria, owners and verification methods.
4. Complete hazard analysis and preliminary system architecture for that approved mission.
5. Conduct evidence-based material, actuator, power, sensing and compute trade studies.
6. Only after design inputs are approved, create controlled CAD, drawings, schematics and a draft BOM.
7. Build and verify a prototype under an approved test plan before production release.

**Manufacturing release rule:** Until the required gate evidence is complete and approved, this product remains **NOT RELEASED FOR MANUFACTURE**. No manufacturer should infer missing dimensions, materials, components, tolerances, processes or acceptance limits.
