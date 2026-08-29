@echo off
echo Starting CSV Pipeline Server...
cd /d "C:\Users\belam\Downloads\csv-pipeline"
call venv\Scripts\activate
start http://127.0.0.1:8000/docs
uvicorn app.main:app --reload