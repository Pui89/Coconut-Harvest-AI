"""Documentation smoke tests: these do not validate model accuracy or physical robot safety."""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

# Keep these paths aligned with the current README and checked-in artwork.
ROBOT_CONCEPT_SVG = "docs/images/coconut-harvest-realistic-all-stage-concept.svg"
OVERVIEW_SVG = "docs/images/coconut-harvest-ai-overview.svg"


def test_core_project_evidence_files_exist():
    required = [
        "README.md",
        "docs/COMPLETE_SYSTEM_BLUEPRINT.md",
        "docs/VALIDATION_MATRIX.md",
        ROBOT_CONCEPT_SVG,
        OVERVIEW_SVG,
    ]
    missing = [path for path in required if not (ROOT / path).is_file()]
    assert not missing, f"Missing project evidence/documentation files: {missing}"


def test_readme_links_to_architecture_validation_and_visuals():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for relative_path in (
        "docs/COMPLETE_SYSTEM_BLUEPRINT.md",
        "docs/VALIDATION_MATRIX.md",
        ROBOT_CONCEPT_SVG,
        OVERVIEW_SVG,
    ):
        assert relative_path in readme, f"README should link to {relative_path}"


def test_concept_and_architecture_svgs_are_well_formed():
    for relative_path in (ROBOT_CONCEPT_SVG, OVERVIEW_SVG):
        root = ET.parse(ROOT / relative_path).getroot()
        assert root.tag.endswith("svg"), f"{relative_path} must have an SVG root element"


def test_readme_keeps_validation_boundary_explicit():
    readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
    assert "not validated" in readme or "not yet evidenced" in readme
    assert "physical harvesting" in readme
