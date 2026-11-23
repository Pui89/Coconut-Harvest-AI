# Labour-Reduction Market & Engineering Requirements

**Document status:** Proposed product requirements and market-validation plan  
**Last reviewed:** 23 November 2026  
**Product:** Coconut Harvest AI  
**Scope:** Software-first intelligence and future operator-supervised harvesting-system research

## 1. Product objective

Develop an AI-assisted coconut-harvesting system that can help commercial farms and coconut-processing supply chains reduce dependence on manual harvesting labour, improve worker safety, and increase predictable harvesting productivity.

The product must address measurable operating problems. It must not assume that every target market has a shortage of workers, uses migrant labour, or uses monkeys for harvesting. Labour availability, labour cost, harvesting practices, regulations and farm conditions must be validated separately in each market.

**Primary value proposition:** support safer, more productive coconut harvesting with lower labour input per harvested coconut or tonne, subject to field evidence and economic validation.

The objective is not necessarily to eliminate workers. Human supervision, inspection, maintenance and safe operation remain part of the system.

## 2. Target customers and users

1. Commercial coconut plantation owners and farm operators.
2. Coconut collection and harvesting service providers.
3. Coconut milk, coconut cream and other coconut-processing factories that depend on reliable mature-coconut supply.
4. Agricultural cooperatives and machinery-service businesses.
5. Agricultural engineering and research organisations evaluating mechanisation.

The initial industrial use case prioritises mature coconuts intended for coconut meat and coconut milk processing. Variety-specific maturity and harvest-suitability criteria must be validated with agronomists, processors and local standards; visible colour class alone must not be treated as a definitive biological maturity measurement.

## 3. Geographic market priorities

| Market | Priority | Questions to validate before market claims |
|---|---|---|
| Thailand | Initial reference market | Regional labour cost and availability; current climbing and harvesting practices; farm size and terrain; processor quality and supply requirements; willingness to pay and service model. |
| India | International validation market | State-level differences in labour availability and cost; existing climbing aids and machines; tree and plantation variation; local service and distribution partners. |
| Indonesia | International validation market | Island and regional differences; plantation scale and access; labour practices; maintenance and transport constraints; processor demand. |
| Philippines | Secondary market screening | Manual harvesting workflow; labour economics; farm structure; local equipment and safety requirements. |
| Malaysia | Secondary market screening | Commercial plantation practices; labour and mechanisation economics; operating conditions and local compliance. |

These are research priorities, not a verified ranking of market size, labour shortage, customer demand or willingness to purchase. Do not publish unsupported market-size estimates or claims that a country has a universal labour shortage.

## 4. Market discovery method

Conduct structured interviews and field observations with farm owners, harvest workers, contractors, agricultural machinery dealers and coconut processors in each target region.

Record, where available:

- Harvesting method and who performs each task.
- Number of workers per harvesting team and hours per shift.
- Labour cost per worker-hour, tree, bunch, coconut and tonne.
- Worker availability, seasonality and time required to arrange a team.
- Tree height, trunk diameter, inclination, crown geometry and spacing.
- Terrain, soil, access roads, drainage and weather constraints.
- Harvest frequency, bunches per tree, coconuts per bunch and product maturity requirements.
- Current equipment purchase/rental cost, service availability, repair time and consumables.
- Safety incidents and near misses, using lawful and privacy-respecting records.
- Fruit/bunch damage, missed bunches, collection losses and downtime.
- Customer's acceptable operating cost, payback period and service arrangement.

Separate observed facts, interview statements, estimates and assumptions. Record source, date, location, sample size and permission for each research record.

## 5. Engineering requirements

### 5.1 AI perception and decision support — current software-first scope

- Detect and identify whole coconut trees and visible crowns where image evidence supports it.
- Detect or segment visible bunches and individual coconuts when the data supports the task.
- Preserve the four visual classes: Young Green, Mature Green, Yellow and Brown.
- Keep visual appearance separate from biological maturity and harvest suitability.
- Assess image quality, occlusion, viewpoint and uncertainty; send ambiguous cases to human review.
- Maintain tree, bunch and fruit identifiers so that observations from multiple views can be associated without double counting.
- Record image provenance, licence/permission, capture context, annotation version, reviewer and dataset split.
- Evaluate across the agreed tree-height strata H1–H6 (0–30 m) as dataset/evaluation groups only. These groups do not define machine reach or validated detection range.
- Estimate physical height or reachability only from calibrated and validated geometry/depth measurements; do not infer reliable metric height from an uncalibrated RGB image.
- Do not allow AI classification alone to trigger a physical cut.

### 5.2 Future harvesting mechanism — research scope, not an implemented capability

- Select the harvesting method only after field workflow and operating-envelope studies.
- Prefer simple, robust, maintainable mechanisms over unnecessary mechanical complexity.
- Compare ground-operated tools, assisted access, pole/remote cutting, supported bunch capture and other feasible concepts against the same safety and productivity requirements.
- Investigate the proposed single-cut-at-bunch-attachment concept, but treat it as an unvalidated design hypothesis.
- Support and control the bunch and its fall path before any cutting operation.
- Require operator supervision, guarded tooling, emergency stop, hazard analysis, safe-state behaviour and a documented recovery procedure before physical trials.
- Define tree and terrain operating limits explicitly. Do not imply that an AI system can safely climb or reach every tree from 0–30 m.

