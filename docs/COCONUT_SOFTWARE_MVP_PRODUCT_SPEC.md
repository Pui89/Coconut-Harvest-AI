# Coconut Harvest AI — Software MVP Product Specification

**Version:** 1.0  
**Status:** proposed build specification; not an implemented product, validated detector, customer pilot, or commercial release.  
**Product strategy:** deliver a useful, bounded software product before attempting to commercialise a physical harvesting robot.

## 1. Product decision

The first product is an **operator-assisted coconut inspection and harvest-planning application**. It helps a farm operator organise image-based inspections, review candidate fruit, record maturity assessments, and produce traceable reports.

The first release is not an autonomous harvesting system. It does not control a robot, recommend cutting from unverified AI output, guarantee maturity, estimate harvest yield, or claim a validated 0–30 m capability.

## 2. Intended first customer

Primary discovery group:
- coconut growers and farm managers;
- agricultural cooperatives and extension teams;
- agricultural research groups;
- agricultural equipment and robotics integrators.

The first discovery activity is to understand the actual inspection workflow and agree on a measurable trial. No customer, partner, order, or willingness-to-pay is assumed.

## 3. MVP user workflow

1. **Create an inspection:** record an inspection ID, date, operator alias, farm/site code, and optional notes. Avoid unnecessary personal data.
2. **Add an image:** import a user-authorised image and preserve its file hash and source/provenance fields. Reject unsupported or unreadable files clearly.
3. **Review image quality:** let the operator mark image quality, visibility, occlusion, and whether fruit can be assessed. Do not infer missing metadata.
4. **Record fruit candidates:** allow a human operator to add or correct bounding boxes and select one of four project labels: young green, developing green, mature green, or brown/aging. Unknown and needs-review remain valid outcomes.
5. **Record assessment:** store the label, reviewer, review time, confidence as a human-entered or model-supplied value with its origin stated, and reason for uncertainty.
6. **Generate a report:** export a machine-readable JSON record and a human-readable inspection summary containing the image hash, annotations, review status, limitations, and unresolved items.
7. **Correct and audit:** preserve revisions and identify who changed a label; do not silently overwrite prior assessments.

## 4. AI integration boundary

The MVP must work as a useful human-led inspection and evidence tool before any detector is integrated.

A future detector may propose candidate boxes and labels only after:
- source and commercial reuse rights are verified for every training/evaluation asset;
- annotations are reviewed and quality-checked;
- train/validation/test splits are separated by tree, orchard, source, or capture session;
- a held-out evaluation protocol is frozen;
- class-wise precision, recall, F1 and/or appropriate detection metrics, sample counts, thresholds, uncertainty, and failure cases are published;
- model and dataset provenance, licences, and intended-use limits are documented.

Model outputs must be labelled as machine-generated proposals. Human review remains visible. Missing, obscured, conflicting, or low-confidence cases must remain UNKNOWN / REVIEW. No model output may authorise cutting or physical actuation.

## 5. Functional acceptance criteria

| ID | Requirement | Acceptance evidence |
|---|---|---|
| MVP-01 | Create and reopen an inspection record | Automated test and sample record |
| MVP-02 | Import a supported image without altering the source | File hash before/after matches |
| MVP-03 | Reject missing, corrupt, or unsupported image inputs | Negative tests with explicit error codes |
| MVP-04 | Record all four maturity labels plus UNKNOWN / REVIEW | Schema and validation tests |
| MVP-05 | Create and edit human annotations | Bounding-box boundary and revision tests |
| MVP-06 | Preserve provenance and reviewer history | JSON round-trip and audit tests |
| MVP-07 | Export a report with evidence and limitations | Golden-file/report schema tests |
| MVP-08 | Handle missing or conflicting metadata conservatively | Fail-closed regression tests |
| MVP-09 | Run without hosted AI services | Offline test; no network dependency |
| MVP-10 | Keep all robot/actuator operations absent | Static inspection and tests proving no actuation path |

A criterion is complete only when its test or review evidence is linked to a commit and recorded. A planned feature is not a pass.

