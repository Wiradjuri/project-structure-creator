"""
Main module for Project Structure Creator
"""

import os
import sys
import re
from typing import List, Tuple


class StructureParseError(Exception):
    """Custom exception for structure parsing errors"""
    pass


def parse_structure(lines: List[str]) -> List[Tuple[str, bool]]:
    """
    Parse a list of lines representing a project structure.
    Supports multiple formats: indented, tree-style, JSON, YAML, Markdown lists, and more.
    
    Args:
        lines: List of strings representing the project structure
        
    Returns:
        List of tuples (path, is_directory)
        
    Raises:
        StructureParseError: If the input format cannot be parsed
    """
    if not lines or all(not line.strip() for line in lines):
        raise StructureParseError("No valid input provided")
    
    # Clean and filter lines
    clean_lines = [line.rstrip() for line in lines if line.strip()]
    
    try:
        import json
    except ImportError:
        json = None
    
    try:
        import yaml
    except ImportError:
        yaml = None

    stack = []
    paths = []
    
    # Join all lines to detect format
    joined = '\n'.join(clean_lines).strip()
    
    # Try JSON format
    if json and (joined.startswith('{') or joined.startswith('[')):
        try:
            return _parse_json_structure(joined)
        except Exception as e:
            raise StructureParseError(f"Invalid JSON format: {e}")
    
    # Try YAML format
    if yaml and (':' in joined and not any(line.strip().startswith('├') or line.strip().startswith('└') for line in clean_lines)):
        try:
            return _parse_yaml_structure(joined, yaml)
        except Exception as e:
            # Don't raise error here, continue to other formats
            pass
    
    # Try Markdown list format
    if any(re.match(r'^\s*[-*+]\s+', line) for line in clean_lines):
        try:
            return _parse_markdown_structure(clean_lines)
        except Exception as e:
            raise StructureParseError(f"Invalid Markdown list format: {e}")
    
    # Try filesystem listing format (like `find` or `ls -R` output)
    if any(line.endswith(':') for line in clean_lines):
        try:
            return _parse_filesystem_listing(clean_lines)
        except Exception as e:
            # Continue to tree/indented format
            pass
    
    # Try tree-style or indented format
    try:
        return _parse_tree_or_indented(clean_lines)
    except Exception as e:
        raise StructureParseError(f"Could not parse structure format: {e}")


def _parse_json_structure(json_text: str) -> List[Tuple[str, bool]]:
    """Parse JSON structure format"""
    import json
    paths = []
    
    def walk_json(obj, prefix=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                current_path = os.path.join(prefix, k) if prefix else k
                if isinstance(v, (dict, list)) and v:
                    paths.append((current_path, True))
                    walk_json(v, current_path)
                elif isinstance(v, list) and not v:
                    paths.append((current_path, True))
                else:
                    # Treat as file if it has extension or explicit value
                    if '.' in k or (isinstance(v, str) and v):
                        if isinstance(v, str) and v != k:
                            paths.append((os.path.join(current_path, v), False))
                        else:
                            paths.append((current_path, False))
                    else:
                        paths.append((current_path, True))
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, str):
                    is_dir = '.' not in item
                    full_path = os.path.join(prefix, item) if prefix else item
                    paths.append((full_path, is_dir))
                else:
                    walk_json(item, prefix)
    
    data = json.loads(json_text)
    walk_json(data)
    return paths


def _parse_yaml_structure(yaml_text: str, yaml_module) -> List[Tuple[str, bool]]:
    """Parse YAML structure format"""
    paths = []
    
    def walk_yaml(obj, prefix=""):
        if isinstance(obj, dict):
            for k, v in obj.items():
                current_path = os.path.join(prefix, k) if prefix else k
                if isinstance(v, (dict, list)) and v:
                    paths.append((current_path, True))
                    walk_yaml(v, current_path)
                elif isinstance(v, list) and not v:
                    paths.append((current_path, True))
                else:
                    if '.' in k or (isinstance(v, str) and v):
                        if isinstance(v, str) and v != k:
                            paths.append((os.path.join(current_path, v), False))
                        else:
                            paths.append((current_path, False))
                    else:
                        paths.append((current_path, True))
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, str):
                    is_dir = '.' not in item
                    full_path = os.path.join(prefix, item) if prefix else item
                    paths.append((full_path, is_dir))
                else:
                    walk_yaml(item, prefix)
    
    data = yaml_module.safe_load(yaml_text)
    walk_yaml(data)
    return paths


