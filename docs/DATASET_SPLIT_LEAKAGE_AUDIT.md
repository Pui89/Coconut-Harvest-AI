# Coconut Dataset Split-Leakage Audit

Use this standard-library-only audit before publishing a train/validation/test benchmark. It checks whether the CSV manifest records exact file hashes or source groups that cross split boundaries, plus duplicate image IDs/filenames and malformed rows.

## Manifest columns

Create a CSV with these columns:

    image_id,filename,split,group_id,sha256
    orchard_a_001,orchard_a_001.jpg,train,orchard_a_session_01,<64-character SHA-256>
    orchard_b_001,orchard_b_001.jpg,test,orchard_b_session_03,<64-character SHA-256>

Replace example values with real records. Do not copy the example hash placeholder into a real manifest. Compute hashes from the actual files (for example, on Windows PowerShell with Get-FileHash -Algorithm SHA256 -LiteralPath <path>).

Use stable group IDs for the highest-level source that must not cross splits: often orchard/session, video sequence, or original image before crops/augmentation. A split must be one of train, validation, or test for a ready report. The audit accepts challenge/unassigned labels for review, but will not pass them as a final split manifest.

## Run

    python tools/audit_dataset_split_leakage.py path/to/manifest.csv --output split-audit.json

Exit code 0 means the manifest passed these structural and declared-leakage checks; exit code 1 means it did not pass. Malformed/missing input produces a command-line error. Inspect the JSON findings and correct the source manifest rather than suppressing findings.

## Limits

- Exact SHA-256 matches catch byte-identical files only. Resized/recompressed duplicates need perceptual similarity review.
- The script trusts the recorded group IDs and hashes; it does not inspect image bytes, annotations, licences, or detector output.
- A pass does not establish that the dataset is representative or labels are correct, and does not validate model performance or robot safety.
