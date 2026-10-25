import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.check_optional_resources import build_report, probe_resource


class OptionalResourceProbeTests(unittest.TestCase):
    def test_detects_standard_library_module_without_importing_it(self):
        result = probe_resource(
            {
                "id": "stdlib-json",
                "name": "JSON",
                "check": "python_module",
                "module": "json",
                "distributions": [],
            }
        )
        self.assertEqual(result["status"], "available")
        self.assertIsNone(result["version"])

    def test_reports_missing_optional_module(self):
        result = probe_resource(
            {
                "id": "unlikely-module",
                "name": "Optional module",
                "check": "python_module",
                "module": "pui89_module_that_should_not_exist_9a71",
                "distributions": [],
            }
        )
        self.assertEqual(result["status"], "not_installed")

    def test_command_probe_checks_path_without_running_command(self):
        with patch("tools.check_optional_resources.shutil.which", return_value="/fake/tesseract"):
            result = probe_resource(
                {
                    "id": "tesseract",
                    "name": "Tesseract OCR",
                    "check": "command",
                    "command": "tesseract",
                }
            )
        self.assertEqual(result["status"], "available")
        self.assertNotIn("path", result)

    def test_manual_resource_is_not_assumed_to_be_installed(self):
        result = probe_resource(
            {
                "id": "cvat",
                "name": "CVAT Community",
                "check": "manual",
            }
        )
        self.assertEqual(result["status"], "manual_check")

    def test_unknown_check_type_is_rejected(self):
        with self.assertRaises(ValueError):
            probe_resource({"id": "bad", "check": "not-a-check"})

    def test_report_discloses_no_network_or_install_actions(self):
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "resources.json"
            config_path.write_text(
                json.dumps(
                    {
                        "project": "unit-test",
                        "resources": [
                            {
                                "id": "cvat",
                                "name": "CVAT",
                                "check": "manual",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            report = build_report(config_path)

        self.assertEqual(report["project"], "unit-test")
        self.assertFalse(report["network_access_used"])
        self.assertFalse(report["packages_installed"])
        self.assertFalse(report["models_downloaded"])
        self.assertEqual(report["resources"][0]["status"], "manual_check")
        self.assertNotIn("home", report)
        self.assertNotIn("absolute_path", report)


if __name__ == "__main__":
    unittest.main()
