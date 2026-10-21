@echo off
setlocal EnableExtensions
title Coconut Harvest AI - Dataset Validator
cd /d "%~dp0"

echo ============================================================
echo Coconut Harvest AI - Local Dataset Validator
echo ============================================================
echo.
echo This tool checks YOLO dataset folders and label syntax.
echo It does NOT train a model or measure model accuracy.
echo Your dataset stays on this computer; nothing is uploaded.
echo.

where python >nul 2>nul
if errorlevel 1 (
  echo ERROR: Python was not found on PATH.
  echo Install Python from https://www.python.org/downloads/windows/
  echo During installation, enable "Add python.exe to PATH".
  echo Then reopen this tool.
  echo.
  pause
  exit /b 2
)

python --version
if errorlevel 1 (
  echo ERROR: Python could not start.
  pause
  exit /b 2
)

echo.
echo Enter the FULL path to your dataset root folder.
echo That folder must contain images and labels folders, each with train, val, test.
echo Example: C:\data\coconut-dataset
echo.
set "DATASET_ROOT="
set /p "DATASET_ROOT=Dataset folder path: "
if not defined DATASET_ROOT (
  echo ERROR: No folder path entered.
  pause
  exit /b 2
)

set "DATASET_ROOT=%DATASET_ROOT:"=%"
if not exist "%DATASET_ROOT%\images" (
  echo ERROR: Cannot find an images folder inside:
  echo "%DATASET_ROOT%"
  echo Check the path and dataset layout, then run this tool again.
  echo.
  pause
  exit /b 2
)
if not exist "%DATASET_ROOT%\labels" (
  echo ERROR: Cannot find a labels folder inside:
  echo "%DATASET_ROOT%"
  echo Expected both images and labels folders.
  echo.
  pause
  exit /b 2
)

echo.
set "CLASS_COUNT=1"
set /p "CLASS_COUNT=Number of classes [1]: "
if not defined CLASS_COUNT set "CLASS_COUNT=1"

echo.
echo Running validator...
python "%~dp0apps\pui89_app\validate_coconut_dataset.py" --root "%DATASET_ROOT%" --classes %CLASS_COUNT% --output "%~dp0coconut_dataset_validation.json"
set "RESULT=%ERRORLEVEL%"

echo.
if "%RESULT%"=="0" (
  echo VALIDATION PASSED: structure and label syntax checks passed.
) else (
  echo VALIDATION DID NOT PASS. Read the errors above and in:
)
echo "%~dp0coconut_dataset_validation.json"
echo.
echo Note: a PASS does not prove labels are visually correct or that a model is accurate.
pause
exit /b %RESULT%
