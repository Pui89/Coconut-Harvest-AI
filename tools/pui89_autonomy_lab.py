#!/usr/bin/env python3
"""PUI89 local autonomy lab: stdlib-only simulation, mock VLA and offline model preflight.
No network request, package installation, model download, or hardware command is performed.
"""
from __future__ import annotations
import argparse, csv, ctypes, hashlib, json, os, shutil, statistics, subprocess, time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ENGINE_VERSION = "pui89-autonomy-lab-1.0.0"
MODEL_PROFILE = {
    "model_id": "HuggingFaceTB/SmolVLM-256M-Instruct",
    "model_card_url": "https://huggingface.co/HuggingFaceTB/SmolVLM-256M-Instruct",
    "license": "Apache-2.0 (as declared by publisher; manually re-check before use)",
    "license_url": "https://huggingface.co/HuggingFaceTB/SmolVLM-256M-Instruct",
    "weight_file": "model.safetensors", "weight_file_bytes": 513_000_000,
    "minimum_free_disk_gib": 3.0, "minimum_available_ram_gib": 4.0,
    "minimum_available_vram_gib": 1.0,
}

def stable_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

class MockVLA:
    """Return action labels for simulation only. There is no robot adapter."""
    SAFETY_FLAGS = ("emergency_stop", "sensors_ok", "sensor_data_fresh", "comms_ok",
                    "target_visible", "target_valid", "human_review_required", "operator_approved")

    def __init__(self, confidence_threshold: float = 0.65) -> None:
        import math
        if isinstance(confidence_threshold, bool) or not isinstance(confidence_threshold, (int, float)):
            raise ValueError("confidence_threshold must be a finite number in [0, 1]")
        if not math.isfinite(confidence_threshold) or not 0.0 <= confidence_threshold <= 1.0:
            raise ValueError("confidence_threshold must be a finite number in [0, 1]")
        self.threshold = float(confidence_threshold)

    def propose(self, state: dict[str, Any], ready_action: str) -> tuple[str, list[str]]:
        import math
        if not isinstance(state, dict):
            return "SAFE_HOLD", ["state_not_object: SAFE_HOLD"]
        # Explicit safety flags must be real Booleans; truthy strings/integers
        # must never be interpreted as safe sensor or approval states.
        for key in self.SAFETY_FLAGS:
            if key in state and not isinstance(state[key], bool):
                return "SAFE_HOLD", [f"malformed_safety_flag:{key}: SAFE_HOLD"]
        if state.get("emergency_stop", False):
            return "SAFE_HOLD", ["emergency_stop: SAFE_HOLD"]
        if not state.get("sensors_ok", True):
            return "SAFE_HOLD", ["sensor_fault: SAFE_HOLD"]
        if not state.get("sensor_data_fresh", True):
            return "SAFE_HOLD", ["stale_sensor_data: SAFE_HOLD"]
        if not state.get("comms_ok", True):
            return "SAFE_HOLD", ["communications_lost: SAFE_HOLD"]
        if state.get("modalities_conflict", False):
            return "UNKNOWN", ["modalities_conflict: UNKNOWN"]
        if state.get("missing_required_modality", False):
            return "UNKNOWN", ["missing_modality: UNKNOWN"]
        confidence = state.get("confidence", 1.0)
        if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
            return "UNKNOWN", ["confidence_not_numeric: UNKNOWN"]
        if not math.isfinite(confidence) or not 0.0 <= confidence <= 1.0 or confidence < self.threshold:
            return "UNKNOWN", ["confidence_invalid_or_below_threshold: UNKNOWN"]
        if state.get("target_visible", True) is False or state.get("target_valid", True) is False:
            return "SEARCH", ["target_unavailable: SEARCH"]
        if state.get("human_review_required", False):
            return "REQUEST_HUMAN_REVIEW", ["human_review_required: REQUEST_HUMAN_REVIEW"]
        if state.get("operator_approved", True) is False:
            return "REQUEST_APPROVAL", ["operator_approval_missing: REQUEST_APPROVAL"]
        return ready_action, ["simulated_inputs_passed", "simulation_only_action"]

def validate_config(config: dict[str, Any]) -> None:
    if config.get("schema_version") != 1 or not config.get("project_id"):
        raise ValueError("scenario config requires schema_version=1 and project_id")
    scenarios = config.get("scenarios")
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("scenarios must be a non-empty list")
    ids: set[str] = set()
    for scenario in scenarios:
        sid = scenario.get("id")
        if not sid or sid in ids:
            raise ValueError(f"scenario id missing or duplicated: {sid!r}")
        ids.add(sid)
        if not scenario.get("steps"):
            raise ValueError(f"scenario {sid!r} has no steps")
        for n, step in enumerate(scenario["steps"], 1):
            if "expected_action" not in step or float(step.get("dt_s", 1.0)) <= 0:
                raise ValueError(f"scenario {sid!r}, step {n}: expected_action and positive dt_s required")
            if not isinstance(step.get("state", {}), dict):
                raise ValueError(f"scenario {sid!r}, step {n}: state must be an object")

