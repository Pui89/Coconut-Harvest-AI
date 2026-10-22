# Coconut Dataset Structural Audit

Run from the repository root after downloading candidate images:

```bat
python tools\\fetch_coconut_candidates.py --download
python tools\\audit_coconut_dataset.py
```

Optional: validate annotation JSON files stored as `<candidate_id>.json`:

```bat
python tools\\audit_coconut_dataset.py --annotations-dir data\\annotations
```

The report is written to `data\\candidate_images\\dataset_audit_report.json`. The audit checks manifest shape, local-file presence, SHA-256 integrity, safe filenames, annotation structure, finite normalized box geometry, and whether the manifest attempts to mark candidates as training-approved. It does not modify the manifest or promote images.

**A passing report is not approval for training.** It does not inspect image pixels, verify coconut labels, determine whether the exact licence is suitable for a use, or substitute for independent human QA. Keep the training-approved count at zero until the documented review process is completed.
