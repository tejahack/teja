@echo off
echo Windows App Lock Manager - Installation Script
echo =============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found. Installing dependencies...
echo.

REM Install required packages
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ✅ Installation completed successfully!
echo.
echo To run the application:
echo   python main.py
echo.
echo For best results, run as Administrator:
echo   1. Open Command Prompt as Administrator
echo   2. Navigate to this folder
echo   3. Run: python main.py
echo.
echo Default password: admin123
echo (Change this immediately in Settings after first run)
echo.
pause