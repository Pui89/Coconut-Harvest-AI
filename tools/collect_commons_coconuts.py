"""Download openly licensed coconut-related images from Wikimedia Commons.

Only CC0, Public Domain, CC BY, and CC BY-SA files are accepted by default.
This is a candidate image collector, not a ready-made labelled detection dataset:
every image must be reviewed and coconut instances annotated before training.
"""
from __future__ import annotations
import argparse, csv, json, re, time
from pathlib import Path
from urllib.parse import urlparse
import requests

API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "Pui89-Coconut-Harvest-AI-research/1.0 (open dataset curation; contact via GitHub repository)"
ALLOWED_LICENSE = re.compile(r"^(CC0|Public domain|CC BY(?:-SA)?(?:\s|$))", re.IGNORECASE)
IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}

def allowed_license(short_name: str) -> bool:
    name = (short_name or "").strip()
    if not name or re.search(r"\b(NC|ND)\b|NonCommercial|NoDerivatives", name, re.IGNORECASE):
        return False
    return bool(ALLOWED_LICENSE.search(name))

def api_get(session: requests.Session, params: dict) -> dict:
    response = session.get(API, params=params, timeout=45)
    response.raise_for_status()
    return response.json()

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default="data/commons_candidates")
    parser.add_argument("--limit", type=int, default=100, help="Maximum candidate images to download.")
    parser.add_argument("--max-mb", type=float, default=12, help="Skip individual files larger than this size.")
    parser.add_argument("--pause", type=float, default=0.5, help="Seconds between downloads.")
    args = parser.parse_args()
    if args.limit < 1 or args.max_mb <= 0 or args.pause < 0:
        parser.error("limit and max-mb must be positive; pause cannot be negative.")
    out = Path(args.out).expanduser().resolve()
    images_dir = out / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT})
    # Prioritize images likely to show fruits on a palm; general coconut images
    # are useful for annotation practice but may be out-of-domain for harvesting.
    queries = [
        '"coconuts on tree"',
        '"coconut palm fruits"',
        '"coconut harvest"',
        '"coconut plantation"',
        '"coconut tree fruit"',
        '"coconut bunch"',
    ]
    seen_titles, records = set(), []
    for query in queries:
        if len(records) >= args.limit:
            break
        params = {
            "action": "query", "format": "json", "generator": "search",
            "gsrsearch": f"filetype:bitmap {query}", "gsrnamespace": 6,
            "gsrlimit": min(50, args.limit), "prop": "imageinfo",
            "iiprop": "url|size|extmetadata", "iiurlwidth": 1280,
        }
        try:
            data = api_get(session, params)
        except Exception as exc:
            print(f"Search failed for {query!r}: {exc}")
            continue
        pages = (data.get("query") or {}).get("pages") or {}
        for page in sorted(pages.values(), key=lambda x: x.get("title", "")):
            if len(records) >= args.limit:
                break
            title = page.get("title", "")
            if title in seen_titles:
                continue
            seen_titles.add(title)
            info = (page.get("imageinfo") or [{}])[0]
            meta = info.get("extmetadata") or {}
            short = (meta.get("LicenseShortName") or {}).get("value", "")
            if not allowed_license(short):
                continue
            original_url = info.get("url", "")
            download_url = info.get("thumburl") or original_url
            ext = Path(urlparse(original_url).path).suffix.lower()
            if ext not in IMAGE_SUFFIXES:
                continue
            size = info.get("size") or 0
            if size > args.max_mb * 1024 * 1024:
                continue
            page_url = "https://commons.wikimedia.org/wiki/" + title.replace(" ", "_")
            filename = re.sub(r"[^A-Za-z0-9._-]+", "_", Path(urlparse(download_url).path).name)[:120]
            if not filename or filename.startswith("."):
                filename = f"commons_{len(records)+1}{ext}"
            target = images_dir / f"{len(records)+1:04d}_{filename}"
            try:
                response = session.get(download_url, timeout=60)
                response.raise_for_status()
                if not response.headers.get("Content-Type", "").lower().startswith("image/"):
                    print(f"Skip non-image response: {title}")
                    continue
                target.write_bytes(response.content)
            except Exception as exc:
                print(f"Download failed for {title!r}: {exc}")
                continue
            def value(key: str) -> str:
                return re.sub(r"<[^>]+>", "", (meta.get(key) or {}).get("value", "")).strip()
            records.append({
                "local_file": str(target.relative_to(out)),
                "commons_title": title,
                "file_page_url": page_url,
                "downloaded_from": download_url,
                "license_short_name": short,
                "license_url": value("LicenseUrl"),
                "usage_terms": value("UsageTerms"),
                "artist": value("Artist"),
                "credit": value("Credit"),
                "attribution_required": value("AttributionRequired"),
                "description": value("ImageDescription"),
                "search_query": query,
                "annotation_status": "UNREVIEWED_NOT_LABELLED",
            })
            print(f"Downloaded candidate {len(records)}/{args.limit}: {title} [{short}]")
            time.sleep(args.pause)
    fields = [
        "local_file", "commons_title", "file_page_url", "downloaded_from",
        "license_short_name", "license_url", "usage_terms", "artist", "credit",
        "attribution_required", "description", "search_query", "annotation_status",
    ]
    with (out / "provenance.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)
    (out / "collection_summary.json").write_text(json.dumps({
        "candidate_images_downloaded": len(records),
        "limit": args.limit,
        "out_dir": str(out),
        "status": "CANDIDATES_ONLY_REVIEW_AND_ANNOTATION_REQUIRED",
        "warning": "Not a ready-made dataset. Verify each image's licence and coconut visibility, label every coconut, and split by source/session before training.",
    }, indent=2) + "\n", encoding="utf-8")
    print(f"\nDownloaded {len(records)} candidate images. Review images and provenance.csv before annotation.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
