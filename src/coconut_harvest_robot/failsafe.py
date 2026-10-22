"""Software-level fail-safe mode selector for Coconut Harvest AI.

This module only produces a decision record. It does NOT control hardware and is
not a substitute for an independent, safety-rated controller, emergency stop,
motor driver interlocks, or physical validation.
"""
from dataclasses import dataclass
from enum import Enum


class OperatingMode(str, Enum):
    AI_OPERATION = "AI_OPERATION"
    LIMITED_SAFE_OPERATION = "LIMITED_SAFE_OPERATION"
    MANUAL_RECOVERY = "MANUAL_RECOVERY"


@dataclass(frozen=True)
class SystemHealth:
    ai_ready: bool
    perception_ready: bool
    safety_sensors_ready: bool
    localization_ready: bool
    route_verified: bool
    operator_link_ready: bool
    battery_return_reserve_ok: bool
    emergency_stop_active: bool = False
    hardware_fault: bool = False


@dataclass(frozen=True)
class ModeDecision:
    mode: OperatingMode
    harvesting_allowed: bool
    autonomous_motion_allowed: bool
    cutter_enabled: bool
    alert_operator: bool
    reason: str


def select_operating_mode(health: SystemHealth) -> ModeDecision:
    """Select the most conservative mode from explicit health signals.

    Emergency stop or hardware fault always selects manual recovery.
    Limited mode never permits harvesting or cutter operation.
    Autonomous limited movement is only suggested when safety sensors,
    localization, route verification, operator link, and return reserve are OK.
    """
    if health.emergency_stop_active:
        return ModeDecision(
            OperatingMode.MANUAL_RECOVERY, False, False, False, True,
            "Emergency stop active; keep hazardous actuators disabled and require manual reset.",
        )

    if health.hardware_fault:
        return ModeDecision(
            OperatingMode.MANUAL_RECOVERY, False, False, False, True,
            "Hardware fault; stop hazardous actions and request operator recovery.",
        )

    if not health.safety_sensors_ready:
        return ModeDecision(
            OperatingMode.MANUAL_RECOVERY, False, False, False, True,
            "Safety sensor status unknown or failed; autonomous movement is not permitted.",
        )

    full_ai_ready = (
        health.ai_ready
        and health.perception_ready
        and health.localization_ready
    )
    if full_ai_ready:
        return ModeDecision(
            OperatingMode.AI_OPERATION, True, True, False, False,
            "Health signals permit AI-assisted operation; cutter still requires separate hardware interlocks and authorization.",
        )

    limited_motion_ready = (
        health.localization_ready
        and health.route_verified
        and health.operator_link_ready
        and health.battery_return_reserve_ok
    )
    if limited_motion_ready:
        return ModeDecision(
            OperatingMode.LIMITED_SAFE_OPERATION, False, True, False, True,
            "AI/perception unavailable; harvesting disabled. Limited low-speed movement only on a verified safe route.",
        )

    return ModeDecision(
        OperatingMode.MANUAL_RECOVERY, False, False, False, True,
        "Safe route or recovery prerequisites are not confirmed; wait for manual recovery.",
    )
