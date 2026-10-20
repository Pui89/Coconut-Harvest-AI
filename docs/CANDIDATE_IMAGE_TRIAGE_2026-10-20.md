# Candidate image visual triage — 20 October 2026

## Purpose and limits

This is a first-pass **contact-sheet visual triage** of the 30-image candidate artifact from workflow run 39092214196. It is not an independent pixel-level annotation review, licence clearance, or approval for training. Full-resolution files and source pages must be checked before any image enters the dataset.

The artifact was downloaded and preserved locally on 20 October 2026. The artifact itself reports `CANDIDATES_ONLY_REVIEW_AND_ANNOTATION_REQUIRED`. The GitHub Actions artifact is scheduled to expire on 25 October 2026.

## Initial triage

| ID | Candidate title | Initial visual relevance | Provisional action |
|---|---|---|---|
| 0001 | Coconuts on Tree | Whole palm/tree view; individual fruit targets not clearly usable in contact sheet | Inspect full resolution; likely context only unless fruit are clearly visible |
| 0002 | Fresh coconuts | Fruit bunch is visible | **Priority for pixel-level box and maturity-label review**; existing boxes are first-pass only |
| 0003 | Owoce Orzech kokosowy | Collage/educational composite with several coconut-related images | Exclude from detector training unless original component images are obtained and separately cleared |
| 0004 | Cocos nucifera 003 | Several green fruits clearly visible | **Priority for pixel-level box and maturity-label review**; existing boxes are first-pass only |
| 0005 | Climbing Balinese Palm Tree | Person climbing palm; fruit targets not clearly visible at contact-sheet scale | Harvest-context only unless full-resolution target fruit are clearly annotatable |
| 0006 | Climbing coconut tree | Person/tree climbing scene; no clear individual target fruit | Context/negative candidate; not a positive fruit image based on current view |
| 0007 | Coconut harvest tool | Tool close-up, no coconut fruit target | Exclude from fruit detector positives; may be separate tool/safety data later |
| 0008 | Coconut harvest | Harvesting person/tree scene; individual fruit not clear | Context only unless full-resolution review identifies clear fruit |
| 0009 | Coconut harvesting Zanzibar | Harvesting scene; target fruit not clearly resolved in contact sheet | Context only pending full-resolution review |
| 0010 | DSC 8970 | Harvesting/palm scene; possible bunch but individual fruit need review | Full-resolution review required; do not label fruit from thumbnail |
| 0011 | Giay-dua / coconut processing | People processing coconut material, not a clear fruit-on-tree target | Exclude from fruit detector positives |
| 0012 | Goa coconut harvest | Distant palm/harvest scene; individual fruit not clear | Context only unless full-resolution review confirms usable fruit |
| 0013 | Grimpé - cocotier | Person climbing palm; no clear individual fruit targets | Context only pending full-resolution review |
| 0014 | Liberia, Africa - panoramio | Palm/climbing scene; fruit target not clear at contact-sheet scale | Full-resolution review required; likely context only |
| 0015 | Morros, Maranhão | Person using a long tool near a palm; fruit not clearly resolved | Context only pending full-resolution review |
| 0016 | Agricultural Research / Western Samoa | Landscape/palm scene; individual fruit not clear | Context/negative candidate, not a positive fruit label |
| 0017 | Bhattlem | Coconut grove/plantation view | Exclude from fruit positives unless fruit are visible and annotatable at full resolution |
| 0018 | Bobongan coconut plantation | Image appears to be a map/plantation-related graphic rather than fruit targets | Exclude from fruit detector positives |
| 0019 | Coconut Plantation | Wide plantation view; individual fruit not clear | Context/negative candidate only |
| 0020 | Coconut Plantation | Wide plantation view; individual fruit not clear | Context/negative candidate only |
| 0021 | Coconut Plantation in Kilifi County | Wide plantation/people scene; fruit not individually clear | Context only pending full-resolution review |
| 0022 | Coconut Plantation2 | Wide grove view; individual fruit not clear | Context/negative candidate only |
| 0023 | Coconut plant 3 | Small plant/seedling, not mature fruit on a palm | Exclude from harvest-fruit detector positives |
| 0024 | Coconut plant planted in red soil | Young plant/seedling, not a harvestable fruit target | Exclude from harvest-fruit detector positives |
| 0025 | Coconut trees 001 | Wide palm/landscape view; individual fruit not clear | Context/negative candidate only |
| 0026 | Cuba - Coconut grove | Historical/wide grove scene; individual fruit not clear | Context/negative candidate only |
| 0027 | NL-HaNA plantation with palms | Historical wide plantation scene; fruit targets not clear | Context/negative candidate only |
| 0028 | NL-HaNA plantation with palms | Historical wide plantation scene; fruit targets not clear | Context/negative candidate only |
| 0029 | Philippine Jockey Club Homestretch | Appears unrelated to coconut harvesting | **Reject as irrelevant** |
| 0030 | TM-10021456 | Wide plantation scene; individual fruit not clear | Context/negative candidate only |

## Priority decisions

1. Do not treat all 30 files as positive coconut-fruit training examples. Many appear to show trees, people harvesting, tools, plantations, seedlings, or unrelated content.
2. Start the next visual annotation review with 0002 and 0004, but independently inspect every box, missed fruit, false box, and class label at full resolution.
3. Review 0010 and other harvest-scene images at full resolution only to see whether individual fruit are clearly visible; do not assume a visible palm means visible fruit.
4. The current candidate batch does **not** establish coverage of all desired stages. The visible green fruits in 0002/0004 do not prove that young green, mature green, mature brown/dry, damaged, occluded, and uncertain classes are adequately represented.
5. Before training, verify each retained image's exact source page, creator, licence version, attribution/share-alike requirements, downloaded-file hash, and whether the particular file/version matches the recorded metadata.
6. Annotate individual fruits only when boundaries and class criteria are supported by the image. Use `uncertain_stage` when visual evidence cannot establish a stage; do not infer biological maturity from colour alone.
7. After review, split by source/tree/session where possible, audit leakage, and only then train a local baseline.

## Licence note

The accompanying `provenance.csv` records candidate licence names and creator/credit fields, but this report has **not** independently re-verified those source-page licence records. No candidate is declared legally cleared by this triage.

## Current conclusion

**Dataset status remains BLOCKED for training.** The candidate batch is useful for review, not yet an approved, independently annotated, all-stage dataset. Keep results and missing evidence explicit; do not claim a trained detector or physical harvesting performance.
