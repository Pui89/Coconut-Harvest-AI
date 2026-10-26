#!/usr/bin/env python3
"""Audit curated free-resource rows for dead links and explicit paid-upgrade gates."""
import html, json, os, re
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

STATE = Path(".github/link-audit-state.json")
REPORT = Path("FREE_RESOURCE_LINK_AUDIT.md")
TARGETS = [Path(p) for p in os.environ.get("LINK_AUDIT_FILES", "").splitlines() if p.strip()]
URL_RE = re.compile(r"https?://[^\s\]\)<>|]+", re.I)
THRESHOLD = 3
TIMEOUT = 12
# Conservative signals: a generic "pricing" page alone is not enough.
PAID_PATTERNS = [
    re.compile(r"\bupgrade\s+to\s+(?:the\s+)?(?:pro|premium|paid|business|enterprise)\b", re.I),
    re.compile(r"\b(?:paid|premium|pro)\s+(?:plan|tier|subscription|monitoring|features?)\b", re.I),
    re.compile(r"\bsubscription\s+required\b", re.I),
    re.compile(r"\bupgrade\s+(?:your|to\s+the)\s+plan\b", re.I),
    re.compile(r"\bbuy\s+(?:more\s+)?credits\b", re.I),
    re.compile(r"\bpurchase\s+(?:more\s+)?credits\b", re.I),
    re.compile(r"\bpay[- ]as[- ]you[- ]go\b", re.I),
    re.compile(r"\bfree\s+trial\b.{0,100}\b(?:paid|subscription|billing)\b", re.I),
]

def fetch(url, method="GET"):
    req = Request(url, method=method, headers={"User-Agent": "PUI89-Free-Resource-Audit/1.1", "Accept": "text/html,*/*"})
    with urlopen(req, timeout=TIMEOUT) as response:
        body = response.read(1_500_000) if method == "GET" else b""
        return response.status, response.headers.get("Content-Type", ""), body

def check(url):
    url = url.rstrip(".,;:")
    for method in ("HEAD", "GET"):
        try:
            status, _, _ = fetch(url, method)
            return status < 400, "HTTP " + str(status)
        except HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 501):
                continue
            return False, "HTTP " + str(e.code)
        except (URLError, TimeoutError, OSError) as e:
            if method == "HEAD":
                continue
            return False, type(e).__name__
    return False, "request failed"

def check_paid_upgrade(url):
    """Return explicit paid-gate evidence only; access failures are not evidence."""
    try:
        status, content_type, body = fetch(url, "GET")
        if status >= 400:
            return None, "page unavailable for pricing review"
        if content_type and not any(x in content_type.lower() for x in ("text/html", "text/plain", "application/xhtml")):
            return None, "non-HTML page; paid status not inferred"
        page = html.unescape(body.decode("utf-8", errors="ignore"))
        page = re.sub(r"(?is)<(script|style|noscript)\b.*?</\1\s*>", " ", page)
        page = re.sub(r"(?s)<[^>]+>", " ", page)
        page = re.sub(r"\s+", " ", page)
        for pattern in PAID_PATTERNS:
            match = pattern.search(page)
            if match:
                return True, "explicit paid-upgrade wording: " + match.group(0)[:100]
        return False, "no explicit paid-upgrade signal found in fetched page text"
    except Exception as e:
        return None, "pricing review inconclusive: " + type(e).__name__

