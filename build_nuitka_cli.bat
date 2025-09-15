@echo off
REM Nuitka build script for Project Structure Creator CLI

echo Building Project Structure Creator CLI with Nuitka...
echo.

REM Clean previous builds
if exist "dist\ProjectStructureCreator-CLI.exe" del "dist\ProjectStructureCreator-CLI.exe"
if exist "cli_main.dist" rmdir /s /q "cli_main.dist"
if exist "cli_main.build" rmdir /s /q "cli_main.build"

REM Create dist directory if it doesn't exist
if not exist "dist" mkdir "dist"

echo Running Nuitka for CLI version...
python -m nuitka ^
    --standalone ^
    --onefile ^
    --output-dir=dist ^
    --output-filename=ProjectStructureCreator-CLI.exe ^
    --windows-console-mode=force ^
    --enable-plugin=tk-inter ^
    --include-package=project_structure_creator ^
    --include-module=pyyaml ^
    --nofollow-import-to=tkinter ^
    --assume-yes-for-downloads ^
    --show-progress ^
    --show-memory ^
    cli_main.py

REM Check if build was successful
if exist "dist\ProjectStructureCreator-CLI.exe" (
    echo.
    echo ✅ CLI executable built successfully: dist\ProjectStructureCreator-CLI.exe

    REM Get file size
    for %%I in ("dist\ProjectStructureCreator-CLI.exe") do set size=%%~zI
    set /a size_mb=!size!/1024/1024
    echo 📊 File size: !size_mb! MB
) else (
    echo.
    echo ❌ CLI executable build failed!
    exit /b 1
)

echo.
echo 🎉 CLI build complete!
echo.
echo You can now run: dist\ProjectStructureCreator-CLI.exe --help
echo.
pause
