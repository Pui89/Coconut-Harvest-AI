#!/usr/bin/env python3
"""Fetch allowlisted Wikimedia Commons coconut-image candidates for local review.

This utility downloads source images and writes a provenance manifest. It NEVER
creates annotations or marks images as training-approved. Run from repository root:
    python tools/fetch_coconut_candidates.py --download
Without --download it only queries source metadata and prints a report.
Standard library only; no model downloads, paid services, or extra dependencies.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API = "https://commons.wikimedia.org/w/api.php"
OUT_DIR = Path("data/candidate_images")
MANIFEST = Path("data/candidate_images/source_manifest.json")
USER_AGENT = "PUI89-Coconut-Harvest-Research/1.0 (research provenance; contact via GitHub repository)"
# Fixed allowlist: do not accept arbitrary URLs or paths from command-line input.
CANDIDATES = (
    {"id": "candidate_0032", "title": "File:Coconut in Coconut Tree.jpg"},
    {"id": "shortlist_a", "title": "File:Coconuts in coconut tree.jpg"},
    {"id": "shortlist_b", "title": "File:Coconut tree top.JPG"},
    {"id": "shortlist_c", "title": "File:Coconut Tree With Coconuts.jpg"},
    {"id": "shortlist_d", "title": "File:Coconut bunch in the tree.JPG"},
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def commons_metadata(title: str) -> dict:
    params = urlencode({
        "action": "query", "format": "json", "formatversion": "2",
        "titles": title, "prop": "imageinfo", "iiprop": "url|size|extmetadata",
    })
    request = Request(f"{API}?{params}", headers={"User-Agent": USER_AGENT})
    # Wikimedia may temporarily throttle automated requests. Respect Retry-After
    # when present and retry 429s with bounded backoff rather than failing the
    # entire candidate batch on the first transient rate limit.
    for attempt in range(4):
        try:
            with urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
            break
        except HTTPError as exc:
            if exc.code != 429 or attempt == 3:
                raise
            retry_after = exc.headers.get("Retry-After")
            try:
                wait_seconds = max(1, int(retry_after)) if retry_after else min(30, 5 * (2 ** attempt))
            except (TypeError, ValueError):
                wait_seconds = min(30, 5 * (2 ** attempt))
            print(
                f"Rate limited for {title}; retry {attempt + 1}/3 in {wait_seconds}s",
                file=sys.stderr,
            )
            time.sleep(wait_seconds)
    pages = payload.get("query", {}).get("pages", [])
    if not pages or pages[0].get("missing"):
        raise ValueError(f"Commons file page not found: {title}")
    infos = pages[0].get("imageinfo", [])
    if not infos:
        raise ValueError(f"No imageinfo returned for: {title}")
    info = infos[0]
    ext = info.get("extmetadata", {})

    def plain(key: str) -> str:
        value = ext.get(key, {})
        raw = value.get("value", "") if isinstance(value, dict) else ""
        return re.sub(r"<[^>]*>", "", str(raw)).strip()

    return {
        "title": pages[0].get("title", title),
        "file_page": "https://commons.wikimedia.org/wiki/" + pages[0].get("title", title).replace(" ", "_"),
        "image_url": info.get("url"),
        "width": info.get("width"),
        "height": info.get("height"),
        "size_bytes": info.get("size"),
        "artist": plain("Artist"),
        "credit": plain("Credit"),
        "license_short_name": plain("LicenseShortName"),
        "license_url": plain("LicenseUrl"),
        "usage_terms": plain("UsageTerms"),
        "description": plain("ImageDescription"),
    }


def download_image(url: str, destination: Path) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response, destination.open("wb") as handle:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            handle.write(chunk)
    if destination.stat().st_size == 0:
        destination.unlink(missing_ok=True)
        raise ValueError(f"Downloaded empty file: {destination.name}")
    return sha256_file(destination)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true",
                        help="Download images locally after fetching current Commons metadata")
    parser.add_argument("--output-dir", type=Path, default=OUT_DIR)
    parser.add_argument("--manifest", type=Path, default=None)
    args = parser.parse_args()
    manifest_path = args.manifest or (args.output_dir / "source_manifest.json")
    records = []
    failures = []
    if args.download:
        args.output_dir.mkdir(parents=True, exist_ok=True)

    for index, candidate in enumerate(CANDIDATES):
        try:
            record = {"candidate_id": candidate["id"], **commons_metadata(candidate["title"])}
            record["downloaded"] = False
            record["sha256"] = None
            record["local_file"] = None
            if args.download:
                suffix = Path(record["title"].replace("File:", "")).suffix.lower()
                if suffix not in {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}:
                    raise ValueError(f"Unexpected image extension for {record['title']}")
                local_path = args.output_dir / f"{candidate['id']}{suffix}"
                record["sha256"] = download_image(record["image_url"], local_path)
                record["local_file"] = str(local_path).replace("\\", "/")
                record["downloaded"] = True
            record["training_approved"] = False
            record["human_annotation_qa"] = "not_completed"
            records.append(record)
            print(f"OK {candidate['id']}: {record['width']}x{record['height']} | "
                  f"{record['license_short_name'] or 'licence metadata missing'} | "
                  f"{'downloaded' if record['downloaded'] else 'metadata only'}")
        except Exception as exc:  # keep processing other candidates if one source fails
            failures.append({"candidate_id": candidate["id"], "error": str(exc)})
            print(f"ERROR {candidate['id']}: {exc}", file=sys.stderr)
        if index < len(CANDIDATES) - 1:
            time.sleep(1)  # be polite to Wikimedia Commons

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema": "pui89-coconut-source-manifest-v1",
        "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "download_requested": args.download,
        "candidate_count": len(CANDIDATES),
        "records_returned": len(records),
        "failures": failures,
        "warning": "Metadata and downloads are for manual review only. Verify the source page, exact licence/attribution, image contents, annotations, and independent QA. No record is training-approved.",
        "candidates": records,
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Manifest: {manifest_path}")
    print(f"Returned: {len(records)}/{len(CANDIDATES)}; failures: {len(failures)}")
    print("Training-approved by this tool: 0")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
