# Project Structure Creator

A Python tool that parses text-based project structure descriptions and creates the corresponding directory and file structure. Available as both a command-line tool and a graphical desktop application.

## Features

- 📝 **Multiple Format Support**: Parse various structure formats (indented, tree, JSON, YAML, Markdown lists)
- 📁 Create directories and empty files based on the structure
- 🌳 Support for nested folder hierarchies with unlimited depth
- 💻 Command-line interface for automation and scripting
- 🖥️ Graphical user interface for easy interactive use
- 📋 Built-in structure preview and validation
- 🎯 Intelligent file type detection
- ⚡ Fast and efficient structure creation
- 🛡️ Comprehensive error handling and validation
- 🔍 Real-time input validation

## Supported Input Formats

### 1. Simple Indented Format

```text
project/
    src/
        main.py
        utils/
            config.py
    tests/
        test_main.py
    README.md
```

### 2. Tree Format (ASCII Art)

```text
project/
├── src/
│   ├── main.py
│   └── utils/
│       └── config.py
├── tests/
│   └── test_main.py
└── README.md
```

### 3. Markdown List Format

```markdown
- project/
  - src/
    - main.py
    - utils/
      - config.py
  - tests/
    - test_main.py
  - README.md
```

### 4. JSON Format

```json
  "project": {
    "src": ["main.py", "utils/config.py"],
    "tests": ["test_main.py"],
    "README.md": ""
  }
}
```

### 5. YAML Format (requires pyyaml)

```yaml
project:
  src:
    - main.py
    - utils:
        - config.py
  tests:
    - test_main.py
  README.md: ""
```

## Installation

```bash
pip install project-structure-creator
```

### Optional Dependencies

For YAML format support:

```bash
pip install project-structure-creator[yaml]
# or
pip install pyyaml
```

## Usage

### Command Line Interface

1. Create a structure file with your desired project structure using any supported format
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
