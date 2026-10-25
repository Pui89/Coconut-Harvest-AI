import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.run_agentic_workflow import main, parse_observation


class AgenticWorkflowCliTests(unittest.TestCase):
    def test_parse_observation_requires_json_object(self):
        self.assertEqual(parse_observation('{"ok": true}'), {"ok": True})
        with self.assertRaises(ValueError):
            parse_observation("[]")
        with self.assertRaises(ValueError):
            parse_observation("NaN")

    def test_cli_reads_file_and_emits_machine_readable_proposal(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "observation.json"
            path.write_text('{"sensor_ok": false}', encoding="utf-8")
            output = io.StringIO()
            errors = io.StringIO()
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                result = main(["--input", str(path)])

        self.assertEqual(result, 0)
        self.assertEqual(errors.getvalue(), "")
        report = json.loads(output.getvalue())
        self.assertEqual(report["status"], "PROPOSAL_READY_FOR_HUMAN_REVIEW")
        self.assertEqual(report["decision"]["status"], "STOP")
        self.assertTrue(report["human_review_required"])
        self.assertFalse(report["execution_performed"])
        self.assertFalse(report["network_access_used"])
        self.assertFalse(report["model_inference_used"])
        self.assertFalse(report["actuator_commands_issued"])

    def test_cli_reads_from_stdin(self):
        output = io.StringIO()
        errors = io.StringIO()
        with (
            patch("sys.stdin", io.StringIO("{}")),
            contextlib.redirect_stdout(output),
            contextlib.redirect_stderr(errors),
        ):
            result = main(["--input", "-"])

        self.assertEqual(result, 0)
        self.assertEqual(errors.getvalue(), "")
        self.assertEqual(
            json.loads(output.getvalue())["status"],
            "PROPOSAL_READY_FOR_HUMAN_REVIEW",
        )

    def test_cli_invalid_json_returns_two_and_does_not_emit_report(self):
        output = io.StringIO()
        errors = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.json"
            path.write_text("{nope}", encoding="utf-8")
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                result = main(["--input", str(path)])

        self.assertEqual(result, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("invalid JSON", errors.getvalue())

    def test_cli_missing_file_returns_two_without_leaking_absolute_path(self):
        output = io.StringIO()
        errors = io.StringIO()
        with (
            contextlib.redirect_stdout(output),
            contextlib.redirect_stderr(errors),
        ):
            result = main(["--input", "/private/example/missing.json"])

        self.assertEqual(result, 2)
        self.assertEqual(output.getvalue(), "")
        self.assertIn("missing.json", errors.getvalue())
        self.assertNotIn("/private/example", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
