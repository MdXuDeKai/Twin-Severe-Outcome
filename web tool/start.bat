@echo off
REM Startup Script - Twin Severe Outcome Prediction Web Diagnostic Tool

echo 🚀 Starting Twin Severe Outcome Prediction Web Diagnostic Tool...
echo.

REM Check Python environment
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python environment not found, please install Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python environment check passed
echo.

REM Install dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Error: Dependency installation failed
    pause
    exit /b 1
)

echo ✅ Dependencies installation completed
echo.

REM Start application
echo 🌐 Starting Web application...
echo Access URL: http://localhost:5000
echo Press Ctrl+C to stop service
echo.

python app.py

pause


