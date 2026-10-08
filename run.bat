@echo off
pushd "%~dp0"
set "PYTHON=%CD%\..\venv\Scripts\python.exe"
if not exist "%PYTHON%" (
    echo Virtual environment not found at "%PYTHON%".
    pause
    popd
    exit /b 1
)
REM Windows: starts backend in a new window, then the frontend
start "LegalEase API" cmd /k ""%PYTHON%" -m uvicorn legalEaseAPI.main:app --reload --port 8000"
timeout /t 4 >nul
"%PYTHON%" -m streamlit run frontend/app.py
popd
