#!/usr/bin/env python3
"""Dependency-free audit for PUI89's free-first advanced technology registry.

This checks registry integrity and governance only. It does not install packages,
download models, contact external services, run inference, certify safety, or
validate a physical robot.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
REGISTRY = ROOT / "pui89_technology_capabilities.json"
ALLOWED_STATUS = {"ROADMAP", "FOUNDATION", "PROTOTYPE", "VERIFIED", "BLOCKED"}
REQUIRED_POLICY = {
    "paid_apis_allowed": False,
    "subscriptions_allowed": False,
    "cloud_gpu_required": False,
    "automatic_model_downloads": False,
    "hardware_actuation_from_ci": False,
    "network_access_from_audit": False,
}

def audit_registry(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    if not data.get("project", {}).get("name"):
        errors.append("project.name is required")
    policy = data.get("execution_policy", {})
    for key, expected in REQUIRED_POLICY.items():
        if policy.get(key) is not expected:
            errors.append(f"execution_policy.{key} must be {expected}")
    if policy.get("local_first") is not True:
        errors.append("execution_policy.local_first must be true")
    if policy.get("dependency_installation_in_ci") is not False:
        errors.append("CI must not install project/model dependencies in this audit")
    capabilities = data.get("capabilities")
    if not isinstance(capabilities, list) or not capabilities:
        errors.append("capabilities must be a non-empty list")
        return errors
    seen: set[str] = set()
    for index, item in enumerate(capabilities):
        prefix = f"capabilities[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{prefix} must be an object")
            continue
        capability_id = item.get("id")
        if not isinstance(capability_id, str) or not capability_id:
            errors.append(f"{prefix}.id is required")
        elif capability_id in seen:
            errors.append(f"duplicate capability id: {capability_id}")
        else:
            seen.add(capability_id)
        if item.get("status") not in ALLOWED_STATUS:
            errors.append(f"{prefix}.status is invalid")
        if item.get("activation") != "DISABLED_BY_DEFAULT":
            errors.append(f"{prefix}.activation must remain DISABLED_BY_DEFAULT")
        if item.get("license_review") not in {"REQUIRED_BEFORE_ADOPTION", "APPROVED"}:
            errors.append(f"{prefix}.license_review must be explicit")
        evidence = item.get("implementation_evidence")
        if not isinstance(evidence, list):
            errors.append(f"{prefix}.implementation_evidence must be a list")
        elif item.get("status") == "VERIFIED" and not evidence:
            errors.append(f"{prefix}: VERIFIED requires evidence references")
    if not data.get("safety_boundary", {}).get("no_hardware_actuation"):
        errors.append("safety_boundary.no_hardware_actuation must be true")
    if not data.get("safety_boundary", {}).get("human_review_for_high_impact"):
        errors.append("safety_boundary.human_review_for_high_impact must be true")
    return errors

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--report", type=Path, default=ROOT / "pui89-technology-audit-report.json")
    args = parser.parse_args()
    try:
        data = json.loads(args.registry.read_text(encoding="utf-8"))
        errors = audit_registry(data)
    except Exception as exc:
        errors = [f"Could not read or parse registry: {type(exc).__name__}: {exc}"]
        data = {}
    report = {
        "audit": "PUI89 free-first advanced technology registry integrity",
        "project": data.get("project", {}).get("name", "UNKNOWN"),
        "status": "POLICY_CHECKS_PASSED" if not errors else "REVIEW_REQUIRED",
        "checks": "registry and governance integrity only",
        "capability_count": len(data.get("capabilities", [])) if isinstance(data.get("capabilities"), list) else 0,
        "errors": errors,
        "limitations": [
            "This audit does not prove that a capability is implemented.",
            "This audit does not install dependencies, download models, use paid services or access the network.",
            "This audit does not test model accuracy, physical safety, simulation fidelity or real-world performance.",
            "A ROADMAP status is a planned capability, not a delivered feature."
        ]
    }
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if not errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
