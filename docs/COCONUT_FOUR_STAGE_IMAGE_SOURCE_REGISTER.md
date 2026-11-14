# PUI89 Coconut Four-Stage Image Source Register

**Created:** 14 November 2026  
**Status:** research and image-source candidates identified; no new image bytes imported; no new image is approved for training.  
**Purpose:** build a rights-traceable real-image collection for the project's four operational classes without confusing fruit colour, biological maturity, and variety.

## 1. PUI89 operational labels

The product currently uses these four classes:

| Class ID | PUI89 label | Operational description | Important limitation |
|---|---|---|---|
| C1 | `young_green` | Young/immature fruit, usually green | Green colour alone cannot prove young age. |
| C2 | `mature_green` | Developed fruit that remains predominantly green | Requires maturity evidence; do not infer from size or colour alone. |
| C3 | `yellow` | Fruit with clearly yellow/yellowing husk appearance | Yellow may be a cultivar trait (including tender-coconut varieties), not a universal maturity stage. |
| C4 | `brown` | Mature, dry or aging fruit with brown husk | Distinguish attached fruit from harvested/processed product when the task is canopy detection. |

These are **PUI89 operational image labels**, not a claim that all coconut cultivars pass through four visually separable colour stages. A qualified coconut/agronomy reviewer must confirm the label policy for the intended cultivar and harvest use. Record biological stage and visible husk colour as separate fields where known. Use `uncertain` or `ignore` for ambiguous fruit; never force a label.

## 2. Research basis

1. **CUSAT PhD thesis, Chapter 4, Figure 4.12, printed page 89 / PDF page around 90.** The thesis describes and illustrates young, tender, mature and dry/brown coconut images. It explains tender fruit by endosperm development and mature fruit by hardening/thickening of the meat and husk. This supports a four-development-stage reference, but its figure images are research references only: the thesis page does not establish an open image-reuse licence for PUI89. Do not extract or redistribute the figure without permission.
   - https://events.cusat.ac.in/xmlui/bitstream/handle/purl/5481/Dyuthi%20T-2523.pdf?sequence=1
2. **Paull & Ketsa, University of Hawai‘i at Mānoa / Kasetsart University, Coconut: Postharvest Quality-Maintenance Guidelines (2015).** Describes immature and mature market stages and typical development timing; use as agronomic context, not as a four-class visual labelling authority.
   - https://www.growables.org/information/TropicalFruit/documents/CoconutCTAHR.pdf
3. **Fruit Biology of Coconut (Cocos nucifera L.), Plants (2022).** Documents cultivar and developmental variation; supports separating colour phenotype from maturity interpretation.
   - https://pmc.ncbi.nlm.nih.gov/articles/PMC9738799/

## 3. Wikimedia Commons image-source candidates

The following are source-page candidates, not imported dataset records. The licence and attribution shown below were visible on the source pages when checked on 14 November 2026. Recheck the exact file revision and licence immediately before downloading or reuse. A source-page licence does not prove that a particular fruit has the required biological stage.

| Candidate | Source page / creator | Displayed licence | Possible use | Status |
|---|---|---|---|---|
| WMC-01 | [Coconut in Coconut Tree.jpg](https://commons.wikimedia.org/wiki/File:Coconut_in_Coconut_Tree.jpg) — Sarmi~Kili | CC BY-SA 4.0 | Attached green-looking fruit; canopy/occlusion and detection practice | Existing project candidate 0032; source metadata checked previously; original-byte hash and human labels still pending. |
| WMC-02 | [Mature Coconut Palm with Coconuts](https://commons.wikimedia.org/wiki/File:Mature_Coconut_Palm_with_Coconuts_%28Cocos_nucifera%29.jpg) — Johnnybam | CC BY-SA 4.0 | Mature palm with fully grown coconuts; inspect individual fruit colour and visibility | New source candidate; maturity labels and visual suitability not independently reviewed. |
| WMC-03 | [Coconut Yellow Gourigatram.jpg](https://commons.wikimedia.org/wiki/File:Coconut_Yellow_Gourigatram.jpg) — Giri1234 | Public domain as stated by uploader | Yellow-coloured cultivar / colour-variation reference | New source candidate; page describes a yellow variety mainly used as tender coconut. Do **not** label as biologically mature solely because it is yellow. |
| WMC-04 | [Coconut Yellow.JPG](https://commons.wikimedia.org/wiki/File:Coconut_Yellow.JPG) — Iaminfo | CC BY-SA 3.0; GFDL also offered | Yellow-husk appearance and cultivar variation | New source candidate; biological maturity and orchard-attached context are not established by metadata. |
| WMC-05 | [The fruit of coconut.jpg](https://commons.wikimedia.org/wiki/File:The_fruit_of_coconut.jpg) — Lotadegbemijowa | CC BY-SA 4.0 | Brown / ripened plucked fruit; close-up maturity appearance | New source candidate; plucked fruit is not a canopy-detection example. |

**Important:** these five records do not mean that all four PUI89 classes are already represented by validated, labelled, orchard-attached images. In particular, a strong young-green versus mature-green image set still needs expert-confirmed fruit examples, ideally with known cultivar, age/harvest context, and images of attached fruits.

## 4. Required source-record fields

For each image actually acquired, record at minimum:

- stable candidate ID and unchanged original filename;
- source page URL, direct original-file URL, creator and source-page review date;
- exact licence name, licence URL, attribution text and any share-alike obligations;
- original dimensions, byte size, file format, SHA-256 of local original bytes;
- cultivar, orchard/tree/session and capture context when known;
- attached-to-palm / harvested / close-up / market / other domain label;
- provisional maturity class, visible husk colour, reviewer and evidence/rationale;
- annotation version, independent QA outcome, inclusion/exclusion reason;
- split group (orchard/tree/session), never a random frame-only split.

Do not put image files into the public repository by default. Keep originals in the local data workspace and commit only non-sensitive metadata or documentation that is safe to publish. Preserve the source bytes unchanged for hashing.

## 5. Collection and approval workflow

1. Open the original Commons file page and recheck creator, exact licence, revision and attribution.
2. Download only after the operator approves the source and local collection action. Do not automatically treat search results as permitted or relevant.
3. Calculate and record the local original-file hash; do not re-encode before hashing.
4. Visually inspect at native resolution. Reject irrelevant, non-coconut, collage, market-only or unidentifiable images for the canopy task; retain out-of-domain images only in a separately identified auxiliary set.
5. Annotate each individually distinguishable fruit. Record detection visibility and maturity class separately; mark uncertain/occluded fruit as uncertain/ignore.
6. Require independent human label review and rights review before dataset promotion.
7. Group by orchard/tree/source/session before train/validation/test splitting. Keep a frozen, independent test set.
8. Run the existing fail-closed dataset promotion and leakage gates. Training remains blocked until every required gate passes.

## 6. Current status and next action

- Four-class taxonomy: documented as an operational proposal; qualified agronomy review still required.
- Research reference for four developmental stages: found (CUSAT thesis); reuse permission for thesis figures not established.
- Wikimedia source-page candidates: 5 recorded above; all need image-by-image suitability review, and the new candidates need to be added to the canonical ledgers only after actual review.
- New image downloads/imports in this change: **0**.
- New human-reviewed labels: **0**.
- New training-approved images: **0**.

**Next action:** review the candidate pages and acquire approved original files in a controlled local batch; then annotate and independently review examples for each class. Do not change existing approval flags or claim a four-class dataset is ready.
