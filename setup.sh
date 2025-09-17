#!/bin/bash
# Setup script for Wikipedia to Notion Importer

echo "🚀 Setting up Wikipedia to Notion Importer..."
echo "This will install everything you need to import Wikipedia articles into Notion."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3 from https://www.python.org/downloads/"
    echo "Then run this setup script again."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if python3 -m venv venv; then
    echo "✅ Virtual environment created successfully"
else
    echo "❌ Failed to create virtual environment"
    echo "Make sure you have write permissions in this directory"
    exit 1
fi

# Activate virtual environment and install dependencies
echo ""
echo "📥 Installing dependencies..."
source venv/bin/activate

if pip install -r requirements.txt; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    echo "Make sure you have an internet connection"
    exit 1
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📖 Next steps:"
echo "1. Get your Notion integration token from https://www.notion.so/my-integrations"
echo "2. Get your Notion page ID from any Notion page URL"
echo "3. Run the app:"
echo "   python3 run_gui.py"
echo ""
echo "Or double-click 'run_gui.py' to start the app!"
echo ""
echo "Need help? Check the Help tab in the app or read the README.md file."
