# Coconut dataset promotion gate

The promotion gate joins the source-rights ledger and candidate-review ledger. It is deliberately fail-closed: **recording a licence is not the same as independent permission review, and valid box geometry is not the same as correct annotation.** It also rejects duplicate candidate IDs and case-insensitive duplicate filenames within either ledger, because ambiguous file identity can undermine record matching.

## Run locally (Python standard library only)

From the repository root:

```powershell
python tools/coconut_dataset_promotion_gate.py --rights-csv data/review_batch_2026-10-18/source_rights_audit_2026-10-19.csv --review-csv data/review_batch_2026-10-18/candidate_review_2026-10-18.csv --output reports/coconut-dataset-promotion-gate.json
```

Exit code 0 means every row in the supplied rights ledger is eligible. Exit code 1 means the dataset is blocked or a ledger has structural errors. The JSON report names each candidate's failed gates.

## Requirements for an eligible candidate

- Source page, creator/credit, displayed licence and licence URL are recorded.
- Source page is independently checked; attribution is recorded.
- Annotation QA is explicitly `passed` in the rights ledger and `qa_passed` in the review ledger.
- Training promotion is explicitly `approved` in the rights ledger and the review decision is `approved`.
- The same candidate ID and filename appear in both ledgers.
- The candidate is explicitly marked as a positive target candidate.

The required `qa_passed` status should only be recorded after a second human reviewer checks the image overlay and resolves missing, loose, duplicate or incorrect boxes. Archived labels must never be relabelled as passed without new independent review.

## Scope and limitations

This gate checks recorded metadata only. It does not independently establish legal rights, inspect image pixels, validate box correctness, compute hashes, detect near-duplicates, audit group-aware splits, or evaluate an AI model. Run the image/annotation and split audits separately before training. Do not add public photos or model weights to Git unless redistribution rights are confirmed.

## Current dataset status

The gate is expected to block the current batch: most candidates are excluded or unreviewed, and the historical labels for candidates 0002 and 0004 are explicitly archived/not for training. This is the correct result until the evidence changes.
