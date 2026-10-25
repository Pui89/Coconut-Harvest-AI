#!/usr/bin/env python3
"""Report optional free/open-source tool availability without installing anything.

Uses only the Python standard library. It does not import optional AI packages,
contact the network, download model weights, or alter the machine.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import platform
import shutil
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Any

DEFAULT_CONFIG = Path(__file__).resolve().parents[1] / "config" / "optional_resources.json"


def _module_available(module_name: str) -> bool:
    """Check whether a top-level Python module has an import specification."""
    try:
        return importlib.util.find_spec(module_name) is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        return False


def _distribution_version(distribution_names: list[str]) -> str | None:
    """Return the first installed distribution version without importing it."""
    for distribution_name in distribution_names:
        try:
            return metadata.version(distribution_name)
        except metadata.PackageNotFoundError:
            continue
    return None


def probe_resource(resource: dict[str, Any]) -> dict[str, Any]:
    """Check one registry entry. Unknown check types fail clearly."""
    check_type = resource.get("check", "manual")
    status = "manual_check"
    version = None

    if check_type == "python_module":
        module_name = resource.get("module")
        if not isinstance(module_name, str) or not module_name:
            raise ValueError("python_module resources require a non-empty 'module'")
        if _module_available(module_name):
            status = "available"
            version = _distribution_version(resource.get("distributions", []))
        else:
            status = "not_installed"
    elif check_type == "command":
        command_name = resource.get("command")
        if not isinstance(command_name, str) or not command_name:
            raise ValueError("command resources require a non-empty 'command'")
        status = "available" if shutil.which(command_name) else "not_installed"
    elif check_type != "manual":
        raise ValueError(f"Unsupported check type: {check_type}")

    return {
        "id": resource.get("id", "unnamed"),
        "name": resource.get("name", "Unnamed resource"),
        "check": check_type,
        "status": status,
        "version": version,
        "priority": resource.get("priority", "optional"),
        "purpose": resource.get("purpose", ""),
        "license_note": resource.get("license_note", ""),
        "official_url": resource.get("official_url", ""),
        "limitation": resource.get("limitation", ""),
    }


def build_report(config_path: Path = DEFAULT_CONFIG) -> dict[str, Any]:
    """Build a privacy-conscious local report from the JSON resource registry."""
    with config_path.open("r", encoding="utf-8") as handle:
        config = json.load(handle)

    resources = config.get("resources")
    if not isinstance(resources, list):
        raise ValueError("Resource config must contain a 'resources' list")

    return {
        "schema_version": 1,
        "project": config.get("project", "PUI89"),
        "generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "environment": {
            "python": platform.python_version(),
            "implementation": platform.python_implementation(),
            "operating_system": platform.system(),
        },
        "network_access_used": False,
        "packages_installed": False,
        "models_downloaded": False,
        "resources": [probe_resource(item) for item in resources],
        "interpretation": (
            "Availability is a local presence check only. It does not verify model weights, "
            "version compatibility, licences of transitive dependencies, accuracy, or hardware readiness."
        ),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check optional resource availability without installing or downloading anything."
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="JSON resource registry")
    args = parser.parse_args(argv)
    report = build_report(args.config)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
