from coconut_harvest_robot.failsafe import (
    OperatingMode,
    SystemHealth,
    select_operating_mode,
)


def healthy(**overrides):
    values = dict(
        ai_ready=True,
        perception_ready=True,
        safety_sensors_ready=True,
        localization_ready=True,
        route_verified=True,
        operator_link_ready=True,
        battery_return_reserve_ok=True,
    )
    values.update(overrides)
    return SystemHealth(**values)


def test_healthy_system_selects_ai_mode_but_does_not_enable_cutter():
    result = select_operating_mode(healthy())
    assert result.mode is OperatingMode.AI_OPERATION
    assert result.harvesting_allowed is True
    assert result.cutter_enabled is False


def test_ai_failure_selects_limited_mode_without_harvesting():
    result = select_operating_mode(healthy(ai_ready=False))
    assert result.mode is OperatingMode.LIMITED_SAFE_OPERATION
    assert result.harvesting_allowed is False
    assert result.autonomous_motion_allowed is True
    assert result.cutter_enabled is False
    assert result.alert_operator is True


def test_lost_localization_requires_manual_recovery():
    result = select_operating_mode(healthy(localization_ready=False))
    assert result.mode is OperatingMode.MANUAL_RECOVERY
    assert result.autonomous_motion_allowed is False
    assert result.cutter_enabled is False


def test_failed_safety_sensor_requires_manual_recovery():
    result = select_operating_mode(healthy(safety_sensors_ready=False))
    assert result.mode is OperatingMode.MANUAL_RECOVERY
    assert result.cutter_enabled is False


def test_emergency_stop_overrides_all_other_states():
    result = select_operating_mode(healthy(emergency_stop_active=True))
    assert result.mode is OperatingMode.MANUAL_RECOVERY
    assert result.harvesting_allowed is False
    assert result.autonomous_motion_allowed is False
    assert result.cutter_enabled is False


def test_hardware_fault_overrides_ai_ready_state():
    result = select_operating_mode(healthy(hardware_fault=True))
    assert result.mode is OperatingMode.MANUAL_RECOVERY
    assert result.cutter_enabled is False


def test_no_verified_route_means_no_limited_autonomous_motion():
    result = select_operating_mode(healthy(ai_ready=False, route_verified=False))
    assert result.mode is OperatingMode.MANUAL_RECOVERY
    assert result.autonomous_motion_allowed is False


def test_no_return_battery_reserve_means_manual_recovery():
    result = select_operating_mode(healthy(ai_ready=False, battery_return_reserve_ok=False))
    assert result.mode is OperatingMode.MANUAL_RECOVERY
    assert result.autonomous_motion_allowed is False
