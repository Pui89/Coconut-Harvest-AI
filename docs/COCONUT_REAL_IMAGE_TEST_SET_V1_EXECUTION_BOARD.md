# Coconut Real-Image Test Set v1 — Execution Board

**Status:** implementation tracker; collection and validation are in progress only when evidence is recorded below.  
**Policy:** open-source-first, CPU-first, rights-first, human-reviewed, no fabricated labels or metrics.  
**Scope:** real RGB coconut imagery for the four PUI89 operational labels. This is a dataset/evaluation workstream within Coconut Harvest AI, not a new product.

## Current verified starting point

- Existing repository source register: 5 Wikimedia Commons source-page candidates are documented.
- Existing rights/review ledgers: 34 candidate records and 34 matching review records in the 29 October 2026 snapshot.
- Training-approved candidates in that snapshot: **0**.
- Candidate 0032: an eight-box draft exists; source-byte SHA-256 and independent visual annotation QA remain incomplete.
- Existing annotation, provenance, promotion-gate, split-audit, conversion, and evaluation tools are documented. Do not duplicate them.
- No new images have been downloaded or imported by this execution board. No new labels, model predictions, or evaluation scores are claimed.

See:
- [Four-stage image source register](COCONUT_FOUR_STAGE_IMAGE_SOURCE_REGISTER.md)
- [Dataset readiness and candidate 0032 procedure](COCONUT_DATASET_READINESS.md)
- [Real-image validation gates](COCONUT_REAL_IMAGE_VALIDATION_EXECUTION_GATES.md)
- [First real-image benchmark checklist](FIRST_REAL_IMAGE_BENCHMARK_CHECKLIST.md)
- [Annotation-to-benchmark workflow](ANNOTATION_TO_BENCHMARK_WORKFLOW.md)

## Execution queue

| ID | Work item | Required evidence to close | Current state |
|---|---|---|---|
| R1 | Recheck source page, creator, exact licence/revision and attribution for each candidate | Dated rights review in canonical rights ledger | Pending image-by-image review |
| R2 | Verify local original bytes and calculate SHA-256 for candidate 0032 | Successful documented dry-run/source check and recorded real digest | Blocked: original local image file required |
| R3 | Review candidate 0032 eight-box draft at full resolution | Saved reviewed annotation version plus independent second-person QA | Pending |
| R4 | Independently review the 15 existing first-pass boxes in images 0002 and 0004 | Full-resolution overlays and per-box QA decisions | Pending |
| R5 | Visually assess WMC-02 to WMC-05 and other candidates | Suitability decision, task-domain label, rights decision and ledger entry | Pending |
| R6 | Confirm four-class operational labelling policy with qualified coconut/agronomy reviewer | Written class definitions and ambiguity/ignore rules | Pending |
| R7 | Promote only rights-cleared, human-reviewed images | Promotion-gate report with all required approvals | Blocked: 0 currently approved in dated snapshot |
| R8 | Freeze independent train/validation/test groups | Versioned manifest, group separation and passing leakage audit | Not ready |
| R9 | Run an actual local CPU detector on the frozen held-out set | Model/checkpoint provenance, actual prediction file and reproducible command | Not run |
| R10 | Calculate and publish evaluation | Ground-truth QA, actual predictions, per-class metrics and failure analysis | Not run |

## Four-class annotation policy

Use the repository's operational class IDs:

- `young_green`
- `mature_green`
- `yellow`
- `brown`

Do not infer biological maturity from colour alone. Record visible husk colour separately from biological stage when known. Use `uncertain` / `ignore` for ambiguous, occluded, blurred or insufficiently visible fruit; never force a class. A qualified reviewer must confirm the policy for the intended cultivar and harvest task.

## Execution protocol

1. Start with candidate 0032. Obtain the original, unmodified local file from the operator; verify source identity and run the documented hash helper in dry-run mode first.
2. Review the eight-box draft against the full-resolution original. Correct or reject each box and record reasons. Keep the original draft unchanged.
3. Arrange independent second-person review. A geometry pass or AI-generated annotation is not human QA.
4. Review images 0002 and 0004 independently; then assess the remaining source candidates one by one.
5. Update the existing canonical ledgers only with observed facts. Do not create duplicate ledgers or mark a candidate approved because its source page has a licence.
6. Run the existing fail-closed promotion gate. If any required field or approval is missing, leave the image excluded.
7. Split by orchard/tree/source/capture session, not random near-duplicate frames. Freeze the test set before model selection or threshold tuning.
8. Run inference only with an approved compatible local checkpoint already available. Do not download weights, install packages, or use paid/cloud services without explicit approval.
9. Evaluate only real predictions against reviewed ground truth. Report precision, recall and F1 at declared IoU/score thresholds; add per-class TP/FP/FN and failure cases. Do not describe the single-threshold evaluator as COCO mAP.
10. Publish a dated evidence report that distinguishes **confirmed**, **pending**, **blocked**, and **not run**.

## Stop conditions

- Licence, creator, source revision or commercial/derivative-use rights unclear: exclude the image.
- Local source bytes do not match the reviewed source: stop and resolve provenance.
- Annotation or maturity class uncertain: mark ignore/uncertain and request review.
- No independent human QA: do not promote labels.
- No suitable approved local checkpoint: report inference as **NOT RUN**.
- No held-out predictions: report metrics as **NOT AVAILABLE**.
- Never commit original image files, private footage, model weights or other data unless redistribution rights and repository suitability are explicitly confirmed.

## Completion definition

Test Set v1 is complete only when its versioned manifest identifies every included original image, rights and provenance are verified, labels have independent human QA, source groups are separated across train/validation/test, the held-out test set is frozen, and a reproducible evaluation has been run using actual detector predictions. Until then, describe it as an **execution-in-progress dataset**, not a validated dataset or working coconut detector.
