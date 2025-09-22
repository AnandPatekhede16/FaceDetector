@echo off
echo ========================================
echo    FACE RECOGNITION SYSTEM INSTALLER
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo.
    echo IMPORTANT: During installation, check "Add Python to PATH"
    echo.
    echo After installing Python:
    echo 1. Restart this command prompt
    echo 2. Run this script again
    echo.
    echo Opening Python download page...
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Python found! Version:
python --version
echo.

echo Installing dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Error installing dependencies. Trying with --user flag...
    pip install --user -r requirements.txt
)

echo.
echo Testing the system...
python test_simple.py

echo.
echo System ready! You can now run:
echo   python run_simple.py
echo   python simple_register.py
echo.
pause

