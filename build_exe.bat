@echo off
REM Build script for Project Structure Creator executables

echo Building Project Structure Creator executables...
echo.

REM Clean previous builds
if exist "build" rmdir /s /q "build"
if exist "dist\ProjectStructureCreator-CLI.exe" del "dist\ProjectStructureCreator-CLI.exe"
if exist "dist\ProjectStructureCreator-GUI.exe" del "dist\ProjectStructureCreator-GUI.exe"

REM Build executables
echo Running PyInstaller...
pyinstaller build_exe.spec --clean

REM Check if build was successful
if exist "dist\ProjectStructureCreator-CLI.exe" (
    echo.
    echo ✅ CLI executable built successfully: dist\ProjectStructureCreator-CLI.exe
) else (
    echo.
    echo ❌ CLI executable build failed!
    exit /b 1
)

if exist "dist\ProjectStructureCreator-GUI.exe" (
    echo ✅ GUI executable built successfully: dist\ProjectStructureCreator-GUI.exe
) else (
    echo ❌ GUI executable build failed!
    exit /b 1
)

echo.
echo 🎉 Build complete! Both executables are ready in the dist\ folder.
echo.
echo You can now run:
echo   - dist\ProjectStructureCreator-GUI.exe (for GUI mode)
echo   - dist\ProjectStructureCreator-CLI.exe --help (for CLI help)
echo.
pause
