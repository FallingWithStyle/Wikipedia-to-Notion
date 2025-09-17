@echo off
echo 🚀 Starting Wikipedia to Notion Importer...

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo Please run setup.bat first to install everything.
    echo.
    echo Double-click setup.bat to get started.
    echo.
    pause
    exit /b 1
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found!
    echo Please install Python from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo ✅ Starting the app...
echo.

REM Activate virtual environment and run GUI
call venv\Scripts\activate.bat
python gui.py

echo.
echo App closed. Press any key to exit.
pause
