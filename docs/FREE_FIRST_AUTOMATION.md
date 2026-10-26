# Free-first local automation

Use the repository's existing CI, agent tests, dataset-readiness gate, and security checks. This helper adds a simple local entry point; it does not replace those workflows.

## Run locally (Windows PowerShell)

From the repository root:

```powershell
python tools/free_first_check.py --syntax-only
python tools/free_first_check.py --report reports/free-first-check.json
```

The first command uses only Python's standard library. The second also runs the existing pytest suite and writes a JSON report; pytest must already be installed. The script never installs dependencies, downloads models, edits files, or calls paid services.

## Dataset and evidence boundary

A passing software check does not approve image-source rights, annotations, data splits, detector accuracy, or physical harvesting capability. Keep candidate data blocked until provenance, rights, labels, geometry, and independent review meet the repository's dataset gate. Report measurements only after a reproducible evaluation.

## Safe automation loop

1. Run checks and capture the report.
2. Inspect the first failing test or syntax error.
3. Make a small, reviewable change.
4. Re-run the same checks.
5. Keep the change unmerged until the review and CI results support it.

Automatic repair is intentionally limited: this helper diagnoses failures but does not rewrite code or approve dataset records.
