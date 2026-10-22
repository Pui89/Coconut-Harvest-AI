from coconut_harvest_robot.harvest_assessment import (
    CoconutObservation,
    HarvestDecision,
    HarvestSafetyContext,
    MaturityClass,
    assess_coconut_for_harvest,
)


def good_observation(**overrides):
    values = dict(
        fruit_id="fruit-001",
        maturity_class=MaturityClass.MATURE_GREEN,
        class_confidence=0.95,
        position_3d_m=(1.0, 2.0, 3.0),
        position_uncertainty_m=0.05,
        location_valid=True,
        reachability_verified=True,
        within_verified_workspace=True,
        capture_ready=True,
    )
    values.update(overrides)
    return CoconutObservation(**values)


def safe_context(**overrides):
    values = dict(
        sensors_healthy=True,
        calibration_valid=True,
        localization_ready=True,
        obstacle_zone_clear=True,
        people_clear=True,
        overhead_hazards_clear=True,
        base_stable=True,
        environment_within_validated_limits=True,
        independent_interlock_ready=True,
        required_supervision_present=True,
    )
    values.update(overrides)
    return HarvestSafetyContext(**values)


def test_mature_green_can_only_be_recommended_for_supervised_authorization():
    result = assess_coconut_for_harvest(good_observation(), safe_context())
    assert result.decision is HarvestDecision.ELIGIBLE_FOR_SUPERVISED_AUTHORIZATION
    assert result.cutter_enabled is False


def test_young_green_is_not_selected_by_default():
    result = assess_coconut_for_harvest(
        good_observation(maturity_class=MaturityClass.YOUNG_GREEN), safe_context()
    )
    assert result.decision is HarvestDecision.REVIEW_REQUIRED
    assert "maturity_not_selected" in result.reason_codes
    assert result.cutter_enabled is False


def test_brown_aging_is_not_selected_by_default():
    result = assess_coconut_for_harvest(
        good_observation(maturity_class=MaturityClass.BROWN_AGING), safe_context()
    )
    assert "maturity_not_selected" in result.reason_codes
    assert result.cutter_enabled is False


def test_uncertain_maturity_never_qualifies():
    result = assess_coconut_for_harvest(
        good_observation(maturity_class=MaturityClass.UNCERTAIN), safe_context()
    )
    assert "uncertain_maturity" in result.reason_codes
    assert result.cutter_enabled is False


def test_low_confidence_requires_review():
    result = assess_coconut_for_harvest(
        good_observation(class_confidence=0.30), safe_context()
    )
    assert result.decision is HarvestDecision.REVIEW_REQUIRED
    assert "low_class_confidence" in result.reason_codes


def test_missing_depth_position_stops():
    result = assess_coconut_for_harvest(
        good_observation(position_3d_m=None, location_valid=False), safe_context()
    )
    assert result.decision is HarvestDecision.STOP
    assert "invalid_or_missing_3d_position" in result.reason_codes


def test_nan_coordinate_stops():
    result = assess_coconut_for_harvest(
        good_observation(position_3d_m=(1.0, float("nan"), 3.0)), safe_context()
    )
    assert result.decision is HarvestDecision.STOP


def test_unknown_or_excessive_location_uncertainty_stops():
    unknown = assess_coconut_for_harvest(
        good_observation(position_uncertainty_m=None), safe_context()
    )
    excessive = assess_coconut_for_harvest(
        good_observation(position_uncertainty_m=0.9), safe_context()
    )
    assert unknown.decision is HarvestDecision.STOP
    assert excessive.decision is HarvestDecision.REVIEW_REQUIRED


def test_outside_verified_workspace_stops():
    result = assess_coconut_for_harvest(
        good_observation(within_verified_workspace=False), safe_context()
    )
    assert result.decision is HarvestDecision.STOP
    assert result.cutter_enabled is False


def test_people_or_overhead_hazard_stops():
    for context in (
        safe_context(people_clear=False),
        safe_context(overhead_hazards_clear=False),
    ):
        result = assess_coconut_for_harvest(good_observation(), context)
        assert result.decision is HarvestDecision.STOP
        assert result.cutter_enabled is False


def test_failed_capture_or_interlock_prevents_authorization():
    capture = assess_coconut_for_harvest(
        good_observation(capture_ready=False), safe_context()
    )
    interlock = assess_coconut_for_harvest(
        good_observation(), safe_context(independent_interlock_ready=False)
    )
    assert capture.decision is HarvestDecision.REVIEW_REQUIRED
    assert interlock.decision is HarvestDecision.STOP
    assert capture.cutter_enabled is False
    assert interlock.cutter_enabled is False
