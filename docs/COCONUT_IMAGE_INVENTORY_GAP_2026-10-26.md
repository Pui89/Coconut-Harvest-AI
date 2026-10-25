# Coconut image inventory gap — 26 October 2026

## Finding

A read-only inspection of the repository's current ledgers found:

- Image SHA-256 manifest: **30 rows**, covering candidate IDs `0001`–`0030`.
- Source-rights ledger: **34 candidate records**.
- Candidate-review ledger: **34 candidate records**.
- Candidate IDs present in both ledgers but absent from the manifest: **0031, 0032, 0033, 0034**.
- Training-approved candidates in the existing readiness snapshot: **0**.

This is an inventory-coverage discrepancy. It does **not** establish that the four source images are missing from a user's computer, nor does it prove that any recorded digest matches an image file.

## Safe resolution

1. Locate each original candidate image locally and confirm the exact filename.
2. Compute SHA-256 from the actual file bytes; record the actual byte size. Do not copy a digest from another image or invent one.
3. Check that each filename and candidate ID match both ledgers.
4. Run the repository's [manifest coverage audit](../tools/audit_coconut_manifest_coverage.py) and inspect its JSON output.
5. Keep each candidate blocked from training until source/licence checks and annotation QA are independently completed.

## No-cost audit command

Run from the repository root in a Python environment:

```powershell
python tools/audit_coconut_manifest_coverage.py --manifest data/review_batch_2026-10-18/image_sha256_manifest_2026-10-20.csv --rights-csv data/review_batch_2026-10-18/source_rights_audit_2026-10-19.csv --review-csv data/review_batch_2026-10-18/candidate_review_2026-10-18.csv --output coconut-inventory-coverage.json
```

The audit checks CSV coverage and digest formatting only. It does not read or hash the image files, validate licensing, judge bounding boxes, approve training, or measure detector accuracy.
