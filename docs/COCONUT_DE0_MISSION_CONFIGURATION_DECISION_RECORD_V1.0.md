# Coconut Harvest AI — DE-0 Mission & Configuration Decision Record v1.0

**Document class:** Mission-definition and configuration-control worksheet  
**Status:** OPEN — no physical harvesting mission or platform configuration approved  
**Revision date:** 23 November 2026  
**Applies to:** Coconut Harvest AI  
**Parent control:** [Detailed Engineering Release Gates v1.0](COCONUT_DETAILED_ENGINEERING_RELEASE_GATES_V1.0.md)  
**Decision rule:** No mechanical architecture, production CAD, component selection, BOM or manufacturing release may be based on an unapproved mission assumption.

> **Important:** This record prepares the decision; it does not make the decision. All fields marked OPEN/TBD require evidence and approval by the designated product and engineering authorities. A concept illustration, preliminary brief or AI capability statement is not a mission approval.

## 1. Current approved product boundary

The current product milestone is software-first coconut image assessment and human-reviewed harvest decision support. The documented software workflow may review supplied orchard images, assess visible appearance using the defined maturity taxonomy, preserve uncertainty and prepare traceable information for a human harvest-planning decision.

The following are **not established**:
- A physical harvesting robot or field prototype.
- A selected mobility, access, lifting, climbing, aerial or reach mechanism.
- A validated operating height, reach, payload, speed, slope, wind envelope or endurance.
- Autonomous cutting, fruit detachment, bunch handling or capture.
- Physical safety performance or environmental qualification.

The 0–30 m tree-height range is a research challenge only. It is not an approved reach or operating requirement.

## 2. DE-0 decision status

| Decision item | Current status | Required closure evidence |
|---|---|---|
| Intended product configuration | OPEN | Explicit selection of software-only milestone or a separately defined physical configuration |
| Primary user and accountable operator | OPEN | User-role definition and responsibility/RACI record |
| Intended use and harvest objective | OPEN | Domain-reviewed use-case statement and exclusions |
| Orchard/site operating context | OPEN | Representative site data and documented operating scenarios |
| Physical access strategy, if any | NOT SELECTED | Comparative feasibility, risk and validation evidence |
| Human supervision and authorization | OPEN | Approved operator workflow, authority and intervention rules |
| Hazardous-task boundary | OPEN | Preliminary hazard analysis and safety concept |
| Operating/environmental envelope | TBD | Evidence-based environmental and site requirements |
| Target markets and variants | OPEN | Initial market scope and jurisdictional review plan |
| Product/system boundary and interfaces | OPEN | Context diagram and interface ownership |
| Configuration owner and approvers | OPEN | Named roles and documented approval authority |

No row may be closed solely by filling in an assumed value. Attach a source, rationale, owner and approval record.

## 3. Mission statement template

Complete and review the following statement before architecture selection:

> For **[defined user/operator]** working in **[defined orchard/site context]**, Coconut Harvest AI will **[specific task and intended outcome]** using **[approved software and/or physical system boundary]**. The operator will **[supervision and authorization responsibilities]**. The system will operate only within **[evidence-supported operating envelope]** and will not **[explicit exclusions]**. Success will be judged against **[measurable, verifiable outcomes]**.

**Current disposition:** NOT APPROVED — inputs remain OPEN.

## 4. Configuration paths for evaluation — none selected

These are mutually distinguishable study paths, not recommendations or approved product commitments. A decision may retain the current software-only scope and defer physical engineering.

