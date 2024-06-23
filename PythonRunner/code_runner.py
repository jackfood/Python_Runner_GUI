import subprocess
import os
import threading
from typing import Callable, Optional
from queue import Queue
import tkinter as tk

class CodeRunner:
    def __init__(self, root: tk.Tk):
        self.running_process: Optional[subprocess.Popen] = None
        self.last_code: Optional[str] = None
        self.output_queue = Queue()
        self.root = root

    def run_code(self, code: str, update_callback: Callable[[str, str], None]):
        self.last_code = code
        try:
            if self.running_process and self.running_process.poll() is None:
                self.running_process.kill()
            with open('guiscript.py', 'w') as file:
                file.write(code)
            if code.strip().startswith('pip install') or code.strip().startswith('pip uninstall'):
                self.handle_pip_command(code, update_callback)
            else:
                self.run_python_code(update_callback)
        except Exception as e:
            update_callback(f"An error occurred: {str(e)}\n", "normal")

    def handle_pip_command(self, code: str, update_callback: Callable[[str, str], None]):
        try:
            package_name = code.split()[2]
            if code.startswith('pip install'):
                process = subprocess.Popen(['pip', 'install', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)
            else:  # pip uninstall
                process = subprocess.Popen(['pip', 'uninstall', '-y', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)
            
            for line in process.stdout:
                update_callback(line, "normal")
            for line in process.stderr:
                update_callback(line, "normal")
            
            process.wait()
            if process.returncode == 0:
                update_callback(f"Successfully {'installed' if 'install' in code else 'uninstalled'} {package_name}\n", "normal")
            else:
                update_callback(f"Failed to {'install' if 'install' in code else 'uninstall'} {package_name}\n", "normal")
        except Exception as e:
            update_callback(f"An error occurred while handling pip command: {str(e)}\n", "normal")

    def run_python_code(self, update_callback: Callable[[str, str], None]):
        try:
            command = ["python", "guiscript.py"]
            self.running_process = subprocess.Popen(
                command, cwd=os.getcwd(), shell=True, stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, universal_newlines=True, bufsize=1
            )
            update_callback("Running Python script...\n", "normal")
            
            def stream_output():
                for line in self.running_process.stdout:
                    self.output_queue.put(line)
                return_code = self.running_process.wait()
                if return_code == 0:
                    self.output_queue.put("\nScript executed successfully.\n")
                else:
                    self.output_queue.put(f"\nScript exited with error code {return_code}\n")
                self.output_queue.put(None)  # Signal that we're done
            
            threading.Thread(target=stream_output).start()
            
            def check_output():
                while not self.output_queue.empty():
                    line = self.output_queue.get()
                    if line is None:
                        return
                    update_callback(line, "normal")
                self.root.after(100, check_output)
            
            self.root.after(100, check_output)
        except Exception as e:
            update_callback(f"An error occurred while starting the script: {str(e)}\n", "normal")