"""
GUI version of Project Structure Creator using tkinter
"""

import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
import os
import sys
from pathlib import Path

# Import the main functionality
from .main import parse_structure, create_structure


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
        example_text = """project/
    src/
        main.py
        models/
            data.py
            user.py
        utils/
            config.py
            helpers.py
    tests/
        test_main.py
        test_utils.py
    docs/
        README.md
        API.md
    requirements.txt
    setup.py"""
        self.text_input.insert("1.0", example_text)
        
        # Output frame
        output_frame = ttk.LabelFrame(main_frame, text="Output Directory", padding=10)
        output_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        output_frame.grid_columnconfigure(0, weight=1)
        
        # Output path frame
        path_frame = ttk.Frame(output_frame)
        path_frame.grid(row=0, column=0, sticky="ew")
        path_frame.grid_columnconfigure(0, weight=1)
        
        self.output_path = tk.StringVar(value=str(Path.home() / "Desktop" / "generated_project"))
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
                
            paths = parse_structure(lines)
            
            # Create preview window
            preview_window = tk.Toplevel(self.root)
            preview_window.title("Structure Preview")
            preview_window.geometry("500x400")
            
            # Preview text
            preview_text = scrolledtext.ScrolledText(preview_window, wrap=tk.WORD)
            preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            preview_content = "Files and directories that will be created:\n\n"
            for path, is_dir in paths:
                icon = "📁" if is_dir else "📄"
                preview_content += f"{icon} {path}\n"
                
            preview_text.insert("1.0", preview_content)
            preview_text.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview structure: {e}")
            
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
                
            # Ask for confirmation if directory exists
            if os.path.exists(output_dir):
                result = messagebox.askyesno(
                    "Directory Exists", 
                    f"Directory '{output_dir}' already exists. Continue?"
                )
                if not result:
                    return
                    
            self.status_var.set("Generating structure...")
            self.root.update()
            
            # Create the structure
            create_structure(output_dir, lines)
            
            self.status_var.set(f"Structure created successfully at: {output_dir}")
            
            # Ask if user wants to open the directory
            result = messagebox.askyesno(
                "Success", 
                f"Project structure created successfully!\n\nOpen the directory?"
            )
            if result:
                if sys.platform == "win32":
                    os.startfile(output_dir)
                elif sys.platform == "darwin":
                    os.system(f"open '{output_dir}'")
                else:
                    os.system(f"xdg-open '{output_dir}'")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate structure: {e}")
            self.status_var.set("Error occurred")


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
