@echo off
title Project Structure Creator GUI
echo Starting Project Structure Creator GUI...
echo.

:: Try to run with Python
python "%~dp0run_gui.py"
if errorlevel 1 (
    echo.
    echo Error: Could not start the application.
    echo Please ensure Python is installed and in your PATH.
    echo.
    pause
)
