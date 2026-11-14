# Coconut Harvest AI — BOM & Cost Register v1.0

**Status:** Preliminary research register — G0 requirements are partially defined; G1 evidence collection is in progress. This is not a supplier quotation, purchase list, verified build cost, or authorisation to buy.

**Estimate scope:** One controlled vision-bench research prototype for capturing the four coconut maturity classes (young green, mature green, yellow and brown). Harvesting mechanics, gripper, reach mechanism, orchard vehicle and field deployment are excluded from this first BOM.

**Reporting currency:** THB. Keep original supplier currency and record the dated exchange-rate source when a price is eventually entered.

## 1. Cost boundary

The existing README contains a preliminary planning allowance of **฿13,500–59,000** for a research prototype. Treat it only as an inherited planning range, not as a verified subtotal or current market quote. This register does not validate or recalculate that range.

The separate shared engineering-bench allowance (previously stated as approximately ฿16,500–46,000) is portfolio infrastructure. Do not add it in full to this product BOM. Allocate a shared asset once and document its allocation basis if a project-specific share is needed.

## 2. Product BOM — controlled vision bench

| Item ID | Subsystem / item | Qty per prototype | Function / acceptance need | Manufacturer / exact model | Country of manufacture evidence | Supplier / source | Unit price / currency / date | Cost status | Confidence / next action |
|---|---|---:|---|---|---|---|---|---|---|
| COC-VIS-001 | Industrial RGB camera | 1 | Repeatable image capture; interface and resolution to be selected against working distance and target detail | TBD | UNVERIFIED | TBD | TBD | UNKNOWN / NOT VERIFIED | UNVERIFIED — define field of view, resolution, frame rate, interface and environmental needs |
| COC-VIS-002 | Compatible lens | 1 | Match camera mount, sensor format, field of view and working distance | TBD | UNVERIFIED | TBD | TBD | UNKNOWN / NOT VERIFIED | UNVERIFIED — calculate focal length and focus range after camera geometry is fixed |
| COC-VIS-003 | Diffuse LED lights | 2 | Controlled, repeatable illumination; minimise glare and colour shifts | TBD | UNVERIFIED | TBD | TBD | UNKNOWN / NOT VERIFIED | UNVERIFIED — define colour temperature, CRI, dimming and mounting |
| COC-VIS-004 | Adjustable camera / light stand | 1 set | Stable, repeatable camera distance, angle and height | TBD | UNVERIFIED | TBD | TBD | UNKNOWN / NOT VERIFIED | UNVERIFIED — determine adjustment range and load capacity |
| COC-VIS-005 | Colour / geometric calibration chart | 1 | Repeatable colour and geometric checks; use only with documented suitability | TBD | UNVERIFIED | TBD | TBD | UNKNOWN / NOT VERIFIED | UNVERIFIED — identify chart type, target and licence/usage conditions |
| COC-VIS-006 | Mounts, cables and fixtures | 1 set | Secure camera/light mounting and reliable data/power connections | TBD | UNVERIFIED | TBD | TBD | UNKNOWN / NOT VERIFIED | UNVERIFIED — derive connector, length, voltage and mechanical requirements |
| COC-VIS-007 | Compute | 1 shared / existing preferred | Image capture, annotation and CPU-first evaluation | Existing computer preferred; exact host TBD | N/A until host identified | Existing asset | Incremental cost TBD | UNKNOWN / NOT VERIFIED | UNVERIFIED — inventory available computer before considering new hardware |
| COC-VIS-008 | Storage / backup media | 1 as required | Preserve original images, labels, manifests and audit records | TBD | UNVERIFIED | TBD | TBD | UNKNOWN / NOT VERIFIED | UNVERIFIED — estimate dataset size and retention before selecting capacity |
| COC-VIS-009 | Power / protection accessories | 1 set as required | Safe, compatible power distribution and cable protection | TBD | UNVERIFIED | TBD | TBD | UNKNOWN / NOT VERIFIED | UNVERIFIED — derive from selected camera and lighting specifications |

**Quantity note:** quantities are initial planning quantities only. Confirm after interface and mechanical design review. Do not infer that any item has been sourced, purchased, received or tested.

## 3. Shared equipment — tracked separately

