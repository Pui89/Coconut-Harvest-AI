# PUI89 Commercial Product & Company-Readiness Standard

**Portfolio rule:** mandatory for this and every future PUI89 project.  
**Goal:** enable lawful commercial use and establish an evidence-backed path from research to high-quality products, customers, partners, manufacturing and a future PUI89 company.

## Project-specific gates
Agricultural AI and proposed harvesting robot. Commercial gates: licensed orchard datasets, detector validation, worker exclusion, machinery risk assessment, guarded tools, reach/stability testing, field trials and serviceability.

## 1. Commercial rights and intellectual property
- The root `LICENSE` governs original materials the project owner is entitled to license. MIT and Apache-2.0 both permit commercial use, modification and redistribution subject to their conditions.
- Existing licences are preserved; this standard does not retroactively relicense earlier releases.
- Third-party code, models/weights, datasets, images, CAD, fonts and other assets are NOT automatically covered by the repository licence. Record source, version, owner, exact licence, attribution, restrictions and commercial-use permission before inclusion or sale.
- Exclude assets with unclear, research-only, non-commercial, no-redistribution or incompatible terms from commercial releases.
- PUI89 names, logos and trademarks are not granted by the software licence. Keep brand/trademark permissions separate.
- Maintain contributor permissions, copyright provenance, third-party notices and an SBOM for distributable software.

## 2. First-class product quality requirements
Every product must have a defined customer and intended use; measurable requirements and acceptance criteria; architecture and interface documentation; reproducible builds and tests; traceability and version history; secure defaults and vulnerability handling; privacy/data governance; installation, user, maintenance and troubleshooting documentation; support, incident, rollback and end-of-life plans.

## 3. Safety, security and regulatory requirements
- Complete hazard identification, risk assessment, safe-state design, human override and foreseeable-misuse analysis before field/customer use.
- For AI, document data provenance, label quality, leakage-safe splits, calibration, uncertainty, error rates, limitations, drift and human-review rules.
- For hardware, define and test mechanical, electrical, thermal, battery, fire, water/dust ingress, EMC/radio and environmental requirements as applicable. A design target is not a test result.
- Identify applicable laws, standards, certifications and approvals for each target market with qualified assessors. Do not claim certification, roadworthiness, life-safety protection, rescue effectiveness, accuracy or resistance without evidence.
- Simulation and software tests do not establish physical safety or field performance.

## 4. Commercial stage gates
| Gate | Evidence required | Status permitted |
|---|---|---|
| G0 Concept | Customer problem, intended use, exclusions, initial risks | Concept |
| G1 Requirements | Requirements, architecture, hazards, IP/data/licence review | Specified |
| G2 Prototype | Working software/prototype and reproducible tests | Prototype |
| G3 Verification | Test reports, benchmarks, security review, failure analysis | Verified within tested scope |
| G4 Validation | Representative user/environment trials and independent review where needed | Validated within tested scope |
| G5 Compliance | Required legal, safety, privacy and market approvals | Approved only with evidence |
| G6 Pilot | Qualified supply, support, warranty, manufacturing/service processes | Pilot |
| G7 Commercial release | Release sign-off, unit economics, quality controls, documentation and post-market support | Sale-ready only after all required gates |

## 5. Startup and company readiness
Maintain a product catalogue; IP and contributor register; third-party licence inventory; customer discovery and pilot records; bill-of-materials and unit-economics model; supplier/component qualification; manufacturing, repair, warranty and support plans; and clear separation of open-source code, future proprietary components, services and brand assets. Existing open-source grants cannot simply be withdrawn.

## 6. Strict PUI89 zero-cost rule
Prefer free/open-source and offline/local tools. No paid APIs, subscriptions, cloud GPUs, paid datasets, metered services, automatic paid upgrades or unexpected billing. Check licence, provenance, security, resource fit and cost before adding dependencies/models/data/services. Use only existing free allowances. If certification, lab testing, legal review or manufacturing requires funding, record it as a future funding/partner gate; do not incur charges without explicit approval.

## 7. Required evidence records
Create and maintain as the project matures: `docs/PRODUCT_REQUIREMENTS.md`, `docs/HAZARD_AND_RISK_REGISTER.md`, `docs/VERIFICATION_AND_VALIDATION_PLAN.md`, `docs/THIRD_PARTY_NOTICES.md`, and `docs/COMMERCIAL_READINESS.md`. Their mention here does not mean they already exist or have passed review.

## 8. Truthful claims
Use explicit evidence labels: **PROPOSED**, **IMPLEMENTED**, **TESTED**, **SIMULATION-ONLY**, **BENCH-TESTED**, **FIELD-TESTED**, **INDEPENDENTLY-VALIDATED**, **CERTIFIED/APPROVED**. Never market a concept as a finished product or claim a gate passed without traceable evidence.

**PUI89 standard:** high ambition, clear commercial rights, disciplined engineering, safety-first design, evidence before claims, and zero-cost development until funding is explicitly approved.
