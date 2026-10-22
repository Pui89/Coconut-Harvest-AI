"""Unit tests for the optional local coconut detector adapter.

These tests use fake model outputs and do not download weights or require a GPU.
"""
import math
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

from apps.pui89_app.local_detector import (
    coconut_class_ids,
    detect_coconuts,
    load_local_coconut_model,
    resolve_inference_device,
)


class FakeTensor:
    def __init__(self, values):
        self.values = values

    def detach(self):
        return self

    def cpu(self):
        return self

    def tolist(self):
        return self.values


class FakeBoxes:
    def __init__(self, xyxy, conf, cls):
        self.xyxy = FakeTensor(xyxy)
        self.conf = FakeTensor(conf)
        self.cls = FakeTensor(cls)


class FakeResult:
    def __init__(self, boxes, names=None):
        self.boxes = boxes
        self.names = names or {0: "coconut", 1: "person"}


class FakeModel:
    names = {0: "coconut", 1: "person"}

    def __init__(self, results=None):
        self.results = results or []
        self.kwargs = None

    def predict(self, **kwargs):
        self.kwargs = kwargs
        return self.results


class LocalDetectorTests(unittest.TestCase):
    def test_coconut_class_ids_accepts_coconut_label_variants(self):
        self.assertEqual(
            coconut_class_ids({0: "Coconut", 1: "coconut bunch", 2: "coco-nut", 3: "person", 4: "coconuts"}),
            {0, 1, 4},
        )

    def test_coconut_class_ids_supports_list_names(self):
        self.assertEqual(coconut_class_ids(["person", "coconut"]), {1})

    def test_resolve_device_cpu_does_not_need_cuda(self):
        self.assertEqual(resolve_inference_device("cpu", cuda_available=True), "cpu")

    def test_resolve_auto_uses_cpu_when_cuda_unavailable(self):
        self.assertEqual(resolve_inference_device("auto", cuda_available=False), "cpu")

    def test_resolve_auto_uses_first_gpu_when_cuda_available(self):
        self.assertEqual(resolve_inference_device("auto", cuda_available=True), "0")

    def test_explicit_cuda_fails_when_unavailable(self):
        with self.assertRaisesRegex(RuntimeError, "CUDA was requested"):
            resolve_inference_device("cuda", cuda_available=False)

    def test_unknown_device_is_rejected(self):
        with self.assertRaises(ValueError):
            resolve_inference_device("mps", cuda_available=False)

    def test_missing_model_path_fails_before_ultralytics_import(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "missing.pt"
            with patch.dict(sys.modules, {"ultralytics": None}):
                with self.assertRaises(FileNotFoundError):
                    load_local_coconut_model(missing)

    def test_non_pt_model_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            model_file = Path(directory) / "weights.onnx"
            model_file.write_bytes(b"placeholder")
            with self.assertRaisesRegex(ValueError, "Only local .pt"):
                load_local_coconut_model(model_file)

    def test_loader_rejects_model_without_coconut_class(self):
        with tempfile.TemporaryDirectory() as directory:
            model_file = Path(directory) / "weights.pt"
            model_file.write_bytes(b"placeholder")
            fake_yolo = lambda _path: types.SimpleNamespace(names={0: "person"})
            with patch.dict(sys.modules, {"ultralytics": types.SimpleNamespace(YOLO=fake_yolo)}):
                with self.assertRaisesRegex(ValueError, "do not include 'coconut'"):
                    load_local_coconut_model(model_file)

    def test_detect_returns_only_valid_coconut_boxes_and_sets_cpu_options(self):
        boxes = FakeBoxes(
            [[1.123, 2, 30, 40], [0, 0, 10, 10], [5, 5, 2, 8], [math.nan, 0, 3, 4]],
            [0.91, 0.99, 0.8, 0.7],
            [0, 1, 0, 0],
        )
        model = FakeModel([FakeResult(boxes)])
        detections = detect_coconuts(model, "image.jpg", {0}, device="cpu")
        self.assertEqual(len(detections), 1)
        self.assertEqual(detections[0]["class_name"], "coconut")
        self.assertEqual(detections[0]["bbox_xyxy_pixels"], [1.12, 2.0, 30.0, 40.0])
        self.assertEqual(model.kwargs["device"], "cpu")
        self.assertFalse(model.kwargs["half"])
        self.assertEqual(model.kwargs["source"], "image.jpg")

    def test_detect_returns_empty_when_model_has_no_results(self):
        self.assertEqual(detect_coconuts(FakeModel([]), "image.jpg", {0}, device="cpu"), [])

    def test_detect_rejects_invalid_confidence_values(self):
        for confidence in (-0.1, 1.1, math.nan, math.inf):
            with self.subTest(confidence=confidence):
                with self.assertRaises(ValueError):
                    detect_coconuts(FakeModel(), "image.jpg", {0}, confidence=confidence)

    def test_detect_rejects_invalid_image_size(self):
        for image_size in (0, 31, 4097):
            with self.subTest(image_size=image_size):
                with self.assertRaises(ValueError):
                    detect_coconuts(FakeModel(), "image.jpg", {0}, image_size=image_size)

    def test_detect_requires_verified_coconut_class_ids(self):
        with self.assertRaisesRegex(ValueError, "verified coconut class ID"):
            detect_coconuts(FakeModel(), "image.jpg", set(), device="cpu")


if __name__ == "__main__":
    unittest.main()
