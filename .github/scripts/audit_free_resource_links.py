#!/usr/bin/env python3
"""Prune curated resource-table rows only after three consecutive failed checks."""
import json, os, re
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

STATE = Path(".github/link-audit-state.json")
REPORT = Path("FREE_RESOURCE_LINK_AUDIT.md")
TARGETS = [Path(p) for p in os.environ.get("LINK_AUDIT_FILES", "").splitlines() if p.strip()]
URL_RE = re.compile(r"https?://[^\s\]\)<>|]+", re.I)
THRESHOLD = 3
TIMEOUT = 10

def check(url):
    url = url.rstrip(".,;:")
    for method in ("HEAD", "GET"):
        try:
            req = Request(url, method=method, headers={"User-Agent": "PUI89-Free-Resource-Audit/1.0"})
            with urlopen(req, timeout=TIMEOUT) as response:
                return response.status < 400, "HTTP " + str(response.status)
        except HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 501):
                continue
            return False, "HTTP " + str(e.code)
        except (URLError, TimeoutError, OSError) as e:
            if method == "HEAD":
                continue
            return False, type(e).__name__
    return False, "request failed"

def main():
    STATE.parent.mkdir(parents=True, exist_ok=True)
    try:
        state = json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        state = {}
    failures = state.get("failures", {})
    cache = {}
    checked = datetime.now(timezone.utc).isoformat(timespec="seconds")
    findings, removals = [], []
    changed_rows = 0

    for path in TARGETS:
        if not path.exists():
            continue
        old = path.read_text(encoding="utf-8")
        kept = []
        for line_no, line in enumerate(old.splitlines(keepends=True), 1):
            dead = []
            for raw in dict.fromkeys(URL_RE.findall(line)):
                url = raw.rstrip(".,;:")
                if url not in cache:
                    cache[url] = check(url)
                ok, reason = cache[url]
                key = path.as_posix() + "|" + url
                if ok:
                    failures.pop(key, None)
                    continue
                item = failures.get(key, {"count": 0})
                item["count"] = int(item.get("count", 0)) + 1
                item["reason"] = reason
                item["last_failed_at"] = checked
                failures[key] = item
                findings.append("- " + path.as_posix() + ":" + str(line_no) + " — " + url + " — " + reason + " — consecutive failures: " + str(item["count"]))
                if item["count"] >= THRESHOLD and line.lstrip().startswith("|") and "|" in line:
                    dead.append((url, key))
            if dead:
                removals.append("- Removed a resource row from " + path.as_posix() + " after three consecutive failures: " + ", ".join(u for u, _ in dead))
                for _, key in dead:
                    failures.pop(key, None)
                changed_rows += 1
            else:
                kept.append(line)
        new = "".join(kept)
        if new != old:
            path.write_text(new, encoding="utf-8")

    state = {"failures": failures, "last_checked": checked}
    STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report = [
        "# Free Resource Link Audit", "",
        "Last checked: " + checked, "",
        "This scheduled audit checks only the curated Markdown resource files configured in the workflow. A resource row is removed only after three consecutive failed checks, to reduce false removals caused by temporary outages or rate limits.", "",
        "## Removed rows", "", *(removals or ["- None this run."]), "",
        "## Failing links under review", "", *(findings or ["- No failing links detected this run."]), "",
        "## Safety limits", "",
        "- Only rows in Markdown tables in configured resource catalogues/guides can be removed.",
        "- Never deletes code, tests, datasets, project evidence, entire files, or repository history.",
        "- This is a URL response check, not a pricing, licence, uptime, or commercial-use guarantee.",
        "- Free tiers and commercial licences still require separate review.", ""
    ]
    REPORT.write_text("\n".join(report), encoding="utf-8")
    print("Audited", len(TARGETS), "files; removed", changed_rows, "rows; failing-link findings:", len(findings))

if __name__ == "__main__":
    main()
