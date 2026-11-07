#!/usr/bin/env python3
"""Build PUI89 evidence-led project health reports. Python standard library only."""
import json, os, re, subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"docs/project-progress.json"; README=ROOT/"README.md"
HISTORY=ROOT/"docs/project-progress-history.json"; LATEST=ROOT/"docs/project-health-latest.json"
CORE=ROOT/"docs/shared-ai-core-integration.json"
START="<!-- PUI89_DAILY_PROGRESS:START -->"; END="<!-- PUI89_DAILY_PROGRESS:END -->"
PATTERNS=[re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY-----"),re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),re.compile(r"\bAKIA[0-9A-Z]{16}\b")]
SUFFIXES={".py",".js",".ts",".tsx",".jsx",".json",".yml",".yaml",".toml",".ini",".cfg",".sh",".env",".md"}
SKIP={".git",".venv","venv","node_modules","dist","build","__pycache__"}
def readj(p,d): return json.loads(p.read_text(encoding="utf-8")) if p.exists() else d
def tracked():
    try: return [ROOT/x.decode("utf-8") for x in subprocess.check_output(["git","ls-files","-z"],cwd=ROOT).split(b"\0") if x]
    except Exception: return [p for p in ROOT.rglob("*") if p.is_file() and not any(x in SKIP for x in p.parts)]
def audit():
    hits=[]; manifests=[]; workflows=[]
    names={"requirements.txt","pyproject.toml","poetry.lock","uv.lock","package-lock.json","pnpm-lock.yaml","yarn.lock","Cargo.lock","go.sum"}
    for p in tracked():
        if not p.is_file() or any(x in SKIP for x in p.parts): continue
        rel=p.relative_to(ROOT).as_posix()
        if p.name in names: manifests.append(rel)
        if ".github/workflows" in p.as_posix(): workflows.append(rel)
        if p.suffix.lower() not in SUFFIXES or p.stat().st_size>1000000: continue
        try: s=p.read_text(encoding="utf-8",errors="ignore")
        except OSError: continue
        if any(rx.search(s) for rx in PATTERNS): hits.append(rel)
    return {"secret_pattern_findings":sorted(set(hits)),"dependency_manifests":sorted(set(manifests)),"workflow_files":sorted(set(workflows)),"license_file_present":any((ROOT/n).exists() for n in ("LICENSE","LICENSE.md","LICENSE.txt","COPYING")),"security_policy_present":(ROOT/".github/SECURITY.md").exists() or (ROOT/"SECURITY.md").exists(),"scope":"Limited high-confidence text-pattern and file-presence checks; not a full secret scanner, dependency vulnerability audit, licence opinion, branch-ruleset audit or penetration test."}
def main():
    cfg=readj(DATA,{}); weights=cfg.get("gate_weights",[]); credits=cfg.get("evidence_credit",[]); gates=cfg.get("gate_names",[])
    if not weights or len(weights)!=len(credits) or len(weights)!=len(gates) or any(not isinstance(c,int) or c<0 or c>w for c,w in zip(credits,weights)): raise SystemExit("Invalid project-progress.json gate definitions or evidence credits.")
    tz=cfg.get("review_timezone","Asia/Bangkok"); now=datetime.now(ZoneInfo(tz)); cadence=os.getenv("PUI89_CADENCE","manual")
    score=sum(credits); possible=sum(weights); pct=round(score/possible*100); coverage=round(sum(c>0 for c in credits)/len(credits)*100)
    confidence="High" if coverage>=75 else "Medium" if coverage>=50 else "Low"
    colour,stage=("🟢","Advanced evidence stage") if pct>=75 else ("🟡","Developing evidence stage") if pct>=50 else ("🟠","Foundation and prototype stage") if pct>=25 else ("🔴","Early foundation stage")
    bar="🟦"*round(pct/5)+"⬜"*(20-round(pct/5))
    rows="\n".join(f"| {g} | {c}/{w} | {'🟩'*c}{'⬜'*(w-c)} |" for g,c,w in zip(gates,credits,weights))
    core=readj(CORE,{"items":[]}); items=core.get("items",[])
    verified=sum(1 for x in items if x.get("status")=="verified" and x.get("evidence_ref")); corepct=round(verified/len(items)*100) if items else 0
    security=audit(); history=readj(HISTORY,[]); today=now.date().isoformat()
    point={"date":today,"timestamp":now.isoformat(),"cadence":cadence,"score":score,"score_percent":pct,"evidence_coverage_percent":coverage,"evidence_confidence_proxy":confidence,"shared_ai_core_integration_percent":corepct}
    if history and history[-1].get("date")==today: history[-1]=point
    else: history.append(point)
    HISTORY.parent.mkdir(parents=True,exist_ok=True); HISTORY.write_text(json.dumps(history,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    months={}
    for x in history: months[x["date"][:7]]=x
    monthly=sorted(months.items())[-12:]
    monthrows="\n".join(f"| {m} | {v['score_percent']}% | {'🟦'*round(v['score_percent']/5)}{'⬜'*(20-round(v['score_percent']/5))} |" for m,v in monthly) or "| No monthly history yet | — | — |"
    low=min(range(len(credits)),key=lambda i:credits[i]/weights[i]); milestone=f"Add traceable, reproducible evidence for: {gates[low]}."
    latest={"project":cfg.get("project",ROOT.name),"review_date":today,"review_timezone":tz,"cadence":cadence,"progress_percent":pct,"evidence_score":score,"evidence_possible":possible,"evidence_coverage_percent":coverage,"evidence_confidence_proxy":confidence,"shared_ai_core_integration_percent":corepct,"shared_ai_core_verified_items":verified,"shared_ai_core_total_items":len(items),"next_milestone":milestone,"security_review":security,"limitations":["Confidence is a coverage-derived proxy, not statistical confidence.","Static checks do not replace security alerts, dependency audits, human licence review, threat modelling or penetration testing.","Scores do not increase with elapsed time; evidence credits require deliberate review."]}
    LATEST.write_text(json.dumps(latest,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    riskline=("🔴 Secret-like high-confidence pattern found in: "+", ".join(security["secret_pattern_findings"])) if security["secret_pattern_findings"] else "🟢 No high-confidence private-key, GitHub-token or AWS-access-key patterns detected by this limited scan."
    section=f"""{START}
## PUI89 project intelligence dashboard

**{colour} {pct}% — {stage}** · **Evidence score:** {score}/{possible}  
**Evidence coverage:** {coverage}% of readiness gates have non-zero credits · **Coverage-derived confidence:** {confidence}  
**Review:** {now.strftime('%d %B %Y %H:%M')} ({tz}) · **Cycle:** {cadence.title()}  
**Progress:** {bar} {pct}%

This is an evidence-weighted readiness estimate, not code completion, product certification, field validation or commercial performance. Scores do not increase with time. Credits change only after human review of traceable evidence.

| Readiness gate | Evidence credit | Visual score |
|---|---:|---|
{rows}
| **Total** | **{score}/{possible}** | **{bar}** |

### Monthly history (latest snapshot per month)
| Month | Score | Graph |
|---|---:|---|
{monthrows}

### Shared AI Core integration
**{corepct}% verified** ({verified}/{len(items)} integration controls). Only controls marked verified with a supporting evidence_ref count. See docs/shared-ai-core-integration.json.

### Security and repository health
{riskline}

- Licence file: {"present" if security["license_file_present"] else "not detected"}
- Security policy: {"present" if security["security_policy_present"] else "not detected"}
- Dependency manifests: {len(security["dependency_manifests"])} detected
- Workflow files: {len(security["workflow_files"])} detected
- Review details: docs/project-health-latest.json

**Next milestone:** {milestone}

**Limitations:** This automated check is a first-line repository review, not a complete security audit, licence opinion, dependency vulnerability scan, branch-ruleset verification or physical safety validation. Software tests and simulations do not establish a built, certified or field-tested robot.

{END}"""
    readme=README.read_text(encoding="utf-8")
    readme=(readme.split(START,1)[0]+section+readme.split(END,1)[1]) if START in readme and END in readme else readme.rstrip()+"\n\n"+section+"\n"
    README.write_text(readme,encoding="utf-8")
if __name__=="__main__": main()
