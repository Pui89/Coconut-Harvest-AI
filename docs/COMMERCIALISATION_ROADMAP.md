# Commercialisation Roadmap — Coconut Harvest AI

**Purpose:** identify a credible, low-cost path from the current software prototype to a product that farmers or agricultural partners could evaluate.

**Current stage:** early prototype and research project. This document is a plan, not evidence of paying customers, validated performance, field deployment, or commercial readiness.

## 1. Start with a small problem customers can verify

Do not begin by selling a fully autonomous harvesting robot. First investigate a lower-risk product:

**Coconut Orchard Survey & Harvest-Planning Assistant**
- A user imports permitted orchard photos or captures images with a phone/camera.
- The application helps mark and count visible coconut bunches, records image/source information, and lets a person correct the results.
- A simple report records location or tree ID when supplied by the user, review status, and follow-up inspection needs.
- The tool states uncertainty and never treats a model prediction as a confirmed harvest instruction.

This software-first service can be tested before building an arm, cutter, climbing mechanism, or autonomous mobile robot. It may be commercially useful only if it saves measurable time or improves planning compared with the farmer's current method.

## 2. Potential first customers (not confirmed)

1. Coconut growers and farm managers with a recurring inspection/planning problem.
2. Grower cooperatives and agricultural extension teams that coordinate multiple farms.
3. Agricultural universities and research institutes that need a reproducible inspection workflow.
4. Equipment integrators interested in evaluating perception software.

Interview these groups before choosing a final feature set. Do not assume willingness to pay from interest in AI alone.

## 3. Questions to ask during customer discovery

Ask at least 8–12 people across growers, cooperatives, and agricultural researchers:
- How do you currently inspect trees and record bunches or harvest readiness?
- How many trees and inspections are involved, and how often?
- Which errors are costly: missed bunches, repeat visits, labour time, access difficulty, or poor records?
- Who performs the task and how much time does it take per tree or plot?
- What evidence would make a photo-based report trustworthy?
- Would a human-reviewed tool fit the existing workflow? What would prevent adoption?
- What budget or procurement process applies to a small trial?
- What data can be shared with written permission, and what must remain private?

Record answers without personal or farm-sensitive details unless permission and storage rules are agreed. Do not describe interviews as customer validation until they have occurred.

## 4. Minimum viable product (MVP)

### Phase A — evidence-first software
- Local-first photo import and image/source manifest.
- Human correction of proposed detections; visible `unreviewed`, `reviewed`, and `uncertain` states.
- Exportable CSV/JSON summary with sample counts and known limitations.
- Repeatable benchmark on a permissioned, human-reviewed dataset.
- Clear installation steps, sample workflow, and no paid service by default.

### Phase B — orchard-specific pilot
- Agree on one partner's task and acceptance criteria in writing.
- Compare the tool with the current manual workflow on the same plots or image sessions.
- Measure detection precision/recall, missed bunches, correction time, end-to-end time, and failures.
- Keep a human responsible for all harvest decisions.
- Publish only approved, privacy-safe aggregate results.

### Phase C — robot feasibility
Only after perception and customer value are evidenced: define robot geometry, reachability, target pose and tool constraints; test in simulation; conduct a formal hazard assessment; then consider supervised hardware trials with emergency stops, exclusion zones and qualified oversight. No software prediction should directly trigger a cutter or actuator.

## 5. Commercial proof gates

| Gate | Evidence required | Decision |
|---|---|---|
| Problem fit | Repeated interviews identify the same costly workflow problem | Refine or stop the idea |
| Data readiness | Documented image permissions, reviewed labels, source-separated test split | Proceed to baseline |
| AI performance | Reproducible held-out metrics, false-positive/false-negative review, runtime and failure examples | Improve or restrict intended use |
| Workflow value | Measured comparison against the current method with partner-defined criteria | Consider a limited pilot |
| Safety | Risk assessment, independent controls and supervised test plan | Consider robotics feasibility only |
| Commercial fit | Written pilot scope, cost model, support expectations and an identified budget owner | Consider a paid pilot |

The current two-image HSV baseline has precision 0 and recall 0 at IoU ≥ 0.50. Do not claim the AI is commercially accurate until a new, reviewed benchmark has actually run.

## 6. Business model options to test (not prices or commitments)

- **Research/feasibility service:** a fixed-scope, human-reviewed orchard image audit and report.
- **Local software pilot:** installation and workflow evaluation for one cooperative or research group.
- **Later licensing/support:** only after the software is useful, maintainable, and supported by evidence.
- **Hardware/integration partnership:** later-stage option; do not finance robot hardware before demand and feasibility are demonstrated.

Do not set a price until customer discovery establishes the task, time saved, support burden, and buyer's budget. Keep the initial plan at USD 0 additional spend unless the project owner explicitly approves a cost.

## 7. What to measure in the first pilot

- Number of trees, images, visible bunches, and reviewed annotations.
- Precision, recall, false positives and missed bunches on a frozen test set.
- Human correction time and total task time versus the existing method.
- Performance by lighting, occlusion, distance and viewpoint.
- Software installation failures, latency on named hardware, and operator-reported usability.
- Any safety-relevant error or unsupported prediction.

Report sample sizes and uncertainty. Do not turn a small pilot into a claim of universal performance or guaranteed savings.

## 8. Immediate next actions

1. Complete the rights-cleared image review and first reproducible detector benchmark.
2. Prepare a one-page interview guide and contact potential grower/research collaborators.
3. Ask for workflow feedback, not endorsement or a purchase commitment.
4. Use results to narrow the MVP and agree on measurable acceptance criteria.
5. Keep the robot a staged research track until the software and customer value are demonstrated.

**Positioning:** “Coconut Harvest AI is an early-stage, local-first tool for evaluating coconut-orchard image inspection and harvest planning. It is being developed with human review and reproducible evaluation; autonomous physical harvesting has not been validated.”
