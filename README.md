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


## What we are building now — 25 November 2026

**Current implementation focus: prove the AI vision workflow before building harvesting hardware.** The active milestone remains a local-first software prototype and evidence preparation. We are not currently claiming a trained coconut detector, automatic four-class maturity model, or working robot.

### Current work
1. **Dataset evidence:** identify candidate coconut image sources and verify file-level provenance, licence/permission and permitted use before accepting images.
2. **Human-reviewed labels:** define and review the four visible classes — young green, mature green, yellow and brown — while separating visible appearance from biological maturity and harvest suitability.
3. **Dataset quality:** check annotation geometry, duplicates and leakage-safe splits grouped by orchard/tree/capture session.
4. **First reproducible AI baseline:** after the data gate passes, evaluate a suitable open-source vision model locally on CPU; publish per-class precision, recall, F1, confusion counts, sample sizes, failure cases, runtime and RAM. Until then, model metrics remain NOT MEASURED.
5. **Harvest decision support:** keep target-stage selection, uncertainty handling, safety checks and human approval as advisory software. No actuator command or automatic cut is enabled.

### Intended product workflow (future integration)
Orchard camera/image input → image-quality and provenance checks → coconut/bunch detection → per-fruit four-class assessment → operator selects **Selective Harvest** or **Mixed-Stage Harvest** → location/reach/obstacle and safety checks → human approval → future supported cutting/collection mechanism → outcome and audit record.

A mixed-maturity bunch must be assessed fruit by fruit. The proposed mechanical concept is one controlled cut at the bunch attachment, with the bunch supported before release. Future collection options include a basket or a controlled drop into a verified clear landing area. These are design requirements, not implemented capabilities.

### Robotics research direction
The longer-term concept is a mobile orchard vehicle with perception sensors, navigation, a robotic arm and a guarded cutting/retention mechanism. The **0–30 m** palm-height range is a long-term research challenge: seeing a bunch, reaching it mechanically and safely harvesting it are separate problems requiring separate evidence. No height range, autonomous cutting, basket handling or field operation is currently validated.

**Immediate next gate:** complete image-rights/provenance review and human annotation QA, freeze leakage-safe dataset splits, then run and publish the first reproducible CPU vision benchmark. Do not advance to physical harvesting trials until a separate mission definition, engineering design, hazard analysis and supervised test plan are approved.

## Latest verified progress — 24 November 2026

Recent work has strengthened the evidence and field-validation foundation. These are documentation and software-governance milestones; they do not establish a trained model or a working harvesting robot.

- **Dataset split isolation:** merged validator and tests check group separation using orchard, tree, capture-session and near-duplicate metadata. This is a leakage-control check, not image-rights, label-quality or model-accuracy verification. See [dataset quality gate](docs/COCONUT_DATASET_QUALITY_GATE_V0_2.md).
- **Public image-source research:** six candidate sources have been documented, with a separate review of their public archive/export paths. No image archive or image file has been downloaded. See [open dataset source audit](docs/COCONUT_OPEN_DATASET_SOURCE_AUDIT_V1.0.md) and [archive access review](docs/COCONUT_DATASET_ARCHIVE_ACCESS_REVIEW_V1.0.md).
- **Mendeley coconut tree crown:** the public dataset page describes 400 RGB images at 512 × 512 and declares CC BY 4.0. Its archive has not been retrieved or inspected. A linked research description reports a different image count (900); this discrepancy remains unresolved and the counts must not be combined.
- **CRipS research candidate:** the paper reports an approximately 500-image RGB orchard dataset, but a public downloadable archive and reuse licence have not been verified. It is not approved for training.
- **Thailand field discovery:** merged a blank [G0 field evidence register](docs/COCONUT_G0_EVIDENCE_REGISTER.md) for future farm, worker-workflow and processor discovery. It contains no interviews, field measurements or customer validation yet.

**Current evidence boundary:** no approved real-orchard training set, image-level rights approval, completed four-class human annotation, trained/evaluated PUI89 model, held-out accuracy metrics or real-world harvesting validation is established. No downloads were made as part of this update.

**Next gate:** verify source files and licence conditions without bypassing access controls; reconcile the four public visual classes with the internal schema; then complete human annotation/QA and leakage-safe splits before any reproducible CPU evaluation.


## Single-Cut, Mixed-Maturity Coconut Bunch (Proposed)

