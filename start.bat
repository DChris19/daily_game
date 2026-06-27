@echo off
start "Backend" cmd /k "cd /d %~dp0 && venv\Scripts\activate && uvicorn main:app --reload --reload-dir auth --reload-dir goals"
start "Frontend" cmd /k "cd /d %~dp0FrontEnd && python -m http.server 3000"
timeout /t 2 /nobreak > nul
start http://localhost:3000/login.html
