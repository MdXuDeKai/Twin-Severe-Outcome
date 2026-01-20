@echo off
REM Fixed Python Detection Script

echo Testing Python installation...
echo.

REM Try different Python commands
python --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Found 'python' command
    set PYTHON_CMD=python
    goto :found_python
)

py --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Found 'py' command
    set PYTHON_CMD=py
    goto :found_python
)

python3 --version >nul 2>&1
if not errorlevel 1 (
    echo ✅ Found 'python3' command
    set PYTHON_CMD=python3
    goto :found_python
)

echo ❌ Python not found in PATH
echo.
echo Please try one of these solutions:
echo 1. Install Python from https://python.org (make sure to check "Add to PATH")
echo 2. Try running: py app.py
echo 3. Use the static demo version: demo.html
echo.
pause
exit /b 1

:found_python
echo.
echo Testing pip installation...
%PYTHON_CMD% -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip not working properly
    echo Try running: %PYTHON_CMD% -m pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✅ pip is working
echo.

echo Testing files...
if not exist "app.py" (
    echo ❌ app.py not found
    echo Please make sure you are in the correct directory
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo ❌ requirements.txt not found
    pause
    exit /b 1
)

echo ✅ All files found
echo.

echo Installing dependencies...
%PYTHON_CMD% -m pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Dependency installation failed
    echo Try running manually: %PYTHON_CMD% -m pip install flask scikit-learn pandas numpy shap
    pause
    exit /b 1
)

echo ✅ Dependencies installed
echo.

echo Starting Flask application...
echo Open your browser and go to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

%PYTHON_CMD% app.py

echo.
echo Application stopped.
pause
