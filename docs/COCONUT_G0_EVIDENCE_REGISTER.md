# G0 Field Evidence Register — Coconut Harvest AI

**Status:** Blank operational template; no field evidence is recorded by this file.  
**Version:** 1.0  
**Created:** 24 November 2026  
**Applies to:** Thailand G0 market and workflow validation  
**Related document:** [Thailand G0 Field Survey](COCONUT_G0_THAILAND_FIELD_SURVEY.md)  
**Market requirements:** [Labour-Reduction Market & Engineering Requirements](COCONUT_LABOUR_REDUCTION_MARKET_REQUIREMENTS.md)

> **Important:** This register is a template, not evidence that a farm, processor, worker, harvesting workflow or customer has been interviewed. Never enter invented or inferred values as observations. Keep each site visit and each evidence item traceable.

## 1. Evidence handling rules

1. Assign a unique site ID and evidence ID. Do not use a person's name as an identifier.
2. Record the date, broad location, evidence owner/collector role, method and source type. Avoid collecting personal identifiers or sensitive worker details.
3. Obtain permission before interviews, photography, audio recording or copying business records. Record the consent status and permitted use.
4. Do not ask anyone to climb, cut, lower bunches or demonstrate hazardous work for this survey. Observe only from a safe location; never stand below harvesting activity.
5. Separate **Measured**, **Documented**, **Reported**, **Estimated** and **Unknown**. A reported number is not a measurement.
6. Record units, period, denominator, sample size and method for every quantitative value. Do not compare values with different definitions.
7. Preserve original evidence in an access-controlled location. This Markdown register should contain evidence IDs and safe summaries, not private personal data or confidential documents.
8. Redact personal data and commercially sensitive details before any public release. Do not upload private farm imagery or records to a public repository.
9. Correct errors by adding a dated correction note; do not silently overwrite the historical record.
10. A single farm or interview cannot support a country-wide market claim.

## 2. Controlled vocabularies

### Evidence status
- `MEASURED` — directly measured using a stated method and instrument.
- `DOCUMENTED` — transcribed from an existing record or document with permission.
- `REPORTED` — stated by an interviewee; not independently verified.
- `ESTIMATED` — calculated or approximated; method and assumptions required.
- `UNKNOWN` — not available or not established.
- `NOT_APPLICABLE` — field does not apply; explain why.

### Evidence type
- `SITE_OBSERVATION`
- `INTERVIEW_FARM_OPERATOR`
- `INTERVIEW_HARVEST_CONTRACTOR`
- `INTERVIEW_PROCESSOR`
- `BUSINESS_RECORD`
- `TIME_STUDY`
- `PHOTO_OR_VIDEO`
- `OTHER` (describe)

### Consent status
- `GRANTED_LIMITED` — permission granted for the specific recorded purpose only.
- `GRANTED_RESEARCH` — permission granted for stated research use.
- `DECLINED`
- `NOT_REQUIRED` — explain why (for example, public document); do not assume.
- `PENDING`

## 3. Site register

Create one row per farm, plantation, contractor operation or processing site. Use a neutral site code such as `TH-CF-001`; do not publish exact coordinates or private addresses.

| Field | Entry |
|---|---|
| Site ID | |
| Site category | Commercial farm / plantation / contractor / processor / cooperative / other |
| Province / broad area | |
| Visit date(s) | |
| Crop / product context | Mature coconut / mixed purpose / coconut milk / other |
| Approximate operation scale | Value + unit + source status |
| Palm/tree profile | Observed height range or UNKNOWN; do not guess height from an uncalibrated photo |
| Harvest frequency / seasonality | Value + period + source status |
| Main harvesting method | |
| Site contact role (not name) | |
| Consent status and permitted use | |
| Evidence IDs linked to this site | |
| Follow-up required | |
| Record owner / reviewer | |

## 4. Evidence-item register

Create one row for each interview note, time study, business record, safe observation, photo set or other source. Do not put personal names, phone numbers, exact home addresses or confidential raw data in this table.

| Evidence ID | Site ID | Date | Evidence type | Topic | Status | Unit / sample size / period | Consent / use limit | Secure source reference | Reviewer / QA |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

Suggested evidence IDs: `TH-CF-001-E001`, `TH-PR-001-E001`.

## 5. Operating baseline — one record per observed harvest session

Record actual workflow without requesting a hazardous demonstration. Where possible, use existing records or observe routine work from a safe distance.

| Field | Value | Unit / definition | Evidence status | Evidence ID | Notes / limitations |
|---|---:|---|---|---|---|
| Number of workers involved | | persons | | | |
| Active harvesting time | | worker-hours and elapsed minutes; keep separate | | | |
| Coconuts harvested | | count | | | |
| Bunches harvested | | count | | | |
| Trees serviced | | count | | | |
| Travel / setup time | | minutes | | | |
| Waiting / downtime | | minutes | | | |
| Fruit damaged or lost | | count and defined cause | | | |
| Harvest incomplete / missed | | count or documented method | | | |
| Safety events / near misses | | count and reporting method; do not solicit names | | | |
| Weather / ground / access conditions | | descriptive categories | | | |
| Harvest method / equipment | | description | | | |

