"""Dependency-free, deterministic IoU tracker for frame-by-frame detections.

This is a simple baseline, not a robust multi-object tracking benchmark. It
associates boxes greedily by IoU and does not handle camera motion or occlusion
reasoning. Run on detections produced by a separately validated detector.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Sequence


@dataclass(frozen=True)
class Detection:
    bbox_xyxy_pixels: tuple[float, float, float, float]
    confidence: float
    class_name: str = "coconut"


@dataclass(frozen=True)
class TrackedDetection:
    track_id: str
    bbox_xyxy_pixels: tuple[float, float, float, float]
    confidence: float
    age_frames: int


def box_iou(a: Sequence[float], b: Sequence[float]) -> float:
    if len(a) != 4 or len(b) != 4:
        return 0.0
    ax1, ay1, ax2, ay2 = map(float, a)
    bx1, by1, bx2, by2 = map(float, b)
    if not all(isfinite(v) for v in (ax1, ay1, ax2, ay2, bx1, by1, bx2, by2)):
        return 0.0
    if ax2 <= ax1 or ay2 <= ay1 or bx2 <= bx1 or by2 <= by1:
        return 0.0
    iw = max(0.0, min(ax2, bx2) - max(ax1, bx1))
    ih = max(0.0, min(ay2, by2) - max(ay1, by1))
    intersection = iw * ih
    union = (ax2 - ax1) * (ay2 - ay1) + (bx2 - bx1) * (by2 - by1) - intersection
    return intersection / union if union > 0 else 0.0


class IoUTracker:
    def __init__(self, *, min_iou: float = 0.30, max_missed_frames: int = 2) -> None:
        if not 0 <= min_iou <= 1:
            raise ValueError("min_iou must be in [0, 1]")
        if max_missed_frames < 0:
            raise ValueError("max_missed_frames must be non-negative")
        self.min_iou = min_iou
        self.max_missed_frames = max_missed_frames
        self._next_id = 1
        self._tracks: dict[str, dict] = {}

    def update(self, detections: Sequence[Detection]) -> list[TrackedDetection]:
        candidates = []
        for track_id, track in self._tracks.items():
            for index, det in enumerate(detections):
                if track["class_name"] != det.class_name:
                    continue
                overlap = box_iou(track["bbox"], det.bbox_xyxy_pixels)
                if overlap >= self.min_iou:
                    candidates.append((-overlap, track_id, index))
        candidates.sort()
        used_tracks: set[str] = set()
        used_detections: set[int] = set()
        assignment: dict[int, str] = {}
        for _negative_iou, track_id, index in candidates:
            if track_id in used_tracks or index in used_detections:
                continue
            used_tracks.add(track_id)
            used_detections.add(index)
            assignment[index] = track_id

        for index, det in enumerate(detections):
            if index not in assignment:
                track_id = f"track-{self._next_id:04d}"
                self._next_id += 1
                assignment[index] = track_id
                self._tracks[track_id] = {
                    "bbox": det.bbox_xyxy_pixels, "class_name": det.class_name,
                    "confidence": det.confidence, "age": 1, "missed": 0,
                }
            else:
                track = self._tracks[assignment[index]]
                track.update(bbox=det.bbox_xyxy_pixels, confidence=det.confidence,
                             age=track["age"] + 1, missed=0)

        for track_id in list(self._tracks):
            if track_id not in used_tracks and track_id not in assignment.values():
                self._tracks[track_id]["missed"] += 1
                if self._tracks[track_id]["missed"] > self.max_missed_frames:
                    del self._tracks[track_id]

        return [
            TrackedDetection(
                track_id=assignment[index],
                bbox_xyxy_pixels=det.bbox_xyxy_pixels,
                confidence=det.confidence,
                age_frames=self._tracks[assignment[index]]["age"],
            )
            for index, det in enumerate(detections)
        ]
