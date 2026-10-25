# Coconut Image Inventory Coverage Audit

The legacy SHA-256 inventory currently records the first 30 candidate files. The source-rights and candidate-review ledgers also contain later candidates, so coverage must be audited before assuming every candidate has a recorded digest.

## Run locally

From the repository root, using the checked-out files and no additional packages:

```powershell
python tools/audit_coconut_manifest_coverage.py --manifest data/review_batch_2026-10-18/image_sha256_manifest_2026-10-20.csv --rights-csv data/review_batch_2026-10-18/source_rights_audit_2026-10-19.csv --review-csv data/review_batch_2026-10-18/candidate_review_2026-10-18.csv --output coconut-inventory-coverage.json
```

The tool reports candidate IDs missing from the inventory, duplicate IDs, filename mismatches, invalid byte counts, and malformed digest strings. Exit code 0 means only that the inventory rows cover the candidate IDs represented in both ledgers and their recorded metadata is structurally consistent.

## Important limits

- The audit does **not** open or hash image files. A 64-character SHA-256 string may still be wrong.
- After coverage is repaired, verify actual file bytes with `tools/verify_image_manifest_hashes.py` using its separate split-manifest format.
- Do not invent hashes for candidates 0031–0034. Compute them from the actual local files and record the true byte counts.
- This is inventory-integrity tooling, not licence verification, annotation QA, training approval, detector accuracy, or robot-performance evidence.
