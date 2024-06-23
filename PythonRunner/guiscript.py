import pandas as pd
from dotenv import load_dotenv
from langchain_groq.chat_models import ChatGroq
from pandasai import Agent
import os
from tkinter import Tk, Label, Entry, Button, Text, END, NORMAL, DISABLED, StringVar, OptionMenu
from tkinter.filedialog import askopenfilename

# Load environment variables from .env file at the start
load_dotenv()

# Create the main window
window = Tk()
window.title("PandasAI Chat")

def select_file():
    file_path = askopenfilename(filetypes=[("CSV and Excel Files", "*.csv;*.xlsx")])
    if file_path:
        global df
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".xlsx"):
            df = pd.read_excel(file_path)
        else:
            result_text.insert(END, "Invalid file format. Please select a CSV or XLSX file.\n")
            return
        
        global agent
        if chat_model.get() == "Groq":
            llm = ChatGroq(
                model_name="mixtral-8x7b-32768",
                api_key=os.getenv("GROQ_API_KEY")  # Fetch the GROQ_API_KEY from .env
            )
            agent = Agent(df, llm=llm)  # Pass llm to Agent if using Groq model
        else:
            agent = Agent(df)
        
        result_text.insert(END, "File loaded successfully. You can now ask questions.\n")
        question_entry.config(state=NORMAL)
        submit_button.config(state=NORMAL)

def ask_question():
    question = question_entry.get()
    if question:
        result_text.insert(END, f"Question: {question}\n")
        try:
            response = agent.chat(question)
            result_text.insert(END, f"Response: {response}\n")
        except Exception as e:
            result_text.insert(END, f"An error occurred: {str(e)}\n")
        question_entry.delete(0, END)

# Create and pack the widgets
file_button = Button(window, text="Select File", command=select_file)
file_button.pack()

chat_model = StringVar(window)
chat_model.set("Default")  # Default value
chat_model_label = Label(window, text="Select Chat Model:")
chat_model_label.pack()
chat_model_dropdown = OptionMenu(window, chat_model, "Default", "Groq")
chat_model_dropdown.pack()

question_label = Label(window, text="Enter your question:")
question_label.pack()

question_entry = Entry(window, width=50, state=DISABLED)
question_entry.pack()

submit_button = Button(window, text="Submit", command=ask_question, state=DISABLED)
submit_button.pack()

result_text = Text(window, height=20, width=80)
result_text.pack()

# No need to manually set PANDASAI_API_KEY here since it's loaded from .env
# Start the main event loop
window.mainloop()