import sys
import os

# Add the PythonRunner folder to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
python_runner_dir = os.path.join(current_dir, 'PythonRunner')
sys.path.insert(0, python_runner_dir)  # Insert at the beginning of sys.path

from app_main import run_application

if __name__ == "__main__":
    run_application()