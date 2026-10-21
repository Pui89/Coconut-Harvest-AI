# Dataset review-ledger validator

Free, standard-library-only validator for a **candidate-review ledger**. It checks the ledger's structure and internal consistency; it does not verify source licences, prove image ownership, assess whether labels are correct, or approve data for training by itself.

## Run locally

From the repository root:

```bash
python tools/validate_review_ledger.py data/review_ledger.template.csv
python -m unittest tests/test_validate_review_ledger.py -v
```

Copy `data/review_ledger.template.csv` to a new local CSV before adding real review records. Do not overwrite historical review records or place restricted images in Git.

Required columns: `candidate_id, filename, decision, reason_code, reviewer, reviewed_on, source_url, rights_status, annotation_status, split`.

- Candidate IDs and filenames must be unique (filename comparison is case-insensitive).
- Decision and status values must use the documented controlled vocabularies in the script.
- Rejected, quarantined, or deferred candidates require a reason code.
- `approved` is accepted by this validator only when rights are marked `cleared`, annotation status is `reviewed`, and a split is assigned. These fields are assertions recorded by the reviewer, **not independent proof** that the checks occurred.
- The tool does not inspect image bytes, calculate duplicates, verify URLs/licences, inspect boxes, or establish leakage-safe group splits.

The validator is a data-quality preflight, not a model benchmark. Only use images for training after independent rights, annotation, integrity, and group-split review.
