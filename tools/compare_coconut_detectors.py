"""Compare multiple coconut detector exports on one shared ground-truth CSV.

This tool evaluates supplied prediction CSVs only; it does not run AI models.
All candidates use the same ground truth, IoU threshold, and score threshold.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from tools.evaluate_coconut_detections import evaluate, read_boxes


def parse_candidate(value: str) -> tuple[str, Path]:
    name, separator, raw_path = value.partition("=")
    name = name.strip()
    raw_path = raw_path.strip()
    if not separator or not name or not raw_path:
        raise ValueError("Candidate must use NAME=PATH format.")
    return name, Path(raw_path)


def compare_candidates(
    ground_truth_path: Path,
    candidates: list[tuple[str, Path]],
    iou_threshold: float = 0.5,
    score_threshold: float = 0.0,
) -> dict:
    if not candidates:
        raise ValueError("At least one candidate prediction file is required.")
    names = [name for name, _ in candidates]
    if len(names) != len(set(names)):
        raise ValueError("Candidate names must be unique.")
    truth = read_boxes(ground_truth_path, predictions=False)
    results = []
    for name, path in candidates:
        predictions = read_boxes(path, predictions=True)
        metrics = evaluate(
            truth,
            predictions,
            iou_threshold=iou_threshold,
            score_threshold=score_threshold,
        )
        results.append({
            "name": name,
            "prediction_file": str(path),
            "precision": metrics["precision"],
            "recall": metrics["recall"],
            "f1": metrics["f1"],
            "true_positives": metrics["true_positives"],
            "false_positives": metrics["false_positives"],
            "false_negatives": metrics["false_negatives"],
            "prediction_count_after_score_threshold": metrics["prediction_count_after_score_threshold"],
            "per_class": metrics["per_class"],
        })
    # Deterministic ordering; this is a metric ranking, not an overall robot ranking.
    results.sort(
        key=lambda item: (item["f1"], item["recall"], item["precision"], item["name"]),
        reverse=True,
    )
    for rank, result in enumerate(results, start=1):
        result["rank_by_detection_metrics"] = rank
    return {
        "comparison_type": "shared-ground-truth single-threshold detection comparison",
        "ground_truth_file": str(ground_truth_path),
        "ground_truth_count": len(truth),
        "iou_threshold": iou_threshold,
        "score_threshold": score_threshold,
        "candidates": results,
        "limitations": [
            "This tool evaluates supplied CSV boxes; it does not run AI models.",
            "Fair comparison requires identical image IDs, reviewed ground truth, and a frozen held-out split.",
            "Ranking uses F1, then recall, then precision; it does not include runtime, memory, energy, cost, safety, maturity accuracy, localization, or robot performance.",
            "Do not select models on the final test set or claim generalization from a tiny sample.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ground-truth", type=Path, required=True)
    parser.add_argument(
        "--candidate",
        action="append",
        required=True,
        metavar="NAME=PATH",
        help="Prediction CSV; repeat for each detector export.",
    )
    parser.add_argument("--iou", type=float, default=0.5)
    parser.add_argument("--score", type=float, default=0.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        candidates = [parse_candidate(value) for value in args.candidate]
        report = compare_candidates(
            args.ground_truth, candidates, args.iou, args.score
        )
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    rendered = json.dumps(report, indent=2)
    print(rendered)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
