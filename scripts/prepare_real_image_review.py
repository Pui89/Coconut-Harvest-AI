"""Download openly licensed coconut photos and create a manual review template.

This is a data-preparation helper, not an image detector. It uses only the Python
standard library. Network access is used only when the user runs --download.
"""
from __future__ import annotations

import argparse
import csv
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "real_image_samples"
MANIFEST = OUT_DIR / "SOURCES.md"
CSV_PATH = OUT_DIR / "image_review.csv"

SAMPLES = [
    {
        "filename": "fruiting_coconut_palm_canopy.jpg",
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Fruiting_Coconut_Palm_Canopy.jpg?width=1100",
        "source_page": "https://commons.wikimedia.org/wiki/File:Fruiting_Coconut_Palm_Canopy.jpg",
        "creator": "Paul The Writer",
        "license": "CC0 1.0",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
        "purpose": "Coconut canopy visual review",
    },
    {
        "filename": "coconut_plucker_harvesting.jpg",
        "url": "https://commons.wikimedia.org/wiki/Special:FilePath/Coconut_Plucker_plucking_coconuts_on_a_tree_in_Mumbai..JPG?width=1100",
        "source_page": "https://commons.wikimedia.org/wiki/File:Coconut_Plucker_plucking_coconuts_on_a_tree_in_Mumbai..JPG",
        "creator": "Rudolph A. Furtado",
        "license": "CC0 1.0",
        "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
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


def download_samples() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest_lines = [
        "# Real coconut image sample sources",
        "",
        "These photographs are downloaded on demand; they are not included in the repository.",
        "Review the original source page and licence before redistribution.",
        "",
    ]
    for sample in SAMPLES:
        target = OUT_DIR / sample["filename"]
        request = urllib.request.Request(
            sample["url"],
            headers={"User-Agent": "Coconut-Harvest-AI-local-research-demo/1.0"},
        )
        print(f"Downloading {sample['filename']} ...")
        with urllib.request.urlopen(request, timeout=30) as response:
            content_type = response.headers.get("Content-Type", "")
            data = response.read()
        if not data or (content_type and "image" not in content_type.lower()):
            raise RuntimeError(
                f"Expected an image for {sample['filename']}, got "
                f"{content_type or 'unknown content type'}. Open the source page manually."
            )
        target.write_bytes(data)
        manifest_lines.extend(
            [
                f"## {sample['filename']}",
                f"- Creator: {sample['creator']}",
                f"- Source: {sample['source_page']}",
                f"- Licence stated in repository reference: {sample['license']} ({sample['license_url']})",
                f"- Intended use: {sample['purpose']}",
                f"- Download URL: {sample['url']}",
                "",
            ]
        )
        print(f"Saved: {target}")

    MANIFEST.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    with CSV_PATH.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for sample in SAMPLES:
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
