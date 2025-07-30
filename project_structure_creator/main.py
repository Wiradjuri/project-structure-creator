"""
Main module for Project Structure Creator
"""

import os
import sys
from typing import List, Tuple


def parse_structure(lines: List[str]) -> List[Tuple[str, bool]]:
    """
    Parse a list of lines representing a project structure.
    
    Args:
        lines: List of strings representing the project structure
        
    Returns:
        List of tuples (path, is_directory)
    """
    stack = []
    paths = []

    for line in lines:
        stripped = line.lstrip()
        depth = (len(line) - len(stripped)) // 4  # 4 spaces per indent
        name = stripped.replace('├── ', '').replace('└── ', '').replace('│   ', '')

        # Determine current parent based on depth
        while len(stack) > depth:
            stack.pop()

        current_path = os.path.join(*(stack + [name]))
        paths.append((current_path, name.endswith('/')))
        
        if name.endswith('/'):
            stack.append(name[:-1])
        elif '.' not in name:  # Folder without trailing slash
            stack.append(name)

    return paths


def create_structure(base_path: str, structure_lines: List[str]) -> None:
    """
    Create the project structure based on the parsed lines.
    
    Args:
        base_path: Base directory where the structure will be created
        structure_lines: List of strings representing the structure
    """
    paths = parse_structure(structure_lines)
    
    for path, is_dir in paths:
        full_path = os.path.join(base_path, path)
        
        if is_dir:
            os.makedirs(full_path, exist_ok=True)
            print(f"Created directory: {full_path}")
        else:
            dir_path = os.path.dirname(full_path)
            os.makedirs(dir_path, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write('')  # Empty file
            print(f"Created file: {full_path}")


def main() -> None:
    """Main entry point for the command-line interface."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Create project structures from text descriptions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  project-structure-creator structure.txt ~/Desktop/my_project
  project-structure-creator structure.txt C:\\Users\\username\\Documents\\my_project
  project-structure-creator --gui
  python -m project_structure_creator --gui
        """
    )
    
    parser.add_argument(
        "input_file", 
        nargs="?", 
        default="structure.txt",
        help="Input file containing the project structure (default: structure.txt)"
    )
    parser.add_argument(
        "output_dir", 
        nargs="?", 
        help="Output directory where the structure will be created (required for CLI mode)"
    )
    parser.add_argument(
        "--gui", 
        action="store_true",
        help="Launch the graphical user interface"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version="%(prog)s 0.1.0"
    )
    
    args = parser.parse_args()
    
    # Launch GUI if requested
    if args.gui:
        try:
            from .gui import run_gui
            run_gui()
            return
        except ImportError as e:
            print(f"Error: GUI dependencies not available: {e}")
            print("GUI requires tkinter which should be included with Python.")
            sys.exit(1)
    
    # CLI mode
    input_file = args.input_file
    output_dir = args.output_dir
    
    if not output_dir:
        print("Error: Output directory is required for CLI mode.")
        print(f"Usage: {sys.argv[0]} [input_file] [output_dir]")
        print(f"       {sys.argv[0]} --gui")
        sys.exit(1)

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        print(f"Usage: {sys.argv[0]} [input_file] [output_dir]")
        print(f"       {sys.argv[0]} --gui")
        sys.exit(1)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f if line.strip()]
        
        print(f"Reading structure from: {input_file}")
        print(f"Creating structure at: {output_dir}")
        print()
        
        create_structure(output_dir, lines)
        print(f"\n✅ Project structure created successfully at '{output_dir}/'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
