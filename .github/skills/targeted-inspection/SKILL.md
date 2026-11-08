---
name: targeted-inspection
description: Find and inspect only the repository files and line ranges needed for a task. Use when repository scope is broad or reading whole files would add noise.
---

# Targeted Repository Inspection

## Procedure
1. Identify the likely entry point from filenames, imports, tests, configuration, and documentation.
2. Search for the exact symbol, contract, route, test, or setting before opening files.
3. Read the smallest useful range around each match; expand only when dependencies or control flow require it.
4. Trace callers and tests only as far as needed to establish behavior.
5. Check for an existing implementation before adding a new helper, dependency, or duplicate document.
6. Record paths and line ranges so the same files do not need to be rediscovered.

## Efficient commands
- Prefer `rg -n "term" path/` for indexed text search when available.
- Prefer `sed -n 'START,ENDp' file` for bounded reading.
- Prefer focused test selection over the full suite during iteration.
- Avoid dumping entire directories, lockfiles, generated assets, or large logs into the prompt.

## Guardrails
- Search output is a locator, not proof of full behavior; inspect the relevant source.
- Do not skip security, safety, or license files when the task touches them.
- If search is unavailable, use the narrowest supported repository/file listing.
