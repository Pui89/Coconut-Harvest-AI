"""Opt-in LeRobot SmolVLA adapter for offline coconut-arm research.

This loader only returns a policy object. It never connects to robot hardware,
sends commands, or downloads weights unless explicitly permitted.
"""
from __future__ import annotations
import os

MODEL_ID = "lerobot/smolvla_base"

def load_smolvla_policy(*, allow_download: bool = False):
    """Load the SmolVLA base policy from local cache by default.

    The base checkpoint is not calibrated for PUI89's proposed harvesting arm.
    Fine-tuning, a matching LeRobot dataset/robot configuration, simulation
    evaluation and an independent safety case are required before any use.
    """
    try:
        from lerobot.policies.smolvla.modeling_smolvla import SmolVLAPolicy
    except ImportError as exc:
        raise RuntimeError(
            "LeRobot SmolVLA dependencies are not installed. Do not install them "
            "automatically; first check Python, disk, RAM/VRAM, package licences "
            "and the official LeRobot installation requirements."
        ) from exc
    local_only = not (
        allow_download
        or os.environ.get("PUI89_ALLOW_MODEL_DOWNLOAD", "").strip() == "1"
    )
    return SmolVLAPolicy.from_pretrained(MODEL_ID, local_files_only=local_only)

def propose_action_vector(policy, prepared_observation_batch):
    """Return an unexecuted, simulation-only proposal; never send to hardware."""
    import torch
    with torch.inference_mode():
        action = policy.select_action(prepared_observation_batch)
    if hasattr(action, "detach"):
        action = action.detach().cpu().tolist()
    return {
        "model_id": MODEL_ID,
        "status": "SIMULATION_ONLY_ACTION_PROPOSAL",
        "action_vector": action,
        "actuator_authorized": False,
        "human_review_required": True,
        "note": "Uncalibrated base-model output; not a safe robot command.",
    }
