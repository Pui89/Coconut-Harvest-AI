"""Structural contract tests for project-specific Gazebo starter worlds."""
import json
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class GazeboWorldContractTests(unittest.TestCase):
    def test_starter_world_is_well_formed_sdf(self):
        path = ROOT / "simulation" / "gazebo" / "pui89_world.sdf"
        content = path.read_text(encoding="utf-8")
        self.assertNotIn("WORLD_NAME", content)
        self.assertNotIn("SCENE_OBJECTS", content)
        root = ET.parse(path).getroot()
        self.assertEqual(root.tag, "sdf")
        world = root.find("world")
        self.assertIsNotNone(world)
        self.assertIsNotNone(world.find("physics"))
        models = world.findall("model")
        model_names = {model.get("name") for model in models}
        self.assertIn("ground_plane", model_names)
        self.assertGreaterEqual(len(models), 2)

    def test_stack_manifest_keeps_download_and_actuation_off(self):
        manifest = json.loads((ROOT / "config" / "robotics_stack.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], 1)
        self.assertFalse(manifest["safety"]["physical_actuation"])
        self.assertFalse(manifest["stack"]["smolvlm"]["downloaded"])


if __name__ == "__main__":
    unittest.main()