| Shared asset | Current treatment | Allocation rule |
|---|---|---|
| Development computer | Reuse existing computer first; exact model and available capacity not yet recorded here | Record as an existing asset; do not charge full purchase price to Coconut if shared |
| RGB-D camera | Optional shared engineering-bench candidate; not required for the initial RGB-only vision bench unless a documented experiment needs depth | Track in portfolio shared-asset register; allocate once |
| Bench power supply / multimeter | Shared test equipment candidate | Allocate only the project-specific usage or depreciation basis if needed |
| Microcontroller boards | Not required for the initial RGB-only vision bench | Exclude until a defined integration requirement exists |
| Reusable tools, wiring and adapters | Shared workshop assets | Do not duplicate full cost across products |

## 4. Required evidence for every priced line

Before changing a line from UNKNOWN / NOT VERIFIED, record:

- Exact manufacturer, brand, model and part number.
- Product specification URL and supplier identity.
- Country of manufacture evidence; do not substitute brand headquarters, seller location or ship-from country.
- Price, currency, quantity, source URL, access date, quote date and validity.
- Stock status, minimum order quantity and lead time.
- Shipping origin, Incoterms if quoted, freight, insurance, duty, VAT, brokerage and local delivery assumptions.
- Compatibility review: dimensions, mass, power, interface, software support, environment and mounting.
- Licence and usage terms for software, firmware, datasets or calibration assets where applicable.
- Reviewer, review date, confidence and next verification action.

Use only suppliers and products whose origin and provenance can be checked. If origin is unclear, keep the item UNVERIFIED and do not treat it as an acceptable sourced candidate.

## 5. Cost summary — not yet established

| Metric | Current value |
|---|---|
| Estimate revision | v1.0 |
| Estimate date | 2026-11-14 |
| Currency | THB; original currency required for future quotes |
| Configuration | One controlled RGB vision-bench research prototype |
| Known, evidence-backed BOM subtotal | NOT ESTABLISHED |
| Unpriced required items | 9 initial line items; exact scope to be confirmed |
| One-time NRE | NOT ESTABLISHED |
| Fabrication / assembly | NOT ESTABLISHED |
| Prototype total | NOT ESTABLISHED |
| Production unit cost | NOT APPLICABLE at this stage |
| Lifecycle / operating cost | NOT ESTABLISHED |
| Market comparison | NOT ESTABLISHED |
| Confidence / gate | Preliminary; G0 partially defined, G1 pending evidence |

Do not calculate a project total by treating UNKNOWN as zero. When evidence is available, publish the known subtotal, unpriced-item count, excluded costs, assumptions and confidence separately.

## 6. Cost-reduction sequence

1. Reuse an existing computer and existing compatible equipment before buying hardware.
2. Validate the camera field of view and lighting geometry on paper before selecting exact models.
3. Prefer modular, replaceable mounts and standard interfaces.
4. Compare non-Chinese-origin candidates only when manufacturer and manufacturing-origin evidence is available.
5. Compare at least two technically equivalent supplier options where possible, using landed cost rather than headline price.
6. Do not reduce cost by weakening image quality, electrical safety, calibration, data provenance or validation requirements.

## 7. Approval gates

- **G0 — Requirements:** capture geometry, image-quality needs, interfaces and scope defined.
- **G1 — Research estimate:** exact candidates and dated indicative prices documented; unknowns remain visible.
- **G2 — Supplier quote:** written quote and landed-cost inputs verified.
- **G3 — Purchase approval:** explicit user approval for the exact items, quantities and budget.
- **G4 — Receipt:** invoices, shipping/import charges, received quantities and substitutions reconciled.
- **G5 — Verified build cost:** as-built BOM, integration, rework and test costs recorded.

No gate is passed by documentation alone. This register authorises no purchase, subscription, installation or supplier commitment.

## 8. Next engineering actions

1. Confirm the existing computer and available camera / lighting equipment before considering purchases.
2. Specify the target capture distance, field of view, image resolution and lighting arrangement.
3. Research exact non-Chinese-origin camera, lens and lighting candidates with traceable origin evidence.
4. Record dated supplier prices and calculate Thai landed cost only from documented terms.
5. Update the README planning snapshot only after the evidence-backed estimate is reviewed.

**Evidence boundary:** No component in this register is represented as purchased, installed, prototype-tested or validated. No verified total cost, market-price advantage or savings claim is established.
