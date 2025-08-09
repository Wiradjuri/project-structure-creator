"""
GUI version of Project Structure Creator using tkinter
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
import sys
from pathlib import Path

# Import the main functionality
from .main import parse_structure, create_structure, validate_structure_input, StructureParseError


class ProjectStructureGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Structure Creator")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configure the root window
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="Project Structure Creator", 
            font=("Arial", 16, "bold")
        )
        title_label.grid(row=0, column=0, pady=10, sticky="ew")
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Project Structure Input", padding=10)
        input_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        input_frame.grid_columnconfigure(0, weight=1)
        
        # Buttons frame
        buttons_frame = ttk.Frame(input_frame)
        buttons_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        buttons_frame.grid_columnconfigure(1, weight=1)
        
        # Load file button
        load_btn = ttk.Button(buttons_frame, text="Load from File", command=self.load_file)
        load_btn.grid(row=0, column=0, padx=(0, 10))
        
        # Clear button
        clear_btn = ttk.Button(buttons_frame, text="Clear", command=self.clear_input)
        clear_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Validate button
        validate_btn = ttk.Button(buttons_frame, text="Validate", command=self.validate_input)
        validate_btn.grid(row=0, column=1, padx=(10, 0))
        
        # Text input area
        self.text_input = scrolledtext.ScrolledText(
            input_frame, 
            height=12, 
            wrap=tk.WORD,
            font=("Consolas", 10)
        )
        self.text_input.grid(row=1, column=0, sticky="nsew")
        input_frame.grid_rowconfigure(1, weight=1)
        
        # Add example text
        example_text = """Supported formats:

1. Simple indented:
project/
    src/
        main.py
        utils/
            config.py
    tests/
        test_main.py
    README.md

2. Tree format:
project/
├── src/
│   ├── main.py
│   └── utils/
│       └── config.py
├── tests/
│   └── test_main.py
└── README.md

3. Markdown list:
- project/
  - src/
    - main.py
    - utils/
      - config.py
  - tests/
    - test_main.py
  - README.md

