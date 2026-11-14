# Coconut Image Human-Review Checklist

**Status:** Review protocol proposal. This document does not approve any image, grant a licence, create labels, or authorize model training.

## 1. Review one image at a time

Record the following before an image can be considered for the PUI89 dataset.

| Check | Required evidence | Pass condition |
|---|---|---|
| Source identity | Original source-page URL, file title, creator/uploader, retrieval date | Source page is identifiable and matches the candidate file |
| Rights and licence | Licence name/version or public-domain basis, licence URL, required attribution, modification/share-alike conditions | Terms are checked for this exact file and permit the intended use |
| File integrity | Original filename, file format, dimensions, byte size, SHA-256 after authorised acquisition | File is readable and hash is recorded; no unexplained mismatch |
| Image quality | Reviewer notes on focus, exposure, resolution, compression and obstruction | Fruit details are sufficiently visible for the intended task |
| Subject relevance | Fruit count, visible fruit regions, attached/plucked status, canopy/background context | Image actually represents the intended detection or classification task |
| Label evidence | Visible cues, uncertainty, cultivar/context if known, independent agronomy review | Label is supported by evidence beyond husk colour alone |
| Privacy/safety | People, faces, vehicle plates, sensitive location details or other restricted content | No unresolved privacy or safety concern |
| Review traceability | Reviewer ID/name, date, decision, rationale, second-review status | Decision and rationale are recorded and auditable |

## 2. PUI89 operational labels

Use these four project labels only after qualified human review:

- `young_green`
- `mature_green`
- `yellow`
- `brown`

**Important:** These are PUI89 operational classes, not a claim that husk colour alone establishes biological maturity. Yellow cultivars and colour variation can mislead. Record cultivar, harvest/use context and biological maturity as separate metadata when known. If evidence is insufficient, do not force a class.

## 3. Decision values

Each candidate receives exactly one current review status:

- `pending_rights` — exact-file licence/attribution not yet verified.
- `pending_acquisition` — rights appear suitable, but the file has not been lawfully acquired and hashed.
- `pending_quality_review` — file acquired; image quality and task suitability not yet assessed.
- `pending_agronomy_review` — visual review completed; class evidence needs qualified agronomy review.
- `approved_for_annotation` — rights and image suitability checks passed; human annotation may begin.
- `approved_for_dataset` — required annotation and independent review completed; eligible for the specified dataset split/use.
- `rejected` — unsuitable, rights unclear/incompatible, duplicate, corrupt, or otherwise excluded.

A source-page candidate is never automatically `approved_for_annotation` or `approved_for_dataset`.

## 4. Annotation and disagreement rules

1. Keep the original image unchanged; store annotations separately.
2. Record bounding boxes/masks only when the visible fruit boundaries support them.
3. Record occlusion, blur, partial visibility, overlapping fruit and uncertain boundaries.
4. Ask two reviewers to label maturity independently where practical.
5. Escalate disagreement to a qualified coconut agronomist; preserve both initial labels and the adjudication record.
6. Use `uncertain` / `needs_expert_review` rather than guessing. Do not silently convert uncertainty into one of the four classes.
7. Keep tree-attached fruit and harvested/plucked fruit contexts distinguishable.

## 5. Minimum record fields

Recommended CSV/JSONL fields:

`candidate_id, source_url, source_title, creator, licence, licence_url, attribution_text, retrieval_date, original_filename, sha256, width, height, file_format, rights_status, quality_status, task_context, attached_or_plucked, cultivar, operational_label, biological_maturity, label_evidence, uncertainty_notes, reviewer_1, reviewer_1_date, reviewer_2, reviewer_2_date, adjudicator, decision, decision_reason, dataset_split, approved_use`

Do not populate unknown values by inference. Use an explicit empty/null value and explain what evidence is missing.

## 6. Dataset admission gates

An image may enter the dataset only when all applicable gates pass:

- Exact-file rights and attribution verified.
- Lawful acquisition completed and integrity hash recorded.
- Image quality and task relevance accepted.
- Privacy/safety review passed.
- Annotation completed with uncertainty recorded.
- Agronomy review completed for maturity labels.
- Independent review/adjudication recorded.
- Intended use and dataset split explicitly approved.

No training, evaluation or accuracy claim may use a candidate that has not passed the applicable gates. Keep source candidates, acquired files, annotated files and dataset-approved files as separate states.

## 7. Current pilot boundary

The five Wikimedia Commons entries in the four-stage source register remain **source-page candidates only** until each exact file completes this checklist. This protocol does not download files. Do not run collection scripts or acquire image bytes without explicit approval.

## 8. Reviewer sign-off template

```text
Candidate ID:
Exact source URL:
Exact-file licence verified: yes / no / pending
Attribution captured: yes / no / pending
File hash recorded: yes / no / not acquired
Image quality: pass / fail / uncertain
Task context: tree-attached / harvested / other / uncertain
Proposed operational label: young_green / mature_green / yellow / brown / uncertain
Evidence for label:
Cultivar/context known:
Agronomy review: pass / fail / pending / not required
Privacy/safety: pass / fail / pending
Final status:
Reviewer and date:
Second reviewer/adjudicator and date:
Decision rationale:
```

---
*Evidence rule: record only what was observed or verified. A licence shown on a source page, a visually plausible colour, or a candidate listing is not by itself proof of dataset approval or biological maturity.*
