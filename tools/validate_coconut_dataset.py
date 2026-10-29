"""Dependency-free Coconut Harvest dataset preflight; this does not measure model accuracy.

Manifest CSV required columns: image_id,path,source,license,split.
Optional leakage-group columns: source_id,tree_id,session_id.
Annotation CSV required columns: image_id,xmin,ymin,xmax,ymax,class.
Image paths are checked only when --root is supplied. SHA-256 is checked when
manifest has sha256 and the corresponding file exists.
"""
from __future__ import annotations
import argparse, csv, hashlib, json
from collections import defaultdict
from pathlib import Path

MANIFEST_REQUIRED = {"image_id", "path", "source", "license", "split"}
ANNOTATION_REQUIRED = {"image_id", "xmin", "ymin", "xmax", "ymax", "class"}
SPLITS = {"train", "validation", "val", "test"}

def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"{path}: missing CSV header")
        return list(reader), set(reader.fieldnames)

def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

def validate_dataset(manifest_path: Path, annotations_path: Path | None = None,
                     root: Path | None = None) -> dict:
    errors, warnings = [], []
    rows, fields = read_csv(manifest_path)
    missing = MANIFEST_REQUIRED - fields
    if missing:
        return {"status":"BLOCKED", "errors":["Manifest missing required columns: " + ", ".join(sorted(missing))],
                "warnings":[], "manifest_rows":len(rows), "annotation_rows":None, "accuracy_metrics":None}
    seen, groups = set(), defaultdict(set)
    hashes_checked = 0
    for line, row in enumerate(rows, start=2):
        image_id = (row.get("image_id") or "").strip()
        if not image_id: errors.append(f"Manifest row {line}: image_id is blank")
        elif image_id in seen: errors.append(f"Manifest row {line}: duplicate image_id {image_id!r}")
        seen.add(image_id)
        for field in ("path", "source", "license", "split"):
            if not (row.get(field) or "").strip(): errors.append(f"Manifest row {line}: {field} is blank")
        split = (row.get("split") or "").strip().lower()
        if split not in SPLITS: errors.append(f"Manifest row {line}: unsupported split {split!r}")
        for field in ("source_id", "tree_id", "session_id"):
            value = (row.get(field) or "").strip()
            if value: groups[f"{field}:{value}"].add(split)
        rel = (row.get("path") or "").strip()
        if root is not None and rel:
            image_path = root / rel
            if not image_path.is_file():
                errors.append(f"Manifest row {line}: image file not found: {rel}")
            elif (row.get("sha256") or "").strip():
                if sha256_file(image_path).lower() != row["sha256"].strip().lower():
                    errors.append(f"Manifest row {line}: SHA-256 mismatch for {rel}")
                hashes_checked += 1
    for group, splits in groups.items():
        if len(splits) > 1: errors.append(f"Potential split leakage: {group} appears in {sorted(splits)}")
    annotation_count = None
    if annotations_path is not None:
        ann_rows, ann_fields = read_csv(annotations_path)
        annotation_count = len(ann_rows)
        missing_ann = ANNOTATION_REQUIRED - ann_fields
        if missing_ann:
            errors.append("Annotations missing required columns: " + ", ".join(sorted(missing_ann)))
        else:
            for line, row in enumerate(ann_rows, start=2):
                if (row.get("image_id") or "").strip() not in seen:
                    errors.append(f"Annotation row {line}: image_id not in manifest")
                try:
                    coords = [float(row[k]) for k in ("xmin","ymin","xmax","ymax")]
                    if not all(map(lambda x: x == x and abs(x) != float("inf"), coords)): raise ValueError()
                    xmin,ymin,xmax,ymax = coords
                    if xmin < 0 or ymin < 0 or xmax <= xmin or ymax <= ymin:
                        errors.append(f"Annotation row {line}: invalid box coordinates")
                except (TypeError, ValueError, KeyError):
                    errors.append(f"Annotation row {line}: coordinates must be finite numbers with positive box area")
    if not rows: warnings.append("Manifest has no image rows")
    if not any((r.get("split") or "").strip().lower()=="test" for r in rows):
        warnings.append("No test split declared; held-out evaluation is not ready")
    if root is None: warnings.append("Image existence and hashes were not checked because --root was not supplied")
    return {"status":"PASS_PREFLIGHT" if not errors else "FAIL", "manifest_rows":len(rows),
            "annotation_rows":annotation_count, "hashes_checked":hashes_checked, "errors":errors,
            "warnings":warnings, "accuracy_metrics":None,
            "note":"Dataset preflight only; no detector was run and no accuracy was measured."}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--annotations", type=Path)
    parser.add_argument("--root", type=Path, help="Root directory for manifest-relative image paths")
    parser.add_argument("--output", type=Path, help="Optional JSON report path")
    args = parser.parse_args()
    try: report = validate_dataset(args.manifest, args.annotations, args.root)
    except (OSError, ValueError) as exc:
        report = {"status":"BLOCKED","errors":[str(exc)],"warnings":[],"accuracy_metrics":None,
                  "note":"Dataset preflight only; no detector was run and no accuracy was measured."}
    encoded = json.dumps(report, indent=2, sort_keys=True)
    print(encoded)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded + "\n", encoding="utf-8")
    return 0 if report["status"] == "PASS_PREFLIGHT" else 1

if __name__ == "__main__":
    raise SystemExit(main())
