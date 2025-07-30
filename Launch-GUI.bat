@echo off
REM Desktop launcher for Project Structure Creator GUI
REM Place this file on your desktop for easy access

echo Starting Project Structure Creator...

REM Try to find the executable in common locations
if exist "%~dp0ProjectStructureCreator-GUI.exe" (
    start "" "%~dp0ProjectStructureCreator-GUI.exe"
) else if exist "%~dp0dist\ProjectStructureCreator-GUI.exe" (
    start "" "%~dp0dist\ProjectStructureCreator-GUI.exe"
) else (
    echo Error: ProjectStructureCreator-GUI.exe not found!
    echo.
    echo Please ensure the executable is in the same directory as this launcher,
    echo or in a 'dist' subdirectory.
    echo.
    pause
)
