#!/usr/bin/env python3
"""Read-only PUI89 portfolio monitor for the four public project repositories.

Uses only Python's standard library and GitHub's public REST API. It does not
change repositories, merge pull requests, deploy software, or infer AI readiness.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPOSITORIES = (
    "Pui89/Coconut-Harvest-AI",
    "Pui89/Extreme-Flood-Rescue-AI",
    "Pui89/Multimodal-Narcotics-Screening-AI",
    "Pui89/Homeguard-Ai-Nomad",
)
API = "https://api.github.com"


def get_json(path: str):
    request = urllib.request.Request(
        API + path,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "PUI89-Portfolio-Monitor",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


def monitor(repo: str) -> dict:
    result = {"repository": repo, "checked_at_utc": datetime.now(timezone.utc).isoformat()}
    errors = []
    try:
        meta = get_json(f"/repos/{repo}")
        result["default_branch"] = meta.get("default_branch")
        result["private"] = meta.get("private")
        result["archived"] = meta.get("archived")
        result["updated_at"] = meta.get("updated_at")
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        errors.append(f"repository metadata: {exc}")

    try:
        runs = get_json(f"/repos/{repo}/actions/runs?per_page=20").get("workflow_runs", [])
        result["workflow_runs"] = [
            {
                "name": run.get("name"),
                "branch": run.get("head_branch"),
                "status": run.get("status"),
                "conclusion": run.get("conclusion"),
                "created_at": run.get("created_at"),
                "url": run.get("html_url"),
            }
            for run in runs[:10]
        ]
        # Ignore GitHub's Dependabot dynamic-update runs: they are dependency
        # maintenance jobs, not evidence that a PUI89 project verification ran.
        project_runs = [
            run for run in runs
            if run.get("event") in {"push", "pull_request", "workflow_dispatch", "schedule"}
            and not str(run.get("path", "")).startswith("dynamic/dependabot/")
        ]
        completed = [
            run for run in project_runs
            if run.get("status") == "completed"
            and run.get("conclusion") not in ("cancelled", "skipped")
        ]
        result["recent_project_workflow_count"] = len(project_runs)
        result["recent_project_workflow_failures"] = sum(
            run.get("status") == "completed" and run.get("conclusion") == "failure"
            for run in project_runs
        )
        result["latest_completed_check"] = (
            {key: completed[0].get(key) for key in
             ("name", "head_branch", "conclusion", "created_at", "html_url", "event", "path")}
            if completed else None
        )
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        errors.append(f"workflow runs: {exc}")

    try:
        prs = get_json(f"/repos/{repo}/pulls?state=open&per_page=100")
        result["open_pull_request_count"] = len(prs)
        result["open_pull_requests"] = [
            {"number": pr.get("number"), "title": pr.get("title"),
             "branch": pr.get("head", {}).get("ref"),
             "url": pr.get("html_url")}
            for pr in prs
        ]
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        errors.append(f"open pull requests: {exc}")

    result["monitor_status"] = "PARTIAL" if errors else "READ_ONLY_SNAPSHOT"
    result["errors"] = errors
    result["limitations"] = [
        "This is a read-only public GitHub snapshot, not a live runtime monitor.",
        "Workflow success verifies only the checks actually executed.",
        "It does not establish model accuracy, dataset suitability, simulation validity, or physical robot safety.",
        "A cancelled or skipped workflow is not counted as a failed check.",
    ]
    return result


def main() -> int:
    reports = [monitor(repo) for repo in REPOSITORIES]
    payload = {
        "schema_version": "1.0",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "monitor_type": "read_only_public_github_portfolio_snapshot",
        "projects": reports,
    }
    out = Path(os.environ.get("PUI89_REPORT_DIR", "portfolio-status"))
    out.mkdir(parents=True, exist_ok=True)
    (out / "portfolio-status.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    lines = [
        "# PUI89 Portfolio Status",
        "",
        f"Generated: {payload['generated_at_utc']}",
        "",
        "> Read-only snapshot of public GitHub metadata. This is not evidence of AI or robot performance.",
        "",
    ]
    for item in reports:
        lines += [f"## {item['repository']}", ""]
        lines += [
            f"- Monitor: **{item['monitor_status']}**",
            f"- Default branch: `{item.get('default_branch', 'UNKNOWN')}`",
            f"- Open pull requests: **{item.get('open_pull_request_count', 'UNKNOWN')}**",
        ]
        latest = item.get("latest_completed_check")
        if latest:
            lines.append(
                f"- Latest completed project CI workflow: **{latest.get('conclusion', 'UNKNOWN')}** "
                f"({latest.get('name')}, {latest.get('head_branch')}) — {latest.get('html_url')}"
            )
        else:
            lines.append("- Latest completed project CI workflow: **NOT FOUND**")
        lines.append(
            f"- Recent project workflow failures (up to 20 fetched runs): "
            f"**{item.get('recent_project_workflow_failures', 'UNKNOWN')}**"
        )
        if item["errors"]:
            lines += ["- Retrieval issues: " + "; ".join(item["errors"])]
        if item.get("open_pull_requests"):
            lines.append("- Open PRs:")
            lines.extend(
                f"  - [#{pr['number']} {pr['title']}]({pr['url']}) — `{pr['branch']}`"
                for pr in item["open_pull_requests"]
            )
        lines.append("")
    lines += [
        "## Evidence boundary",
        "",
        "- GitHub Actions results describe only the automated checks that ran.",
        "- No model accuracy, field performance, simulation fidelity, or physical safety is inferred.",
        "- The monitor does not write to project repositories, merge PRs, deploy, or trigger hardware.",
        "",
    ]
    (out / "portfolio-status.md").write_text("\n".join(lines), encoding="utf-8")
    partial = any(item["monitor_status"] == "PARTIAL" for item in reports)
    print(json.dumps({
        "projects_checked": len(reports),
        "partial_results": sum(item["monitor_status"] == "PARTIAL" for item in reports),
        "output_directory": str(out),
    }, indent=2))
    return 1 if partial else 0


if __name__ == "__main__":
    sys.exit(main())
