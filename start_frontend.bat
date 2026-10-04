@echo off
echo ========================================================
echo Starting ProdIntel AI React Development Server...
echo ========================================================
cd /d "%~dp0frontend"
echo Opening browser at http://localhost:5173/ ...
start "" "http://localhost:5173/"
cmd.exe /c "npm run dev"
pause
