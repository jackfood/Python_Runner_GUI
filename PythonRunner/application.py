from gui import GUI
from code_runner import CodeRunner
from config import Config
import tkinter as tk

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.config = Config()
        self.code_runner = CodeRunner(self.root)
        self.gui = GUI(self.root, self.code_runner, self.config)

    def run(self):
        self.root.mainloop()