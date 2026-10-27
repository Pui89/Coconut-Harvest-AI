"""Minimal world-state records; no sensors or model dependencies required."""
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class TrackedObject:
    object_id: str
    label: str
    confidence: float
    attributes: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.object_id.strip():
            raise ValueError("object_id must not be empty")
        if not self.label.strip():
            raise ValueError("label must not be empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")


@dataclass
class WorldState:
    """Latest known objects and task status, suitable for JSON reporting."""
    objects: dict[str, TrackedObject] = field(default_factory=dict)
    task_status: str = "idle"
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def upsert(self, item: TrackedObject) -> None:
        self.objects[item.object_id] = item
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> dict[str, Any]:
        return {
            "objects": {key: asdict(value) for key, value in sorted(self.objects.items())},
            "task_status": self.task_status,
            "updated_at": self.updated_at,
        }
