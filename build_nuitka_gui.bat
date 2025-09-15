@echo off
REM Nuitka build script for Project Structure Creator GUI

echo Building Project Structure Creator GUI with Nuitka...
echo.

REM Clean previous builds
if exist "dist\ProjectStructureCreator-GUI.exe" del "dist\ProjectStructureCreator-GUI.exe"
if exist "gui_main.dist" rmdir /s /q "gui_main.dist"
if exist "gui_main.build" rmdir /s /q "gui_main.build"

REM Create dist directory if it doesn't exist
if not exist "dist" mkdir "dist"

echo Running Nuitka for GUI version...
python -m nuitka ^
    --standalone ^
    --onefile ^
    --output-dir=dist ^
    --output-filename=ProjectStructureCreator-GUI.exe ^
    --windows-disable-console ^
    --enable-plugin=tk-inter ^
    --include-package=project_structure_creator ^
    --include-module=pyyaml ^
    --follow-import-to=tkinter ^
    --assume-yes-for-downloads ^
    --show-progress ^
    --show-memory ^
    gui_main.py

REM Check if build was successful
if exist "dist\ProjectStructureCreator-GUI.exe" (
    echo.
    echo ✅ GUI executable built successfully: dist\ProjectStructureCreator-GUI.exe

    REM Get file size
    for %%I in ("dist\ProjectStructureCreator-GUI.exe") do set size=%%~zI
    set /a size_mb=!size!/1024/1024
    echo 📊 File size: !size_mb! MB
) else (
    echo.
    echo ❌ GUI executable build failed!
    exit /b 1
)

echo.
echo 🎉 GUI build complete!
echo.
echo You can now run: dist\ProjectStructureCreator-GUI.exe
echo.
