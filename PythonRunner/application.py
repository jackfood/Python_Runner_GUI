from gui import GUI
from code_runner import CodeRunner

class Application:
    def __init__(self):
        self.code_runner = CodeRunner()
        self.gui = GUI(self.code_runner)

    def run(self):
        self.gui.root.mainloop()