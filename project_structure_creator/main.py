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
    input_file = "structure.txt"
    output_dir = "output_project"
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        print("Usage: project-structure-creator [input_file] [output_dir]")
        sys.exit(1)
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f if line.strip()]
        
        create_structure(output_dir, lines)
        print(f"\nProject structure created successfully at '{output_dir}/'")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
