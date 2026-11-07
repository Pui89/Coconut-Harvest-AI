#!/usr/bin/env python3
"""PUI89 zero-cost, read-only repository security baseline audit.

Scans tracked files only. Never prints secret values and never modifies files.
Uses Python standard library and Git; installs no packages and calls no APIs.
"""
from __future__ import annotations
import os
import re
import subprocess
import sys
from pathlib import Path

MAX_FILE_BYTES = 2 * 1024 * 1024
SECRET_PATTERNS = [
    ("private-key", re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("AWS-access-key", re.compile(rb"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub-token", re.compile(rb"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("GitHub-fine-grained-token", re.compile(rb"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("Slack-token", re.compile(rb"\bxox[baprs]-[A-Za-z0-9-]{10,}\b")),
    ("Stripe-live-secret", re.compile(rb"\bsk_live_[A-Za-z0-9]{16,}\b")),
]
SAFE_ENV_NAMES = {".env.example", ".env.sample", ".env.template", ".env.dist"}
MANIFEST_NAMES = {
    "pyproject.toml", "requirements.txt", "Pipfile", "poetry.lock", "uv.lock",
    "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock",
    "Cargo.toml", "Cargo.lock", "go.mod", "go.sum", "pom.xml", "build.gradle",
    "Gemfile", "Gemfile.lock",
}

def tracked_files() -> list[str]:
    result = subprocess.run(["git", "ls-files", "-z"], check=True, stdout=subprocess.PIPE)
    return [p.decode("utf-8", "replace") for p in result.stdout.split(b"\0") if p]

def main() -> int:
    files = tracked_files()
    findings: list[str] = []
    warnings: list[str] = []
    manifests: set[str] = set()
    scanned = 0
    skipped = 0
    workflow_files: list[Path] = []

    for name in files:
        path = Path(name)
        base = path.name
        if base in MANIFEST_NAMES or (base.startswith("requirements") and base.endswith(".txt")):
            manifests.add(name)
        if ".github/workflows" in path.as_posix() and path.suffix.lower() in {".yml", ".yaml"}:
            workflow_files.append(path)
        if ((base.startswith(".env") and base not in SAFE_ENV_NAMES)
                or path.suffix.lower() in {".pem", ".p12", ".pfx"}):
            findings.append(f"Sensitive-looking tracked file: {name}")
        try:
            if not path.is_file() or path.stat().st_size > MAX_FILE_BYTES:
                skipped += 1
                continue
            data = path.read_bytes()
            if b"\0" in data:
                skipped += 1
                continue
        except OSError:
            skipped += 1
            continue
        scanned += 1
        for label, pattern in SECRET_PATTERNS:
            match = pattern.search(data)
            if match:
                line = data.count(b"\n", 0, match.start()) + 1
                findings.append(f"Possible {label} in {name}:{line}")

    for wf in workflow_files:
        try:
            content = wf.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if "pull_request_target" in content:
            warnings.append(f"Review privileged pull_request_target trigger: {wf}")
        if re.search(r"(?m)^\s*permissions:\s*write-all\s*$", content):
            warnings.append(f"Workflow grants write-all permissions: {wf}")
        if not re.search(r"(?m)^\s*permissions\s*:", content):
            warnings.append(f"Workflow has no explicit permissions block: {wf}")
        for line_no, line in enumerate(content.splitlines(), 1):
            match = re.search(r"^\s*uses:\s*([^\s#]+)", line)
            if match and not re.search(r"@[0-9a-fA-F]{40}$", match.group(1)):
                warnings.append(f"Action is not pinned to a full commit SHA: {wf}:{line_no}")

    summary = [
        "# PUI89 Repository Security Audit", "",
        f"- Tracked files discovered: {len(files)}",
        f"- Text files scanned: {scanned}",
        f"- Files skipped (binary, missing, or over 2 MiB): {skipped}",
        f"- Dependency/build manifests detected: {len(manifests)}",
        "- Dependency installation: not performed",
        "- External API/network calls by this audit script: none", "",
    ]
    if manifests:
        summary += ["## Detected manifests"] + [f"- {m}" for m in sorted(manifests)] + [""]
    if findings:
        summary += ["## Findings requiring human review", ""] + [f"- {x}" for x in sorted(set(findings))] + [""]
    else:
        summary += ["## Findings", "", "No high-confidence secret patterns or sensitive-looking tracked filenames were detected by this limited scan.", ""]
    if warnings:
        summary += ["## Workflow hardening warnings", ""] + [f"- {x}" for x in sorted(set(warnings))] + [""]
    else:
        summary += ["## Workflow hardening", "", "No warnings detected by the basic workflow checks.", ""]
    summary += [
        "## Limitations", "",
        "This is a lightweight baseline, not a penetration test, malware scanner, complete secret scanner, or proof that the repository is secure. Review findings manually. Rotate any exposed credential immediately; deleting it from the latest commit alone does not revoke it.",
    ]
    report = "\n".join(summary) + "\n"
    print(report)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as handle:
            handle.write(report)
    return 1 if findings else 0

if __name__ == "__main__":
    sys.exit(main())
