"""Model-agnostic contracts for vision-language observations and action plans.

This module does not load an LLM/VLM, call an API, or control hardware. It
validates structured outputs so a future model adapter can be tested safely.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class VisionFinding:
    """A model-proposed observation with provenance and calibrated-range confidence."""
    label: str
    confidence: float
    source_id: str
    bbox_xyxy: tuple[float, float, float, float] | None = None
    notes: str = ""


@dataclass(frozen=True)
class ActionStep:
    """A high-level proposed step; never a direct actuator command."""
    action: str
    parameters: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ActionPlan:
    """Structured plan proposed for independent validation before execution."""
    goal: str
    steps: tuple[ActionStep, ...]
    requires_human_review: bool = True
    rationale: str = ""


def validate_vision_finding(finding: VisionFinding) -> tuple[str, ...]:
    """Return validation issues; an empty tuple means the record is well-formed."""
    issues: list[str] = []
    if not finding.label.strip():
        issues.append("label must not be empty")
    if not finding.source_id.strip():
        issues.append("source_id/provenance must not be empty")
    if not math.isfinite(finding.confidence) or not 0.0 <= finding.confidence <= 1.0:
        issues.append("confidence must be finite and between 0 and 1")
    if finding.bbox_xyxy is not None:
        if len(finding.bbox_xyxy) != 4 or not all(math.isfinite(v) for v in finding.bbox_xyxy):
            issues.append("bbox_xyxy must contain four finite values")
        else:
            x1, y1, x2, y2 = finding.bbox_xyxy
            if not (0.0 <= x1 < x2 <= 1.0 and 0.0 <= y1 < y2 <= 1.0):
                issues.append("bbox_xyxy must be normalized to 0..1 with positive area")
    return tuple(issues)


def _is_json_safe(value: Any) -> bool:
    """Accept only finite JSON-like values, so arbitrary objects cannot pass through."""
    if value is None or isinstance(value, (str, bool, int)):
        return True
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, (list, tuple)):
        return all(_is_json_safe(item) for item in value)
    if isinstance(value, Mapping):
        return all(isinstance(key, str) and _is_json_safe(item) for key, item in value.items())
    return False


def validate_action_plan(
    plan: ActionPlan,
    allowed_actions: Sequence[str],
    max_steps: int = 12,
) -> tuple[str, ...]:
    """Check structure and allowlisted action names; this does not prove a plan is safe."""
    issues: list[str] = []
    allowed = set(allowed_actions)
    if not plan.goal.strip():
        issues.append("goal must not be empty")
    if not plan.steps:
        issues.append("plan must contain at least one step")
    if max_steps < 1 or len(plan.steps) > max_steps:
        issues.append(f"plan must contain between 1 and {max_steps} steps")
    if not plan.requires_human_review:
        issues.append("human review must remain enabled for this scaffold")
    for index, step in enumerate(plan.steps):
        if not step.action.strip():
            issues.append(f"step {index}: action must not be empty")
        elif step.action not in allowed:
            issues.append(f"step {index}: action is not allowlisted")
        if not _is_json_safe(step.parameters):
            issues.append(f"step {index}: parameters must contain only finite JSON-like values")
    return tuple(issues)