def main():
    STATE.parent.mkdir(parents=True, exist_ok=True)
    try:
        state = json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        state = {}
    failures = state.get("failures", {})
    paid_flags = state.get("paid_flags", {})
    cache, paid_cache = {}, {}
    checked = datetime.now(timezone.utc).isoformat(timespec="seconds")
    findings, paid_findings, removals = [], [], []
    changed_rows = 0

    for path in TARGETS:
        if not path.exists():
            continue
        old = path.read_text(encoding="utf-8")
        kept = []
        for line_no, line in enumerate(old.splitlines(keepends=True), 1):
            remove_reasons = []
            if line.lstrip().startswith("|") and not re.match(r"^\s*\|[\s:|-]+\|\s*$", line):
                for raw in dict.fromkeys(URL_RE.findall(line)):
                    url = raw.rstrip(".,;:")
                    if url not in cache:
                        cache[url] = check(url)
                    ok, reason = cache[url]
                    key = path.as_posix() + "|" + url
                    if ok:
                        failures.pop(key, None)
                    else:
                        item = failures.get(key, {"count": 0})
                        item["count"] = int(item.get("count", 0)) + 1
                        item["reason"] = reason
                        item["last_failed_at"] = checked
                        failures[key] = item
                        findings.append("- " + path.as_posix() + ":" + str(line_no) + " — " + url + " — " + reason + " — consecutive failures: " + str(item["count"]))
                        if item["count"] >= THRESHOLD:
                            remove_reasons.append("link failed " + str(item["count"]) + " consecutive checks: " + url)

                    if url not in paid_cache:
                        paid_cache[url] = check_paid_upgrade(url)
                    paid, paid_reason = paid_cache[url]
                    if paid is True:
                        item = paid_flags.get(key, {"count": 0})
                        item["count"] = int(item.get("count", 0)) + 1
                        item["reason"] = paid_reason
                        item["last_flagged_at"] = checked
                        paid_flags[key] = item
                        paid_findings.append("- " + path.as_posix() + ":" + str(line_no) + " — " + url + " — " + paid_reason + " — consecutive flags: " + str(item["count"]))
                        if item["count"] >= THRESHOLD:
                            remove_reasons.append("explicit paid-upgrade signal persisted " + str(item["count"]) + " checks: " + url)
                    elif paid is False:
                        paid_flags.pop(key, None)
                    else:
                        # Inconclusive page checks neither increment nor reset the paid counter.
                        paid_findings.append("- " + path.as_posix() + ":" + str(line_no) + " — " + url + " — " + paid_reason + " — no decision")
            if remove_reasons:
                removals.append("- Removed resource row from " + path.as_posix() + " after repeated checks: " + "; ".join(dict.fromkeys(remove_reasons)))
                for raw in dict.fromkeys(URL_RE.findall(line)):
                    url = raw.rstrip(".,;:")
                    key = path.as_posix() + "|" + url
                    failures.pop(key, None)
                    paid_flags.pop(key, None)
                changed_rows += 1
            else:
                kept.append(line)
        new = "".join(kept)
        if new != old:
            path.write_text(new, encoding="utf-8")

    STATE.write_text(json.dumps({"failures": failures, "paid_flags": paid_flags, "last_checked": checked}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    report = [
        "# Free Resource and Paid-Upgrade Audit", "",
        "Last checked: " + checked, "",
        "A resource-table row is removed only after three consecutive checks of an explicit paid-upgrade signal or a failed URL. Inconclusive page fetches do not count as paid evidence.", "",
        "## Removed rows", "", *(removals or ["- None this run."]), "",
        "## Explicit paid-upgrade signals under review", "", *(paid_findings or ["- No paid-upgrade signals detected this run."]), "",
        "## Unavailable links under review", "", *(findings or ["- No failing links detected this run."]), "",
        "## Safety limits", "",
        "- Only Markdown table rows in configured resource catalogues/guides can be removed.",
        "- No code, workflows, tests, datasets, project evidence, entire files, or repository history are deleted.",
        "- This is a conservative page-text scan, not a legal/pricing guarantee. It may miss JavaScript-rendered pricing or wording outside the fetched page.",
        "- A paid-upgrade signal means this catalogue's free-first policy removes the resource row, even if a limited free tier remains.",
        "- No account is upgraded, no billing is enabled, and no paid service is purchased.",
        "- Temporary outages and inconclusive page fetches do not count as evidence that a service requires payment.", ""
    ]
    REPORT.write_text("\n".join(report), encoding="utf-8")
    print("Audited", len(TARGETS), "files; removed", changed_rows, "rows; paid signals:", len(paid_findings), "; dead-link findings:", len(findings))

if __name__ == "__main__":
    main()
