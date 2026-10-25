# Dataset review-ledger validator

Free, standard-library-only validator for a **candidate-review ledger**. It checks the ledger's structure and internal consistency; it does not verify source licences, prove image ownership, assess whether labels are correct, or approve data for training by itself.

## Run locally

From the repository root:

```bash
python tools/validate_review_ledger.py data/review_ledger.template.csv
python -m unittest discover -s tests -p test_validate_review_ledger.py -v
```

Copy `data/review_ledger.template.csv` to a new local CSV before adding real review records. The example row contains a placeholder URL and placeholder review identity/date; replace them with truthful source and review details before using it as a real ledger. Do not overwrite historical review records or place restricted images in Git.

Required columns: `candidate_id, filename, group_id, decision, reason_code, reviewer, reviewed_on, source_url, rights_status, annotation_status, split`.

- Candidate IDs and filenames must be unique (filename comparison is case-insensitive).
- Every record needs a `group_id` that identifies its shared tree, original source, or capture session. Use a stable identifier, not a different ID for every image.
- Common untouched template markers are rejected: example filenames, the `tree_or_source_session` placeholder, `reviewer_initials`, and reserved `example.org` / `example.com` / `example.net` source URLs. Source URLs must be absolute HTTP(S) URLs. Replace these with truthful values before treating a ledger as reviewed evidence.
- The validator rejects an assigned group that appears across different `train`, `validation`, `test`, or `challenge` splits. Keep all images from the same tree/source/session in one split to reduce leakage risk. Unassigned candidates are not yet part of an evaluation split.
- Each record requires a reviewer, a non-empty source URL, and a real review date written exactly as `YYYY-MM-DD`.
- Decision and status values must use the documented controlled vocabularies in the script.
- Rejected, quarantined, or deferred candidates require a reason code.
- `approved` is accepted by this validator only when rights are marked `cleared`, annotation status is `reviewed`, and a split is assigned. These fields are assertions recorded by the reviewer, **not independent proof** that the checks occurred.
- A non-empty source URL is a provenance field only: the tool does not fetch URLs or verify licence claims.
- The group check depends on honest, consistent group IDs. It does not detect visually similar images, independently verify source grouping, inspect image bytes, inspect boxes, or establish that annotations are correct.

The validator is a data-quality preflight, not a model benchmark. Only use images for training after independent rights, annotation, image-integrity, and group-split review.
