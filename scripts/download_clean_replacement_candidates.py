#!/usr/bin/env python3
"""Download two newly reviewed coconut image candidates; does not create labels."""
import hashlib
import urllib.request
from pathlib import Path

OUT = Path("data/review_batch_2026-10-19/images")
ITEMS = [
    ("0033_Coconut_bunch_in_the_tree.JPG",
     "https://upload.wikimedia.org/wikipedia/commons/d/d0/Coconut_bunch_in_the_tree.JPG",
     "36986fc8a09899c84468b60491cae1acdef567c9"),
    ("0034_Coconut_fruits.jpg",
     "https://upload.wikimedia.org/wikipedia/commons/d/d8/Coconut_fruits.jpg",
     "afb1ab478f0b2b25af495082665fa3ede7fdfc55"),
]

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    failed = False
    for filename, url, expected in ITEMS:
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Pui89-Coconut-Harvest-AI/1.0"})
            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read()
            digest = hashlib.sha1(data).hexdigest()
            if digest != expected or data[:3] != bytes([255, 216, 255]):
                raise ValueError(f"integrity check failed (SHA-1 {digest})")
            (OUT / filename).write_bytes(data)
            print(f"OK {filename} {len(data)} bytes sha1={digest}")
        except Exception as exc:
            failed = True
            print(f"FAILED {filename}: {exc}")
    print("Images are candidates only; annotation and independent QA are still required.")
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
