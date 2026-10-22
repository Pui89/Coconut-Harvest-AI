from agents.project_agent import run_agent


def test_missing_target_requests_new_view():
    d = run_agent({})
    assert d.recommendation == "REQUEST_NEW_VIEW"
    assert d.actuator_command is None


def test_obstacle_not_clear_stops():
    d = run_agent({"target_detected": True, "confidence": .95, "depth_m": 2.0,
                   "reachable": True, "obstacle_clear": False})
    assert d.status == "STOP"


def test_human_approval_is_required():
    d = run_agent({"target_detected": True, "confidence": .95, "depth_m": 2.0,
                   "reachable": True, "obstacle_clear": True})
    assert d.status == "AWAITING_APPROVAL"
    assert d.requires_human_approval is True


def test_rejects_invalid_confidence():
    assert run_agent({"target_detected": True, "confidence": 3, "depth_m": 2}).status == "NEED_DATA"


def test_rejects_non_finite_confidence_and_depth():
    assert run_agent({"target_detected": True, "confidence": float('nan')}).status == "NEED_DATA"
    assert run_agent({"target_detected": True, "confidence": .95, "depth_m": float('inf')}).status == "NEED_DATA"
