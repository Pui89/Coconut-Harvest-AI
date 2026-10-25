"""Contract tests for the offline HTML coconut annotator."""
from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
ANNOTATOR = ROOT / "tools" / "coconut_annotator.html"


def script_source() -> str:
    html = ANNOTATOR.read_text(encoding="utf-8")
    scripts = re.findall(r"<script>(.*?)</script>", html, flags=re.DOTALL | re.IGNORECASE)
    assert len(scripts) == 1, "Expected one inline script in the offline annotator"
    return scripts[0]


def test_export_keeps_review_and_training_unapproved():
    source = script_source()
    assert "human_qa_acknowledged:false" in source
    assert "training_approved:false" in source
    assert "not independently QA-approved" in source
    assert "not approved for training or benchmarking" in source


def test_source_metadata_is_preserved_only_for_matching_single_image():
    source = script_source()
    assert "importedSource={...sourceCandidate}" in source
    assert "payload.images.length===1&&restored===1" in source
    assert "restoredFiles.has(sourceCandidate.filename)" in source
    assert "const singleSource=items.length===1&&importedSource&&importedSource.filename===items[0].file.name" in source
    assert "payload.source={...importedSource,filename:items[0].file.name}" in source


def test_new_image_selection_clears_previous_source_metadata():
    source = script_source()
    assert "items=[];importedSource=null;importedAnnotationNotes=[];" in source


@pytest.mark.skipif(shutil.which("node") is None, reason="Node.js is not installed; JavaScript syntax check skipped")
def test_inline_javascript_parses_without_execution():
    source = script_source()
    with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as handle:
        handle.write(source)
        path = Path(handle.name)
    try:
        run = subprocess.run(
            [shutil.which("node"), "--check", str(path)],
            capture_output=True,
            text=True,
            check=False,
            timeout=10,
        )
        assert run.returncode == 0, run.stderr or run.stdout
    finally:
        path.unlink(missing_ok=True)
