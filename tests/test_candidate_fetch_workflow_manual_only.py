"""Guard the no-surprise-cost policy for external candidate downloads."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "fetch-coconut-candidates.yml"


class CandidateFetchWorkflowPolicyTests(unittest.TestCase):
    def test_external_image_download_is_manual_only(self) -> None:
        source = WORKFLOW.read_text(encoding="utf-8")
        trigger_block = source.split("\non:", maxsplit=1)[1].split(
            "\npermissions:", maxsplit=1
        )[0]

        self.assertRegex(trigger_block, r"(?m)^\s{2}workflow_dispatch:\s*$")
        self.assertNotRegex(trigger_block, r"(?m)^\s{2}(?:push|schedule):\s*$")
        self.assertIn("if: github.event_name == 'workflow_dispatch'", source)


if __name__ == "__main__":
    unittest.main()
