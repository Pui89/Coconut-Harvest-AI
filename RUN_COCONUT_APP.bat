@echo off
setlocal
cd /d "%~dp0"

echo.
echo PUI89 Coconut Harvest AI - local launcher
echo =========================================
echo Repository folder: %CD%
echo.

where python >nul 2>nul
if errorlevel 1 (
  echo ERROR: Python was not found on PATH.
  echo Install Python 3.10-3.12 from https://www.python.org/downloads/
  echo During installation, enable "Add python.exe to PATH".
  pause
  exit /b 1
)

python --version
if errorlevel 1 (
  echo ERROR: Python could not start.
  pause
  exit /b 1
)

if not exist "apps\pui89_app\web_demo.py" (
  echo ERROR: App files were not found. This launcher should be inside the repository root.
  pause
  exit /b 1
)

python -c "import streamlit" >nul 2>nul
if errorlevel 1 (
  echo Streamlit is not installed in the active Python environment.
  echo To install the free local app dependencies, run:
  echo   python -m pip install -r apps\pui89_app\requirements.txt
  echo Then run this launcher again.
  pause
  exit /b 1
)

echo Starting the local app. No hosted API or cloud inference is used by this launcher.
echo Keep this window open while using the app. Press Ctrl+C here to stop it.
echo.
python -m streamlit run apps\pui89_app\web_demo.py
if errorlevel 1 (
  echo.
  echo The app exited with an error. Read the message above to troubleshoot.
  pause
  exit /b 1
)
endlocal
