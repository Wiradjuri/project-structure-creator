# Project Structure Creator

A Python tool that parses text-based project structure descriptions and creates the corresponding directory and file structure.

## Features

- Parse indented text files describing project structures
- Create directories and empty files based on the structure
- Support for nested folder hierarchies
- Simple and intuitive text-based input format

## Installation

```bash
pip install project-structure-creator
```

## Usage

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
python -m project_structure_creator
```

Or use the command-line interface:

```bash
project-structure-creator
```

## License

MIT License