| Path | Description | Evidence needed before selection |
|---|---|---|
| A — Software-only decision support | Image intake, maturity assessment, uncertainty handling and human-reviewed harvest planning; no physical actuation | User workflow, data rights/provenance, software requirements, CPU evaluation and deployment context |
| B — Operator-carried or stationary sensing aid | Human-operated camera/sensor arrangement; no autonomous harvesting mechanism | Site workflow, ergonomic/access study, sensor calibration, power/interface needs and human-factors assessment |
| C — Ground-mobile sensing platform | Mobile ground unit for observation or data collection; no cutting unless separately approved | Orchard access survey, ground/soil/slope data, stability and mobility risks, obstacle/person detection and safe-stop concept |
| D — Supervised manipulator / harvesting platform | Ground-supported mechanism that may position a tool or capture fruit under a separately validated supervised workflow | Reach/load/workspace study, structural analysis, fruit-contact/capture concept, falling-object controls, exclusion zones, interlocks and staged test plan |
| E — Other / staged hybrid | A different architecture or phased combination justified by mission evidence | Written concept definition, alternatives analysis, risk review and approval |

Do not combine paths implicitly. If a staged approach is selected, define the phase boundary, interfaces and independent release gates for each phase.

## 5. Required mission inputs

### 5.1 User, operator and task
- Primary user, purchaser, operator, maintainer and affected bystanders.
- Who selects a tree/bunch/fruit and who authorizes any physical action.
- Task sequence from arrival/site setup through observation, decision, intervention (if any), recovery and shutdown.
- Required training, PPE, staffing, communication and emergency response.
- Expected task frequency, duration and seasonal use, supported by field evidence.

**Status:** OPEN — no user study or workflow approval recorded here.

### 5.2 Orchard and access context
Record representative, sourced values or ranges for:
- Coconut varieties and tree/bunch/fruit characteristics relevant to the task.
- Tree spacing, canopy geometry, access paths and working clearances.
- Ground material, bearing capacity, slope, unevenness, mud, standing water and obstacles.
- Wind, rain, temperature, humidity, solar exposure, dust and visibility.
- Overhead electrical lines, nearby structures, people, animals and public access.
- Transport, storage, cleaning, charging and maintenance locations.

For each input, identify measurement method, sample/site, date, uncertainty and representativeness. Do not infer site conditions from generic photographs.

**Status:** OPEN — representative orchard survey required.

### 5.3 Harvest objective and biological criteria
- Define which maturity classes are relevant to the intended harvest objective.
- Have a qualified agricultural/domain reviewer approve the taxonomy, label boundaries and harvest suitability rules.
- Keep visible colour, physiological maturity and harvest suitability as distinct concepts.
- Define how damaged, occluded, diseased, ambiguous or out-of-distribution fruit is handled.
- Define the human review and rejection process.

**Status:** OPEN — domain approval and use-case-specific acceptance criteria required.

### 5.4 Physical interaction, only if a physical path is selected
Define through risk assessment and evidence:
- Whether the system only observes, contacts, supports, detaches, cuts, catches or transports fruit.
- Fruit/bunch handling and uncontrolled-fall prevention concept.
- Permitted contact surfaces/forces and damage criteria.
- Tool hazards, stored energy, pinch/crush/shear zones and guarding.
- Safe tool state, independent interlocks, emergency stop, recovery and maintenance isolation.
- People exclusion zones and site control responsibilities.

No tool, actuator, reach, force, load or safety threshold is specified by this worksheet.

**Status:** NOT DEFINED — physical mission path not selected.

## 6. Safety and human-control principles for DE-0

These are mandatory design constraints for any later physical proposal; they are not evidence that a safe machine exists:
1. Human-reviewed harvest decisions remain the baseline unless a separate, explicitly approved authorization concept is established.
2. Perception uncertainty, invalid/stale sensor data, loss of calibration, communications faults or unknown reachability must lead to stop/hold/review, never implicit permission to actuate.
3. AI perception must not be the sole safety control for hazardous motion or cutting.
4. Hazardous energy and motion require an independently engineered safety architecture, interlocks, emergency stop and safe recovery.
5. No operation may be proposed near overhead electrical lines, people or public areas without a site-specific hazard assessment and approved controls.
6. The system must not rely on cloud connectivity or a phone app for essential local safety functions.
7. Test progression must be staged and risk-controlled; simulation is not field validation.

