"""Run a local PUI89 appearance model on one cropped coconut image."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pui89_models.coconut_maturity import extract_rgb_features, load_model, predict_features


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, type=Path)
    parser.add_argument("--image", required=True, type=Path)
    args = parser.parse_args()
    if not args.model.is_file() or not args.image.is_file():
        parser.error("model and image must both exist")
    result = predict_features(load_model(args.model), extract_rgb_features(args.image))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