4. JSON format:
{
  "project": {
    "src": ["main.py", "utils/config.py"],
    "tests": ["test_main.py"],
    "README.md": ""
  }
}"""
        self.text_input.insert("1.0", example_text)
        
        # Output frame
        output_frame = ttk.LabelFrame(main_frame, text="Output Directory", padding=10)
        output_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        output_frame.grid_columnconfigure(0, weight=1)
        
        # Output path frame
        path_frame = ttk.Frame(output_frame)
        path_frame.grid(row=0, column=0, sticky="ew")
        path_frame.grid_columnconfigure(0, weight=1)
        
        self.output_path = tk.StringVar(value=str(Path.home() / "Desktop"))
        path_entry = ttk.Entry(path_frame, textvariable=self.output_path)
        path_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        browse_btn = ttk.Button(path_frame, text="Browse", command=self.browse_output_dir)
        browse_btn.grid(row=0, column=1)
        
        # Action buttons frame
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=2, column=0, pady=10)
        
        # Generate button
        generate_btn = ttk.Button(
            action_frame, 
            text="Generate Project Structure", 
            command=self.generate_structure,
            style="Accent.TButton"
        )
        generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Preview button
        preview_btn = ttk.Button(action_frame, text="Preview", command=self.preview_structure)
        preview_btn.pack(side=tk.LEFT)
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=2, column=0, sticky="ew", padx=5, pady=2)
        
    def load_file(self):
        """Load structure from a text file"""
        file_path = filedialog.askopenfilename(
            title="Select Structure File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert("1.0", content)
                self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")
                
    def clear_input(self):
        """Clear the input text area"""
        self.text_input.delete("1.0", tk.END)
        self.status_var.set("Input cleared")
        
    def validate_input(self):
        """Validate the current input"""
        lines = self.get_structure_lines()
        if not lines:
            messagebox.showwarning("Warning", "Please enter a project structure to validate")
            return
            
        is_valid, error_msg = validate_structure_input(lines)
        if is_valid:
            messagebox.showinfo("Validation", "✅ Structure format is valid!")
            self.status_var.set("Structure validated successfully")
        else:
            messagebox.showerror("Validation Error", f"❌ Invalid structure format:\n\n{error_msg}")
            self.status_var.set("Validation failed")
        
    def browse_output_dir(self):
        """Browse for output directory"""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_path.set(directory)
            
    def get_structure_lines(self):
        """Get the structure lines from the text input"""
        content = self.text_input.get("1.0", tk.END)
        return [line.rstrip('\n') for line in content.split('\n') if line.strip()]
        
    def preview_structure(self):
        """Preview the structure that will be created"""
        try:
            lines = self.get_structure_lines()
            if not lines:
                messagebox.showwarning("Warning", "Please enter a project structure")
                return
                
            # Validate input first
            is_valid, error_msg = validate_structure_input(lines)
            if not is_valid:
                messagebox.showerror("Validation Error", f"Invalid structure format:\n\n{error_msg}")
                return
                
            output_dir = self.output_path.get()
            try:
                paths = parse_structure(lines)
            except StructureParseError as e:
                messagebox.showerror("Parse Error", f"Failed to parse structure:\n\n{e}")
                return
            except Exception as e:
                messagebox.showerror("Parse Error", f"Unexpected parsing error:\n\n{e}")
                return
                
            if not paths:
                messagebox.showwarning("Warning", "No valid structure found. Please check your input format.")
                return
                
            # Get the root folder name from the first path
            if paths:
                first_path = paths[0][0]
                root_folder = first_path.split(os.sep)[0] if os.sep in first_path else first_path
                project_path = os.path.join(output_dir, root_folder) if output_dir else root_folder
            else:
                project_path = output_dir or "output_project"
                
            # Create preview window
            preview_window = tk.Toplevel(self.root)
            preview_window.title("Structure Preview")
            preview_window.geometry("600x500")
            preview_window.transient(self.root)
            preview_window.grab_set()
            
            # Preview text
            preview_text = scrolledtext.ScrolledText(
                preview_window, 
                wrap=tk.WORD,
                font=("Consolas", 10)
            )
            preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            preview_content = f"📍 Project will be created at:\n{project_path}\n\n"
            preview_content += f"📊 Summary: {len([p for p in paths if p[1]])} directories, {len([p for p in paths if not p[1]])} files\n\n"
            preview_content += "📁 Structure preview:\n\n"
            
            # Build tree representation
            for i, (path, is_dir) in enumerate(paths):
                icon = "📁" if is_dir else "📄"
                # Add proper indentation based on path depth
                depth = path.count(os.sep)
                indent = "  " * depth
                name = os.path.basename(path) if os.sep in path else path
                preview_content += f"{indent}{icon} {name}\n"
                
            preview_text.insert("1.0", preview_content)
            preview_text.config(state=tk.DISABLED)
            
            # Add close button
            close_btn = ttk.Button(
                preview_window, 
                text="Close", 
                command=preview_window.destroy
            )
            close_btn.pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview structure: {e}")
            self.status_var.set("Preview failed")
            
    def generate_structure(self):
        """Generate the project structure"""
        try:
            lines = self.get_structure_lines()
            if not lines:
                messagebox.showwarning("Warning", "Please enter a project structure")
                return
                
            output_dir = self.output_path.get()
            if not output_dir:
                messagebox.showwarning("Warning", "Please specify an output directory")
                return
                
            # Validate input first
            is_valid, error_msg = validate_structure_input(lines)
            if not is_valid:
                messagebox.showerror("Validation Error", f"Invalid structure format:\n\n{error_msg}")
                return
                
            try:
                paths = parse_structure(lines)
            except StructureParseError as e:
                messagebox.showerror("Parse Error", f"Failed to parse structure:\n\n{e}")
                return
            except Exception as e:
                messagebox.showerror("Parse Error", f"Unexpected parsing error:\n\n{e}")
                return
                
            if not paths:
                messagebox.showwarning("Warning", "No valid structure found. Please check your input format.")
                return
                
            # Get the root folder name from the first path
            first_path = paths[0][0]
            root_folder = first_path.split(os.sep)[0] if os.sep in first_path else first_path
            project_path = os.path.join(output_dir, root_folder)
            
            # Check if the project directory already exists
            if os.path.exists(project_path):
                result = messagebox.askyesno(
                    "Directory Exists", 
                    f"Project directory '{project_path}' already exists.\n\nContinue? (Existing files will be preserved)"
                )
                if not result:
                    return
            else:
                # Confirm the creation location
                result = messagebox.askyesno(
                    "Confirm Creation", 
                    f"Create project structure at:\n{project_path}\n\nThis will create {len([p for p in paths if p[1]])} directories and {len([p for p in paths if not p[1]])} files."
                )
                if not result:
                    return
                    
            self.status_var.set("Generating structure...")
            self.root.update()
            
            try:
                create_structure(output_dir, lines)
                self.status_var.set(f"✅ Structure created successfully at: {project_path}")
                
                # Ask if user wants to open the directory
                result = messagebox.askyesno(
                    "Success", 
                    f"Project structure created successfully!\n\n📁 Location: {project_path}\n\nOpen the project directory?"
                )
                if result:
                    try:
                        if sys.platform == "win32":
                            os.startfile(project_path)
                        elif sys.platform == "darwin":
                            os.system(f"open '{project_path}'")
                        else:
                            os.system(f"xdg-open '{project_path}'")
                    except Exception as e:
                        messagebox.showwarning("Warning", f"Could not open directory: {e}")
                        
            except StructureParseError as e:
                messagebox.showerror("Structure Error", f"Failed to create structure:\n\n{e}")
                self.status_var.set("❌ Structure creation failed")
            except OSError as e:
                messagebox.showerror("File System Error", f"Failed to create files/directories:\n\n{e}")
                self.status_var.set("❌ File system error")
            except Exception as e:
                messagebox.showerror("Unexpected Error", f"An unexpected error occurred:\n\n{e}")
                self.status_var.set("❌ Unexpected error")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate structure: {e}")
            self.status_var.set("❌ Generation failed")


def run_gui():
    """Run the GUI application"""
    root = tk.Tk()
    app = ProjectStructureGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    run_gui()