### 5.3 Industrial operation

- Prefer local-first operation and avoid mandatory continuous cloud connectivity.
- Design for inspection, cleaning, calibration, replaceable wear parts and repair using locally available service capability where feasible.
- Record machine downtime, maintenance time, consumables, energy use and operator workload during future trials.
- Define compatibility with plantation access, collection workflow and processor receiving requirements.
- No hardware purchase, fabrication, installation or field cutting is authorised by this requirements document.

## 6. Performance and business KPIs

Establish a manual-harvesting baseline before setting numerical product targets. Compare the assisted system and baseline under equivalent tree, terrain, crop and weather conditions.

| KPI | Measurement |
|---|---|
| Labour input | Worker-hours per tree, per 100 coconuts and per tonne harvested |
| Harvest productivity | Trees/hour, bunches/hour, coconuts/hour and kg or tonnes/hour |
| Labour reduction | Percentage change in worker-hours for equivalent harvested output |
| Harvest completeness | Eligible bunches harvested / eligible bunches identified |
| Fruit and bunch damage | Damaged fruit or bunches / total harvested |
| Missed or dropped fruit | Count and mass lost per harvest session |
| Setup and relocation | Minutes per tree and between trees |
| Availability and downtime | Operating time, unplanned stops and repair time |
| Safety | Hazard exposure, near misses and incidents per operating hour; no claim of safety from absence of reported incidents alone |
| Operating cost | Cost per tree, per coconut and per tonne |
| Economic value | Payback period and total cost of ownership under transparent utilisation assumptions |
| AI quality | Per-class precision, recall, F1, confusion counts, sample sizes and failure cases |
| Edge resources | Measured latency, peak RAM, energy and thermal behaviour on the target device |

Do not set or advertise numerical targets until customer baseline data and engineering trials justify them. Report uncertainty, sample sizes and test conditions.

## 7. Development gates

| Gate | Required evidence | Exit condition |
|---|---|---|
| G0 — Market baseline | Customer interviews, field workflow, cost and safety baseline | Initial target customer and problem statement supported by documented evidence |
| G1 — Data readiness | Rights-cleared real images, provenance, human labels and QA | Dataset approved for the stated evaluation purpose |
| G2 — AI baseline | Reproducible CPU-first evaluation and leakage-safe splits | Metrics, failure cases, runtime and RAM reported with dataset/version details |
| G3 — Harvest concept selection | Field measurements, hazard analysis and concept comparison | A mechanically plausible concept selected with documented trade-offs; no fabrication implied |
| G4 — Controlled prototype | Approved design, risk controls, supervised test plan and instrumentation | Bench tests pass before any controlled field trial |
| G5 — Field validation | Representative sites, comparable manual baseline, safety and productivity records | Evidence supports defined operating envelope and economic case |
| G6 — Industrial readiness | Service plan, manufacturing controls, documentation, compliance and lifecycle cost | Release decision based on complete evidence; no automatic progression |

A gate cannot be passed by concept art, simulation alone, unverified supplier claims or AI metrics that do not represent harvesting performance.

## 8. Competitive and alternative-method comparison

Compare the proposed system against the actual alternatives available at each site, which may include manual climbing, trained climbers, climbing aids, pole tools, mechanised access platforms and other locally used harvesting methods.

Use the same comparison dimensions:

- Labour input and skill dependency.
- Safety hazards and exposure.
- Productivity and harvest completeness.
- Damage and loss.
- Tree-height and terrain operating envelope.
- Setup, relocation, maintenance and downtime.
- Purchase/rental cost and total cost per tonne.
- Local serviceability and regulatory acceptance.

Do not describe a climbing aid as an autonomous harvesting robot. Do not treat monkey harvesting as a universal practice or the primary market problem. It is one local practice to document only where relevant and lawful.

## 9. Immediate implementation sequence

1. Keep the existing software-first scope and real-image evidence gates intact.
2. Prepare a field-survey sheet and collect a manual-harvesting baseline in Thailand before choosing a mechanical architecture.
3. Prioritise mature-coconut workflows for coconut milk processors while validating local maturity criteria.
4. Continue whole-tree, crown, bunch and fruit-level image evidence collection; include complete-tree views and record height only when measured or calibrated.
5. Interview prospective commercial customers and machinery-service providers to validate labour economics and acceptable operating cost.
6. Compare simple harvesting concepts only after the field workflow, operating envelope and safety hazards are documented.
7. Reassess India and Indonesia using the same survey instrument before making country-level demand claims.

## 10. Claims and evidence control

Permitted wording before validation: **proposed**, **planned**, **research target**, **candidate concept**, **to be measured**.

Do not claim that the product currently reduces labour, improves safety, increases throughput, works at 30 m, harvests autonomously, or is commercially ready. Such claims require representative, reproducible field evidence.

**Current status:** This document establishes product requirements and a market-validation plan. It does not establish customer demand, market size, a validated harvesting mechanism, a built machine or field performance.
