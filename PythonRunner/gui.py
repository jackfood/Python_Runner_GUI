import tkinter as tk
from tkinter import scrolledtext, Menu, filedialog, simpledialog, Toplevel, Listbox, messagebox
from typing import Callable
from code_runner import CodeRunner
from config import Config
import os

class GUI:
    def __init__(self, root: tk.Tk, code_runner: CodeRunner, config: Config):
        self.root = root
        self.code_runner = code_runner
        self.config = config
        self.setup_gui()


    def setup_gui(self):
        self.root.title("Python Code Runner Lite v1.7 - Refactored Code - Live Console Streaming")
        self.root.geometry("900x700")

        self.create_menus()
        self.create_code_entry()
        self.create_run_button()
        self.create_result_text()
        self.create_status_bar()


    def create_menus(self):
        menu_bar = Menu(self.root)
        self.root.config(menu=menu_bar)

        self.create_analysis_menu(menu_bar)
        menu_bar.add_command(label="List Python Scripts", command=self.list_python_scripts)
        self.create_gpt_prompt_menu(menu_bar)
        self.create_python_prompt_menu(menu_bar)

    def create_analysis_menu(self, menu_bar):
        analysis_menu = Menu(menu_bar)
        menu_bar.add_cascade(label="Data Analysis", menu=analysis_menu)
        analysis_menu.add_command(label="Data Visualization prompt generation", 
                                  command=self.process_excel_csv_option)
        analysis_menu.add_command(label="Data Analyse prompt generation", 
                                  command=self.process_python_prompt_Analyse_S1)

    def create_gpt_prompt_menu(self, menu_bar):
        gpt_prompt_menu = Menu(menu_bar)
        menu_bar.add_cascade(label="ChatGPT prompts", menu=gpt_prompt_menu)
        
        prompts = [
            ("Prompt Generator", 'prompt_generator'),
            ("Table Organizer", 'table_organizer'),
            ("Summarise Text", 'summarise_text'),
            ("AI writing assistant", 'ai_writing_assistant'),
            ("Unrestricted Opinion Prompt", 'unrestricted_opinion'),
            ("Flow and Cohesion of Sentence Improver", 'cohesion_and_engagement_improver'),
            ("Professional Writer", 'professional_writer')
        ]

        for label, prompt_key in prompts:
            gpt_prompt_menu.add_command(
                label=label, 
                command=lambda k=prompt_key: self.insert_code_into_entry(self.config.get_prompt(k))
            )

    def create_python_prompt_menu(self, menu_bar):
        python_prompt_menu = Menu(menu_bar)
        menu_bar.add_cascade(label="Python Prompts", menu=python_prompt_menu)
        
        prompts = [
            ("Python Prompt", 'python_prompt'),
            ("Python Code Optimization", 'python_optimise_prompt'),
            ("Mermaid Flow Diagram Prompt", 'visualization_mermaid')
        ]

        for label, prompt_key in prompts:
            python_prompt_menu.add_command(
                label=label, 
                command=lambda k=prompt_key: self.insert_code_into_entry(self.config.get_prompt(k))
            )

    def create_code_entry(self):
        code_label = tk.Label(self.root, text="Enter Python Code:")
        code_label.pack()

        code_frame = tk.Frame(self.root)
        code_frame.pack(fill=tk.BOTH, expand=True)

        self.code_entry = scrolledtext.ScrolledText(code_frame, height=15, width=70, wrap=tk.WORD, undo=True)
        self.code_entry.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def create_run_button(self):
        save_and_run_button = tk.Button(self.root, text="Run Code", command=self.save_and_run_python_code)
        save_and_run_button.pack()

    def create_result_text(self):
        self.result_text = scrolledtext.ScrolledText(self.root, height=15, width=70, bg="black", fg="white")
        self.result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.result_text.config(state=tk.DISABLED)

    def create_result_text(self):
        self.result_text = scrolledtext.ScrolledText(self.root, height=15, width=70, bg="black", fg="white")
        self.result_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.result_text.config(state=tk.DISABLED)

    def update_result_text(self, message: str, state: str):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, message)
        self.result_text.see(tk.END)
        self.result_text.config(state=tk.DISABLED)
        
        if "successfully" in message.lower():
            self.update_status("Code execution completed successfully.")
        elif "error" in message.lower():
            self.update_status("Code execution completed with errors.")
        else:
            self.update_status("Running...")

    def save_and_run_python_code(self):
        code = self.code_entry.get("1.0", "end-1c")
        if not code.strip():
            messagebox.showwarning("Empty Code", "Please enter some code before running.")
            return
        self.update_status("Running code...")
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        self.code_runner.run_code(code, self.update_result_text)

    def update_result_text(self, message: str, state: str):
        self.result_text.config(state="normal")
        self.result_text.insert(tk.END, message)
        self.result_text.see(tk.END)
        self.result_text.config(state=state)
        if "successfully" in message.lower():
            self.update_status("Code execution completed successfully.")
        elif "error" in message.lower():
            self.update_status("Code execution completed with errors.")
        else:
            self.update_status("Ready")

    def create_status_bar(self):
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self, message):
        self.status_bar.config(text=message)
        self.root.update_idletasks()

    def list_python_scripts(self):
        scripts_window = Toplevel(self.root)
        scripts_window.title("List of Python Scripts")
        scripts_window.geometry("400x600")
        
        script_listbox = Listbox(scripts_window)
        script_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scripts = [file for file in os.listdir() if file.endswith(".py")]
        if not scripts:
            messagebox.showinfo("No Scripts", "No Python scripts found in the current directory.")
            scripts_window.destroy()
            return

        for script in scripts:
            script_listbox.insert(tk.END, script)

        def on_script_selected():
            selected_index = script_listbox.curselection()
            if selected_index:
                selected_script = script_listbox.get(selected_index)
                try:
                    with open(selected_script, 'r') as file:
                        script_content = file.read()
                    self.code_entry.delete("1.0", tk.END)
                    self.code_entry.insert(tk.END, script_content)
                    self.root.clipboard_clear()
                    self.root.clipboard_append(script_content)
                    scripts_window.destroy()
                    self.update_status(f"Loaded script: {selected_script}")
                    self.save_and_run_python_code()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load script: {str(e)}")

        copy_button = tk.Button(scripts_window, text="Load and Run Script", command=on_script_selected)
        copy_button.pack(pady=10)

    def insert_code_into_entry(self, code: str):
        self.code_entry.delete("1.0", tk.END)
        # Remove leading and trailing whitespace and quotes
        code = code.strip().strip('"""').strip("'''")
        self.code_entry.insert(tk.END, code)
        self.update_status("Code inserted into editor")

    def create_gpt_prompt_menu(self, menu_bar):
        gpt_prompt_menu = Menu(menu_bar)
        menu_bar.add_cascade(label="ChatGPT prompts", menu=gpt_prompt_menu)
        
        prompts = [
            ("Prompt Generator", 'prompt_generator'),
            ("Table Organizer", 'table_organizer'),
            ("Summarise Text", 'summarise_text'),
            ("AI writing assistant", 'ai_writing_assistant'),
            ("Unrestricted Opinion Prompt", 'unrestricted_opinion'),
            ("Flow and Cohesion of Sentence Improver", 'cohesion_and_engagement_improver'),
            ("Professional Writer", 'professional_writer')
        ]

        for label, prompt_key in prompts:
            gpt_prompt_menu.add_command(
                label=label, 
                command=lambda k=prompt_key: self.insert_code_into_entry(self.config.get_prompt(k))
            )

    def create_python_prompt_menu(self, menu_bar):
        python_prompt_menu = Menu(menu_bar)
        menu_bar.add_cascade(label="Python Prompts", menu=python_prompt_menu)
        
        prompts = [
            ("Python Prompt", 'python_prompt'),
            ("Python Code Optimization", 'python_optimise_prompt'),
            ("Mermaid Flow Diagram Prompt", 'visualization_mermaid')
        ]

        for label, prompt_key in prompts:
            python_prompt_menu.add_command(
                label=label, 
                command=lambda k=prompt_key: self.insert_code_into_entry(self.config.get_prompt(k))
            )

    def process_excel_csv_option(self):
        code = f'''{self.config.get_prompt('excel_csv_prompt')}'''
        self.insert_code_into_entry(code)
        self.save_and_run_python_code()
        print('excel_csv_prompt_option selected')

    def process_python_prompt_Analyse_S1(self):
        code = f'''{self.config.get_prompt('process_python_prompt_Analyse_S1')}'''
        self.insert_code_into_entry(code)
        self.save_and_run_python_code()
        print('process_python_prompt_Analyse_S1 selected')

    # Add other methods as needed