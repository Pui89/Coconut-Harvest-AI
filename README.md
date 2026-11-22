# Coconut Harvest AI

[English](README.md) · [ภาษาไทย](README.th.md)


**Local-first coconut maturity assessment and human-reviewed harvest decision support.**

[English project page](https://pui89.github.io/coconut.html) · [ภาษาไทย](https://pui89.github.io/coconut-th.html) · [PUI89 portfolio](https://pui89.github.io/)

![Coconut Harvest AI conceptual harvesting robot](docs/images/coconut-harvest-realistic-all-stage-concept.svg)

*Concept illustration only. It is not a built robot or evidence of a successful harvest.*

## What this product is

Coconut Harvest AI is an agricultural computer-vision project that helps orchard operators review visible coconut maturity and prepare traceable harvest-planning decisions. The first product milestone is software-based image assessment; a physical harvesting robot is a later research direction.

**ผู้ใช้งาน:** เกษตรกร ผู้ดูแลสวนมะพร้าว และหน่วยงานด้านการเกษตร  
**ประโยชน์หลัก:** ช่วยตรวจสอบภาพและประเมินลักษณะความแก่ของมะพร้าว พร้อมบันทึกความไม่แน่นอนและผลการตรวจสอบโดยมนุษย์

## Product-specific functions

- Review locally supplied orchard images and check image quality and source provenance.
- Use four visible assessment classes: **young green, mature green, yellow and brown**.
- Keep colour observations separate from biological maturity and harvest suitability; these require an appropriate human-reviewed definition.
- Record uncertain or obscured cases for human review instead of forcing a prediction.
- Prepare traceable assessment records for harvest planning.

## What is not established

- No approved real-orchard training dataset or held-out detector accuracy is established.
- No validated 0–30 m perception or reach capability is claimed; 0–30 m is a long-term research challenge.
- No autonomous cutting, tree climbing, physical harvesting robot or field safety performance is established.
- A concept illustration or software test is not evidence of harvesting performance.

## Current development status

**Implemented — software and evaluation-preparation foundation.** This label refers to software work only; it does not mean a physical harvesting system is implemented.

**Next evidence gate:** complete image-rights and provenance review, human annotation and QA, leakage-safe dataset splitting, then run a reproducible CPU evaluation. Report per-class precision, recall, F1, confusion counts, sample sizes, failure cases and measured runtime/RAM only after the evaluation has actually run.

## Product documentation

- [Software MVP product specification](docs/COCONUT_SOFTWARE_MVP_PRODUCT_SPEC.md)
- [Real-image validation execution gates](docs/COCONUT_REAL_IMAGE_VALIDATION_EXECUTION_GATES.md)
- [Four-class and 0–30 m validation roadmap](docs/FOUR_CLASS_0_30M_VALIDATION_ROADMAP.md)
- [Coconut maturity, location and harvest requirements](docs/COCONUT_MATURITY_LOCATION_HARVEST_REQUIREMENTS.md)

## Shared PUI89 engineering

Cross-product architecture, evidence contracts, safety, privacy, security, recovery, device interaction and localization requirements are maintained centrally in the [PUI89 Shared AI Core](https://github.com/Pui89/PUI89-Shared-AI-Core). This repository defines Coconut-specific tasks and validation; shared requirements are linked, not duplicated.

Current maturity labels and portfolio scope follow the [PUI89 Portfolio Alignment Register](https://github.com/Pui89/Pui89.github.io/blob/main/docs/PUI89_PORTFOLIO_ALIGNMENT_REGISTER_2026-11-18.md) and [Evidence-Based Development Maturity Standard](https://github.com/Pui89/Pui89.github.io/blob/main/docs/PUI89_DEVELOPMENT_STAGE_STANDARD.md).

**PUI89 has six active products.** Shared AI Core is infrastructure, not a seventh product.

## AI Model & Intelligence profile

**Candidate capability profile:** Object Detection and Image Segmentation for coconut/scene localisation; Object Tracking only where temporal continuity is useful; VLM for supervised visual review; Predictive Models for maturity/harvest trends only after representative, rights-cleared dataset validation. SLAM and Sensor Fusion are not assumed requirements for the current software-first milestone.

All nine shared capability families and their definitions, evaluation requirements, provenance/uncertainty rules and safety boundaries are maintained in the [PUI89 Shared AI Core Model Intelligence Framework](https://github.com/Pui89/PUI89-Shared-AI-Core/blob/main/docs/architecture/PUI89_MODEL_INTELLIGENCE_FRAMEWORK_V1.0.md). This product profile is a **candidate engineering allocation**, not evidence of model installation, runtime integration, benchmark results, field validation or certified performance. Select and enable each capability only after product-specific requirements, approved data, compute/energy budgets and verification gates are satisfied.

## Robot Capabilities & Functional Capacity

**Scope boundary:** The current milestone is software-based coconut image assessment and harvest decision support. A physical harvesting robot is a later research direction. The capacities below are requirements to define and validate, not claims of a built machine.

### 1. Physical capacity
- Define the future platform envelope, complete mass, payload, stability, tool mass and fruit-handling limits after the harvesting mission and mechanical concept are selected.
- Define gripper/cutter interface, fruit-contact limits, bunch handling and safe release requirements before hardware selection.
- **Current values:** robot dimensions, mass, payload, tool reach and fruit-handling capacity: **TBD**; no physical robot is established.

### 2. Mobility capacity
- Define orchard ground conditions, slope, soil bearing, wheel/track choice, turning envelope, ground clearance and access around palm trees.
- Treat tree climbing, aerial access and operation on unstable ground as out of scope unless separately engineered and validated.
- **Current values:** speed, slope, clearance, terrain envelope and endurance: **TBD**.

### 3. Perception capacity
- Assess image quality, lighting, shadows, wind-driven motion, occlusion and camera viewpoint.
- Detect and count visible coconuts; classify visible appearance into young green, mature green, yellow and brown classes.
- Distinguish visual colour class from biological maturity and harvest suitability; retain uncertainty and human review.
- Estimate fruit/bunch location and 3D reachability only when suitable calibrated depth/geometry evidence exists. The 0–30 m range remains a research challenge, not a validated range.
- **Current validated accuracy and detection range:** not established.

### 4. Computing capacity
- Prefer local CPU-first assessment and reproducible open-source workflows; evaluate accelerator use only when justified by measured workload.
- Record model/version, input size, runtime, peak RAM, confidence calibration and failure cases when measured.
- No cloud GPU, metered API or remote image transfer is required by this specification.
- **Compute hardware and measured performance:** TBD.

### 5. Power capacity
- Define battery chemistry, usable energy, peak/continuous power, runtime, charging, protection and thermal limits only when a physical platform is designed.
- **Battery capacity, runtime and charging time:** TBD; no physical power system is established.

### 6. Communication capacity
- The software assessment workflow should support local/offline image review and export of approved, traceable results.
- Any future robot-to-operator link must define range, protocol, loss-of-link behaviour and data permissions.
- **Radio range and robot connectivity:** TBD; no integrated robot link is established.

### 7. Safety capacity
- Require operator-supervised harvesting decisions, safe tool states, guarded moving parts, emergency stop and a defined recovery procedure before physical trials.
- Stop or request human review when fruit position, maturity, reachability, people proximity or sensor health is uncertain.
- No autonomous cutting, tree climbing or safe harvesting performance is currently claimed.

### 8. Maintenance capacity
- Define camera/depth-sensor cleaning, calibration checks, tool inspection, wear parts, battery service and diagnostic logs in the future hardware plan.
- Preserve dataset/model provenance and versioned evaluation records for software maintenance.
- **Service intervals and replacement procedures:** TBD.

### 9. Operating limits
- Current scope: software-first image assessment and decision-support foundations.
- No physical harvesting robot, field mobility, 0–30 m detection/reach, autonomous cutting, crop-yield guarantee or validated field accuracy is established.
- Unknown, occluded or out-of-distribution cases must be marked uncertain and referred for human review.

**Capacity evidence status:** Software requirements documented; physical capacities **TBD / not built / not validated**. Only measured results with reproducible test records may be labelled *Tested* or *Verified*.


## Physical & Multimodal Sensor Privacy

PUI89 adopts the [Physical & Multimodal Sensor Privacy Standard v1.0](https://github.com/Pui89/PUI89-Shared-AI-Core/blob/main/docs/privacy/PUI89_PHYSICAL_MULTIMODAL_SENSOR_PRIVACY_STANDARD_V1.0.md) as a shared engineering requirement. Any future RGB, depth or thermal imaging camera must have a manual physical cover. The current software-first image-review workflow does not imply a physical camera system exists. User-supplied orchard images remain local unless transfer is explicitly authorised.

**Evidence status:** requirements/specification only. No product-level hardware implementation or verification is claimed by this README section.


## Long-Life Battery & Energy Intelligence

PUI89 adopts the [Long-Life Battery & Energy Intelligence Standard v1.0](https://github.com/Pui89/PUI89-Shared-AI-Core/blob/main/docs/energy/PUI89_LONG_LIFE_BATTERY_ENERGY_INTELLIGENCE_STANDARD_V1.0.md) as a shared engineering requirement. For software-first or operator-device configurations, optimise local inference and display energy. Any future field unit or mobile platform requires a measured energy budget; no battery-powered harvesting robot or runtime is claimed.

Battery runtime, chemistry, capacity, cycle life, charging performance and safety compliance remain **TBD until designed and evidenced**. No unverified runtime or battery-life claim is made. The design must include an energy budget, independent BMS protections, thermal/electrical safety, service strategy and representative runtime validation.


## Offline Independence & Connectivity Resilience

**The product must work without the app. Safety must work without connectivity.** Basic supported local operation, local status and safety controls must not require a smartphone, app, Wi-Fi, internet or cloud. The complete printed User Manual and printed Quick Start & Safety Guide are supplied inside the product box in the destination-market language. Both are readable without a smartphone, QR scan, account, app, Wi-Fi or internet. QR and short URL are optional supplements. QR and short URL are optional supplements. On link loss, remote commands are disabled and the product follows its own hazard-based safe state. See the [PUI89 Offline Independence & Connectivity Resilience Standard v1.0](https://github.com/Pui89/Pui89.github.io/blob/main/docs/PUI89_OFFLINE_INDEPENDENCE_CONNECTIVITY_RESILIENCE_STANDARD_V1.0.md) and the [product manual/Remote Companion specification](docs/PRODUCT_MANUAL_AND_REMOTE_COMPANION_STANDARD_V1.md).

**Product-specific offline baseline:** Local image import/capture where supported; image-quality checks; on-device maturity assessment only when the approved model, sensors and compute are installed; human review; local result display and storage. If AI resources are unavailable, preserve manual review/recording and mark automated assessment unavailable. Remote loss must not erase local work. No remote cutting, harvesting or actuator commands.

These are development requirements, not claims of implemented, tested or validated capability.


## Latest engineering progress — 22 November 2026

**Maturity:** Implemented — software and evaluation-preparation foundation. **Evidence status:** PARTIAL. This describes software/documentation only; no physical harvesting capability is established.

**Recent verified repository progress:**
- Merged multilingual user-manual and remote-companion specification (PR #326).
- Added offline-first requirements, local-operation boundaries and verification status to the README and engineering documentation.
- Shared AI Core has added a Coconut multi-view image-intake/ZIP-validation workflow and annotation-quality diagnostics; these are evidence-intake controls, not detector-performance results.

**Not established:** an approved rights-cleared orchard dataset, held-out detector accuracy, field harvesting, a built harvesting robot, or validated 0–30 m perception/reach.

**Next evidence gate:** complete source-rights/provenance review, human annotation and QA, leakage-safe dataset splitting, then execute a reproducible CPU evaluation reporting per-class precision, recall, F1, confusion counts, sample sizes, failure cases, runtime and RAM. Record the exact dataset, code commit, environment and results before making performance claims.

**Last reviewed:** 22 November 2026. See [multilingual manual/remote companion PR #326](https://github.com/Pui89/Coconut-Harvest-AI/pull/326) and [Shared AI Core](https://github.com/Pui89/PUI89-Shared-AI-Core).

## Global manufacturing engineering

The product-specific [PUI89 Global Manufacturing Design Brief v1.0](docs/PUI89_GLOBAL_MANUFACTURING_DESIGN_BRIEF_V1.0.md) defines the preliminary product envelope, candidate material families, component architecture, global human-factors requirements, extreme-environment design strategy, manufacturing transfer package, quality gates and unresolved specifications. It distinguishes proposed targets from tested or verified performance. Candidate materials and component types are not an approved BOM; exact grades, models, dimensions and tolerances remain open until engineering analysis and validation.

## Global engineering and manufacturing control

For international engineering, factory and worker handoff, use the controlled PUI89 documents:
- [PUI89 Global Engineering & Manufacturing Portal](https://pui89.github.io/global-engineering.html)
- [PUI89 Global Manufacturing Handoff System v1.0](https://github.com/Pui89/Pui89.github.io/blob/main/docs/PUI89_GLOBAL_MANUFACTURING_HANDOFF_SYSTEM_V1.0.md)

**Production rule:** Build, buy, substitute, inspect or release only against the exact approved product configuration, revision, drawing, BOM and work instruction. Missing or conflicting values are **STOP — DO NOT GUESS**; raise a Technical Query (TQ). The shared blank manufacturing templates are being reviewed in [PUI89 website PR #639](https://github.com/Pui89/Pui89.github.io/pull/639) and are not yet production authority.