def run_scenarios(config_path: Path, output_dir: Path) -> dict[str, Any]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    validate_config(config)
    cfg_hash = digest(stable_json(config))
    run_id = digest(f"{ENGINE_VERSION}:{cfg_hash}")[:16]
    policy = MockVLA(config.get("confidence_threshold", 0.65))
    output_dir.mkdir(parents=True, exist_ok=True)
    rows, scenarios_out, failures, timings = [], [], [], []
    actions: dict[str, int] = {}
    total_steps = passed_steps = 0
    for scenario in config["scenarios"]:
        sim_time, scenario_ok = 0.0, True
        world_state: dict[str, Any] = {}
        for index, step in enumerate(scenario["steps"], 1):
            sim_time = round(sim_time + float(step.get("dt_s", 1.0)), 6)
            # State updates persist within a scenario; each row records the full snapshot.
            for key in step.get("remove_state_keys", []):
                world_state.pop(key, None)
            world_state.update(step.get("state", {}))
            state = dict(world_state)
            start = time.perf_counter()
            start = time.perf_counter()
            actual, trace = policy.propose(state, config["action_if_ready"])
            latency_ms = round((time.perf_counter() - start) * 1000.0, 4)
            timings.append(latency_ms)
            expected, passed = str(step["expected_action"]), actual == str(step["expected_action"])
            total_steps += 1
            passed_steps += int(passed)
            scenario_ok = scenario_ok and passed
            actions[actual] = actions.get(actual, 0) + 1
            row = {"project_id": config["project_id"], "run_id": run_id, "scenario_id": scenario["id"],
                   "seed": int(scenario.get("seed", 0)), "step_index": index, "sim_time_s": sim_time,
                   "state": state, "actual_action": actual, "expected_action": expected, "passed": passed,
                   "rule_trace": trace, "latency_ms_observed": latency_ms, "hardware_actuation": False}
            rows.append(row)
            if not passed:
                failures.append({k: row[k] for k in ("scenario_id","step_index","state","actual_action","expected_action","rule_trace")})
        scenarios_out.append({"scenario_id": scenario["id"], "seed": int(scenario.get("seed", 0)),
                              "steps": len(scenario["steps"]), "passed": scenario_ok})
    ordered = sorted(timings)
    p95 = ordered[min(len(ordered)-1, int(0.95*(len(ordered)-1)))] if ordered else None
    json_path = output_dir / f"simulation-report-{config['project_id']}-{run_id}.json"
    csv_path = output_dir / f"simulation-steps-{config['project_id']}-{run_id}.csv"
    report = {
        "schema_version": 1, "engine_version": ENGINE_VERSION, "project_id": config["project_id"],
        "run_id": run_id, "scenario_config_sha256": cfg_hash, "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": "PASS" if not failures else "FAIL",
        "safety_statement": config.get("project_limit", "Simulation only; no physical capability is verified."),
        "reproducibility": {"run_id_stable_for_same_config_and_engine": True, "seed_values_recorded": True,
                            "deterministic_metrics_exclude_timing": True, "scenario_config_sha256": cfg_hash},
        "metrics": {"scenario_count": len(scenarios_out),
                    "scenario_pass_count": sum(int(s["passed"]) for s in scenarios_out),
                    "step_count": total_steps, "step_pass_count": passed_steps, "failure_count": len(failures),
                    "step_pass_rate": round(passed_steps/total_steps, 6) if total_steps else 0.0,
                    "scenario_pass_rate": round(sum(int(s["passed"]) for s in scenarios_out)/len(scenarios_out), 6),
                    "action_counts": dict(sorted(actions.items())), "safe_hold_count": actions.get("SAFE_HOLD", 0)},
        "observed_runtime_metrics_not_reproducible": {
            "latency_unit": "ms", "latency_mean_ms": round(statistics.fmean(timings), 4) if timings else None,
            "latency_median_ms": round(statistics.median(timings), 4) if timings else None,
            "latency_p95_ms_observed": round(p95, 4) if p95 is not None else None,
            "note": "Host load and timer variation affect runtime values; compare only like-for-like hosts."},
        "scenarios": scenarios_out, "failures": failures, "steps": rows,
        "output_files": {"json": str(json_path), "csv": str(csv_path)},
    }
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        fields = ["project_id","run_id","scenario_id","seed","step_index","sim_time_s","state_json",
                  "actual_action","expected_action","passed","rule_trace","latency_ms_observed","hardware_actuation"]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            export = dict(row)
            export["state_json"] = stable_json(export.pop("state"))
            export["rule_trace"] = " | ".join(export["rule_trace"])
            writer.writerow(export)
    return report

