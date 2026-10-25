"""Model-agnostic contracts for vision-language observations and action plans.

This module validates structured proposals only. It does not load models, call APIs,
execute plans, or control hardware.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class VisionFinding:
    """A proposed observation with source provenance and a confidence score."""
    label: str
    confidence: float
    source_id: str
    bbox_xyxy: tuple[float, float, float, float] | None = None
    notes: str = ""


@dataclass(frozen=True)
class ActionStep:
    """A high-level proposed step, never a direct actuator command."""
    action: str
    parameters: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ActionPlan:
    """Structured plan proposed for independent validation before any execution."""
    goal: str
    steps: tuple[ActionStep, ...]
    requires_human_review: bool = True
    rationale: str = ""


def _finite_number(value: Any) -> bool:
    """Reject booleans and non-numeric/non-finite values."""
    return not isinstance(value, bool) and isinstance(value, (int, float)) and math.isfinite(value)


def validate_vision_finding(finding: VisionFinding) -> tuple[str, ...]:
    """Return validation issues; an empty tuple means the record is well-formed."""
    issues: list[str] = []
    if not isinstance(finding.label, str) or not finding.label.strip():
        issues.append("label must not be empty")
    if not isinstance(finding.source_id, str) or not finding.source_id.strip():
        issues.append("source_id/provenance must not be empty")
    if not _finite_number(finding.confidence) or not 0.0 <= finding.confidence <= 1.0:
        issues.append("confidence must be a finite number between 0 and 1")
    if finding.bbox_xyxy is not None:
        box = finding.bbox_xyxy
        if (
            not isinstance(box, (tuple, list))
            or len(box) != 4
            or not all(_finite_number(value) for value in box)
        ):
            issues.append("bbox_xyxy must contain four finite numeric values")
        else:
            x1, y1, x2, y2 = box
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
    if not isinstance(plan.goal, str) or not plan.goal.strip():
        issues.append("goal must not be empty")
    if not isinstance(plan.steps, (tuple, list)):
        issues.append("steps must be a tuple or list of ActionStep records")
        steps = ()
    else:
        steps = plan.steps
    if not steps:
        issues.append("plan must contain at least one step")
    if isinstance(max_steps, bool) or not isinstance(max_steps, int) or max_steps < 1:
        issues.append("max_steps must be a positive integer")
    elif len(steps) > max_steps:
        issues.append(f"plan must contain no more than {max_steps} steps")
    if plan.requires_human_review is not True:
        issues.append("human review must remain enabled for this scaffold")
    allowed = set(item for item in allowed_actions if isinstance(item, str))
    for index, step in enumerate(steps):
        if not isinstance(step, ActionStep):
            issues.append(f"step {index}: must be an ActionStep record")
            continue
        if not isinstance(step.action, str) or not step.action.strip():
            issues.append(f"step {index}: action must not be empty")
        elif step.action not in allowed:
            issues.append(f"step {index}: action is not allowlisted")
        if not isinstance(step.parameters, Mapping) or not _is_json_safe(step.parameters):
            issues.append(f"step {index}: parameters must contain only finite JSON-like values")
    return tuple(issues)
