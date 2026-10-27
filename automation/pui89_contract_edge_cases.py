"""Additional local-only safety edge cases for the PUI89 proposal gate.

Run manually from the repository root:
    python automation/pui89_contract_edge_cases.py

Uses only the Python standard library. It performs no network access, installs,
model downloads, report uploads, or physical robot actions.
"""
from __future__ import annotations
import importlib.util
from pathlib import Path
import unittest

MODULE_PATH = Path(__file__).with_name("pui89_contract_smoke.py")
_SPEC = importlib.util.spec_from_file_location("pui89_contract_smoke", MODULE_PATH)
if _SPEC is None or _SPEC.loader is None:
    raise RuntimeError("Cannot load local proposal gate")
_MODULE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MODULE)
check_proposal = _MODULE.check_proposal

class ProposalGateEdgeCases(unittest.TestCase):
    def test_blank_and_non_string_actions_fail_closed(self):
        for action in (None, {}, [], "   "):
            with self.subTest(action=action):
                ok, reason = check_proposal({"action": action, "confidence": 0.9, "simulation_only": True}, True)
                self.assertFalse(ok)
                self.assertEqual(reason, "empty_action")

    def test_truthy_but_unknown_state_fails_closed(self):
        ok, reason = check_proposal({"action": "observe", "confidence": 0.9, "simulation_only": True}, "unknown")
        self.assertFalse(ok)
        self.assertEqual(reason, "unknown_world_state")

    def test_truthy_human_approval_fails_closed(self):
        proposal = {"action": "review_case", "confidence": 0.9, "requires_human_approval": True, "simulation_only": True}
        ok, reason = check_proposal(proposal, True, human_approved="yes")
        self.assertFalse(ok)
        self.assertEqual(reason, "human_approval_required")

if __name__ == "__main__":
    result = unittest.main(verbosity=2)