**Definitions**
- **Worker-hours** = sum of time spent by all workers on the defined task. Example: 3 workers × 2 hours = 6 worker-hours. Do not confuse this with 2 elapsed hours.
- **Elapsed time** = clock time from the defined start to end of the task, excluding or including breaks as explicitly stated.
- **Harvested coconut count** must specify whether rejected, damaged or immature fruit is included.
- **Damage/loss rate** requires a defined denominator and inspection method. If no inspection was performed, record UNKNOWN.

## 6. Processor / buyer evidence

Use a separate record for each processor or buyer. Record requirements as stated by the organisation and distinguish them from independently tested agronomic facts.

| Field | Value | Evidence status | Evidence ID | Notes |
|---|---|---|---|---|
| Product / use | | | | |
| Preferred incoming coconut characteristics | | | | |
| Acceptance / rejection criteria | | | | |
| Supply volume and period | | | | |
| Seasonal variation | | | | |
| Current sourcing / collection model | | | | |
| Quality problems / losses | | | | |
| Traceability requirements | | | | |
| Interest in a service or product | | | | |
| Purchasing authority / process | | | | |
| Price / willingness-to-pay evidence | | | | |

## 7. KPI calculation sheet

Calculate only when numerator, denominator, period and method are available. Keep each site/session separate before considering aggregation.

| KPI | Formula | Required evidence |
|---|---|---|
| Labour input per 100 coconuts | Worker-hours ÷ coconuts harvested × 100 | Worker-hours and coconut count from same session |
| Labour input per tonne | Worker-hours ÷ harvested mass in tonnes | Worker-hours and measured/recorded mass |
| Labour cost per 100 coconuts | Harvest labour cost ÷ coconut count × 100 | Cost period, included costs and coconut count |
| Throughput per elapsed hour | Coconuts harvested ÷ elapsed task hours | Same task boundary and session |
| Throughput per worker-hour | Coconuts harvested ÷ worker-hours | Same task boundary and session |
| Damage/loss rate | Damaged or lost coconuts ÷ inspected/harvested coconuts × 100 | Defined damage criteria and denominator |
| Harvest completeness | Eligible bunches harvested ÷ eligible bunches identified × 100 | Defined eligibility, survey area and inspection method |
| Equipment utilisation | Active productive time ÷ available operating time × 100 | Defined availability and downtime log |
| Operating cost per coconut | Total defined operating cost ÷ coconuts handled | Include labour, energy, transport, maintenance and other stated cost items |
| Payback period | Initial investment ÷ net periodic benefit | Verified costs, benefits, utilisation and maintenance assumptions |

**Do not calculate labour reduction or ROI from an imagined machine baseline.** A future comparison requires a clearly matched manual baseline and a measured prototype/service trial under comparable conditions. Until then, record the KPI as NOT AVAILABLE.

## 8. Quality and review checklist

For every evidence item, check:

- [ ] Site ID and evidence ID are unique and linked.
- [ ] Date, method, source type and collector role are recorded.
- [ ] Consent and permitted use are clear.
- [ ] Quantitative values include units, denominator, period and sample size.
- [ ] Measured, documented, reported, estimated and unknown values are distinguished.
- [ ] Interview statements are attributed by role only, unless explicit permission requires otherwise.
- [ ] Photos/video have rights, consent, safe capture conditions and source provenance.
- [ ] No private personal data or restricted business information is exposed.
- [ ] Limitations, missing values and possible bias are recorded.
- [ ] A second reviewer has checked material calculations and interpretations.

## 9. G0 synthesis — do not mark passed until evidence supports it

Complete only after reviewing multiple relevant evidence items.

| G0 question | Finding | Evidence IDs | Confidence / limitations | Open action |
|---|---|---|---|---|
| Is there a clearly described customer problem? | | | | |
| Which customer segment experiences it? | | | | |
| What is the current manual workflow? | | | | |
| Is a baseline available with units and a defined method? | | | | |
| What are the real operating conditions and constraints? | | | | |
| What are the safety and regulatory questions? | | | | |
| What would a customer pay for: product, service or outcome? | | | | |
| What evidence is still missing? | | | | |

### G0 decision
- `NOT STARTED` — no field evidence collected.
- `IN PROGRESS` — evidence collection is underway; key questions remain.
- `READY FOR REVIEW` — minimum evidence package assembled; independent review pending.
- `PASSED WITH LIMITATIONS` — documented review supports proceeding to the next defined gate, with limitations recorded.
- `NOT PASSED` — evidence does not support proceeding; revise the problem, segment or scope.

**Current G0 status for this template:** NOT STARTED. This status must be changed only when real evidence is entered and reviewed. A completed blank template is not a passed gate.

## 10. Change log

| Date | Change | Author / reviewer |
|---|---|---|
| 2026-11-24 | Initial blank register template created | PUI89 |
