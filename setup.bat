@echo off
echo 🚀 Setting up Wikipedia to Notion Importer...
echo This will install everything you need to import Wikipedia articles into Notion.
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed!
    echo Please install Python from https://www.python.org/downloads/
    echo Then run this setup script again.
    echo.
    pause
    exit /b 1
)

echo ✅ Python found:
python --version

REM Create virtual environment
echo.
echo 📦 Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    echo Make sure you have write permissions in this directory
    echo.
    pause
    exit /b 1
)
echo ✅ Virtual environment created successfully

REM Activate virtual environment and install dependencies
echo.
echo 📥 Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    echo Make sure you have an internet connection
    echo.
    pause
    exit /b 1
)
echo ✅ Dependencies installed successfully

echo.
echo 🎉 Setup complete!
echo.
echo 📖 Next steps:
echo 1. Get your Notion integration token from https://www.notion.so/my-integrations
echo 2. Get your Notion page ID from any Notion page URL
echo 3. Double-click 'run_gui.bat' to start the app!
echo.
echo Need help? Check the Help tab in the app or read the README.md file.
echo.
pause
