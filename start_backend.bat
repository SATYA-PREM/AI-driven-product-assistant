@echo off
echo ========================================================
echo Starting Customer Feedback AI Pipeline FastAPI Server...
echo ========================================================
cd /d "%~dp0"
echo Opening API Swagger Docs at http://127.0.0.1:8000/docs ...
start "" "http://127.0.0.1:8000/docs"
venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
pause
