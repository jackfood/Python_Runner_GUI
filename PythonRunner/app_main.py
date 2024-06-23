import logging
from application import Application

def run_application():
    logging.basicConfig(level=logging.INFO)
    app = Application()
    app.run()

if __name__ == "__main__":
    run_application()