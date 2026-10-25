import unittest
from pui89_autonomy.world_state import WorldStateTracker

class TrackerTest(unittest.TestCase):
    def test_observation_is_counted(self):
        tracker = WorldStateTracker()
        tracker.update({"object_id":"item-1","label":"candidate","timestamp":1,"confidence":0.9,"source":"test"})
        self.assertEqual(tracker.snapshot(1)["usable_track_count"], 1)

if __name__ == "__main__":
    unittest.main()
