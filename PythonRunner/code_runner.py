import subprocess
import os
import threading
from typing import Callable, Optional

class CodeRunner:
    def __init__(self):
        self.running_process: Optional[subprocess.Popen] = None
        self.last_code: Optional[str] = None

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
            update_callback(f"An error occurred: {str(e)}", "normal")

    def handle_pip_command(self, code: str, update_callback: Callable[[str, str], None]):
        try:
            package_name = code.split()[2]
            if code.startswith('pip install'):
                process = subprocess.Popen(['pip', 'install', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            else:  # pip uninstall
                process = subprocess.Popen(['pip', 'uninstall', '-y', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                update_callback(f"Successfully {'installed' if 'install' in code else 'uninstalled'} {package_name}\n{stdout}", "normal")
            else:
                update_callback(f"Failed to {'install' if 'install' in code else 'uninstall'} {package_name}\n{stderr}", "normal")
        except Exception as e:
            update_callback(f"An error occurred while handling pip command: {str(e)}", "normal")

    def run_python_code(self, update_callback: Callable[[str, str], None]):
        try:
            command = ["python", "guiscript.py"]
            self.running_process = subprocess.Popen(
                command, cwd=os.getcwd(), shell=True, stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, universal_newlines=True
            )

            update_callback("Running Python script...", "normal")

            def update_result():
                try:
                    for line in self.running_process.stdout:
                        update_callback(line, "normal")
                    return_code = self.running_process.wait()
                    if return_code == 0:
                        update_callback("\nScript executed successfully.", "normal")
                    else:
                        update_callback(f"\nScript exited with error code {return_code}", "normal")
                except Exception as e:
                    update_callback(f"\nAn error occurred while running the script: {str(e)}", "normal")

            threading.Thread(target=update_result).start()
        except Exception as e:
            update_callback(f"An error occurred while starting the script: {str(e)}", "normal")