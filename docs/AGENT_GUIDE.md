# Decision-support agent

## Purpose

Checks supplied target confidence, depth, reachability, sensor health, obstacle clearance, and human approval before returning a recommendation. It never sends arm or cutter commands.

## Run a local example

From the repository root:

```bash
python -c "from agents.project_agent import run_agent; print(run_agent({}).to_dict())"
python -m pytest tests/test_project_agent.py -q
```

The module uses only the Python standard library. It makes no network calls and does not download models. Inputs are observations supplied by the caller; it does not run perception models by itself.

## Integration contract

Call `run_agent(observation: dict)`. The result contains a status, a recommendation, reasons, and `requires_human_approval`. `actuator_command` is always `None`: this is a decision-support gate, not a robot controller. A real integration must validate inputs, log provenance, test failure cases, and keep any physical action behind a separately validated safety controller and operator approval.

## Limitations

- Passing these tests verifies decision logic only, not model accuracy or real-world performance.
- Thresholds and rules are illustrative defaults and need domain-specific validation before research or operational use.
- Do not report this module as a trained or autonomous AI agent; it is a deterministic, rule-based decision-support prototype.