## 6. Non-functional and product-quality requirements

- **Reliability:** deterministic validation and export; actionable errors; no silent data loss.
- **Privacy:** data minimisation; local-first handling by default; no image upload without an explicit, documented user action and approved destination.
- **Security:** validate file types and sizes; avoid path traversal; restrict file access to the selected workspace; do not store credentials or secrets in records or logs.
- **Usability:** a farm operator can complete a basic inspection without reading developer documentation; use clear labels and Thai/English terminology where practical.
- **Accessibility:** keyboard-operable workflows, readable contrast, clear status text, and no colour-only meaning.
- **Maintainability:** versioned schemas, migration policy, documented backup/export and recovery.
- **Interoperability:** documented JSON export; no proprietary cloud dependency in the first release.

## 7. Release stages and commercial gates

### Stage A — Internal software alpha
- Complete MVP-01 to MVP-10.
- Run automated tests and manual usability walkthroughs with synthetic fixtures.
- Publish known limitations and a reproducible setup guide.
- Status label: **internal alpha**.

### Stage B — Research / design-partner evaluation
- Obtain permission and a written data-handling agreement before using partner images.
- Agree on workflow, sample selection, evaluation criteria, and success thresholds with the partner.
- Keep partner data private unless publication permission is explicit.
- Report false positives, false negatives, unknown/review rates, and operator corrections.
- Status label: **controlled evaluation**, not commercial validation.

### Stage C — Limited pilot candidate
- Complete lawful data and model review, security/privacy review, user acceptance, backup/recovery checks, and a documented support process.
- Demonstrate performance on an independent, representative, held-out dataset for the defined use case.
- Define the operating environment, exclusions, support responsibilities, incident handling, and rollback.
- Obtain qualified review of any safety implications.
- Status label: **pilot candidate** only after evidence review.

### Stage D — Commercial release
Before offering a product for sale, confirm:
- legal ability to contract, invoice, collect payment, and provide support in the relevant jurisdiction;
- product ownership, contributor rights, open-source notices, dataset rights, model licences, and third-party terms;
- applicable Thai and target-market privacy, consumer, software, and product requirements;
- final release testing, security review, installation documentation, backup, support, update and rollback procedures;
- truthful product claims, defined warranty/service scope, pricing basis, and customer terms.

A website, repository, concept image, successful unit test, or discussion with a prospective partner does not by itself satisfy these gates.

## 8. Evidence ledger fields

Every release claim should be linked to:
- requirement ID and acceptance criterion;
- implementation commit and release version;
- test command, environment, and result;
- dataset/model/configuration identifiers and hashes where applicable;
- sample counts, metric definitions, thresholds, and failure cases;
- reviewer and review date;
- limitations, unresolved risks, and NOT RUN items.

Keep software tests, synthetic scenarios, simulation, laboratory measurements, field evaluation, and independent certification as separate evidence classes.

## 9. First implementation sequence

1. Inspect existing image intake, annotation, dataset preflight, report, and provenance tools; reuse them rather than duplicate them.
2. Map existing code and tests against MVP-01 to MVP-10.
3. Implement only the missing human-led inspection workflow and schema.
4. Add tests for each acceptance criterion and failure path.
5. Run the existing project verification before introducing optional dependencies.
6. Produce one complete example inspection using a rights-cleared sample or synthetic fixture; label it clearly.
7. Conduct customer discovery before expanding features or choosing a pricing model.

## 10. Explicit exclusions from this MVP

- autonomous fruit maturity decisions;
- unverified AI accuracy or maturity guarantees;
- height or reach estimation from ordinary RGB images;
- robotic arm, cutter, basket, lowering, or physical control;
- safety certification or field-harvest claims;
- automatic upload of farm images;
- paid APIs, recurring services, or unapproved external dependencies.

**Definition of a credible first product:** an operator can create, review, correct, export, and audit an inspection record; the workflow passes its documented acceptance tests; the product's limits are obvious; and a prospective farm partner can evaluate it without being misled about AI or robot capabilities.
