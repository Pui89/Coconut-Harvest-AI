#!/usr/bin/env python3
"""Fast, free-first PUI89 preflight shared by the three project repositories.

Default: standard-library-only Python syntax and repository-structure checks.
Optional: --pytest runs the installed pytest only; it never installs packages,
downloads models, calls hosted APIs, or controls hardware.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tokenize
from pathlib import Path

SKIP_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    "site-packages", "build", "dist", ".mypy_cache", ".pytest_cache",
}


def python_files(root: Path):
    for path in root.rglob("*.py"):
        relative = path.relative_to(root)
        if not any(part in SKIP_DIRS for part in relative.parts):
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(),
                        help="repository root (default: current directory)")
    parser.add_argument("--pytest", action="store_true",
                        help="run pytest if already installed; install nothing")
    parser.add_argument("--json", type=Path,
                        help="optional report path; otherwise print to stdout")
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        print(f"ERROR: root is not a directory: {root}", file=sys.stderr)
        return 2

    checks = []
    for name in ("README.md", "tests", ".github/workflows"):
        exists = (root / name).exists()
        checks.append({
            "check": f"required item: {name}",
            "status": "PASS" if exists else "WARN",
            "detail": "present" if exists else "missing",
        })

    files = sorted(python_files(root))
    errors = []
    for path in files:
        try:
            with tokenize.open(path) as stream:
                compile(stream.read(), str(path), "exec")
        except (SyntaxError, UnicodeDecodeError, OSError) as exc:
            errors.append({
                "file": str(path.relative_to(root)),
                "error": f"{type(exc).__name__}: {exc}",
            })
    checks.append({
        "check": "Python syntax",
        "status": "FAIL" if errors else "PASS",
        "detail": f"{len(files)} Python files scanned; {len(errors)} syntax/read errors",
        "errors": errors,
    })

    if args.pytest:
        try:
            import pytest  # noqa: F401
        except ImportError:
            checks.append({
                "check": "pytest suite",
                "status": "SKIP",
                "detail": "pytest is not installed; no packages were installed",
            })
        else:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "-q"],
                cwd=root,
                check=False,
            )
            checks.append({
                "check": "pytest suite",
                "status": "PASS" if result.returncode == 0 else "FAIL",
                "detail": f"pytest exit code {result.returncode}",
            })

    failed = any(item["status"] == "FAIL" for item in checks)
    report = {
        "tool": "PUI89 Fast Check",
        "root": str(root),
        "python": sys.version.split()[0],
        "checks": checks,
        "overall": "FAIL" if failed else "PASS",
        "limitations": [
            "Syntax success is not proof that tests or runtime behavior pass.",
            "Dataset licences, labels, model accuracy, and physical robot safety need separate verification.",
            "No code is automatically edited or repaired by this checker.",
        ],
    }
    output = json.dumps(report, indent=2, ensure_ascii=False)
    if args.json:
        target = args.json if args.json.is_absolute() else root / args.json
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output + "\n", encoding="utf-8")
    print(output)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
