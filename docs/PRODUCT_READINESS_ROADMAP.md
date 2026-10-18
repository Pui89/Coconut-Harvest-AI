# Product Readiness Roadmap — Application and Agricultural Robot

## Current status (honest baseline)

**Product category:** research-stage agricultural AI software prototype with a proposed robotic harvesting system.

The repository includes a local Streamlit decision-support demo, synthetic end-to-end pipeline, safety-gate logic, sensor-quality checks, tests, and documentation. The current app displays an uploaded photo but does not automatically detect coconuts in that image. The current pipeline uses synthetic imagery and explicitly supplied evidence; its simplified planner is not a validated collision checker. No physical robot, calibrated depth sensor, ROS 2 actuator interface, cutter/gripper, emergency-stop circuit, or field trial is established by this repository.

**Not yet commercially ready:** there is no verified detector benchmark, field dataset, validated robot integration, production support process, product cybersecurity review, or conformity assessment evidence. Do not market the system as autonomous, safe for unsupervised operation, or ready for production harvesting.

## Product boundaries

Keep these deliverables distinct:

1. **AI application:** local-first interface for image review, candidate detection once implemented, evidence capture, uncertainty display, decision support, exportable audit records, and operator review.
2. **AI robot:** a separate physical system with calibrated sensors, a robot description, motion controller, independent collision checking, guarded work area, emergency-stop hardware, and verified safe-state behavior.
3. **Commercial service/product:** installation and updates, user documentation, licensing and third-party notices, support and incident handling, privacy/security controls, manufacturing/maintenance process, and jurisdiction-specific compliance.

A working application is not proof of a working robot. Passing software tests is not proof of machinery safety.

## Release gates

### Gate A — Reproducible software baseline
- [ ] Clean environment setup documented and tested.
- [ ] Unit tests and static checks run automatically on pull requests.
- [ ] Dependencies pinned or bounded with a tested compatibility matrix.
- [ ] No secrets, private images, or personal data committed.
- [ ] Reproducible demo output and known limitations documented.
- [ ] Dependency and licence inventory generated and reviewed.

### Gate B — Evidence-backed AI application
- [ ] Representative, permissioned dataset with source/licence manifest.
- [ ] Written annotation rules and review of label quality.
- [ ] Frozen train/validation/test split with source/tree/session leakage controls.
- [ ] A detector whose classes actually include coconuts, with model/weights licence checked.
- [ ] Held-out precision, recall, F1 and AP at explicit IoU thresholds.
- [ ] Per-condition results for occlusion, lighting, distance and clutter where sample counts permit.
- [ ] Runtime, memory use, hardware, preprocessing, versions and failure examples reported.
- [ ] Uncertainty and low-confidence behavior visible to the operator.
- [ ] Privacy notice, local data-retention controls, and accessible operator workflow reviewed.

### Gate C — Simulation and robot integration
- [ ] Named robot model and validated kinematic description.
- [ ] Joint, workspace, speed, force and payload limits derived from actual hardware specifications.
- [ ] Independent collision checking tested against obstacle and edge cases.
- [ ] Sensor calibration, synchronization, dropout and stale-data behavior measured.
- [ ] Physics-backed simulation includes relevant geometry, contact and failure conditions.
- [ ] Hardware-in-the-loop tests performed before field testing.
- [ ] Emergency stop and safe-state controls are independent of AI software.
- [ ] Formal hazard analysis and risk-reduction evidence reviewed by competent engineers.

### Gate D — Controlled field validation
- [ ] Written test plan and permission for the test site.
- [ ] Supervised trials in a controlled, exclusion-zoned environment.
- [ ] Predefined success, failure, abort and stop criteria.
- [ ] Logged target detection, localization, planning, cycle time, harvest success, damage, dropped objects and near misses.
- [ ] Environmental coverage includes realistic lighting, wind/movement, occlusion, varied trees and sensor degradation.
- [ ] Independent review of incidents and residual risks.
- [ ] No unattended operation until the complete system has passed applicable safety and conformity requirements.

### Gate E — Commercial release
- [ ] Intended use, prohibited use, target customer and supported hardware specified.
- [ ] Applicable machinery, electrical, EMC, radio, cybersecurity, privacy and AI requirements assessed for each sales jurisdiction.
- [ ] Required technical file, risk assessment, test reports, declarations, marking and instructions completed where applicable.
- [ ] Third-party model/data/software licences cleared for commercial use.
- [ ] Secure updates, version rollback, vulnerability disclosure, backups and audit logs implemented.
- [ ] Manufacturing QA, maintenance schedule, spare parts, training, warranty and incident-response process defined.
- [ ] Product liability, insurance, export/import, worker-safety and local service obligations reviewed.

## Commercial positioning before the gates pass

Use wording such as **“research prototype for AI-assisted coconut-harvesting decision support”**. Show simulated output and real-world photos only with clear labels. Do not promise autonomous harvesting, yield gains, reduced injury, quantified accuracy, or safety benefits without independent evidence.

## Low-cost execution order

1. Automate software checks and fix failures.
2. Implement and test the CSV detection evaluator.
3. Build a legally reusable labelled dataset and freeze a small baseline split.
4. Select a compatible, commercially licensed detector only after checking its class labels and model licence.
5. Run local inference and record real predictions; evaluate on the frozen split.
6. Add a measured robustness report and visible uncertainty.
7. Only then expand to robot simulation, calibrated depth, and hardware integration.

The early software/data stages can be kept local-first and free of paid inference APIs. Real-world safety validation, compliance testing, insurance, manufacturing and commercial support may require qualified external people and budget; do not imply these can be eliminated by code alone.

## Release decision template

For every release, record:
- commit/tag and model version;
- test commands, environment, pass/fail summary and unresolved issues;
- datasets and licences used;
- benchmark results and test-set limitations;
- known hazards and mitigations;
- supported hardware/operating systems;
- intended use and explicit restrictions;
- reviewer and date;
- release status: research-only, internal test, supervised field trial, or commercially released after required approvals.
