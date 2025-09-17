#!/usr/bin/env python3
"""
Simple launcher for the Wikipedia to Notion GUI
"""

import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_setup():
    """Check if the project is properly set up"""
    # Check if virtual environment exists
    if not os.path.exists("venv"):
        print("❌ Virtual environment not found!")
        print("Please run the setup script first:")
        print("  • Mac/Linux: ./setup.sh")
        print("  • Windows: setup.bat")
        print("\nOr double-click the setup script to get started.")
        return False
    
    # Check if required files exist
    required_files = ["gui.py", "WTNI.py", "requirements.txt"]
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Required file not found: {file}")
            print("Make sure you're running this from the project directory.")
            return False
    
    return True

def main():
    """Main launcher function"""
    print("🚀 Starting Wikipedia to Notion Importer...")
    print()
    
    # Check setup
    if not check_setup():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Check if we're in a virtual environment
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Not running in virtual environment")
        print("For best results, activate the virtual environment first:")
        print("  • Mac/Linux: source venv/bin/activate")
        print("  • Windows: venv\\Scripts\\activate.bat")
        print()
    
    try:
        print("✅ Starting the app...")
        from gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"❌ Error importing GUI: {e}")
        print("\nThis usually means:")
        print("• tkinter is not installed (usually comes with Python)")
        print("• Some dependencies are missing")
        print("\nTry running the setup script again:")
        print("  • Mac/Linux: ./setup.sh")
        print("  • Windows: setup.bat")
        input("\nPress Enter to exit...")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running GUI: {e}")
        print("\nTry running the setup script again:")
        print("  • Mac/Linux: ./setup.sh")
        print("  • Windows: setup.bat")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
