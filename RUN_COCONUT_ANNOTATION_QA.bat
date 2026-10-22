@echo off
setlocal
title PUI89 Coconut Annotation QA
cd /d "%~dp0"

echo.
echo PUI89 Coconut Harvest AI - local annotation QA
echo This tool runs locally. It does not upload images or train a detector.
echo.
if not exist "tools\coconut_annotator.html" (
  echo ERROR: Run this file from the extracted Coconut-Harvest-AI repository.
  pause
  exit /b 1
)

echo Opening the offline annotator in your browser...
start "" "tools\coconut_annotator.html"
echo.
echo 1. Select images you are permitted to use.
echo 2. Draw boxes around clearly visible individual coconuts.
echo 3. Export annotation JSON to a known location, for example Documents.
echo 4. Return here after exporting.
echo.
set /p "ANNOTATIONS=Enter full path to exported annotation JSON: "
if "%ANNOTATIONS%"=="" (
  echo ERROR: No annotation path supplied.
  pause
  exit /b 1
)
if not exist "%ANNOTATIONS%" (
  echo ERROR: File not found: "%ANNOTATIONS%"
  echo Tip: Use the full path, for example C:\Users\YourName\Documents\coconut-annotations.json
  pause
  exit /b 1
)

if not exist "data\human_review" mkdir "data\human_review"
set "AUDIT=data\human_review\annotation-geometry-audit.json"
echo.
echo Running geometry checks. These checks do NOT confirm label correctness.
python "tools\audit_coconut_annotations.py" --annotations "%ANNOTATIONS%" --output "%AUDIT%"
if errorlevel 1 (
  echo.
  echo Geometry audit reported errors or could not read the file.
  echo Inspect the output above and fix the annotation JSON before conversion.
  echo Audit report: "%AUDIT%"
  pause
  exit /b 1
)

echo.
echo Geometry checks completed. Human review is still required.
echo Open every image at full resolution and verify every box, missed coconut,
echo truncated-object policy, and image usage permission/licence.
echo Only answer Y if you personally completed those checks.
set /p "HUMANQA=Have you completed visual label QA AND confirmed image-use permissions? (Y/N): "
if /I not "%HUMANQA%"=="Y" (
  echo.
  echo Conversion skipped. Keep labels as drafts until human QA and rights review are complete.
  echo Geometry audit: "%AUDIT%"
  pause
  exit /b 0
)

set "OUTPUT=data\human_review\ground_truth.csv"
echo.
echo Creating evaluator-ready CSV at "%OUTPUT%"...
python "tools\annotations_to_ground_truth_csv.py" --annotations "%ANNOTATIONS%" --output "%OUTPUT%" --confirm-human-qa --summary "data\human_review\ground_truth-summary.json"
if errorlevel 1 (
  echo.
  echo Conversion failed. Review the error above. No detector was run.
  pause
  exit /b 1
)

echo.
echo SUCCESS: CSV created at "%OUTPUT%"
echo This is human-reviewed ground truth, not detector output or model performance evidence.
echo Keep original image provenance and ensure the image IDs match your evaluation predictions.
pause