A competent safety/engineering review must identify applicable risk-assessment methods and standards after intended use and market scope are defined.

## 7. Required DE-0 records and sign-off

The DE-0 package is complete only when all applicable records are controlled and approved:

- [ ] Mission statement and intended-use definition.
- [ ] Product configuration/path selection with alternatives considered.
- [ ] User/operator roles, workflow and responsibility matrix.
- [ ] Representative orchard/site survey and source records.
- [ ] Harvest objective and domain-reviewed maturity/eligibility definitions.
- [ ] Operating scenarios, foreseeable misuse and explicit exclusions.
- [ ] Preliminary hazard analysis and safety-control concept.
- [ ] System context diagram and physical/software boundary.
- [ ] Initial target-market scope and variant assumptions.
- [ ] Measurable mission success criteria and verification approach.
- [ ] Open-issue register with owner, due condition and closure evidence.
- [ ] Formal review record, decision date, approvers and configuration baseline.

| Approval role | Required confirmation | Name / record | Status |
|---|---|---|---|
| Product owner | Intended use, user value, exclusions and configuration path | TBD | OPEN |
| Agricultural/domain reviewer | Crop, maturity and harvest criteria | TBD | OPEN |
| Systems engineering | Requirements, boundaries, interfaces and architecture readiness | TBD | OPEN |
| Safety engineering | Hazard analysis and safe-work concept | TBD | OPEN |
| Manufacturing/quality | Feasibility of later controlled design and verification | TBD | OPEN |
| Market/compliance owner | Initial jurisdiction scope and obligations review | TBD | OPEN |

Do not fabricate approver names or treat repository authorship as independent technical approval.

## 8. DE-0 exit criteria and downstream hold points

DE-0 may be marked **VERIFIED** only when:
- The intended use and product configuration are unambiguous.
- A single mission path or explicitly staged set of paths is selected.
- Users, operators, environment, task sequence and exclusions are documented with evidence.
- Safety hazards, human authority and stop/hold principles are reviewed.
- Measurable mission outcomes and verification methods are defined.
- Required roles have approved the same revision and all critical OPEN items are closed or explicitly deferred with justified scope.

Until then:
- DE-1 physical system requirements remain OPEN.
- DE-2 physical architecture and trade studies remain NOT RELEASED.
- DE-3 production CAD, drawings and electrical design must not begin as a frozen design.
- DE-4 procurement BOM and supplier release remain prohibited.
- No physical prototype build or factory manufacture is authorized by this document.

Software-only requirements and evidence work may continue within its existing scope and controls.

## 9. Decision log

| Decision ID | Decision / issue | Options considered | Evidence reference | Decision / rationale | Approver | Date | Status |
|---|---|---|---|---|---|---|---|
| DE0-001 | Physical mission/configuration path | A / B / C / D / E | TBD | No decision recorded | TBD | TBD | OPEN |
| DE0-002 | Initial target orchard/site context | TBD | TBD | No decision recorded | TBD | TBD | OPEN |
| DE0-003 | Human authorization and physical intervention boundary | TBD | TBD | No decision recorded | TBD | TBD | OPEN |
| DE0-004 | Initial target-market scope | TBD | TBD | No decision recorded | TBD | TBD | OPEN |

## 10. Controlled status

**DE-0 status: OPEN — NOT FROZEN.**  
**Physical platform architecture: NOT SELECTED.**  
**Production CAD / BOM / drawings: NOT AUTHORIZED.**  
**Manufacturing: NOT RELEASED.**

The next engineering action is to gather the mission evidence and complete the review records above. Do not replace OPEN fields with plausible-looking estimates to make the package appear complete.

**Manufacturing principle:** Design Once. Document Clearly. Manufacture Globally. Verify Everywhere.
