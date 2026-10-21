# Dataset readiness report (fail-closed)

This free, standard-library tool summarizes the recorded rights and annotation audit. It is intended to stop the team from confusing a filled-in spreadsheet with a training-ready dataset.

## Run

```bash
python tools/summarize_dataset_readiness.py data/review_batch_2026-10-18/source_rights_audit_2026-10-19.csv
python -m pytest tests/test_summarize_dataset_readiness.py -q
```

The JSON report lists each candidate, whether all recorded gates pass, and the gates that remain incomplete. The strict promotion gates require a source page, creator credit, displayed licence and licence URL, an independently recorded page check, recorded attribution, annotation QA status `passed`, and promotion status `approved`. Blank, pending, excluded, or blocked values do not pass.

## Important limitations

This tool checks recorded CSV values only. It does **not** independently verify a licence, source-page contents, attribution obligations, image authenticity, label correctness, duplicate/leakage-free group splits, or robot performance. Do not change a candidate to `approved` merely to make the report green; the human review and evidence must happen first. An empty audit is not ready for training.
