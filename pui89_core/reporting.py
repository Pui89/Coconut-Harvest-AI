"""Small dependency-free JSON failure reports."""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


def write_failure_report(path: str | Path, failures: Iterable[dict[str, Any]], *, run_name: str = "local-check") -> Path:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    failure_list = list(failures)
    payload = {
        "schema_version": "1.0",
        "run_name": run_name,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "failure_count": len(failure_list),
        "failures": failure_list,
    }
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target
