#!/usr/bin/env python3
"""Download and verify the two CC BY-SA coconut-image candidates.

This script downloads the original files from Wikimedia Commons into
data/review_batch_2026-10-19/images/. It does not create labels or approve
images for training. Run from the repository root with Python 3.
"""
from __future__ import annotations

import hashlib
import urllib.request
from pathlib import Path

OUT = Path("data/review_batch_2026-10-19/images")
CANDIDATES = [
    {
        "id": "0031",
        "filename": "0031_Coconuts_in_coconut_tree.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/5/54/Coconuts_in_coconut_tree.jpg",
        "sha1": "563f124499949b9bef3bd78c0ace61aacfbaf961",
        "source": "https://commons.wikimedia.org/wiki/File:Coconuts_in_coconut_tree.jpg",
        "license": "CC BY-SA 3.0",
    },
    {
        "id": "0032",
        "filename": "0032_Coconut_in_Coconut_Tree.jpg",
        "url": "https://upload.wikimedia.org/wikipedia/commons/b/be/Coconut_in_Coconut_Tree.jpg",
        "sha1": "34a77896b7ad78532cd41aadc2c3967220fd91ab",
        "source": "https://commons.wikimedia.org/wiki/File:Coconut_in_Coconut_Tree.jpg",
        "license": "CC BY-SA 4.0",
    },
]


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    failures = 0
    for item in CANDIDATES:
        path = OUT / item["filename"]
        request = urllib.request.Request(
            item["url"],
            headers={"User-Agent": "Coconut-Harvest-AI-dataset-audit/1.0"},
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read()
            digest = hashlib.sha1(data).hexdigest()
            if digest != item["sha1"]:
                raise ValueError(
                    f"SHA-1 mismatch: expected {item['sha1']}, received {digest}"
                )
            if not data.startswith(b"\xff\xd8\xff"):
                raise ValueError("Downloaded content does not appear to be a JPEG")
            path.write_bytes(data)
            print(
                f"OK {item['id']}: {path} ({len(data)} bytes; SHA-1 {digest})\n"
                f"  Source: {item['source']}\n"
                f"  License: {item['license']}"
            )
        except Exception as exc:
            failures += 1
            print(f"FAILED {item['id']} ({item['source']}): {exc}")
    if failures:
        print(
            "\nOne or more downloads failed. Do not create labels or use these "
            "files for training until the original image and license are verified."
        )
        return 1
    print(
        "\nDownload/checksum stage passed. This does NOT mean the images are "
        "annotation-reviewed or training-approved. Inspect full-resolution "
        "images, create labels, run annotation QA, and record reviewer approval."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
