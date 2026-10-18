import math
from pathlib import Path

import pytest

from apps.pui89_app.local_detector import (
    coconut_class_ids,
    detect_coconuts,
    load_local_coconut_model,
)


def test_coconut_class_ids_support_dict_and_list_names():
    assert coconut_class_ids({0: "person", 1: "coconut", 2: "coconut bunch"}) == {1, 2}
    assert coconut_class_ids(["person", "coconuts"]) == {1}


def test_non_coconut_labels_are_not_accepted():
    assert coconut_class_ids({0: "sports ball", 1: "apple", 2: "banana"}) == set()


def test_missing_local_model_fails_before_ultralytics_import(tmp_path):
    with pytest.raises(FileNotFoundError, match="Local model file"):
        load_local_coconut_model(tmp_path / "missing.pt")


@pytest.mark.parametrize("confidence", [-0.1, 1.1, math.nan, math.inf])
def test_invalid_confidence_is_rejected_without_model_call(confidence):
    with pytest.raises(ValueError, match="confidence"):
        detect_coconuts(object(), object(), {0}, confidence=confidence)


@pytest.mark.parametrize("image_size", [0, 31, 4097])
def test_invalid_image_size_is_rejected_without_model_call(image_size):
    with pytest.raises(ValueError, match="image_size"):
        detect_coconuts(object(), object(), {0}, image_size=image_size)


def test_empty_class_set_is_rejected_without_model_call():
    with pytest.raises(ValueError, match="coconut class ID"):
        detect_coconuts(object(), object(), set())


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
    def __init__(self):
        self.xyxy = FakeTensor([[10, 20, 40, 60], [1, 2, 3, 4], [5, 5, 5, 9]])
        self.conf = FakeTensor([0.91, 0.99, 0.88])
        self.cls = FakeTensor([1, 0, 1])


class FakeResult:
    boxes = FakeBoxes()
    names = {0: "person", 1: "coconut"}


class FakeModel:
    names = {0: "person", 1: "coconut"}

    def predict(self, **kwargs):
        assert kwargs["device"] == "cpu"
        assert kwargs["verbose"] is False
        return [FakeResult()]


def test_detection_filters_other_classes_and_invalid_boxes():
    detections = detect_coconuts(FakeModel(), object(), {1})
    assert len(detections) == 1
    assert detections[0]["class_name"] == "coconut"
    assert detections[0]["confidence"] == pytest.approx(0.91)
    assert detections[0]["bbox_xyxy_pixels"] == [10.0, 20.0, 40.0, 60.0]
