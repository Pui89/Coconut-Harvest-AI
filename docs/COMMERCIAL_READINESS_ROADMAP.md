# Commercial and award-readiness roadmap — Coconut Harvest AI

**Updated:** 18 October 2026  
**Stage:** software prototype and simulation-oriented workflow; not a commercially validated physical harvesting robot.

## Product goal
Build a locally runnable AI application and simulation-first agricultural robot workflow to evaluate coconut detection, spatial localization, harvest-task planning and safety decisions. The first deliverable is a reproducible software demonstrator, not a promise of autonomous harvesting.

## Evidence already recorded
- Python CI passed on Python 3.10, 3.11 and 3.12: https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39096443251
- Candidate-image workflow collected 30 candidates and generated provenance/review files: https://github.com/Pui89/Coconut-Harvest-AI/actions/runs/39092214196
- Application components, annotation/conversion tools, dataset audits and simulation-oriented decision logic are present.

## Not yet proven
- A complete, labelled, licence-reviewed dataset.
- A trained detector's held-out precision, recall, mAP or latency.
- RGB-D localization accuracy, robot reachability, collision-free motion, safe cutting or field harvesting.
- Commercial ROI, customer demand, certification or superiority over competitors.

## Product ladder
1. **Open-source software demonstrator:** install instructions, lawful sample data, reproducible tests and clearly labelled concept/simulation media.
2. **Research benchmark package:** versioned dataset manifest, label QA, fixed splits, baseline results, error gallery and reproduction commands.
3. **Simulation demonstrator:** robot geometry and coordinate conventions, reachability/collision tests, stop/fault tests and recorded simulation runs.
4. **Research partner pilot:** orchard-specific data collection and supervised, non-cutting feasibility tests after risk assessment and qualified oversight.
5. **Commercial exploration:** customer discovery, cost model, maintenance plan, operator workflow and independent safety review.

## Immediate priorities
- [ ] Download and preserve the temporary 30-image candidate artifact before its stated expiry on 25 October 2026.
- [ ] Review source pages, reuse terms, attribution and relevance; exclude unclear items.
- [ ] Annotate approved images and conduct label-quality review.
- [ ] Create group-separated train/validation/test splits and pass duplicate/leakage audits.
- [ ] Train a baseline only after data and checkpoint licences are checked; freeze the test split before tuning.
- [ ] Publish actual metrics, latency, false positives/negatives, failure examples and reproduction steps. Mark missing results “not measured”.
- [ ] Measure RGB-D localization against reference positions.
- [ ] Test reachability, collisions, missing observations and stop/fault behavior in simulation.

## Minimum acceptance gates
| Gate | Required evidence |
|---|---|
| Reproducible software | Clean install, passing automated tests, recorded versions and commands |
| Dataset integrity | Sources/licences, labels, splits and leakage audit |
| Perception | Frozen held-out results, class counts, errors and latency |
| Spatial reasoning | Localization error measured against reference positions |
| Robot workflow | Repeatable simulation, reachability/collision and fail-safe tests |
| Buyer readiness | Scope, limitations, operating requirements, support plan and customer-validated use case |

## Commercial positioning
**Value proposition to test:** a low-cost, locally deployable research platform for coconut-orchard perception and harvest-task feasibility studies.

Potential early users to interview include agricultural research institutes, university robotics labs, coconut growers/cooperatives and equipment integrators. These are target segments, not confirmed customers.

Before pricing, investigate orchard size, harvest labour cost, yield loss, acceptable cycle time, maintenance, seasonal use and safety requirements. Compare against manual harvesting and available tools with fair trials. Do not claim “number one”, guaranteed savings or superiority without independent comparative evidence.

## Award application evidence pack
- Problem statement and target users.
- Reproducible software demo and clearly labelled recording.
- Dataset provenance and evaluation protocol.
- Results table with baselines, uncertainty and failure cases.
- Simulation safety report and risk register.
- Open-source/data licensing statement.
- Milestones, realistic budget, impact measures and partner letters only when obtained.

## Cost, safety and integrity
- Free/open-source and local-first; no paid APIs, cloud GPUs, subscriptions or billing-enabled services without explicit approval.
- Keep large datasets and model weights out of Git; publish manifests and lawful download instructions.
- Do not connect cutting actuators or represent simulation as physical testing.
- Never fabricate metrics, customers, awards, certification or field outcomes.
- This is a plan, not evidence that checklist items are complete. Update after each verified run with commit, command, environment, result and unresolved failures.
