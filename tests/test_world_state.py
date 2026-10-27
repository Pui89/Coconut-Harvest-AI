import unittest
from pui89_autonomy.world_state import WorldStateTracker

class TrackerTest(unittest.TestCase):
    def test_observation_is_counted(self):
        tracker = WorldStateTracker()
        tracker.update({"object_id":"item-1","label":"candidate","timestamp":1,"confidence":0.9,"source":"test"})
        self.assertEqual(tracker.snapshot(1)["usable_track_count"], 1)

    def test_invalid_confidence_is_rejected(self):
        tracker = WorldStateTracker()
        for confidence in (True, -0.1, 1.1, float("nan"), float("inf")):
            with self.subTest(confidence=confidence):
                with self.assertRaises(ValueError):
                    tracker.update({"object_id":"x","label":"A","timestamp":1,"confidence":confidence,"source":"test"})

    def test_old_observation_does_not_replace_newer_state(self):
        tracker = WorldStateTracker()
        tracker.update({"object_id":"x","label":"A","timestamp":2,"confidence":0.9,"source":"test"})
        result = tracker.update({"object_id":"x","label":"B","timestamp":1,"confidence":0.9,"source":"test"})
        self.assertFalse(result["accepted"])
        self.assertEqual(tracker.snapshot(2)["tracks"][0]["label"], "A")

if __name__ == "__main__":
    unittest.main()
