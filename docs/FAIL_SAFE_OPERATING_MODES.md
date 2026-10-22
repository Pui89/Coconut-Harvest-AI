# Fail-safe operating modes

**Status:** software decision prototype and design requirements only. This is not a validated robot safety system and does not directly control actuators.

## Three modes

1. **AI operation** — AI-assisted perception and planning may propose harvesting tasks. A separate safety controller, interlocks, operator authorization, and hardware limits must independently govern any hazardous action.
2. **Limited safe operation** — when AI or perception is unavailable, harvesting and cutter operation are disabled. Low-speed movement may be considered only if safety sensors, localization, a verified return route, operator communication, and battery reserve are all confirmed. Otherwise select manual recovery.
3. **Manual recovery** — stop autonomous motion when safe to do so, disable hazardous actuators, alert the operator, and wait for trained recovery. An active emergency stop must require a deliberate manual reset after inspection.

## Fault response

| Fault | Expected software decision |
|---|---|
| AI/model unavailable | Limited safe operation only if all limited-mode prerequisites are confirmed; otherwise manual recovery |
| Camera/perception unavailable | No harvesting; limited safe movement only if prerequisites are confirmed |
| Safety sensor missing/failed | Manual recovery; no autonomous motion |
| Localization lost or route not verified | Manual recovery; no autonomous motion |
| Operator link lost | Manual recovery unless a separately validated local policy defines a safe response |
| Battery return reserve unavailable | Manual recovery; no autonomous return claim |
| Emergency stop active | Manual recovery state; hazardous actuators must be disabled by independent hardware |
| Hardware fault | Manual recovery; hazardous actions disabled |

## Test locally

From the repository root, after installing the package or setting the source path:

```bash
python -m pip install -e .
python -m pip install pytest
python -m pytest -q tests/test_failsafe.py
```

No model download or paid API is needed for these tests.

## Before connecting real hardware

- Implement emergency stop and cutter power isolation in independent, appropriately rated hardware.
- Verify braking, arm holding, and power-loss behaviour with the physical design.
- Do not assume that stopping every motor is always safe; heavy arms may need controlled holding/braking.
- Add independent watchdogs, current/temperature limits, manual override, and a documented reset procedure.
- Simulate fault injection first, then test without a cutter, then with a qualified safety review.
- Never use this Python selector as the sole safety layer or as proof of functional safety.
