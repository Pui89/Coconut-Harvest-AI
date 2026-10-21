"""Download referenced coconut photos for manual review, with integrity checks.

This is a data-preparation helper, not an image detector. It uses only the Python
standard library. Network access is used only when the user runs --download.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "real_image_samples"
MANIFEST = OUT_DIR / "SOURCES.md"
CSV_PATH = OUT_DIR / "image_review.csv"
MAX_IMAGE_BYTES = 25 * 1024 * 1024
JPEG_SIGNATURE = bytes((0xFF, 0xD8, 0xFF))

SAMPLES = [
    {
        "filename": "fruiting_coconut_palm_canopy.jpg",
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Fruiting_Coconut_Palm_Canopy.jpg?width=1100",
        "source_page": "https://commons.wikimedia.org/wiki/File:Fruiting_Coconut_Palm_Canopy.jpg",
        "creator": "Paul The Writer",
        "license": "Verify current source page before reuse",
        "license_url": "https://commons.wikimedia.org/wiki/File:Fruiting_Coconut_Palm_Canopy.jpg",
        "purpose": "Coconut canopy visual review",
    },
    {
        "filename": "coconut_plucker_harvesting.jpg",
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Coconut_Plucker_plucking_coconuts_on_a_tree_in_Mumbai..JPG?width=1100",
        "source_page": "https://commons.wikimedia.org/wiki/File:Coconut_Plucker_plucking_coconuts_on_a_tree_in_Mumbai..JPG",
        "creator": "Rudolph A. Furtado",
        "license": "Verify current source page before reuse",
        "license_url": "https://commons.wikimedia.org/wiki/File:Coconut_Plucker_plucking_coconuts_on_a_tree_in_Mumbai..JPG",
        "purpose": "Human harvesting context; not a robot trial",
    },
]

FIELDS = [
    "image_file",
    "source_page",
    "license",
    "visible_coconut_count",
    "occluded_or_partly_hidden_count",
    "lighting_conditions",
    "background_clutter",
    "review_notes",
]


def validate_jpeg_payload(data: bytes, content_type: str = "", filename: str = "image.jpg") -> None:
    """Reject empty, oversized, or non-JPEG payloads before saving."""
    if not data:
        raise ValueError(f"{filename}: download was empty.")
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError(
            f"{filename}: file exceeds the {MAX_IMAGE_BYTES // (1024 * 1024)} MiB size limit."
        )
    if not data.startswith(JPEG_SIGNATURE):
        raise ValueError(
            f"{filename}: payload does not have a JPEG signature "
            f"(reported content type: {content_type or 'unknown'})."
        )


def download_one(sample: dict[str, str]) -> tuple[Path, int, str]:
    target = OUT_DIR / sample["filename"]
    partial = target.with_suffix(target.suffix + ".part")
    request = urllib.request.Request(
        sample["url"],
        headers={"User-Agent": "Coconut-Harvest-AI-local-research-demo/1.0"},
    )
    print(f"Downloading {sample['filename']} ...")
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            content_type = response.headers.get("Content-Type", "")
            data = response.read(MAX_IMAGE_BYTES + 1)
        validate_jpeg_payload(data, content_type, sample["filename"])
        checksum = hashlib.sha256(data).hexdigest()
        partial.write_bytes(data)
        partial.replace(target)
        return target, len(data), checksum
    finally:
        if partial.exists():
            partial.unlink()


def download_samples() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_lines = [
        "# Real coconut image sample sources",
        "",
        "Photographs are downloaded on demand; they are not included in the repository.",
        "The downloader rejects non-JPEG payloads and files over 25 MiB, and records SHA-256.",
        "Verify the current licence and attribution requirements on each original source page",
        "before redistribution or dataset inclusion. These references are not benchmark evidence.",
        "",
    ]
    downloaded: list[tuple[dict[str, str], Path, int, str]] = []
    for sample in SAMPLES:
        target, size, checksum = download_one(sample)
        downloaded.append((sample, target, size, checksum))
        manifest_lines.extend(
            [
                f"## {sample['filename']}",
                f"- Creator shown in repository reference: {sample['creator']}",
                f"- Source: {sample['source_page']}",
                f"- Licence status: {sample['license']}",
                f"- Licence/source review: {sample['license_url']}",
                f"- Intended use: {sample['purpose']}",
                f"- Download URL: {sample['url']}",
                f"- File size: {size} bytes",
                f"- SHA-256: {checksum}",
                "",
            ]
        )
        print(f"Saved validated JPEG: {target} ({size} bytes)")
    MANIFEST.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    with CSV_PATH.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for sample, _, _, _ in downloaded:
            writer.writerow(
                {
                    "image_file": sample["filename"],
                    "source_page": sample["source_page"],
                    "license": sample["license"],
                    "visible_coconut_count": "",
                    "occluded_or_partly_hidden_count": "",
                    "lighting_conditions": "",
                    "background_clutter": "",
                    "review_notes": "",
                }
            )
    print()
    print(f"Review template: {CSV_PATH}")
    print(f"Source notes:    {MANIFEST}")
    print("Next: open each image, fill the CSV manually, and keep observations separate")
    print("from model predictions. No AI detection or robot safety check was performed.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download the two referenced real photographs and create a CSV review template.",
    )
    args = parser.parse_args()
    if not args.download:
        parser.print_help()
        print("\nNo files were downloaded. Add --download when you are ready.")
        return 0
    try:
        download_samples()
    except Exception as exc:
        print(f"Download failed: {exc}", file=sys.stderr)
        print("No paid service is needed; you can open the source links in the guide instead.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
