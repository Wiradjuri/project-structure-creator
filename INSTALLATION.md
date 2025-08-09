# Project Structure Creator - Installation & Usage Guide

## 📦 What's Included

Your Project Structure Creator now comes in multiple formats:

### 🖥️ Standalone Executables (Recommended for Users)

- **ProjectStructureCreator-GUI.exe** - Double-click to run the graphical interface
- **ProjectStructureCreator-CLI.exe** - Command-line version for automation
- **No Python installation required!**

### 🐍 Python Packages (For Developers)

- **project_structure_creator-0.1.0-py3-none-any.whl** - Installable Python package
- **project_structure_creator-0.1.0.tar.gz** - Source distribution

## 🚀 Quick Start

### Option 1: Use the GUI Executable (Easiest)

1. Navigate to the `dist/` folder
2. Double-click `ProjectStructureCreator-GUI.exe`
3. The application opens with an example project structure
4. Click "Browse" to select where you want to create your project
5. Click "Generate Project Structure"

### Option 2: Use the CLI Executable

```bash
# Open Command Prompt or PowerShell in the dist/ folder
ProjectStructureCreator-CLI.exe structure.txt C:\path\to\your\project

# Example
ProjectStructureCreator-CLI.exe structure.txt C:\Users\%USERNAME%\Desktop\MyNewProject
```

### Option 3: Install as Python Package

```bash
pip install project_structure_creator-0.1.0-py3-none-any.whl

# Then use commands
project-structure-creator --gui
project-structure-creator structure.txt output_folder
```

## 📁 Distribution

### For End Users (No Python Knowledge)

- Copy the entire `dist/` folder to any location
- Share `ProjectStructureCreator-GUI.exe` - it runs standalone
- Include `structure.txt` file with your desired project template

### For Developers

- Share the `.whl` file for pip installati on
- Include source code for customization

### For Teams/Organizations

- Place executables on shared network drives
- Create custom structure templates in `.txt` files
- Use CLI version in build scripts and automation

## 🎯 Use Cases

### Project Templates

Create standardized project structures for:

- Python projects with virtual environments
- Web development setups (React, Vue, etc.)
- Documentation structures
- Data science projects
- Microservice architectures

### Automation

- Include CLI in build scripts
- Generate project scaffolding in CI/CD pipelines
- Batch create multiple similar projects

### Team Standardization

- Ensure consistent project layouts across teams
- Distribute company-specific templates
- Version control structure definitions

## 🔧 Customization

### Creating Custom Templates

1. Create a new `.txt` file with your structure:

```
my_api_project/
    src/
        controllers/
            auth.py
            users.py
        models/
            __init__.py
            user.py
        utils/
            database.py
            helpers.py
    tests/
        test_auth.py
        test_users.py
    requirements.txt
    README.md
    .env.example
```

2. Use with either executable:
   - GUI: Load your custom file using "Load from File"
   - CLI: `ProjectStructureCreator-CLI.exe your_template.txt output_path`

## 📊 File Sizes

- CLI Executable: ~13-15 MB
- GUI Executable: ~15-18 MB  
- Python Wheel: ~15 KB

## ⚠️ Security Notes

- Executables may trigger antivirus warnings (false positive from PyInstaller)
- Add to antivirus exclusions if needed
- Executables are self-contained and don't modify system files

## 🐛 Troubleshooting

### "Windows protected your PC" message

- Click "More info" → "Run anyway"
- This is normal for unsigned executables

### GUI doesn't start

- Try running from command prompt to see error messages
- Ensure Windows 10/11 64-bit system

### CLI shows "not recognized" error

- Use full path: `C:\path\to\ProjectStructureCreator-CLI.exe`
- Or run from the directory containing the executable

---

**Need help?** Check the main README.md for more detailed information and examples.
