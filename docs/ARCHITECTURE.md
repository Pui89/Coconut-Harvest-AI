# Coconut Harvest AI — Software Architecture and Current Implementation Boundary

**Status: architecture reference for the current software/concept stage.** This document describes intended system boundaries and distinguishes repository software from proposed robot hardware. It is not a description of a completed autonomous robot.

## 1. Current system boundary

The repository currently contains software foundations for:
- image/data provenance review and dataset preflight;
- maturity-label and annotation workflow design;
- detection-metric evaluation utilities (evaluation tooling, not a trained detector result);
- rule-based task and fail-safe decision logic;
- simulation-oriented scenarios and evidence-report validation;
- automated tests and continuous-integration checks.

The repository does **not** currently establish a trained, independently evaluated coconut detector, calibrated RGB-D perception, a validated 3D orchard map, a built robotic arm, a guarded cutter, a collection basket, a controlled lowering mechanism, or a field-tested harvesting robot.

## 2. Intended high-level workflow

1. **Image intake:** accept a permitted image with traceable source metadata.
2. **Input-quality gate:** check image availability and quality; reject unusable or ambiguous inputs.
3. **Perception (future model gate):** a detector may propose fruit locations and maturity labels only after a licensed dataset, human-reviewed annotations, and held-out evaluation are available.
4. **Uncertainty and review:** represent unknown, occluded, conflicting, stale, or low-confidence observations explicitly; request human review rather than guessing.
5. **Task proposal:** software may produce a non-actuating recommendation such as review, wait, or candidate target.
6. **Simulation/evidence record:** test decision logic in defined scenarios and record inputs, outputs, failures, configuration and evidence hashes.
7. **Hardware integration (future, gated):** any physical sensing, positioning, cutting, capture or lowering system requires separate mechanical design, risk assessment, independent safety functions and staged validation by qualified specialists.

## 3. Conceptual components and status

| Component | Intended responsibility | Current status |
|---|---|---|
| Image/data provenance | Record source, licence review, file hash and review state | Software/documentation tools; each asset still needs individual approval |
| Maturity taxonomy | Four working labels: young green, developing green, mature green, brown/aging | Project label scheme; annotation quality and class performance not established |
| Coconut detector | Propose fruit boxes and class scores | No validated detector accuracy claim |
| Depth/3D perception | Estimate target geometry and distance | Future integration; no calibrated sensor performance claimed |
| Height metadata | Store measured palm height separately from fruit maturity | Protocol and template; no verified 0–30 m dataset claim |
| Task/fail-safe logic | Reject missing/uncertain inputs and select review/hold outcomes | Software logic and tests; not a hardware safety controller |
| Arm, cutter, basket, lowering path | Physical positioning, guarded cutting and controlled capture | Design concept only; not built or physically validated |
| Simulation/evidence reports | Exercise software scenarios and validate report integrity | Software tests/CI; simulation does not prove field capability |
| Human oversight | Review uncertain targets and authorise any future staged test | Required design principle; no autonomous harvesting claim |

## 4. Four maturity labels

- **Young green**
- **Developing green**
- **Mature green**
- **Brown / aging**

Colour alone is not sufficient to establish maturity. Cultivar, intended product, lighting, occlusion and field conditions can affect visual appearance. Unknown or obscured fruit must remain unknown/review—not be forced into a class.

A mixed-stage bunch is a scene condition, not a fifth maturity label. Where possible, assess individual visible fruits separately.

## 5. Safety and actuation boundary

The current software workflow is non-actuating. A recommendation, test pass, simulation result or diagram must never be interpreted as permission to move a physical arm or activate a cutter.

Before any hardware integration, the project requires:
- documented intended use, operating envelope and hazard analysis;
- measured geometry, load, stability and collision-clearance evidence;
- guarded tools, retention/lowering design and independent safety functions;
- tested emergency stop, safe hold, loss-of-link and power-fault behavior;
- qualified engineering review and staged tests in a secured environment;
- human approval and a documented recovery procedure.

Missing, stale, conflicting or uncertain safety-critical information must block the proposed task and trigger review/hold.

## 6. Performance reporting

Do not publish detector accuracy, inference latency, reach, throughput, harvest rate or field reliability unless measured on a defined configuration and reproducible evaluation set. Reports should include dataset/source status, sample counts, split method, class-wise precision/recall/F1 or appropriate detection metrics, thresholds, failure cases, uncertainty and measurement conditions.

Software unit tests validate code behavior under test conditions only. Synthetic scenarios validate only the scenarios encoded. Neither establishes real-world perception, mechanical feasibility or safety.

## 7. Engineering standards and references

The project uses the following as **design and review references**, not as claims of compliance or certification:

- [ISO 12100 — Safety of machinery: risk assessment and risk reduction](https://www.iso.org/standard/51528.html): a starting point for machinery hazard identification and risk reduction where applicable.
- [ISO 10218-1:2025 — Industrial robots: safety requirements](https://www.iso.org/standard/73933.html) and [ISO 10218-2:2025 — Industrial robot applications and robot cells](https://www.iso.org/standard/73934.html): applicability to a future mobile/agricultural robot must be assessed by qualified specialists.
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework): useful lifecycle guidance for AI validity, reliability, safety, transparency and accountability.

The applicable standards depend on the final machine, intended use, workplace, jurisdiction and integration. Obtain qualified review of the current editions and relevant Thai/target-market requirements before any pilot or sale. Referencing a standard does not mean the project meets it.

## 8. Related project documents

- [Product quality and safety roadmap](PRODUCT_QUALITY_AND_SAFETY_ROADMAP.md)
- [System fault and hardware safety playbook](SYSTEM_FAULT_AND_HARDWARE_SAFETY.md)
- [Height-labeling protocol](height-labeling-protocol.md)
- [Shared PUI89 AI Core integration](SHARED_PUI89_AI_CORE_INTEGRATION.md)
- [Evidence benchmark and simulation reports](../reports/)
