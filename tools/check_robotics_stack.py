#!/usr/bin/env python3
"""Report whether the local ROS 2 / Nav2 / Gazebo / Open3D stack is discoverable.

Run inside a shell where the chosen ROS 2 distribution has been sourced.
This is an environment preflight, not proof that robot drivers or missions work.
"""
from __future__ import annotations

import argparse
import importlib.util
import os
import shutil
import subprocess


def command_check(label: str, command: list[str]) -> bool:
    if shutil.which(command[0]) is None:
        print(f"MISSING  {label}: executable '{command[0]}' not found")
        return False
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=10, check=False
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"MISSING  {label}: {exc}")
        return False
    if result.returncode == 0:
        print(f"OK       {label}")
        return True
    detail = (result.stderr or result.stdout).strip().splitlines()
    suffix = f" ({detail[-1][:180]})" if detail else ""
    print(f"MISSING  {label}: command exited {result.returncode}{suffix}")
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return exit code 1 if any requested component is unavailable",
    )
    args = parser.parse_args()

    results: list[bool] = []
    distro = os.environ.get("ROS_DISTRO")
    if distro:
        print(f"ROS_DISTRO={distro}")
    else:
        print("MISSING  ROS_DISTRO environment variable (source the ROS setup file)")
        results.append(False)

    results.append(command_check("ROS 2 CLI", ["ros2", "--help"]))
    for package in ("nav2_bringup", "navigation2", "ros_gz_sim", "ros_gz_bridge"):
        results.append(
            command_check(f"ROS package {package}", ["ros2", "pkg", "prefix", package])
        )
    results.append(command_check("Gazebo Sim CLI", ["gz", "sim", "--help"]))

    if importlib.util.find_spec("open3d") is not None:
        try:
            import open3d
            print(f"OK       Open3D Python import (version {open3d.__version__})")
            results.append(True)
        except Exception as exc:
            print(f"MISSING  Open3D import failed: {exc}")
            results.append(False)
    else:
        print("MISSING  Open3D Python module (import name: open3d)")
        results.append(False)

    missing = sum(not result for result in results)
    print(f"\nPreflight: {len(results) - missing}/{len(results)} checks available.")
    print("This does not test hardware drivers, TF correctness, motion safety, or mission success.")
    return 1 if args.strict and missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
