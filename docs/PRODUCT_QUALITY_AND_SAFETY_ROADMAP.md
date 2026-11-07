# Product Quality and Safety Roadmap — Coconut-Harvest-AI

**Status:** development roadmap, not a safety certification, compliance claim or proof of validated real-world performance.

## Project-specific safety focus

coconut arm, guarded cutter, collection basket and lowering system; four maturity classes; uncertain height; 0–30 m is a design challenge only.

**Required conservative behavior:** No cut unless target, maturity, measured geometry, reach, arm/base stability, collision clearance, tool guard, basket readiness, retention/lowering path, communication health and human approval all pass.



## Environmental, water-ingress and fire-risk validation

**Current status: NOT VALIDATED.** No enclosure ingress rating, rain/flood tolerance, fire resistance, battery thermal-safety result or environmental operating limit is claimed for a physical Coconut Harvest AI system.

Before any outdoor or powered prototype test, define the actual operating environment and obtain qualified review of the enclosure, connectors, cable entries, moving joints, sensors, battery, charging arrangement and electrical isolation. Record the selected test standard and acceptance criteria for the exact design; do not assign an IP rating or fire-resistance class by assumption.

Required evidence gates:

1. **Water and dust exposure:** specify rain, splash, washdown, humidity, dust and drainage exposure from the intended farm use; assess ingress paths and condensation; test representative assembled hardware using a documented method. Keep powered and unpowered tests distinct, inspect internally after exposure, and record failures. Do not test in standing water or operate damaged/wet electrical equipment.
2. **Electrical and battery protection:** document battery chemistry, protection circuitry, fusing, isolation, connector ratings, charging controls, temperature limits and emergency disconnect. Verify these against the selected components and qualified design review before energising the prototype.
3. **Fire and thermal hazards:** assess battery fault, overcharge, short circuit, stalled motor, cutter friction, hot surfaces, wiring faults and charging faults. Define detection, isolation, evacuation and responder procedures. Any abuse or fault-injection testing must use a qualified, controlled test facility—not an improvised farm or office test.
4. **Post-exposure function:** after each environmental test, inspect seals, insulation, corrosion, sensor windows, brakes, guards, emergency stop and safety interlocks; repeat the relevant electrical and functional checks before any further operation.
5. **Evidence record:** publish the hardware revision, component/BOM identifiers, test method, environmental conditions, instruments and calibration, pass/fail criteria, results, failures, reviewer and limitations. A component datasheet, concept rendering or software test is not system-level validation.

Until these gates are completed, the project must be described as a software/evaluation-preparation prototype with a proposed outdoor robot concept. Do not advertise it as waterproof, weatherproof, fireproof, fire-resistant or safe for wet operation.

## Cross-project quality gates

1. **Requirements and hazard analysis:** define intended use, prohibited use, users, operating environment, measurable acceptance criteria, foreseeable misuse, hazards, emergency procedures and stop-work authority with qualified domain experts.
2. **Fail-safe software:** test missing, stale, conflicting, malformed, out-of-range and low-confidence inputs; communications loss; emergency stop requests; restart/power loss; safe hold; manual override; bounded logging; and recovery from faults. Never silently guess missing safety data.
3. **Reproducible evidence:** record exact commit, environment, configuration hash, test/scenario ID, expected and observed outcome, failure codes, latency where measured, reviewer and NOT RUN items. Keep synthetic, simulation, lab and field evidence separate.
4. **Independent evaluation:** freeze a lawful, licensed, human-reviewed, leakage-safe held-out dataset or scenario set before testing. Publish sample counts, class-wise performance, false positives/negatives, uncertainty and limitations. Never copy literature metrics as project results or infer results from tool presence.
5. **Physical validation:** before people-at-risk testing, require a documented risk assessment, qualified engineering review, staged tests, emergency/recovery plan, incident log, and signed acceptance criteria for the exact hardware/software configuration.
6. **Cybersecurity and privacy:** least privilege, no secrets in Git, dependency/vulnerability review, controlled updates and rollback, data minimisation, access controls, retention/deletion rules and incident response.
7. **Maintainability:** document calibration/pre-use checks, operating limits, wear parts, maintenance intervals, fault codes, operator training, spares, warranty/support assumptions and safe decommissioning.
8. **Commercial release gate:** no buyer-facing safety, accuracy, autonomy, lives-saved, reach, chemical-identification or rescue-capability claim without independent evidence for the released configuration. Include limitations and known failure modes.

## Standards and external review

Use [ISO 12100](https://www.iso.org/standard/51528.html) as a general machinery risk-assessment starting point where applicable and the [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework) for AI risk-lifecycle practices. [ISO 10218-1:2025](https://www.iso.org/standard/73933.html) and [ISO 10218-2:2025](https://www.iso.org/standard/73934.html) address industrial robots and industrial robot applications; applicability to each PUI89 mobile, agricultural, rescue or public-facing concept must be determined by qualified specialists. Referencing a standard is not compliance or certification. Check relevant Thai and target-market laws and standards before any pilot or sale.

## Customer/buyer evidence pack

Before a pilot, prepare: intended-use statement; operating envelope; risk register and residual risks; test plan/results including failures; dataset/model/sensor provenance; hardware/software bill of materials; cybersecurity/privacy notes; installation/site requirements; operator training; maintenance/support plan; incident and rollback procedure; and clear exclusions. A polished README or simulation pass alone is not product readiness.

## Free-first policy

Prefer offline, standard-library checks and synthetic tests first. No paid API, recurring service, automatic model download, external data upload or hardware actuation is required by this roadmap. Review licences, privacy, hardware fit, maintenance cost and safety impact before adding any tool or dependency.
