# Coconut Split-Leakage Automation v1

## Purpose

The Coconut Evidence Gate Monitor now invokes the existing standard-library split-leakage auditor when the canonical split manifest is present.

Expected manifest path:

`data/coconut_dataset_split_manifest.csv`

Required columns:

`image_id,filename,split,group_id,sha256`

Allowed final split values are `train`, `validation`, and `test`. The auditor also accepts `challenge` and `unassigned` as review states, but any such row prevents a final passing split report.

## Fail-closed behaviour

- If the manifest is absent, the workflow reports `NOT_CONFIGURED`; it does not generate rows, assign splits, or create placeholder hashes.
- If present, the workflow checks required fields, duplicate IDs/filenames, declared SHA-256 formatting and cross-split exact-hash/group leakage.
- A failed audit is reported as `BLOCKED`; an execution error fails the workflow step.
- The scheduled monitor runs at 05:45 Asia/Bangkok after this workflow is merged to the default branch.
- Workflow permissions remain `contents: read`; checkout credentials are not persisted.

## Evidence limitations

The hosted audit does not download private images and does not independently verify image bytes. The existing auditor supports local `--verify-files --image-root` checks, which must be run in an approved local environment against the actual original files. Exact hashes do not detect resized or visually similar duplicates.

A passing split audit does not establish source rights, image representativeness, annotation correctness, maturity-label validity, detector performance, or safety. Rights review, native-resolution human annotation QA, independent review and explicit dataset approval remain separate mandatory gates. Training remains blocked until all required evidence gates pass.

## Current status

`NOT_CONFIGURED` until a genuine, curator-reviewed manifest is supplied. No synthetic manifest or split assignments are created by this automation.
