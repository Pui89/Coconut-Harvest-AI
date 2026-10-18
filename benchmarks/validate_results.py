#!/usr/bin/env python3
"""Validate JSONL benchmark records; this does not run or certify a model."""
from __future__ import annotations
import argparse, json, math, sys
from pathlib import Path

REQUIRED = {"scenario", "metric", "value", "unit", "split", "seed", "source", "notes"}

def validate_record(record: object, line_number: int) -> list[str]:
    if not isinstance(record, dict):
        return [f"line {line_number}: record must be a JSON object"]
    errors = []
    missing = sorted(REQUIRED - record.keys())
    if missing:
        errors.append(f"line {line_number}: missing fields: {', '.join(missing)}")
    if "value" in record and (isinstance(record["value"], bool) or not isinstance(record["value"], (int, float)) or not math.isfinite(record["value"])):
        errors.append(f"line {line_number}: value must be a finite number")
    for field in REQUIRED - {"value", "seed"}:
        if field in record and (not isinstance(record[field], str) or not record[field].strip()):
            errors.append(f"line {line_number}: {field} must be a non-empty string")
    if "seed" in record and (isinstance(record["seed"], bool) or not isinstance(record["seed"], int)):
        errors.append(f"line {line_number}: seed must be an integer")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", help="JSONL file containing one benchmark record per line")
    parser.add_argument("--self-test", action="store_true", help="validate an in-memory example record")
    args = parser.parse_args()
    if args.self_test:
        example = {"scenario":"validator-self-test","metric":"example_score","value":0.5,"unit":"fraction","split":"synthetic","seed":0,"source":"synthetic","notes":"Validator test only; not a performance claim."}
        errors = validate_record(example, 1)
        if errors:
            print("\n".join(errors), file=sys.stderr); return 1
        print("Benchmark validator self-test passed (no model performance measured).")
        return 0
    if not args.file:
        parser.error("provide a JSONL file or use --self-test")
    path = Path(args.file)
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        print(f"cannot read {path}: {exc}", file=sys.stderr); return 2
    errors, records = [], 0
    for line_number, line in enumerate(lines, 1):
        if not line.strip() or line.lstrip().startswith("#"): continue
        records += 1
        try: record = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f"line {line_number}: invalid JSON: {exc.msg}"); continue
        errors.extend(validate_record(record, line_number))
    if records == 0: errors.append("no benchmark records found")
    if errors:
        print("\n".join(errors), file=sys.stderr); return 1
    print(f"Validated {records} benchmark record(s) in {path}. Validation is not model evaluation.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