**Design concept:** one coconut bunch is detached with one cut at its bunch attachment point. That single bunch may contain individual coconuts at different visible maturity stages. The system must assess the whole bunch and classify each visible coconut separately; it must not assume that every fruit in one bunch has the same maturity.

The four proposed visual classes are:

1. **Young Green**
2. **Mature Green**
3. **Yellow**
4. **Brown**

**Intended workflow**
- Capture real images of complete, naturally mixed-maturity bunches before and after cutting, where safely and lawfully available.
- Detect or segment individual coconuts within the same bunch, preserve a shared bunch identifier, and assign a per-fruit class, confidence/uncertainty and review status.
- Produce per-bunch counts for all four classes, including zero counts where a class is absent. Mark occluded, overlapping, damaged or ambiguous fruit for human review.
- Evaluate candidate open-source models on the same rights-cleared, human-annotated real-image dataset. Compare per-class precision, recall and F1, confusion matrix, instance-count accuracy, missed/duplicate detections, uncertainty handling, inference time and peak RAM. Use leakage-safe train/validation/test splits and report sample sizes and failure cases.
- Treat a **single cut at the bunch attachment** as a future mechanical design requirement. The bunch must be securely supported/captured and its fall path controlled before any cutting trial. Cutting must remain operator-supervised with guarded tooling, emergency stop and a safe state; AI classification alone must never trigger a cut.

**Variable geometry requirement:** investigate different bunch sizes, shapes, fruit sizes, orientations, stem/peduncle geometry, camera viewpoints, lighting and levels of occlusion. The phrase “all dimensions” is a design objective to test across a defined operating envelope—not a claim that one cutter or model can already handle every possible dimension.

**Evidence status:** proposed design and validation plan only. The user will supply or collect real images for testing. No real-image benchmark, selected best model, mixed-bunch accuracy, universal dimensional capability, one-cut mechanical performance or safe physical harvesting capability is established. Do not publish model rankings or performance numbers until reproducible tests have run.

## Product documentation

- [Labour-reduction market and engineering requirements](docs/COCONUT_LABOUR_REDUCTION_MARKET_REQUIREMENTS.md) — target customers, market-validation priorities, engineering requirements, KPIs and development gates.
- [G0 Thailand field evidence register](docs/COCONUT_G0_EVIDENCE_REGISTER.md) — blank, traceable record for site visits, interviews, operational baselines, KPIs and evidence review.

- [Software MVP product specification](docs/COCONUT_SOFTWARE_MVP_PRODUCT_SPEC.md)
- [Real-image validation execution gates](docs/COCONUT_REAL_IMAGE_VALIDATION_EXECUTION_GATES.md)
- [Four-class and 0–30 m validation roadmap](docs/FOUR_CLASS_0_30M_VALIDATION_ROADMAP.md)
- [Coconut maturity, location and harvest requirements](docs/COCONUT_MATURITY_LOCATION_HARVEST_REQUIREMENTS.md)

## Shared PUI89 engineering

