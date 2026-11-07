"""PUI89 AI Security Gateway v1 — dependency-free advisory policy checks.

This module inspects text and proposed tool calls. It never executes tools, calls
models, sends network requests, stores raw content, or authorizes physical action.
It is a deterministic baseline, not a complete prompt-injection or malware defence.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import re
from typing import Iterable

VERSION = "1.0.0"
DEFAULT_MAX_CHARS = 12_000

# High-confidence indicators only. These rules are intentionally transparent and
# conservative; they are not a substitute for model-aware or human review.
_INJECTION_PATTERNS = (
    re.compile(r"ignore (?:all |any |the )?(?:previous|prior|above) instructions", re.I),
    re.compile(r"reveal (?:the )?(?:system|developer) prompt", re.I),
    re.compile(r"show (?:me )?(?:all )?(?:secrets|credentials|api keys|tokens)", re.I),
    re.compile(r"exfiltrat(?:e|ion).{0,80}(?:secret|credential|token|key)", re.I),
    re.compile(r"override (?:the )?(?:safety|security) (?:rules|policy|gate)", re.I),
    re.compile(r"disable (?:all )?(?:security|safety) checks", re.I),
)
_SECRET_PATTERNS = (
    ("private_key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("github_fine_grained_token", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("aws_access_key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("generic_api_key_assignment", re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|secret)\s*[:=]\s*['\"]?[A-Za-z0-9_./+=-]{16,}"
    )),
)
_HIGH_IMPACT_TOOL_WORDS = (
    "delete", "remove", "purge", "format", "shutdown", "reboot",
    "transfer", "payment", "purchase", "send_email", "publish",
    "deploy", "merge", "write_file", "shell", "terminal", "execute",
    "actuator", "motor", "brake", "steering", "throttle", "unlock",
)


@dataclass(frozen=True)
class GatewayDecision:
    decision: str
    reasons: tuple[str, ...]
    content_sha256: str
    content_length: int
    gateway_version: str = VERSION
    raw_content_logged: bool = False
    tool_execution_performed: bool = False
    physical_actuation_permitted: bool = False

    def to_dict(self) -> dict:
        result = asdict(self)
        result["reasons"] = list(self.reasons)
        return result


def _decision(text: str, decision: str, reasons: Iterable[str]) -> GatewayDecision:
    encoded = text.encode("utf-8", errors="replace")
    return GatewayDecision(
        decision=decision,
        reasons=tuple(sorted(set(reasons))),
        content_sha256=sha256(encoded).hexdigest(),
        content_length=len(text),
    )


def inspect_text(text: object, *, direction: str = "input",
                 max_chars: int = DEFAULT_MAX_CHARS) -> GatewayDecision:
    """Inspect untrusted input/output. Invalid or oversized content fails closed."""
    if direction not in {"input", "output"}:
        raise ValueError("direction must be 'input' or 'output'")
    if not isinstance(max_chars, int) or isinstance(max_chars, bool) or max_chars < 1:
        raise ValueError("max_chars must be a positive integer")
    if not isinstance(text, str):
        return _decision("", "BLOCK", ["invalid_content_type"])
    if len(text) > max_chars:
        return _decision(text, "BLOCK", ["content_limit_exceeded"])
    if not text.strip():
        return _decision(text, "REVIEW", ["empty_content"])

    reasons = []
    for name, pattern in _SECRET_PATTERNS:
        if pattern.search(text):
            reasons.append("sensitive_data_detected:" + name)

    if direction == "input":
        for index, pattern in enumerate(_INJECTION_PATTERNS, start=1):
            if pattern.search(text):
                reasons.append(f"prompt_injection_indicator:{index}")

    if any(reason.startswith("sensitive_data_detected:") for reason in reasons):
        return _decision(text, "BLOCK", reasons)
    if reasons:
        return _decision(text, "REVIEW", reasons)
    return _decision(text, "ALLOW", ["no_configured_rule_triggered"])


def inspect_tool_call(tool_name: object, arguments: object, *,
                      allowed_tools: Iterable[str] = ()) -> GatewayDecision:
    """Check a proposed tool call against an explicit allowlist; never executes it."""
    if not isinstance(tool_name, str) or not tool_name.strip():
        return _decision("", "BLOCK", ["invalid_tool_name"])
    if not isinstance(arguments, str):
        return _decision("", "BLOCK", ["tool_arguments_must_be_text"])
    payload = tool_name + "\n" + arguments
    if len(payload) > DEFAULT_MAX_CHARS:
        return _decision(payload, "BLOCK", ["content_limit_exceeded"])

    allowed = set(allowed_tools)
    if tool_name not in allowed:
        return _decision(payload, "BLOCK", ["tool_not_explicitly_allowlisted"])

    lowered = tool_name.lower()
    if any(word in lowered for word in _HIGH_IMPACT_TOOL_WORDS):
        return _decision(payload, "REVIEW", ["high_impact_tool_requires_human_approval"])

    content_check = inspect_text(arguments, direction="input")
    if content_check.decision != "ALLOW":
        return _decision(payload, content_check.decision,
                         ["tool_arguments_" + reason for reason in content_check.reasons])
    return _decision(payload, "REVIEW", ["allowlisted_tool_call_still_requires_caller_authorization"])


def inspect_exchange(prompt: object, response: object, *,
                     max_chars: int = DEFAULT_MAX_CHARS) -> dict:
    """Return separate input/output decisions; never infer that output is truthful."""
    return {
        "input": inspect_text(prompt, direction="input", max_chars=max_chars).to_dict(),
        "output": inspect_text(response, direction="output", max_chars=max_chars).to_dict(),
        "limitations": [
            "Pattern checks can miss novel or obfuscated attacks and can produce false positives.",
            "No model, tool, network request, file operation, or physical actuator was executed.",
            "ALLOW means only that configured deterministic checks did not trigger.",
            "Human authorization and downstream least-privilege controls remain mandatory.",
        ],
    }
