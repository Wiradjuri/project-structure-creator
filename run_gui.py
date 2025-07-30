#!/usr/bin/env python3
"""
Desktop launcher for Project Structure Creator GUI
"""

import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from project_structure_creator.gui import run_gui
    
    if __name__ == "__main__":
        run_gui()
        
except ImportError as e:
    print(f"Error importing GUI module: {e}")
    print("Please ensure the project_structure_creator package is installed.")
    input("Press Enter to exit...")
except Exception as e:
    print(f"An error occurred: {e}")
    input("Press Enter to exit...")
