#!/usr/bin/env python3
"""Create local image/box previews to manually QA a YOLO coconut dataset.

This does not change labels or decide whether boxes are correct. It only renders
existing annotations so a person can inspect missed/incorrect boxes.
"""
from __future__ import annotations

import argparse
import html
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path, help="Dataset root with images/<split> and labels/<split>.")
    parser.add_argument("--split", choices=("train", "val", "test"), default="train")
    parser.add_argument("--out", type=Path, default=Path("reports/label_previews"))
    parser.add_argument("--limit", type=int, default=100, help="Maximum number of images to preview.")
    parser.add_argument("--max-side", type=int, default=1000)
    args = parser.parse_args()
    root = args.root.expanduser().resolve()
    image_dir, label_dir = root / "images" / args.split, root / "labels" / args.split
    if not image_dir.is_dir() or not label_dir.is_dir():
        raise FileNotFoundError(f"Expected {image_dir} and {label_dir}")
    if args.limit < 1 or args.max_side < 128:
        parser.error("--limit must be positive and --max-side must be at least 128.")
    images = sorted(p for p in image_dir.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES)
    if not images:
        raise ValueError(f"No images found in {image_dir}")
    output = args.out.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    cards = []
    problems = []
    for index, source in enumerate(images[:args.limit], start=1):
        rel = source.relative_to(image_dir)
        label = (label_dir / rel).with_suffix(".txt")
        if not label.is_file():
            problems.append(f"{rel}: missing label file")
            continue
        try:
            with Image.open(source) as im:
                image = im.convert("RGB")
        except Exception as exc:
            problems.append(f"{rel}: unreadable image ({exc})")
            continue
        draw = ImageDraw.Draw(image)
        width, height = image.size
        boxes = 0
        for line_no, line in enumerate(label.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            fields = line.split()
            if len(fields) != 5:
                problems.append(f"{rel}:{line_no}: expected five label columns")
                continue
            try:
                class_id = int(fields[0])
                x, y, w, h = (float(v) for v in fields[1:])
            except ValueError:
                problems.append(f"{rel}:{line_no}: invalid numeric label")
                continue
            if class_id != 0 or not (0 <= x <= 1 and 0 <= y <= 1 and 0 < w <= 1 and 0 < h <= 1):
                problems.append(f"{rel}:{line_no}: invalid coconut class or normalized coordinates")
                continue
            left, top = (x - w / 2) * width, (y - h / 2) * height
            right, bottom = (x + w / 2) * width, (y + h / 2) * height
            if left < 0 or top < 0 or right > width or bottom > height:
                problems.append(f"{rel}:{line_no}: box extends outside image")
                continue
            draw.rectangle((left, top, right, bottom), outline=(255, 135, 0), width=max(2, round(min(width, height) / 300)))
            draw.text((left + 2, max(0, top - 16)), f"coconut {boxes + 1}", fill=(255, 235, 80), stroke_width=2, stroke_fill=(20, 20, 20))
            boxes += 1
        scale = min(args.max_side / max(width, height), 1)
        if scale < 1:
            image = image.resize((round(width * scale), round(height * scale)), Image.Resampling.LANCZOS)
        target = output / f"{index:04d}_{source.stem}.jpg"
        image.save(target, quality=90)
        cards.append((target.name, str(rel).replace("\\", "/"), boxes))
    rows = []
    for filename, rel, boxes in cards:
        rows.append(
            '<article><a href="' + html.escape(filename, quote=True) + '"><img loading="lazy" src="' +
            html.escape(filename, quote=True) + '" alt="Bounding-box preview for ' + html.escape(rel, quote=True) +
            '"></a><p><strong>' + html.escape(rel) + '</strong><br>Boxes: ' + str(boxes) + '</p></article>'
        )
    problem_html = "".join("<li>" + html.escape(problem) + "</li>" for problem in problems)
    page = """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>PUI89 label QA preview</title><style>body{font-family:system-ui,sans-serif;margin:1.5rem;color:#17212b}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1rem}article{border:1px solid #ccd5d9;border-radius:8px;padding:.6rem;overflow:hidden}img{width:100%;height:auto}p{overflow-wrap:anywhere;font-size:.9rem}.warn{background:#fff5df;padding:.8rem}h1{font-size:1.4rem}</style>
<h1>PUI89 Coconut dataset — manual label QA</h1><p>Split: """ + html.escape(args.split) + """ · Previewed """ + str(len(cards)) + """ image(s).</p>
<p class="warn">Visually inspect each image: every visible target should be boxed, boxes should fit fruit tightly, and negative images should have zero boxes. This preview cannot certify annotation correctness.</p>
""" + ("<h2>File/label warnings</h2><ul>" + problem_html + "</ul>" if problems else "<p>No file/format warnings were found in the previews.</p>") + "<main>" + "".join(rows) + "</main></html>"
    index_path = output / "index.html"
    index_path.write_text(page, encoding="utf-8")
    print(f"Previewed {len(cards)} image(s); warnings={len(problems)}")
    print(f"Open: {index_path}")
    print("Manual visual review is still required; this tool does not assess box correctness.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
