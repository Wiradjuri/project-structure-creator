#!/usr/bin/env python3
"""
Main entry point for the Project Structure Creator GUI executable.
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
    """Main entry point for GUI executable."""
    try:
        from project_structure_creator.gui import run_gui
        run_gui()
    except ImportError as e:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror(
            "Import Error", 
            f"Failed to import GUI components: {e}\n\n"
            "Please ensure the application is properly installed."
        )
        sys.exit(1)
    except Exception as e:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror(
            "Application Error", 
            f"An unexpected error occurred: {e}"
        )
        sys.exit(1)

if __name__ == "__main__":
    main()
