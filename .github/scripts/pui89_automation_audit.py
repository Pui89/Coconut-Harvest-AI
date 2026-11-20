#!/usr/bin/env python3
"""PUI89 dependency-free repository audit; static hygiene only."""
from __future__ import annotations
import argparse, json, os, re
from pathlib import Path
SKIP_DIRS={".git",".venv","venv","node_modules","__pycache__",".pytest_cache",".mypy_cache",".ruff_cache","dist","build","site-packages",".next",".tox",".idea",".vscode",".pui89-core"}
TEXT_SUFFIXES={".py",".md",".json",".yml",".yaml",".toml",".txt",".ini",".cfg",".sh"}
SECRET_PATTERNS=[re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),re.compile(r"\bAKIA[0-9A-Z]{16}\b"),re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{30,}\b")]
LINK_RE=re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
IMAGE_SUFFIXES={".png",".jpg",".jpeg",".gif",".svg",".webp",".avif"}
def iter_files(root):
    for current,dirs,names in os.walk(root,followlinks=False):
        dirs[:]=sorted(d for d in dirs if d not in SKIP_DIRS and not d.startswith(".git"))
        for name in sorted(names):
            p=Path(current)/name
            if not p.is_symlink(): yield p
def rel(path,root):
    try:return path.relative_to(root).as_posix()
    except ValueError:return str(path)
def audit(root):
    errors,warnings,info=[],[],[]
    if not (root/"README.md").is_file(): errors.append("Missing root README.md")
    files=list(iter_files(root)); py=[p for p in files if p.suffix.lower()==".py"]; js=[p for p in files if p.suffix.lower()==".json"]; md=[p for p in files if p.suffix.lower() in {".md",".markdown"}]
    info.extend([f"Files scanned: {len(files)}",f"Python files: {len(py)}",f"JSON files: {len(js)}",f"Markdown files: {len(md)}"])
    for p in py:
        try: compile(p.read_text(encoding="utf-8"),str(p),"exec")
        except UnicodeDecodeError: warnings.append(f"Python file is not UTF-8: {rel(p,root)}")
        except SyntaxError as e: errors.append(f"Python syntax error: {rel(p,root)}:{e.lineno}: {e.msg}")
        except OSError as e: warnings.append(f"Could not read {rel(p,root)}: {e}")
    for p in js:
        try:
            if "invalid" in p.stem.lower() or "malformed" in p.stem.lower():
                warnings.append(f"Intentional invalid/malformed JSON fixture skipped: {rel(p,root)}"); continue
            if p.stat().st_size>2_000_000: warnings.append(f"JSON skipped (>2 MB): {rel(p,root)}"); continue
            json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError,UnicodeDecodeError) as e: errors.append(f"Invalid JSON: {rel(p,root)}: {e}")
        except OSError as e: warnings.append(f"Could not read {rel(p,root)}: {e}")
    for p in md:
        try: body=p.read_text(encoding="utf-8")
        except (OSError,UnicodeDecodeError): warnings.append(f"Could not read Markdown: {rel(p,root)}"); continue
        seen=set()
        for raw in LINK_RE.findall(body):
            target=raw.strip().split()[0].strip("<>")
            if not target or target.startswith(("#","http://","https://","mailto:","data:")): continue
            target=target.split("#",1)[0].split("?",1)[0]
            if not target: continue
            if not (p.parent/target).resolve().exists(): warnings.append(f"Broken or unresolved local Markdown link (manual review): {rel(p,root)} -> {target}")
            elif Path(target).suffix.lower() in IMAGE_SUFFIXES:
                if target in seen: warnings.append(f"Repeated image reference in {rel(p,root)}: {target}")
                seen.add(target)
    for p in files:
        if p.suffix.lower() not in TEXT_SUFFIXES: continue
        try:
            if p.stat().st_size>1_000_000: continue
            body=p.read_text(encoding="utf-8",errors="ignore")
        except OSError: continue
        if any(rx.search(body) for rx in SECRET_PATTERNS): warnings.append(f"High-confidence secret pattern needs manual review: {rel(p,root)}")
    return {"root":str(root),"status":"FAIL" if errors else ("WARN" if warnings else "PASS"),"errors":sorted(set(errors)),"warnings":sorted(set(warnings)),"info":info}
def render(r):
    lines=[f"## PUI89 repository audit — {r['status']}","",f"Repository path: {r['root']}",""]+[f"- {x}" for x in r["info"]]+["",f"- Errors: {len(r['errors'])}",f"- Warnings: {len(r['warnings'])}"]
    if r["errors"]: lines+=["","### Errors"]+[f"- {x}" for x in r["errors"]]
    if r["warnings"]: lines+=["","### Warnings"]+[f"- {x}" for x in r["warnings"]]
    lines+=["","Static repository hygiene only; not a security audit, licence opinion, model evaluation, safety validation or proof of product readiness."]
    return "\n".join(lines)+"\n"
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root",default="."); ap.add_argument("--json-out"); ap.add_argument("--summary"); a=ap.parse_args()
    root=Path(a.root).resolve(); report=audit(root); output=render(report); print(output)
    if a.json_out: Path(a.json_out).write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    if a.summary:
        with Path(a.summary).open("a",encoding="utf-8") as f:f.write(output+"\n")
    return 1 if report["errors"] else 0
if __name__=="__main__": raise SystemExit(main())
