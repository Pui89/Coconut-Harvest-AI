"""Create a read-only local image inventory with real SHA-256 hashes.

This tool never downloads images, changes source files, or edits the canonical manifest.
It writes a separate CSV report so a human can review it before promoting any values.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp"}
SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_ledger(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"candidate_id", "filename"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Ledger missing columns: {', '.join(sorted(missing))}")
        rows = []
        for row in reader:
            candidate_id = (row.get("candidate_id") or "").strip()
            filename = (row.get("filename") or "").strip()
            if candidate_id and filename:
                rows.append({"candidate_id": candidate_id, "filename": filename})
        return rows


def find_images(root: Path) -> dict[str, list[Path]]:
    found: dict[str, list[Path]] = {}
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        try:
            relative = path.relative_to(root)
        except ValueError:
            continue
        if any(part in SKIP_DIRS or part.startswith(".") for part in relative.parts[:-1]):
            continue
        found.setdefault(path.name, []).append(path)
    return found


def build_report(root: Path, ledger_path: Path) -> list[dict[str, str]]:
    ledger = read_ledger(ledger_path)
    image_paths = find_images(root)
    rows: list[dict[str, str]] = []
    expected_names = {item["filename"] for item in ledger}

    for item in ledger:
        matches = sorted(image_paths.get(item["filename"], []))
        status = "missing"
        relative_paths = ""
        size = ""
        digest = ""
        if len(matches) == 1:
            path = matches[0]
            status = "found_hashed"
            relative_paths = path.relative_to(root).as_posix()
            size = str(path.stat().st_size)
            digest = sha256_file(path)
            if not size or size == "0":
                status = "found_empty_file"
        elif len(matches) > 1:
            status = "ambiguous_duplicate_filename"
            relative_paths = ";".join(path.relative_to(root).as_posix() for path in matches)
        rows.append({
            "candidate_id": item["candidate_id"],
            "expected_filename": item["filename"],
            "status": status,
            "local_paths": relative_paths,
            "bytes": size,
            "sha256": digest,
            "note": "Hash is computed from local file bytes; this does not verify rights, labels, or training approval.",
        })

    for filename, matches in sorted(image_paths.items()):
        if filename in expected_names:
            continue
        for path in sorted(matches):
            rows.append({
                "candidate_id": "",
                "expected_filename": filename,
                "status": "local_image_not_in_ledger",
                "local_paths": path.relative_to(root).as_posix(),
                "bytes": str(path.stat().st_size),
                "sha256": sha256_file(path),
                "note": "Unexpected local image; review its identity and rights before adding it to a ledger.",
            })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Project folder to scan")
    parser.add_argument("--ledger", type=Path, required=True, help="CSV with candidate_id and filename columns")
    parser.add_argument("--output", type=Path, default=Path("coconut_local_image_inventory_report.csv"),
                        help="Separate report CSV path (default: current directory)")
    args = parser.parse_args()

    root = args.root.expanduser().resolve()
    ledger = args.ledger.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if not root.is_dir():
        parser.error(f"--root is not a directory: {root}")
    if not ledger.is_file():
        parser.error(f"--ledger is not a file: {ledger}")
    if output == ledger:
        parser.error("--output must not overwrite the input ledger")
    try:
        rows = build_report(root, ledger)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=["candidate_id", "expected_filename", "status", "local_paths", "bytes", "sha256", "note"],
            )
            writer.writeheader()
            writer.writerows(rows)
    except (OSError, UnicodeError, csv.Error, ValueError) as exc:
        parser.error(str(exc))

    found = sum(row["status"] == "found_hashed" for row in rows)
    missing = sum(row["status"] == "missing" for row in rows)
    ambiguous = sum(row["status"] == "ambiguous_duplicate_filename" for row in rows)
    unexpected = sum(row["status"] == "local_image_not_in_ledger" for row in rows)
    print(f"Report written: {output}")
    print(f"Expected files hashed: {found}; missing: {missing}; ambiguous: {ambiguous}; unexpected local images: {unexpected}")
    print("This report does not approve images for training or verify licences or annotations.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
