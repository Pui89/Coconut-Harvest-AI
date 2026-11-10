#!/usr/bin/env python3
"""Dependency-free PUI89 repository hygiene check. No network access; never prints secret values."""
from __future__ import annotations
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SENSITIVE_NAMES = re.compile(r"(^|/)(\.env(?:\..*)?|id_rsa|id_ed25519|.*\.(?:pem|p12|pfx|key))$", re.I)
ALLOW_NAME = {".env.example", ".env.template", ".env.sample"}
TEXT_SUFFIXES = {".py", ".yml", ".yaml", ".json", ".toml", ".ini", ".cfg", ".md", ".txt", ".sh", ".bat", ".ps1", ".js", ".ts", ".html", ".css"}
PATTERNS = [
    ("GitHub token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private key material", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("likely populated API key assignment", re.compile(r"(?i)\b(?:OPENAI_API_KEY|ANTHROPIC_API_KEY|AWS_SECRET_ACCESS_KEY|SECRET_KEY|ACCESS_TOKEN)\s*[:=]\s*['\"]?([A-Za-z0-9_\-/+=]{20,})")),
]

def main() -> int:
    try:
        raw = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ERROR: git is required to enumerate tracked files.")
        return 2
    files = [p.decode("utf-8", "surrogateescape") for p in raw.split(b"\0") if p]
    if not files:
        print("ERROR: no tracked files found; run inside a Git checkout.")
        return 2
    findings = []
    for rel in files:
        path = Path(rel)
        if path.name in ALLOW_NAME:
            continue
        if SENSITIVE_NAMES.search(rel):
            findings.append(f"{rel}: sensitive filename is tracked")
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            full = ROOT / path
            if full.stat().st_size > 1_000_000:
                continue
            content = full.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for label, pattern in PATTERNS:
            if pattern.search(content):
                findings.append(f"{rel}: possible {label} detected (value suppressed)")
                break
    if findings:
        print("PUI89 SECURITY CHECK: FAIL")
        for item in findings:
            print(f"- {item}")
        print("Remove exposed material, rotate any real credential from a clean device, and review Git history.")
        return 1
    print(f"PUI89 SECURITY CHECK: PASS ({len(files)} tracked paths inspected; no network or extra packages)")
    return 0

if __name__ == "__main__":
    sys.exit(main())
