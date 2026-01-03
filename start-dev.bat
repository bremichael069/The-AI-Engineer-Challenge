@echo off
echo Starting Mental Coach Application...
echo.
echo This will start both the backend and frontend servers.
echo.
echo Make sure you have:
echo   1. Python 3.12+ and uv installed
echo   2. Node.js 18+ and npm installed
echo   3. OPENAI_API_KEY environment variable set
echo.
pause

echo.
echo Starting Backend API server...
echo Loading environment variables from .env file...
for /f "usebackq tokens=1,2 delims==" %%a in ("%~dp0.env") do (
    if "%%a"=="OPENAI_API_KEY" set OPENAI_API_KEY=%%b
)
start "Backend API" cmd /k "cd /d %~dp0 && set OPENAI_API_KEY=%OPENAI_API_KEY% && uv run uvicorn api.index:app --reload"

timeout /t 3 /nobreak >nul

echo.
echo Starting Frontend development server...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit this window (servers will continue running)...
pause >nul

