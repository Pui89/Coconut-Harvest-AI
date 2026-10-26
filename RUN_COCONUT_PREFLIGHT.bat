@echo off
setlocal EnableExtensions
title Coconut Harvest AI - Read-only Dataset Preflight
cd /d "%~dp0"

echo ============================================================
echo Coconut Harvest AI - Read-only Dataset Preflight
echo ============================================================
echo.
echo Free and local. This does not install packages or download models.
echo It does not edit annotations, ledgers, hashes, or approval flags.
echo Geometry checks cannot replace human visual review.
echo.

where python >nul 2>nul
if errorlevel 1 (
  echo ERROR: Python was not found on PATH. No installation was attempted.
  echo Please use a Python installation already available on this computer.
  exit /b 2
)

if not exist "tools\run_coconut_dataset_preflight.py" (
  echo ERROR: This project copy does not include the current preflight tool.
  echo It may be an older ZIP snapshot. No files were changed.
  echo Check the latest project files at:
  echo https://github.com/Pui89/Coconut-Harvest-AI
  exit /b 2
)
if not exist "data\review_batch_2026-10-22\ai_annotation_draft_NOT_FOR_TRAINING.json" (
  echo ERROR: Candidate 0032 draft is missing from this project copy.
  echo No files were changed.
  exit /b 2
)
if not exist "data\review_batch_2026-10-18\source_rights_audit_2026-10-19.csv" (
  echo ERROR: Source-rights ledger is missing. No files were changed.
  exit /b 2
)
if not exist "data\review_batch_2026-10-18\candidate_review_2026-10-18.csv" (
  echo ERROR: Candidate-review ledger is missing. No files were changed.
  exit /b 2
)

if not exist "reports" mkdir "reports"
if not exist "reports" (
  echo ERROR: Could not create the reports folder.
  exit /b 2
)

echo Python version:
python --version
echo.
echo Running read-only checks. The dataset may correctly remain BLOCKED.
echo.

python "tools\run_coconut_dataset_preflight.py" --annotations "data\review_batch_2026-10-22\ai_annotation_draft_NOT_FOR_TRAINING.json" --rights-csv "data\review_batch_2026-10-18\source_rights_audit_2026-10-19.csv" --review-csv "data\review_batch_2026-10-18\candidate_review_2026-10-18.csv" --output "reports\coconut-dataset-preflight-report.json"
set "RESULT=%ERRORLEVEL%"

echo.
if exist "reports\coconut-dataset-preflight-report.json" (
  echo Report saved to:
  echo %CD%\reports\coconut-dataset-preflight-report.json
) else (
  echo ERROR: No report was produced. Review the Python error above.
  exit /b 2
)
echo.
echo A non-zero result can be expected while required reviews or approvals are incomplete.
echo Do not approve any image based on geometry or ledger checks alone.
echo No training was run and no detector accuracy was measured.
echo.
exit /b %RESULT%