def _parse_markdown_structure(lines: List[str]) -> List[Tuple[str, bool]]:
    """Parse Markdown list format"""
    paths = []
    stack = []
    
    for line in lines:
        # Match markdown list items: - item, * item, + item
        match = re.match(r'^(\s*)[-*+]\s+(.+)$', line)
        if not match:
            continue
            
        indent, name = match.groups()
        depth = len(indent) // 2  # Assume 2 spaces per level
        
        # Clean the name
        name = name.strip()
        if not name:
            continue
            
        # Remove markdown formatting
        name = re.sub(r'`([^`]+)`', r'\1', name)  # Remove backticks
        name = re.sub(r'\*\*([^*]+)\*\*', r'\1', name)  # Remove bold
        name = re.sub(r'\*([^*]+)\*', r'\1', name)  # Remove italic
        
        # Adjust stack to current depth
        while len(stack) > depth:
            stack.pop()
            
        # Determine if it's a directory
        is_directory = not _has_file_extension(name)
        
        # Build path
        if stack:
            current_path = os.path.join(*stack, name)
        else:
            current_path = name
            
        paths.append((current_path, is_directory))
        
        if is_directory:
            stack.append(name)
    
    return paths


def _parse_filesystem_listing(lines: List[str]) -> List[Tuple[str, bool]]:
    """Parse filesystem listing format (like find or ls -R output)"""
    paths = []
    current_dir = ""
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Directory headers end with ':'
        if line.endswith(':'):
            current_dir = line[:-1]
            if current_dir and current_dir != '.':
                paths.append((current_dir, True))
        else:
            # File or directory in current directory
            if current_dir:
                full_path = os.path.join(current_dir, line)
            else:
                full_path = line
                
            is_directory = not _has_file_extension(line)
            paths.append((full_path, is_directory))
    
    return paths


def _parse_tree_or_indented(lines: List[str]) -> List[Tuple[str, bool]]:
    """Parse tree-style or simple indented format"""
    stack = []
    paths = []
    
    for line in lines:
        if not line.strip():
            continue
            
        depth = 0
        name = ""
        
        # Tree-style format
        if '├──' in line or '└──' in line or '│' in line:
            # Count indentation for tree format
            before_content = re.match(r'^(\s*[│├└─\s]*)', line)
            if before_content:
                prefix = before_content.group(1)
                # Count depth based on tree symbols
                depth = prefix.count('├') + prefix.count('└')
                if '├──' in line:
                    name = line.split('├──', 1)[1].strip()
                elif '└──' in line:
                    name = line.split('└──', 1)[1].strip()
                else:
                    # Line with just │ or other tree chars, skip
                    continue
            else:
                continue
        else:
            # Simple indented format
            stripped = line.lstrip()
            if len(line) == len(stripped):
                depth = 0
            else:
                # Support both tabs and spaces
                leading = line[:len(line) - len(stripped)]
                if '\t' in leading:
                    depth = leading.count('\t')
                else:
                    depth = len(leading) // 4  # Assume 4 spaces per level
            name = stripped.strip()
        
        # Clean the name
        name = _clean_name(name)
        if not name:
            continue

        # Adjust stack to current depth
        while len(stack) > depth:
            stack.pop()

        # Determine if it's a directory
        is_directory = not _has_file_extension(name)
        
        # Build the full path
        if stack:
            current_path = os.path.join(*stack, name)
        else:
            current_path = name
            
        paths.append((current_path, is_directory))
        
        # Add to stack if it's a directory
        if is_directory:
            stack.append(name)

    return paths


