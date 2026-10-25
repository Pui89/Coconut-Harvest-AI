"""Run the local model-optional agent workflow from a JSON observation.

This command uses only the Python standard library and the project's existing
decision agent. It does not access the network, invoke a shell, execute a plan,
or control hardware. Output is a JSON review proposal on stdout.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from agents.agentic_workflow import run_agentic_workflow


def _reject_constant(value: str) -> None:
    """Reject non-standard JSON constants such as NaN and Infinity."""
    raise ValueError(f"non-standard JSON constant is not allowed: {value}")


def parse_observation(text: str) -> dict[str, Any]:
    """Parse a JSON object and reject malformed/non-object input."""
    try:
        observation = json.loads(text, parse_constant=_reject_constant)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON at line {exc.lineno}, column {exc.colno}"
        ) from exc

    if not isinstance(observation, dict):
        raise ValueError("JSON root must be an object (key/value pairs)")
    return observation


def main(argv: list[str] | None = None) -> int:
    """Read one observation and print one JSON workflow report."""
    parser = argparse.ArgumentParser(
        description=(
            "Run the existing local decision agent and policy gate. "
            "No model, package, network or actuator is used."
        )
    )
    parser.add_argument(
        "--input",
        default="-",
        metavar="PATH",
        help="path to a JSON observation; use '-' for stdin (default)",
    )
    args = parser.parse_args(argv)

    if args.input == "-":
        raw_input = sys.stdin.read()
    else:
        try:
            raw_input = Path(args.input).read_text(encoding="utf-8")
        except OSError:
            print(
                f"agentic workflow input error: cannot read file '{Path(args.input).name}'",
                file=sys.stderr,
            )
            return 2

    try:
        observation = parse_observation(raw_input)
    except ValueError as exc:
        print(f"agentic workflow input error: {exc}", file=sys.stderr)
        return 2

    report = run_agentic_workflow(observation)
    sys.stdout.write(
        json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    )
    # Inconclusive/blocked proposals are valid reports; callers must inspect
    # the structured status field rather than mistake a review for execution.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
