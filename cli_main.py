#!/usr/bin/env python3
"""
Main entry point for the Project Structure Creator CLI executable.
This script is specifically designed for PyInstaller packaging.
"""

import sys
import os

# Add the current directory to Python path for imports
if hasattr(sys, '_MEIPASS'):
    # When running as PyInstaller executable
    sys.path.insert(0, sys._MEIPASS)
else:
    # When running as regular Python script
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main entry point for CLI executable."""
    try:
        from project_structure_creator.main import main as cli_main
        cli_main()
    except ImportError as e:
        print(f"❌ Import Error: Failed to import CLI components: {e}")
        print("Please ensure the application is properly installed.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Application Error: An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
