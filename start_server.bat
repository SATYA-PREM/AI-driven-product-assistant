@echo off
title Customer Feedback AI Pipeline Server
color 0A
cd /d "C:\Users\belam\Downloads\csv-pipeline"

echo ============================================================
echo   Starting Customer Feedback AI Pipeline (Milestone 2)
echo ============================================================
echo.

if not exist "venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found in %CD%\venv
    pause
    exit /b 1
)

echo [1/2] Launching background browser watcher...
REM This watcher waits until the server is 100%% ready before opening the browser
start "" powershell -WindowStyle Hidden -Command "$sw = [System.Diagnostics.Stopwatch]::StartNew(); while ($sw.Elapsed.TotalSeconds -lt 45) { Start-Sleep -Milliseconds 800; try { $res = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/health' -TimeoutSec 1; if ($res.api -eq 'ok') { Start-Process 'http://127.0.0.1:8000/'; break } } catch {} }"

echo [2/2] Starting Uvicorn Web Server (takes ~10s to load libraries)...
echo.
echo ============================================================
echo   Local Dashboard:  http://127.0.0.1:8000/
echo   Swagger API Docs: http://127.0.0.1:8000/docs
echo   Status: Loading AI dependencies... Browser will auto-open when ready!
echo   To Stop Server:   Press CTRL + C
echo ============================================================
echo.

venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

if errorlevel 1 (
    echo.
    echo ============================================================
    echo   [ERROR] The server stopped unexpectedly.
    echo   See the error log above.
    echo ============================================================
    pause
)