def _available_ram_gib() -> float | None:
    try:
        if os.name == "nt":
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [("dwLength",ctypes.c_ulong),("dwMemoryLoad",ctypes.c_ulong),
                    ("ullTotalPhys",ctypes.c_ulonglong),("ullAvailPhys",ctypes.c_ulonglong),
                    ("ullTotalPageFile",ctypes.c_ulonglong),("ullAvailPageFile",ctypes.c_ulonglong),
                    ("ullTotalVirtual",ctypes.c_ulonglong),("ullAvailVirtual",ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual",ctypes.c_ulonglong)]
            s = MEMORYSTATUSEX(); s.dwLength = ctypes.sizeof(s)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(s)):
                return s.ullAvailPhys/(1024**3)
        return os.sysconf("SC_PAGE_SIZE")*os.sysconf("SC_AVPHYS_PAGES")/(1024**3)
    except (AttributeError, OSError, ValueError):
        return None

def _nvidia_memory_gib() -> dict[str, float] | None:
    exe = shutil.which("nvidia-smi")
    if not exe:
        return None
    try:
        result = subprocess.run([exe,"--query-gpu=memory.total,memory.free","--format=csv,noheader,nounits"],
                                capture_output=True, check=True, text=True, timeout=5)
        total, free = [float(v.strip()) for v in result.stdout.strip().splitlines()[0].split(",")[:2]]
        return {"total_gib": round(total/1024, 3), "free_gib": round(free/1024, 3)}
    except (OSError, subprocess.SubprocessError, IndexError, ValueError):
        return None

def model_preflight(probe_path: Path) -> dict[str, Any]:
    disk = shutil.disk_usage(probe_path).free/(1024**3)
    ram, gpu = _available_ram_gib(), _nvidia_memory_gib()
    checks = {"model_license_declared": True, "free_disk_meets_3_gib_minimum": disk >= 3.0,
              "available_ram_meets_4_gib_estimate": None if ram is None else ram >= 4.0,
              "nvidia_free_vram_meets_1_gib_estimate": None if gpu is None else gpu["free_gib"] >= 1.0}
    hard_fail = [name for name, value in checks.items() if value is False]
    unknown = [name for name, value in checks.items() if value is None]
    return {"schema_version": 1, **MODEL_PROFILE, "weight_file_mib": round(MODEL_PROFILE["weight_file_bytes"]/(1024**2),2),
            "download_scope": "Allowlisted weights/config/tokenizer/processor only; never clone the full repository or fetch ONNX variants.",
            "hardware_observed": {"free_disk_gib": round(disk,3),
                "available_ram_gib": None if ram is None else round(ram,3), "nvidia_gpu_memory_gib": gpu},
            "checks": checks, "hard_failures": hard_fail, "unknown_checks": unknown,
            "preflight_status": "BLOCKED" if hard_fail else ("READY_FOR_MANUAL_REVIEW" if not unknown else "READY_WITH_HARDWARE_UNKNOWN"),
            "download_performed": False, "software_installed": False, "hardware_actuation": False,
            "next_step": "Review the official model card and report manually; this command never installs or downloads weights.",
            "safety_note": "VLM output is untrusted perception assistance, not a validated detector or autonomous decision."}

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    sim = sub.add_parser("simulate"); sim.add_argument("--config",type=Path,default=Path("simulation/scenarios.json"))
    sim.add_argument("--output-dir",type=Path,default=Path("reports/simulation"))
    pre = sub.add_parser("preflight"); pre.add_argument("--probe-path",type=Path,default=Path("."))
    pre.add_argument("--output",type=Path,default=Path("reports/model-readiness-preflight.json"))
    args = parser.parse_args()
    try:
        if args.command == "simulate":
            report = run_scenarios(args.config,args.output_dir)
            m = report["metrics"]
            print(f"project={report['project_id']} status={report['status']} run_id={report['run_id']} "
                  f"scenarios={m['scenario_pass_count']}/{m['scenario_count']} steps={m['step_pass_count']}/{m['step_count']} "
                  f"failures={m['failure_count']} hardware_actuation=false")
            print(f"report={report['output_files']['json']}")
            return 1 if m["failure_count"] else 0
        report = model_preflight(args.probe_path)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
        print(f"model={report['model_id']} status={report['preflight_status']} download_performed=false report={args.output}")
        return 1 if report["preflight_status"] == "BLOCKED" else 0
    except (OSError,json.JSONDecodeError,ValueError,KeyError,TypeError) as exc:
        print(f"AUTONOMY_LAB_ERROR: {exc}")
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
