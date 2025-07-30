# Project Structure Creator

A Python tool that parses text-based project structure descriptions and creates the corresponding directory and file structure. Available as both a command-line tool and a graphical desktop application.

## Features

- 📝 Parse indented text files describing project structures
- 📁 Create directories and empty files based on the structure
- 🌳 Support for nested folder hierarchies
- 💻 Command-line interface for automation
- 🖥️ Graphical user interface for easy use
- 📋 Built-in structure preview
- 🎯 Simple and intuitive text-based input format

## Installation

```bash
pip install project-structure-creator
```

## Usage

### Command Line Interface

1. Create a `structure.txt` file with your desired project structure:

```text
project/
    src/
        main.py
        utils/
            helpers.py
    tests/
        test_main.py
    README.md
```

2. Run the tool:

```bash
project-structure-creator structure.txt output_folder
```

Or use the module directly:

```bash
python -m project_structure_creator structure.txt output_folder
```

### Graphical User Interface

Launch the GUI application:

```bash
project-structure-creator --gui
```

Or use the dedicated GUI command:

```bash
project-structure-creator-gui
```

Or run the module with GUI flag:

```bash
python -m project_structure_creator --gui
```

The GUI provides:

- ✨ Interactive text editor with syntax highlighting
- 📂 File browser for loading structure files
- 👀 Live preview of the structure to be created
- 🎯 Point-and-click directory selection
- ✅ Real-time validation and error reporting

### Development Mode

For development, you can run the GUI directly:

```bash
python run_gui.py
```

Or on Windows, double-click `run_gui.bat`.

## Structure Format

The tool uses a simple indented text format:

```text
project_name/
    folder1/
        file1.py
        file2.txt
        subfolder/
            file3.js
    folder2/
        file4.md
    root_file.txt
```

- Use 4 spaces for each indentation level
- Folders should end with `/`
- Files are any line that doesn't end with `/`
- Empty lines are ignored

## Command Line Options

```bash
project-structure-creator [OPTIONS] [INPUT_FILE] [OUTPUT_DIR]

Options:
  --gui         Launch the graphical user interface
  --version     Show version information
  --help        Show help message

Arguments:
  INPUT_FILE    Input file containing structure (default: structure.txt)
  OUTPUT_DIR    Output directory (required for CLI mode)
```

## Examples

### Basic Usage

```bash
project-structure-creator my_structure.txt ~/Desktop/my_project
project-structure-creator structure.txt C:\Users\username\Documents\my_project
```

### GUI Mode

```bash
project-structure-creator --gui
```

## License

MIT License
