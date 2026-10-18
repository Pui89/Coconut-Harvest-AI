#!/usr/bin/env python3
"""Build a local HTML gallery for reviewing downloaded Commons candidates.

Reads tools/collect_commons_coconuts.py output (images/ and provenance.csv).
It does not label images, determine whether an image is an orchard scene, or
replace human licence and relevance review. Output stays on the local machine.
"""
from __future__ import annotations

import argparse
import csv
import html
from pathlib import Path
from urllib.parse import quote


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--collection-dir", type=Path, default=Path("data/commons_candidates"))
    parser.add_argument("--output", type=Path, help="Output HTML; defaults to <collection-dir>/review_gallery.html")
    args = parser.parse_args()
    root = args.collection_dir.expanduser().resolve()
    provenance = root / "provenance.csv"
    if not provenance.is_file():
        parser.error(f"Missing {provenance}; run tools/collect_commons_coconuts.py first.")
    output = args.output.expanduser().resolve() if args.output else root / "review_gallery.html"
    records = []
    with provenance.open("r", newline="", encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            rel = Path(row.get("local_file", ""))
            image = (root / rel).resolve()
            if not image.is_file() or root not in image.parents:
                row["local_exists"] = "NO"
            else:
                row["local_exists"] = "YES"
                row["browser_path"] = Path(rel).as_posix()
            records.append(row)

    cards = []
    for row in records:
        title = html.escape(row.get("commons_title", "Untitled"))
        artist = html.escape(row.get("artist", ""))
        license_name = html.escape(row.get("license_short_name", "Unspecified"))
        credit = html.escape(row.get("credit", ""))
        description = html.escape(row.get("description", ""))
        page = html.escape(row.get("file_page_url", ""), quote=True)
        local = html.escape(row.get("browser_path", ""), quote=True)
        image_html = f'<img src="{local}" loading="lazy" alt="{title}">' if row["local_exists"] == "YES" else '<div class="missing">Local image missing</div>'
        cards.append(f"""
<article class="card">
  {image_html}
  <div class="meta">
    <h2>{title}</h2>
    <p><strong>Licence shown by Commons:</strong> {license_name}</p>
    <p><strong>Creator:</strong> {artist or "Not recorded"}</p>
    <p><strong>Credit:</strong> {credit or "Not recorded"}</p>
    <p>{description}</p>
    <p><a href="{page}" target="_blank" rel="noopener">Open original file page and verify terms ↗</a></p>
    <label><input type="checkbox"> Reviewed</label>
    <label><input type="checkbox"> Useful orchard/canopy image</label>
    <label><input type="checkbox"> Licence and attribution verified</label>
    <p class="note">Do not treat browser checkboxes as a saved audit. Record decisions in your own review sheet.</p>
  </div>
</article>""")
    output.parent.mkdir(parents=True, exist_ok=True)
    document = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PUI89 Coconut candidate review gallery</title>
<style>
body{font-family:system-ui,sans-serif;margin:0;background:#f3f6f5;color:#182521}header{padding:1.2rem;background:#143f36;color:white}main{max-width:1200px;margin:auto;padding:1rem}.card{display:grid;grid-template-columns:minmax(220px,42%) 1fr;gap:1rem;background:white;border:1px solid #d5e0dc;border-radius:12px;padding:1rem;margin:1rem 0}.card img{width:100%;max-height:420px;object-fit:contain;background:#eaf0ed}.meta h2{font-size:1.1rem;margin-top:0;overflow-wrap:anywhere}.meta p{overflow-wrap:anywhere}.note{font-size:.85rem;color:#5c6b65}.missing{padding:3rem 1rem;background:#eee}.notice{background:#fff4d7;padding:.8rem;border-left:4px solid #bd8313}label{display:block;margin:.45rem 0}@media(max-width:680px){.card{grid-template-columns:1fr}}
</style></head><body><header><h1>PUI89 Coconut Harvest AI — candidate image review</h1><p>Local review page · no upload · no automatic labels</p></header><main>
<div class="notice"><strong>Important:</strong> candidates were retrieved by search terms, not verified as orchard images. Open each source page and verify the exact licence, attribution requirements, and permitted use. Remove irrelevant images. This page does not persist checkbox selections.</div>
<p>Review images for coconut visibility, orchard/canopy relevance, image quality, licence terms, and attribution. Do not assume that a permissive licence alone makes the image representative of real harvesting conditions.</p>
""" + "\n".join(cards) + "\n</main></body></html>\n"
    output.write_text(document, encoding="utf-8")
    print(f"Created review gallery: {output}")
    print(f"Candidate records: {len(records)}")
    print("Open the HTML file in a browser. Verify original licences and record review decisions separately.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
