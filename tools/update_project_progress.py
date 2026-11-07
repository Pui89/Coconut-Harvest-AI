#!/usr/bin/env python3
"""Generate an evidence-led daily README progress panel. Standard library only."""
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "docs" / "project-progress.json"
README = ROOT / "README.md"
START = "<!-- PUI89_DAILY_PROGRESS:START -->"
END = "<!-- PUI89_DAILY_PROGRESS:END -->"
WEIGHTS = [10,10,15,15,15,15,10,10]
GATES = ["Purpose & requirements","Architecture & engineering","Working software baseline","Reproducible tests & evaluation","Integrated product prototype","Safety & real-world validation","Licensing & regulatory readiness","Release package & support"]

def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    now = datetime.now(ZoneInfo("Asia/Bangkok"))
    credits = data["evidence_credit"]
    if len(credits) != len(WEIGHTS) or any(not isinstance(x, int) or x < 0 or x > w for x, w in zip(credits, WEIGHTS)):
        raise SystemExit("Invalid evidence credits; expected eight integer credits within gate weights.")
    score = sum(credits)
    pct = round(score / sum(WEIGHTS) * 100)
    if pct >= 75:
        colour, label = "🟢", "Advanced evidence stage"
    elif pct >= 50:
        colour, label = "🟡", "Developing evidence stage"
    elif pct >= 25:
        colour, label = "🟠", "Foundation and prototype stage"
    else:
        colour, label = "🔴", "Early foundation stage"
    filled = round(pct / 5)
    bar = "🟦" * filled + "⬜" * (20 - filled)
    rows = "\n".join(f"| {g} | {c}/{w} | {'🟩' * c}{'⬜' * (w-c)} |" for g, c, w in zip(GATES, credits, WEIGHTS))
    section = f"""{START}
## Daily project progress

**{colour} {pct}% — {label}**  
**Evidence score:** {score}/100 · **Review date:** {now.strftime('%d %B %Y')} (Asia/Bangkok)  
**Progress graph:** {bar} {pct}%

This is an evidence-weighted commercial-readiness estimate, not a code-completion percentage, sales forecast, certification, or measured real-world performance. Scores change only when repository evidence is reviewed and the evidence credits below are updated. The daily run refreshes the review date; it never increases the score merely because time has passed.

| Readiness gate | Evidence credit | Visual score |
|---|---:|---|
{rows}
| **Total** | **{score}/100** | **{bar}** |

**Next milestone:** Improve the lowest-scoring applicable gate with reproducible project-specific evidence. Planned work, concept artwork, unrun tests, synthetic-only results and tool inventories do not earn evidence credit.

**Status boundary:** Software tests and simulations do not establish a built, certified, field-tested or commercially validated physical product. Real-world claims require separate, traceable validation.

<!-- PUI89_DAILY_PROGRESS:END -->"""
    text = README.read_text(encoding="utf-8")
    if START in text and END in text:
        before = text.split(START, 1)[0]
        after = text.split(END, 1)[1]
        text = before + section + after
    else:
        text = text.rstrip() + "\n\n" + section + "\n"
    README.write_text(text, encoding="utf-8")

if __name__ == "__main__":
    main()