def _clean_name(name: str) -> str:
    """Clean and normalize file/directory names"""
    if not name:
        return ""
        
    # Remove comments and descriptions
    for separator in ['–', ' #', ' //']:
        if separator in name:
            name = name.split(separator)[0].strip()
    
    # Remove trailing slashes/backslashes
    name = name.rstrip('/\\')
    
    # Remove quotes
    name = name.strip('"\'')
    
    return name.strip()


def _has_file_extension(name: str) -> bool:
    """Check if a name has a file extension"""
    # Known file extensions
    file_extensions = {
        '.txt', '.md', '.py', '.js', '.ts', '.html', '.css', '.json', '.xml', '.yml', '.yaml',
        '.java', '.kt', '.swift', '.cpp', '.c', '.h', '.cs', '.php', '.rb', '.go', '.rs',
        '.gradle', '.pro', '.properties', '.manifest', '.gitignore', '.dockerfile',
        '.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.pdf', '.zip', '.tar', '.gz'
    }
    
    name_lower = name.lower()
    
    # Check for known extensions
    for ext in file_extensions:
        if name_lower.endswith(ext):
            return True
    
    # Check for files with dots but unknown extensions
    if '.' in name and not name.startswith('.'):
        parts = name.split('.')
        if len(parts) > 1 and parts[-1]:  # Has extension and it's not empty
            return True
    
    # Special cases for files without extensions
    special_files = {
        'readme', 'license', 'changelog', 'makefile', 'dockerfile', 'gemfile',
        'rakefile', 'gulpfile', 'gruntfile', 'package-lock', 'yarn'
    }
    
    return name_lower in special_files


def create_structure(base_path: str, structure_lines: List[str]) -> None:
    """
    Create the project structure based on the parsed lines.
    
    Args:
        base_path: Base directory where the structure will be created
        structure_lines: List of strings representing the structure
        
    Raises:
        StructureParseError: If the structure cannot be parsed
        OSError: If file/directory creation fails
    """
    try:
        paths = parse_structure(structure_lines)
    except StructureParseError:
        raise
    except Exception as e:
        raise StructureParseError(f"Unexpected error parsing structure: {e}")
    
    if not paths:
        raise StructureParseError("No valid structure found")
    
    created_dirs = set()
    created_files = []
    
    try:
        for path, is_dir in paths:
            full_path = os.path.join(base_path, path)
            
            if is_dir:
                if full_path not in created_dirs:
                    os.makedirs(full_path, exist_ok=True)
                    created_dirs.add(full_path)
                    print(f"Created directory: {full_path}")
            else:
                dir_path = os.path.dirname(full_path)
                if dir_path and dir_path not in created_dirs:
                    os.makedirs(dir_path, exist_ok=True)
                    created_dirs.add(dir_path)
                
                # Only create file if it doesn't exist
                if not os.path.exists(full_path):
                    with open(full_path, 'w', encoding='utf-8') as f:
                        f.write('')  # Empty file
                    created_files.append(full_path)
                    print(f"Created file: {full_path}")
                else:
                    print(f"File already exists, skipped: {full_path}")
                    
    except OSError as e:
        raise OSError(f"Failed to create structure: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error creating structure: {e}")


def validate_structure_input(lines: List[str]) -> Tuple[bool, str]:
    """
    Validate structure input and provide helpful feedback.
    
    Args:
        lines: List of strings representing the structure
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not lines:
        return False, "No input provided"
    
    # Check if all lines are empty
    clean_lines = [line.strip() for line in lines if line.strip()]
    if not clean_lines:
        return False, "All lines are empty"
    
    # Check for obviously invalid content
    if len(clean_lines) == 1 and not any(char in clean_lines[0] for char in ['/', '\\', '{', '[', '-', '├', '└']):
        return False, "Input appears to be plain text, not a structure format"
    
    # Try to parse and catch specific errors
    try:
        paths = parse_structure(lines)
        if not paths:
            return False, "No valid structure items found"
        return True, ""
    except StructureParseError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Unknown parsing error: {e}"


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
