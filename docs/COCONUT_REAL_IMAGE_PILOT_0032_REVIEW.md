# Coconut real-image pilot — candidate 0032

**Review date:** 10 November 2026  
**Status:** source-page metadata checked; visual preview inspected; original-byte fingerprint and annotation QA remain pending.  
**Training gate:** BLOCKED.  
**Scope:** one-image annotation-process pilot only; not a detector training or accuracy benchmark.

## 1. Source and reuse record

- **Title / filename:** Coconut in Coconut Tree.jpg / 0032_Coconut_in_Coconut_Tree.jpg
- **Creator:** Sarmi~Kili
- **Source page:** https://commons.wikimedia.org/wiki/File:Coconut_in_Coconut_Tree.jpg
- **Original file:** https://upload.wikimedia.org/wikipedia/commons/b/be/Coconut_in_Coconut_Tree.jpg
- **Displayed licence:** Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
- **Licence:** https://creativecommons.org/licenses/by-sa/4.0/
- **Source-page metadata:** 5,184 × 3,456 pixels; 8,631,989 bytes; published SHA-1 34a77896b7ad78532cd41aadc2c3967220fd91ab.
- **Attribution:** “Sarmi~Kili, Coconut in Coconut Tree.jpg, Wikimedia Commons, CC BY-SA 4.0” with links to the source page and licence; state any changes if an adapted copy is distributed.

The source page was checked on 10 November 2026. Its displayed creator, licence, dimensions, byte size and SHA-1 match the existing candidate-0032 record in the project source-rights ledger and the fixed reference in tools/record_coconut_source_hash.py.

**Rights boundary:** CC BY-SA 4.0 allows reuse subject to attribution and share-alike conditions. Obtain an IP/licensing review before incorporating this image or adaptations into a proprietary/commercial dataset or distributing derivative annotations. This record is not legal advice or a blanket approval of the complete dataset.

## 2. Visual suitability — preliminary only

The Commons source preview (960 × 640) was inspected. It shows multiple attached, predominantly green-looking coconuts in a dense palm crown. Several fruits are partly obscured by fronds or neighbouring fruit; bright highlights and backlighting are present.

This is a useful **challenging cluster/occlusion annotation exercise**, but it is not a representative four-stage maturity image. The preview does not support reliable full-resolution box review, fruit-by-fruit maturity labelling, stem-keypoint placement, or tree-height measurement.

### Suitable tasks to attempt after obtaining the exact original locally

1. Individually box only clearly distinguishable visible fruit; do not draw boxes around a whole bunch.
2. Record fruit visibility as visible, partially_occluded, or uncertain.
3. Link fruit to a cluster only when the relationship is visually supported.
4. Add a stem-attachment keypoint only when the attachment is actually visible.
5. Record maturity as provisional and independently review it; do not equate green appearance with confirmed biological maturity.
6. Mark hidden fruit as unknown, not as missed ground truth.
7. Do not infer palm height or metric 3D position from this photograph.

## 3. Existing draft — preserve unchanged

Existing draft: data/review_batch_2026-10-22/ai_annotation_draft_NOT_FOR_TRAINING.json

It contains eight AI-assisted draft boxes. The repository already records human_qa_acknowledged = false, training_approved = false, an unverified source SHA-256, and coordinates/target coverage that are not ground truth.

Do not overwrite this draft. Export any corrected annotations to a new version and retain the original for audit history.

## 4. Required local verification sequence

The original image bytes are not stored in this repository by this pilot change. Before any hash is written:

1. Download the original file from the source page to a local, access-controlled working folder.
2. Preserve the original bytes and filename exactly; do not resize, crop, re-encode or annotate the source file.
3. Run the source-hash helper in read-only mode:

```powershell
python tools/record_coconut_source_hash.py --annotations data/review_batch_2026-10-22/ai_annotation_draft_NOT_FOR_TRAINING.json --image "C:\path\to\0032_Coconut_in_Coconut_Tree.jpg" --rights-csv data/review_batch_2026-10-18/source_rights_audit_2026-10-19.csv --output reports/candidate-0032-source-check.json
```

4. Continue only if all fixed-reference checks pass, including filename, dimensions, byte size and published SHA-1. The helper then reports the local SHA-256.
5. Only after a successful dry run, an explicit operator may rerun with --write-source-sha256. That option changes only the SHA-256 field in the draft JSON; it does not approve labels or training.
6. Inspect the original at native resolution in the offline annotator. Review all eight draft boxes, add missed clearly visible fruit, remove false boxes and record uncertain/occluded cases.
7. Save the corrected annotation as a new version, request an independent second-person visual review, update the existing review/rights ledgers only with observed outcomes, and rerun the existing dataset promotion gate.

If the local file does not match the published SHA-1 and byte size, stop. Do not bypass the check or silently update the fixed reference.

## 5. Pilot manifest

The companion data/real_image_samples/coconut_pilot_manifest.csv is a one-record execution manifest. It references the canonical source-rights ledger and existing draft rather than replacing them. Unknown values remain pending or unverified. It must be updated only from observed local checks and recorded human review.

## 6. Acceptance criteria

Candidate 0032 may be considered for a later reviewed pilot only when all are true:

- original bytes match the source-page fingerprint and local SHA-256 is recorded;
- licence/attribution obligations have been reviewed for the intended use;
- all visible fruit labels are checked at native resolution;
- ambiguous and occluded fruit are explicitly represented;
- maturity labels follow a written operational policy and receive independent review;
- corrected annotation version is immutable and linked to its reviewers;
- split assignment is by independent source/tree/session group, not random image splitting;
- existing fail-closed promotion and leakage audits pass.

Even then, one photograph is only a reviewed annotation example. It is not enough for model training, a four-class dataset, a held-out benchmark, or a safe-harvesting claim.

## 7. Current outcome

**Source page:** checked.  
**Preview:** inspected; promising for green-looking cluster/occlusion tasks.  
**Original local file hash:** NOT VERIFIED.  
**Eight draft boxes:** NOT HUMAN-QA-VERIFIED.  
**Four-stage maturity labels:** NOT ESTABLISHED.  
**Tree height / 3D location:** NOT MEASURED.  
**Training / benchmark:** BLOCKED.
