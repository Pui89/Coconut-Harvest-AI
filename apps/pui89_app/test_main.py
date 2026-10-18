import unittest
from apps.pui89_app.main import AnalyzeRequest, Candidate, analyze


class HarvestAppTests(unittest.TestCase):
    def test_bad_sensor_forces_safe_hold(self):
        result = analyze(AnalyzeRequest(rgb_available=True, depth_valid=False,
                                        timestamp_skew_ms=0, candidates=[]))
        self.assertEqual(result["status"], "SAFE_HOLD")
        self.assertFalse(result["actuator_commands_sent"])

    def test_candidate_is_proposal_not_execution(self):
        c = Candidate(target_id="c1", ripeness_score=.9, localization_confidence=.95,
                      distance_m=2, obstacle_clearance_m=.5, stable_track_frames=10)
        result = analyze(AnalyzeRequest(rgb_available=True, depth_valid=True,
                                        timestamp_skew_ms=4, candidates=[c]))
        self.assertEqual(result["decisions"][0]["status"], "PROPOSAL_APPROVED_NOT_EXECUTED")
        self.assertFalse(result["actuator_commands_sent"])

    def test_low_clearance_rejected(self):
        c = Candidate(target_id="c2", ripeness_score=.9, localization_confidence=.95,
                      distance_m=2, obstacle_clearance_m=.1, stable_track_frames=10)
        result = analyze(AnalyzeRequest(rgb_available=True, depth_valid=True,
                                        timestamp_skew_ms=4, candidates=[c]))
        self.assertEqual(result["decisions"][0]["status"], "REJECTED")


if __name__ == "__main__":
    unittest.main()
