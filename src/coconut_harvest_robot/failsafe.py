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

    Invalid or missing health records fail closed. Emergency stop or hardware
    fault always selects manual recovery. Full AI operation requires healthy
    perception/localization plus a verified route, a live operator link, and
    sufficient return reserve. Limited mode never permits harvesting or cutter
    operation. This is decision support, not a hardware safety controller.
    """
    if not isinstance(health, SystemHealth):
        return ModeDecision(
            OperatingMode.MANUAL_RECOVERY, False, False, False, True,
            "System health record is missing or malformed; require manual recovery.",
        )

    signals = (
        health.ai_ready,
        health.perception_ready,
        health.safety_sensors_ready,
        health.localization_ready,
        health.route_verified,
        health.operator_link_ready,
        health.battery_return_reserve_ok,
        health.emergency_stop_active,
        health.hardware_fault,
    )
    if any(type(signal) is not bool for signal in signals):
        return ModeDecision(
            OperatingMode.MANUAL_RECOVERY, False, False, False, True,
            "System health contains a missing or invalid boolean signal; require manual recovery.",
        )

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
        and health.route_verified
        and health.operator_link_ready
        and health.battery_return_reserve_ok
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
