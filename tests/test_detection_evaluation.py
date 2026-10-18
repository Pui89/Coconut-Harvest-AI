import csv
import json

import pytest

from scripts.evaluate_coconut_detections import evaluate


def write_csv(path, fieldnames, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


GT_FIELDS = ["image_file", "xmin", "ymin", "xmax", "ymax", "class_name"]
PRED_FIELDS = GT_FIELDS + ["confidence"]


def box(image="a.jpg", xmin=0, ymin=0, xmax=10, ymax=10, confidence=0.9):
    return {
        "image_file": image, "xmin": xmin, "ymin": ymin,
        "xmax": xmax, "ymax": ymax, "class_name": "coconut",
        "confidence": confidence,
    }


def test_perfect_prediction_has_perfect_metrics(tmp_path):
    gt = tmp_path / "gt.csv"
    pred = tmp_path / "pred.csv"
    write_csv(gt, GT_FIELDS, [{k: v for k, v in box().items() if k != "confidence"}])
    write_csv(pred, PRED_FIELDS, [box()])
    report = evaluate(gt, pred)
    assert report["precision"] == 1.0
    assert report["recall"] == 1.0
    assert report["f1"] == 1.0
    assert report["macro_ap_at_iou_threshold"] == 1.0


def test_missed_ground_truth_is_false_negative(tmp_path):
    gt = tmp_path / "gt.csv"
    pred = tmp_path / "pred.csv"
    write_csv(gt, GT_FIELDS, [{k: v for k, v in box().items() if k != "confidence"}])
    write_csv(pred, PRED_FIELDS, [])
    report = evaluate(gt, pred)
    assert report["false_negatives"] == 1
    assert report["recall"] == 0.0


def test_duplicate_prediction_counts_as_false_positive(tmp_path):
    gt = tmp_path / "gt.csv"
    pred = tmp_path / "pred.csv"
    write_csv(gt, GT_FIELDS, [{k: v for k, v in box().items() if k != "confidence"}])
    write_csv(pred, PRED_FIELDS, [box(confidence=0.9), box(confidence=0.8)])
    report = evaluate(gt, pred)
    assert report["true_positives"] == 1
    assert report["false_positives"] == 1


def test_wrong_image_prediction_does_not_match(tmp_path):
    gt = tmp_path / "gt.csv"
    pred = tmp_path / "pred.csv"
    write_csv(gt, GT_FIELDS, [{k: v for k, v in box().items() if k != "confidence"}])
    write_csv(pred, PRED_FIELDS, [box(image="other.jpg")])
    report = evaluate(gt, pred)
    assert report["false_positives"] == 1
    assert report["false_negatives"] == 1


@pytest.mark.parametrize("confidence", [-0.1, 1.1, float("nan")])
def test_invalid_confidence_is_rejected(tmp_path, confidence):
    gt = tmp_path / "gt.csv"
    pred = tmp_path / "pred.csv"
    write_csv(gt, GT_FIELDS, [{k: v for k, v in box().items() if k != "confidence"}])
    write_csv(pred, PRED_FIELDS, [box(confidence=confidence)])
    with pytest.raises(ValueError, match="confidence"):
        evaluate(gt, pred)


def test_zero_area_box_is_rejected(tmp_path):
    gt = tmp_path / "gt.csv"
    pred = tmp_path / "pred.csv"
    write_csv(gt, GT_FIELDS, [{k: v for k, v in box().items() if k != "confidence"}])
    write_csv(pred, PRED_FIELDS, [box(xmax=0)])
    with pytest.raises(ValueError, match="positive width"):
        evaluate(gt, pred)
