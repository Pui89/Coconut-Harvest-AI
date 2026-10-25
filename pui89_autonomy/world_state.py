"""Deterministic world-state tracking scaffold; standard library only."""
from __future__ import annotations
import math
from typing import Any, Mapping

def _finite_number(value: Any) -> bool:
    return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value)

class WorldStateTracker:
    """Track latest observations; conflicts/stale/low-confidence data remain unknown.
    This scaffold is not validated sensor fusion or a physical safety system.
    """
    def __init__(self, usable_confidence: float = 0.7) -> None:
        if not _finite_number(usable_confidence) or not 0 <= usable_confidence <= 1:
            raise ValueError("usable_confidence must be finite and in [0, 1]")
        self.usable_confidence = float(usable_confidence)
        self._tracks: dict[str, dict[str, Any]] = {}

    def update(self, observation: Mapping[str, Any]) -> dict[str, Any]:
        for key in ("object_id", "label", "source"):
            if not isinstance(observation.get(key), str) or not observation[key].strip():
                raise ValueError(f"{key} must be non-empty text")
        ts, confidence = observation.get("timestamp"), observation.get("confidence")
        if not _finite_number(ts) or ts < 0:
            raise ValueError("timestamp must be finite and non-negative")
        if not _finite_number(confidence) or not 0 <= confidence <= 1:
            raise ValueError("confidence must be finite and in [0, 1]")
        hazard = observation.get("hazard", False)
        if not isinstance(hazard, bool):
            raise ValueError("hazard must be boolean")
        oid, label, source = observation["object_id"].strip(), observation["label"].strip(), observation["source"].strip()
        ts, confidence = float(ts), float(confidence)
        previous = self._tracks.get(oid)
        if previous and ts < previous["timestamp"]:
            return {"accepted": False, "reason": "out_of_order_observation"}
        if previous and ts == previous["timestamp"] and label != previous["label"]:
            previous["label"] = None
            previous["confidence"] = min(previous["confidence"], confidence)
            previous["source"] = str(previous["source"]) + "," + source
            previous["hazard"] = previous["hazard"] or hazard
            previous["conflict"] = True
            return {"accepted": True, "conflict": True, "object_id": oid}
        self._tracks[oid] = {"object_id": oid, "label": label, "timestamp": ts,
                             "confidence": confidence, "source": source, "hazard": hazard, "conflict": False}
        return {"accepted": True, "conflict": False, "object_id": oid}

    def snapshot(self, now: float, stale_after: float = 5.0) -> dict[str, Any]:
        if not _finite_number(now) or now < 0:
            raise ValueError("now must be finite and non-negative")
        if not _finite_number(stale_after) or stale_after < 0:
            raise ValueError("stale_after must be finite and non-negative")
        tracks, stale_ids, unknown_ids, hazard_ids, conflict_ids = [], [], [], [], []
        for oid in sorted(self._tracks):
            track = dict(self._tracks[oid])
            track["stale"] = float(now) - track["timestamp"] > float(stale_after)
            track["usable"] = not track["stale"] and not track["conflict"] and track["confidence"] >= self.usable_confidence
            if track["stale"]: stale_ids.append(oid)
            if not track["usable"]: unknown_ids.append(oid)
            if track["hazard"]: hazard_ids.append(oid)
            if track["conflict"]: conflict_ids.append(oid)
            tracks.append(track)
        return {"track_count": len(tracks), "tracks": tracks, "stale_ids": stale_ids,
                "unknown_ids": unknown_ids, "hazard_ids": hazard_ids, "conflict_ids": conflict_ids,
                "usable_track_count": sum(t["usable"] for t in tracks),
                "note": "Software scaffold only; not a sensor-fusion or safety guarantee."}
