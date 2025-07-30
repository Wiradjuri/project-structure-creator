import os

def parse_structure(lines):
    stack = []
    paths = []

    for line in lines:
        stripped = line.lstrip()
        depth = (len(line) - len(stripped)) // 4  # 4 spaces per indent or adjust to your needs
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

def create_structure(base_path, structure_lines):
    paths = parse_structure(structure_lines)
    for path, is_dir in paths:
        full_path = os.path.join(base_path, path)
        if is_dir:
            os.makedirs(full_path, exist_ok=True)
        else:
            dir_path = os.path.dirname(full_path)
            os.makedirs(dir_path, exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write('')  # Empty file

if __name__ == "__main__":
    input_file = "structure.txt"   # User-provided file
    output_dir = "test_generated_project"  # Where to build the project

    with open(input_file, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f if line.strip()]

    create_structure(output_dir, lines)
    print(f"Project structure created at {output_dir}/")
