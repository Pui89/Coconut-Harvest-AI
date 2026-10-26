#!/usr/bin/env python3
"""Create a free, fail-closed dataset recovery queue without silently approving labels."""
import csv, hashlib, json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(".")
MANIFESTS = [Path("data/manifest.csv"), Path("data/manifest.template.csv")]
OUT = Path("reports/dataset-recovery")
ALLOWED_SPLITS = {"train", "validation", "test"}
GOOD_LABELS = {"human_verified", "verified", "approved"}
GOOD_RIGHTS = {"approved", "verified", "clear"}

def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    issues, rows_seen, ready = [], 0, 0
    manifest = next((p for p in MANIFESTS if p.is_file() and p.name == "manifest.csv"), None)
    if manifest is None:
        manifest = next((p for p in MANIFESTS if p.is_file()), None)

    if manifest:
        with manifest.open(newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            required = {"image_path", "source_url", "license_status", "sha256", "label_status", "split"}
            missing = required - set(reader.fieldnames or [])
            if missing:
                issues.append({"type":"manifest_schema", "file":str(manifest), "reason":"Missing required columns: "+", ".join(sorted(missing)), "action":"Fix manifest schema; do not promote dataset."})
            else:
                for line, row in enumerate(reader, 2):
                    image = (row.get("image_path") or "").strip()
                    if not image:
                        continue
                    rows_seen += 1
                    reasons = []
                    rights = (row.get("license_status") or "").strip().lower()
                    label = (row.get("label_status") or "").strip().lower()
                    split = (row.get("split") or "").strip().lower()
                    if rights not in GOOD_RIGHTS:
                        reasons.append("source/licence not explicitly approved")
                    if label not in GOOD_LABELS:
                        reasons.append("label/annotation not human-verified")
                    if split not in ALLOWED_SPLITS:
                        reasons.append("split missing or invalid")
                    if not (row.get("source_url") or "").strip():
                        reasons.append("source URL missing")
                    p = (ROOT / image).resolve()
                    try:
                        p.relative_to(ROOT.resolve())
                    except ValueError:
                        reasons.append("image path escapes repository root")
                        p = None
                    if p is not None and not p.is_file():
                        reasons.append("image file missing")
                    elif p is not None and p.is_file():
                        actual = sha256(p)
                        expected = (row.get("sha256") or "").strip().lower()
                        if not expected or expected != actual:
                            reasons.append("SHA-256 missing or mismatched")
                    if reasons:
                        issues.append({"type":"quarantine_candidate", "manifest":str(manifest), "line":line, "image_path":image, "reasons":reasons, "action":"Exclude from training/scored testing; retain original and queue a replacement candidate. Verify source rights, annotate, independently review, then update manifest."})
                    else:
                        ready += 1
    else:
        issues.append({"type":"no_manifest", "reason":"No populated data/manifest.csv found; a template is not a dataset.", "action":"Collect source-cleared candidates and record each source and licence before annotation."})

    # Detect explicitly named non-training drafts and archived labels, without editing them.
    for p in ROOT.glob("data/**/*"):
        if p.is_file() and any(token in p.name.upper() for token in ("NOT_FOR_TRAINING", "ARCHIVE")):
            issues.append({"type":"protected_review_file", "file":p.as_posix(), "reason":"Draft/archive filename indicates it must not be treated as approved training data.", "action":"Keep for audit history; do not use for training. Replace only in the active dataset after a candidate passes review."})

    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    report = [
        "# Dataset Recovery Queue", "",
        "**Generated:** "+stamp, "",
        "This report is fail-closed: it identifies data that must be excluded from the active training/scored-test path. It does not delete original files, invent labels, approve licences, or promote replacements.", "",
        "## Summary", "",
        "- Manifest rows inspected: "+str(rows_seen),
        "- Rows passing basic manifest checks: "+str(ready),
        "- Review / quarantine findings: "+str(len(issues)), "",
        "## Findings", ""
    ]
    if issues:
        for i, issue in enumerate(issues, 1):
            report.append("### "+str(i)+". "+str(issue.get("type","review")))
            for key, value in issue.items():
                if key != "type":
                    report.append("- **"+key.replace("_"," ").title()+":** "+(json.dumps(value, ensure_ascii=False) if isinstance(value,(list,dict)) else str(value)))
            report.append("")
    else:
        report.append("No manifest blockers detected by these basic checks. Human annotation review and task-specific validation are still required.")
    report += [
        "## Replacement workflow", "",
        "1. Keep the original image/annotation and record the reason in this queue; do not erase audit history.",
        "2. Exclude the flagged sample from training and scored evaluation until corrected.",
        "3. Add a new candidate only with a verifiable source URL, licence, attribution and checksum.",
        "4. Have a human create/correct labels and an independent reviewer verify them; automated geometry checks are necessary but cannot confirm semantic correctness.",
        "5. Assign source/tree/scene/session group and split; check duplicates and leakage.",
        "6. Promote only through the existing project validation gate. Never replace a difficult but valid test example solely because model performance is poor.",
        "",
        "No paid APIs or cloud model inference are used by this audit."
    ]
    (OUT / "README.md").write_text("\n".join(report)+"\n", encoding="utf-8")
    with (OUT / "replacement_queue.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["type","manifest","line","image_path","reasons","action","file","reason"])
        writer.writeheader()
        for issue in issues:
            writer.writerow({k: json.dumps(v, ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in issue.items() if k in writer.fieldnames})
    print("Recovery report written to reports/dataset-recovery/README.md")
    print("Rows inspected:", rows_seen, "basic pass:", ready, "findings:", len(issues))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