Cross-product architecture, evidence contracts, safety, privacy, security, recovery, device interaction and localization requirements are maintained centrally in the [PUI89 Shared AI Core](https://github.com/Pui89/PUI89-Shared-AI-Core). This repository defines Coconut-specific tasks and validation; shared requirements are linked, not duplicated.

Current maturity labels and portfolio scope follow the [PUI89 Portfolio Alignment Register](https://github.com/Pui89/Pui89.github.io/blob/main/docs/PUI89_PORTFOLIO_ALIGNMENT_REGISTER_2026-11-18.md) and [Evidence-Based Development Maturity Standard](https://github.com/Pui89/Pui89.github.io/blob/main/docs/PUI89_DEVELOPMENT_STAGE_STANDARD.md).

**PUI89 has five active products.** Shared AI Core is infrastructure, not an additional product.

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

## Future-Ready Technology Policy

This product follows the portfolio-wide [PUI89 Future-Ready Technology Policy v1.0](https://github.com/Pui89/PUI89-Shared-AI-Core/blob/main/docs/architecture/PUI89_FUTURE_READY_TECHNOLOGY_POLICY_V1.0.md). The policy requires upgradeable interfaces, evidence-based technology selection, provenance/licence review, local-first resource discipline, compatibility testing, safe fallback and controlled release scope. Technology candidates are reviewed monthly and architecture decisions quarterly. This link records policy adoption intent; it does **not** claim that model switching, hardware abstraction, sensor adapters, automated monitoring or product-level validation are already implemented.

## Product-Specific Technology Upgrade Plan

**Gartner 2026 alignment:** Physical AI, Domain-Specific Language Models, hybrid/AI supercomputing and Digital Provenance. See the [canonical portfolio policy](https://github.com/Pui89/PUI89-Shared-AI-Core/blob/main/docs/architecture/PUI89_FUTURE_READY_TECHNOLOGY_POLICY_V1.0.md).

| Upgrade area | Planned sequence (not yet a capability claim) |
|---|---|
| Vision & multimodal AI | Establish licensed image provenance and a reproducible RGB baseline; benchmark detection, classification and segmentation; evaluate multimodal fusion only when it improves crop decisions. |
| Orchard 3D / multi-view mapping | Define mapping use cases and coordinate/data contracts; evaluate multi-view/depth mapping after the RGB baseline; retain 3D only when measured value justifies its compute and sensor cost. |
| Edge AI | Benchmark CPU-first inference, memory, latency, power and thermal behaviour; keep model/runtime replaceable and define a fallback. |
| Domain knowledge assistant | Consider a bounded crop-domain assistant with cited sources and human review; no unsupported agronomic recommendations. |

**First gate:** data rights/provenance, human-verified labels, reproducible metrics and resource baseline. **Status:** Planned roadmap only.


## Long-Term Technology Evolution & Anti-Obsolescence Strategy (2027–2030+)

This forward-looking roadmap extends the current P1–P4 development sequence beyond the 2026 trend baseline. It identifies evaluation horizons, not guaranteed future capabilities or fixed adoption dates. Each technology remains conditional on verified user value, provenance and licensing, target-hardware fit, safety, maintainability and reproducible evidence.

| Horizon | Product evolution focus |
|---|---|
| 2027 | Establish replaceable vision/model interfaces, licensed dataset provenance, reproducible RGB baselines and CPU-first edge benchmarks. |
| 2028 | Evaluate multimodal and multi-view perception, depth/3D orchard mapping and crop-specific small/domain models only where measured field value justifies added sensors and compute. |
| 2029 | Explore spatial/temporal orchard intelligence, crop-state tracking and evidence-grounded decision support with agronomist review. |
| 2030+ | Maintain model, sensor and edge-hardware portability; evolve toward precision-orchard workflows without depending on one model vendor or sensor generation. |

**Continuous anti-obsolescence rule:** review technology signals monthly, architecture quarterly and the full roadmap annually; trigger an out-of-cycle review when a critical dependency is unsupported, a security issue emerges, or measured performance/resource limits are breached. Keep a verified baseline, migration and rollback path, compatibility/regression tests and a documented decision for every upgrade. Do not adopt a trend solely because it is new. **Status:** Planned roadmap; no future capability is claimed as implemented or validated.


---

## Academic Research Direction — Q1-Targeted Study (Proposed)

**Research topic:** Multimodal Vision AI for Coconut Maturity and Harvest Readiness  
**Working manuscript title:** *Temporal, Occlusion-Aware Multimodal Vision for Uncertainty-Calibrated Coconut Maturity Assessment under Orchard Conditions*

**Status:** Proposed academic study for lecturer review. The research gap, novelty, protocol, dataset permissions and hypotheses must be verified before the study is approved. No research result or Q1 publication is claimed.

### 1. Problem and motivation

A single RGB image may not provide enough evidence to distinguish coconut maturity reliably. Fruit overlap, partial visibility, changing illumination, camera distance, cultivar, orchard conditions and differences between visible colour and biological maturity can lead to incorrect decisions. The study will investigate whether multiple observations and complementary visual/geometric information can improve maturity assessment while explicitly identifying uncertain cases.

The four product assessment classes remain **young green, mature green, yellow and brown**. Visible colour must not automatically be treated as biological maturity or harvest suitability; the ground-truth protocol must be defined with an agricultural expert.

### 2. Research gap to verify

- Limited evaluation of maturity classification across independent trees, capture sessions and orchards.
- Performance degradation from occlusion, mixed-maturity bunches, lighting and viewpoint changes.
- Insufficient calibration and abstention: models may output a confident class when evidence is weak.
- Limited evidence connecting image observations with expert-confirmed maturity and harvest suitability.

These are candidate gaps, not established claims of being the first or only study.

### 3. Research questions and hypotheses

- **RQ1:** How does temporal or multi-view evidence affect four-class coconut maturity assessment compared with a single RGB frame?
- **RQ2:** Does adding available depth/geometric information improve performance under occlusion and variable distance?
- **RQ3:** Can calibrated uncertainty and selective human review reduce consequential classification errors?
- **H1:** Temporal/multi-view evidence will improve class-wise performance on held-out trees or orchards compared with a matched single-frame baseline.
- **H2:** An uncertainty-aware model will improve the risk–coverage trade-off by abstaining on ambiguous or heavily occluded fruit.

Hypotheses must be revised after the literature review and power/precision analysis.

### 4. Proposed hybrid-AI method and workflow

1. **Data quality:** verify image rights, provenance, capture metadata and annotation instructions.
2. **Fruit localisation:** compare a lightweight specialist detector/instance-segmentation model with a strong contemporary vision baseline.
3. **Visual representation:** evaluate a conventional CNN or vision transformer; assess a suitable vision foundation model only if its origin, licence and resource fit are verified.
4. **Temporal/multi-view fusion:** associate observations of the same fruit or bunch where identity can be established; compare single-frame, feature-level and decision-level fusion.
5. **Optional geometry:** incorporate depth or size/shape cues only where calibrated depth data are genuinely available.
6. **Decision reliability:** evaluate probability calibration, uncertainty estimation and abstention/human-review thresholds.
7. **Decision support:** produce per-fruit and per-bunch class counts with provenance and review status. The AI must not autonomously trigger cutting or harvesting.

### 5. Candidate datasets and data collection

- **Essential original data:** permissioned coconut orchard images/video, with tree, bunch, fruit, orchard, date/session, camera, lighting, viewpoint and occlusion metadata.
- Obtain expert-reviewed labels for the four classes and document how borderline cases are adjudicated. Where biological maturity is claimed, collect an appropriate independent ground-truth measure rather than relying on colour alone.
- RGB-D fruit datasets such as **AmodalAppleSize RGB-D** may be considered for methodological transfer or geometry experiments; they are not coconut maturity ground truth.
- Public coconut image sources remain candidates until archive accessibility, licence, provenance and image-level suitability are independently verified. Do not treat a dataset webpage as proof that its files are approved for training.

### 6. Experimental design

- **Baselines:** class-prior/majority baseline; colour/texture features where justified; compact CNN; specialist detector/classifier; contemporary transformer or foundation-feature baseline with matched evaluation conditions.
- **E1:** single-frame versus temporal/multi-view input.
- **E2:** RGB-only versus RGB plus calibrated depth/geometric features.
- **E3:** stratified occlusion, overlap, distance, illumination and mixed-maturity bunch tests.
- **E4:** calibration and selective prediction; plot risk versus coverage and review workload.
- **E5:** grouped generalisation to held-out trees, sessions and preferably a separate orchard.
- **E6:** CPU-first latency, throughput, peak RAM and model-size measurements.

**Primary outcomes:** pre-register macro-F1 or balanced accuracy as the primary endpoint, with per-class precision/recall and confusion matrix.  
**Secondary outcomes:** instance-count error, calibration (Brier score/reliability diagram and carefully specified ECE), selective risk/coverage, latency, RAM and model size.

### 7. Expected scientific contribution

A reproducible, orchard-aware evaluation protocol and a temporal/occlusion-aware, uncertainty-calibrated coconut maturity method, including explicit human-review behaviour and evidence about when additional modalities help or do not help.

### 8. Validation, ethics and publication gates

Use leakage-resistant splits grouped by tree, bunch, capture session and orchard; keep near-duplicates together and seal the test set. Report annotator agreement, sample counts, confidence intervals, failure cases and negative results. Confirm landowner/worker permissions and image privacy. A Q1 submission requires verified novelty against current literature and independent evidence; Q1 status or acceptance is not guaranteed.

## 360° Intelligence

The [360° Intelligence Profile v1.0](docs/PUI89_360_DEGREE_INTELLIGENCE_PROFILE_V1.0.md) defines multi-view orchard/tree/bunch perception, cross-view fruit association, duplicate-count prevention and human review. **Status: Proposed**; no 360° camera system or field result is established.
\n\n## Hybrid End-to-End Multimodal AI\n[PUI89 Hybrid End-to-End AI Product Adapter v1.0](docs/architecture/PUI89_HYBRID_END_TO_END_AI_ADAPTER_V1.0.md) — proposed architecture and project-specific adoption plan. E2E benefits require comparative evidence; product boundaries, independent safety and evidence gates remain mandatory.\n