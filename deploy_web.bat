@echo off
echo Deploying Face Recognition System as Web Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please run install.bat first
    pause
    exit /b 1
)

REM Install Flask for web deployment
echo Installing Flask for web deployment...
pip install flask

echo.
echo Starting web server...
echo Open your browser and go to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python web_deploy.py

pause

