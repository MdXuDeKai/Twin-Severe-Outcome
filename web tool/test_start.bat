@echo off
REM Simple Test Script for Twin Prediction Tool

echo Testing Python installation...
python --version
if errorlevel 1 (
    echo Trying alternative Python commands...
    py --version
    if errorlevel 1 (
        python3 --version
        if errorlevel 1 (
            echo Python is not installed or not in PATH
            echo Please install Python 3.8+ from https://python.org
            echo Or try running: py app.py
            pause
            exit /b 1
        ) else (
            echo Found python3, using it...
            set PYTHON_CMD=python3
        )
    ) else (
        echo Found py command, using it...
        set PYTHON_CMD=py
    )
) else (
    echo Found python command, using it...
    set PYTHON_CMD=python
)

echo.
echo Testing pip installation...
pip --version
if errorlevel 1 (
    echo pip is not working properly
    pause
    exit /b 1
)

echo.
echo Testing if app.py exists...
if not exist "app.py" (
    echo app.py file not found in current directory
    echo Please make sure you are in the correct folder
    pause
    exit /b 1
)

echo.
echo Testing if requirements.txt exists...
if not exist "requirements.txt" (
    echo requirements.txt file not found
    pause
    exit /b 1
)

echo.
echo All checks passed! Starting the application...
echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting Flask application...
echo Open your browser and go to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

echo.
echo Application stopped.
pause
