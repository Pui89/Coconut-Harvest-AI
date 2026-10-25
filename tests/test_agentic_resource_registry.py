import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AgenticResourceRegistryTests(unittest.TestCase):
    def test_registry_contains_free_agent_framework_and_local_runtime_options(self):
        config = json.loads((ROOT / "config" / "optional_resources.json").read_text(encoding="utf-8"))
        resources = {item["id"]: item for item in config["resources"]}
        expected = {"smolagents", "langgraph", "pydantic-ai", "ollama", "llama-cpp-cli"}
        self.assertTrue(expected.issubset(resources))
        for resource_id in expected:
            self.assertTrue(resources[resource_id]["official_url"].startswith("https://"))
            self.assertTrue(resources[resource_id]["license_note"])
            self.assertIn(resources[resource_id]["check"], {"python_module", "command"})

    def test_local_agent_guide_clearly_blocks_paid_or_automatic_use(self):
        text = (ROOT / "docs" / "LOCAL_AGENTIC_AI.md").read_text(encoding="utf-8").lower()
        self.assertIn("no paid api keys", text)
        self.assertIn("no automatic", text)
        self.assertIn("human review", text)
        self.assertIn("read-only", text)
        self.assertIn("model weights", text)

    def test_optional_resource_probe_is_documented(self):
        guide = (ROOT / "docs" / "OPTIONAL_FREE_VISION_TOOLS.md").read_text(encoding="utf-8")
        self.assertIn("tools/check_optional_resources.py", guide)
        self.assertTrue((ROOT / "tools" / "check_optional_resources.py").is_file())


if __name__ == "__main__":
    unittest.main()
